#!/usr/bin/env python3
"""
vault_to_github.py
One-way, on-demand sync: Obsidian BA vault → GitHub Issues

Reads stories/spikes/enablers from 03-product-backlog-v1.md, creates or
updates GitHub Issues. Never deletes or closes issues automatically.
Tracks issue numbers in 04-speckit-specs/.github-sync.json.

Usage:
  python vault_to_github.py                    # dry-run (default, safe)
  python vault_to_github.py --apply            # actually create/update
  python vault_to_github.py --apply --story US-001   # single item only

Required env var:
  GITHUB_TOKEN   Personal access token with repo scope
                 (fine-grained: Issues read/write + Contents read/write)

Required env var (in addition to GITHUB_TOKEN):
  GITHUB_REPO    owner/repo — no default, must be set explicitly per project

Optional env vars:
  VAULT_PATH     path to vault root  (default: parent of this script)
"""

import os
import re
import sys
import json
import base64
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

import requests

# ─── Configuration ────────────────────────────────────────────────────────────
# This script is project-agnostic: it derives all sprint/epic/label structure
# from whatever is written in the vault's backlog file. Nothing here should
# be hardcoded to a specific project — set GITHUB_REPO (and optionally
# VAULT_PATH) per project via environment variables instead.

GITHUB_REPO    = os.getenv("GITHUB_REPO", "")
VAULT_PATH     = Path(os.getenv("VAULT_PATH", Path(__file__).parent.parent))
BACKLOG_FILE   = "03-product-backlog-v1.md"
SPECS_DIR      = "04-speckit-specs"
TRACKING_FILE  = f"{SPECS_DIR}/.github-sync.json"
SPECS_REPO_DIR = "specs"   # folder in the GitHub repo where spec files are published
GITHUB_API     = "https://api.github.com"
GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN", "")
LOG_DIR        = Path(__file__).parent / "sync-logs"

# ─── Data model ───────────────────────────────────────────────────────────────

@dataclass
class Item:
    id: str                                      # US-001 / SPIKE-001 / ENABLER-001
    title: str = ""
    item_type: str = "Story"                     # Story | Spike | Enabler
    story_text: str = ""                         # "As a X, I want Y, so that Z"
    goal: str = ""                               # for Spike / Enabler
    done_when: str = ""                          # for Spike
    ac_lines: list = field(default_factory=list) # Given/When/Then bullets
    priority: str = "Must"
    size: str = ""
    phase: str = "Phase 1"
    sprint_raw: str = ""                         # raw "Phase/Sprint" field text, e.g. "Sprint 3 — hardening"
    epic_id: str = ""
    epic_title: str = ""
    depends_raw: list = field(default_factory=list)  # ["US-002", "SPIKE-001"]
    status_raw: str = "Ready"
    notes: str = ""
    spec_file: Optional[Path] = None

# ─── Vault parser ─────────────────────────────────────────────────────────────

def load_backlog(vault: Path) -> str:
    path = vault / BACKLOG_FILE
    if not path.exists():
        raise FileNotFoundError(f"Backlog not found: {path}")
    return path.read_text(encoding="utf-8")


def parse_epic_titles(text: str) -> dict:
    """Return {EPIC-1: 'Auth & Identity', ...}"""
    titles = {}
    # From epics table: | [[#EPIC-1\|EPIC-1]] | Title | ...
    for m in re.finditer(r'\[\[#(EPIC-\d+)\\?\|EPIC-\d+\]\]\s*\|\s*([^|]+?)\s*\|', text):
        titles[m.group(1)] = m.group(2).strip()
    # From section header: ## EPIC-1 \n\n **Title:** ...
    for m in re.finditer(r'^## (EPIC-\d+)\s*\n+\*\*Title:\*\*\s*(.+)$', text, re.MULTILINE):
        titles[m.group(1)] = m.group(2).strip()
    return titles


def find_spec_file(item_id: str, vault: Path) -> Optional[Path]:
    """Match epic*-us001-*.md by the normalized story ID in the filename."""
    # US-001 → us001,  SPIKE-001 → spike001,  ENABLER-001 → enabler001
    norm = item_id.lower().replace("-", "")
    specs_dir = vault / SPECS_DIR
    if not specs_dir.exists():
        return None
    for f in specs_dir.glob("*.md"):
        if f.name.startswith("00-") or "blocked" in f.name:
            continue
        # filename: epic1-us001-slug-words.md → parts[1] = 'us001'
        parts = f.stem.split("-")
        if len(parts) >= 2 and parts[1].replace("-", "") == norm:
            return f
    return None


