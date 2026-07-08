"""
apply_change_handler.py

Applies an approved vault-qa change proposal by running the change-management skill as an
agentic, tool-using Claude session that edits vault files directly on disk, then opens a
pull request for a human to review. Never merges the PR. Never closes the originating issue.
Never edits main directly -- every change lands on a fresh branch.

Triggered only when a human with write access to this repo adds the 'approved' label to an
issue that already carries 'status:possible-change' (see
.github/workflows/vault-qa-apply-change.yml). Adding a label requires repo write/triage
permission, so -- unlike vault-qa's Q&A workflow, which anyone who can comment can trigger --
this cannot be set off by an arbitrary external commenter or agent. That's the deliberate
approval gate: vault-qa can *propose*, only a human with real repo access can make this run.

Safety model, in order of what actually enforces it (not just what the prompt asks for):
  1. The agent is given exactly three tools: read_file, edit_file, finish. There is no
     create-file, delete-file, or shell tool, so it cannot touch anything outside ordinary
     text edits to files that already exist.
  2. Every read_file/edit_file call is checked against ALLOWED_EDIT_FILES /
     ALLOWED_EDIT_GLOB in code, before the filesystem is touched -- not just described in the
     system prompt. A path outside the vault's content set is rejected by the tool itself.
  3. Before anything is committed, verify_only_allowed_files_changed() independently re-checks
     `git status --porcelain` against the same allowlist. If anything unexpected shows up as
     changed, the run aborts without committing, pushing, or opening a PR.
  4. The agentic loop has a hard turn ceiling (MAX_TOOL_TURNS). If the model doesn't call
     `finish` before that, the run aborts -- no partial branch, no partial PR.
  5. The result is always a pull request, never a direct commit to main, and this script never
     merges it or closes the originating issue.

Env vars required (all set by the workflow):
  ANTHROPIC_API_KEY  - Claude API key
  GITHUB_TOKEN       - provided automatically by GitHub Actions (needs contents:write,
                       pull-requests:write, issues:write -- see workflow permissions)
  REPO               - "owner/repo"
  ISSUE_NUMBER       - the issue that got the 'approved' label
  BASE_BRANCH        - the branch to open the PR against (the repo's default branch)
"""

import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import requests
from anthropic import Anthropic

VAULT_ROOT = Path(".")
CHANGE_MGMT_SKILL_PATH = VAULT_ROOT / "00-pipeline-skills" / "change-management" / "SKILL.md"
CHANGE_LOG_PATH = VAULT_ROOT / "06-change-log.md"
BOT_LOGIN = "github-actions[bot]"

# The exact set of files change-management is allowed to touch, per its own SKILL.md (Section
# "How to do it", steps 4-9). Anything outside this set -- pipeline instructions, workflows,
# scripts, READMEs -- is off-limits no matter what the model decides mid-run.
ALLOWED_EDIT_FILES = {
    "01-requirements-structured-v1.md",
    "02-scope-and-context-v1.md",
    "03-product-backlog-v1.md",
    "05-traceability-matrix.md",
    "06-change-log.md",
    "00-project-home.md",
}
ALLOWED_EDIT_GLOB_PREFIX = "04-speckit-specs" + os.sep

MAX_TOOL_TURNS = 40  # hard ceiling on the agentic loop -- abort rather than run away on cost


def is_path_allowed(path_str: str) -> bool:
    """True only for existing files inside the vault's content set. Resolves the path first so
    '..' tricks or absolute paths can't escape VAULT_ROOT."""
    try:
        root = VAULT_ROOT.resolve()
        full = (VAULT_ROOT / path_str).resolve()
    except Exception:
        return False
    if root != full and root not in full.parents:
        return False
    rel = os.path.relpath(full, root)
    if rel in ALLOWED_EDIT_FILES:
        return True
    if rel.startswith(ALLOWED_EDIT_GLOB_PREFIX) and rel.endswith(".md"):
        return True
    return False


TOOLS = [
    {
        "name": "read_file",
        "description": (
            "Read the full current contents of a vault file, given its path relative to the "
            "repo root. You must read a file before editing it. Only files inside the vault's "
            "content set can be read this way; anything else is rejected."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "edit_file",
        "description": (
            "Make a surgical edit to an existing vault file: replace exactly one occurrence of "
            "old_string with new_string. old_string must match the file's current content "
            "exactly, including whitespace, and must be long/unique enough to identify a "
            "single location in the file -- if it matches more than once, or not at all, the "
            "edit is rejected and you should re-read the file and try again with a more "
            "specific match. This tool can only edit files that already exist inside the "
            "vault's content set; it cannot create new files."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_string": {"type": "string"},
                "new_string": {"type": "string"},
            },
            "required": ["path", "old_string", "new_string"],
        },
    },
    {
        "name": "finish",
        "description": (
            "Call this exactly once, when -- and only when -- every materially affected item "
            "has been updated and the change log entry has been written, matching the skill's "
            "own 'Output summary' section. Ends the session."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": (
                        "Plain-text summary: CHG-ID, items reviewed but left unchanged (with "
                        "why), and any follow-up actions Mohamed needs to take -- e.g. writing "
                        "a spec for a newly-unblocked story."
                    ),
                },
                "files_edited": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Every file path actually edited, relative to the repo root.",
                },
            },
            "required": ["summary", "files_edited"],
        },
    },
]


