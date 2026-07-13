# Push alert attempts DND bypass

**Story:** US-217 — Push alert attempts DND bypass
**Epic:** EPIC-7 — Real push delivery
**Traces to:** REQ-F-022
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — a best-effort enhancement on top of basic push (US-216, which stays in Phase 2). Kept as-is, ready to pick up later.

---

## Overview

A phone on silent shouldn't be the reason a volunteer misses a nearby cardiac-arrest call, so the alert makes a best effort to get through even in do-not-disturb mode.

---

## User scenarios

### Scenario 1 — Bypass succeeds where platform allows
Given the volunteer's device is in silent/DND mode and platform settings allow an override, when an alert is sent, then the notification attempts to bypass silent/DND.

### Scenario 2 — Bypass not possible (edge case)
Given the platform or the volunteer's own settings do not allow an override, when an alert is sent, then the notification is still delivered through the normal channel without erroring, even if it doesn't audibly interrupt DND.

---

## Constraints and assumptions

- Best-effort, "Should"-priority requirement, not a guarantee (REQ-F-022).
- The specific technical mechanism for maximising DND-bypass reliability is delegated to the development team (OQ-004 resolved — CHG-007) — this spec does not prescribe one.
- Depends on US-216 (the underlying push delivery this behaviour modifies).

---

## Out of scope

- Guaranteeing delivery in all DND configurations — explicitly best-effort, not a hard requirement.

**Unresolved:**
- None blocking. The mechanism is intentionally left to the dev team rather than an open BA question.

---

## Constitution snippet

- Never let a failed DND-bypass attempt block or delay the underlying notification from being delivered through the normal channel.