def extract_field(text: str, field_name: str) -> str:
    """Extract value of '- **FieldName:** value' (full line after the colon)."""
    pattern = re.compile(
        rf'^\s*-\s*\*\*{re.escape(field_name)}:\*\*\s*(.+?)$',
        re.MULTILINE
    )
    m = pattern.search(text)
    return m.group(1).strip() if m else ""


def extract_ac(section: str) -> list:
    """Return acceptance criteria as a flat list of strings.
    Stops at the first metadata bullet (- **FieldName:**) so priority,
    epic, status etc. don't leak into the AC list.
    """
    m = re.search(r'\*\*Acceptance criteria:\*\*\s*\n', section)
    if not m:
        return []
    lines = []
    for line in section[m.end():].splitlines():
        # Stop when we hit a top-level metadata field like '- **Priority:**'
        if re.match(r'\s*- \*\*\w', line):
            break
        stripped = line.strip().lstrip("- ").strip()
        if stripped:
            lines.append(stripped)
    return lines


def extract_depends(section: str) -> list:
    """Return story IDs from 'Depends on / Blocked by' field, deduplicated."""
    raw = extract_field(section, r"Depends on / Blocked by")
    if not raw or raw.strip() == "—":
        return []
    seen, result = set(), []
    for dep_id in re.findall(r'\b(US-\d+|SPIKE-\d+|ENABLER-\d+)\b', raw):
        if dep_id not in seen:
            seen.add(dep_id)
            result.append(dep_id)
    return result


def parse_priority_line(section: str) -> tuple:
    """Parse the combined '- **Priority:** Must · **Size:** M · **Phase/Sprint:** Phase 1' line."""
    raw = extract_field(section, "Priority")
    if not raw:
        return "Must", "", "Phase 1", ""

    # Priority is the word immediately after "**Priority:**"
    priority = raw.split("·")[0].strip().split()[-1]

    size_m = re.search(r'\*\*Size:\*\*\s*(\S+)', raw)
    size = size_m.group(1).rstrip("·").strip() if size_m else ""

    phase_m = re.search(r'\*\*Phase/Sprint:\*\*\s*(.+?)(?:\s*·|$)', raw)
    phase_raw = phase_m.group(1).strip() if phase_m else ""
    phase = "Phase 2" if "2" in phase_raw else "Phase 1"

    # Strip bracketed/parenthetical asides (change-history tags, footnotes)
    # so they don't bleed into the derived sprint label — e.g.
    # "Phase 1 [CHG-008 — resized ...]" should yield the label "Phase 1",
    # not a label containing the whole aside.
    sprint_raw = re.sub(r'\[.*?\]|\(.*?\)', '', phase_raw).strip(' —-')

    return priority, size, phase, sprint_raw


def parse_epic_ref(epic_line: str) -> str:
    """Extract 'EPIC-1' from '[[#EPIC-1|EPIC-1]] · ...'"""
    m = re.search(r'\[\[#(EPIC-\d+)[|\\]', epic_line)
    return m.group(1) if m else ""


def parse_items(backlog_text: str, epic_titles: dict, vault: Path) -> list:
    """Parse all US-xxx / SPIKE-xxx / ENABLER-xxx blocks from the backlog."""
    heading_re = re.compile(
        r'^### (US-\d+|SPIKE-\d+|ENABLER-\d+)\s*$', re.MULTILINE
    )
    positions = [(m.start(), m.group(1)) for m in heading_re.finditer(backlog_text)]

    items = []
    for i, (start, item_id) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(backlog_text)
        section = backlog_text[start:end]

        it = Item(id=item_id)
        it.title      = extract_field(section, "Title")
        # "Spike (timeboxed)" → "Spike"
        it.item_type  = extract_field(section, "Type").split("(")[0].strip()
        it.story_text = extract_field(section, "Story")
        it.goal       = extract_field(section, "Goal")
        it.done_when  = extract_field(section, "Done when")
        it.ac_lines   = extract_ac(section)
        it.notes      = extract_field(section, "Notes")

        it.priority, it.size, it.phase, it.sprint_raw = parse_priority_line(section)

        epic_line    = extract_field(section, "Epic")
        it.epic_id   = parse_epic_ref(epic_line)
        it.epic_title = epic_titles.get(it.epic_id, "")

        it.depends_raw = extract_depends(section)
        it.status_raw  = extract_field(section, "Status")
        it.spec_file   = find_spec_file(item_id, vault)

        items.append(it)

    return items

