# Create incident

**Story:** US-001 — Create incident
**Epic:** EPIC-1 — Incident record management (dispatcher-web)
**Traces to:** REQ-F-002, REQ-F-003, REQ-F-004
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

A dispatcher needs to register a new case the moment they learn about it, so nothing is lost while the details are still coming in over the phone. This feature lets a dispatcher open a form, describe the situation, and pin its location on a map — by clicking the map, typing coordinates, or typing an address — so the case exists as a record the team can work from.

---

## User scenarios

### Scenario 1 — Create with a map click
Given the incident form is open, when the dispatcher fills in type and notes and clicks a point on the map to set the location, then a new incident is created with status "open" and the clicked coordinates stored.

### Scenario 2 — Create with coordinates
Given the incident form is open, when the dispatcher types latitude/longitude directly instead of clicking the map, then the incident is created with those coordinates.

### Scenario 3 — Create with an address
Given the incident form is open, when the dispatcher types an address and the (mocked) geocoding step succeeds, then the incident is created using the returned coordinates.

### Scenario 4 — Missing location (negative)
Given the incident form is open, when the dispatcher submits it without setting a location by any of the three methods, then the incident is not created and a validation message states that a location is required.

### Scenario 5 — Optional country
Given the incident form is open, when the dispatcher leaves the country field blank and submits with a valid location, then the incident is still created, with country left unset.

### Scenario 6 — Single location invariant
An incident has exactly one location at creation time; the three input methods (click, coordinates, address) are alternative ways to set that one location, not three separate fields.

---

## Constraints and assumptions

- Address geocoding is mocked in Phase 1 — no real geocoding provider is called; assume any well-formed address input resolves to a coordinate pair for testing purposes.
- The `type` field on an incident has no fixed set of values yet — treat it as free text/a simple selector for now. Provisional simplification agreed with Mohamed (02-scope-and-context-v1.md §3), not a value list stated anywhere upstream.
- No authentication in Phase 1 — any user of the dispatcher-web app can create an incident (REQ-F-001/login is Phase 2, out of scope here).
- Built in Next.js (CON-002).

---

## Out of scope

- Real address geocoding (Phase 2 — depends on choosing a geocoding provider, not yet decided).
- Tiered alerting, notifying volunteers, or any live-dispatch behavior triggered by creating an incident (Phase 2 — REQ-F-006..009).
- Login/roles (Phase 2 — REQ-F-001).

**Unresolved — dev should not implement until confirmed:**
- None blocking this specific story. (Broader open questions such as OQ-001/OQ-005/OQ-006 affect other Phase 1 stories, not this one.)

---

## Constitution snippet

- Location is a required field on an incident — never allow a save without one, in this story or any later one that edits incidents.
- Keep the geocoding call isolated behind a small interface/mock boundary now, so swapping in a real provider in Phase 2 doesn't touch the form logic.
