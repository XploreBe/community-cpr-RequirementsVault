# Widen the alert pool after a timeout

**Story:** US-207 — Widen the alert pool after a timeout
**Epic:** EPIC-5 — Volunteer matching & alerting
**Traces to:** REQ-F-009
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

If nobody in the first tier responds in time, the patient shouldn't be left waiting — the system automatically reaches out to the next broader tier.

---

## User scenarios

### Scenario 1 — Widen after timeout
Given a tier has been notified and a configurable time window (N seconds, set per country) elapses with no acceptance, when the window expires, then the next broader tier is notified.

### Scenario 2 — Acceptance just before expiry (edge case)
Given a volunteer in the original tier accepts just as the window is about to expire, when the acceptance is recorded before the window actually expires, then widening does not occur.

### Scenario 3 — Already at the broadest tier (edge case)
Given the pool has already widened to the broadest tier (willing-but-untrained) and the window expires again with no acceptance, when this happens, then the dispatcher is shown that no further widening is possible, rather than the system silently doing nothing.

---

## Constraints and assumptions

- The widening window (N) and the widening order are configurable per country, not hard-coded to one value or sequence (REQ-N-016).
- Requires US-206 (tiered order) to define the sequence being widened through.

---

## Out of scope

- The specific value of N for any given country — that's operational configuration, not something this spec fixes.
- How the 5s/95% delivery target and this widening delay are measured/monitored in production — see Unresolved.

**Unresolved:**
- OQ-015 (how the 5-second/95% delivery target and the widening delay are measured/monitored in production, and what counts as "delivered") — do not build a production monitoring/alerting dashboard against a guessed measurement methodology. The widening logic itself is not blocked by this.

---

## Constitution snippet

- Widening window and tier sequence must be read from per-country configuration, never hard-coded.