# ─── Tracking file ────────────────────────────────────────────────────────────

def load_tracking(vault: Path) -> dict:
    path = vault / TRACKING_FILE
    if not path.exists():
        return {"version": 1, "issues": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_tracking(vault: Path, data: dict, dry_run: bool):
    data["last_sync"] = datetime.now(timezone.utc).isoformat()
    if dry_run:
        return
    path = vault / TRACKING_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

# ─── Wikilink converter ───────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def convert_wikilinks(text: str, tracking: dict) -> str:
    """
    Convert Obsidian wikilinks to GitHub Markdown or plain text.

    [[#US-002|US-002]]          → #42 (US-002)   if tracked, else plain 'US-002'
    [[#SPIKE-001|SPIKE-001]]    → #43 (SPIKE-001) if tracked, else plain text
    [[file#section|REQ-F-001]]  → REQ-F-001       (no GitHub equivalent)
    [[anyfile|display]]         → display
    """
    issues = tracking.get("issues", {})

    def replace(m):
        inner = m.group(1)
        # Handle escaped pipes (Markdown table escaping) and normal pipes
        if r'\|' in inner:
            target, display = inner.split(r'\|', 1)
        elif '|' in inner:
            target, display = inner.split('|', 1)
        else:
            target = display = inner

        target  = target.strip()
        display = display.strip()

        # Within-backlog reference: [[#US-002|...]]
        if target.startswith('#'):
            ref_id = target.lstrip('#')
            if ref_id in issues:
                num = issues[ref_id]["issue_number"]
                return f"#{num} ({display})"
            return display   # not yet synced

        # Vault document reference → plain display text
        return display

    return WIKILINK_RE.sub(replace, text)

# ─── Change-history cleaner ────────────────────────────────────────────────────
#
# The vault deliberately keeps every edit visible for BA traceability:
# ~~struck-through~~ old text plus a trailing [CHG-xxx ...] / (CHG-xxx ...)
# annotation on every changed line. That's exactly right for Obsidian, and
# exactly wrong for a GitHub issue a developer re-reads sprint after sprint —
# left in place, it accumulates into unreadable noise as more changes land.
# GitHub issues should only ever show the *current* requirement; the vault
# is the permanent record of how it got there.

## Note the leading \s* — the tag's own leading whitespace is consumed as
## part of the match, since in this vault a tag always trails the text it
## annotates ("...done here. [CHG-008]"). Removing the whitespace *with* the
## tag (rather than as a separate cleanup pass) means we never have to guess
## which stray "**" a leftover space belongs to, so "**Label:** value"
## metadata lines elsewhere in a document are never touched.
CHG_TAG_RE       = re.compile(r'\s*\[CHG-\d+[^\]]*\]|\s*\(CHG-\d+[^)]*\)')
STRIKETHROUGH_RE = re.compile(r'~~.*?~~', re.DOTALL)


def clean_for_github(text: str) -> str:
    """Strip vault change-history markup before it reaches GitHub.

    - ~~struck-through~~ spans are removed entirely (old/removed content —
      it no longer applies, so it shouldn't linger in an issue)
    - [CHG-xxx ...] / (CHG-xxx ...) annotations are stripped, along with the
      whitespace immediately before them
    - leftover empty bold markers and double spaces left behind by the
      removals above are cleaned up
    """
    if not text:
        return text
    text = STRIKETHROUGH_RE.sub('', text)
    text = CHG_TAG_RE.sub('', text)
    text = re.sub(r'\*\*\s*\*\*', '', text)        # now-empty bold markers
    text = re.sub(r'\s{2,}', ' ', text)            # collapse double spaces
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)   # fix spacing before punctuation
    return text.strip()


