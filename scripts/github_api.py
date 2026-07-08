"""
github_api.py

Small shared wrapper around the GitHub REST API calls both vault_qa_handler.py and
apply_change_handler.py need. Extracted because BOT_LOGIN / get_issue / get_comments /
post_comment used to be defined twice, verbatim, in both scripts -- any future change to how
one of these calls works (auth, pagination, error handling) had to be made in two places, and
a missed spot would be a silent bug, not a loud one.

STATUS_LINES also lives here (not just in vault_qa_handler.py) because apply_change_handler.py
needs to recognise a vault-qa "proposed_change" comment, and it should do that by referencing
the same machine-readable contract vault_qa_handler.py writes, not a hardcoded copy of the
literal string.

Every request carries REQUEST_TIMEOUT so a slow/hanging GitHub API call can't leave a workflow
run stuck until the runner's own multi-hour default timeout.
"""

import requests

BOT_LOGIN = "github-actions[bot]"

# Generous but bounded -- GitHub's API is normally sub-second; this only exists to stop an
# actual hang (network partition, GitHub incident) from silently burning CI minutes.
REQUEST_TIMEOUT = 30

# Maps the vault-qa skill's JSON "mode" to the literal machine-readable status line prepended
# to every comment it posts. Owned here, not by either script individually, so both scripts
# agree on the exact string to write/match -- no risk of one being updated without the other.
STATUS_LINES = {
    "qa": "answered",
    "proposed_change": "proposed_change",
    "needs_clarification": "needs_clarification",
}


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


def get_issue(repo: str, issue_number: str, token: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    resp = requests.get(url, headers=_headers(token), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def get_comments(repo: str, issue_number: str, token: str) -> list[dict]:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    resp = requests.get(url, headers=_headers(token), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def post_comment(repo: str, issue_number: str, token: str, body: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    resp = requests.post(url, headers=_headers(token), json={"body": body}, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()


def add_label(repo: str, issue_number: str, token: str, label: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    resp = requests.post(url, headers=_headers(token), json={"labels": [label]}, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()


def get_current_labels(repo: str, issue_number: str, token: str) -> list[str]:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    resp = requests.get(url, headers=_headers(token), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return [label["name"] for label in resp.json()]


def remove_label(repo: str, issue_number: str, token: str, label: str) -> None:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels/{label}"
    resp = requests.delete(url, headers=_headers(token), timeout=REQUEST_TIMEOUT)
    # A 404 just means the label was already gone (e.g. a race with a manual edit) -- not worth
    # failing the whole run over.
    if resp.status_code != 404:
        resp.raise_for_status()


def open_pull_request(repo: str, token: str, branch: str, base: str, title: str, body: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/pulls"
    resp = requests.post(
        url, headers=_headers(token),
        json={"title": title, "head": branch, "base": base, "body": body},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()
