# Product Backlog — Community CPR Volunteer Dispatch (Phase 1 & Phase 2)

**Based on:** 02-scope-and-context-v1.md, 01-requirements-structured-v1.md
**Date:** 2026-07-06
**Produced by:** product-backlog skill
**Status:** Draft — for refinement with the team
**Last updated:** 2026-07-13 (CHG-009 — Phase 2 rescoped to the simple core loop; auth/MFA, certification workflow, location consent, and country-portability/admin stories deferred to Phase 3)

## Legend

- **Repo (Phase 1 items only):** volunteer-app · dispatcher-web · backend-api — which GitHub repository this item belonged to, back when the team worked across separate repos. **Phase 2 items onward do not use this field** — the team now works out of one consolidated repository, so Phase 2+ epics/stories have no repo tag.
- **Priority:** MoSCoW (Must / Should / Could / Won't)
- **Size:** S / M / L — relative, provisional (confirm in refinement)
- **Type:** Story (Phase 1 also used Spike/Enabler; Phase 2 onward uses Story only — see CLAUDE.md)
- **Status:** New · Backlog · Ready (conditional — assumption stated) · Not Ready (reason) — BA-readiness, not delivery progress
- **Delivery status:** Not started · In Progress · Done — manually maintained by the delivery team; not touched by any pipeline skill
- **Grounding:** Direct (traces to a stated requirement) · Derived (rests on the Phase 1 walking-skeleton simplification agreed with Mohamed — see 02-scope-and-context-v1.md §3 — or another stated assumption)

This backlog covers **Phase 1** (the walking skeleton, EPIC-1..3, repo-tagged, includes enablers), **Phase 2** (the simple, real core dispatch loop — no auth, no cert workflow, no country config, per CHG-009), and **Phase 3** (deferred: authentication/MFA, certification workflow, location consent, country portability, admin tools). Phase 2 stories became draftable once OQ-001, OQ-003, OQ-004, OQ-005, OQ-006, and OQ-011 were resolved via CHG-003 through CHG-008 (2026-07-13) — see 06-change-log.md. On review with Mohamed (CHG-009, same day), the first Phase 2 draft turned out bigger than intended: it included things the brief eventually needs (real login/MFA, a full certification lifecycle, country configurability) but that aren't needed to get the actual core loop — a volunteer being found, alerted, and notified — working simply. Those stories are kept (IDs and content intact, nothing deleted, per CLAUDE.md's "IDs are permanent" rule) but reassigned to Phase 3 rather than built now. Every remaining Phase 2 story is still grounded in 01-requirements-structured-v1.md and 02-scope-and-context-v1.md §4; no new scope was invented, and any technical decision Mohamed delegated to the dev team is called out as such rather than specified here.

## Epics

| Epic ID | Repo | Title | Outcome | Requirement IDs | Phase |
|---------|------|-------|---------|-----------------|-------|
| EPIC-1 | dispatcher-web | Incident record management | A dispatcher can create, view, update, and resolve incident records with a location, and browse a list of volunteers — no login, no real backend | REQ-F-002..005, 010 (simplified), 011, 012 (simplified), 013 | Phase 1 |
| EPIC-2 | volunteer-app | Alert response walking skeleton | A volunteer can sign up, see a mocked alert, accept/decline, navigate to the scene, consult CPR guidance, and check in afterward — no login, no real push | REQ-F-014, 015, 024, 025, 026, 027, 028, 029, 030 | Phase 1 |
| EPIC-3 | backend-api | API & module scaffold | The backend has its module boundaries in place plus minimal CRUD endpoints for incidents and a read endpoint for volunteers — no auth, no geospatial/alert/push logic | CON-003, REQ-F-035 (partial) | Phase 1 |
| EPIC-4 | — | Authentication & roles | A dispatcher or admin can log in securely with role-appropriate access; admin gets cross-incident oversight | REQ-F-001, REQ-N-005, REQ-N-006, REQ-N-007, REQ-N-008 | **Phase 3** [CHG-009 — deferred] |
| EPIC-5 | — | Volunteer matching & alerting | The dispatcher can find nearby volunteers, send a tiered alert, see it widen if unanswered, track live status per volunteer, and see a full audit trail | REQ-F-006..010 (full), 012 (full), 031, 032 | Phase 2 |
| EPIC-6 | — | Certification, availability & privacy | A volunteer can upload/maintain certification, get expiry reminders, set availability, and give location consent; admin can see registry history | REQ-F-016..020, 023, 035 (full), REQ-N-009, 010, 011, 018 | Phase 2 (US-213 only) / **Phase 3** (rest) [CHG-009] |
| EPIC-7 | — | Real push delivery | A volunteer receives a real, trackable push alert that best-effort bypasses silent/DND mode | REQ-F-021 (full), 022, 033, 034, REQ-N-001 | Phase 2 (US-216, US-218) / **Phase 3** (US-217) [CHG-009] |
| EPIC-8 | — | Country portability & admin tools | The system can be configured and operated per country, and admins can manage volunteers, certifications, and reference content | REQ-F-036..039, REQ-N-004, 012..016 | **Phase 3** [CHG-009 — deferred] |

---

## EPIC-1 — Incident record management (Repo: dispatcher-web)

### US-001 — Create incident
- **Type:** Story
- **Story:** As a dispatcher, I want to create an incident by filling a form (type, notes, optional country) and setting its location on the map (click, coordinates, or address), so that a case is registered.
- **Acceptance criteria:**
  - Given the incident form is open, when the dispatcher submits it with type, notes, and a location set by clicking the map, then a new incident is created with status "open" and the clicked coordinates stored.
  - Given the incident form is open, when the dispatcher enters coordinates directly instead of clicking, then the incident is created with those coordinates.
  - Given the incident form is open, when the dispatcher enters an address, then the (mocked) geocoding step returns coordinates and the incident is created with them.
  - Given the incident form is open, when the dispatcher submits without setting a location by any method, then the incident is not created and a validation message states location is required.
  - Given the incident form is open, when the dispatcher leaves the country field blank, then the incident is still created (country is optional).
  - Given the incident form is open, when the dispatcher submits with a latitude outside [-90, 90] or a longitude outside [-180, 180], then the incident is not created and a validation message states the coordinates are out of range. [CHG-002]
  - Rule: an incident has exactly one location at creation time.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-002, REQ-F-003, REQ-F-004
