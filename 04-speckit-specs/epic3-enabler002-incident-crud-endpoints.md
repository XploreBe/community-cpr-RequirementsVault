# Basic incident CRUD endpoints

**Story:** ENABLER-002 — Basic incident CRUD endpoints
**Epic:** EPIC-3 — API & module scaffold (backend-api)
**Traces to:** REQ-F-002, REQ-F-003, REQ-F-004, REQ-F-005, REQ-F-010 (simplified), REQ-F-011, REQ-F-012 (simplified)
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

This enabler gives the Incidents + Audit module real create/list/get/update endpoints for incidents, matching the same data shape dispatcher-web's Phase 1 mock already uses (EPIC-1), so dispatcher-web can later swap its local mock for real API calls without a data-model rework.

---

## User scenarios

Framed at the API level:

### Scenario 1 — Create an incident
Given a valid payload (type, notes, optional country, location), when a client sends a create request, then a new incident is persisted with status "open" and returned with an id.

### Scenario 2 — Reject a missing location (negative)
Given a payload with no location, when a client sends a create request, then the request is rejected with a validation error — mirrors US-001's "location is required" rule.

### Scenario 3 — List incidents
Given incidents exist, when a client requests the list, then all incidents are returned (no filtering in Phase 1, mirrors US-002).

### Scenario 4 — Get a single incident
Given an incident id, when a client requests it, then its full record is returned, or a not-found response if the id doesn't exist (mirrors US-003).

### Scenario 5 — Update an incident
Given an existing incident id and a valid payload, when a client sends an update request, then the incident's fields are updated, including status, and its updated timestamp changes (mirrors US-004/US-005). Status values accepted: open, in progress, resolved, cancelled — no sequencing enforced (same open assumption as epic1-us004-update-incident.md).

### Scenario 6 — Reject clearing the location (negative)
Given an update payload that would remove the incident's location, when a client sends it, then the request is rejected — location remains required on update too.

---

## Constraints and assumptions

- No authentication on these endpoints in Phase 1 (REQ-F-001 is Phase 2) — anyone who can reach the service can call them.
- Data is stored in a datastore that is already partitioned per country (CON-007) even though Phase 1 only exercises a single country — this avoids a migration when Phase 2 enforces partitioning for real.
- Lives inside the Incidents + Audit module scaffolded by ENABLER-001.

---

## Out of scope

- Any endpoint consumed by dispatcher-web in Phase 1 — dispatcher-web's Phase 1 stories (EPIC-1) use their own local mock; wiring dispatcher-web to call these endpoints for real is a Phase 2 integration task.
- Full audit logging of every change (REQ-F-012 full is Phase 2) — only created/updated timestamps are tracked here.
- Geospatial querying (Phase 2 — REQ-F-031).

**Unresolved — dev should not implement until confirmed:**
- Whether status transitions should be sequentially enforced — see epic1-us004-update-incident.md's Scenario 3. Keep unrestricted until confirmed.

---

## Constitution snippet

- Enforce the "location is required" invariant server-side too, not only in dispatcher-web's form — a backend enabler exists precisely so this rule isn't only client-side.
- Design the incident record's shape to be extensible for Phase 2's audit trail (REQ-F-012) and status set (REQ-F-010) without a breaking schema change.
