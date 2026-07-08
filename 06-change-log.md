# Change Log — Community CPR Volunteer Dispatch

**Project:** Community CPR Volunteer Dispatch
**Pipeline initial run:** 2026-07-06
**Maintained by:** change-management skill

Changes are listed newest first. Each entry is permanent — never deleted or edited after creation.

---

## CHG-001 — OQ-009 resolved: patient location retention period set to 30 days
**Date:** 2026-07-08
**Triggered by:** GitHub issue opened by SaadiMoh (team discussion conclusion)
**Change type:** OQ resolved / Requirement modified
**Affected item:** OQ-009, REQ-N-010
**Old value:** OQ-009 open and unresolved — "What is the precise retention period for patient location data once an incident is closed?"; REQ-N-010 Notes: "Precise retention period not defined — see OQ-009."
**New value:** OQ-009 resolved — patient location data must be deleted no later than 30 days after incident closure; REQ-N-010 Notes updated to reflect the definitive retention period.
**Reason:** Team discussion (GitHub issue, SaadiMoh) concluded that 30 days post-closure is the definitive answer.
**Resolves:** OQ-009

### Items updated
- `01-requirements-structured-v1.md §3` — REQ-N-010 Notes column updated with the definitive 30-day retention period; "Precise retention period not defined — see OQ-009" replaced. [CHG-001]
- `01-requirements-structured-v1.md §5` — OQ-009 struck through and marked RESOLVED with one-line resolution. [CHG-001]
- `05-traceability-matrix.md §2` — REQ-N-010 row "Implemented in" column updated; "depends on OQ-009" replaced with the resolved retention period note. [CHG-001]
- `05-traceability-matrix.md §5` — OQ-009 row struck through and marked "Resolved — CHG-001". [CHG-001]

### Items reviewed — no change needed
- `03-product-backlog-v1.md` — No Phase 1 story covers REQ-N-010, and no story in the backlog references OQ-009 as a blocker. No change required.
- `04-speckit-specs/blocked-stories.md` — Only references OQ-001 and OQ-006. OQ-009 was never listed as a Phase 1 blocker. No change required.
- All `04-speckit-specs/` spec files — REQ-N-010 is Phase 2 with no spec yet written; OQ-009 does not appear in any existing spec. No change required.

### Follow-up actions required
- None. REQ-N-010 remains a Phase 2 item. When Phase 2 stories for the Privacy module are drafted, the 30-day deletion rule established by this resolution should be captured as an acceptance criterion in the relevant story/spec at that time.

---

<!-- SKILL: insert new entries above this line, newest first -->
