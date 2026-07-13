# Track certification expiry

**Story:** US-211 — Track certification expiry
**Epic:** EPIC-6 — Certification, availability & privacy
**Traces to:** REQ-F-017
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — depends on certification upload (US-210), also deferred. Kept as-is, ready to pick up later.

---

## Overview

A certification that's quietly gone stale shouldn't keep counting as valid, so the system tracks expiry dates and flags certifications once they lapse.

---

## User scenarios

### Scenario 1 — Certification expires
Given a volunteer's certification has an expiry date, when that date passes, then the certification is flagged "expired" on the volunteer's record and to any admin viewing it.

### Scenario 2 — Certification still valid
Given a certification is not yet expired, when viewed, then its status remains "valid" with the expiry date shown.

### Scenario 3 — No expiry date recorded (edge case)
Given a certification was uploaded without a machine-readable expiry date (e.g. the admin hasn't set one yet during review), when viewed, then the record shows "expiry not set" rather than silently treating it as valid indefinitely or as expired.

---

## Constraints and assumptions

- Requires US-210 (upload) — there's nothing to track expiry on until a certification exists.
- This story only covers tracking and flagging; it does not define what happens next.

---

## Out of scope

- Sending a reminder ahead of expiry — US-212.
- What happens once flagged expired (demotion, exclusion from alerts, or something else) — see Unresolved.

**Unresolved:**
- OQ-014 (what happens when a certification expires without re-verification — demoted to a lower tier, excluded from alerts entirely, or something else; and what happens to an in-flight incident if a notified/accepted volunteer's account is affected) — do not invent this behaviour. Raise a follow-up story once OQ-014 is answered.

---

## Constitution snippet

- Store expiry status as a derived/computed value from the expiry date, not a manually-set flag that can drift out of sync with the actual date.
