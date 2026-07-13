# Remind volunteer to re-verify before expiry

**Story:** US-212 — Remind volunteer to re-verify before expiry
**Epic:** EPIC-6 — Certification, availability & privacy
**Traces to:** REQ-F-018
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — depends on certification expiry tracking (US-211), also deferred. Kept as-is, ready to pick up later.

---

## Overview

Volunteers shouldn't be surprised by an expired certification — a timely reminder gives them the chance to re-verify before it lapses.

---

## User scenarios

### Scenario 1 — Reminder sent ahead of expiry
Given a volunteer's certification is approaching its expiry date, when the reminder trigger point is reached, then the volunteer receives a reminder.

### Scenario 2 — Re-verification stops further reminders
Given a volunteer re-verifies before expiry, when they do, then no further reminders are sent for that certification cycle.

### Scenario 3 — Volunteer ignores the reminder (edge case)
Given a volunteer does not act on the reminder and the certification expires anyway, when it expires, then it follows the normal expiry flagging behaviour from US-211 — this story does not add separate consequence logic.

---

## Constraints and assumptions

- Requires US-211 (expiry tracking) — a reminder trigger point is calculated relative to the tracked expiry date.
- Provisional assumption (development team's decision, not a BA requirement): exact timing (e.g. 30/14/7 days before expiry) and channel (push, email, in-app) are not specified in the brief.

---

## Out of scope

- What happens if the volunteer never re-verifies and the certification expires — US-211 (OQ-014 resolved [CHG-017]: excluded from new alerts until re-verified, no auto-demotion).

**Unresolved:**
- None blocking. Timing/channel is intentionally left to the dev team rather than an open BA question.

---

## Constitution snippet

- Make the reminder schedule (how many days before expiry, how many reminders) configurable rather than a single hard-coded trigger point.
