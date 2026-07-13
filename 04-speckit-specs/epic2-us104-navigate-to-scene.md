# Navigate to the scene

**Story:** US-104 — Navigate to the scene
**Epic:** EPIC-2 — Alert response walking skeleton (volunteer-app)
**Traces to:** REQ-F-026
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

Once a volunteer has committed to responding, they need to get to the patient as quickly as possible. This feature hands off to a maps app with turn-by-turn directions to the (mocked) patient location.

---

## User scenarios

### Scenario 1 — Open navigation
Given a volunteer has accepted an alert, when they tap "Navigate," then a Google Maps deep link opens with the patient's coordinates as the destination.

### Scenario 2 — No maps app available (edge case)
Given no maps app is available on the device, when "Navigate" is tapped, then the coordinates/address are shown as fallback text instead of the action failing silently.

### Scenario 3 — Only reachable after accepting
"Navigate" is only offered once a volunteer has accepted the alert (via US-103) — declined or not-yet-responded alerts do not expose this action.

---

## Constraints and assumptions

- Uses Google Maps per the brief's text ("fine to lean on Google Maps for this"). OQ-006 is resolved [CHG-004]: navigation provider is a development-team implementation choice, not a fixed requirement — Google Maps as already built stands, no rework required.
- Android-only, React Native (CON-001).

---

## Out of scope

- In-app turn-by-turn rendering — this story hands off to an external maps app/intent, it does not build its own navigation UI.
- Live rerouting or tracking the volunteer's progress toward the scene (not requested anywhere upstream).

**Unresolved:**
- ~~OQ-006 (navigation provider conflict)~~ — RESOLVED [CHG-004]: provider is a dev decision, Google Maps as already built stands, no rework needed.

---

## Constitution snippet

- Isolate the maps-provider integration behind an interface. Provider is now a confirmed dev decision [CHG-004] rather than a fixed requirement, so keeping it swappable remains good practice if the dev team ever wants to change it.
