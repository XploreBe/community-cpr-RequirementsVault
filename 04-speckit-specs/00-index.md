# Speckit Specs — Index

All Phase 1 stories are Ready, so every Phase 1 backlog item has a spec file below. No Phase 1 items are blocked — see [[blocked-stories]] (empty; kept for future pipeline runs). US-101 and US-104 were previously Ready (conditional) but their open questions are now resolved (CHG-003, CHG-004) with no rework needed.

All 24 Phase 2 stories (EPIC-4 through EPIC-8) are also Ready and have spec files below — see 03-product-backlog-v1.md for the full backlog. Unlike Phase 1, Phase 2 has no repo tags and no enablers/spikes (one consolidated repo, spec-driven development). US-206 is Ready (conditional — rests on AS-001, not an open question); every other Phase 2 story is unconditionally Ready.

## EPIC-1 — Incident record management (dispatcher-web)

- [[epic1-us001-create-incident|US-001 — Create incident]]
- [[epic1-us002-view-incidents|US-002 — View incidents]]
- [[epic1-us003-view-incident-detail|US-003 — View incident detail]]
- [[epic1-us004-update-incident|US-004 — Update incident]]
- [[epic1-us005-cancel-resolve-incident|US-005 — Cancel / resolve incident]]
- [[epic1-us006-view-volunteers|US-006 — View volunteers]]

## EPIC-2 — Alert response walking skeleton (volunteer-app)

- [[epic2-us101-sign-up-with-tier|US-101 — Sign up with tier]]
- [[epic2-us102-view-incoming-alert|US-102 — View an incoming alert]]
- [[epic2-us103-accept-decline-alert|US-103 — Accept or decline an alert]]
- [[epic2-us104-navigate-to-scene|US-104 — Navigate to the scene]]
- [[epic2-us105-cpr-aed-reference|US-105 — CPR/AED reference]]
- [[epic2-us106-post-event-check-in|US-106 — Post-event check-in]]

## EPIC-3 — API & module scaffold (backend-api)

- [[epic3-enabler001-scaffold-modular-monolith|ENABLER-001 — Scaffold the modular monolith]]
- [[epic3-enabler002-incident-crud-endpoints|ENABLER-002 — Basic incident CRUD endpoints]]
- [[epic3-enabler003-volunteer-read-endpoint|ENABLER-003 — Basic volunteer read endpoint]]

---

## EPIC-4 — Authentication & roles (Phase 2)

- [[epic4-us201-login-with-role-based-access|US-201 — Log in with role-based access]]
- [[epic4-us202-complete-mfa-at-login|US-202 — Complete MFA at login]]
- [[epic4-us203-admin-cross-incident-oversight|US-203 — Admin: cross-incident oversight]]

## EPIC-5 — Volunteer matching & alerting (Phase 2)

- [[epic5-us204-nearby-volunteers-radius-bands|US-204 — See nearby volunteers within radius bands]]
- [[epic5-us205-send-alert-to-volunteers|US-205 — Send an alert to identified volunteers]]
- [[epic5-us206-tiered-notification-order|US-206 — Tiered notification order]] — Ready (conditional — rests on AS-001)
- [[epic5-us207-widen-alert-pool|US-207 — Widen the alert pool after a timeout]]
- [[epic5-us208-live-per-volunteer-status|US-208 — Live per-volunteer status view]]
- [[epic5-us209-full-dispatch-audit-trail|US-209 — Full dispatch audit trail]]

## EPIC-6 — Certification, availability & privacy (Phase 2)

- [[epic6-us210-upload-certification|US-210 — Upload certification documentation]]
- [[epic6-us211-track-certification-expiry|US-211 — Track certification expiry]]
- [[epic6-us212-remind-reverify-certification|US-212 — Remind volunteer to re-verify before expiry]]
- [[epic6-us213-set-availability|US-213 — Set availability]]
- [[epic6-us214-consent-background-location|US-214 — Give consent for background location collection]]
- [[epic6-us215-volunteer-status-history|US-215 — View volunteer status and certification history (admin)]]

## EPIC-7 — Real push delivery (Phase 2)

- [[epic7-us216-receive-real-push-alert|US-216 — Receive a real push alert via FCM]]
- [[epic7-us217-push-dnd-bypass|US-217 — Push alert attempts DND bypass]]
- [[epic7-us218-track-push-delivery-status|US-218 — Track push delivery status]]

## EPIC-8 — Country portability & admin tools (Phase 2)

- [[epic8-us219-country-scoped-data-visibility|US-219 — Country-scoped data visibility]]
- [[epic8-us220-configure-country-settings|US-220 — Configure country-specific settings]]
- [[epic8-us221-configure-country-alerting-rules|US-221 — Configure country-specific alerting rules]]
- [[epic8-us222-admin-manage-volunteers|US-222 — Admin manages volunteers]]
- [[epic8-us223-admin-verify-certifications|US-223 — Admin verifies volunteer certifications]]
- [[epic8-us224-admin-manage-reference-content|US-224 — Admin manages in-app reference content]]
