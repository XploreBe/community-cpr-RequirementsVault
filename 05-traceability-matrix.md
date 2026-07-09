# Traceability Matrix — Community CPR Volunteer Dispatch

**Based on:** 01-requirements-structured-v1.md, 02-scope-and-context-v1.md, 03-product-backlog-v1.md, 04-speckit-specs/
**Date:** 2026-07-06
**Status:** Draft — Phase 1 only has stories/specs; Phase 2 rows show requirement IDs with no story yet.
**Last updated:** 2026-07-09 (CHG-002)

## 1. Functional Requirements → Story → Spec

| REQ-F | Short description | Repo | Phase | Epic | Story | Spec |
|-------|--------------------|------|-------|------|-------|------|
| REQ-F-001 | Login with dispatcher/supervisor/admin roles | dispatcher-web | Phase 2 | — | Not yet drafted | — |
| REQ-F-002 | Pin patient location by map click | dispatcher-web | Phase 1 (derived) | EPIC-1 | US-001, US-002, US-003 | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| REQ-F-003 | Pin patient location by address (mocked geocoding) | dispatcher-web | Phase 1 (derived) | EPIC-1 | US-001, US-002, US-003 | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| REQ-F-004 | Pin patient location by coordinates | dispatcher-web | Phase 1 (derived) | EPIC-1 | US-001, US-002, US-003 | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| REQ-F-005 | Correct/move the pin if wrong | dispatcher-web | Phase 1 (derived, via general edit) | EPIC-1 | US-002, US-003, US-004 | [[04-speckit-specs/epic1-us004-update-incident\|Spec]] |
| REQ-F-006 | See volunteers within configurable radius bands | dispatcher-web | Phase 2 | — | Not yet drafted | — |
| REQ-F-007 | Send alert with one action | dispatcher-web | Phase 2 | — | Not yet drafted | — |
| REQ-F-008 | Tiered order — certified first | dispatcher-web / backend-api | Phase 2 | — | Not yet drafted (blocked on OQ-001) | — |
| REQ-F-009 | Widen alert pool after N seconds | dispatcher-web / backend-api | Phase 2 | — | Not yet drafted (blocked on OQ-015) | — |
| REQ-F-010 | Live per-volunteer status (notified/accepted/declined/en route/arrived/stood down) | dispatcher-web | Phase 1 (simplified to open/in progress/resolved) + Phase 2 (full) | EPIC-1 | US-004, US-005 | [[04-speckit-specs/epic1-us004-update-incident\|Spec]], [[04-speckit-specs/epic1-us005-cancel-resolve-incident\|Spec]] |
| REQ-F-011 | Cancel/stand down incident | dispatcher-web | Phase 1 (simplified) + Phase 2 (full, notifies volunteers) | EPIC-1 | US-005 | [[04-speckit-specs/epic1-us005-cancel-resolve-incident\|Spec]] |
| REQ-F-012 | Full audit trail of dispatch events | dispatcher-web / backend-api | Phase 1 (simplified to timestamps) + Phase 2 (full) | EPIC-1 | US-003 | [[04-speckit-specs/epic1-us003-view-incident-detail\|Spec]] |
| REQ-F-013 | View list of registered volunteers | dispatcher-web | Phase 1 | EPIC-1 | US-006 | [[04-speckit-specs/epic1-us006-view-volunteers\|Spec]] |
| REQ-F-014 | Volunteer sign-up | volunteer-app | Phase 1 | EPIC-2 | US-101 | [[04-speckit-specs/epic2-us101-sign-up-with-tier\|Spec]] |
| REQ-F-015 | Select training tier at sign-up | volunteer-app | Phase 1 (conditional — OQ-001) | EPIC-2 | US-101 | [[04-speckit-specs/epic2-us101-sign-up-with-tier\|Spec]] |
| REQ-F-016 | Upload certification | volunteer-app | Phase 2 | — | Not yet drafted | — |
| REQ-F-017 | Track certification expiry | volunteer-app | Phase 2 | — | Not yet drafted | — |
| REQ-F-018 | Remind to re-verify certification | volunteer-app | Phase 2 | — | Not yet drafted | — |
| REQ-F-019 | Set availability (always on/scheduled/DND) | volunteer-app | Phase 2 | — | Not yet drafted | — |
| REQ-F-020 | Background location collection with consent | volunteer-app | Phase 2 | — | Not yet drafted | — |
| REQ-F-021 | Receive push alert | volunteer-app | Phase 1 (partial — in-app display only) + Phase 2 (full delivery) | EPIC-2 | US-102 | [[04-speckit-specs/epic2-us102-view-incoming-alert\|Spec]] |
| REQ-F-022 | Push bypasses silent/DND where allowed | volunteer-app | Phase 2 (blocked on OQ-004) | — | Not yet drafted | — |
| REQ-F-023 | Explicit consent record | volunteer-app / backend-api | Phase 2 | — | Not yet drafted | — |
| REQ-F-024 | Accept alert (one tap) | volunteer-app | Phase 1 | EPIC-2 | US-103 | [[04-speckit-specs/epic2-us103-accept-decline-alert\|Spec]] |
| REQ-F-025 | Decline alert (one tap) | volunteer-app | Phase 1 | EPIC-2 | US-103 | [[04-speckit-specs/epic2-us103-accept-decline-alert\|Spec]] |
| REQ-F-026 | Turn-by-turn navigation to scene | volunteer-app | Phase 1 (conditional — OQ-006) | EPIC-2 | US-104 | [[04-speckit-specs/epic2-us104-navigate-to-scene\|Spec]] |
| REQ-F-027 | In-app CPR/AED reference | volunteer-app | Phase 1 | EPIC-2 | US-105 | [[04-speckit-specs/epic2-us105-cpr-aed-reference\|Spec]] |
| REQ-F-028 | Post-event check-in — arrived | volunteer-app | Phase 1 | EPIC-2 | US-106 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| REQ-F-029 | Post-event check-in — stood down | volunteer-app | Phase 1 | EPIC-2 | US-106 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| REQ-F-030 | Post-event check-in — optional wellbeing | volunteer-app | Phase 1 | EPIC-2 | US-106 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| REQ-F-031 | Backend nearby-volunteer search | backend-api | Phase 2 (blocked on OQ-003) | — | Not yet drafted | — |
| REQ-F-032 | Backend tiered alert logic, per-country configurable | backend-api | Phase 2 (blocked on OQ-001, OQ-005) | — | Not yet drafted | — |
| REQ-F-033 | Backend sends push via FCM | backend-api | Phase 2 (blocked on OQ-004) | — | Not yet drafted | — |
| REQ-F-034 | Backend tracks push delivery status | backend-api | Phase 2 | — | Not yet drafted | — |
| REQ-F-035 | Volunteer registry (tier, cert, status, history) | backend-api | Phase 1 (partial — read-only, no history) + Phase 2 (full) | EPIC-3 | ENABLER-003 | [[04-speckit-specs/epic3-enabler003-volunteer-read-endpoint\|Spec]] |
| REQ-F-036 | Data partitioned per country/jurisdiction | backend-api | Phase 1 (datastore shaped for it, not enforced) + Phase 2 (enforced) | EPIC-3 | ENABLER-002 | [[04-speckit-specs/epic3-enabler002-incident-crud-endpoints\|Spec]] |
| REQ-F-037 | Admin tools — manage volunteers | backend-api | Phase 2 | — | Not yet drafted | — |
| REQ-F-038 | Admin tools — verify certifications | backend-api | Phase 2 | — | Not yet drafted | — |
| REQ-F-039 | Admin tools — manage in-app content | backend-api | Phase 2 | — | Not yet drafted | — |

