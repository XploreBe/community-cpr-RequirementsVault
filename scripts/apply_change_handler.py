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
from datetime import date
from pathlib import Path

from anthropic import Anthropic

from github_api import (
    BOT_LOGIN,
    STATUS_LINES,
    get_comments,
    get_issue,
    open_pull_request,
    post_comment,
)

VAULT_ROOT = Path(".")
CHANGE_MGMT_SKILL_PATH = VAULT_ROOT / "00-pipeline-skills" / "change-management" / "SKILL.md"
CHANGE_LOG_PATH = VAULT_ROOT / "06-change-log.md"

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
            # Automatic prompt caching: the system prompt (the whole change-management SKILL.md)
            # and the tool definitions are identical on every turn, and the growing message
            # history only ever gets appended to, never rewritten -- exactly the multi-turn
            # pattern automatic caching is built for. This matters for more than cost: per
            # Anthropic's docs, cache_read_input_tokens do NOT count towards the per-minute input
            # token rate limit for this model, only genuinely new (uncached) input tokens do. The
            # 429 we hit on the very first live run was an input-tokens-per-minute limit, driven
            # almost entirely by resending the same SKILL.md and already-read file contents on
            # every turn -- this cuts that repeated cost to ~10% of its token price and takes it
            # out of the rate-limit calculation entirely from the second turn onward.
            cache_control={"type": "ephemeral"},
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


def branch_exists_remotely(branch: str) -> bool:
    """True if origin already has this branch. Checked before ever settling on a CHG number, so
    a branch left over from an earlier run -- e.g. a CHG whose PR was opened but never merged,
    or was merged without its branch being deleted -- can't cause a confusing 'failed to push'
    git error. checkout@v4 already configures an authenticated origin remote, so this needs no
    extra credentials."""
    result = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", branch],
        capture_output=True, text=True, check=True,
    )
    return bool(result.stdout.strip())


def get_next_chg_number() -> str:
    """Next CHG-xxx not yet mentioned in 06-change-log.md AND not already claimed by a
    chg/chg-xxx branch on the remote. The log-only check used to be the whole algorithm, but
    that silently breaks the moment an earlier CHG's branch/PR exists without (yet) being
    merged into the base branch: the log on main still says "no changes yet", so this would
    recompute the exact same number and its branch push would collide with that still-existing
    branch -- which is exactly the failure this run just hit live."""
    if not CHANGE_LOG_PATH.exists():
        nxt = 1
    else:
        text = CHANGE_LOG_PATH.read_text(encoding="utf-8")
        nums = [int(n) for n in re.findall(r"CHG-(\d+)", text)]
        nxt = (max(nums) + 1) if nums else 1

    while branch_exists_remotely(f"chg/chg-{nxt:03d}"):
        nxt += 1
    return f"CHG-{nxt:03d}"


def find_latest_proposal_comment(comments: list[dict]) -> str | None:
    marker = f"STATUS: {STATUS_LINES['proposed_change']}"
    for c in reversed(comments):
        if c["user"]["login"] == BOT_LOGIN and marker in c["body"]:
            return c["body"]
    return None


# Forces a small, dedicated tool call to pull change-record-template.md's fields out of
# vault-qa's draft proposal. This replaced an earlier regex parser that assumed the model would
# reproduce chg-proposal-template.md's exact bolded-field-per-line layout every time -- in a
# live run it instead wrote the same information as a Markdown table with different field names
# ("Affected IDs" instead of "Affected ID(s)", no separate "Requested by"), which a literal
# header match couldn't handle at all. Forcing a tool call is the same fix that already solved
# vault-qa's JSON-crash bug (ANSWER_TOOL in vault_qa_handler.py): it's robust to whatever
# markdown shape surrounds the fields -- a table, bullets, bolded lines, prose -- while still
# guaranteeing a clean, structured result, instead of leaving the mapping as one instruction
# buried inside a much longer agentic system prompt (the original problem) or assuming a rigid
# text format the model doesn't reliably produce (this module's first attempt at a fix).
CHG_FIELD_EXTRACTION_TOOL = {
    "name": "extract_chg_fields",
    "description": (
        "Extract change-record fields from vault-qa's draft change proposal below, regardless "
        "of whether it's written as a Markdown table, bolded field labels, bullet points, or "
        "prose. Always call this exactly once with your best-effort extraction of the meaning "
        "-- never answer with plain text instead, and never leave a field empty; if a value "
        "genuinely isn't stated, write 'not specified' rather than omitting it."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "affected_item": {
                "type": "string",
                "description": "The affected requirement/story/OQ ID(s), e.g. 'REQ-N-018, OQ-008'.",
            },
            "old_value": {
                "type": "string",
                "description": "The current vault content/value that would change, as quoted or summarized in the proposal.",
            },
            "new_value": {
                "type": "string",
                "description": "The proposed new value or content.",
            },
            "reason": {
                "type": "string",
                "description": "Why this change is being proposed.",
            },
            "triggered_by": {
                "type": "string",
                "description": "Where this proposal came from -- the issue, comment, or person that triggered it.",
            },
        },
        "required": ["affected_item", "old_value", "new_value", "reason", "triggered_by"],
    },
}


