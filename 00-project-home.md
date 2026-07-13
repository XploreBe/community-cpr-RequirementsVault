# Community CPR Volunteer Dispatch

**Pipeline run:** 2026-07-06 (Phase 1); Phase 2 backlog + specs added 2026-07-13, then rescoped same day (CHG-009); remaining open questions/assumption resolved same day (CHG-010 through CHG-017)
**Status:** Phase 1 (walking skeleton) is fully structured, scoped, backlogged, and spec'd. **Phase 2 is now the simple core notification loop only** (9 stories, all fully Ready — no conditional items) — find nearby volunteers, alert them in tiered order, widen if unanswered, live status, audit trail, availability, real push, delivery tracking. Everything else from the brief's real MVP (login/MFA, certification workflow, location consent, country portability, admin tools — 15 stories) is fully drafted but deliberately deferred to **Phase 3**, per CHG-009. Phase 2/3 use no repo tags and no enablers/spikes — the team consolidated into one repository and moved to spec-driven development at pickup time (see CLAUDE.md).

> **New here?** → [[00-how-to-use|How to use this vault]]

## What this project is

A 911/112 dispatcher pins a cardiac-arrest patient on a map, the system finds nearby trained volunteers, and alerts them with one tap. The volunteer accepts, navigates to the scene, and starts CPR until EMS arrives — with certified volunteers prioritised but untrained bystanders still reachable. Built across four repos (volunteer-app, dispatcher-web, backend-api, e2e-tests) with portability across countries as a first-class design goal.

Phase 1, currently in this vault, is deliberately smaller than the brief's own "MVP" section: a walking skeleton per repo — no login, mocked data, no real cross-repo integration — so the team has something working to build on before tackling auth, real geospatial matching, real push delivery, and the security/privacy/portability requirements.

## Current status

**Phase 1** (dispatcher-web, volunteer-app, backend-api walking skeleton) is fully structured, scoped, backlogged, and spec'd. **Phase 2** was originally drafted as the full 24-story real-MVP theme from [[02-scope-and-context-v1|scope & context]] §4, then trimmed the same day (CHG-009) to just the simple core loop — 9 stories, no auth, no country config, no cert workflow — so the team has something straightforward to build first. The other 15 stories are fully written and spec'd, just reassigned to **Phase 3** (see below).

**Backlog readiness (Phase 1)** — repo-tagged, includes enablers, per the team's original multi-repo structure:

| Repo | Items | Ready | Ready (conditional) | Not Ready | Won't |
|------|------:|------:|---------------------:|----------:|------:|
| dispatcher-web | 6 | 6 | 0 | 0 | 0 |
| volunteer-app | 6 | 6 | 0 | 0 | 0 |
| backend-api | 3 | 3 | 0 | 0 | 0 |
| **Total** | **15** | **15** | **0** | **0** | **0** |

