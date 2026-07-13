# Scope & Context — Community CPR Volunteer Dispatch

**Based on:** 01-requirements-structured-v1.md
**Date:** 2026-07-06
**Produced by:** scope-and-context skill
**Status:** Draft — proposed scope for review

## 1. Context

- **Problem:** Bystander CPR in the first 3–4 minutes of a cardiac arrest more than doubles survival, but ambulances take 7–10 minutes. Nobody currently connects a 911/112 dispatcher to nearby trained volunteers who could start CPR sooner.
- **Goal:** A dispatcher can pin a patient and alert nearby volunteers within seconds; a volunteer can accept in one tap and get to the scene; certified volunteers are prioritised but untrained bystanders can still be reached; the system is portable to a new country without a rewrite.
- **Stakeholders:** Mohamed (BA/product owner for this pipeline), a 2-developer + QA + BA delivery team (per the architecture diagram's subtitle), 911/112 dispatchers and admins (console users — roles confirmed per OQ-011 [RESOLVED CHG-005]), volunteers (app users), and — indirectly — EMS services. No tension between stakeholders is recorded; the navigation-provider question (OQ-006) is resolved [CHG-004] — provider is a dev decision, not a stakeholder conflict.
- **As-is:** Greenfield project. No existing system; the brief references comparable external systems (HartslagNu, GoodSAM, PulsePoint, Mobile Save, Staying Alive) as prior art, not as something being replaced.

**Team decision carried into this document (not an analyst proposal):** Mohamed confirmed, in the kickoff conversation on 2026-07-06, that Phase 1 across all three product repositories (volunteer-app, dispatcher-web, backend-api) is a **walking skeleton**: each repo ships a small, working, end-to-end slice built against mocked data/dependencies, with no login/auth and no real cross-repo integration yet. Backend-api's Phase 1 slice is itself real code (simple CRUD-style endpoints, no auth, no geospatial/tiered-alert/push logic) — its endpoints are not necessarily called by the frontends yet in Phase 1, since the frontends are also working against their own mocks in parallel. Real cross-repo integration, authentication, and the core dispatch/alerting logic are Phase 2, not Phase 1. This decision **fixes the shape of Phase 1** below; it is not something this document proposes or could reasonably override — where a requirement conflicts with this constraint (e.g. REQ-N-005 MFA, REQ-F-001 login), it is deferred to Phase 2 for that reason alone, stated explicitly per item.

The e2e-tests repository shown in the architecture diagram is excluded from this scope/backlog round, per the same conversation — deferred, not out of scope permanently.

## 2. Scope-overzicht (at a glance)

| Fase | Repo | Thema | Requirement-IDs | Korte motivatie |
|------|------|-------|-----------------|-----------------|
| Fase 1 | dispatcher-web | Incident record management (no login, mocked data) | REQ-F-002..005, 010 (simplified), 011, 012 (simplified), 013 | Smallest end-to-end slice: create/view/update/resolve an incident and browse volunteers, no auth, no real alerting. Matches Mohamed's example stories directly. |
| Fase 1 | volunteer-app | Alert response walking skeleton (no login, mocked data) | REQ-F-014, 015 [CHG-003], 024, 025, 026 [CHG-004], 027, 028, 029, 030 | Sign up, see a mocked alert, accept/decline, navigate, reference material, post-event check-in — no real push, no cert workflow yet. |
| Fase 1 | backend-api | API & module scaffold | CON-003 (module scaffold), REQ-F-035 (partial, read-only) | Modular-monolith skeleton plus minimal CRUD endpoints for incidents and a read endpoint for volunteers — no auth, no geospatial/alert/push logic. |
| Fase 2 | all three | Core dispatch loop + integration | REQ-F-001, 006, 007, 008, 009, 010 (full), 012 (full), 016, 017, 018, 019, 020, 021, 022, 023, 031, 032, 033, 034, 036, 037, 038, 039; REQ-N-001..018 | Real login/roles/MFA, real geospatial nearby-search, tiered alert send + live status, real FCM push + delivery tracking, cert upload/expiry, background location + consent, country partitioning and configurability, security/privacy/reliability targets, audit trail. This is most of the brief's stated MVP — deliberately not Phase 1, see Section 3. **[CHG-009, 2026-07-13]** At backlog time this theme was itself split into a simple **Phase 2** (core notification loop only — REQ-F-006..010 (full)/012 (full)/019/021/031/033/034, REQ-N-001..003/010/017) and a **Phase 3** (auth/MFA — REQ-F-001, REQ-N-005/007/008; certification/consent — REQ-F-016..018/020/023, REQ-N-009/011/018; country portability/admin — REQ-F-022/032 (per-country part)/036..039, REQ-N-004/006/012..016). See Section 4 and 03-product-backlog-v1.md's Phase 3 section for the exact story-level split. |
| Later / TBD | — | AED-fetch flow, AED registry | (none yet — no REQ-F assigned) | Explicitly deferred in the brief; needs OQ-002 resolved first. |
| Later / TBD | volunteer-app | iOS app | CON-001 | Brief: "Android only for now." |
| Later / TBD | — | Reporting & analytics | (none yet — no REQ-F assigned) | Explicitly deferred in the brief. |
| Buiten scope (this round) | e2e-tests | End-to-end test repo setup | CON-008 | Deferred per Mohamed, 2026-07-06 — not part of this backlog. |

## 3. In scope — Fase 1 (eerste release)

Phase 1 is not "the MVP" as the brief describes it — the brief's stated MVP (Section "What's in scope (MVP)") includes login/roles, a real registry, real alerting, and account/certification handling, which this document places in Phase 2 (Section 4). Phase 1 here is the walking skeleton Mohamed asked for: three small, independent, mockable slices — one per repo — sized so a 2-developer team can ship something demoable quickly, before the harder integration and NFR-heavy work.

**dispatcher-web — Incident record management**
- **REQ-F-002, REQ-F-003, REQ-F-004** — create an incident and set its location by map click, address (geocoding mocked), or coordinates. In Phase 1 this is folded into a single incident-creation form (type, notes, optional country, location) rather than a live, in-progress dispatch flow — a simplification agreed with Mohamed (chat, 2026-07-06), not stated this way in the brief. The brief's "type" concept for an incident doesn't exist yet (every brief incident is implicitly a cardiac arrest); "type" is scoped here as a free field for future-proofing, not a resolved taxonomy.
- **REQ-F-005** — correcting the pin is covered by the general "edit incident" capability (all fields, including location, are editable), not a dedicated "fix the pin" flow.
- **REQ-F-013** — browse the (mocked) list of registered volunteers, ignoring position/availability per Mohamed's example.
- **REQ-F-010 (simplified), REQ-F-011** — Phase 1 uses a simple incident status lifecycle (open → in progress → resolved, plus cancelled) rather than the brief's full per-volunteer live status (notified/accepted/declined/en route/arrived/stood down). The full live-status view is Phase 2 (Section 4).
- **REQ-F-012 (simplified)** — basic created/updated tracking on the incident record; the brief's "full audit trail of everything" is Phase 2.
- Explicitly **not** in Phase 1: login/roles (REQ-F-001, deferred by the walking-skeleton decision), seeing volunteers filtered by radius (REQ-F-006), sending any alert (REQ-F-007, 008, 009).

**volunteer-app — Alert response walking skeleton**
- **REQ-F-014** — sign up (mocked persistence, no backend validation yet).
- **REQ-F-015** — select a tier at sign-up. **[CHG-003] Confirmed**: final tier list is certified/verified CPR-BLS, healthcare professional (its own separate tier), willing-but-untrained — matches the brief's three provisional names, no rework needed.
- **REQ-F-024, REQ-F-025** — accept/decline a (mocked, not push-delivered) incoming alert with one tap.
- **REQ-F-026** — navigate to the scene via a maps deep link with mocked coordinates. **[CHG-004] Resolved**: provider choice is a development-team decision, not a requirement; Phase 1 continues to use Google Maps as already built, no rework required.
- **REQ-F-027** — static in-app CPR/AED reference content, no backend needed.
- **REQ-F-028, REQ-F-029, REQ-F-030** — mocked post-event check-in (arrived / stood down / optional wellbeing).
- Explicitly **not** in Phase 1: real push delivery (REQ-F-021, REQ-F-022), certification upload/expiry/reminders (REQ-F-016, 017, 018), availability modes (REQ-F-019), real background location + consent (REQ-F-020, REQ-F-023).

**backend-api — API & module scaffold**
- **CON-003** — scaffold the six module boundaries (Auth/MFA/Roles, Volunteers + Accounts, Incidents + Audit, Geospatial, Notifications, Countries/Config) as an enabler, even if most modules start empty.
- **REQ-F-035 (partial)** — a minimal, read-oriented volunteer endpoint (name, tier, status — no history yet) so dispatcher-web's volunteer list (REQ-F-013) has something real to eventually call.
- A basic incident CRUD endpoint (create/list/get/update), ungrounded in a single REQ-F on its own but existing to support REQ-F-002..005/010/011/012 once dispatcher-web is ready to stop using its own mock.
- No auth (REQ-F-001, REQ-N-005 deferred), no geospatial search (REQ-F-031), no tiered alert logic (REQ-F-032), no real push (REQ-F-033, REQ-F-034), no enforced country partitioning (REQ-F-036) yet — the module exists as a boundary, not a working feature, until Phase 2.

## 4. Latere fases

**[CHG-009, 2026-07-13]** The backlog pass through this theme split it further, at Mohamed's direction, into a simple **Phase 2** (the core notification loop — find volunteer, alert, tiered order, widen, live status, audit trail, availability, real push, delivery tracking) and a **Phase 3** (auth/MFA, certification workflow, background-location consent, country portability, admin tools — deferred, not needed to make the core loop real). See 03-product-backlog-v1.md's "Phase 3 (deferred, CHG-009)" section for the exact story-level split. The theme description below is kept as originally scoped (all of it is still real, planned work); the phase split is a build-order/prioritization decision layered on top, not a scope cut.

- **Fase 2 — Core dispatch loop + integration (all three repos):** REQ-F-001 (login/roles), REQ-F-006 (radius-filtered volunteer view), REQ-F-007/008/009 (send alert, tiered logic, widening), REQ-F-010 (full live per-volunteer status), REQ-F-012 (full audit trail), REQ-F-016..020, 023 (certification workflow, availability, background location + consent), REQ-F-021/022 (real push + DND handling), REQ-F-031..034 (geospatial search, tiered logic, FCM send + delivery tracking), REQ-F-036..039 (country partitioning, admin tools), and effectively all of Section 3 (non-functional requirements: REQ-N-001..018 — speed, reliability, MFA, encryption, least privilege, audit logging, privacy, portability). Deferred because the walking-skeleton decision explicitly excludes auth and real integration from Phase 1, and because most of these items depend on Phase 1's mocked slices being replaced by real ones first.
- **Later / TBD — AED-fetch flow and AED registry:** explicitly deferred in the brief; blocked on OQ-002 (AED data sourcing) even once picked up.
- **Later / TBD — Reporting and analytics:** explicitly deferred in the brief; no requirements captured yet (would need its own requirements-structuring pass).
- **Later / TBD — iOS volunteer app:** brief says "Android only for now" (CON-001); no timeline given.

## 5. Buiten scope

- **AED-fetch flow, AED registry, reporting/analytics** — brief, explicitly out of scope for the MVP; architecture should leave room (brief's own words).
- **iOS app** — brief, "Android only for now."
- **e2e-tests repo** — Mohamed, chat 2026-07-06: excluded from this backlog round. Architecture should still leave room (it's already drawn into the diagram as a fourth repo).

## 6. Dependencies & build-volgorde

| Item | Hangt af van | Reden | Effect op volgorde |
|------|--------------|-------|--------------------|
| dispatcher-web Phase 1 | — | Uses its own mocked data; no dependency on backend-api or volunteer-app in Phase 1. | Can start immediately, in parallel with the other two repos. |
| volunteer-app Phase 1 | — | Same — mocked alert data, no real push, no real backend call. | Can start immediately, in parallel. |
| backend-api Phase 1 | — | Independent scaffold + CRUD endpoints; not required by the other two repos' Phase 1 work. | Can start immediately, in parallel; useful to start the module scaffold (enabler) first since the CRUD endpoints build inside it. |
| dispatcher-web Phase 2 (real data) | backend-api Phase 2 (real incident/volunteer endpoints, auth) | Dispatcher-web can only replace its mock with real calls once the backend exposes the real, authenticated endpoints. | Phase 2 backend work should lead Phase 2 frontend integration work by at least enough to have endpoints available. |
| volunteer-app Phase 2 (real alerts) | backend-api Phase 2 (geospatial search, tiered alert logic, FCM sending) | Volunteer app can't receive a real alert until the backend can compute "nearby" and actually send one. | Same as above. |
| Full dispatch loop (Phase 2) | REQ-F-006 → REQ-F-007/008/009 → REQ-F-010 | Must know who's nearby before alerting; must alert before tracking status. | Sequencing within Phase 2. |
| REQ-F-018 (cert reminders) | REQ-F-016, REQ-F-017 (upload, expiry tracking) | Can't remind about an expiry that isn't tracked. | Sequencing within Phase 2. |

Within each Phase 1 repo, the internal build order follows the "Suggested build order" in [[03-product-backlog-v1]] (create before view/update/resolve, sign-up before alert-handling, module scaffold before endpoints).

## 7. Effort, risico & prioriteit (analyse-inschatting — ter review)

Grouped by Phase 1 capability and by Phase 2 theme rather than one row per individual requirement, given the number of requirements (57) — each row still lists its requirement IDs for traceability.

| Requirement(s) | Prioriteit | Effort (S/M/L) | Risico | Reden risico |
|-------------|------------|----------------|--------|--------------|
| REQ-F-002..005 (create/edit incident + location) | Must | S | Laag | Standard CRUD form, no new tech, mocked geocoding. |
| REQ-F-010 (simplified), REQ-F-011 (status lifecycle, cancel/resolve) | Must | S | Laag | Simple state field on an existing record. |
| REQ-F-012 (simplified audit) | Must | S | Laag | Timestamps only in Phase 1. |
| REQ-F-013 (volunteer list, mocked) | Should | S | Laag | Static/mocked list rendering. |
| REQ-F-014, 015 (sign-up + tier) | Must | S | Laag | OQ-001 resolved [CHG-003] — tier list confirmed as already built, no rework needed. |
| REQ-F-024, 025 (accept/decline) | Must | S | Laag | Simple state toggle on mocked data. |
| REQ-F-026 (navigate) | Must | S | Laag | OQ-006 resolved [CHG-004] — provider is a dev decision, Phase 1's Google Maps implementation stands, no rework needed. |
| REQ-F-027 (CPR reference) | Should | S | Laag | Static content. |
| REQ-F-028..030 (check-in) | Should | S | Laag | Simple form, mocked persistence. |
| CON-003 (module scaffold, backend) | — (enabler) | S | Laag | Project setup, well understood. |
| Backend incident CRUD + volunteer read endpoint | Must | M | Laag | Standard REST CRUD, no auth/geospatial complexity yet. |
| REQ-F-001, REQ-N-005 (login/roles/MFA) | Must | M | Laag | OQ-011 resolved [CHG-005] — two roles (dispatcher, admin), permission boundaries now defined; standard well-understood pattern. **[CHG-009] Deferred to Phase 3** — build order reprioritised, not a scope cut (US-201..203). |
| REQ-F-006, 031, REQ-N-017 (radius search, nearby-volunteer search, sub-second target) | Must | L | Medium | Geospatial DB/indexing choice delegated to dev team (OQ-003 resolved [CHG-006]); OQ-007 resolved [CHG-011] — kept simple, flat "under 1 second," no benchmark methodology. |
| REQ-F-007, 008, 009, 032 (tiered alert send + widening, configurable per country) | Must | L | Medium | Tier breakdown confirmed (OQ-001 resolved [CHG-003]) and country-abstraction approach delegated to dev team (OQ-005 resolved [CHG-008]); still genuinely new logic to build. |
| REQ-F-010 (full), REQ-F-012 (full) (live status, full audit trail) | Must | M | Medium | Needs the WebSocket path (CON-005) actually built and a real event log; real-time UI adds complexity. |
| REQ-F-021, 022, 033, 034 (real push send + DND handling + delivery tracking) | Must | L | Medium | Push reliability approach delegated to dev team (OQ-004 resolved [CHG-007]) — focus is normal-condition delivery; DND-bypass remains best-effort with no mandated mechanism. |
| REQ-F-016..020, 023 (cert upload/expiry/reminders, availability, background location + consent) | Must/Should | M | Medium | Several sub-flows, but each individually well understood; consent/location touches privacy requirements (REQ-N-009..011). **[CHG-009]** REQ-F-019 (availability, US-213) stayed in Phase 2 as the simple core-loop slice; REQ-F-016..018/020/023 (cert upload/expiry/reminders, background location + consent, US-210/211/212/214) deferred to Phase 3. |
| REQ-F-036, REQ-N-004, REQ-N-012..016 (country partitioning + full portability config) | Must | L | Medium | Country-abstraction technical approach delegated to dev team (OQ-005 resolved [CHG-008]); still touches almost every module. **[CHG-009] Deferred to Phase 3** (US-219..221). |
| REQ-N-001, 002, 003 (speed, uptime, graceful degradation) | Must | L | High | Depends on the geospatial and push work above; measurement approach undefined (OQ-015 — still open, non-blocking). |
| REQ-N-006, 007, 008 (encryption, least privilege, security audit logging) | Must | M | Medium | OQ-010 resolved [CHG-016] — minimum TLS in transit + at-rest for sensitive fields via datastore defaults, no key-management scheme mandated; otherwise standard practice. |
| REQ-N-009, 010, 011 (privacy: minimisation, retention, location opt-in) | Must | M | Medium | OQ-009 resolved [CHG-012] — 90-day retention placeholder, pending real legal review per jurisdiction; otherwise policy + implementation, not new tech. |
| REQ-F-037, 038, 039 (admin tools) | Must/Should | M | Laag | Standard admin CRUD once the underlying data models exist. **[CHG-009] Deferred to Phase 3** (US-222..224). |

## 8. Constraints & vroege architectuurbeslissingen

- **CON-001** — React Native, Android only for now. Effect: no iOS work planned; if iOS is picked up later, check for React Native APIs used that aren't Android-only-safe.
- **CON-002** — Next.js for dispatcher-web. Effect: no change to scope, but fixes the dispatcher-web tech stack for both Phase 1 and Phase 2 stories.
- **CON-003** — Backend is a single-repo modular monolith with six named modules. Effect: Phase 1's backend enabler should scaffold exactly these six module boundaries, not fewer or more, so Phase 2 work has a stable place to land.
- **CON-004, CON-005** — REST/HTTPS (volunteer-app) and REST + WebSocket (dispatcher-web) as the integration protocols. Effect: the WebSocket channel is why REQ-F-010's full live-status view is feasible as "live" rather than polled — worth deciding early in Phase 2, since it shapes the backend's Notifications module.
- **CON-006** — FCM for push. Effect: fixes the push provider; OQ-004 (push reliability approach, i.e. how FCM is used, not which provider) is resolved [CHG-007] — delegated to the dev team.
- **CON-007** — geo-indexed, per-country-partitioned datastore. Effect: **[CHG-006] resolved** — specific database/indexing technology is delegated to the development team's discretion, not a BA-level decision. The dev team should still be mindful that the Phase 1 CRUD endpoint's datastore choice won't need replacing for the geospatial work in Phase 2, but that tradeoff is theirs to make.
- **CON-008** — four repos for a 2-dev + QA + BA team. Effect: confirms the Repo-tagged single-backlog approach used in [[03-product-backlog-v1]]; e2e-tests repo excluded from this round (Section 5).
- **[CHG-008] resolved:** the country-abstraction technical approach (OQ-005) is delegated to the development team's discretion, not a BA-level decision. The dev team should still be mindful that CON-003's module scaffold (Countries/Config) is being built in Phase 1 — deciding the abstraction shape early avoids reworking that module's boundary later, but that's their call to make, not a BA-specified requirement.

## 9. Open scopingvragen

- ~~**OQ-001 (tier breakdown)**~~ — **RESOLVED [CHG-003]:** healthcare professional is its own separate tier (certified/verified CPR-BLS, healthcare professional, willing-but-untrained). REQ-F-015 (Phase 1) needed no rework — the built list already matches. Phase 2 tiered-alert logic (REQ-F-008/032) can now be scoped.
- ~~**OQ-006 (navigation provider conflict)**~~ — **RESOLVED [CHG-004]:** provider choice is a development-team decision, not a requirement. Phase 1's Google Maps implementation stands as built; REQ-F-026 only requires that navigation is provided.
- ~~**OQ-003 (geospatial database/indexing)**~~ — **RESOLVED [CHG-006]:** delegated to the development team's discretion; no BA-specified database technology. REQ-F-031/REQ-N-017 can now be scoped for Phase 2 without waiting on this decision.
- ~~**OQ-005 (country-abstraction approach)**~~ — **RESOLVED [CHG-008]:** technical modelling approach delegated to the development team. REQ-N-012..016 and REQ-F-032 can now be scoped for Phase 2; the Countries/Config module's internal shape is a dev decision.
- ~~**OQ-004 (push reliability approach)**~~ — **RESOLVED [CHG-007]:** delegated to the development team; requirements focus on normal-condition delivery. REQ-F-021/022/033 can now be scoped for Phase 2 as a best-effort requirement, not a blocked one.
- ~~**OQ-011 (role permission boundaries)**~~ — **RESOLVED [CHG-005]:** two roles — dispatcher and admin (admin has cross-incident oversight). REQ-F-001 (Phase 2 login/roles) can now be scoped.
- ~~All other open questions carried from [[01-requirements-structured-v1]] (OQ-002, OQ-007, OQ-008, OQ-009, OQ-010, OQ-012, OQ-013, OQ-014, OQ-015) affect Phase 2 or later items only and do not block Phase 1 as scoped above; none of these six resolutions touch them.~~ — **[CHG-010 through CHG-017, 2026-07-13]** OQ-007, 008, 009, 010, 012, 013, and 014 are now resolved (see [[01-requirements-structured-v1]] §5 and [[06-change-log]]); none of them blocked Phase 1 either way. Only OQ-002 (AED sourcing, a fully future/out-of-scope theme) and OQ-015 (delivery-target measurement methodology, non-blocking) remain open.
