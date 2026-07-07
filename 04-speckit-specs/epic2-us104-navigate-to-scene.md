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

- Provisional assumption (to confirm): uses Google Maps per the brief's text ("fine to lean on Google Maps for this"). This does not resolve OQ-006 — the architecture diagram shows the volunteer-app's navigation edge pointing to OpenStreetMap/MapLibre/OSRM instead. If that source is confirmed as the actual intended provider, this scenario needs to be rebuilt, not just reconfigured.
- Android-only, React Native (CON-001).

---

## Out of scope

- In-app turn-by-turn rendering — this story hands off to an external maps app/intent, it does not build its own navigation UI.
- Live rerouting or tracking the volunteer's progress toward the scene (not requested anywhere upstream).

**Unresolved — dev should not implement until confirmed:**
- OQ-006 (navigation provider conflict) — affects Scenario 1 directly. Implement against Google Maps as stated, but keep the maps integration isolated behind a small interface so switching providers later doesn't ripple through the rest of the app.

---

## Constitution snippet

- Isolate the maps-provider integration behind an interface — OQ-006 is unresolved and a provider switch is a real possibility, not a hypothetical.
