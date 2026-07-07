# Scope & Context — Community CPR Volunteer Dispatch

**Based on:** Structured Requirements — Community CPR Volunteer Dispatch (condensed)
**Date:** 2026-06-17
**Produced by:** scope-and-context skill
**Status:** Draft — proposed scope for review

## 1. Context

- **Problem / why:** Out-of-hospital cardiac arrest survival drops ~7–10% per minute without CPR; ambulances take 7–10 minutes. Bystander CPR in the first 3–4 minutes more than doubles survival.
- **Goal:** A dispatcher can locate a patient and alert nearby trained volunteers within seconds; a volunteer accepts with one tap and navigates to the scene. Designed to be portable across countries from day one.
- **Stakeholders:** Emergency operators/dispatchers, volunteers (certified, healthcare professionals, willing-but-untrained), EMS partners, and per-country regulators. Tension point: who is alerted, in what order, at what distance must be configurable per country.
- **As-is:** Comparable systems exist abroad (HartslagNu, GoodSAM, PulsePoint); this is built portable rather than tied to one jurisdiction.

## 2. Scope overview (at a glance)

| Phase | Theme | Requirement IDs | Short rationale |
|-------|-------|-----------------|-----------------|
| Phase 1 | Core dispatch loop | REQ-F-001..008, REQ-N-001/002/003/005/007 | Smallest slice that delivers value end to end. |
| Phase 1 (conditional) | Tiered alerting | REQ-F-009 | Wanted now, but blocked by open questions — see §10. |
| Phase 2 | Volunteer self-service | REQ-F-010, REQ-F-011, REQ-F-012 | Valuable, not on the critical dispatch path. |
| Phase 2 | After-care | REQ-F-013 | Could-priority. |
| Cross-cutting | Multi-country foundation | REQ-N-004, REQ-N-006 | Architectural; built into Phase 1, see §9. |
| Out of scope | AED-fetch, AED registry, analytics, iOS | — | Carried from requirements. |

## 3. In scope — Phase 1 (first release)

The smallest coherent slice that delivers value: a dispatcher can locate a patient, find and alert nearby volunteers, and a volunteer can accept and navigate.

- **REQ-F-001** — operator pins the patient on a map — Must, entry point of the loop.
- **REQ-F-002** — find nearby volunteers — Must, the heart of the matching.
- **REQ-F-003** — send the alert — Must.
- **REQ-F-004** — volunteer accepts with one tap — Must (decline open, see §10).
- **REQ-F-005** — navigation to the scene — Must, leans on Google Maps.
- **REQ-F-006 / 007 / 008** — dispatcher login, live status, stand-down — Must, the console side of the loop.
- **REQ-N-001 / 002 / 003** — speed, uptime, graceful degradation — Must, these are the dispatch path's qualities, not optional add-ons.
- **REQ-N-005 / 007** — security baseline and consent-based location — Must, required for the loop to be lawful and safe from day one.

## 4. Later phases

- **Phase 2 — REQ-F-010:** certification expiry tracking and re-verify reminders — Should; needed soon but not to prove the core loop.
- **Phase 2 — REQ-F-011:** availability scheduling — Should.
- **Phase 2 — REQ-F-012:** in-app CPR reference — Should; valuable during an event but the volunteer can still act without it, so deferred to keep Phase 1 minimal. *(Analyst proposal — could be pulled into Phase 1 if the team prefers.)*
- **Phase 2 — REQ-F-013:** post-event check-in and wellbeing follow-up — Could.

## 5. Out of scope

- AED-fetch flow — later phase; **architecture should leave room** (carried from requirements).
- AED registry / source of AED locations — open, not in this build.
- Reporting/analytics dashboards for EMS partners — later.
- iOS volunteer app — later/undecided (CON-001 fixes Android-only for now).

## 6. Dependencies & build order

| Item | Depends on | Reason | Effect on order |
|------|-----------|--------|-----------------|
| REQ-F-002 (find volunteers) | A volunteer registry + sign-up (location, availability, tier) | You cannot find/alert volunteers who aren't registered | **Prerequisite for all of Phase 1 — and not explicitly in the requirements; see §10** |
| REQ-F-003 (alert) | REQ-F-002 | Must know who is nearby before alerting | Build matching before alerting |
| REQ-N-001 (5s push) | Push infrastructure (e.g. FCM); REQ-F-003 | Reliable wake-up is the hard part | Spike push reliability early |
| REQ-F-005 (navigation) | Google Maps integration (CON-002) | External dependency | Low risk, can parallelise |
| REQ-F-009 (tiered alerting) | OQ-01 (tiers), OQ-02 (delay) | Can't order tiers that aren't defined | Blocked until answered |
| All Phase 1 | REQ-N-005 (security), REQ-N-006 (country abstraction) | Cross-cutting foundations | Decide and lay down first |

## 7. Effort, risk & priority (analyst assessment — for review)

*Relative t-shirt sizing, not time estimates. To validate with the delivery team.*

| Requirement | Priority | Effort (S/M/L) | Risk | Risk reason |
|-------------|----------|----------------|------|-------------|
| REQ-F-001 | Must | M | Low | Standard map pinning |
| REQ-F-002 | Must | L | High | Sub-second geospatial matching at city scale is unsolved in the brief |
| REQ-F-003 | Must | M | Medium | Depends on push delivery |
| REQ-F-005 | Must | S | Low | Leaning on Google Maps |
| REQ-F-006/007/008 | Must | M | Low | Conventional console features |
| REQ-F-009 | Must | M | Medium | Logic is moderate but blocked by open questions |
| REQ-N-001 | Must | L | High | Guaranteed 5s wake-up through DND/silent is genuinely hard |
| REQ-N-004/006 | Must | L | High | Multi-country abstraction is architectural and pervasive |
| REQ-N-005 | Must | M | Medium | Security baseline, well understood but non-trivial |

## 8. Constraints & early architectural decisions

- **CON-001** — Android only for now; **CON-002** — Google Maps for navigation; **CON-003** — web console for dispatchers.
- **Decide now (affects multiple requirements):**
  - Geospatial database and indexing approach — drives REQ-F-002 and REQ-N-001.
  - Push-reliability strategy (waking the phone through silent/DND) — drives REQ-N-001.
  - Country-abstraction model and per-country data isolation — drives REQ-N-004 and REQ-N-006; cheaper to build in now than to retrofit.

## 9. Open scoping questions

- **The volunteer registry and sign-up flow is a prerequisite for all of Phase 1 but is not in the structured requirements.** This is a new finding — send it back to the requirements step rather than inventing it here. Phase 1 cannot start without it.
- **Tiered alerting (REQ-F-009) is blocked by OQ-01 (tier breakdown) and OQ-02 (widen delay).** Can Phase 1 ship "alert all nearby volunteers" first, with tiered ordering following once the tiers are agreed?
- **Decline action (OQ-04)** — does Phase 1's accept flow (REQ-F-004) also need an explicit decline? Affects the console's live status too.
- **Exact alert-speed target (OQ-03)** — REQ-N-001 cannot be made testable until "5 seconds, 95%" is confirmed.
- **Which country launches first?** Not stated. Determines how much of the country-abstraction (REQ-N-004/006) must be proven in Phase 1 versus designed-for-later.
