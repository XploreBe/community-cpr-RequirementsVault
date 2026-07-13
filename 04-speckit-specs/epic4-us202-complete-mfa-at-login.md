# Complete MFA at login

**Story:** US-202 — Complete MFA at login
**Epic:** EPIC-4 — Authentication & roles
**Traces to:** REQ-N-005
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — not part of the current Phase 2 round. Kept as-is, ready to pick up once basic login (US-201) is prioritized.

---

## Overview

A password alone isn't enough protection for accounts that can dispatch real emergency responders, so every dispatcher and admin confirms their identity with a second step before reaching the console.

---

## User scenarios

### Scenario 1 — Second factor requested
Given correct credentials, when the user submits them, then they are prompted for a second verification factor before reaching the console.

### Scenario 2 — Correct second factor
Given a correct second factor is submitted, when it's verified, then the user reaches the console.

### Scenario 3 — Incorrect second factor (negative)
Given an incorrect second factor is submitted, when it's checked, then access is denied and the user may retry.

### Scenario 4 — No opt-out
Every dispatcher and admin account requires MFA; there is no account-level setting to disable it.

---

## Constraints and assumptions

- MFA applies to every dispatcher and admin account without exception (REQ-N-005).
- Provisional assumption (to confirm with the dev team, not a BA decision): the specific second-factor mechanism (SMS code, authenticator app, email code, etc.) is not specified by requirements — the development team chooses, consistent with how OQ-003/004/005/006 were resolved (technical implementation left to the dev team).

---

## Out of scope

- The underlying login/credentials step — covered in US-201.
- Choosing the specific MFA technology/provider — development team's decision, not specified here.

**Unresolved:**
- None blocking. The MFA mechanism itself is intentionally left open to the dev team rather than an unanswered BA question.

---

## Constitution snippet

- Treat the second-factor mechanism as swappable configuration, not a hard-coded single provider, in case the dev team's chosen mechanism changes later.
