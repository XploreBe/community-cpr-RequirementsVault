# View incidents

**Story:** US-002 — View incidents
**Epic:** EPIC-1 — Incident record management (dispatcher-web)
**Traces to:** REQ-F-002, REQ-F-003, REQ-F-004, REQ-F-005
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

A dispatcher needs a quick overview of what's currently registered, so they can see the whole picture at a glance instead of hunting for individual records. This feature shows every incident both as a list and as markers on a map, using the same mocked data source as the rest of Phase 1.

---

## User scenarios

### Scenario 1 — Incidents shown in both views
Given incidents exist, when the dispatcher opens the incidents overview, then every incident appears both in a list and as a marker on the map.

### Scenario 2 — Empty state
Given no incidents exist, when the dispatcher opens the overview, then an empty state is shown instead of a blank list and blank map.

### Scenario 3 — List and map stay in sync
Given the incident set changes (one is created, edited, or resolved elsewhere in the app), when the dispatcher is on the overview, then both the list and the map reflect the current set — Phase 1 has no separate filtering that could make them diverge.

---

## Constraints and assumptions

- Mocked/local data source — no real backend call in Phase 1 (dispatcher-web's own mock, per the walking-skeleton decision, 02-scope-and-context-v1.md §1).
- No filtering, sorting, or search in Phase 1 — the overview always shows the full set.
- Built in Next.js (CON-002).

---

## Out of scope

- Filtering by status, distance, or any other attribute (not requested for Phase 1).
- Real-time updates pushed from a backend (Phase 2 — depends on CON-005's WebSocket channel, not built yet).
- Anything related to alerting or volunteer response status.

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- List and map views must always read from the same underlying data — don't let them drift by maintaining separate copies of the incident set.