- **Grounding:** Derived — the generic "incident" entity with a `type` field is a Phase 1 simplification agreed with Mohamed (02-scope-and-context-v1.md §3), not literally described in the brief, which frames location-pinning as part of a single live cardiac-arrest dispatch rather than a general case record.
- **Depends on / Blocked by:** —
- **Status:** Ready
- **Delivery status:** Not started

### US-002 — View incidents
- **Type:** Story
- **Story:** As a dispatcher, I want to see incidents in a list and on the map for an overview, so that I can see what's active at a glance. (Mocked data.)
- **Acceptance criteria:**
  - Given incidents exist, when the dispatcher opens the incidents view, then all incidents appear both in a list and as markers on the map.
  - Given no incidents exist, when the dispatcher opens the view, then an empty state is shown instead of an empty list/map.
  - Rule: the list and the map show the same incident set at all times — Phase 1 has no filtering.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-002, REQ-F-003, REQ-F-004, REQ-F-005
- **Grounding:** Derived — a multi-incident overview isn't a capability the brief states explicitly (it describes a single live dispatch, not a case list); this is Mohamed's Phase 1 framing (chat, 2026-07-06).
- **Depends on / Blocked by:** US-001 (needs incidents to exist)
- **Status:** Ready
- **Delivery status:** Not started

### US-003 — View incident detail
- **Type:** Story
- **Story:** As a dispatcher, I want to open an incident and see all its data, so that I have the full picture before acting on it.
- **Acceptance criteria:**
  - Given an incident exists, when the dispatcher opens it from the list or map, then all its fields (type, notes, country, location, status, created/updated timestamps) are shown.
  - Given an incident id doesn't exist (e.g. bad link), when the dispatcher navigates to its detail view, then a "not found" state is shown instead of an error page.
  - Rule: the detail view is read-only; edits happen through US-004.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-002..005, REQ-F-012 (simplified)
- **Grounding:** Derived — same Phase 1 framing as US-002.
- **Depends on / Blocked by:** US-001
- **Status:** Ready
- **Delivery status:** Not started

### US-004 — Update incident
- **Type:** Story
- **Story:** As a dispatcher, I want to edit any of an incident's details — status (open → in progress → resolved) and all other fields — so that the record stays accurate.
- **Acceptance criteria:**
  - Given an existing incident, when the dispatcher edits any field (type, notes, country, or location) and saves, then the incident reflects the new values and its updated timestamp changes.
  - Given an existing incident, when the dispatcher changes its status to "open," "in progress," or "resolved," then the new status is saved and reflected in the list/map view.
  - Given an existing incident, when the dispatcher edits it so that it no longer has a location, then the save is rejected — location remains required (same rule as US-001).
  - Given an existing incident, when the dispatcher edits its location to a latitude outside [-90, 90] or a longitude outside [-180, 180] and saves, then the save is rejected and a validation message states the coordinates are out of range — same range rule as US-001. [CHG-002]
  - Rule: status may be set to any of open / in progress / resolved / cancelled directly. Phase 1 does not enforce a strict sequential order between them — this is a stated assumption, not a decision; confirm if strict workflow enforcement (e.g. no skipping "in progress") is actually wanted.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-005, REQ-F-010 (simplified)
- **Grounding:** Derived — the open/in progress/resolved status enum is Mohamed's Phase 1 simplification of REQ-F-010's fuller live-status concept (notified/accepted/declined/en route/arrived/stood down), which is Phase 2.
- **Depends on / Blocked by:** US-001
- **Status:** Ready
- **Delivery status:** Not started

### US-005 — Cancel / resolve incident
- **Type:** Story
- **Story:** As a dispatcher, I want to close an incident (resolved or cancelled) to remove it from the active set.
- **Acceptance criteria:**
  - Given an incident with status "open" or "in progress," when the dispatcher sets it to "resolved," then it is excluded from the default active list (still viewable via search/detail).
  - Given an incident with status "open" or "in progress," when the dispatcher sets it to "cancelled," then it is excluded from the default active list.
  - Given an incident already "resolved" or "cancelled," when the dispatcher repeats the close action, then no further change occurs (idempotent) and the current closed state is shown.
  - Rule: "active set" = incidents with status open or in progress.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-011, REQ-F-010 (simplified)
- **Grounding:** Derived — REQ-F-011's "stand down" concept also notifies volunteers, which is out of scope in Phase 1 (no real alerting yet); this story only closes the record.
- **Depends on / Blocked by:** US-004 (uses the same status field)
- **Status:** Ready
- **Delivery status:** Not started

### US-006 — View volunteers
- **Type:** Story
- **Story:** As a dispatcher, I want to see the list of registered volunteers, so that I know who exists in the system. (Mocked data; position and availability status ignored for now.)
- **Acceptance criteria:**
  - Given registered (mocked) volunteers exist, when the dispatcher opens the volunteers view, then each volunteer's name and tier are listed.
  - Given no volunteers exist in the mock dataset, when the dispatcher opens the view, then an empty state is shown.
  - Rule: this is a read-only view in Phase 1 — no dispatcher action on a volunteer from this screen yet.
- **Priority:** Should · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-1 · **Traces to:** REQ-F-013
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Ready
- **Delivery status:** Not started

---

## EPIC-2 — Alert response walking skeleton (Repo: volunteer-app)

### US-101 — Sign up with tier
- **Type:** Story
- **Story:** As a volunteer, I want to sign up and select my training tier, so that I have an account the system recognises me by.
- **Acceptance criteria:**
  - Given the sign-up form, when a volunteer fills in their name/contact details, selects a tier, and submits, then a (mocked) account is created and stored locally on the device.
  - Given the sign-up form, when a volunteer submits without selecting a tier, then sign-up is rejected with a "tier is required" message.
  - Given the sign-up form, when a volunteer submits with an identifier already used in the mocked dataset (e.g. duplicate email), then sign-up is rejected with a duplicate-account message.
  - Rule: the tier options offered are certified/verified CPR-BLS, healthcare professional (its own separate tier), willing-but-untrained — confirmed final list, see OQ-001 [RESOLVED CHG-003].
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-014, REQ-F-015
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Ready [CHG-003 — OQ-001 resolved, tier list confirmed as already built, no rework needed]
- **Delivery status:** Not started

