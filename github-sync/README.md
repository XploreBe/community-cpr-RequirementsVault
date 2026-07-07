# Vault → GitHub Issues sync

One-way, on-demand sync from an Obsidian BA pipeline vault (see the vault's
`CLAUDE.md` / `00-pipeline-skills/`) to GitHub Issues in a repo of your choice.
Project-agnostic: it reads whatever epics, sprints, and stories your vault's
`03-product-backlog-v1.md` actually contains — nothing here is hardcoded to
a specific project.

---

## Prerequisites

- Python 3.9 or higher
- A GitHub Personal Access Token with **Issues: read/write** and **Contents: read/write**
  (fine-grained token) — or classic token with `repo` scope
- The token must have access to the target repo

---

## One-time setup

```bash
cd github-sync
pip install -r requirements.txt

# Set your token (never put this in a file)
export GITHUB_TOKEN=ghp_your_token_here

# Required — no default, set this per project
export GITHUB_REPO=your-org/your-repo
```

If your vault is not the parent of the `github-sync/` folder, set the path:

```bash
export VAULT_PATH=/path/to/your/vault
```

---

## Running the script

### Dry-run (default — always start here)

Shows exactly what would happen. Reads the vault and GitHub, writes nothing.

```bash
python vault_to_github.py
```

Example output:
```
══════════════════════════════════════════════════════════════
  Vault → GitHub Issues sync
  Mode : DRY-RUN  (add --apply to execute)
  Repo : your-org/your-repo
══════════════════════════════════════════════════════════════

Items to sync: 25  (22 stories, 2 spikes, 1 enabler)

── Labels ────────────────────────────────────────────
  [DRY-RUN] Would create label: priority:must
  ...

── Issues ────────────────────────────────────────────
  [DRY-RUN] CREATE       US-001 — Example story title
  [DRY-RUN] CREATE       US-002 — Another example story
  ...

  Nothing was written. Run with --apply to execute.
```

### Apply (creates and updates for real)

```bash
python vault_to_github.py --apply
```

### Single item

```bash
python vault_to_github.py --apply --story US-007
python vault_to_github.py --story SPIKE-001   # dry-run for one item
```

---

## What the script does (in order)

1. **Labels** — creates any missing GitHub labels (priority, type, phase, status, epic). Skips labels that already exist.
2. **Spec files** — publishes spec `.md` files from `04-speckit-specs/` to a `/specs` folder in the GitHub repo. Stories without a spec file get a placeholder note in the issue.
3. **Orphan check** — flags story IDs that are in the tracking file but no longer in the backlog. These are reported as warnings and **never closed automatically**.
4. **Issues** — for each story/spike/enabler:
   - Not yet tracked → **create** issue, save issue number to tracking file
   - Already tracked → **update** issue if title, body, or labels changed
5. **Tracking file** — saves `04-speckit-specs/.github-sync.json` with the mapping `"US-001": {"issue_number": 42, ...}`.

---

## Traceability

The stable identifier is the story ID (`US-001`, `SPIKE-001`, etc.). The mapping between story ID and GitHub issue number lives in:

```
04-speckit-specs/.github-sync.json
```

Example content after first run:
```json
{
  "version": 1,
  "last_sync": "2026-06-24T10:00:00+00:00",
  "issues": {
    "US-001": {
      "issue_number": 1,
      "created_at": "2026-06-24T10:00:00+00:00",
      "last_synced": "2026-06-24T10:00:00+00:00",
      "url": "https://github.com/your-org/your-repo/issues/1"
    },
    "US-002": { ... }
  }
}
```

Commit this file to your vault (or keep it in your vault folder). It is the source of truth for upsert logic. Without it, every run would try to create all issues again.

---

## Common workflows

### Push a new story to GitHub
1. Add the story to `03-product-backlog-v1.md` following the existing format.
2. Run dry-run to confirm: `python vault_to_github.py`
3. Apply: `python vault_to_github.py --apply`

### Update an existing story
1. Edit the story in `03-product-backlog-v1.md`.
2. Run: `python vault_to_github.py --apply`
   The script detects the change and updates the existing issue.

### Push a single updated story
```bash
python vault_to_github.py --apply --story US-007
```

### A story becomes Ready (was Not Ready)
Edit the `**Status:**` field in the backlog, run `--apply`. The script updates the issue body and swaps the label from `status:not-ready` to `status:ready`.

### A story gets a spec file (was blocked, now Ready)
Once you generate the spec file in `04-speckit-specs/`, run `--apply`. The script publishes the spec to `/specs` in the repo and updates the Spec link in the issue.

### Dependency links in issues
Issue bodies render cross-story dependencies as `#42 (US-002)` only when the target story has already been synced (its issue number is in the tracking file). If you sync all 25 items in one `--apply` run, dependencies created before their targets won't have issue numbers yet. Run `--apply` a second time after the first full run — on the second pass all issue numbers are known and dependency links will resolve correctly.

---

## Logs

Every run writes a timestamped log to `github-sync/sync-logs/`:

```
sync-logs/
  sync_20260624_100000_dry-run.log
  sync_20260624_100500_apply.log
```

The log records: every create, every update, every unchanged item, every orphan warning, and every label created.

---

## What the script never does

- Closes or deletes issues
- Syncs content from GitHub back to the vault
- Creates duplicate issues (upsert logic via tracking file)
- Writes tokens or secrets to any file
- Touches anything outside `03-product-backlog-v1.md` context (all vault edits are writes to the tracking JSON only)

---

## Scope: what gets synced

| Item type | Synced? | Rationale |
|-----------|---------|-----------|
| User stories (US-xxx) | Yes — all of them | Core backlog items |
| Spikes (SPIKE-xxx) | Yes | Concrete research deliverables the dev team must act on |
| Enablers (ENABLER-xxx) | Yes | Infrastructure tasks that other stories depend on |
| Not Ready stories | Yes, with `status:not-ready` label | Dev team needs visibility into what's blocked and why |
| Phase 2 / later-sprint stories | Yes, with the relevant `sprint:` label | Keeps the full picture in GitHub; dev team won't touch them until their sprint comes up |

---

## Troubleshooting

**`GITHUB_TOKEN is not set`** — run `export GITHUB_TOKEN=ghp_...` in your terminal session.

**`Backlog not found`** — set `VAULT_PATH` to the folder containing `03-product-backlog-v1.md`.

**`403 Forbidden` from GitHub API** — your token doesn't have the required permissions (Issues read/write + Contents read/write on the target repo).

**Dependency links show `(not yet synced)`** — run `--apply` a second time after the first full run. On the second pass all issue numbers are known.

**Orphan warning** — a story ID in `.github-sync.json` no longer exists in the backlog. The issue is NOT closed automatically. Review it manually and close if appropriate.