## 2. Non-functional Requirements → Story/Enabler

None of the non-functional requirements are implemented in Phase 1 — the walking-skeleton decision (02-scope-and-context-v1.md §1) explicitly defers authentication, security, privacy enforcement, performance targets, and portability configuration to Phase 2, since Phase 1 is mocked/local data with no real backend integration.

| REQ-N | Description | Category | Implemented in |
|-------|-------------|----------|-----------------|
| REQ-N-001 | Alert reaches phone <5s, 95% of the time | Performance | Not yet — Phase 2, depends on OQ-004, OQ-015 |
| REQ-N-002 | 99.9% uptime on dispatch path | Reliability | Not yet — Phase 2 |
| REQ-N-003 | Graceful degradation if a dependency fails | Reliability | Not yet — Phase 2 |
| REQ-N-004 | Multi-country deployment without re-platforming | Scalability | Not yet — Phase 2, depends on OQ-005 |
| REQ-N-005 | MFA for dispatchers | Security | Not yet — Phase 2, paired with REQ-F-001 |
| REQ-N-006 | Encryption "everywhere" | Security | Not yet — Phase 2, depends on OQ-010 |
| REQ-N-007 | Least-privilege access control | Security | Not yet — Phase 2 |
| REQ-N-008 | Security audit logging | Security | Not yet — Phase 2 |
| REQ-N-009 | Data minimisation | Privacy | Not yet — Phase 2 |
| REQ-N-010 | Patient location retention limit | Privacy | Not yet — Phase 2, depends on OQ-009 |
| REQ-N-011 | Volunteer location only while active/opt-in | Privacy | Not yet — Phase 2, paired with REQ-F-020 |
| REQ-N-012 | Language configurable per country | Portability | Not yet — Phase 2, depends on OQ-005 |
| REQ-N-013 | Address format configurable per country | Portability | Not yet — Phase 2, depends on OQ-005 |
| REQ-N-014 | Emergency number configurable per country | Portability | Not yet — Phase 2, depends on OQ-005 |
| REQ-N-015 | Units configurable per country | Portability | Not yet — Phase 2, depends on OQ-005 |
| REQ-N-016 | Country-specific business rules configurable | Portability | Not yet — Phase 2, depends on OQ-005 |
| REQ-N-017 | Sub-second nearby-volunteer search | Performance | Not yet — Phase 2, depends on OQ-003, OQ-007 |
| REQ-N-018 | Battery-friendly background location | Performance/Usability | Not yet — Phase 2, depends on OQ-008 |

