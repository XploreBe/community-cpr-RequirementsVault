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

### Scenario 1 — Certified tier notified first
Given nearby volunteers span more than one tier, when an alert is sent, then certified/verified CPR-BLS volunteers are notified first, ahead of the healthcare-professional and willing-but-untrained tiers.

### Scenario 2 — Single-tier case (edge case)
Given all nearby volunteers happen to be in the same tier, when an alert is sent, then they are all notified together — there is no artificial delay waiting for a "next tier" that doesn't apply.

### Scenario 3 — Country-configurable ordering
Tiering, ordering, and distance rules are configurable per country (REQ-F-032, REQ-N-016) — the tier sequence used is read from that country's configuration, not hard-coded to one fixed global order.

---

## Constraints and assumptions

- Final tier breakdown confirmed (OQ-001 resolved — CHG-003): certified/verified CPR-BLS, healthcare professional (its own separate tier), willing-but-untrained.
- Provisional assumption (to confirm with Mohamed, not resolved by CHG-003): AS-001 — whether the brief's "trained volunteers" phrase in the core flow description means the same thing as the "certified" tier. This was not addressed by the OQ-001 resolution and remains open; do not silently assume an answer beyond what's stated in 01-requirements-structured-v1.md §6.
- The technical mechanism for per-country configuration (how the Countries/Config module is shaped) is a development-team decision (OQ-005 resolved — CHG-008).

---

## Out of scope

- Sending the alert itself — US-205.
- The country-settings admin UI used to configure the order — US-221.

**Unresolved:**
- AS-001 (see above) — flag to Mohamed for explicit confirmation if it materially affects how "trained volunteers" is matched against the certified tier before building.

---

## Constitution snippet

- Read tier order and distance rules from per-country configuration at alert time — never hard-code a single global tiering sequence.