def is_fully_removed(raw_line: str) -> bool:
    """True if a bullet's entire original content is struck through, meaning
    it no longer applies at all — this bullet should not appear in GitHub
    (as opposed to a bullet that's merely been edited, which stays, cleaned)."""
    return raw_line.strip().startswith('~~')

# ─── Spec file helpers ────────────────────────────────────────────────────────

def extract_spec_section(spec_file: Optional[Path], heading: str) -> list:
    """Return bullet lines under a ## heading in a spec file."""
    if not spec_file or not spec_file.exists():
        return []
    text = spec_file.read_text(encoding="utf-8")
    m = re.search(
        rf'## {re.escape(heading)}\s*\n((?:[ \t]*- .+\n?)+)',
        text
    )
    if not m:
        return []
    return [
        line.strip().lstrip("- ").strip()
        for line in m.group(1).splitlines()
        if line.strip().lstrip("- ").strip()
    ]

# ─── Issue body builder ───────────────────────────────────────────────────────

def build_issue_title(it: Item) -> str:
    return f"[{it.id}] {clean_for_github(it.title)}"


def spec_url(it: Item, repo: str) -> Optional[str]:
    if not it.spec_file:
        return None
    return (
        f"https://github.com/{repo}/blob/main"
        f"/{SPECS_REPO_DIR}/{it.spec_file.name}"
    )


def build_body(it: Item, tracking: dict, repo: str) -> str:
    wl = lambda t: convert_wikilinks(clean_for_github(t), tracking)
    lines = []

    # Story / Goal
    if it.item_type == "Story" and it.story_text:
        lines += ["## Story", wl(it.story_text), ""]
    elif it.goal:
        lines += ["## Goal", wl(it.goal), ""]
        if it.done_when:
            lines += ["## Done when", wl(it.done_when), ""]

    # Acceptance criteria — bullets that are entirely struck through (fully
    # removed by a change record) are dropped instead of shown, so removed
    # scope doesn't linger in the issue; surviving bullets are cleaned of
    # their change-history markup but otherwise kept.
    if it.ac_lines:
        active_ac = [wl(ac) for ac in it.ac_lines if not is_fully_removed(ac)]
        active_ac = [ac for ac in active_ac if ac]
        if active_ac:
            lines.append("## Acceptance criteria")
            for ac in active_ac:
                lines.append(f"- {ac}")
            lines.append("")

    # Spec link
    url = spec_url(it, repo)
    lines.append("## Spec")
    if url:
        lines.append(f"[{it.id} spec]({url})")
    elif "Not Ready" in it.status_raw:
        lines.append("_No spec file yet — story is Not Ready._")
    else:
        lines.append("_No spec file yet — story is Ready but the spec hasn't been written yet._")
    lines.append("")

    # Dependencies
    lines.append("## Dependencies")
    issues = tracking.get("issues", {})
    if it.depends_raw:
        for dep_id in it.depends_raw:
            if dep_id in issues:
                num = issues[dep_id]["issue_number"]
                lines.append(f"- #{num} ({dep_id})")
            else:
                lines.append(f"- {dep_id} _(not yet synced — run again after first batch)_")
    else:
        lines.append("_None_")
    lines.append("")

    # Out of scope (pulled from spec file)
    oos = extract_spec_section(it.spec_file, "Out of scope")
    if oos:
        active_oos = [wl(line) for line in oos if not is_fully_removed(line)]
        active_oos = [line for line in active_oos if line]
        if active_oos:
            lines.append("## Out of scope")
            for line in active_oos:
                lines.append(f"- {line}")
            lines.append("")

    # Notes
    if it.notes:
        cleaned_notes = wl(it.notes)
        if cleaned_notes:
            lines += ["## Notes", cleaned_notes, ""]

    # Not Ready callout
    if "Not Ready" in it.status_raw:
        reason = re.sub(r'^Not Ready\s*[—-]\s*', '', it.status_raw).strip()
        lines.append("> **Status: Not Ready**")
        if reason:
            cleaned_reason = wl(reason)
            if cleaned_reason:
                lines.append(f"> {cleaned_reason}")
        lines.append("")

    # Footer
    lines += [
        "---",
        f"_Synced from vault · `{it.id}` · {datetime.now(timezone.utc).strftime('%Y-%m-%d')}_",
    ]

    return "\n".join(lines)

