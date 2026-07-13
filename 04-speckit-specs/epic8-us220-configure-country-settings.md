# Configure country-specific settings

**Story:** US-220 — Configure country-specific settings
**Epic:** EPIC-8 — Country portability & admin tools
**Traces to:** REQ-N-012, REQ-N-013, REQ-N-014, REQ-N-015
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

Rolling out to a new country shouldn't require a code change, so an admin can configure the basics — language, address format, emergency number, units — for their country directly.

---

## User scenarios

### Scenario 1 — Language configured
Given the admin sets the display language for their country, when it's saved, then the console and app content render in that language for users in that country.

### Scenario 2 — Address format and units configured
Given the admin sets the local address format and units of measurement, when incidents/volunteers are displayed, then addresses and distances render in that country's configured format/units.

### Scenario 3 — Emergency number configured
Given the admin sets the local emergency number, when it's referenced anywhere in the app/console, then the configured number is shown, not a hard-coded default.

### Scenario 4 — No configuration set yet (edge case)
Given a country has no configuration set yet, when a user in that country uses the system, then a documented default (not a blank or broken field) is shown for language/format/units/emergency number.

---

## Constraints and assumptions

- Requires US-219 (country-scoped data visibility) as the underlying partitioning foundation.
- The technical mechanism for this configurability (how the Countries/Config module is internally shaped) is a development-team decision (OQ-005 resolved — CHG-008) — this spec covers only the admin-facing behaviour.

---

## Out of scope

- Country-specific alerting rules (who's alerted, order, distance) — separate story, US-221.
- The internal module design for storing/applying this configuration — dev team's decision.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Every country-specific value (language, address format, emergency number, units) must be read from configuration at request time — never hard-coded anywhere in the codebase.