### US-102 — View an incoming alert
- **Type:** Story
- **Story:** As a volunteer, I want to see an incoming alert with the patient's location on a map, so that I understand where I'm being asked to respond.
- **Acceptance criteria:**
  - Given a (mocked) alert exists for this volunteer, when they open the app, then the alert screen shows the patient's approximate location on a map plus any available notes.
  - Given no alert is active, when the volunteer opens the app, then a neutral "no active alert" state is shown instead.
  - Rule: Phase 1 alerts come from seeded/sample data, not a real push notification — real push delivery is Phase 2 (REQ-F-021 full).
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-021 (partial — in-app display only, not delivery)
- **Grounding:** Derived — Phase 1 simplification; real push mechanics deferred to Phase 2.
- **Depends on / Blocked by:** Loosely depends on US-101 for a volunteer identity to attach the mocked alert to — not a hard blocker since Phase 1 data is mocked.
- **Status:** Ready
- **Delivery status:** Not started

### US-103 — Accept or decline an alert
- **Type:** Story
- **Story:** As a volunteer, I want to accept or decline an alert with one tap, so that I can quickly let the system know whether I'm responding.
- **Acceptance criteria:**
  - Given an active alert, when the volunteer taps "I'm going," then the alert's local status becomes "accepted" and a confirmation is shown.
  - Given an active alert, when the volunteer taps "Decline," then the alert's local status becomes "declined" and it's removed from the active-alert screen.
  - Given an alert already marked accepted, when either button is tapped again, then no duplicate action is recorded.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-024, REQ-F-025
- **Grounding:** Direct
- **Depends on / Blocked by:** US-102
- **Status:** Ready
- **Delivery status:** Not started

### US-104 — Navigate to the scene
- **Type:** Story
- **Story:** As a volunteer who accepted an alert, I want turn-by-turn directions to the patient, so that I can get there as fast as possible.
- **Acceptance criteria:**
  - Given a volunteer has accepted an alert, when they tap "Navigate," then a Google Maps deep link opens with the (mocked) patient coordinates as the destination.
  - Given no maps app is available on the device, when "Navigate" is tapped, then the coordinates/address are shown as fallback text instead of the action failing silently.
  - Rule: this story uses Google Maps; provider choice is confirmed as a development-team implementation decision, not a fixed requirement — see OQ-006 [RESOLVED CHG-004]. No rework needed; Google Maps as already built stands.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-026
- **Grounding:** Direct
- **Depends on / Blocked by:** US-103
- **Status:** Ready [CHG-004 — OQ-006 resolved, provider is a dev decision, no rework needed]
- **Delivery status:** Not started

### US-105 — CPR/AED reference
- **Type:** Story
- **Story:** As a volunteer, I want to look up basic CPR/AED guidance in the app, so that I can refresh my technique during a live event.
- **Acceptance criteria:**
  - Given the app is open, when the volunteer navigates to the reference section, then static CPR/AED guidance content is shown — reachable without needing an active alert.
  - Given the device is offline, when the volunteer opens the reference section, then the content still loads, since it is bundled with the app rather than fetched live.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-027
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Ready
- **Delivery status:** Not started

### US-106 — Post-event check-in
- **Type:** Story
- **Story:** As a volunteer, I want a quick check-in after an incident, so that I can confirm whether I arrived, was stood down, and optionally share how I'm doing.
- **Acceptance criteria:**
  - Given a volunteer accepted an alert, when the (mocked) incident ends, then they are prompted to answer "Did you arrive?" and "Were you stood down?" (both yes/no).
  - Given the check-in is shown, when the volunteer submits without answering the optional wellbeing follow-up, then the check-in still completes successfully.
  - Given a volunteer declined the alert (never accepted), when the incident ends, then no check-in is shown to them.
- **Priority:** Should · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-028, REQ-F-029, REQ-F-030
- **Grounding:** Direct
- **Depends on / Blocked by:** US-103
- **Status:** Ready
- **Delivery status:** Not started

---

## EPIC-3 — API & module scaffold (Repo: backend-api)

### ENABLER-001 — Scaffold the modular monolith
- **Type:** Enabler
- **Goal:** Set up the backend-api repository as a single-repo modular monolith with six module boundaries — Auth/MFA/Roles, Volunteers + Accounts, Incidents + Audit, Geospatial, Notifications, Countries/Config (per CON-003) — each as a clearly bounded module (most can be empty stubs at this point), plus a basic health-check endpoint.
- **Done when:** the repository builds and runs with the six module boundaries in place and a health-check endpoint responds.
- **Priority:** Must · **Phase/Sprint:** Phase 1 (first)
- **Traces to:** CON-003
- **Delivery status:** Not started

### ENABLER-002 — Basic incident CRUD endpoints
- **Type:** Enabler
- **Goal:** Inside the Incidents + Audit module, provide create/list/get/update REST endpoints for incidents (type, notes, country, location, status), with no authentication and no geospatial logic, backed by a datastore already partitioned per country (per CON-007) even though only one country is used in Phase 1 — so dispatcher-web can later swap its mock for real calls without a data-model change.
- **Done when:** the four endpoints exist, are independently testable, and their data shape matches the incident fields used in EPIC-1.
- **Priority:** Must · **Phase/Sprint:** Phase 1
- **Traces to:** REQ-F-002, REQ-F-003, REQ-F-004, REQ-F-005, REQ-F-010 (simplified), REQ-F-011, REQ-F-012 (simplified) — Derived, same Phase 1 framing as EPIC-1.
- **Depends on / Blocked by:** ENABLER-001
- **Delivery status:** Not started

### ENABLER-003 — Basic volunteer read endpoint
- **Type:** Enabler
- **Goal:** Inside the Volunteers + Accounts module, provide a read/list REST endpoint for volunteers returning name, tier, and status only (no history, no location, no availability), with no authentication, so dispatcher-web's volunteer list (US-006) and future sign-up work can integrate with real data later.
- **Done when:** the endpoint exists, is independently testable, and its response shape matches what US-006 needs to render.
- **Priority:** Should · **Phase/Sprint:** Phase 1
- **Traces to:** REQ-F-035 (partial)
- **Depends on / Blocked by:** ENABLER-001
- **Delivery status:** Not started

---

## Suggested build order — Phase 1

