# Traceability Matrix — Community CPR Volunteer Dispatch

**Based on:** 01-requirements-structured-v1.md, 02-scope-and-context-v1.md, 03-product-backlog-v1.md, 04-speckit-specs/
**Date:** 2026-07-06
**Status:** Draft — Phase 1, Phase 2, and Phase 3 all have stories and specs now. Phase 2/3 use no repo tag (one consolidated repo) and no enablers/spikes, per the team's move to spec-driven development. **Phase 2 is now just the simple core loop (9 stories); Phase 3 (15 stories: auth/MFA, certification workflow, location consent, country portability, admin tools) is deferred but fully drafted, per CHG-009.**
**Last updated:** 2026-07-13 (CHG-003 through CHG-009; Phase 2 backlog + specs added, then rescoped)

## 1. Functional Requirements → Story → Spec

| REQ-F | Short description | Repo | Phase | Epic | Story | Spec |
|-------|--------------------|------|-------|------|-------|------|
| REQ-F-001 | Login with dispatcher/admin roles [CHG-005 — simplified from dispatcher/supervisor/admin] | — | **Phase 3** [CHG-009 — deferred] | EPIC-4 | US-201, US-203 | [[04-speckit-specs/epic4-us201-login-with-role-based-access\|Spec]], [[04-speckit-specs/epic4-us203-admin-cross-incident-oversight\|Spec]] |
| REQ-F-002 | Pin patient location by map click | dispatcher-web | Phase 1 (derived) | EPIC-1 | US-001, US-002, US-003 | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| REQ-F-003 | Pin patient location by address (mocked geocoding) | dispatcher-web | Phase 1 (derived) | EPIC-1 | US-001, US-002, US-003 | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| REQ-F-004 | Pin patient location by coordinates | dispatcher-web | Phase 1 (derived) | EPIC-1 | US-001, US-002, US-003 | [[04-speckit-specs/epic1-us001-create-incident\|Spec]] |
| REQ-F-005 | Correct/move the pin if wrong | dispatcher-web | Phase 1 (derived, via general edit) | EPIC-1 | US-002, US-003, US-004 | [[04-speckit-specs/epic1-us004-update-incident\|Spec]] |
| REQ-F-006 | See volunteers within configurable radius bands | — | Phase 2 | EPIC-5 | US-204 | [[04-speckit-specs/epic5-us204-nearby-volunteers-radius-bands\|Spec]] |
| REQ-F-007 | Send alert with one action | — | Phase 2 | EPIC-5 | US-205 | [[04-speckit-specs/epic5-us205-send-alert-to-volunteers\|Spec]] |
| REQ-F-008 | Tiered order — certified first | — | Phase 2 [CHG-003 — OQ-001 resolved] | EPIC-5 | US-206 (Ready, conditional — rests on AS-001) | [[04-speckit-specs/epic5-us206-tiered-notification-order\|Spec]] |
| REQ-F-009 | Widen alert pool after N seconds | — | Phase 2 | EPIC-5 | US-207 | [[04-speckit-specs/epic5-us207-widen-alert-pool\|Spec]] |
| REQ-F-010 | Live per-volunteer status (notified/accepted/declined/en route/arrived/stood down) | dispatcher-web | Phase 1 (simplified to open/in progress/resolved) + Phase 2 (full) | EPIC-1 (Phase 1) / EPIC-5 (Phase 2) | US-004, US-005 (Phase 1); US-208 (Phase 2 full) | [[04-speckit-specs/epic1-us004-update-incident\|Spec]], [[04-speckit-specs/epic1-us005-cancel-resolve-incident\|Spec]], [[04-speckit-specs/epic5-us208-live-per-volunteer-status\|Spec]] |
| REQ-F-011 | Cancel/stand down incident | dispatcher-web | Phase 1 (simplified) + Phase 2 (full, notifies volunteers) | EPIC-1 | US-005 | [[04-speckit-specs/epic1-us005-cancel-resolve-incident\|Spec]] |
| REQ-F-012 | Full audit trail of dispatch events | dispatcher-web / backend-api | Phase 1 (simplified to timestamps) + Phase 2 (full) | EPIC-1 (Phase 1) / EPIC-5 (Phase 2) | US-003 (Phase 1); US-209 (Phase 2 full) | [[04-speckit-specs/epic1-us003-view-incident-detail\|Spec]], [[04-speckit-specs/epic5-us209-full-dispatch-audit-trail\|Spec]] |
| REQ-F-013 | View list of registered volunteers | dispatcher-web | Phase 1 | EPIC-1 | US-006 | [[04-speckit-specs/epic1-us006-view-volunteers\|Spec]] |
| REQ-F-014 | Volunteer sign-up | volunteer-app | Phase 1 | EPIC-2 | US-101 | [[04-speckit-specs/epic2-us101-sign-up-with-tier\|Spec]] |
| REQ-F-015 | Select training tier at sign-up | volunteer-app | Phase 1 [CHG-003 — OQ-001 resolved] | EPIC-2 | US-101 | [[04-speckit-specs/epic2-us101-sign-up-with-tier\|Spec]] |
| REQ-F-016 | Upload certification | — | **Phase 3** [CHG-009 — deferred] | EPIC-6 | US-210 | [[04-speckit-specs/epic6-us210-upload-certification\|Spec]] |
| REQ-F-017 | Track certification expiry | — | **Phase 3** [CHG-009 — deferred] | EPIC-6 | US-211 (consequence of expiry still rests on OQ-014, open) | [[04-speckit-specs/epic6-us211-track-certification-expiry\|Spec]] |
| REQ-F-018 | Remind to re-verify certification | — | **Phase 3** [CHG-009 — deferred] | EPIC-6 | US-212 | [[04-speckit-specs/epic6-us212-remind-reverify-certification\|Spec]] |
| REQ-F-019 | Set availability (always on/scheduled/DND) | — | Phase 2 | EPIC-6 | US-213 | [[04-speckit-specs/epic6-us213-set-availability\|Spec]] |
| REQ-F-020 | Background location collection with consent | — | **Phase 3** [CHG-009 — deferred] | EPIC-6 | US-214 | [[04-speckit-specs/epic6-us214-consent-background-location\|Spec]] |
| REQ-F-021 | Receive push alert | volunteer-app / — | Phase 1 (partial — in-app display only) + Phase 2 (full delivery) | EPIC-2 (Phase 1) / EPIC-7 (Phase 2) | US-102 (Phase 1); US-216 (Phase 2 full) | [[04-speckit-specs/epic2-us102-view-incoming-alert\|Spec]], [[04-speckit-specs/epic7-us216-receive-real-push-alert\|Spec]] |
| REQ-F-022 | Push bypasses silent/DND where allowed | — | **Phase 3** [CHG-009 — deferred] (OQ-004 resolved — CHG-007; best-effort, no mandated mechanism) | EPIC-7 | US-217 | [[04-speckit-specs/epic7-us217-push-dnd-bypass\|Spec]] |
| REQ-F-023 | Explicit consent record | — | **Phase 3** [CHG-009 — deferred] | EPIC-6 | US-214 | [[04-speckit-specs/epic6-us214-consent-background-location\|Spec]] |
| REQ-F-024 | Accept alert (one tap) | volunteer-app | Phase 1 | EPIC-2 | US-103 | [[04-speckit-specs/epic2-us103-accept-decline-alert\|Spec]] |
| REQ-F-025 | Decline alert (one tap) | volunteer-app | Phase 1 | EPIC-2 | US-103 | [[04-speckit-specs/epic2-us103-accept-decline-alert\|Spec]] |
| REQ-F-026 | Turn-by-turn navigation to scene | volunteer-app | Phase 1 [CHG-004 — OQ-006 resolved] | EPIC-2 | US-104 | [[04-speckit-specs/epic2-us104-navigate-to-scene\|Spec]] |
| REQ-F-027 | In-app CPR/AED reference | volunteer-app | Phase 1 | EPIC-2 | US-105 | [[04-speckit-specs/epic2-us105-cpr-aed-reference\|Spec]] |
| REQ-F-028 | Post-event check-in — arrived | volunteer-app | Phase 1 | EPIC-2 | US-106 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| REQ-F-029 | Post-event check-in — stood down | volunteer-app | Phase 1 | EPIC-2 | US-106 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| REQ-F-030 | Post-event check-in — optional wellbeing | volunteer-app | Phase 1 | EPIC-2 | US-106 | [[04-speckit-specs/epic2-us106-post-event-check-in\|Spec]] |
| REQ-F-031 | Backend nearby-volunteer search | — | Phase 2 (OQ-003 resolved — CHG-006) | EPIC-5 | US-204 | [[04-speckit-specs/epic5-us204-nearby-volunteers-radius-bands\|Spec]] |
| REQ-F-032 | Backend tiered alert logic, per-country configurable | — | Phase 2 for the tiering itself (US-206, OQ-001 resolved — CHG-003); **Phase 3** [CHG-009] for per-country configurability (US-221, OQ-005 resolved — CHG-008) | EPIC-5 / EPIC-8 | US-206 (Phase 2), US-221 (Phase 3) | [[04-speckit-specs/epic5-us206-tiered-notification-order\|Spec]], [[04-speckit-specs/epic8-us221-configure-country-alerting-rules\|Spec]] |
| REQ-F-033 | Backend sends push via FCM | — | Phase 2 (OQ-004 resolved — CHG-007) | EPIC-7 | US-216 | [[04-speckit-specs/epic7-us216-receive-real-push-alert\|Spec]] |
| REQ-F-034 | Backend tracks push delivery status | — | Phase 2 | EPIC-7 | US-218 | [[04-speckit-specs/epic7-us218-track-push-delivery-status\|Spec]] |
| REQ-F-035 | Volunteer registry (tier, cert, status, history) | backend-api / — | Phase 1 (partial — read-only, no history) + **Phase 3** [CHG-009 — deferred] (full history) | EPIC-3 (Phase 1) / EPIC-6 (Phase 3) | ENABLER-003 (Phase 1); US-215 (Phase 3 full) | [[04-speckit-specs/epic3-enabler003-volunteer-read-endpoint\|Spec]], [[04-speckit-specs/epic6-us215-volunteer-status-history\|Spec]] |
| REQ-F-036 | Data partitioned per country/jurisdiction | backend-api / — | Phase 1 (datastore shaped for it, not enforced) + **Phase 3** [CHG-009 — deferred] (enforced) | EPIC-3 (Phase 1) / EPIC-8 (Phase 3) | ENABLER-002 (Phase 1); US-219 (Phase 3, enforced) | [[04-speckit-specs/epic3-enabler002-incident-crud-endpoints\|Spec]], [[04-speckit-specs/epic8-us219-country-scoped-data-visibility\|Spec]] |
| REQ-F-037 | Admin tools — manage volunteers | — | **Phase 3** [CHG-009 — deferred] | EPIC-8 | US-222 | [[04-speckit-specs/epic8-us222-admin-manage-volunteers\|Spec]] |
| REQ-F-038 | Admin tools — verify certifications | — | **Phase 3** [CHG-009 — deferred] | EPIC-8 | US-223 | [[04-speckit-specs/epic8-us223-admin-verify-certifications\|Spec]] |
| REQ-F-039 | Admin tools — manage in-app content | — | **Phase 3** [CHG-009 — deferred] | EPIC-8 | US-224 | [[04-speckit-specs/epic8-us224-admin-manage-reference-content\|Spec]] |

