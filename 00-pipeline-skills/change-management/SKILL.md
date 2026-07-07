---
name: change-management
description: Handle mid-project requirement changes in an AI-assisted BA pipeline vault. Use this whenever a requirement changes, an open question is resolved, a new requirement is added, a requirement is removed, or a stakeholder decision updates the scope. Takes a structured change record (CHG-ID, old value, new value, reason) and surgically updates only the affected items across the requirements, scope, backlog, specs, and traceability matrix — without rewriting anything else. Writes a permanent change log entry and tags every edited line with [CHG-xxx] for traceability. Use when the user says "change management", "requirement changed", "use the change-management skill", "OQ resolved", or provides a CHG-ID change record.
---

# Change Management — Pipeline Update Skill

This skill handles mid-project requirement changes. It takes a structured change record, finds every downstream item affected via the traceability matrix, makes surgical edits to only those items, and writes a permanent change log entry. Nothing is rewritten from scratch. Everything not touched stays exactly as it was.

This skill assumes the pipeline has already been run at least once and that the following files exist in the vault:
- `01-requirements-structured-v1.md` (or later version)
- `02-scope-and-context-v1.md`
- `03-product-backlog-v1.md`
- `04-speckit-specs/` folder with individual spec files
- `05-traceability-matrix.md`
- `06-change-log.md` (created by this skill on first run if absent)

---

## What this skill does and does not do

**Does:**
- Parse a structured change record (what changed, from what to what, why)
- Read the traceability matrix to identify all downstream items
- Assess whether each downstream item is *materially* affected (behaviour changes) or only *cosmetically* affected (label/wording only)
- Edit only the materially affected sections of the relevant documents
- Mark every changed passage with a `[CHG-xxx]` tag so changes are always traceable
- Write a change log entry with: what changed, why, what was updated, what was reviewed and left unchanged
- Bump the version or "last updated" line of every file that is edited
- Unblock stories whose blocker was the resolved open question (if the change resolves an OQ)

**Does not:**
- Rewrite entire documents — only the specific fields, rows, or sections that need updating
- Invent new requirements or stories — if the change implies new scope, it flags it as a new open question rather than adding content
- Resolve ambiguity in the change record — if the description is unclear, it asks before acting
- Run autonomously on multiple changes at once — one change record at a time for a clean audit trail

---

## The line this skill must not cross

A change record is not a licence to improve the documents. The skill edits only what the change requires. If it notices an unrelated issue while reading a document, it records it as an observation in the change log — it does not fix it.

---

## Change record format

The user provides a change in this format (use `assets/change-record-template.md`):

```
CHG-ID:        CHG-001
Date:          YYYY-MM-DD
Triggered by:  [stakeholder name / meeting / new decision / resolved OQ]
Change type:   [Requirement modified | New requirement | Requirement removed | Priority change | OQ resolved | Scope change | Story modified]
Affected item: [REQ-F-xxx / REQ-N-xxx / OQ-xxx / US-xxx / CON-xxx]
Old value:     [exact previous text or "none" for new items]
New value:     [exact new text or "removed" for deletions]
Reason:        [why this changed — one or two sentences]
Resolves OQ:   [OQ-xxx if this change answers an open question, else "—"]
Notes:         [anything else the BA wants to flag]
```

If the change record is incomplete or ambiguous, stop and ask for clarification before doing anything. A bad input produces bad cascades.

---

## How to do it — step by step

### 1. Assign a CHG-ID
If `06-change-log.md` exists, read it and use the next sequential ID. If it does not exist, start at CHG-001 and create the file.

### 2. Read the traceability matrix
Open `05-traceability-matrix.md`. Find every row that references the affected item ID. This is your impact list. Work through it top to bottom.

### 3. For each item on the impact list — assess materiality
Ask: does the change actually alter what this item *does*, *requires*, or *defines*? Use this rubric:

**Material** (must update):
- An acceptance criterion describes a behaviour that no longer applies
- A constraint or rule is invalidated
- A story's scope changes (e.g. a field is added, removed, or renamed)
- A spec scenario no longer matches the new requirement
- A status changes (e.g. "Not Ready — blocked on OQ-004" becomes ready because OQ-004 is now resolved)

**Cosmetic** (note and skip):
- Only a label or ID reference changes, not the meaning
- The item references the changed requirement but its content is unaffected
- The item is in a later phase and doesn't yet depend on the specific detail that changed

Record your assessment for every item — both the ones you update and the ones you deliberately skip. The change log must show that skipped items were reviewed, not ignored.