The three repos have no runtime dependency on each other in Phase 1 (each works against its own mock) and can be built in parallel by the team. Suggested order **within** each repo:

**dispatcher-web:** 1. US-001 → 2. US-002 → 3. US-003 → 4. US-004 → 5. US-005 → 6. US-006 (independent, can slot in anytime).

**volunteer-app:** 1. US-101 (sign-up) and US-105 (reference content) can start in parallel, both independent → 2. US-102 → 3. US-103 → 4. US-104 → 5. US-106.

**backend-api:** 1. ENABLER-001 (scaffold) → 2. ENABLER-002 and ENABLER-003 in parallel.

## Dependencies overview — Phase 1

| Story | Depends on | Reason |
|-------|-----------|--------|
| US-002 | US-001 | Needs incidents to exist to list/map them |
| US-003 | US-001 | Needs an incident to view |
| US-004 | US-001 | Needs an incident to edit |
| US-005 | US-004 | Uses the same status field |
| US-103 | US-102 | Accept/decline acts on a displayed alert |
| US-104 | US-103 | Navigation only applies after accepting |
| US-106 | US-103 | Check-in only applies to volunteers who engaged with an alert |
| ENABLER-002 | ENABLER-001 | Endpoints live inside the module scaffold |
| ENABLER-003 | ENABLER-001 | Same as above |

## Items sent back — Phase 1 (not turned into stories)

None this round. Everything identified as needing real backend logic, auth, or unresolved decisions (geospatial search, tiered alerting, real push, certification workflow, country configurability, roles/permissions) is documented as a Phase 2 theme in 02-scope-and-context-v1.md §4 rather than invented as a Phase 1 story.

---

## Phase 2 Backlog

## EPIC-4 — Authentication & roles

### US-201 — Log in with role-based access
- **Type:** Story
- **Story:** As a dispatcher or admin, I want to log in to the console with an account tied to my role, so that I only see and can do what my role allows.
- **Acceptance criteria:**
  - Given valid credentials for a dispatcher account, when the user logs in, then they reach the console with dispatcher-level access (create/manage/dispatch incidents; no cross-incident oversight view).
  - Given valid credentials for an admin account, when the user logs in, then they reach the console with admin-level access (oversight of all dispatchers and incidents, per REQ-F-001 [CHG-005]).
  - Given invalid credentials, when the user attempts to log in, then access is denied with a generic "invalid credentials" message (no hint about which field was wrong).
  - Rule: least-privilege applies (REQ-N-007) — a dispatcher account never sees admin-only screens or actions, regardless of URL/API access attempts.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-4 · **Traces to:** REQ-F-001, REQ-N-007
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — not needed to make the core notification loop (EPIC-5/7) real; Phase 1 already proved the dispatcher side works without login.
- **Delivery status:** Not started
- **Notes:** Encryption scope (REQ-N-006) and audit logging (REQ-N-008) apply to this story's login flow but are tracked as cross-cutting NFRs below (see "Non-functional requirements — Phase 2"), not as separate acceptance criteria here. OQ-010 resolved [CHG-016]: minimum HTTPS/TLS in transit plus at-rest encryption for sensitive fields via the chosen datastore's defaults, no specific key-management scheme mandated.

### US-202 — Complete MFA at login
- **Type:** Story
- **Story:** As a dispatcher or admin, I want to confirm my identity with a second verification step when logging in, so that my account can't be accessed with just a stolen password.
- **Acceptance criteria:**
  - Given correct credentials, when the user submits them, then they are prompted for a second factor before reaching the console.
  - Given a correct second factor, when submitted, then the user reaches the console.
  - Given an incorrect second factor, when submitted, then access is denied and the user may retry.
  - Rule: MFA is required for every dispatcher and admin account, no opt-out (REQ-N-005).
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-4 · **Traces to:** REQ-N-005
- **Grounding:** Direct
- **Depends on / Blocked by:** US-201
- **Status:** Deferred to Phase 3 [CHG-009] — explicitly deferred by Mohamed; builds on US-201 (also deferred).
- **Delivery status:** Not started
- **Notes:** The specific MFA mechanism (SMS, authenticator app, email code, etc.) is not specified in the requirements — that choice is left to the development team, same principle as the OQ-003/004/005/006 resolutions (CHG-006/007/008/004): the requirement is that a second factor exists, not which one.

### US-203 — Admin: cross-incident oversight
- **Type:** Story
- **Story:** As an admin, I want to see all dispatchers and all their incidents in one view, so that I can oversee dispatch activity across the whole system rather than one incident at a time.
- **Acceptance criteria:**
  - Given the admin is logged in, when they open the oversight view, then they see a list of all dispatchers and, for each, their currently open and recently closed incidents.
  - Given the admin selects a specific incident from this view, when they open it, then they see the same incident detail a dispatcher would see (REQ-F-012 full audit trail included).
  - Given a dispatcher (not admin) attempts to reach this view directly, when they try, then access is denied (least-privilege, REQ-N-007).
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-4 · **Traces to:** REQ-F-001
- **Grounding:** Direct
- **Depends on / Blocked by:** US-201 (also deferred)
- **Status:** Deferred to Phase 3 [CHG-009] — depends on login (US-201), which is deferred.
- **Delivery status:** Not started

---

## EPIC-5 — Volunteer matching & alerting

### US-204 — See nearby volunteers within radius bands
- **Type:** Story
- **Story:** As a dispatcher, I want to see which trained volunteers are available within configurable radius bands around the patient, so that I know who I could alert before sending anything.
- **Acceptance criteria:**
  - Given an incident with a location set, when the dispatcher opens the nearby-volunteers view, then volunteers are listed grouped by radius band (e.g. inner/outer band), with band distances set as simple system-wide configuration for now (not per-country — see Notes).
  - Given a volunteer's availability is set to "do-not-disturb" (REQ-F-019), when the search runs, then that volunteer is excluded from the results.
  - Given no volunteers are found within any configured band, when the dispatcher opens the view, then an explicit "no volunteers found nearby" state is shown, not an empty/broken list.
