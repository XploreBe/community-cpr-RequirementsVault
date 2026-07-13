# Sign up with tier

**Story:** US-101 — Sign up with tier
**Epic:** EPIC-2 — Alert response walking skeleton (volunteer-app)
**Traces to:** REQ-F-014, REQ-F-015
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

Someone willing to respond to nearby cardiac-arrest calls needs a way to register themselves and say what kind of responder they are, so the system has a record of them to work with later. This feature lets a volunteer create an account and pick a training tier.

---

## User scenarios

### Scenario 1 — Successful sign-up
Given the sign-up form, when a volunteer fills in their name/contact details, selects a tier, and submits, then a (mocked) account is created and stored on the device.

### Scenario 2 — Missing tier (negative)
Given the sign-up form, when a volunteer submits without selecting a tier, then sign-up is rejected with a "tier is required" message.

### Scenario 3 — Duplicate account (negative)
Given the sign-up form, when a volunteer submits with an identifier already used in the mocked dataset (e.g. the same email), then sign-up is rejected with a duplicate-account message.

### Scenario 4 — Confirmed tier list [CHG-003]
The tier selector offers exactly three options: certified/verified CPR-BLS, healthcare professional (its own separate tier), willing-but-untrained. This is the confirmed final list (OQ-001 resolved) — do not add, remove, or relabel options without a new change record.

---

## Constraints and assumptions

- Mocked persistence only — no real backend call, no certification upload in this story (that's Phase 2 — REQ-F-016).
- No login/auth beyond this local account creation.
- Android-only, React Native (CON-001).
- Tier list confirmed [CHG-003, OQ-001 resolved]: certified/verified CPR-BLS, healthcare professional (separate tier), willing-but-untrained.

---

## Out of scope

- Certification upload, expiry tracking, or re-verification reminders (Phase 2 — REQ-F-016, 017, 018).
- Availability modes (always on / scheduled / do-not-disturb) (Phase 2 — REQ-F-019).
- Background location collection and consent recording (Phase 2 — REQ-F-020, REQ-F-023).

**Unresolved:**
- ~~OQ-001 (final tier breakdown)~~ — RESOLVED [CHG-003]: three-tier list confirmed as given in Scenario 4, no further confirmation needed.

---

## Constitution snippet

- Treat the tier list as configuration, not a hard-coded enum baked into UI logic. Tier list is now confirmed [CHG-003], but keeping it configurable remains good practice in case tier definitions evolve later.
