"""
vault_qa_handler.py

Runs the vault-qa skill against a single GitHub Issue and posts the result back as a comment.

Read-only against the vault: this script never writes to any vault file. Its only side effects
are GitHub API calls: posting one comment, and optionally adding the 'possible-change' label.

Env vars required (all set by the workflow):
  ANTHROPIC_API_KEY  - Claude API key
  GITHUB_TOKEN       - provided automatically by GitHub Actions
  REPO               - "owner/repo", provided by the workflow
  ISSUE_NUMBER       - the issue that triggered this run
"""

import json
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
    )
    text = "".join(block.text for block in response.content if block.type == "text").strip()
    # Defensive cleanup in case the model wraps the JSON in a fence despite instructions not to.
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fail loud, not silent — an unparsed response should not turn into a bad guess about
        # what to post.
        print("ERROR: could not parse Claude's response as JSON:\n", text, file=sys.stderr)
        raise


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

    if result.get("mode") == "proposed_change":
        add_label(repo, issue_number, github_token, "possible-change")


if __name__ == "__main__":
    main()
