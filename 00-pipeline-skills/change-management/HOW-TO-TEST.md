# How to Test the Change Management Skill

Three test scenarios using the current CPR vault. Each one tests a different change type and a different blast radius. Run them in order — they build on each other.

---

## Before you start — install the skill

1. Open **Claude desktop → Settings → Capabilities → Skills**
2. Click "Install skill" and select `change-management.skill` from this folder
3. Restart the Cowork session so the skill is active

---

## Test 1 — Resolve an open question (small blast radius)
**What it tests:** OQ resolution, status updates, targeted blocker removal
**Expected files touched:** 5–6 files, surgical edits

This is the easiest test. OQ-004 (the N-seconds escalation timeout) is currently blocking US-008, US-011, and US-013. Resolving it unblocks those stories and should update their status lines — nothing else.

**Paste this into Claude:**

```
CHG-ID:        CHG-001
Date:          2026-07-01
Triggered by:  Stakeholder call — EMS partner (Belgium) + product owner
Change type:   OQ resolved
Affected item: OQ-004
Old value:     N-seconds escalation timeout — value unresolved, shipped as required config with no default
New value:     30 seconds for first-tier escalation, 60 seconds for second-tier escalation. Both configurable per country; these are the system defaults.
Reason:        Belgian EMS protocol requires 30-second window for certified first responders. 60-second second tier aligns with HartslagNu practice confirmed acceptable by product owner.
Resolves OQ:   OQ-004
Notes:         OQ-013 was discussed but remains open. Do not update OQ-013.
```

**What to check in the vault after:**
- `01-requirements-structured-v1.md` → OQ-004 in Section 5 should be struck through and marked RESOLVED
- `03-product-backlog-v1.md` → US-008 and US-011 status lines: OQ-004 should no longer be listed as a blocker (SPIKE-002 blocker stays)
- `03-product-backlog-v1.md` → US-013 Notes: escalation timeout should now show "30 seconds"
- `05-traceability-matrix.md` → OQ-004 row should say "RESOLVED — CHG-001"
- `06-change-log.md` → CHG-001 entry should appear at the top
- `00-project-home.md` → Recent changes section should list CHG-001
- **OQ-013 should be completely untouched** — this is the key negative check

---

## Test 2 — Modify an acceptance criterion (medium blast radius)
**What it tests:** Requirement modification, AC update, spec scenario update, change tagging
**Expected files touched:** 3–4 files

Run this after Test 1. Stakeholders have asked for a "still available?" prompt when a volunteer ignores an alert — this changes REQ-F-021 and cascades to US-013 and its spec.

**Paste this into Claude:**

```
CHG-ID:        CHG-002
Date:          2026-07-05
Triggered by:  UX review session — volunteer app team
Change type:   Requirement modified
Affected item: REQ-F-021
Old value:     The volunteer shall be able to accept or decline an alert with a single tap.
New value:     The volunteer shall be able to accept or decline an alert with a single tap. If the volunteer does not respond within 20 seconds of the notification appearing on screen, the app shall display a "Still available?" prompt before the system records a No Response status.
Reason:        User testing showed volunteers sometimes miss the notification but are still available. The 20-second prompt reduces false No Response statuses and keeps more volunteers in the active pool.
Resolves OQ:   —
Notes:         Check US-009 (live status view) — the dispatcher sees No Response; the timing now has a defined 20-second window which may affect how the status is displayed.
```

**What to check in the vault after:**
- `01-requirements-structured-v1.md` → REQ-F-021 row: new value with `[CHG-002]` tag, old value struck through
- `03-product-backlog-v1.md` → US-013: the "No Response" acceptance criterion updated with the 20-second window
- `04-speckit-specs/epic5-us013-accept-decline.md` → Scenario 4 (no response) updated to reflect 20-second prompt
- `06-change-log.md` → CHG-002 entry added above CHG-001
- **US-009, US-012, US-014 and their specs should be untouched** — check these for the negative case

---

## Test 3 — Add a new requirement (larger blast radius)
**What it tests:** New requirement handling, traceability matrix update, no accidental story creation
**Expected files touched:** 3 files + traceability matrix, NO new stories created

Run this last. Legal review has flagged a GDPR right-to-erasure requirement that wasn't in the original brief.

**Paste this into Claude:**

```
CHG-ID:        CHG-003
Date:          2026-07-10
Triggered by:  Legal review — GDPR counsel (EU deployment preparation)
Change type:   New requirement
Affected item: none (new)
Old value:     none
New value:     The system shall provide a volunteer with the ability to request deletion of their personal data. The request shall be fulfilled within 30 days, except where data must be retained to satisfy audit log obligations under applicable law.
Reason:        GDPR Article 17 (right to erasure) is mandatory for EU deployment. Flagged by legal counsel as missing from the current requirements.
Resolves OQ:   OQ-020 (partially — DPIA now has a confirmed erasure requirement, but full data field mapping still needed)
Notes:         This is a new REQ-F. It likely lands in Phase 2. Do not create a story for it — just register the requirement.
```

**What to check in the vault after:**
- `01-requirements-structured-v1.md` → A new REQ-F-037 row added in Section 2 with `[CHG-003]` tag
- `05-traceability-matrix.md` → New row for REQ-F-037 with status "Story not yet written"
- `06-change-log.md` → CHG-003 entry at the top
- `02-scope-and-context-v1.md` → OQ-020 note updated to reflect partial resolution
- **No new story in the backlog** — the skill should flag it as a follow-up, not invent it

---

## What good output looks like

After each test, the change log entry should show:
- Every file that was touched (listed)
- Every item that was *reviewed and not changed* (listed with a reason)
- Any follow-up actions clearly marked with `[ ]` checkboxes

If the skill edits something that shouldn't have changed, or misses something that should have changed, that's the feedback to improve the `SKILL.md`.

---

## How to improve the skill based on test results

1. Open `00-pipeline-skills/change-management/SKILL.md` in Obsidian
2. Find the rule that caused the wrong behaviour (usually in "How to do it — step by step" or "Common traps to avoid")
3. Edit the rule or add a new trap
4. Re-run the test
5. When the skill behaves correctly, reinstall it via Settings → Capabilities → Skills
