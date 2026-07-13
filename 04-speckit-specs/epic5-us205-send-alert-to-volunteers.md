# Send an alert to identified volunteers

**Story:** US-205 — Send an alert to identified volunteers
**Epic:** EPIC-5 — Volunteer matching & alerting
**Traces to:** REQ-F-007
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

Once the dispatcher knows who's nearby, they need to reach all of them at once rather than contacting each individually. This feature sends the alert with a single action.

---

## User scenarios

### Scenario 1 — Send alert to first tier
Given the nearby-volunteers view is open with results, when the dispatcher presses "Send alert," then all volunteers in the first tier band (per US-206's ordering) receive a notification and their status becomes "notified."

### Scenario 2 — Duplicate send is idempotent (negative/edge case)
Given the dispatcher presses "Send alert" again for the same incident while it's still active, when they do, then no duplicate alert is sent to volunteers already notified.

### Scenario 3 — No volunteers available (edge case)
Given the nearby-volunteers view shows no results, when the dispatcher attempts to send an alert, then the action is disabled or rejected with a message explaining there's nobody to alert.

---

## Constraints and assumptions

- Requires US-204 (nearby volunteers) and US-206 (tiered order) to determine who receives the first send.
- The actual delivery mechanism (push notification) is covered in EPIC-7 — this story only covers triggering the send and updating status to "notified."

---

## Out of scope

- Push delivery mechanics (FCM, DND bypass, delivery tracking) — EPIC-7.
- Widening the pool after a timeout — separate story, US-207.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Treat "send alert" as an idempotent operation keyed to the incident and tier, so a double-click or retry never double-notifies a volunteer.