def execute_tool(name: str, tool_input: dict) -> tuple[str, bool]:
    """Returns (result_text, is_error)."""
    try:
        if name == "read_file":
            path = tool_input["path"]
            if not is_path_allowed(path):
                return f"ERROR: '{path}' is outside the allowed vault content set.", True
            full = VAULT_ROOT / path
            if not full.exists():
                return f"ERROR: '{path}' does not exist. This tool cannot create new files.", True
            return full.read_text(encoding="utf-8"), False

        if name == "edit_file":
            path = tool_input["path"]
            if not is_path_allowed(path):
                return f"ERROR: '{path}' is outside the allowed vault content set -- edit rejected.", True
            full = VAULT_ROOT / path
            if not full.exists():
                return f"ERROR: '{path}' does not exist.", True
            text = full.read_text(encoding="utf-8")
            old, new = tool_input["old_string"], tool_input["new_string"]
            count = text.count(old)
            if count == 0:
                return "ERROR: old_string not found in the file -- re-read it, it may not match exactly.", True
            if count > 1:
                return f"ERROR: old_string matches {count} locations, not unique -- add more surrounding context.", True
            full.write_text(text.replace(old, new, 1), encoding="utf-8")
            return f"OK: edited {path}", False

        if name == "finish":
            return "OK", False

        return f"ERROR: unknown tool '{name}'", True
    except Exception as e:
        return f"ERROR: {e}", True


def run_agent_loop(client: Anthropic, system_prompt: str, user_message: str) -> dict | None:
    """Runs the tool-use loop until `finish` is called or MAX_TOOL_TURNS is exhausted. Returns
    the finish tool's input dict, or None if it never finished cleanly."""
    messages = [{"role": "user", "content": user_message}]

    for _ in range(MAX_TOOL_TURNS):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})

        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
        if not tool_use_blocks:
            # Model stopped without calling any tool, including finish -- incomplete, not success.
            return None

        tool_results = []
        finished = None
        for block in tool_use_blocks:
            result_text, is_error = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_text,
                "is_error": is_error,
            })
            if block.name == "finish" and not is_error:
                finished = block.input

        messages.append({"role": "user", "content": tool_results})
        if finished is not None:
            return finished

    return None


def get_next_chg_number() -> str:
    if not CHANGE_LOG_PATH.exists():
        return "CHG-001"
    text = CHANGE_LOG_PATH.read_text(encoding="utf-8")
    nums = [int(n) for n in re.findall(r"CHG-(\d+)", text)]
    nxt = (max(nums) + 1) if nums else 1
    return f"CHG-{nxt:03d}"


def get_issue(repo: str, issue_number: str, token: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}",
                                       "Accept": "application/vnd.github+json"})
    resp.raise_for_status()
    return resp.json()


def get_comments(repo: str, issue_number: str, token: str) -> list[dict]:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}",
                                       "Accept": "application/vnd.github+json"})
    resp.raise_for_status()
    return resp.json()


def find_latest_proposal_comment(comments: list[dict]) -> str | None:
    for c in reversed(comments):
        if c["user"]["login"] == BOT_LOGIN and "STATUS: proposed_change" in c["body"]:
            return c["body"]
    return None


