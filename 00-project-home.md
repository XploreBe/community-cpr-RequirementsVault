# Community CPR Volunteer Dispatch

**Pipeline run:** 2026-07-06
**Status:** Phase 1 (walking skeleton) fully structured, scoped, backlogged, and spec'd. Phase 2 (the brief's actual MVP: login, real backend, real alerting, security/privacy/portability) is scoped by theme but not yet broken into stories.

> **New here?** → [[00-how-to-use|How to use this vault]]

## What this project is

A 911/112 dispatcher pins a cardiac-arrest patient on a map, the system finds nearby trained volunteers, and alerts them with one tap. The volunteer accepts, navigates to the scene, and starts CPR until EMS arrives — with certified volunteers prioritised but untrained bystanders still reachable. Built across four repos (volunteer-app, dispatcher-web, backend-api, e2e-tests) with portability across countries as a first-class design goal.

Phase 1, currently in this vault, is deliberately smaller than the brief's own "MVP" section: a walking skeleton per repo — no login, mocked data, no real cross-repo integration — so the team has something working to build on before tackling auth, real geospatial matching, real push delivery, and the security/privacy/portability requirements.

## Current status

**Phase 1** (dispatcher-web, volunteer-app, backend-api walking skeleton) is fully structured, scoped, backlogged, and spec'd. **Phase 2** (real login, real backend, real alerting, security/privacy/portability) is scoped by theme in [[02-scope-and-context-v1|scope & context]] §4 but not yet broken into stories.

**Backlog readiness (Phase 1)** — this table is kept accurate by change-management whenever a CHG changes a story's status, same as the rest of this page:

| Repo | Items | Ready | Ready (conditional) | Not Ready | Won't |
|------|------:|------:|---------------------:|----------:|------:|
| dispatcher-web | 6 | 6 | 0 | 0 | 0 |
| volunteer-app | 6 | 4 | 2 | 0 | 0 |
| backend-api | 3 | 3 | 0 | 0 | 0 |
| **Total** | **15** | **13** | **2** | **0** | **0** |

No Phase 1 story or enabler is blocked on an open question right now — the 2 "conditional" items rest on a stated assumption, not a block (see [[#Phase 1 blockers|Phase 1 blockers]] below).

**Delivery progress** — what the team is actually building right now — is tracked directly in the backlog, not duplicated here: every story/enabler in [[03-product-backlog-v1|the product backlog]] has a **Delivery status** field (Not started / In Progress / Done) that the team updates by hand as work happens. That keeps this page from ever showing a stale count. As of the last pipeline/CHG run, every Phase 1 item is still "Not started."

## Documents

- [[01-requirements-structured-v1|Structured requirements]] — REQ-F, REQ-N, CON, OQ, AS extracted from the project brief and the architecture diagram.
- [[02-scope-and-context-v1|Scope & context]] — Phase 1 (walking skeleton, all 3 repos) vs. Phase 2 (the brief's real MVP) vs. later/out of scope, with dependencies, effort/risk, and open scoping questions.
- [[03-product-backlog-v1|Product backlog]] — Phase 1 epics, stories, and enablers, tagged by repo (volunteer-app / dispatcher-web / backend-api), ready for GitHub issue sync per repo.
- [[04-speckit-specs/00-index|Speckit specs]] — one dev-ready spec per Phase 1 story/enabler. See [[04-speckit-specs/blocked-stories|blocked-stories]] for the two items that are Ready only under a stated assumption.
- [[05-traceability-matrix|Traceability matrix]] — REQ ↔ Story ↔ Spec lookups, plus constraints and open-question impact.
- [[06-change-log|Change log]] — full history of every CHG-xxx (empty so far).

## Recent changes

- **CHG-002** (2026-07-09) — Added coordinate-range validation (lat ∈ [-90, 90], lng ∈ [-180, 180]) to US-001 and US-004 ACs and specs → [[06-change-log]]

Full change history: [[06-change-log]]

## Phase 1 blockers

None. Every Phase 1 story/enabler is Ready or Ready (conditional) — see [[04-speckit-specs/blocked-stories|blocked-stories]]. Two items rest on a stated assumption rather than a resolved decision:

| Item | Repo | Conditional on |
|------|------|-----------------|
| US-101 — Sign up with tier | volunteer-app | OQ-001 — final volunteer tier breakdown |
| US-104 — Navigate to the scene | volunteer-app | OQ-006 — navigation provider conflict (brief says Google Maps, architecture diagram says OpenStreetMap/MapLibre/OSRM) |

Phase 2 will hit real blockers quickly — OQ-001, OQ-003, OQ-004, OQ-005, and OQ-011 each block a specific Phase 2 theme (tiering, geospatial search, push reliability, country abstraction, role permissions). See [[05-traceability-matrix|traceability matrix]] §5.

## Other

- [[00-pipeline-skills/00-skills-index|Pipeline skills index]]
- [[05-traceability-matrix]]
