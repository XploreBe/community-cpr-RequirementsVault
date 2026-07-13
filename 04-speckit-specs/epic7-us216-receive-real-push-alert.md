# Receive a real push alert via FCM

**Story:** US-216 — Receive a real push alert via FCM
**Epic:** EPIC-7 — Real push delivery
**Traces to:** REQ-F-021 (full), REQ-F-033, REQ-N-001
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

A volunteer needs to find out about a nearby incident even when the app isn't open, so this feature replaces Phase 1's in-app-only mocked alert with a real push notification.

---

## User scenarios

### Scenario 1 — Push delivered
Given a volunteer is identified as a nearby responder and an alert is sent (US-205), when the alert is dispatched, then a push notification is delivered to their device via FCM.

### Scenario 2 — Tap opens the alert
Given the volunteer taps the notification, when they do, then the app opens directly to that alert's detail screen (reusing Phase 1's US-102 display).

### Scenario 3 — App already open (edge case)
Given the volunteer already has the app open when the alert arrives, when the push is received, then the alert is shown in-app without requiring the volunteer to tap a system notification.

---

## Constraints and assumptions

- Push provider is fixed as FCM (CON-006); the technical approach to maximise delivery reliability is a development-team decision (OQ-004 resolved — CHG-007).
- Target: alert reaches the phone within 5 seconds, 95% of the time (REQ-N-001) — a design target, not a monitored/enforced number until OQ-015 is answered (see Unresolved).

---

## Out of scope

- DND/silent-mode bypass behaviour — separate story, US-217.
- Delivery status tracking — separate story, US-218.
- Behaviour when the device is offline, has no signal, or the app was force-closed by the OS — see Unresolved.

**Unresolved:**
- OQ-012 (what should happen if the volunteer's device is offline/no signal/app force-closed when an alert is sent) — do not invent retry or queueing behaviour; raise as a follow-up once answered.
- OQ-015 (how the 5s/95% target is measured/monitored in production) — build toward the target; do not build a monitoring dashboard against a guessed methodology.

---

## Constitution snippet

- Keep the alert-display component (from Phase 1's US-102) decoupled from how the alert data arrives, so swapping mocked data for a real FCM payload doesn't require rebuilding the screen.