# ─── Labels ───────────────────────────────────────────────────────────────────
#
# Epic and sprint labels are derived entirely from the vault's own content
# (each story's "Epic" field and "Phase/Sprint" field) rather than from a
# project-specific mapping. This keeps the script identical across projects —
# a new project just needs a backlog written in the standard format; no label
# map needs to be hand-maintained here.

# Rotating colour palette used for any label whose colour isn't fixed below.
# A label's colour is picked deterministically from its own name, so re-runs
# are stable without needing a hardcoded name → colour table.
LABEL_COLOR_PALETTE = [
    "0075ca", "e4e669", "d93f0b", "0e8a16", "5319e7",
    "c5def5", "f9d0c4", "1d76db", "006b75", "b60205", "c2e0c6", "fbca04",
]


def palette_color(label_name: str) -> str:
    h = sum(ord(c) for c in label_name)
    return LABEL_COLOR_PALETTE[h % len(LABEL_COLOR_PALETTE)]


BASE_LABELS = {
    "priority:must":        ("b60205", "MoSCoW Must"),
    "priority:should":      ("e99695", "MoSCoW Should"),
    "priority:could":       ("f9d0c4", "MoSCoW Could"),
    "priority:wont":        ("ffffff", "MoSCoW Won't"),
    "type:story":           ("0075ca", "User story"),
    "type:spike":           ("ededed", "Research spike"),
    "type:enabler":         ("bfd4f2", "Technical enabler"),
    "status:ready":         ("0e8a16", "Ready to develop"),
    "status:not-ready":     ("e4e669", "Blocked or Not Ready"),
    "status:conditional":   ("fbca04", "Ready with conditions"),
}


def epic_label_slug(epic_title: str) -> str:
    slug = epic_title.lower()
    slug = re.sub(r'[&]', 'and', slug)
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return f"epic:{slug}"


def sprint_label_slug(sprint_raw: str) -> Optional[str]:
    """Turn a story's raw 'Phase/Sprint' text (e.g. 'Sprint 3 — hardening',
    'Phase 2') into a GitHub label slug, e.g. 'sprint:sprint-3-hardening'.
    Returns None if the field is empty.
    """
    if not sprint_raw:
        return None
    slug = sprint_raw.lower()
    slug = re.sub(r'[&]', 'and', slug)
    slug = re.sub(r'[^\w\s-]', '', slug)   # drop em-dashes/punctuation
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return f"sprint:{slug}" if slug else None


def item_labels(it: Item) -> list:
    labels = []

    # Priority
    p = it.priority.lower().replace("'", "").replace(" ", "")
    labels.append(f"priority:{p}")

    # Type
    t = it.item_type.lower()
    if "spike" in t:
        labels.append("type:spike")
    elif "enabler" in t:
        labels.append("type:enabler")
    else:
        labels.append("type:story")

    # Status
    s = it.status_raw
    if "Not Ready" in s:
        labels.append("status:not-ready")
    elif "conditional" in s.lower():
        labels.append("status:conditional")
    else:
        labels.append("status:ready")

    # Epic
    if it.epic_id and it.epic_title:
        labels.append(epic_label_slug(it.epic_title))

    # Sprint / build order — derived directly from this story's own
    # "Phase/Sprint" field, so no project-specific mapping is needed.
    sprint_label = sprint_label_slug(it.sprint_raw)
    if sprint_label:
        labels.append(sprint_label)

    return labels


def bootstrap_labels(client, items: list, dry_run: bool, log: logging.Logger):
    # In dry-run mode skip the API call — just compute what would be created
    existing = set() if dry_run else {l["name"] for l in client.list_labels()}
    to_create = {}

    for name, (color, desc) in BASE_LABELS.items():
        if name not in existing:
            to_create[name] = (color, desc)

    for it in items:
        if it.epic_id and it.epic_title:
            name = epic_label_slug(it.epic_title)
            if name not in existing and name not in to_create:
                to_create[name] = (palette_color(name), it.epic_title)

        sprint_label = sprint_label_slug(it.sprint_raw)
        if sprint_label and sprint_label not in existing and sprint_label not in to_create:
            to_create[sprint_label] = (palette_color(sprint_label), it.sprint_raw)

    if not to_create:
        log.info("  All labels already exist.")
        return

    for name, (color, desc) in sorted(to_create.items()):
        if dry_run:
            log.info(f"  [DRY-RUN] Would create label: {name}")
        else:
            client.create_label(name, color, desc)
            log.info(f"  Created label: {name}")

