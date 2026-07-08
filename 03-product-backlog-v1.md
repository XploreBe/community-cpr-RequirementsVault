# Product Backlog — Community CPR Volunteer Dispatch (Phase 1)

**Based on:** 02-scope-and-context-v1.md, 01-requirements-structured-v1.md
**Date:** 2026-07-06
**Produced by:** product-backlog skill
**Status:** Draft — for refinement with the team

## Legend

- **Repo:** volunteer-app · dispatcher-web · backend-api — which GitHub repository this item belongs to.
- **Priority:** MoSCoW (Must / Should / Could / Won't)
- **Size:** S / M / L — relative, provisional (confirm in refinement)
- **Type:** Story / Spike / Enabler
- **Status:** New · Backlog · Ready (conditional — assumption stated) · Not Ready (reason) — BA-readiness, not delivery progress
- **Delivery status:** Not started · In Progress · Done — manually maintained by the delivery team; not touched by any pipeline skill
- **Grounding:** Direct (traces to a stated requirement) · Derived (rests on the Phase 1 walking-skeleton simplification agreed with Mohamed — see 02-scope-and-context-v1.md §3 — or another stated assumption)

This backlog covers **Phase 1 only** (the walking skeleton). Phase 2 and later items are listed by theme in 02-scope-and-context-v1.md §4 but not yet broken into stories — that is a follow-up backlog pass once Phase 1 ships and the open questions blocking Phase 2 (OQ-001, OQ-003, OQ-004, OQ-005, OQ-011 — see 02-scope-and-context-v1.md §9) are resolved.

## Epics

| Epic ID | Repo | Title | Outcome | Requirement IDs | Phase |
|---------|------|-------|---------|-----------------|-------|
| EPIC-1 | dispatcher-web | Incident record management | A dispatcher can create, view, update, and resolve incident records with a location, and browse a list of volunteers — no login, no real backend | REQ-F-002..005, 010 (simplified), 011, 012 (simplified), 013 | Phase 1 |
| EPIC-2 | volunteer-app | Alert response walking skeleton | A volunteer can sign up, see a mocked alert, accept/decline, navigate to the scene, consult CPR guidance, and check in afterward — no login, no real push | REQ-F-014, 015, 024, 025, 026, 027, 028, 029, 030 | Phase 1 |
| EPIC-3 | backend-api | API & module scaffold | The backend has its module boundaries in place plus minimal CRUD endpoints for incidents and a read endpoint for volunteers — no auth, no geospatial/alert/push logic | CON-003, REQ-F-035 (partial) | Phase 1 |

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
  - Rule: the tier options offered are the brief's three provisional names (certified, healthcare professional, willing-but-untrained) — not final, see OQ-001.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-014, REQ-F-015
- **Grounding:** Direct
- **Depends on / Blocked by:** —
- **Status:** Ready (conditional — scoped under OQ-001's provisional tier list; final breakdown may require rework)
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
  - Rule: this story uses Google Maps per the brief's text; it does not resolve OQ-006 (the architecture diagram references OpenStreetMap/MapLibre/OSRM instead) — if that source is confirmed as the intended provider, this story needs rework.
- **Priority:** Must · **Size:** S (provisional) · **Phase/Sprint:** Phase 1
- **Epic:** EPIC-2 · **Traces to:** REQ-F-026
- **Grounding:** Direct (for the capability); the specific provider choice is conditional.
- **Depends on / Blocked by:** US-103
- **Status:** Ready (conditional — scoped under OQ-006's Google Maps assumption)
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

## Suggested build order (this phase)

The three repos have no runtime dependency on each other in Phase 1 (each works against its own mock) and can be built in parallel by the team. Suggested order **within** each repo:

**dispatcher-web:** 1. US-001 → 2. US-002 → 3. US-003 → 4. US-004 → 5. US-005 → 6. US-006 (independent, can slot in anytime).

**volunteer-app:** 1. US-101 (sign-up) and US-105 (reference content) can start in parallel, both independent → 2. US-102 → 3. US-103 → 4. US-104 → 5. US-106.

**backend-api:** 1. ENABLER-001 (scaffold) → 2. ENABLER-002 and ENABLER-003 in parallel.

## Dependencies overview

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

## Items sent back (not turned into stories)

None this round. Everything identified as needing real backend logic, auth, or unresolved decisions (geospatial search, tiered alerting, real push, certification workflow, country configurability, roles/permissions) is documented as a Phase 2 theme in 02-scope-and-context-v1.md §4 rather than invented as a Phase 1 story.

## Definition of Ready / Done

- **Ready (per story):** clear role + benefit; testable acceptance criteria incl. edge cases; provisional size; dependencies identified; no blocking open question (or explicitly marked "Ready (conditional)" with the assumption stated).
- **Done:** to be defined by the delivery team.
