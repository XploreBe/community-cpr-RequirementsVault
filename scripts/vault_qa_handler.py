"""
vault_qa_handler.py

Runs the vault-qa skill against a single GitHub Issue and posts the result back as a comment.

Read-only against the vault: this script never writes to any vault file. Its only side effects
are GitHub API calls: posting one comment, and keeping exactly one 'status:*' triage label
(status:answered / status:possible-change / status:needs-clarification / status:rate-limited)
on the issue in sync with the most recent comment's STATUS.

Env vars required (all set by the workflow):
  ANTHROPIC_API_KEY  - Claude API key
  GITHUB_TOKEN       - provided automatically by GitHub Actions
  REPO               - "owner/repo", provided by the workflow
  ISSUE_NUMBER       - the issue that triggered this run
"""

import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from anthropic import Anthropic

VAULT_ROOT = Path(".")
SKILL_PATH = VAULT_ROOT / "00-pipeline-skills" / "vault-qa" / "SKILL.md"
BOT_LOGIN = "github-actions[bot]"

# Global rate limit: max bot-authored comments across the whole repo within the trailing hour.
# This guards against a runaway agent loop (e.g. an agent re-asking the same or similar question
# repeatedly) rather than any single conversation — see README for why this is global, not
# per-issue, and what its known blind spots are.
RATE_LIMIT_MAX_PER_HOUR = 20

# Maps the skill's JSON "mode" to the literal machine-readable status line prepended to every
# comment. Deliberately owned by the script, not the model, so an agent parsing this can rely on
# an exact string match every time — no risk of the model phrasing it slightly differently.
STATUS_LINES = {
    "qa": "answered",
    "proposed_change": "proposed_change",
    "needs_clarification": "needs_clarification",
}

# Maps each status_line value to the GitHub label that reflects it, so Mohamed can triage straight
# from the Issues list (filter by label) instead of opening every issue to read the last comment's
# STATUS line. Prefixed with "status:" to group them visually and avoid colliding with any labels
# Mohamed adds himself. Kept separate from STATUS_LINES on purpose: STATUS_LINES is a stable
# machine-readable contract other agents may already parse verbatim and must not change; these
# labels are purely a human/GitHub-UI triage aid and can be renamed freely.
STATUS_LABELS = {
    "answered": "status:answered",
    "proposed_change": "status:possible-change",
    "needs_clarification": "status:needs-clarification",
    "rate_limited": "status:rate-limited",
}

# Which vault documents are in scope for grounding an answer. Deliberately excludes the
# pipeline-skills folder itself (that's instructions, not vault content) and the raw brief.
CONTEXT_GLOBS = [
    "01-requirements-structured-v1.md",
    "02-scope-and-context-v1.md",
    "03-product-backlog-v1.md",
    "05-traceability-matrix.md",
    "06-change-log.md",
    "04-speckit-specs/**/*.md",
]

# Hard ceiling regardless of retrieval quality — a safety net, not the primary mechanism anymore.
MAX_CONTEXT_CHARS = 60_000

ID_PATTERN = re.compile(
    r"\b(REQ-F-\d+|REQ-N-\d+|CON-\d+|OQ-\d+|AS-\d+|EPIC-\d+|US-\d+|SPIKE-\d+|ENABLER-\d+|CHG-\d+)\b"
)

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "this", "that", "these", "those", "what",
    "which", "does", "do", "did", "can", "could", "should", "would", "have", "has", "had",
    "for", "and", "or", "but", "in", "on", "at", "to", "of", "it", "be", "as", "with", "not",
    "we", "i", "you", "our", "us", "there", "here", "just", "if", "then", "so", "actually",
    "system", "must", "will", "when", "given", "into", "also", "than", "from", "about",
}


def split_into_sections(text: str, file_label: str) -> list[dict]:
    """Split a markdown file into heading-delimited chunks. Flat, not hierarchical — good
    enough for these docs since every requirement/story/section already lives under its own
    heading."""
    lines = text.splitlines()
    sections = []
    heading = "(intro)"
    buf = []
    for line in lines:
        if re.match(r"^#{1,6}\s", line):
            if buf:
                sections.append({"file": file_label, "heading": heading, "text": "\n".join(buf)})
            heading = line.strip()
            buf = [line]
        else:
            buf.append(line)
    if buf:
        sections.append({"file": file_label, "heading": heading, "text": "\n".join(buf)})
    return sections


def load_all_sections() -> list[dict]:
    sections = []
    for pattern in CONTEXT_GLOBS:
        for path in sorted(VAULT_ROOT.glob(pattern)):
            if path.is_file():
                sections.extend(split_into_sections(path.read_text(encoding="utf-8"), str(path)))
    return sections


def extract_ids(text: str) -> set[str]:
    return set(ID_PATTERN.findall(text))


