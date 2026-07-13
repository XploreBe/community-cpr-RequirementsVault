# Tiered notification order

**Story:** US-206 — Tiered notification order
**Epic:** EPIC-5 — Volunteer matching & alerting
**Traces to:** REQ-F-008, REQ-F-032
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

The most qualified volunteers should get the first chance to respond, so the alert reaches certified responders before it reaches less-trained tiers.

---

## User scenarios

### Scenario 1 — Trained tier notified first [CHG-010]
Given nearby volunteers span more than one tier, when an alert is sent, then certified/verified CPR-BLS **and** healthcare-professional volunteers are notified together, in the first wave, ahead of the willing-but-untrained tier. AS-001 resolved [CHG-010]: "trained volunteers" means these two tiers combined, not certified alone.

### Scenario 2 — Single-tier case (edge case)
Given all nearby volunteers happen to be in the same tier, when an alert is sent, then they are all notified together — there is no artificial delay waiting for a "next tier" that doesn't apply.

### Scenario 3 — Configurable ordering
Tiering and ordering rules are configurable (REQ-F-032) rather than hard-coded in application logic — read from one simple, system-wide configuration for now.

---

## Constraints and assumptions

- Final tier breakdown confirmed (OQ-001 resolved — CHG-003): certified/verified CPR-BLS, healthcare professional (its own separate tier), willing-but-untrained.
- AS-001 resolved [CHG-010]: "trained volunteers" (the first notified wave) means certified/verified CPR-BLS **and** healthcare professional combined, not certified alone. Willing-but-untrained is reached only via widening (US-207).
- [CHG-009] Per-country configurability (REQ-N-016) is deferred to Phase 3 along with the rest of country portability — build one system-wide tier order/config for now, not a per-country one.

---

## Out of scope

- Sending the alert itself — US-205.
- Per-country configuration of tier order — deferred to Phase 3 (US-219..221).

**Unresolved:**
- None blocking. AS-001 resolved [CHG-010] — see Constraints above.

---

## Constitution snippet

- Read tier order and distance rules from one system-wide configuration for now [CHG-009] — per-country configurability is deferred to Phase 3 (US-221); do not hard-code values inline in alert-send logic even for a single config, since that's what US-221 will later replace.
