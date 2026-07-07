# View incident detail

**Story:** US-003 — View incident detail
**Epic:** EPIC-1 — Incident record management (dispatcher-web)
**Traces to:** REQ-F-002, REQ-F-003, REQ-F-004, REQ-F-005, REQ-F-012 (simplified)
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

Before acting on a case, a dispatcher needs to see everything recorded about it in one place. This feature opens a single incident and shows its full record — type, notes, country, location, status, and when it was created/updated.

---

## User scenarios

### Scenario 1 — View full record
Given an incident exists, when the dispatcher opens it from the list or the map, then all its fields (type, notes, country, location, status, created/updated timestamps) are displayed.

### Scenario 2 — Incident not found (negative)
Given an incident id that doesn't exist (e.g. a stale link or a deleted record), when the dispatcher navigates to its detail view, then a "not found" state is shown instead of a raw error.

### Scenario 3 — Read-only
The detail view never allows editing directly; all edits happen through the update flow (US-004 / epic1-us004-update-incident).

---

## Constraints and assumptions

- Mocked/local data source — same incident set as US-001/US-002.
- Built in Next.js (CON-002).

---

## Out of scope

- Editing any field from this screen (see epic1-us004-update-incident.md).
- Volunteer response history, live status, or a full audit trail (Phase 2 — REQ-F-010 full, REQ-F-012 full).

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- Treat "not found" as a normal, handled state for any incident lookup — never let a bad id surface a raw error to the dispatcher.
