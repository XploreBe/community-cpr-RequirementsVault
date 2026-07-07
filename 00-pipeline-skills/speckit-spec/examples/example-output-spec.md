# Reschedule jobs when a technician is unavailable

**Story:** US-003 — Job herplannen bij uitval
**Epic:** EPIC-1 — Centrale planning
**Traces to:** REQ-F-003
**Date:** 2026-06-18
**Produced by:** speckit-spec skill

---

## Overview

When a technician calls in sick or is otherwise unavailable for the day, the office staff (bureau) needs to quickly reassign all their jobs to other available technicians. Today this means a half-morning of phone calls. This feature allows the bureau to mark a technician as absent, see all their jobs flagged for rescheduling in one view, and reassign each job to a different available technician in seconds — without leaving the planning screen.

---

## User scenarios

### Scenario 1 — Mark a technician absent and see affected jobs
Given a technician is assigned to one or more jobs on a given day,
when the bureau marks that technician as "absent" for that day and confirms,
then all jobs assigned to that technician for that day are immediately marked with status "te herplannen" (needs rescheduling).

### Scenario 2 — Reassign a job to an available technician
Given a job has status "te herplannen",
when the bureau selects a different available technician for that job,
then the job is reassigned to the selected technician, the technician assignment is updated, and the job disappears from the "te herplannen" list.

### Scenario 3 — No available technician exists for a job
Given a job has status "te herplannen",
when the bureau opens the reassignment view and no other technician is available for that job's region and date,
then the job remains in the "te herplannen" list and a warning is shown indicating no available technician was found.

### Scenario 4 — "Te herplannen" list is empty after all jobs reassigned
Given all jobs of an absent technician have been reassigned,
when the bureau views the "te herplannen" list for that day,
then the list is empty and no warning is shown.

---

## Constraints and assumptions

- **CON-001** — Planning is centrally managed by the bureau. The system must not allow technicians to reassign jobs themselves; only bureau staff can perform this action.
- **Provisional assumption (to confirm, OQ-02/OQ-14):** "Available" means the technician is rostered that day, not marked absent, and has remaining capacity in their day plan. Specialisation and employment status (part-time, in training, former employee) are not yet filtering criteria in Phase 1 — the definition will be extended once OQ-02 and OQ-14 are resolved.
- **Depends on US-001 and US-002:** jobs must already exist and be assigned before rescheduling is possible. This spec assumes those features are in place.

---

## Out of scope

- Automatically suggesting a replacement technician (that is US-002's job — this feature only lets the bureau pick manually from the available list).
- Notifying the reassigned technician of the new job (no notification feature is in scope for Phase 1).
- Rescheduling jobs across multiple days or to a future date — Phase 1 covers same-day reassignment only.
- Bulk reassignment to a single technician in one action — not specified; would need a new requirement.

**Unresolved — dev should not implement until confirmed:**
- User roles and permissions (OQ-13) — it is assumed only bureau staff can mark technicians absent and reassign jobs, but the role definitions are not yet confirmed. The implementation should be built to support role-based access control once OQ-13 is resolved.

---

## Constitution snippet

*(Add to /speckit.constitution for this project — only if not already present)*

- Planning actions (marking absent, reassigning jobs) are bureau-only operations. The system must enforce this at the application level, not just the UI level.
- "Available" is a defined, queryable state — not a UI hint. Any feature that filters or displays available technicians must use the same shared definition.
- All planning state changes (absent marking, reassignment) must be immediately reflected in the day overview without requiring a manual refresh.
