# Scope & Context — Community CPR Volunteer Dispatch (condensed)

**Based on:** Structured Requirements — CPR (condensed)
**Status:** Draft — proposed scope for review
*(Condensed for the backlog example.)*

## Context
- A dispatcher locates a cardiac-arrest patient and alerts nearby trained volunteers, who accept and navigate to start CPR before the ambulance.

## In scope — Phase 1 (core dispatch loop)
- **REQ-F-001** — operator pins the patient on a map.
- **REQ-F-002** — find nearby volunteers. *Blocked: needs a volunteer registry + sign-up, not in the requirements (sent back).* 
- **REQ-F-003** — send the alert to nearby volunteers. *Phase 1 = alert all nearby simultaneously; tiered ordering deferred (OQ-01/OQ-02).*
- **REQ-F-004** — volunteer accepts with one tap ("I'm going"). *Decline action open (OQ-04).*
- **REQ-F-005** — navigation to the scene (via Google Maps, CON-002).
- **REQ-F-008** — dispatcher can stand responders down.
- **REQ-N-001** — notification within ~5s, 95% of the time. *Exact target open (OQ-03); approach unproven.*

## Open questions
- OQ-01 tier breakdown TBD; OQ-02 widen delay undefined; OQ-03 exact alert-speed target; OQ-04 explicit decline action?

## Sent back to requirements
- Volunteer registry and sign-up flow — prerequisite for REQ-F-002 but not in the requirements.

## Constraints
- CON-002 navigation uses Google Maps.