def cleanup_sprint_labels(client, items: list, dry_run: bool, log: logging.Logger):
    """Delete any sprint: labels in GitHub that no longer correspond to a
    Phase/Sprint value currently present in the vault's backlog."""
    valid_sprint_labels = {
        s for s in (sprint_label_slug(it.sprint_raw) for it in items) if s
    }
    existing = [] if dry_run else client.list_labels()
    to_delete = [l["name"] for l in existing if l["name"].startswith("sprint:") and l["name"] not in valid_sprint_labels]

    if not to_delete:
        log.info("  No obsolete sprint labels found.")
        return

    for name in sorted(to_delete):
        if dry_run:
            log.info(f"  [DRY-RUN] Would delete obsolete label: {name}")
        else:
            client.delete_label(name)
            log.info(f"  Deleted obsolete label: {name}")

# ─── GitHub API client ────────────────────────────────────────────────────────

class GitHubClient:
    def __init__(self, token: str, repo: str):
        self.repo    = repo
        self.base    = f"{GITHUB_API}/repos/{repo}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization":        f"Bearer {token}",
            "Accept":               "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def _get(self, path: str, **kw):
        r = self.session.get(f"{self.base}{path}", **kw)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, **kw):
        r = self.session.post(f"{self.base}{path}", **kw)
        r.raise_for_status()
        return r.json()

    def _patch(self, path: str, **kw):
        r = self.session.patch(f"{self.base}{path}", **kw)
        r.raise_for_status()
        return r.json()

    def _put(self, path: str, **kw):
        r = self.session.put(f"{self.base}{path}", **kw)
        r.raise_for_status()
        return r.json()

    def get_issue(self, number: int) -> dict:
        return self._get(f"/issues/{number}")

    def create_issue(self, title: str, body: str, labels: list) -> dict:
        return self._post("/issues", json={"title": title, "body": body, "labels": labels})

    def update_issue(self, number: int, title: str, body: str, labels: list) -> dict:
        return self._patch(f"/issues/{number}", json={"title": title, "body": body, "labels": labels})

    def list_labels(self) -> list:
        results, page = [], 1
        while True:
            try:
                batch = self._get("/labels", params={"per_page": 100, "page": page})
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    raise SystemExit(
                        f"\nERROR: Repo '{self.repo}' not found (404).\n"
                        f"  — Does the repo exist on GitHub?\n"
                        f"  — Does your GITHUB_TOKEN have access to it?\n"
                        f"  — Check the repo name: GITHUB_REPO={self.repo}\n"
                    )
                raise
            results.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return results

    def create_label(self, name: str, color: str, description: str = ""):
        try:
            self._post("/labels", json={"name": name, "color": color, "description": description})
        except requests.HTTPError:
            pass   # already exists — safe to ignore

    def delete_label(self, name: str):
        encoded = requests.utils.quote(name, safe="")
        r = self.session.delete(f"{self.base}/labels/{encoded}")
        r.raise_for_status()

    def get_file(self, repo_path: str) -> Optional[dict]:
        r = self.session.get(f"{self.base}/contents/{repo_path}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def upsert_file(self, repo_path: str, content: bytes, message: str) -> bool:
        """Create or update a file in the repo. Returns True if a write was made."""
        existing  = self.get_file(repo_path)
        encoded   = base64.b64encode(content).decode()
        new_text  = content.decode("utf-8", errors="replace")

        if existing:
            # GitHub's base64 has newlines every 60 chars; strip them before decoding
            old_text = base64.b64decode(
                existing["content"].replace("\n", "")
            ).decode("utf-8", errors="replace")
            if old_text == new_text:
                return False   # no change
            self._put(f"/contents/{repo_path}", json={
                "message": message,
                "content": encoded,
                "sha":     existing["sha"],
            })
        else:
            self._put(f"/contents/{repo_path}", json={
                "message": message,
                "content": encoded,
            })
        return True

# ─── Spec file sync ───────────────────────────────────────────────────────────

REMOVED_HEADING_RE = re.compile(r'^#{1,6}\s+~~.*~~\s*$')
HEADING_RE         = re.compile(r'^#{1,6}\s+')
HR_RE              = re.compile(r'^-{3,}\s*$')


def clean_spec_content(text: str) -> str:
    """Clean a full spec markdown file before publishing it to GitHub.

    Same rationale as clean_for_github(), applied at document scale:
    - A subsection whose heading is entirely struck through (e.g.
      "### ~~Scenario 2 — MFA code accepted~~") means the whole scenario was
      removed by a change record. The heading and everything under it, up to
      the next heading or `---` separator, is dropped rather than published —
      a developer reading the spec on GitHub shouldn't see removed scenarios.
    - Every surviving line still gets the same [CHG-xxx]/~~old~~ cleanup as
      issue text, so partially-edited lines (headings, constraints, etc.)
      keep their current wording without the change-history markup.
    """
    out = []
    skipping = False
    for line in text.splitlines():
        if skipping:
            if HEADING_RE.match(line) or HR_RE.match(line):
                skipping = False
            else:
                continue
        if REMOVED_HEADING_RE.match(line):
            skipping = True
            continue
        out.append(clean_for_github(line))
    cleaned = "\n".join(out)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)   # collapse gaps left by removed blocks
    return cleaned


