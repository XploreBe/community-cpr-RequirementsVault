# Community CPR Volunteer Dispatch

**Pipeline run:** 2026-07-06
**Status:** Phase 1 (walking skeleton) fully structured, scoped, backlogged, and spec'd. Phase 2 (the brief's actual MVP: login, real backend, real alerting, security/privacy/portability) is scoped by theme but not yet broken into stories.

> **New here?** → [[00-how-to-use|How to use this vault]]

## What this project is

A 911/112 dispatcher pins a cardiac-arrest patient on a map, the system finds nearby trained volunteers, and alerts them with one tap. The volunteer accepts, navigates to the scene, and starts CPR until EMS arrives — with certified volunteers prioritised but untrained bystanders still reachable. Built across four repos (volunteer-app, dispatcher-web, backend-api, e2e-tests) with portability across countries as a first-class design goal.

Phase 1, currently in this vault, is deliberately smaller than the brief's own "MVP" section: a walking skeleton per repo — no login, mocked data, no real cross-repo integration — so the team has something working to build on before tackling auth, real geospatial matching, real push delivery, and the security/privacy/portability requirements.

## Documents

- [[01-requirements-structured-v1|Structured requirements]] — REQ-F, REQ-N, CON, OQ, AS extracted from the project brief and the architecture diagram.
- [[02-scope-and-context-v1|Scope & context]] — Phase 1 (walking skeleton, all 3 repos) vs. Phase 2 (the brief's real MVP) vs. later/out of scope, with dependencies, effort/risk, and open scoping questions.
- [[03-product-backlog-v1|Product backlog]] — Phase 1 epics, stories, and enablers, tagged by repo (volunteer-app / dispatcher-web / backend-api), ready for GitHub issue sync per repo.
- [[04-speckit-specs/00-index|Speckit specs]] — one dev-ready spec per Phase 1 story/enabler. See [[04-speckit-specs/blocked-stories|blocked-stories]] for the two items that are Ready only under a stated assumption.
- [[05-traceability-matrix|Traceability matrix]] — REQ ↔ Story ↔ Spec lookups, plus constraints and open-question impact.
- [[06-change-log|Change log]] — full history of every CHG-xxx (empty so far).

## Recent changes

- **CHG-001** (2026-07-08) — REQ-N-018 priority elevated from Should to Must (client confirmation) → [[06-change-log]]

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
