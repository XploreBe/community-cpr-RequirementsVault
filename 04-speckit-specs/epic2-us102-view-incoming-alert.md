# View an incoming alert

**Story:** US-102 — View an incoming alert
**Epic:** EPIC-2 — Alert response walking skeleton (volunteer-app)
**Traces to:** REQ-F-021 (partial — in-app display only, not delivery)
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

When a volunteer is asked to respond to a nearby patient, they need to immediately understand where and what's happening. This feature shows an incoming alert's location on a map along with any available notes — using seeded/mocked alert data rather than a real push notification.

---

## User scenarios

### Scenario 1 — Alert is shown
Given a (mocked) alert exists for this volunteer, when they open the app, then the alert screen shows the patient's approximate location on a map plus any available incident notes.

### Scenario 2 — No active alert
Given no alert is active, when the volunteer opens the app, then a neutral "no active alert" state is shown instead of an empty or broken screen.

### Scenario 3 — Not a real push (assumption, explicit)
This story only covers displaying an alert once one exists in the app's local/mocked state. It does not implement a real push notification arriving from a backend — that mechanism, including waking the device from silent/DND (REQ-F-022) and the 5-second/95% delivery target (REQ-N-001), is Phase 2 and depends on OQ-004 (push reliability approach).

---

## Constraints and assumptions

- Mocked/seeded alert data — no network call to a backend in Phase 1.
- Android-only, React Native (CON-001).

---

## Out of scope

- Real FCM push delivery and delivery tracking (Phase 2 — REQ-F-021 full, REQ-F-033, REQ-F-034).
- DND/silent-mode bypass (Phase 2 — REQ-F-022, blocked on OQ-004).
- Multiple simultaneous alerts — Phase 1 assumes at most one active mocked alert at a time; not stated as a limitation anywhere upstream, flagged here as a scoping simplification for this walking skeleton, not a product decision.

**Unresolved — dev should not implement until confirmed:**
- OQ-004 (push reliability approach) — do not attempt to build real push-wake logic against this story; it's explicitly Phase 2.

---

## Constitution snippet

- Keep the alert display component decoupled from how the alert data arrives, so swapping mocked data for a real FCM payload in Phase 2 doesn't require rebuilding this screen.