- **Priority:** Must · **Size:** L (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-5 · **Traces to:** REQ-F-006, REQ-F-031
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Ready
- **Delivery status:** Not started
- **Notes:** [CHG-009] Per-country-configurable radius bands (REQ-N-016) is deferred along with the rest of country portability (EPIC-8) — build with one simple, system-wide set of radius bands for now; making it per-country configurable is a Phase 3 extension, not a rebuild. Also, since background-location consent/tracking (US-214) is deferred, this search uses each volunteer's registered/last-known location rather than continuous live GPS — flag this as a stated simplification, not an invented requirement. REQ-N-017 (sub-second response) is a performance target — tracked under "Non-functional requirements — Phase 2" below; OQ-007 resolved [CHG-011] — kept simple, a flat "under 1 second," no benchmark methodology specified. The specific geospatial database/indexing technology is a development-team decision (OQ-003 resolved — CHG-006).

### US-205 — Send an alert to identified volunteers
- **Type:** Story
- **Story:** As a dispatcher, I want to send an alert to the volunteers found nearby with a single action, so that I don't have to contact each one individually.
- **Acceptance criteria:**
  - Given the nearby-volunteers view is open with results, when the dispatcher presses "Send alert," then all volunteers in the first tier band receive a notification (mechanics of delivery covered in EPIC-7) and their status becomes "notified."
  - Given the dispatcher presses "Send alert" a second time for the same incident while it's still active, when they do, then no duplicate alert is sent to volunteers already notified (idempotent).
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-5 · **Traces to:** REQ-F-007
- **Grounding:** Direct
- **Depends on / Blocked by:** US-204, US-206
- **Status:** Ready
- **Delivery status:** Not started

### US-206 — Tiered notification order
- **Type:** Story
- **Story:** As a dispatcher, I want the alert to go to trained responders first, so that the most qualified volunteers get the first chance to respond.
- **Acceptance criteria:**
  - Given nearby volunteers span more than one tier, when an alert is sent, then certified/verified CPR-BLS **and** healthcare-professional volunteers are notified together in the first wave, ahead of the willing-but-untrained tier (REQ-F-008, tier breakdown confirmed — OQ-001 [CHG-003]; "trained" defined — AS-001 [CHG-010]).
  - Rule: tiering/ordering/distance rules use one simple, system-wide configuration for now — per-country configurability (REQ-N-016, EPIC-8) is deferred to Phase 3 [CHG-009], not built here.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-5 · **Traces to:** REQ-F-008, REQ-F-032
- **Grounding:** Direct — AS-001 resolved [CHG-010]: "trained volunteers" means certified/verified CPR-BLS and healthcare professional combined, not certified alone.
- **Depends on / Blocked by:** —
- **Status:** Ready [CHG-010]
- **Delivery status:** Not started

### US-207 — Widen the alert pool after a timeout
- **Type:** Story
- **Story:** As a dispatcher, I want the system to automatically widen the alert to the next tier if nobody accepts in time, so that the patient isn't left waiting on a pool that isn't responding.
- **Acceptance criteria:**
  - Given a tier has been notified and a configurable time window (N seconds) elapses with no acceptance, when the window expires, then the next broader tier is notified.
  - Given a volunteer in the original tier accepts just as the window is about to expire, when the acceptance is recorded before expiry, then widening does not occur.
  - Rule: the widening window (N) and the widening order are configurable system-wide (REQ-F-009), not hard-coded — but not per-country yet; per-country configurability (REQ-N-016) is deferred with the rest of country portability [CHG-009].
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-5 · **Traces to:** REQ-F-009
- **Grounding:** Direct
- **Depends on / Blocked by:** US-206
- **Status:** Ready
- **Delivery status:** Not started
- **Notes:** How the 5s/95% delivery target and this widening delay get measured/monitored in production (OQ-015) is still open — do not build a monitoring dashboard against a guessed methodology; the widening logic itself is not blocked by this.

### US-208 — Live per-volunteer status view
- **Type:** Story
- **Story:** As a dispatcher, I want to see each notified volunteer's live status, so that I know exactly where the response stands without having to ask.
- **Acceptance criteria:**
  - Given an incident has notified volunteers, when the dispatcher views it, then each volunteer shows one of: notified, accepted, declined, en route, arrived, stood down.
  - Given a volunteer's status changes, when it changes, then the dispatcher's view updates live, without a manual page refresh (per CON-005's WebSocket channel).
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-5 · **Traces to:** REQ-F-010 (full)
- **Grounding:** Direct
- **Depends on / Blocked by:** US-205
- **Status:** Ready
- **Delivery status:** Not started
- **Notes:** OQ-013 resolved [CHG-014]: a volunteer cannot back out after already accepting — once accepted, accepted. No "back out" status or handling in this view.

### US-209 — Full dispatch audit trail
- **Type:** Story
- **Story:** As a dispatcher, I want a complete, viewable record of everything that happened during a dispatch, so that we can review or account for what occurred after the fact.
- **Acceptance criteria:**
  - Given an incident has been through any dispatch activity, when the audit trail is viewed, then it shows who was notified, when, who responded and how, and the final outcome, in chronological order.
  - Given an incident is still open, when the audit trail is viewed, then it reflects events up to the current moment (not just a post-closure summary).
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-5 · **Traces to:** REQ-F-012 (full)
- **Grounding:** Direct
- **Depends on / Blocked by:** US-205
- **Status:** Ready
- **Delivery status:** Not started
- **Notes:** [CHG-009] Written for the dispatcher only for now — the admin cross-incident view that also consumed this trail (US-203) is deferred to Phase 3; nothing here needs to change when that lands, it just gets a second consumer later. REQ-N-010 (patient location shall not be retained longer than necessary) applies to this trail's data — OQ-009 resolved [CHG-012]: 90-day retention, a placeholder value pending real legal review per deployment jurisdiction.

---

## EPIC-6 — Certification, availability & privacy

### US-210 — Upload certification documentation
- **Type:** Story
- **Story:** As a volunteer, I want to upload proof of my certification, so that the system can verify my training tier.
- **Acceptance criteria:**
  - Given the volunteer is signed up, when they upload a certification document (image or PDF), then it is stored against their account with status "pending verification."
  - Given the volunteer attempts to upload an unsupported file type, when they try, then the upload is rejected with a message stating the supported formats.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-6 · **Traces to:** REQ-F-016
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — the tiered-alert logic (US-206) already works off a volunteer's self-declared tier from Phase 1 sign-up (US-101), same as Phase 1 did; formal certification verification is a trust/compliance improvement, not required to make alerting work.
- **Delivery status:** Not started

### US-211 — Track certification expiry
- **Type:** Story
- **Story:** As the system, I want to track when a volunteer's certification expires, so that expired certifications are visible before they cause a problem in the field.
- **Acceptance criteria:**
  - Given a volunteer's certification has an expiry date, when that date passes, then the certification is flagged "expired" on the volunteer's record and to any admin viewing it.
  - Given a certification is not yet expired, when viewed, then its status remains "valid" with the expiry date shown.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-6 · **Traces to:** REQ-F-017
- **Grounding:** Direct
- **Depends on / Blocked by:** US-210 (also deferred)
- **Status:** Deferred to Phase 3 [CHG-009] — depends on certification upload (US-210), which is deferred.
- **Delivery status:** Not started
- **Notes:** OQ-014 resolved [CHG-017]: once flagged expired, the volunteer is excluded from new alerts until re-verified — no automatic tier demotion. This story covers tracking and flagging; the exclusion behaviour itself is enforced at alert-send time (US-206/US-205), not here.

### US-212 — Remind volunteer to re-verify before expiry
- **Type:** Story
- **Story:** As a volunteer, I want to be reminded before my certification expires, so that I can re-verify in time and stay eligible for alerts.
- **Acceptance criteria:**
  - Given a volunteer's certification is approaching its expiry date, when the reminder trigger point is reached, then the volunteer receives a reminder (channel/timing per dev's implementation).
  - Given a volunteer re-verifies before expiry, when they do, then no further reminders are sent for that certification cycle.
- **Priority:** Should · **Size:** S (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-6 · **Traces to:** REQ-F-018
- **Grounding:** Direct
- **Depends on / Blocked by:** US-211 (also deferred)
- **Status:** Deferred to Phase 3 [CHG-009] — depends on certification expiry tracking (US-211), which is deferred.
- **Delivery status:** Not started
- **Notes:** Exact timing/channel of the reminder isn't specified in the brief — left to the dev team, same principle as the delegated technical OQs.

### US-213 — Set availability
- **Type:** Story
- **Story:** As a volunteer, I want to set my availability (always on, scheduled, or do-not-disturb), so that I'm only alerted when I'm actually able to respond.
- **Acceptance criteria:**
  - Given the volunteer opens availability settings, when they select "always on," "scheduled" (with a time range), or "do-not-disturb," then the selection is saved and takes effect immediately.
  - Given a volunteer is set to "do-not-disturb," when a nearby-volunteer search runs (US-204), then they are excluded from results.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-6 · **Traces to:** REQ-F-019
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Ready
- **Delivery status:** Not started

### US-214 — Give consent for background location collection
- **Type:** Story
- **Story:** As a volunteer, I want to explicitly consent (or not) to background location collection, so that I'm in control of when the app tracks my location.
- **Acceptance criteria:**
  - Given the volunteer is asked for background-location consent, when they grant it, then a consent record is stored with a timestamp (REQ-F-023) and location collection begins only from that point.
  - Given the volunteer declines consent, when they do, then no background location is collected, and the app states this may limit how they're matched to nearby incidents.
  - Rule: location is collected only while an incident/event is active, or with explicit opt-in otherwise (REQ-N-011) — never collected silently in the background outside those cases.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-6 · **Traces to:** REQ-F-020, REQ-F-023, REQ-N-011
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — continuous background-location tracking is real infrastructure, not needed for the simple core loop. US-204's nearby-volunteer search uses each volunteer's registered/last-known location instead for now (see US-204's Notes) — a stated simplification, not silently dropped scope.
- **Delivery status:** Not started
- **Notes:** REQ-N-018 (battery-friendly tracking) applies here — OQ-008 resolved [CHG-015]: no concrete sampling-interval or battery-drain number, "reasonable battery use, no aggressive constant GPS polling," left to the dev team's discretion.

### US-215 — View volunteer status and certification history (admin)
- **Type:** Story
- **Story:** As an admin, I want to see a volunteer's full status and certification history, not just their current state, so that I can review how their standing changed over time.
- **Acceptance criteria:**
  - Given a volunteer has had tier, status, or certification changes over time, when an admin opens their profile, then a chronological history of those changes is shown, not just the current values.
  - Given a volunteer has no history yet (newly signed up), when viewed, then the history shows only the sign-up event.
- **Priority:** Should · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-6 · **Traces to:** REQ-F-035 (full — extends Phase 1's ENABLER-003 read-only, no-history endpoint)
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — an admin-facing view; admin (US-203) is deferred, and this was already "Should" priority, lowest urgency in this epic.
- **Delivery status:** Not started

---

## EPIC-7 — Real push delivery

### US-216 — Receive a real push alert via FCM
- **Type:** Story
- **Story:** As a volunteer, I want to receive a real push notification when I'm identified as a nearby responder, so that I find out about an incident even if the app isn't open.
- **Acceptance criteria:**
  - Given a volunteer is identified as a nearby responder and an alert is sent (US-205), when the alert is dispatched, then a push notification is delivered to their device via FCM (REQ-F-033), replacing Phase 1's in-app-only mocked display (US-102).
  - Given the volunteer taps the notification, when they do, then the app opens directly to that alert's detail screen.
  - Rule: alerts should reach the volunteer's phone within 5 seconds, 95% of the time (REQ-N-001). Exact production measurement/monitoring methodology is not yet defined (OQ-015, open) — build the delivery path to this target, but do not build a monitoring dashboard against an unconfirmed measurement definition.
- **Priority:** Must · **Size:** L (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-7 · **Traces to:** REQ-F-021 (full), REQ-F-033, REQ-N-001
- **Grounding:** Direct
- **Depends on / Blocked by:** US-205
- **Status:** Ready
- **Delivery status:** Not started
- **Notes:** OQ-012 resolved [CHG-013]: offline/no-signal/force-closed counts simply as "not reached" — no retry/queueing logic; widening (US-207) proceeds as if the alert had been ignored.

### US-217 — Push alert attempts DND bypass
- **Type:** Story
- **Story:** As a volunteer, I want the alert to try to get through even if my phone is on silent or do-not-disturb, so that I don't miss a nearby cardiac-arrest call because of a phone setting.
- **Acceptance criteria:**
  - Given the volunteer's device is in silent/DND mode and platform settings allow an override, when an alert is sent, then the notification attempts to bypass silent/DND (REQ-F-022, best-effort — Should priority, not Must).
  - Given the platform or the user's own settings do not allow an override, when an alert is sent, then the notification is still delivered through the normal channel (no error), even if it doesn't audibly interrupt DND.
- **Priority:** Should · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-7 · **Traces to:** REQ-F-022
- **Grounding:** Direct
- **Depends on / Blocked by:** US-216 (which stays in Phase 2)
- **Status:** Deferred to Phase 3 [CHG-009] — a best-effort ("Should") enhancement on top of basic push (US-216); get plain delivery working first.
- **Delivery status:** Not started
- **Notes:** The specific technical mechanism for maximising DND-bypass reliability is delegated to the development team (OQ-004 resolved — CHG-007); this story only specifies the functional behaviour, not the implementation.

### US-218 — Track push delivery status
- **Type:** Story
- **Story:** As a dispatcher, I want to know whether a push alert actually reached each volunteer, so that I can tell a real non-response apart from a delivery failure.
- **Acceptance criteria:**
  - Given an alert has been sent to a volunteer, when delivery is attempted, then the system records "delivered" or "not reached" per volunteer per alert (REQ-F-034).
  - Given a volunteer's delivery status is "not reached," when the dispatcher views that volunteer's status (US-208), then this is visibly distinguished from "notified but no response yet."
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 2
- **Epic:** EPIC-7 · **Traces to:** REQ-F-034
- **Grounding:** Direct
- **Depends on / Blocked by:** US-216
- **Status:** Ready
- **Delivery status:** Not started

---

## EPIC-8 — Country portability & admin tools

### US-219 — Country-scoped data visibility
- **Type:** Story
- **Story:** As a dispatcher or admin, I want to only see and manage incidents and volunteers in my own country/jurisdiction, so that I'm not working across data that isn't mine to handle.
- **Acceptance criteria:**
  - Given a user's account is tied to a country, when they view incidents or volunteers, then only records from their own country are shown.
  - Rule: the underlying data is partitioned per country at the storage level (REQ-F-036, REQ-N-004), extending Phase 1's ENABLER-002 datastore shape (which was built with this partitioning in mind but not enforced).
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-8 · **Traces to:** REQ-F-036, REQ-N-004
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — country portability (the whole of EPIC-8) is explicitly deferred; the system runs single-country for now.
- **Delivery status:** Not started

### US-220 — Configure country-specific settings
- **Type:** Story
- **Story:** As an admin, I want to configure language, address format, the local emergency number, and units of measurement for my country, so that the system reads correctly and makes sense to local users without needing a code change.
- **Acceptance criteria:**
  - Given the admin opens country settings, when they set the display language, then the console and app content render in that language for users in that country.
  - Given the admin sets the local address format and units of measurement, when incidents/volunteers are displayed, then addresses and distances render in that country's configured format/units.
  - Given the admin sets the local emergency number, when it's referenced anywhere in the app/console, then the configured number is shown, not a hard-coded default.
- **Priority:** Must · **Size:** L (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-8 · **Traces to:** REQ-N-012, REQ-N-013, REQ-N-014, REQ-N-015
- **Grounding:** Direct
- **Depends on / Blocked by:** US-219 (also deferred)
- **Status:** Deferred to Phase 3 [CHG-009] — country portability deferred; this was also flagged as the single largest/riskiest story in the original draft (bundles 4 requirements), worth splitting when it's actually picked up.
- **Delivery status:** Not started
- **Notes:** The technical mechanism for this configurability (e.g. how the Countries/Config module is internally shaped) is delegated to the development team (OQ-005 resolved — CHG-008); this story specifies only the functional/admin-facing behaviour.

### US-221 — Configure country-specific alerting rules
- **Type:** Story
- **Story:** As an admin, I want to configure who gets alerted, in what order, and at what distance for my country, so that the alert logic matches local practice without needing a separate build per country.
- **Acceptance criteria:**
  - Given the admin opens alerting-rule settings for their country, when they set the tier order and radius-band distances, then subsequent alerts in that country follow the configured order/distances (feeds US-204, US-206).
  - Given no country-specific override is set, when an alert runs, then a documented default order/distance is used rather than failing or behaving unpredictably.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-8 · **Traces to:** REQ-N-016, REQ-F-032
- **Grounding:** Direct
- **Depends on / Blocked by:** US-219 (also deferred), US-206 (stays in Phase 2, runs on a simple system-wide config until this lands)
- **Status:** Deferred to Phase 3 [CHG-009] — country portability deferred; US-206/US-207 use one simple system-wide configuration in the meantime.
- **Delivery status:** Not started

### US-222 — Admin manages volunteers
- **Type:** Story
- **Story:** As an admin, I want to view, activate, or deactivate volunteer accounts, so that I can keep the volunteer pool accurate and remove people who should no longer be alerted.
- **Acceptance criteria:**
  - Given the admin opens the volunteer management view, when they select a volunteer, then they can view full details and toggle the account between active and deactivated.
  - Given a volunteer is deactivated, when a nearby-volunteer search runs (US-204), then that volunteer is excluded from results.
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-8 · **Traces to:** REQ-F-037
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — admin tooling; admin (US-203) is deferred.
- **Delivery status:** Not started
- **Notes:** OQ-014 resolved [CHG-017]: an in-flight incident is never interrupted — a volunteer already notified/accepted stays active on that incident even if deactivated mid-response. No auto-widening or auto-reassignment triggered by the deactivation.

### US-223 — Admin verifies volunteer certifications
- **Type:** Story
- **Story:** As an admin, I want to review and approve or reject an uploaded certification, so that only genuinely certified volunteers are marked as such in the system.
- **Acceptance criteria:**
  - Given a volunteer has uploaded a certification with status "pending verification" (US-210), when the admin reviews it, then they can mark it "verified" or "rejected" with an optional reason.
  - Given a certification is marked "verified," when the volunteer's tier depends on it, then their tier status reflects "verified" rather than "pending."
- **Priority:** Must · **Size:** M (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-8 · **Traces to:** REQ-F-038
- **Grounding:** Direct
- **Depends on / Blocked by:** US-210 (also deferred)
- **Status:** Deferred to Phase 3 [CHG-009] — depends on certification upload (US-210) and admin (US-203), both deferred.
- **Delivery status:** Not started

### US-224 — Admin manages in-app reference content
- **Type:** Story
- **Story:** As an admin, I want to update the in-app CPR/AED reference content, so that volunteers always see current guidance without needing an app release for every wording change.
- **Acceptance criteria:**
  - Given the admin opens content management, when they edit the CPR/AED reference text, then the updated content is what volunteers see in the app's reference section (US-105) without an app update.
  - Given the admin saves invalid/empty content, when they try, then the save is rejected and the previous content remains live.
- **Priority:** Should · **Size:** S (provisional) · **Phase/Sprint:** Phase 3 [CHG-009 — deferred from Phase 2]
- **Epic:** EPIC-8 · **Traces to:** REQ-F-039
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Deferred to Phase 3 [CHG-009] — admin tooling, lowest urgency ("Should"), no dependents.
- **Delivery status:** Not started

---

## Non-functional requirements — Phase 2 (tracked, not individually story'd)

These are cross-cutting quality targets rather than standalone user stories (per the product-backlog skill: technical/system qualities aren't forced into "As a user..." format). Each is tied to the story/epic it constrains; the delivery team should treat these as ongoing engineering constraints on the stories above, not one-off tickets. **[CHG-009]** Most NFRs below moved to Phase 3 along with the stories they were attached to (auth, country config, cert/admin tooling); only what still applies to the trimmed Phase 2 scope is listed here.

| Requirement | Constrains | Status |
|-------------|-----------|--------|
| REQ-N-002 (99.9% uptime, dispatch path) | EPIC-5 (US-204..209) | Open — no blocking OQ, but no measurement approach defined yet either; track alongside OQ-015. |
| REQ-N-003 (graceful degradation if a dependency fails) | EPIC-5, EPIC-7 (US-216, US-218) | Open — no blocking OQ; standard engineering practice, not a story. |
| REQ-N-017 (sub-second nearby-volunteer search) | EPIC-5 (US-204) | OQ-007 resolved [CHG-011] — kept simple, flat "under 1 second," no benchmark methodology specified. |

Deferred to Phase 3 with their stories: REQ-N-006 (encryption), REQ-N-007 (least-privilege), REQ-N-008 (audit logging) — all attached to EPIC-4 (deferred); REQ-N-018 (battery-friendly location) — attached to US-214 (deferred); REQ-N-004, REQ-N-012..016 (country portability) — attached to EPIC-8 (deferred).

---

## Suggested build order — Phase 2

Phase 2 is now just the simple core loop (9 stories), so the order is short:

1. **US-204** (nearby volunteers) → 2. **US-206** (tiered order) → 3. **US-205** (send alert) → 4. **US-207** (widen pool) → 5. **US-208** (live status) → 6. **US-209** (audit trail) — the core dispatch loop, in dependency order.
7. **US-216** (real push) → 8. **US-218** (delivery tracking) — push delivery, once there's an alert-send path (step 3) to hook into.
9. **US-213** (availability) — independent of the dispatch loop, can be built any time in parallel (feeds an exclusion rule into US-204).

## Dependencies overview — Phase 2

| Story | Depends on | Reason |
|-------|-----------|--------|
| US-205 | US-204, US-206 | Needs to know who's nearby and in what tier order before sending |
| US-207 | US-206 | Widening operates on the same tier sequence |
| US-208 | US-205 | Status view only makes sense once an alert has been sent |
| US-209 | US-205 | Audit trail records events starting from alert send |
| US-216 | US-205 | Push delivers the alert that US-205 triggers |
| US-218 | US-216 | Tracks delivery of the same push |

## Items sent back — Phase 2 (not turned into stories)

- **AED-fetch flow / AED registry** — still explicitly out of scope per the brief; blocked on OQ-002 (AED data sourcing), which remains unresolved. Not drafted as a story.
- **Reporting & analytics** — still explicitly deferred per the brief; no requirements captured for it yet (would need its own requirements-structuring pass before it could become a story).
- **iOS volunteer app** — still "Android only for now" (CON-001); no story drafted.
- **Volunteer back-out-after-accepting behaviour, offline/force-closed device handling, and certification-expiry consequences** — OQ-013, OQ-012, and OQ-014 resolved [CHG-014, CHG-013, CHG-017]; each answer is simple enough to fold directly into the existing stories' acceptance criteria (US-208/US-103, US-216, US-211/US-222) rather than needing its own new story.

---

## Phase 3 (deferred, CHG-009) — auth, certification, country portability, admin tools

Fifteen stories, fully written with specs, kept exactly as drafted — nothing deleted, IDs unchanged, ready to pick up whenever this work is prioritized. Reassigned from Phase 2 on 2026-07-13 because none of them are needed to make the simple core notification loop (find volunteer → alert → notify → respond → track) work; they add real auth/security/i18n/admin infrastructure on top of it.

**EPIC-4 — Authentication & roles:** US-201 (login), US-202 (MFA), US-203 (admin oversight).
**EPIC-6 remainder — Certification & privacy:** US-210 (upload cert), US-211 (track expiry), US-212 (expiry reminder), US-214 (location consent), US-215 (volunteer history).
**EPIC-7 remainder:** US-217 (DND bypass).
**EPIC-8 — Country portability & admin tools:** US-219 (country-scoped data), US-220 (country settings), US-221 (country alerting rules), US-222 (admin manages volunteers), US-223 (admin verifies certs), US-224 (admin manages content).

**Suggested order whenever Phase 3 is picked up:** 1. US-201 → 2. US-202 → 3. US-203 (auth foundation first, everything else in this bucket is role-gated) → 4. US-219 → 5. US-220 → 6. US-221 (country foundation) → 7. US-210 → 8. US-223 → 9. US-211 → 10. US-212 (certification lifecycle) → 11. US-214 → 12. US-215 → 13. US-217 → 14. US-222 → 15. US-224 (remaining, lowest urgency).

**Note for whoever picks this up:** US-220 was already flagged as oversized (bundles 4 requirements) — split it before sprinting on it.

## Definition of Ready / Done

- **Ready (per story):** clear role + benefit; testable acceptance criteria incl. edge cases; provisional size; dependencies identified; no blocking open question (or explicitly marked "Ready (conditional)" with the assumption stated).
- **Done:** to be defined by the delivery team.
