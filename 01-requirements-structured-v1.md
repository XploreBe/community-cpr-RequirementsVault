# Structured Requirements — Community CPR Volunteer Dispatch

**Source(s):** "Community CPR Volunteer Dispatch — Project Brief" (PDF, dated 2026-05-29); "Community CPR — 4-Repo Architecture" diagram (provided by Mohamed, 2026-07-06); Mohamed's kickoff conversation, 2026-07-06 (dispatcher-web example stories, phasing intent)
**Date structured:** 2026-07-06
**Produced by:** requirements-structuring skill
**Status:** Draft — needs human review

## 1. Summary

Community CPR Volunteer Dispatch is a system that lets a 911/112 dispatcher pin a cardiac-arrest patient on a map, find nearby trained volunteers, and alert them with one action. Volunteers get a push notification, accept or decline, navigate to the scene, and perform CPR until EMS arrives. The system is meant to be portable across countries rather than built for one jurisdiction. The brief describes three product components — a volunteer mobile app (Android only for now), a dispatcher web console, and a backend — plus account/certification handling. An AED-fetch flow, an AED registry, and reporting/analytics are explicitly deferred. The architecture diagram adds a fourth repo (e2e-tests) and fixes several technology choices (React Native, Next.js, FCM, a single-repo modular-monolith backend).