def sync_spec_files(items: list, client: GitHubClient, dry_run: bool, log: logging.Logger):
    synced = 0
    for it in items:
        if not it.spec_file or not it.spec_file.exists():
            continue
        repo_path    = f"{SPECS_REPO_DIR}/{it.spec_file.name}"
        raw_text     = it.spec_file.read_text(encoding="utf-8")
        content      = clean_spec_content(raw_text).encode("utf-8")
        if dry_run:
            log.info(f"  [DRY-RUN] Would publish spec: {repo_path}")
            synced += 1
        else:
            changed = client.upsert_file(content=content, repo_path=repo_path,
                                         message=f"sync: spec for {it.id}")
            if changed:
                log.info(f"  Published spec: {repo_path}")
                synced += 1
            else:
                log.debug(f"  Spec unchanged: {repo_path}")
    if synced == 0:
        log.info("  All spec files up to date.")

# ─── Orphan detection ─────────────────────────────────────────────────────────

def detect_orphans(items: list, tracking: dict, log: logging.Logger):
    vault_ids   = {it.id for it in items}
    tracked_ids = set(tracking.get("issues", {}).keys())
    orphans     = tracked_ids - vault_ids
    if orphans:
        log.warning("  ORPHAN ISSUES — in tracking file but not found in vault:")
        for story_id in sorted(orphans):
            num = tracking["issues"][story_id]["issue_number"]
            log.warning(f"    {story_id} → issue #{num}  (NOT closed automatically — review manually)")
    else:
        log.info("  No orphans found.")
    return orphans

# ─── Sync engine ─────────────────────────────────────────────────────────────

def run_sync(items: list, client: GitHubClient, tracking: dict,
             dry_run: bool, log: logging.Logger) -> tuple:
    issues_map = tracking.setdefault("issues", {})
    created, updated, unchanged = [], [], []
    now = datetime.now(timezone.utc).isoformat()

    for it in items:
        title  = build_issue_title(it)
        body   = build_body(it, tracking, client.repo)
        labels = item_labels(it)

        if it.id in issues_map:
            num = issues_map[it.id]["issue_number"]
            if dry_run:
                log.info(f"  [DRY-RUN] UPDATE  #{num}  {it.id} — {it.title}")
                updated.append(it.id)
            else:
                existing = client.get_issue(num)
                existing_labels = {l["name"] for l in existing.get("labels", [])}
                new_labels      = set(labels)
                if (existing["title"] == title
                        and existing["body"] == body
                        and existing_labels == new_labels):
                    log.debug(f"  Unchanged #{num}  {it.id}")
                    unchanged.append(it.id)
                else:
                    client.update_issue(num, title, body, labels)
                    issues_map[it.id]["last_synced"] = now
                    log.info(f"  Updated   #{num}  {it.id} — {it.title}")
                    updated.append(it.id)
        else:
            if dry_run:
                log.info(f"  [DRY-RUN] CREATE       {it.id} — {it.title}")
                created.append(it.id)
            else:
                result = client.create_issue(title, body, labels)
                num    = result["number"]
                issues_map[it.id] = {
                    "issue_number": num,
                    "created_at":   now,
                    "last_synced":  now,
                    "url":          result["html_url"],
                }
                log.info(f"  Created   #{num}  {it.id} — {it.title}  →  {result['html_url']}")
                created.append(it.id)

    return created, updated, unchanged