## 2. Non-functional Requirements → Story/Enabler

None of the non-functional requirements are implemented in Phase 1 — the walking-skeleton decision (02-scope-and-context-v1.md §1) explicitly defers authentication, security, privacy enforcement, performance targets, and portability configuration to Phase 2, since Phase 1 is mocked/local data with no real backend integration. Phase 2's backlog (03-product-backlog-v1.md) tracks these as cross-cutting constraints on specific stories rather than standalone stories — see its "Non-functional requirements — Phase 2" section.

| REQ-N | Description | Category | Implemented in |
|-------|-------------|----------|-----------------|
| REQ-N-001 | Alert reaches phone <5s, 95% of the time | Performance | Phase 2 — US-216 (rule/constraint). OQ-004 resolved (CHG-007, delegated to dev); still depends on OQ-015 for measurement methodology |
| REQ-N-002 | 99.9% uptime on dispatch path | Reliability | Phase 2 — cross-cutting constraint on EPIC-5 (US-204..209), not a standalone story |
| REQ-N-003 | Graceful degradation if a dependency fails | Reliability | Phase 2 — cross-cutting constraint on EPIC-5 and EPIC-7 (US-216, US-218) |
| REQ-N-004 | Multi-country deployment without re-platforming | Scalability | **Phase 3** [CHG-009 — deferred] — US-219, US-220. OQ-005 resolved (CHG-008, delegated to dev) |
| REQ-N-005 | MFA for dispatchers | Security | **Phase 3** [CHG-009 — deferred] — US-202, paired with REQ-F-001/US-201 (OQ-011 resolved — CHG-005) |
| REQ-N-006 | Encryption "everywhere" | Security | **Phase 3** [CHG-009 — deferred] — cross-cutting constraint on US-201 (login) and all data flows; depends on OQ-010 |
| REQ-N-007 | Least-privilege access control | Security | **Phase 3** [CHG-009 — deferred] — covered directly in US-201, US-203 acceptance criteria |
| REQ-N-008 | Security audit logging | Security | **Phase 3** [CHG-009 — deferred] — cross-cutting constraint on EPIC-4 and all admin/security actions (US-222, US-223) |
| REQ-N-009 | Data minimisation | Privacy | **Phase 3** [CHG-009 — deferred] — cross-cutting constraint on US-214 (consent) and US-210 (upload) |
| REQ-N-010 | Patient location retention limit | Privacy | Phase 2 — US-209 (rule/constraint), depends on OQ-009 |
| REQ-N-011 | Volunteer location only while active/opt-in | Privacy | **Phase 3** [CHG-009 — deferred] — US-214, paired with REQ-F-020 |
| REQ-N-012 | Language configurable per country | Portability | **Phase 3** [CHG-009 — deferred] — US-220. OQ-005 resolved (CHG-008, delegated to dev) |
| REQ-N-013 | Address format configurable per country | Portability | **Phase 3** [CHG-009 — deferred] — US-220. OQ-005 resolved (CHG-008, delegated to dev) |
| REQ-N-014 | Emergency number configurable per country | Portability | **Phase 3** [CHG-009 — deferred] — US-220. OQ-005 resolved (CHG-008, delegated to dev) |
| REQ-N-015 | Units configurable per country | Portability | **Phase 3** [CHG-009 — deferred] — US-220. OQ-005 resolved (CHG-008, delegated to dev) |
| REQ-N-016 | Country-specific business rules configurable | Portability | **Phase 3** [CHG-009 — deferred] — US-221. OQ-005 resolved (CHG-008, delegated to dev). Phase 2's US-206/US-207 use one simple system-wide config in the meantime. |
| REQ-N-017 | Sub-second nearby-volunteer search | Performance | Phase 2 — US-204 (rule/constraint). OQ-003 resolved (CHG-006, delegated to dev); still depends on OQ-007 for the precise definition |
| REQ-N-018 | Battery-friendly background location | Performance/Usability | **Phase 3** [CHG-009 — deferred] — US-214 (rule/constraint), depends on OQ-008 |