## 3. Constraints → Implementation

| CON | Constraint | Applied in |
|-----|------------|------------|
| CON-001 | React Native, Android only | EPIC-2 (all volunteer-app specs, US-101..US-106) |
| CON-002 | Next.js for dispatcher-web | EPIC-1 (all dispatcher-web specs, US-001..US-006) |
| CON-003 | Backend-api is a single-repo modular monolith with six named modules | ENABLER-001 |
| CON-004 | Volunteer-app ↔ backend over REST/HTTPS | Not yet applied — Phase 2 integration (Phase 1 volunteer-app uses local mocks, no real call) |
| CON-005 | Dispatcher-web ↔ backend over REST + WebSocket | Not yet applied — Phase 2 integration (Phase 1 dispatcher-web uses local mocks, no real call) |
| CON-006 | Push via FCM | Not yet applied — Phase 2 (REQ-F-033) |
| CON-007 | Geo-indexed, per-country-partitioned datastore | Partially applied in ENABLER-002 (datastore shaped for per-country partitioning from the start; geo-indexing itself unused until Phase 2's REQ-F-031) |
| CON-008 | Four repos, 2-dev + QA + BA team | Reflected in the Repo-tagged single-backlog structure (03-product-backlog-v1.md); e2e-tests repo excluded from this round |

## 4. Story → Requirements (reverse lookup)

| Repo | Story | Requirement IDs covered | Spec |
|------|-------|--------------------------|------|
| dispatcher-web | US-001 | REQ-F-002, REQ-F-003, REQ-F-004 — AC and spec extended with coordinate-range validation [CHG-002] | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| dispatcher-web | US-002 | REQ-F-002, REQ-F-003, REQ-F-004, REQ-F-005 | [[04-speckit-specs/epic1-us002-view-incidents\|Spec]] |
| dispatcher-web | US-003 | REQ-F-002..005, REQ-F-012 (simplified) | [[04-speckit-specs/epic1-us003-view-incident-detail\|Spec]] |
| dispatcher-web | US-004 | REQ-F-005, REQ-F-010 (simplified) — AC and spec extended with coordinate-range validation [CHG-002] | [[04-speckit-specs/epic1-us004-update-incident\|Spec]] |
| dispatcher-web | US-005 | REQ-F-011, REQ-F-010 (simplified) | [[04-speckit-specs/epic1-us005-cancel-resolve-incident\|Spec]] |
| dispatcher-web | US-006 | REQ-F-013 | [[04-speckit-specs/epic1-us006-view-volunteers\|Spec]] |
| volunteer-app | US-101 | REQ-F-014, REQ-F-015 | [[04-speckit-specs/epic2-us101-sign-up-with-tier\|Spec]] |
| volunteer-app | US-102 | REQ-F-021 (partial) | [[04-speckit-specs/epic2-us102-view-incoming-alert\|Spec]] |
| volunteer-app | US-103 | REQ-F-024, REQ-F-025 | [[04-speckit-specs/epic2-us103-accept-decline-alert\|Spec]] |
| volunteer-app | US-104 | REQ-F-026 | [[04-speckit-specs/epic2-us104-navigate-to-scene\|Spec]] |
| volunteer-app | US-105 | REQ-F-027 | [[04-speckit-specs/epic2-us105-cpr-aed-reference\|Spec]] |
| volunteer-app | US-106 | REQ-F-028, REQ-F-029, REQ-F-030 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| backend-api | ENABLER-001 | CON-003 | [[04-speckit-specs/epic3-enabler001-scaffold-modular-monolith\|Spec]] |
| backend-api | ENABLER-002 | REQ-F-002..005, 010 (simplified), 011, 012 (simplified) | [[04-speckit-specs/epic3-enabler002-incident-crud-endpoints\|Spec]] |
| backend-api | ENABLER-003 | REQ-F-035 (partial) | [[04-speckit-specs/epic3-enabler003-volunteer-read-endpoint\|Spec]] |

## 5. Open Questions → What they block

| OQ | Question (short) | Blocks |
|----|-------------------|--------|
| OQ-001 | Final volunteer tier breakdown | US-101 (Phase 1, conditional); REQ-F-008, REQ-F-032 (Phase 2) |
| OQ-002 | AED location sourcing | Future AED-fetch flow / AED registry (out of scope for now) |
| OQ-003 | Geospatial DB/indexing approach | REQ-F-031, REQ-N-017 (Phase 2); early datastore choice for ENABLER-002 |
| OQ-004 | Push delivery reliability approach | REQ-F-021 (full), REQ-F-022, REQ-F-033 (Phase 2); REQ-N-001 feasibility |
| OQ-005 | Country-abstraction technical approach | REQ-N-012..016, REQ-F-032 (Phase 2); shape of the Countries/Config module (ENABLER-001) |
| OQ-006 | Navigation provider conflict (Google Maps vs. OSM/MapLibre/OSRM) | US-104 (Phase 1, conditional); REQ-F-026 |
| OQ-007 | Precise "sub-second" definition | REQ-N-017 (Phase 2) |
| OQ-008 | Precise "battery-friendly" definition | REQ-N-018 (Phase 2) |
| OQ-009 | Patient location retention period | REQ-N-010 (Phase 2) |
| OQ-010 | Scope of "encryption everywhere" | REQ-N-006 (Phase 2) |
| OQ-011 | Role permission boundaries (dispatcher/supervisor/admin) | REQ-F-001 (Phase 2) |
| OQ-012 | Offline/connectivity handling for alerts | REQ-F-021, REQ-N-001 (Phase 2) |
| OQ-013 | Can a volunteer back out after accepting? | REQ-F-024, REQ-F-010 (Phase 2); noted as unresolved in US-103's spec |
| OQ-014 | Certification-expiry consequence; mid-incident volunteer deactivation | REQ-F-017, REQ-F-018, REQ-F-035 (Phase 2) |
| OQ-015 | Measurement of the 5s/95% target and the widening delay | REQ-N-001, REQ-F-009 (Phase 2) |