# ─── Logging ─────────────────────────────────────────────────────────────────

def setup_logging(dry_run: bool) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode    = "dry-run" if dry_run else "apply"
    logfile = LOG_DIR / f"sync_{ts}_{mode}.log"

    logger = logging.getLogger("vault-sync")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s"))

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info(f"Log file: {logfile}")
    return logger

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Sync vault stories to GitHub Issues (dry-run by default)"
    )
    ap.add_argument("--apply",  action="store_true",
                    help="Execute creates/updates (without this flag: dry-run)")
    ap.add_argument("--story",  metavar="ID",
                    help="Sync a single item only, e.g. --story US-001")
    args = ap.parse_args()

    dry_run = not args.apply
    log     = setup_logging(dry_run)

    log.info(f"\n{'='*62}")
    log.info(f"  Vault → GitHub Issues sync")
    log.info(f"  Mode : {'DRY-RUN  (add --apply to execute)' if dry_run else 'APPLY'}")
    log.info(f"  Repo : {GITHUB_REPO}")
    log.info(f"  Vault: {VAULT_PATH.resolve()}")
    log.info(f"{'='*62}\n")

    # Validate config
    if not GITHUB_TOKEN:
        log.error("GITHUB_TOKEN is not set. Export it and try again.")
        log.error("  export GITHUB_TOKEN=ghp_...")
        sys.exit(1)
    if not GITHUB_REPO:
        log.error("GITHUB_REPO is not set. Export it and try again, e.g.:")
        log.error("  export GITHUB_REPO=your-org/your-repo")
        sys.exit(1)

    # Load vault
    try:
        backlog_text = load_backlog(VAULT_PATH)
    except FileNotFoundError as e:
        log.error(str(e))
        sys.exit(1)

    epic_titles = parse_epic_titles(backlog_text)
    log.info(f"Epics detected: {list(epic_titles.keys())}")

    items = parse_items(backlog_text, epic_titles, VAULT_PATH)
    log.info(f"Items to sync:  {len(items)}  "
             f"({sum(1 for i in items if i.item_type=='Story')} stories, "
             f"{sum(1 for i in items if 'Spike' in i.item_type)} spikes, "
             f"{sum(1 for i in items if i.item_type=='Enabler')} enablers)")

    # Single-story filter
    if args.story:
        target = args.story.upper()
        items  = [i for i in items if i.id == target]
        if not items:
            log.error(f"Item '{target}' not found in backlog.")
            sys.exit(1)

    tracking = load_tracking(VAULT_PATH)
    client   = GitHubClient(GITHUB_TOKEN, GITHUB_REPO)

    # 1. Bootstrap labels + remove obsolete sprint labels
    log.info("\n── Labels " + "─" * 52)
    bootstrap_labels(client, items, dry_run, log)
    cleanup_sprint_labels(client, items, dry_run, log)

    # 2. Publish spec files to /specs in the repo
    log.info("\n── Spec files " + "─" * 48)
    sync_spec_files(items, client, dry_run, log)

    # 3. Detect orphans (tracked but no longer in vault)
    log.info("\n── Orphan check " + "─" * 46)
    detect_orphans(items, tracking, log)

    # 4. Upsert issues
    log.info("\n── Issues " + "─" * 52)
    created, updated, unchanged = run_sync(items, client, tracking, dry_run, log)

    # 5. Persist tracking file
    save_tracking(VAULT_PATH, tracking, dry_run)

    # Summary
    log.info(f"\n── Summary " + "─" * 51)
    log.info(f"  Created  : {len(created):3d}  {created or ''}")
    log.info(f"  Updated  : {len(updated):3d}  {updated or ''}")
    log.info(f"  Unchanged: {len(unchanged):3d}")
    if dry_run:
        log.info(f"\n  Nothing was written. Run with --apply to execute.\n")
    else:
        log.info(f"\n  Tracking file saved: {VAULT_PATH / TRACKING_FILE}\n")


if __name__ == "__main__":
    main()