No Phase 1 story or enabler is blocked on an open question or a stated assumption anymore — US-101 and US-104 were the last two conditional items, and both were fully resolved by CHG-003 and CHG-004 (2026-07-13) with no rework needed (see [[#Phase 1 blockers|Phase 1 blockers]] below).

**Backlog readiness (Phase 2 — current round)** — one flat list, no repo tags, no enablers/spikes:

| Epic | Items | Ready | Ready (conditional) | Not Ready | Won't |
|------|------:|------:|---------------------:|----------:|------:|
| EPIC-5 — Volunteer matching & alerting | 6 | 6 | 0 | 0 | 0 |
| EPIC-6 (partial) — Volunteer availability (US-213 only) | 1 | 1 | 0 | 0 | 0 |
| EPIC-7 (partial) — Real push delivery (US-216, US-218) | 2 | 2 | 0 | 0 | 0 |
| **Total** | **9** | **9** | **0** | **0** | **0** |

No Phase 2 item is conditional anymore. **US-206 — Tiered notification order** was the last one, resting on AS-001 (whether "trained volunteers" means the same as the "certified" tier). Resolved [CHG-010]: it means certified/verified CPR-BLS **and** healthcare professional combined.

**Backlog readiness (Phase 3 — deferred, CHG-009)** — fully drafted and spec'd, not being built yet:

| Epic | Items | Status |
|------|------:|--------|
| EPIC-4 — Authentication & roles | 3 | Deferred to Phase 3 |
| EPIC-6 (remainder) — Certification & privacy | 5 | Deferred to Phase 3 |
| EPIC-7 (remainder) — DND bypass | 1 | Deferred to Phase 3 |
| EPIC-8 — Country portability & admin tools | 6 | Deferred to Phase 3 |
| **Total** | **15** | — |

Only two open questions remain unresolved vault-wide: OQ-002 (AED data sourcing — a fully future, out-of-scope theme) and OQ-015 (how the 5s/95% delivery target and widening delay are measured/monitored in production — flagged in US-207/US-216's specs, not blocking either story). OQ-007, 008, 009, 010, 012, 013, and 014 were all resolved 2026-07-13 via CHG-011 through CHG-017 — see [[06-change-log|change log]] and [[05-traceability-matrix|traceability matrix]] §5.

**Delivery progress** — what the team is actually building right now — is tracked directly in the backlog, not duplicated here: every story/enabler in [[03-product-backlog-v1|the product backlog]] has a **Delivery status** field (Not started / In Progress / Done) that the team updates by hand as work happens. That keeps this page from ever showing a stale count. As of this update, every Phase 1 and Phase 2 item is still "Not started."

## Documents

- [[01-requirements-structured-v1|Structured requirements]] — REQ-F, REQ-N, CON, OQ, AS extracted from the project brief and the architecture diagram.
- [[02-scope-and-context-v1|Scope & context]] — Phase 1 (walking skeleton, all 3 repos) vs. Phase 2 (the brief's real MVP) vs. later/out of scope, with dependencies, effort/risk, and open scoping questions.
- [[03-product-backlog-v1|Product backlog]] — Phase 1 (repo-tagged, includes enablers), Phase 2 (9 stories, the simple core loop), and Phase 3 (15 stories, deferred: auth/MFA, certification, country portability, admin tools).
- [[04-speckit-specs/00-index|Speckit specs]] — one dev-ready spec per Phase 1/2/3 story/enabler. See [[04-speckit-specs/blocked-stories|blocked-stories]] (currently empty — no blocked items).
- [[05-traceability-matrix|Traceability matrix]] — REQ ↔ Story ↔ Spec lookups, plus constraints and open-question impact, across all three phases.
- [[06-change-log|Change log]] — full history of every CHG-xxx.

## Recent changes

- **CHG-010 through CHG-017** (2026-07-13) — Resolved the remaining open assumption/questions ahead of vacation: AS-001 (trained = certified + healthcare professional), OQ-007 (sub-second = flat <1s), OQ-009 (90-day retention placeholder), OQ-012 (offline/force-closed = not reached), OQ-013 (no back-out after accepting), OQ-008 (battery-friendly = dev discretion, no number), OQ-010 (encryption = TLS + at-rest defaults, no key-mgmt spec), OQ-014 (expired cert = excluded not demoted; in-flight incidents never interrupted). US-206 moved from Ready (conditional) to fully Ready. Only OQ-002 (future AED theme) and OQ-015 (measurement methodology, non-blocking) remain open → [[06-change-log]]
- **CHG-009** (2026-07-13) — Rescoped Phase 2 down to the simple core notification loop (9 stories); deferred auth/MFA, certification workflow, location consent, and country portability/admin tools (15 stories) to Phase 3. Nothing deleted — all IDs, content, and specs kept intact → [[06-change-log]]
- **Phase 2 backlog + specs** (2026-07-13) — 24 stories across EPIC-4..8 originally drafted from 02-scope-and-context-v1.md §4, in the new flat/no-repo-tag/no-enabler format (see CLAUDE.md), before being rescoped by CHG-009 above. One dev-ready spec per story in [[04-speckit-specs/00-index|speckit specs]]. This initial draft was a full pipeline run (Step 3 + Step 4), not itself a CHG.
- **CHG-003 through CHG-008** (2026-07-13) — Resolved six open questions ahead of Phase 2 backlog work: OQ-001 (tier breakdown — healthcare professional is its own tier), OQ-006 (navigation provider — dev's choice), OQ-011 (roles simplified to dispatcher + admin), OQ-003 (geospatial DB — dev's choice), OQ-004 (push reliability approach — dev's choice, focus on normal devices), OQ-005 (country-abstraction approach — dev's choice). US-101 and US-104 moved from Ready (conditional) to fully Ready, no rework needed → [[06-change-log]]
- **CHG-002** (2026-07-09) — Added coordinate-range validation (lat ∈ [-90, 90], lng ∈ [-180, 180]) to US-001 and US-004 ACs and specs → [[06-change-log]]

Full change history: [[06-change-log]]

## Phase 1 blockers

None. Every Phase 1 story/enabler is Ready — see [[04-speckit-specs/blocked-stories|blocked-stories]]. The last two conditional items are now fully resolved:

| Item | Repo | Was conditional on | Status |
|------|------|---------------------|--------|
| US-101 — Sign up with tier | volunteer-app | OQ-001 — final volunteer tier breakdown | Resolved — CHG-003 (2026-07-13), no rework needed |
| US-104 — Navigate to the scene | volunteer-app | OQ-006 — navigation provider conflict | Resolved — CHG-004 (2026-07-13), no rework needed |

The open questions that used to block Phase 2 theming are also resolved: OQ-001, OQ-003, OQ-004, OQ-005, and OQ-011 (tiering, geospatial search, push reliability, country abstraction, role permissions) were all closed via CHG-003 through CHG-008 (2026-07-13) — most delegated to the development team's technical discretion per Mohamed's direction, keeping the vault's own requirements purely functional. AS-001 and OQ-007/008/009/010/012/013/014 were resolved the same day via CHG-010 through CHG-017. Only OQ-002 (future AED theme, out of scope) and OQ-015 (non-blocking measurement methodology) remain open. See [[05-traceability-matrix|traceability matrix]] §5 and [[06-change-log|change log]].

## Other

- [[00-pipeline-skills/00-skills-index|Pipeline skills index]]
- [[05-traceability-matrix]]