## 3. Constraints → Implementation

| CON | Constraint | Applied in |
|-----|------------|------------|
| CON-001 | React Native, Android only | EPIC-2 (all volunteer-app specs, US-101..US-106) |
| CON-002 | Next.js for dispatcher-web | EPIC-1 (all dispatcher-web specs, US-001..US-006) |
| CON-003 | Backend-api is a single-repo modular monolith with six named modules | ENABLER-001 |
| CON-004 | Volunteer-app ↔ backend over REST/HTTPS | Not yet applied — Phase 2 integration (Phase 1 volunteer-app uses local mocks, no real call) |
| CON-005 | Dispatcher-web ↔ backend over REST + WebSocket | Not yet applied — Phase 2 integration (Phase 1 dispatcher-web uses local mocks, no real call) |
| CON-006 | Push via FCM | Not yet applied — Phase 2 (REQ-F-033) |
| CON-007 | Geo-indexed, per-country-partitioned datastore | Partially applied in ENABLER-002 (datastore shaped for per-country partitioning from the start; geo-indexing itself unused until Phase 2's REQ-F-031). Specific technology delegated to dev team — OQ-003 resolved (CHG-006) |
| CON-008 | Four repos, 2-dev + QA + BA team | Reflected in Phase 1's repo-tagged single-backlog structure (03-product-backlog-v1.md); e2e-tests repo excluded from this round. **Superseded for Phase 2 onward:** the team consolidated volunteer-app/dispatcher-web/backend-api into one repository, so Phase 2 epics/stories carry no repo tag (see CLAUDE.md's Step 3 note). |

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
| — | US-201 (Phase 3, deferred [CHG-009]) | REQ-F-001, REQ-N-007 | [[04-speckit-specs/epic4-us201-login-with-role-based-access\|Spec]] |
| — | US-202 (Phase 3, deferred [CHG-009]) | REQ-N-005 | [[04-speckit-specs/epic4-us202-complete-mfa-at-login\|Spec]] |
| — | US-203 (Phase 3, deferred [CHG-009]) | REQ-F-001 | [[04-speckit-specs/epic4-us203-admin-cross-incident-oversight\|Spec]] |
| — | US-204 | REQ-F-006, REQ-F-031 | [[04-speckit-specs/epic5-us204-nearby-volunteers-radius-bands\|Spec]] |
| — | US-205 | REQ-F-007 | [[04-speckit-specs/epic5-us205-send-alert-to-volunteers\|Spec]] |
| — | US-206 | REQ-F-008, REQ-F-032 — Ready (conditional, rests on AS-001) | [[04-speckit-specs/epic5-us206-tiered-notification-order\|Spec]] |
| — | US-207 | REQ-F-009 | [[04-speckit-specs/epic5-us207-widen-alert-pool\|Spec]] |
| — | US-208 | REQ-F-010 (full) | [[04-speckit-specs/epic5-us208-live-per-volunteer-status\|Spec]] |
| — | US-209 | REQ-F-012 (full) | [[04-speckit-specs/epic5-us209-full-dispatch-audit-trail\|Spec]] |
| — | US-210 (Phase 3, deferred [CHG-009]) | REQ-F-016 | [[04-speckit-specs/epic6-us210-upload-certification\|Spec]] |
| — | US-211 (Phase 3, deferred [CHG-009]) | REQ-F-017 — consequence behaviour rests on OQ-014, open | [[04-speckit-specs/epic6-us211-track-certification-expiry\|Spec]] |
| — | US-212 (Phase 3, deferred [CHG-009]) | REQ-F-018 | [[04-speckit-specs/epic6-us212-remind-reverify-certification\|Spec]] |
| — | US-213 | REQ-F-019 | [[04-speckit-specs/epic6-us213-set-availability\|Spec]] |
| — | US-214 (Phase 3, deferred [CHG-009]) | REQ-F-020, REQ-F-023, REQ-N-011 | [[04-speckit-specs/epic6-us214-consent-background-location\|Spec]] |
| — | US-215 (Phase 3, deferred [CHG-009]) | REQ-F-035 (full) | [[04-speckit-specs/epic6-us215-volunteer-status-history\|Spec]] |
| — | US-216 | REQ-F-021 (full), REQ-F-033, REQ-N-001 | [[04-speckit-specs/epic7-us216-receive-real-push-alert\|Spec]] |
| — | US-217 (Phase 3, deferred [CHG-009]) | REQ-F-022 | [[04-speckit-specs/epic7-us217-push-dnd-bypass\|Spec]] |
| — | US-218 | REQ-F-034 | [[04-speckit-specs/epic7-us218-track-push-delivery-status\|Spec]] |
| — | US-219 (Phase 3, deferred [CHG-009]) | REQ-F-036, REQ-N-004 | [[04-speckit-specs/epic8-us219-country-scoped-data-visibility\|Spec]] |
| — | US-220 (Phase 3, deferred [CHG-009]) | REQ-N-012, REQ-N-013, REQ-N-014, REQ-N-015 | [[04-speckit-specs/epic8-us220-configure-country-settings\|Spec]] |
| — | US-221 (Phase 3, deferred [CHG-009]) | REQ-N-016, REQ-F-032 | [[04-speckit-specs/epic8-us221-configure-country-alerting-rules\|Spec]] |
| — | US-222 (Phase 3, deferred [CHG-009]) | REQ-F-037 | [[04-speckit-specs/epic8-us222-admin-manage-volunteers\|Spec]] |
| — | US-223 (Phase 3, deferred [CHG-009]) | REQ-F-038 | [[04-speckit-specs/epic8-us223-admin-verify-certifications\|Spec]] |
| — | US-224 (Phase 3, deferred [CHG-009]) | REQ-F-039 | [[04-speckit-specs/epic8-us224-admin-manage-reference-content\|Spec]] |

