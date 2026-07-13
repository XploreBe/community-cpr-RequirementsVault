# Admin manages volunteers

**Story:** US-222 — Admin manages volunteers
**Epic:** EPIC-8 — Country portability & admin tools
**Traces to:** REQ-F-037
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — admin tooling; admin (US-203) is deferred. Kept as-is, ready to pick up later.

---

## Overview

The volunteer pool needs upkeep, so an admin can view volunteer details and activate or deactivate accounts as needed.

---

## User scenarios

### Scenario 1 — View and toggle a volunteer
Given the admin opens the volunteer management view, when they select a volunteer, then they can view full details and toggle the account between active and deactivated.

### Scenario 2 — Deactivated volunteer excluded from search
Given a volunteer is deactivated, when a nearby-volunteer search runs (US-204), then that volunteer is excluded from results.

### Scenario 3 — Deactivating a volunteer mid-incident (edge case)
Given a volunteer is currently notified or has accepted an active incident, when an admin deactivates their account, then the deactivation is recorded — see Unresolved for what, if anything, happens to the in-flight incident.

---

## Constraints and assumptions

- Admin-only (least-privilege, REQ-N-007).

---

## Out of scope

- Automatically resolving or reassigning an in-flight incident when a responding volunteer is deactivated — see Unresolved.

**Unresolved:**
- None blocking. OQ-014 resolved [CHG-017]: an in-flight incident is never interrupted — a volunteer already notified/accepted stays active on that incident even if an admin deactivates their account mid-response. No auto-widening or auto-reassignment triggered by the deactivation.

---

## Constitution snippet

- Deactivation must take effect immediately in the next nearby-volunteer search — no caching that could alert an already-deactivated volunteer.