## 2. Functional requirements

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| REQ-F-001 | The dispatcher console shall support login with role-based access for two roles: dispatcher (can create/manage/dispatch incidents) and admin (oversight of all dispatchers and incidents across the system). | Must | Brief — "What the dispatcher console needs to do" | Roles and permissions confirmed — see OQ-011 [RESOLVED CHG-005]. Original brief text named three roles (dispatcher, supervisor, admin); supervisor was folded out per stakeholder decision — admin covers the cross-incident oversight need. |
| REQ-F-002 | The dispatcher shall be able to place the patient's location on a map by clicking a point. | Must | Brief — "What we want to build" (1), "What the dispatcher console needs to do" | |
| REQ-F-003 | The dispatcher shall be able to place the patient's location by entering an address (geocoded). | Must | Brief — "What the dispatcher console needs to do" | |
| REQ-F-004 | The dispatcher shall be able to place the patient's location by entering coordinates directly. | Must | Brief — "What the dispatcher console needs to do" | |
| REQ-F-005 | The dispatcher shall be able to correct/move the patient's pin if it is wrong. | Must | Brief — "What the dispatcher console needs to do" ("Fix it if wrong") | |
| REQ-F-006 | The dispatcher shall be able to see which trained volunteers are available within configurable radius bands around the patient. | Must | Brief — "What we want to build" (2), "What the dispatcher console needs to do" | "Configurable" ties to REQ-N-016 (portability). |
| REQ-F-007 | The dispatcher shall be able to send an alert to the identified nearby volunteers with a single action. | Must | Brief — "What we want to build" (3), "What the dispatcher console needs to do" | |
| REQ-F-008 | The alert logic shall notify certified responders first (tiered order). | Must | Brief — "What the dispatcher console needs to do", "Goals" | Tier breakdown confirmed — see OQ-001 [RESOLVED CHG-003]: certified/verified CPR-BLS, healthcare professional (separate tier), willing-but-untrained. |
| REQ-F-009 | The alert logic shall widen the notified pool to a broader tier if nobody accepts within a configurable time window (N seconds). | Must | Brief — "What the dispatcher console needs to do" | Value of N and widening rule not specified — see OQ-015 (measurement/definition). |
| REQ-F-010 | The dispatcher shall see live status per notified volunteer: notified, accepted, declined, en route, arrived, stood down. | Must | Brief — "What the dispatcher console needs to do" | |
| REQ-F-011 | The dispatcher shall be able to cancel/stand down an incident (e.g. EMS on scene, or situation resolved), which notifies all notified/accepted volunteers to stand down. | Must | Brief — "What the dispatcher console needs to do" | |
| REQ-F-012 | The system shall keep a full, viewable audit trail of everything that happened during a dispatch (who was notified, when, who responded, outcome). | Must | Brief — "What the dispatcher console needs to do", "What the backend needs to do" | |
| REQ-F-013 | The dispatcher shall be able to view the list of registered volunteers. | Should | Mohamed, chat 2026-07-06 (dispatcher-web example US-06) | Not explicitly stated as a standalone dispatcher capability in the brief, but implied by the volunteer registry existing; brief itself never lists "browse volunteers" as a console feature independent of an active incident. Treated here as directly grounded because it's a read view over data (registered volunteers) the brief already requires the backend to hold. |
| REQ-F-014 | A volunteer shall be able to sign up / create an account. | Must | Brief — "What the volunteer app needs to do", "What's in scope (MVP)" (4. Account stuff) | |
| REQ-F-015 | A volunteer shall be able to select/declare a training tier during sign-up. | Must | Brief — "What the volunteer app needs to do", "Volunteer tiers" | Tier breakdown confirmed — see OQ-001 [RESOLVED CHG-003]: certified/verified CPR-BLS, healthcare professional (separate tier), willing-but-untrained. |
| REQ-F-016 | A volunteer shall be able to upload certification documentation. | Must | Brief — "What the volunteer app needs to do" | |
| REQ-F-017 | The system shall track the expiry date of a volunteer's uploaded certification. | Must | Brief — "What the volunteer app needs to do" | |
| REQ-F-018 | The system shall remind a volunteer to re-verify their certification (e.g. ahead of expiry). | Should | Brief — "What the volunteer app needs to do" | Timing/channel of reminder not specified. |
| REQ-F-019 | A volunteer shall be able to set their availability: always on, scheduled, or do-not-disturb. | Must | Brief — "What the volunteer app needs to do" | |
| REQ-F-020 | The system shall collect a volunteer's background location only with the volunteer's explicit consent. | Must | Brief — "What the volunteer app needs to do" | Consent must be recorded — see REQ-F-023. |
| REQ-F-021 | The volunteer app shall receive a push alert when the volunteer is identified as a nearby responder for an incident. | Must | Brief — "What we want to build", "What the volunteer app needs to do" | |
| REQ-F-022 | Push alerts shall attempt to get through the device's silent/do-not-disturb mode, to the extent the platform and the user's settings allow. | Should | Brief — "What the volunteer app needs to do" | Feasibility/approach delegated to the development team — see OQ-004 [RESOLVED CHG-007]. Requirement remains best-effort (Should priority, no mandated mechanism); normal-condition delivery (REQ-F-021, REQ-N-001) is the Must-priority baseline and is unaffected. |
| REQ-F-023 | The system shall record an explicit consent record for a volunteer's data collection (at minimum, background location consent). | Must | Brief — "What's in scope (MVP)" (4. Account stuff — "consent records"), "What the volunteer app needs to do" | |
| REQ-F-024 | A volunteer shall be able to accept an alert with one tap. | Must | Brief — "What we want to build", "Goals", "What the volunteer app needs to do" | |
| REQ-F-025 | A volunteer shall be able to decline an alert with one tap. | Must | Brief — "What the volunteer app needs to do" ("One-tap accept or decline") | |
| REQ-F-026 | After accepting, a volunteer shall receive turn-by-turn navigation directions to the scene. | Must | Brief — "What we want to build", "What the volunteer app needs to do" | Provider choice delegated to the development team — see OQ-006 [RESOLVED CHG-004]. The brief (Google Maps) and the architecture diagram (OpenStreetMap/MapLibre/OSRM) conflicted on provider; requirement is that navigation is provided, specific provider/SDK is a dev decision as long as it works. |
| REQ-F-027 | The volunteer app shall provide an in-app CPR/AED reference a volunteer can consult during a live event. | Must | Brief — "What the volunteer app needs to do" | |
| REQ-F-028 | After an incident, a volunteer shall complete a quick check-in: whether they arrived. | Should | Brief — "What the volunteer app needs to do" | |
| REQ-F-029 | After an incident, a volunteer shall be able to record whether they were stood down. | Should | Brief — "What the volunteer app needs to do" | |
| REQ-F-030 | After an incident, a volunteer may optionally complete a wellbeing follow-up. | Could | Brief — "What the volunteer app needs to do" ("optional wellbeing follow-up") | |
| REQ-F-031 | The backend shall find volunteers near a given location (nearby-volunteer search). | Must | Brief — "What we want to build", "What the backend needs to do" | Performance target: REQ-N-017. |
| REQ-F-032 | The backend shall run the tiered alert logic, with the tiering/ordering/distance rules configurable per country. | Must | Brief — "What the backend needs to do", "Volunteer tiers" | |
| REQ-F-033 | The backend shall send push notifications via FCM (Firebase Cloud Messaging). | Must | Brief — "What the backend needs to do"; Diagram (FCM push service) | |
| REQ-F-034 | The backend shall track push delivery status (delivered / not reached) per volunteer per alert. | Must | Brief — "What the backend needs to do" ("track delivery") | |
| REQ-F-035 | The backend shall hold and maintain the volunteer registry: tier, certification, status, and history. | Must | Brief — "What the backend needs to do" | |
| REQ-F-036 | The backend shall keep volunteer/incident data partitioned per country/jurisdiction. | Must | Brief — "What the backend needs to do", "Non-functional stuff" (Scale) | Related NFR: REQ-N-004. Related technical note: CON-008. |
| REQ-F-037 | The backend shall provide admin tools for managing volunteers. | Must | Brief — "What the backend needs to do" | |
| REQ-F-038 | The backend shall provide admin tools for verifying volunteer certifications. | Must | Brief — "What the backend needs to do", "What's in scope (MVP)" (4. Account stuff) | |
| REQ-F-039 | The backend shall provide admin tools for managing in-app content (e.g. the CPR/AED reference material). | Should | Brief — "What the backend needs to do" | |