def extract_keywords(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def score_section(section: dict, ids: set[str], keywords: list[str]) -> int:
    text = section["text"]
    score = 0
    for id_ in ids:
        if id_ in text:
            score += 25  # an explicit ID match is a near-certain signal, weight it heavily
    lower = text.lower()
    for kw in keywords:
        score += lower.count(kw)
    return score


def build_targeted_context(question: str, full_transcript: str) -> tuple[str, list[str]]:
    """Return (context_text, list_of_included_section_labels) so the answer can cite what was
    actually searched, not just assert it read 'the vault'."""
    sections = load_all_sections()
    if not sections:
        return "[No vault content files found]", []

    # IDs anywhere in the thread matter (an ID mentioned two comments ago is still relevant);
    # free-text keywords only from the current question, to keep the search focused on what's
    # actually being asked right now rather than drifting with the whole thread's vocabulary.
    ids = extract_ids(full_transcript)
    keywords = extract_keywords(question)

    scored = [(score_section(s, ids, keywords), s) for s in sections]
    scored = [pair for pair in scored if pair[0] > 0]
    scored.sort(key=lambda pair: pair[0], reverse=True)

    included = []
    labels = []
    total_len = 0
    for score, section in scored:
        chunk = f"--- {section['file']} | {section['heading']} ---\n{section['text']}"
        if total_len + len(chunk) > MAX_CONTEXT_CHARS:
            break
        included.append(chunk)
        labels.append(f"{section['file']} ({section['heading']})")
        total_len += len(chunk)

    if not included:
        # Nothing matched at all. Real vault files always start with a title heading (not a
        # bare "(intro)" block), so fall back to the first section of each file — that's
        # normally the summary/overview by convention — and say explicitly that this is a
        # no-match fallback, not a targeted answer.
        seen_files = set()
        for section in sections:
            if section["file"] in seen_files:
                continue
            seen_files.add(section["file"])
            chunk = f"--- {section['file']} | {section['heading']} ---\n{section['text']}"
            if total_len + len(chunk) > MAX_CONTEXT_CHARS:
                break
            included.append(chunk)
            labels.append(f"{section['file']} ({section['heading']}) [fallback — no direct match found]")
            total_len += len(chunk)

    return "\n\n".join(included), labels


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


def build_transcript(issue: dict, comments: list[dict]) -> tuple[str, str]:
    """Returns (full_transcript_text, current_question). The current question is the most
    recent human message (a new comment, or the issue body itself if there are no comments yet
    or the latest activity was an 'edited' event on the body)."""
    lines = [f"[ISSUE OPENED by {issue['user']['login']}] {issue['title']}\n{issue.get('body') or ''}"]
    for c in comments:
        speaker = "VAULT-QA BOT (previous answer)" if c["user"]["login"] == BOT_LOGIN else f"[COMMENT by {c['user']['login']}]"
        lines.append(f"{speaker}\n{c['body']}")

    human_comments = [c for c in comments if c["user"]["login"] != BOT_LOGIN]
    current_question = human_comments[-1]["body"] if human_comments else (issue.get("body") or issue["title"])

    return "\n\n".join(lines), current_question


def post_comment(repo: str, issue_number: str, token: str, body: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    resp = requests.post(url, headers={"Authorization": f"Bearer {token}",
                                        "Accept": "application/vnd.github+json"},
                          json={"body": body})
    resp.raise_for_status()


def add_label(repo: str, issue_number: str, token: str, label: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    resp = requests.post(url, headers={"Authorization": f"Bearer {token}",
                                        "Accept": "application/vnd.github+json"},
                          json={"labels": [label]})
    resp.raise_for_status()


def get_current_labels(repo: str, issue_number: str, token: str) -> list[str]:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}",
                                       "Accept": "application/vnd.github+json"})
    resp.raise_for_status()
    return [label["name"] for label in resp.json()]


def remove_label(repo: str, issue_number: str, token: str, label: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels/{label}"
    resp = requests.delete(url, headers={"Authorization": f"Bearer {token}",
                                          "Accept": "application/vnd.github+json"})
    # A 404 just means the label was already gone (e.g. a race with a manual edit) — not worth
    # failing the whole run over.
    if resp.status_code != 404:
        resp.raise_for_status()


def set_status_label(repo: str, issue_number: str, token: str, status_line: str) -> None:
    """Make the issue's status:* label match status_line, replacing whatever status:* label was
    there before. An issue's thread can shift mode across comments (e.g. Mode A, then a later
    comment triggers Mode B) — this keeps exactly one status:* label present at a time so
    filtering the Issues list by label always reflects the *current* state, not every state the
    issue ever passed through. Labels outside the status:* namespace (vault-question, or anything
    Mohamed adds by hand) are left untouched."""
    desired = STATUS_LABELS.get(status_line)
    if not desired:
        return
    current = get_current_labels(repo, issue_number, token)
    for label in current:
        if label.startswith("status:") and label != desired:
            remove_label(repo, issue_number, token, label)
    if desired not in current:
        add_label(repo, issue_number, token, desired)


def count_recent_bot_comments(repo: str, token: str) -> int:
    """Count how many comments the bot has posted anywhere in this repo in the trailing hour.
    One cheap API call, first page only (100 comments) — see README for the known blind spot on
    very high-volume repos."""
    since = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.github.com/repos/{repo}/issues/comments"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}",
                                       "Accept": "application/vnd.github+json"},
                         params={"since": since, "per_page": 100, "sort": "created", "direction": "desc"})
    resp.raise_for_status()
    comments = resp.json()
    return sum(1 for c in comments if c["user"]["login"] == BOT_LOGIN)