### 4. Edit affected documents — surgical only
For each materially affected item:
- Open the file
- Edit only the specific field, row, sentence, or section that needs to change
- Append `[CHG-xxx]` at the end of the changed line or section so the edit is permanently tagged
- If a table row changes, update only that row — leave all other rows intact
- If an acceptance criterion changes, update only that criterion — leave all others intact
- Bump the document header: add or update a `**Last updated:** YYYY-MM-DD (CHG-xxx)` line

**Never** rewrite a section to "improve" it while you're there. Edit the minimum.

### 5. Handle OQ resolutions specially
If the change resolves an open question (OQ-xxx):
- In `01-requirements-structured-v1.md`: find OQ-xxx in Section 5, mark it `~~OQ-xxx~~ — RESOLVED [CHG-xxx]: [one-line resolution]`
- In `05-traceability-matrix.md`: update the OQ row to show "Resolved — CHG-xxx"
- In `03-product-backlog-v1.md`: find every story that says "Not Ready — blocked on OQ-xxx" and update its status to "Ready" (or "Ready (conditional)" with the assumption stated), and add `[CHG-xxx]` to the status line
- In `04-speckit-specs/blocked-stories.md`: remove or strike through the blocker note for those stories
- The now-unblocked stories may also need spec files created — flag this in the change log as a follow-up action

### 6. Handle new requirements
If change type is "New requirement":
- Add it to `01-requirements-structured-v1.md` Section 2 (or 3/4) with a new REQ-F-xxx ID (next in sequence) and `[CHG-xxx]` in the Notes column
- Add a row to `05-traceability-matrix.md` for the new requirement with status "Story not yet written"
- Add an open scoping question to `02-scope-and-context-v1.md` Section 9 if the new requirement affects phasing
- Do NOT create a story or spec for it — that is the BA's job in the next pipeline run

### 7. Handle removed requirements
If change type is "Requirement removed":
- In `01-requirements-structured-v1.md`: strike through the requirement row and add `[CHG-xxx — REMOVED]` in the Notes column. Do not delete the row (traceability).
- In `05-traceability-matrix.md`: mark the requirement row "Removed — CHG-xxx"
- In the backlog: find the story that covers the removed requirement. If the story *only* covered that requirement, mark the story `Won't — requirement removed [CHG-xxx]`. If the story covers multiple requirements and only one is removed, update only the relevant acceptance criterion.
- In the spec file: mark the scenario `[REMOVED — CHG-xxx]` and add it to the spec's out-of-scope section.

### 8. Write the change log entry
In `06-change-log.md`, add an entry at the top (newest first):

```markdown
## CHG-xxx — [short title of what changed]
**Date:** YYYY-MM-DD
**Triggered by:** [source]
**Change type:** [type]
**Affected item:** [ID]
**Old value:** [old]
**New value:** [new]
**Reason:** [why]
**Resolves:** [OQ-xxx / —]

### Items updated
- [file/section] — [what was changed]

### Items reviewed — no change needed
- [item ID] — [why it was unaffected]

### Follow-up actions required
- [e.g. "Spec file needed for US-008 — now unblocked by CHG-001"]
```

### 9. Update the project home
In `00-project-home.md`, add a line to a "Recent changes" section (create it if absent):
```
- **CHG-xxx** (YYYY-MM-DD) — [one-line summary] → [[06-change-log]]
```

---

## Output summary

At the end, produce a brief plain-text summary in chat:
- CHG-ID assigned
- Number of files edited (list them)
- Number of items reviewed but not changed (list the IDs)
- Any follow-up actions the BA needs to take (e.g. write a new spec for an unblocked story)

---

## Common traps to avoid

- **Editing beyond the change.** If the change affects AC criterion 3 of US-013, only criterion 3 changes. Not the story title, not the other criteria, not the spec file unless a scenario directly maps to that criterion.
- **Silently skipping items.** Every item on the impact list must appear in the change log — either as "updated" or "reviewed — no change needed." No silent skips.
- **Cascading an OQ resolution too eagerly.** When an OQ is resolved, unblocked stories become "Ready" — but only write their spec files if the user explicitly asks. Flag it as a follow-up, don't auto-generate.
- **Rewriting history.** Old values are struck through or noted — never deleted. The original text must remain readable in the document.
- **Acting on an ambiguous change record.** If "old value" and "new value" are unclear, stop and ask. A vague input produces a cascade of wrong edits that are expensive to undo.
- **Changing the traceability matrix IDs.** REQ-F-xxx, US-xxx, CHG-xxx — these IDs are permanent once assigned. A changed requirement keeps its ID; only its content changes.
