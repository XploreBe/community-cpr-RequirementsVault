# View volunteers

**Story:** US-006 — View volunteers
**Epic:** EPIC-1 — Incident record management (dispatcher-web)
**Traces to:** REQ-F-013
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

A dispatcher should be able to see who is registered as a volunteer in the system, even before any real matching or alerting exists. This feature shows a simple, read-only list of registered volunteers.

---

## User scenarios

### Scenario 1 — List volunteers
Given registered (mocked) volunteers exist, when the dispatcher opens the volunteers view, then each volunteer's name and tier are shown.

### Scenario 2 — Empty state
Given no volunteers exist in the mocked dataset, when the dispatcher opens the view, then an empty state is shown.

### Scenario 3 — Read-only, no position/availability
Position and availability status are not shown or actionable from this screen in Phase 1 — this view is a plain roster, not a live map of who's near a given incident (that's Phase 2 — REQ-F-006).

---

## Constraints and assumptions

- Mocked/local data source — a static or seeded list of volunteers, independent of any real sign-up flow (the volunteer-app's own Phase 1 sign-up, US-101, is a separate mock and not wired to this view).
- No auth in Phase 1.
- Built in Next.js (CON-002).

---

## Out of scope

- Filtering volunteers by distance/radius from an incident (Phase 2 — REQ-F-006).
- Any action a dispatcher could take on a volunteer from this screen (e.g. contacting them directly) — not requested.
- Certification status, expiry, or verification details (Phase 2 — REQ-F-016..018, 038).

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- Keep this view's data source swappable — it should be trivial to point it at ENABLER-003's real read endpoint later without changing the rendering logic.