## 3. Non-functional requirements

| ID | Requirement | Category | Priority | Source | Notes |
|----|-------------|----------|----------|--------|-------|
| REQ-N-001 | From the dispatcher pressing "send," the alert shall reach the volunteer's phone in under 5 seconds, 95% of the time. | Performance | Must | Brief — "Non-functional stuff" (Speed) | Measurement method (what counts as "reached," how monitored) not defined — see OQ-015. |
| REQ-N-002 | The dispatch path shall target 99.9% uptime. | Reliability | Must | Brief — "Non-functional stuff" (Reliability) | |
| REQ-N-003 | If a non-core dependency fails (e.g. maps, cert service), the rest of the system shall keep working (graceful degradation). | Reliability | Must | Brief — "Non-functional stuff" (Reliability) | |
| REQ-N-004 | The system shall support deployment to multiple countries without re-platforming. | Scalability | Must | Brief — "Non-functional stuff" (Scale) | |
| REQ-N-005 | Dispatcher accounts shall require multi-factor authentication (MFA). | Security | Must | Brief — "Non-functional stuff" (Security) | |
| REQ-N-006 | The system shall encrypt data "everywhere" (source's own wording). | Security | Must | Brief — "Non-functional stuff" (Security) | Vague — precise scope (in transit / at rest / which fields / key management) not defined — see OQ-010. |
| REQ-N-007 | The system shall apply least-privilege access control. | Security | Must | Brief — "Non-functional stuff" (Security) | |
| REQ-N-008 | The system shall log every security-relevant action for audit purposes. | Security | Must | Brief — "Non-functional stuff" (Security — "audit everything") | Distinct from REQ-F-012 (dispatcher-facing dispatch audit trail); this covers system/admin-level action logging. |
| REQ-N-009 | The system shall collect the minimum personal data necessary (data minimisation). | Privacy | Must | Brief — "Non-functional stuff" (Privacy) | |
| REQ-N-010 | Patient location data shall not be retained longer than necessary. | Privacy | Must | Brief — "Non-functional stuff" (Privacy) | Precise retention period not defined — see OQ-009. |
| REQ-N-011 | Volunteer location shall be collected only while an event is active, or with the volunteer's explicit opt-in otherwise. | Privacy | Must | Brief — "Non-functional stuff" (Privacy) | |
| REQ-N-012 | Language shall be configurable per country, not hard-coded. | Portability | Must | Brief — "Non-functional stuff" (Portability) | |
| REQ-N-013 | Address format shall be configurable per country, not hard-coded. | Portability | Must | Brief — "Non-functional stuff" (Portability) | |
| REQ-N-014 | The emergency contact number shall be configurable per country, not hard-coded. | Portability | Must | Brief — "Non-functional stuff" (Portability) | |
| REQ-N-015 | Units of measurement shall be configurable per country, not hard-coded. | Portability | Must | Brief — "Non-functional stuff" (Portability) | |
| REQ-N-016 | Country-specific business rules (who is alerted, in what order, at what distance) shall be configurable, not hard-coded. | Portability | Must | Brief — "Non-functional stuff" (Portability), "Volunteer tiers" | Technical approach for this abstraction delegated to the development team — see OQ-005 [RESOLVED CHG-008]. What must be configurable is unchanged; how it's implemented is a dev decision. |
| REQ-N-017 | Nearby-volunteer search shall return results in sub-second time, including in dense cities. | Performance | Must | Brief — "What the backend needs to do" | "Sub-second" and load conditions not precisely defined — see OQ-007. Related functional requirement: REQ-F-031. |
| REQ-N-018 | Background location tracking on the volunteer app shall be battery-friendly. | Performance/Usability | Should | Brief — "What the volunteer app needs to do" | Vague term, no measurable definition given — see OQ-008. |

## 4. Constraints

| ID | Constraint | Source | Notes |
|----|------------|--------|-------|
| CON-001 | The volunteer app is built in React Native and targets Android only for now. | Brief — "What's in scope (MVP)" (1); Diagram ("volunteer-app / React Native") | iOS is deferred, not built now — see Section 9 (Out of scope). |
| CON-002 | The dispatcher web console is built in Next.js. | Diagram ("dispatcher-web" — annotated "Next.js — Victor's call") | Recorded as a named team decision per the diagram's own annotation. |
| CON-003 | The backend is a single repository, modular monolith (not microservices), with module boundaries: Auth/MFA/Roles, Volunteers + Accounts, Incidents + Audit, Geospatial, Notifications, Countries/Config. | Diagram ("backend-api — single repo · modular monolith") | |
| CON-004 | The volunteer app talks to the backend over REST/HTTPS. | Diagram | |
| CON-005 | The dispatcher web console talks to the backend over REST and WebSocket. | Diagram | WebSocket implies the live-status view (REQ-F-010) is meant to be pushed/streamed rather than polled — not stated explicitly in the brief text, flagged here as inferred from the diagram, not confirmed. |
| CON-006 | Push notifications are delivered via FCM (Firebase Cloud Messaging). | Brief — "What the backend needs to do"; Diagram | |
| CON-007 | The backend's datastore includes geo-indexing and is partitioned per country. | Diagram ("Database — geo-index · per-country") | Implements REQ-F-036 / REQ-N-004; specific database technology delegated to the development team — see OQ-003 [RESOLVED CHG-006]. |
| CON-008 | The system is split across four repositories (volunteer-app, dispatcher-web, backend-api, e2e-tests) for a team of 2 developers, 1 QA, and 1 BA. | Diagram (title, subtitle) | The e2e-tests repo is out of scope for this backlog round per Mohamed, chat 2026-07-06 — see Section 9. |

## 5. Open questions (need stakeholder input)

- ~~**OQ-001:** What is the final breakdown of volunteer tiers?~~ — **RESOLVED [CHG-003]:** Healthcare professional is its own separate tier. Final breakdown: (1) certified/verified CPR-BLS, (2) healthcare professional, (3) willing-but-untrained. — affects REQ-F-008, REQ-F-015, REQ-F-032.
- **OQ-002:** Where do AED locations come from — official government registries, crowdsourcing, or a hybrid? Explicitly called out in the brief as undecided. — affects future AED-fetch flow and AED registry (both out of scope for now, see Section 9), but the data model should leave room per the brief.
- ~~**OQ-003:** What geospatial database and indexing approach will be used to keep nearby-volunteer search fast at country scale?~~ — **RESOLVED [CHG-006]:** Out of scope for requirements — technical implementation choice, delegated to the development team's discretion. No specific database/indexing technology is mandated; REQ-F-031 and REQ-N-017 stand as written (the functional/performance outcome, not the implementation). — affects REQ-F-031, REQ-N-017, CON-007.
- ~~**OQ-004:** What is the technical approach to maximise push delivery reliability (waking a backgrounded or silent Android device)?~~ — **RESOLVED [CHG-007]:** Delegated to the development team. Requirements focus on normal-condition device operation; REQ-F-022's do-not-disturb-bypass behaviour remains a best-effort "Should" with no specific mechanism mandated. — affects REQ-F-021, REQ-F-022, REQ-N-001.
- ~~**OQ-005:** How will country-specific differences (emergency number, regulations, language, integration partners, alert rules) be modelled technically without forking the codebase?~~ — **RESOLVED [CHG-008]:** Technical modelling approach delegated to the development team. REQ-N-012 through REQ-N-016 and REQ-F-032 continue to state what must be configurable; how that's implemented is a dev decision. — affects REQ-N-012 through REQ-N-016, REQ-F-032.
- ~~**OQ-006:** Which map/navigation provider does the volunteer app actually use?~~ — **RESOLVED [CHG-004]:** Navigation provider is a development-team implementation choice, not specified by requirements. REQ-F-026 requires that turn-by-turn navigation is provided to the volunteer; which provider/SDK is used (Google Maps, OpenStreetMap/MapLibre/OSRM, or otherwise) is left to the dev team, as long as navigation works. — affects REQ-F-026.
- **OQ-007:** What precisely does "sub-second" mean for nearby-volunteer search — under what concurrency, region size, and volunteer-count assumptions should this be benchmarked? — affects REQ-N-017.
- **OQ-008:** What precisely does "battery-friendly" mean for background location tracking (e.g. a target sampling interval or battery-drain budget)? — affects REQ-N-018.
- **OQ-009:** What is the precise retention period for patient location data once an incident is closed? — affects REQ-N-010.
- **OQ-010:** What precisely does "encryption everywhere" cover — data in transit only, data at rest, specific fields, and what key-management approach? — affects REQ-N-006.
- ~~**OQ-011:** What specifically distinguishes the permissions of the dispatcher, supervisor, and admin roles, and does a supervisor/admin need any cross-incident overview beyond the per-incident dispatcher view?~~ — **RESOLVED [CHG-005]:** Simplified to two roles: dispatcher (can create/manage/dispatch incidents) and admin (oversight of all dispatchers and incidents across the system, i.e. the cross-incident overview). No separate supervisor role. — affects REQ-F-001.
- **OQ-012:** What should happen if a volunteer's device is offline, has no signal, or the app has been force-closed by the OS when an alert is sent? Not addressed in the brief. — affects REQ-F-021, REQ-N-001.
- **OQ-013:** Can a volunteer back out after already accepting an alert (as opposed to declining before accepting), and if so how is that handled downstream (e.g. does the dispatcher get notified, does the pool widen again)? Not addressed in the brief. — affects REQ-F-024, REQ-F-010.
- **OQ-014:** What happens when a volunteer's certification expires without re-verification (e.g. demoted to a lower tier, excluded from alerts entirely), and what happens to an in-flight incident if a notified/accepted volunteer's account is deactivated mid-response? Not addressed in the brief. — affects REQ-F-017, REQ-F-018, REQ-F-035.
- **OQ-015:** How will the 5-second/95% delivery target (REQ-N-001) and the alert-widening delay (REQ-F-009) actually be measured/monitored in production, and what counts as "delivered" versus excluded (e.g. planned maintenance windows)? — affects REQ-N-001, REQ-F-009.

## 6. Assumptions

- **AS-001:** "Trained volunteers" in the brief's core flow description ("see which trained volunteers are nearby") is assumed to mean the same thing as the "certified" tier defined later in "Volunteer tiers," not a separate category. OQ-001 is now resolved [CHG-003: healthcare professional is a separate tier], but that decision did not address this specific wording question — this assumption stands unconfirmed and is carried forward as-is. — affects REQ-F-008, REQ-F-032.
- **AS-002:** The 5-second/95% delivery target (REQ-N-001) is assumed to apply per country/deployment rather than as a single global aggregate across all countries at once. — affects REQ-N-001.

## 7. Glossary

- **Dispatcher** — the 911/112 operator who uses the dispatcher web console to register an incident and alert volunteers. Console roles confirmed as dispatcher and admin — see OQ-011 [RESOLVED CHG-005]; the brief's original "supervisor" role was folded out.
- **Volunteer / responder** — a signed-up individual who can be alerted to a nearby cardiac-arrest incident. Used interchangeably in the brief.
- **Certified volunteer** — a volunteer with a current, verified CPR/BLS certification (brief, "Volunteer tiers").
- **Healthcare professional** — a separate volunteer tier, distinct from certified — confirmed, see OQ-001 [RESOLVED CHG-003].
- **Willing bystander / willing-but-untrained** — a volunteer without verified training who can still be alerted.
- **Tier** — a volunteer's category (certified / healthcare professional / willing-but-untrained), used to decide alert order.
- **Radius band** — a configurable distance ring around the patient used to decide which volunteers are considered "nearby" for a given alert tier.
- **Stand down** — to close/cancel an incident (dispatcher action) or a volunteer's individual instruction to stop responding.
- **AED** — automated external defibrillator; AED-fetch flow and AED registry are both out of scope for the MVP (Section 9).
- **EMS** — emergency medical services (the ambulance crew).
- **MFA** — multi-factor authentication, required for dispatcher accounts (REQ-N-005).
- **Walking skeleton** — term used by Mohamed (chat, 2026-07-06) for the Phase 1 approach: each repo (volunteer-app, dispatcher-web, backend-api) builds a small, working, end-to-end slice against mocked data/dependencies before real integration. This is a phasing decision, not a system requirement — carried into 02-scope-and-context-v1.md rather than into this document.

## 8. Out of scope (explicitly stated)

- **AED-fetch flow** (dispatching a second volunteer to grab a nearby defibrillator) — Brief, "What's out of scope for now." Architecture should leave room for it later.
- **AED registry** (source of AED location data) — Brief, "What's out of scope for now." Sourcing is itself an open question (OQ-002) even when this is picked back up.
- **Reporting and analytics** (response-time dashboards, outcome tracking, EMS partner reports) — Brief, "What's out of scope for now."
- **iOS volunteer app** — Brief, "What's in scope (MVP)": "Android only for now." Not stated as permanently out of scope, but explicitly deferred.
- **e2e-tests repo work** — the architecture diagram names a fourth repository for end-to-end tests, but Mohamed (chat, 2026-07-06) confirmed this backlog round covers only volunteer-app, dispatcher-web, and backend-api. Deferred, not dropped.