def extract_chg_fields(client: Anthropic, proposal_text: str) -> dict:
    """Runs one small, forced tool call (no agentic loop, no file access) to map vault-qa's
    draft proposal onto change-record-template.md's fields. Raises ValueError -- with the
    model's actual tool call missing or a required field left empty -- rather than silently
    proceeding with a bad or incomplete mapping."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=(
            "You extract structured fields from a draft change proposal written by the "
            "vault-qa skill. Its exact formatting varies from run to run -- a Markdown table, "
            "bolded field labels, bullet points -- extract the meaning of each field, not a "
            "literal string match against any particular template."
        ),
        messages=[{"role": "user", "content": f"Draft change proposal:\n\n{proposal_text}"}],
        tools=[CHG_FIELD_EXTRACTION_TOOL],
        tool_choice={"type": "tool", "name": "extract_chg_fields"},
    )
    for block in response.content:
        if block.type == "tool_use" and block.name == "extract_chg_fields":
            fields = block.input
            missing = [
                k for k in ("affected_item", "old_value", "new_value", "reason", "triggered_by")
                if not fields.get(k)
            ]
            if missing:
                raise ValueError(f"extraction returned an empty value for: {missing}")
            return fields
    raise ValueError("Claude's response did not include an extract_chg_fields tool call")


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

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    try:
        mapped = extract_chg_fields(client, proposal_text)
    except Exception as e:
        post_comment(
            repo, issue_number, token,
            f"STATUS: apply_change_failed\n\nCould not extract change-record fields from the "
            f"proposal comment: {e}\n\nNo action taken -- worth a look before retrying (removing "
            f"and re-adding the `approved` label will try again).",
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
        "posted as a GitHub Issue comment. The fields below have already been extracted and "
        "mapped into change-record-template.md's field names by this script (not by you) -- "
        "use them exactly as given, don't re-derive them from the raw comment text:\n\n"
        f"Affected item: {mapped['affected_item']}\n"
        f"Old value: {mapped['old_value']}\n"
        f"New value: {mapped['new_value']}\n"
        f"Reason: {mapped['reason']}\n"
        f"Triggered by: {mapped['triggered_by']}\n\n"
        "Two fields genuinely need your judgment, not mechanical mapping, so decide these "
        "yourself from context: Change type (e.g. 'Requirement modified', 'Priority change', "
        "'New requirement', 'Requirement removed'), and Resolves OQ (only fill in an OQ-xxx if "
        "the proposal or issue explicitly says this resolves an open question; otherwise use "
        "'—').\n\n"
        f"--- Original GitHub Issue #{issue_number}: {issue['title']} ---\n{issue['body']}\n\n"
        f"--- vault-qa's original proposal comment, for full context only -- the fields above "
        f"are already correctly extracted from it, you do not need to re-parse this ---\n"
        f"{proposal_text}\n"
    )

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
    try:
        run_git("checkout", "-b", branch)
        run_git("add", *changed_files)
        run_git("commit", "-m", f"{chg_id}: {issue['title']}")
        run_git("push", "-u", "origin", branch)
    except subprocess.CalledProcessError as e:
        # The edits themselves succeeded (verify_only_allowed_files_changed already passed) --
        # only the git/push step failed, most likely a branch name collision get_next_chg_number()
        # didn't catch (e.g. it was created in the few seconds between that check and this push).
        # Post something the human can act on instead of leaving them to dig a raw traceback out
        # of the Action log.
        post_comment(
            repo, issue_number, token,
            f"STATUS: apply_change_failed\n\nThe edits for {chg_id} were made correctly, but "
            f"creating/pushing branch `{branch}` failed: `{e}`. This usually means that branch "
            f"already exists on GitHub -- check whether an earlier, unmerged CHG PR is still "
            f"open, or whether a merged one was never deleted. No PR was opened here; nothing "
            f"was left half-committed on this run's branch since it never left the runner. "
            f"Resolve the branch collision, then retry by removing and re-adding the `approved` "
            f"label.",
        )
        return

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