def post_comment(repo: str, issue_number: str, token: str, body: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    resp = requests.post(url, headers={"Authorization": f"Bearer {token}",
                                        "Accept": "application/vnd.github+json"},
                          json={"body": body})
    resp.raise_for_status()


def open_pull_request(repo: str, token: str, branch: str, base: str, title: str, body: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/pulls"
    resp = requests.post(url, headers={"Authorization": f"Bearer {token}",
                                        "Accept": "application/vnd.github+json"},
                          json={"title": title, "head": branch, "base": base, "body": body})
    resp.raise_for_status()
    return resp.json()


def run_git(*args: str) -> None:
    subprocess.run(["git", *args], check=True)


def configure_git_identity() -> None:
    run_git("config", "user.email", "vault-qa-bot@users.noreply.github.com")
    run_git("config", "user.name", "vault-qa-bot")


def verify_only_allowed_files_changed() -> list[str]:
    """Independently re-checks git's own view of what changed against the same allowlist the
    tools enforced, as a second, unrelated safety net before anything gets committed."""
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
    changed, disallowed = [], []
    for line in result.stdout.splitlines():
        path = line[3:].strip().strip('"')
        if is_path_allowed(path):
            changed.append(path)
        else:
            disallowed.append(path)
    if disallowed:
        raise RuntimeError(
            f"Refusing to commit: file(s) outside the allowed vault content set were touched: "
            f"{disallowed}. No branch created, nothing pushed."
        )
    return changed


def main() -> None:
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]
    base_branch = os.environ.get("BASE_BRANCH", "main")

    issue = get_issue(repo, issue_number, token)
    labels = [l["name"] for l in issue.get("labels", [])]
    if "status:possible-change" not in labels:
        post_comment(
            repo, issue_number, token,
            "STATUS: apply_change_skipped\n\nThis issue doesn't carry `status:possible-change`, "
            "so there's no pending vault-qa proposal to apply. No action taken.",
        )
        return

    comments = get_comments(repo, issue_number, token)
    proposal_text = find_latest_proposal_comment(comments)
    if not proposal_text:
        post_comment(
            repo, issue_number, token,
            "STATUS: apply_change_failed\n\nCould not find a vault-qa change-proposal comment "
            "on this issue to apply. No action taken.",
        )
        return

    chg_id = get_next_chg_number()
    skill_instructions = CHANGE_MGMT_SKILL_PATH.read_text(encoding="utf-8")

    system_prompt = (
        skill_instructions
        + "\n\n---\n\nYou are running unattended in a GitHub Action, after a human with write "
        + "access to this repo added the 'approved' label to the issue below -- that label is "
        + "the approval this skill normally waits for. You have exactly three tools: "
        + "read_file, edit_file, and finish. You may ONLY read and edit files inside the "
        + "vault's content set (01/02/03/05/06-*.md, 00-project-home.md, and existing files "
        + "under 04-speckit-specs/) -- anything else is rejected by the tool itself, not just "
        + "advised against. You cannot create new files; only edit ones that already exist. If "
        + "the change genuinely requires a brand-new spec file, note that as a follow-up action "
        + "in your finish summary instead, exactly as the skill's own rules already say for new "
        + "requirements (flag it, don't auto-generate it).\n\n"
        + f"Assigned CHG-ID for this change: {chg_id}\n"
        + f"Today's date: {date.today().isoformat()}\n"
    )

    user_message = (
        "Apply this approved change. It originates from a vault-qa Mode B change proposal "
        "posted as a GitHub Issue comment, not yet in change-management's own CHG-record "
        "field names -- translate it yourself, the fields map directly: Affected IDs -> "
        "Affected item, Current value -> Old value, Proposed new value -> New value, Reason -> "
        "Reason, Source -> Triggered by. Infer Change type from context. Only fill in Resolves "
        "OQ if the proposal or issue explicitly says this resolves an open question; otherwise "
        "use '—'.\n\n"
        f"--- Original GitHub Issue #{issue_number}: {issue['title']} ---\n{issue['body']}\n\n"
        f"--- vault-qa's proposal comment (draft, unprocessed) ---\n{proposal_text}\n"
    )

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    result = run_agent_loop(client, system_prompt, user_message)

    if result is None:
        post_comment(
            repo, issue_number, token,
            f"STATUS: apply_change_failed\n\nThe automated change-management run for {chg_id} "
            f"did not finish within its turn limit, or stopped without calling `finish`. No "
            f"branch was created, nothing was changed. This needs a manual look, or try "
            f"removing and re-adding the `approved` label to retry.",
        )
        return

    try:
        changed_files = verify_only_allowed_files_changed()
    except RuntimeError as e:
        post_comment(
            repo, issue_number, token,
            f"STATUS: apply_change_aborted\n\n{e}\n\nThis is a safety abort, not expected "
            f"behaviour -- worth a look before retrying.",
        )
        return

    if not changed_files:
        post_comment(
            repo, issue_number, token,
            f"STATUS: apply_change_noop\n\nThe change-management run for {chg_id} finished "
            f"without editing any file.\n\n{result.get('summary', '')}",
        )
        return

    branch = f"chg/{chg_id.lower()}"
    configure_git_identity()
    run_git("checkout", "-b", branch)
    run_git("add", *changed_files)
    run_git("commit", "-m", f"{chg_id}: {issue['title']}")
    run_git("push", "-u", "origin", branch)

    pr = open_pull_request(
        repo, token, branch, base_branch,
        title=f"{chg_id}: {issue['title']}",
        body=(
            f"Automated change-management run for **{chg_id}**, applied after the `approved` "
            f"label was added to #{issue_number}.\n\n"
            f"{result.get('summary', '')}\n\n"
            f"**Files changed:** {', '.join(result.get('files_edited', changed_files))}\n\n"
            f"---\n\nThis PR was generated automatically. Nothing has been merged. Review the "
            f"diff like any other PR before merging."
        ),
    )

    post_comment(
        repo, issue_number, token,
        f"STATUS: apply_change_pr_opened\n\n{chg_id} has been applied on a new branch and a "
        f"pull request is open for review: {pr['html_url']}\n\nNothing has been merged into "
        f"{base_branch}. Review the diff before merging.",
    )


if __name__ == "__main__":
    main()
