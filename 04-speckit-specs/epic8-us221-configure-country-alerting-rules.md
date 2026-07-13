# Configure country-specific alerting rules

**Story:** US-221 — Configure country-specific alerting rules
**Epic:** EPIC-8 — Country portability & admin tools
**Traces to:** REQ-N-016, REQ-F-032
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

Alert practices can reasonably differ by country, so an admin configures who gets alerted, in what order, and at what distance for their own country rather than the team building a separate version per country.

---

## User scenarios

### Scenario 1 — Configure tier order and distances
Given the admin opens alerting-rule settings for their country, when they set the tier order and radius-band distances, then subsequent alerts in that country follow the configured order/distances.

### Scenario 2 — No override set (edge case)
Given no country-specific override is set, when an alert runs in that country, then a documented default order/distance is used rather than failing or behaving unpredictably.

---

## Constraints and assumptions

- Requires US-219 (country-scoped data visibility) and US-206 (tiered order) — this story configures the same tiering mechanism US-206 executes.
- The technical shape of this configuration is a development-team decision (OQ-005 resolved — CHG-008).

---

## Out of scope

- Language/address/emergency-number/units configuration — US-220.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Alerting-rule configuration must be read at alert time from the country's current settings — a change to the rules should apply to the next alert, not require a deployment.