# Forces the model's structured output through the Anthropic API's own JSON parsing instead of
# asking the model to hand-write a JSON string. The old approach broke whenever the "answer"
# field legitimately contained a markdown blockquote with double quotes (e.g. citing vault text
# verbatim) and the model didn't escape them perfectly inside its own JSON text — see the
# incident that prompted this fix. tool_choice below forces exactly this tool to be called, so
# there's no plain-text fallback path to fall out of.
ANSWER_TOOL = {
    "name": "submit_answer",
    "description": (
        "Submit the structured answer to the vault question. Always call this tool exactly "
        "once with the final answer for this turn — never answer with plain text instead."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["qa", "proposed_change", "needs_clarification"],
                "description": "Which of the three skill modes applies to this question.",
            },
            "answer": {
                "type": "string",
                "description": "The answer to post as the issue comment body (markdown).",
            },
            "chg_proposal": {
                "type": ["string", "null"],
                "description": (
                    "A draft CHG proposal in the chg-proposal-template.md format. Only set "
                    "when mode is 'proposed_change'; null otherwise."
                ),
            },
        },
        "required": ["mode", "answer"],
    },
}


def ask_claude(skill_instructions: str, context_text: str, context_labels: list[str],
                transcript: str, current_question: str) -> dict:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    labels_note = "\n".join(f"- {label}" for label in context_labels) or "(no sections matched)"
    system_prompt = (
        skill_instructions
        + "\n\n---\n\nVault sections retrieved for this question (cite these, don't claim to "
        + "have read the whole vault if only these were searched):\n"
        + labels_note
        + "\n\n---\n\nRetrieved content:\n\n"
        + context_text
    )
    user_content = (
        "Full conversation so far on this issue (oldest to newest):\n\n"
        + transcript
        + "\n\n---\n\nAnswer the most recent human message above:\n\n"
        + current_question
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
        tools=[ANSWER_TOOL],
        tool_choice={"type": "tool", "name": "submit_answer"},
    )
    for block in response.content:
        if block.type == "tool_use" and block.name == "submit_answer":
            return block.input
    # Fail loud, not silent — a missing tool call should not turn into a bad guess about what
    # to post.
    print("ERROR: Claude's response did not include a submit_answer tool call:\n",
          response.content, file=sys.stderr)
    raise RuntimeError("No submit_answer tool_use block in Claude's response")


def main() -> None:
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]
    github_token = os.environ["GITHUB_TOKEN"]

    recent_count = count_recent_bot_comments(repo, github_token)
    if recent_count >= RATE_LIMIT_MAX_PER_HOUR:
        # Stop before spending any API budget on Claude — the rate limit exists specifically to
        # cap cost and prevent loops, so it must trigger before, not after, the expensive call.
        post_comment(
            repo, issue_number, github_token,
            f"STATUS: rate_limited\n\n"
            f"This repo has hit the vault-qa rate limit ({RATE_LIMIT_MAX_PER_HOUR} answers per "
            f"hour). No question was processed this time. If you're an agent seeing this: back "
            f"off and retry later rather than immediately re-asking — repeated immediate retries "
            f"will just keep hitting this same limit. If this limit is too low for legitimate "
            f"usage, Mohamed can raise RATE_LIMIT_MAX_PER_HOUR in scripts/vault_qa_handler.py.",
        )
        set_status_label(repo, issue_number, github_token, "rate_limited")
        return

    issue = get_issue(repo, issue_number, github_token)
    comments = get_comments(repo, issue_number, github_token)
    transcript, current_question = build_transcript(issue, comments)

    skill_instructions = SKILL_PATH.read_text(encoding="utf-8")
    context_text, context_labels = build_targeted_context(current_question, transcript)

    result = ask_claude(skill_instructions, context_text, context_labels, transcript, current_question)

    status_line = STATUS_LINES.get(result.get("mode"), "answered")
    comment_body = f"STATUS: {status_line}\n\n" + result["answer"]
    if result.get("mode") == "proposed_change" and result.get("chg_proposal"):
        comment_body += "\n\n---\n\n" + result["chg_proposal"]

    post_comment(repo, issue_number, github_token, comment_body)
    set_status_label(repo, issue_number, github_token, status_line)


if __name__ == "__main__":
    main()
