# Accept or decline an alert

**Story:** US-103 — Accept or decline an alert
**Epic:** EPIC-2 — Alert response walking skeleton (volunteer-app)
**Traces to:** REQ-F-024, REQ-F-025
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

Once a volunteer sees an alert, they need to respond in one clear action, without friction, because every second matters. This feature lets a volunteer accept ("I'm going") or decline an alert with a single tap.

---

## User scenarios

### Scenario 1 — Accept
Given an active alert, when the volunteer taps "I'm going," then the alert's local status becomes "accepted" and a confirmation is shown.

### Scenario 2 — Decline
Given an active alert, when the volunteer taps "Decline," then the alert's local status becomes "declined" and it is removed from the active-alert screen.

### Scenario 3 — Duplicate tap is a no-op
Given an alert already marked "accepted" (or "declined"), when the volunteer taps either button again, then no duplicate action is recorded and the existing state is preserved.

---

## Constraints and assumptions

- Operates on the mocked alert from US-102 — no backend call, no notification sent to a dispatcher (there is no live dispatcher-facing status tracking yet in Phase 1; dispatcher-web's EPIC-1 does not consume volunteer responses).
- Android-only, React Native (CON-001).

---

## Out of scope

- Notifying the dispatcher of the acceptance/decline in real time (Phase 2 — REQ-F-010 full, depends on CON-005's WebSocket channel).
- Backing out after already accepting (OQ-013 resolved [CHG-014]: no — not implemented, not planned for this round).

**Unresolved — dev should not implement until confirmed:**
- None blocking. OQ-013 resolved [CHG-014]: once accepted, accepted — no back-out action in this round.

---

## Constitution snippet

- Accept and decline must each be idempotent — tapping the same action twice must never produce a different result the second time.
