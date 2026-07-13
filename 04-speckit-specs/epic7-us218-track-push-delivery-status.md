# Track push delivery status

**Story:** US-218 — Track push delivery status
**Epic:** EPIC-7 — Real push delivery
**Traces to:** REQ-F-034
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

A dispatcher watching the response unfold needs to tell "this volunteer hasn't responded" apart from "this volunteer never even got the alert," so delivery itself is tracked, not just the volunteer's reply.

---

## User scenarios

### Scenario 1 — Delivered
Given an alert has been sent to a volunteer, when delivery is confirmed, then the system records "delivered" for that volunteer/alert pair.

### Scenario 2 — Not reached
Given an alert has been sent to a volunteer, when delivery fails or cannot be confirmed, then the system records "not reached" for that volunteer/alert pair.

### Scenario 3 — Distinguished in the status view
Given a volunteer's delivery status is "not reached," when the dispatcher views that volunteer's status (US-208), then this is visibly distinguished from "notified but no response yet."

---

## Constraints and assumptions

- Requires US-216 (real push delivery) — there's nothing to track until pushes are actually being sent.
- Push provider is FCM (CON-006).

---

## Out of scope

- Automatically retrying a "not reached" delivery — not requested anywhere upstream; flag as a possible future enhancement, not built here.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Record delivery status per volunteer per alert as a distinct field from response status (accepted/declined/etc.) — never conflate "didn't respond" with "never received it."
