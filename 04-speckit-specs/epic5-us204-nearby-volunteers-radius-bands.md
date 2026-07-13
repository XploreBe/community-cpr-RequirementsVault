# See nearby volunteers within radius bands

**Story:** US-204 — See nearby volunteers within radius bands
**Epic:** EPIC-5 — Volunteer matching & alerting
**Traces to:** REQ-F-006, REQ-F-031
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

Before a dispatcher can alert anyone, they need to know who's actually nearby and available. This feature shows trained volunteers within configurable distance bands around the patient's location.

---

## User scenarios

### Scenario 1 — Volunteers grouped by radius band
Given an incident with a location set, when the dispatcher opens the nearby-volunteers view, then volunteers are listed grouped by radius band (e.g. inner/outer band), with band distances set as one simple, system-wide configuration for now.

### Scenario 2 — Do-not-disturb volunteers excluded
Given a volunteer's availability is set to "do-not-disturb," when the nearby-volunteer search runs, then that volunteer does not appear in the results.

### Scenario 3 — No volunteers nearby (edge case)
Given no volunteers are found within any configured band, when the dispatcher opens the view, then an explicit "no volunteers found nearby" state is shown, not an empty or broken list.

---

## Constraints and assumptions

- [CHG-009] Radius-band distances are one simple, system-wide configuration for now, not fixed values baked into code — but also not yet per-country (REQ-N-016 / EPIC-8 is deferred to Phase 3). Build it configurable, just not multi-country yet.
- [CHG-009] Search runs against each volunteer's registered/last-known location rather than continuous background GPS tracking — continuous location tracking and consent (US-214, REQ-F-020/023) is deferred to Phase 3. This is a stated simplification, not a silently dropped requirement.
- The geospatial database/indexing technology used to make this search fast is a development-team decision (OQ-003 resolved — CHG-006); this spec does not prescribe one.
- Performance target: search should return sub-second (REQ-N-017) — tracked as a cross-cutting NFR, see Unresolved below.

---

## Out of scope

- Sending an alert to the volunteers shown here — separate story, US-205.
- The specific database/indexing technology — dev team's decision.
- Excluding deactivated volunteer accounts — admin volunteer management (US-222) is deferred to Phase 3; until then, assume all signed-up volunteers are active.
- Per-country radius configuration — deferred to Phase 3 with the rest of country portability (US-219..221).

**Unresolved:**
- OQ-007 (precise definition of "sub-second" — under what concurrency, region size, volunteer-count assumptions) — affects how this search's performance is benchmarked. Build toward the sub-second intent; do not invent a specific benchmark methodology or number.

---

## Constitution snippet

- Keep the geospatial query behind an interface so the underlying database/indexing choice can change without rippling through the rest of the codebase.
- Read radius-band distances from configuration (even if system-wide for now), never hard-code — this keeps the door open for per-country config later without a rebuild.
