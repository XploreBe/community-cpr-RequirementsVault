# Scaffold the modular monolith

**Story:** ENABLER-001 — Scaffold the modular monolith
**Epic:** EPIC-3 — API & module scaffold (backend-api)
**Traces to:** CON-003
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

This is a technical enabler, not a user-facing feature: it exists so that every later backend story (Phase 1's CRUD endpoints, and all of Phase 2's real logic) has a stable, agreed structure to land in, instead of each story inventing its own project layout. It sets up backend-api as a single-repo modular monolith with six named module boundaries.

---

## User scenarios

Framed at the API/system level rather than an end-user level, since this is an enabler:

### Scenario 1 — Module boundaries exist
Given a fresh checkout of backend-api, when the repository is built, then six module boundaries exist in the codebase: Auth/MFA/Roles, Volunteers + Accounts, Incidents + Audit, Geospatial, Notifications, Countries/Config.

### Scenario 2 — Modules can be empty
Given a module boundary exists, when it has no functionality yet (e.g. Geospatial, Notifications, Countries/Config in Phase 1), then it is still present as a named, empty module rather than omitted — so Phase 2 work has a clear place to go.

### Scenario 3 — Health check
Given the service is running, when a health-check endpoint is called, then it returns a success response, confirming the scaffold runs end to end.

---

## Constraints and assumptions

- Single repository, modular monolith — not microservices, not a separate repo per module (CON-003).
- No authentication is implemented at this stage (REQ-F-001/REQ-N-005 are Phase 2) — the health-check endpoint is intentionally unauthenticated.

---

## Out of scope

- Any real logic inside the Auth/MFA/Roles, Geospatial, or Notifications modules (Phase 2).
- Choosing the specific database/indexing technology (OQ-003 resolved [CHG-006] — delegated to the dev team) — this enabler defines module boundaries in code, not the datastore.

**Unresolved:**
- ~~OQ-005 (country-abstraction approach)~~ — RESOLVED [CHG-008]: delegated to the dev team. Still scaffold Countries/Config as an empty module for now — the internal design is the dev team's call, not something this enabler needs to guess at.

---

## Constitution snippet

- Module boundaries are enforced in code (e.g. no cross-module imports that bypass a public interface) from day one, even while most modules are empty — retrofitting boundaries later, once Phase 2 logic exists, is much more expensive.
- The backend stays a single deployable repo/service through Phase 1 and Phase 2 — do not split into separate services without a deliberate architectural decision.
