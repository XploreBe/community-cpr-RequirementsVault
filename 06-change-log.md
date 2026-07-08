# Change Log — Community CPR Volunteer Dispatch

**Project:** Community CPR Volunteer Dispatch
**Pipeline initial run:** 2026-07-06
**Maintained by:** change-management skill

Changes are listed newest first. Each entry is permanent — never deleted or edited after creation.

---

## CHG-001 — REQ-N-018 priority elevated from Should to Must
**Date:** 2026-07-08
**Triggered by:** GitHub Issue "Vraag: prioriteit REQ-N-018", opened by SaadiMoh — client confirmation that battery-friendly background location tracking is a hard requirement
**Change type:** Requirement modified (priority change)
**Affected item:** REQ-N-018
**Old value:** Priority: `Should`
**New value:** Priority: `Must`
**Reason:** Client (SaadiMoh, GitHub Issue "Vraag: prioriteit REQ-N-018") confirmed that battery-friendly background location tracking is a hard requirement, not a nice-to-have.
**Resolves:** —

### Items updated
- `01-requirements-structured-v1.md` §3, REQ-N-018 row — Priority column changed from `Should` to `Must`; Source column updated to record client confirmation; Notes column updated to flag increased urgency of resolving OQ-008. Header bumped to `Last updated: 2026-07-08 (CHG-001)`.

### Items reviewed — no change needed
- `05-traceability-matrix.md` §2 REQ-N-018 row — the NFR table has no Priority column; the Description, Category, and "Implemented in" cells are unaffected by a priority change. No edit made.
- `03-product-backlog-v1.md` — no Phase 2 story exists for REQ-N-018; no story text, acceptance criterion, or story priority references REQ-N-018's MoSCoW priority directly. No edit made.
- `02-scope-and-context-v1.md` — REQ-N-018 appears only within block references (`REQ-N-001..018`) and is never individually named with its priority. No cell changes. No edit made.
- `04-speckit-specs/` — no spec file exists for REQ-N-018 (Phase 2, no story yet). No edit made.

### Follow-up actions required
- OQ-008 ("What precisely does 'battery-friendly' mean for background location tracking — e.g. a target sampling interval or battery-drain budget?") is now blocking a **Must**-level NFR rather than a Should. Mohamed should prioritise resolving OQ-008 with the client before Phase 2 planning for REQ-N-018 begins, since a Must-level NFR without a measurable definition cannot be verified at Done.

<!-- SKILL: insert new entries above this line, newest first -->