## 5. Open Questions → What they block

| OQ | Question (short) | Blocks |
|----|-------------------|--------|
| OQ-001 | Final volunteer tier breakdown | **Resolved — CHG-003.** Unblocked US-101 (Phase 1, no rework needed); REQ-F-008, REQ-F-032 (Phase 2) can now be scoped. |
| OQ-002 | AED location sourcing | Future AED-fetch flow / AED registry (out of scope for now) |
| OQ-003 | Geospatial DB/indexing approach | **Resolved — CHG-006.** Delegated to dev team. REQ-F-031, REQ-N-017 (Phase 2) can now be scoped; datastore choice for ENABLER-002 is a dev decision. |
| OQ-004 | Push delivery reliability approach | **Resolved — CHG-007.** Delegated to dev team; requirements focus on normal-condition delivery. REQ-F-021 (full), REQ-F-022, REQ-F-033 (Phase 2) can now be scoped; REQ-N-001 feasibility depends on OQ-015 (still open). |
| OQ-005 | Country-abstraction technical approach | **Resolved — CHG-008.** Delegated to dev team. REQ-N-012..016, REQ-F-032 (Phase 2) can now be scoped; shape of the Countries/Config module (ENABLER-001) is a dev decision. |
| OQ-006 | Navigation provider conflict (Google Maps vs. OSM/MapLibre/OSRM) | **Resolved — CHG-004.** Provider is a dev decision. Unblocked US-104 (Phase 1, no rework needed); REQ-F-026 stands as written. |
| OQ-007 | Precise "sub-second" definition | REQ-N-017, US-204 (Phase 2) — not blocking, tracked as an open cross-cutting NFR |
| OQ-008 | Precise "battery-friendly" definition | REQ-N-018, US-214 (Phase 3, deferred [CHG-009]) — not blocking, tracked as an open cross-cutting NFR |
| OQ-009 | Patient location retention period | REQ-N-010, US-209 (Phase 2) — not blocking; do not build auto-deletion against a guessed number |
| OQ-010 | Scope of "encryption everywhere" | REQ-N-006, US-201 (Phase 3, deferred [CHG-009]) — not blocking; build HTTPS-in-transit minimum, do not guess broader scope |
| OQ-011 | Role permission boundaries (dispatcher/supervisor/admin) | **Resolved — CHG-005.** Simplified to two roles (dispatcher, admin). REQ-F-001 (Phase 2) scoped as US-201/US-203. |
| OQ-012 | Offline/connectivity handling for alerts | REQ-F-021, REQ-N-001, US-216 (Phase 2) — flagged in US-216's spec as unresolved, do not invent retry/queueing behaviour |
| OQ-013 | Can a volunteer back out after accepting? | REQ-F-024, REQ-F-010, US-208 (Phase 2) — noted as unresolved in US-103's and US-208's specs |
| OQ-014 | Certification-expiry consequence; mid-incident volunteer deactivation | REQ-F-017, REQ-F-018, REQ-F-035, US-211, US-222 (Phase 3, deferred [CHG-009]) — flagged in both specs as unresolved |
| OQ-015 | Measurement of the 5s/95% target and the widening delay | REQ-N-001, REQ-F-009, US-207, US-216 (Phase 2) — flagged in both specs as unresolved |
