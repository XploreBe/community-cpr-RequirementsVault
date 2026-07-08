# Product Backlog — Community CPR Volunteer Dispatch

**Based on:** Scope & Context — CPR (condensed)
**Date:** 2026-06-17
**Produced by:** product-backlog skill
**Status:** Draft — for refinement with the team

## Legend

- **Priority:** MoSCoW (Must / Should / Could / Won't)
- **Size:** S / M / L — relative, provisional (confirm in refinement)
- **Type:** Story / Spike / Enabler
- **Status:** New · Backlog · Not Ready (reason)
- **Delivery status:** Not started · In Progress · Done — owned by the delivery team, always starts at "Not started"

## Epics

| Epic ID | Title | Outcome | Requirement IDs | Phase |
|---------|-------|---------|-----------------|-------|
| EPIC-1 | Core dispatch loop | A dispatcher can locate a patient, alert nearby volunteers, and see who responds | REQ-F-001..005, REQ-F-008, REQ-N-001 | Phase 1 |

---

## EPIC-1 — Core dispatch loop

### US-001 — Pin the patient on the map
- **Type:** Story
- **Story:** As a dispatcher, I want to place the patient's location on the map, so that the system can search for volunteers near that point.
- **Acceptance criteria:**
  - Given an active incident, when the dispatcher clicks a point on the map, then a patient marker is placed there and its latitude/longitude are stored on the incident.
  - Given a patient marker exists, when the dispatcher drags it to a new point, then the stored coordinates update to the new point.
  - Given the dispatcher types an address, when the address geocodes successfully, then the marker is placed at the geocoded coordinates.
  - Given the dispatcher types an address, when it cannot be geocoded, then an error message is shown and no marker is placed.
  - Rule: an incident has at most one patient marker at any time.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-001
- **Depends on / Blocked by:** —
- **Status:** New
- **Delivery status:** Not started

### US-002 — Find volunteers near the patient
- **Type:** Story
- **Story:** As the system, I want to identify registered volunteers near the patient's location, so that the dispatcher can alert the closest ones.
- **Acceptance criteria:** *(to be finalised once the registry exists — see blocker)*
  - Given a patient location and a search radius, when the search runs, then it returns volunteers whose last known location is within the radius, ordered by distance.
  - Given no volunteers are within the radius, when the search runs, then it returns an empty result and signals "none nearby".
- **Priority:** Must · **Size:** L (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-002
- **Depends on / Blocked by:** **Blocked** — requires a volunteer registry + sign-up (volunteers, location, availability), which is not in the requirements (see "Items sent back").
- **Status:** Not Ready — blocked on missing registry scope.
- **Delivery status:** Not started

### US-003 — Alert nearby volunteers
- **Type:** Story
- **Story:** As a dispatcher, I want to send an alert to the nearby volunteers with one action, so that they can respond to the patient.
- **Acceptance criteria:**
  - Given a set of nearby volunteers, when the dispatcher presses "Alert", then each volunteer receives a push notification containing the incident and patient location.
  - Given a volunteer's device acknowledges receipt, when the push is delivered, then the dispatcher view marks that volunteer as "notified".
  - Given a push fails to deliver to a volunteer, when the failure is detected, then that volunteer is marked "not reached" and is not counted as notified.
  - Rule: Phase 1 alerts all nearby volunteers simultaneously. *Tiered ordering (certified first, widen after a delay) is out of this story — blocked by OQ-01 (tiers) and OQ-02 (delay); a separate story when resolved.*
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-003
- **Depends on / Blocked by:** US-002 (needs the nearby set)
- **Status:** New
- **Delivery status:** Not started

### US-004 — Volunteer accepts an alert
- **Type:** Story
- **Story:** As a volunteer, I want to accept an alert with one tap, so that the dispatcher knows I'm responding.
- **Acceptance criteria:**
  - Given a volunteer received an alert, when they tap "I'm going", then their status for that incident becomes "accepted" and the dispatcher view updates within 2 seconds.
  - Given a volunteer already accepted, when the same alert is tapped again, then no duplicate acceptance is recorded.
  - Given an alert was cancelled/stood down, when the volunteer taps "I'm going", then acceptance is rejected and the app shows the incident is closed.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-004
- **Depends on / Blocked by:** US-003
- **Status:** New
- **Delivery status:** Not started
- **Notes:** Whether an explicit "decline" action is also needed is open (OQ-04). This story covers accept only; decline would be a separate story once decided — not assumed here.

### US-005 — Navigate to the scene
- **Type:** Story
- **Story:** As a volunteer who accepted, I want turn-by-turn directions to the patient, so that I can get there as fast as possible.
- **Acceptance criteria:**
  - Given a volunteer has accepted, when they open "Navigate", then Google Maps opens with the patient location as the destination.
  - Given the device has no map app available, when "Navigate" is tapped, then the patient address and coordinates are shown as fallback text.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-005 · **Constraint:** CON-002
- **Depends on / Blocked by:** US-004
- **Status:** New
- **Delivery status:** Not started

### US-006 — Stand responders down
- **Type:** Story
- **Story:** As a dispatcher, I want to stand all responders down, so that volunteers stop when EMS is on scene or the incident is over.
- **Acceptance criteria:**
  - Given an incident with responders, when the dispatcher presses "Stand down", then every notified and accepted volunteer receives a stand-down notification and the incident status becomes "closed".
  - Given an incident is closed, when a volunteer opens it, then it shows as closed and no further actions are possible.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-008
- **Depends on / Blocked by:** US-003
- **Status:** New
- **Delivery status:** Not started

### SPIKE-001 — How to deliver the alert within ~5 seconds, 95% of the time
- **Type:** Spike (timeboxed)
- **Goal:** Determine a feasible approach to wake a backgrounded/silent Android device and deliver the alert within the target, and confirm whether the target is achievable. Output: a recommended approach and any constraints.
- **Done when:** a documented recommendation and feasibility finding exist for the team to decide on.
- **Priority:** Must · **Phase/Sprint:** Phase 1 (early)
- **Traces to:** REQ-N-001, OQ-03
- **Delivery status:** Not started
- **Notes:** Written as a spike because the approach is unproven and the exact target (OQ-03) isn't confirmed; not a normal story.

---

## Items sent back (not turned into stories)

- **Volunteer registry and sign-up flow** — US-002 depends on volunteers being registered with a location and availability, but no requirement covers sign-up/registry. Sent back to the requirements step rather than invented here. US-002 stays Not Ready until this is added.

## Dependencies overview

| Story | Depends on | Reason |
|-------|-----------|--------|
| US-002 | Volunteer registry (missing scope) | Can't find volunteers who aren't registered |
| US-003 | US-002 | Needs the nearby set |
| US-004 | US-003 | Accept responds to an alert |
| US-005 | US-004 | Navigate after accepting |
| US-006 | US-003 | Stand down those alerted |

## Definition of Ready / Done

- **Ready (per story):** clear role + benefit; testable acceptance criteria incl. edge cases; provisional size; dependencies identified; no blocking open question. (US-002 is Not Ready — blocked.)
- **Done:** to be defined by the delivery team.
