# Change Log — Community CPR Volunteer Dispatch

**Project:** Community CPR Volunteer Dispatch
**Pipeline initial run:** 2026-07-06
**Maintained by:** change-management skill

Changes are listed newest first. Each entry is permanent — never deleted or edited after creation.

---

## CHG-017 — Resolve OQ-014 (certification-expiry consequence; mid-incident deactivation)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-014 / REQ-F-017 / REQ-F-018 / REQ-F-035 / US-211 / US-222
**Old value:** Undefined what happens when a certification expires without re-verification, and undefined what happens to an in-flight incident if a notified/accepted volunteer's account is deactivated mid-response.
**New value:** An expired certification excludes the volunteer from new alerts until re-verified — no automatic demotion to a lower tier. An in-flight incident is never interrupted: a volunteer already notified/accepted on an incident stays active on it regardless of a certification change or account deactivation that happens mid-response.
**Reason:** Mohamed's direction: simplest safe default — don't build automatic tier-demotion logic, and never let a backend-side account change abort or reassign a live incident.
**Resolves:** OQ-014

### Items updated
- `01-requirements-structured-v1.md` — OQ-014 marked resolved (§5); REQ-F-017, REQ-F-018, REQ-F-035 Notes updated (§2)
- `03-product-backlog-v1.md` — US-211 Status/Notes updated (no longer "rests on OQ-014"); US-222 Notes updated
- `04-speckit-specs/epic6-us211-track-certification-expiry.md`, `epic6-us212-remind-reverify-certification.md`, `epic8-us222-admin-manage-volunteers.md` — Unresolved/Out-of-scope sections updated to reflect resolution
- `05-traceability-matrix.md` — REQ-F-017/018/035 rows (§1 n/a — no row edit needed there), Story→Requirements US-211 row (§4), and OQ-014 row (§5) updated

### Items reviewed — no change needed
- US-210, US-215, US-223 — reference the certification lifecycle but don't depend on the specific expiry-consequence detail.

### Follow-up actions required
- None — both affected stories (US-211, US-222) are Phase 3, not being built now; the resolution is recorded and ready when that phase is picked up.

---

## CHG-016 — Resolve OQ-010 (scope of "encryption everywhere")
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-010 / REQ-N-006
**Old value:** "The system shall encrypt data everywhere" — scope undefined (in transit only, at rest, specific fields, key management approach all unspecified).
**New value:** Minimum HTTPS/TLS in transit for everything, plus at-rest encryption for sensitive fields (location, personal data) using whatever the chosen datastore offers by default. No specific key-management scheme mandated — left to the development team's discretion.
**Reason:** Mohamed's direction: keep this loose, not strict — functional requirement is "encrypted," not a prescribed mechanism.
**Resolves:** OQ-010

### Items updated
- `01-requirements-structured-v1.md` — OQ-010 marked resolved (§5); REQ-N-006 Notes updated (§3)
- `03-product-backlog-v1.md` — US-201 Notes updated
- `04-speckit-specs/epic4-us201-login-with-role-based-access.md` — Unresolved section updated
- `05-traceability-matrix.md` — REQ-N-006 row (§2) and OQ-010 row (§5) updated

### Items reviewed — no change needed
- REQ-N-007, REQ-N-008 (least-privilege, audit logging) — separate security NFRs, unaffected by this specific resolution.

### Follow-up actions required
- None — US-201 is Phase 3, not being built now; the resolution is recorded and ready when that phase is picked up.

---

## CHG-015 — Resolve OQ-008 (definition of "battery-friendly")
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-008 / REQ-N-018
**Old value:** "Background location tracking shall be battery-friendly" — no measurable definition (sampling interval, battery-drain budget) given.
**New value:** No concrete number specified — "reasonable battery use, no aggressive constant GPS polling." Left entirely to the development team's engineering discretion.
**Reason:** Mohamed's direction: agreed with the proposed simple, unspecified default rather than inventing a number.
**Resolves:** OQ-008

### Items updated
- `01-requirements-structured-v1.md` — OQ-008 marked resolved (§5); REQ-N-018 Notes updated (§3)
- `03-product-backlog-v1.md` — US-214 Notes updated
- `04-speckit-specs/epic6-us214-consent-background-location.md` — Unresolved section updated
- `05-traceability-matrix.md` — REQ-N-018 row (§2) and OQ-008 row (§5) updated

### Items reviewed — no change needed
- US-204 — uses registered/last-known location, not continuous background tracking, so this resolution doesn't touch it.

### Follow-up actions required
- None — US-214 is Phase 3, not being built now; the resolution is recorded and ready when that phase is picked up.

---

## CHG-014 — Resolve OQ-013 (can a volunteer back out after accepting?)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-013 / REQ-F-024 / REQ-F-010 / US-103 / US-208
**Old value:** Undefined whether a volunteer can back out after already accepting an alert, and if so how that's handled downstream (dispatcher notified, pool widens again).
**New value:** No — a volunteer cannot back out after accepting in this round. Once accepted, accepted; no back-out flow, no downstream handling to build.
**Reason:** Mohamed's direction: keep it simple for this round.
**Resolves:** OQ-013

### Items updated
- `01-requirements-structured-v1.md` — OQ-013 marked resolved (§5); REQ-F-024 Notes updated (§2)
- `03-product-backlog-v1.md` — US-208 Notes updated; "Items sent back — Phase 2" bullet updated
- `04-speckit-specs/epic2-us103-accept-decline-alert.md` (Phase 1) and `epic5-us208-live-per-volunteer-status.md` (Phase 2) — Unresolved sections updated to reflect resolution
- `05-traceability-matrix.md` — Story→Requirements US-208 row (no edit needed — already correct) and OQ-013 row (§5) updated

### Items reviewed — no change needed
- US-104, US-105, US-106 (Phase 1 volunteer-app) — no dependency on back-out behaviour.

### Follow-up actions required
- None. Both stories (US-103, already built in Phase 1; US-208, Phase 2 active) can proceed as originally scoped, now confirmed rather than assumed.

---

## CHG-013 — Resolve OQ-012 (offline/force-closed device handling for alerts)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-012 / REQ-F-021 / REQ-N-001 / US-216
**Old value:** Undefined what should happen if a volunteer's device is offline, has no signal, or the app has been force-closed by the OS when an alert is sent.
**New value:** Counts simply as "not reached" — no retry or queueing logic. The alert-widening flow (US-207) proceeds exactly as if the volunteer had ignored the alert.
**Reason:** Mohamed's direction: agreed with the proposed simplest default rather than building retry/queueing behaviour.
**Resolves:** OQ-012

### Items updated
- `01-requirements-structured-v1.md` — OQ-012 marked resolved (§5); REQ-F-021 Notes updated (§2)
- `03-product-backlog-v1.md` — US-216 Notes updated
- `04-speckit-specs/epic7-us216-receive-real-push-alert.md` — Unresolved section updated
- `05-traceability-matrix.md` — OQ-012 row (§5) updated

### Items reviewed — no change needed
- US-218 (delivery status tracking) — "not reached" is already one of its two tracked states (REQ-F-034); nothing to change there.

### Follow-up actions required
- None. US-216 is Phase 2 active — ready to build as originally scoped, now confirmed.

---

## CHG-012 — Resolve OQ-009 (patient location retention period)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-009 / REQ-N-010 / US-209
**Old value:** "Patient location data shall not be retained longer than necessary" — no precise retention period defined.
**New value:** 90 days, set as a placeholder value — easy to change later, not a legally-researched figure. Context checked: GDPR Art. 5(1)(e) itself sets no fixed number, only a "storage limitation" principle (no longer than necessary for the purpose); a real jurisdiction-specific figure would need legal review, deferred since this is a test project.
**Reason:** Mohamed's direction: use 90 days now so the team has a concrete number to build against; revisit later since it's a test project, not a production legal commitment.
**Resolves:** OQ-009

### Items updated
- `01-requirements-structured-v1.md` — OQ-009 marked resolved (§5); REQ-N-010 Notes updated (§3)
- `03-product-backlog-v1.md` — US-209 Notes updated
- `04-speckit-specs/epic5-us209-full-dispatch-audit-trail.md` — Unresolved section updated
- `05-traceability-matrix.md` — REQ-N-010 row (§2) and OQ-009 row (§5) updated

### Items reviewed — no change needed
- None — this OQ only ever touched US-209.

### Follow-up actions required
- Before any real (non-test) deployment, get actual legal review of the retention period per deployment jurisdiction — 90 days is a working placeholder, not a compliance-reviewed figure.

---

## CHG-011 — Resolve OQ-007 (precise definition of "sub-second")
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** OQ-007 / REQ-N-017 / US-204
**Old value:** "Sub-second" search performance — no precise definition (concurrency, region size, volunteer-count assumptions) given.
**New value:** Kept simple — a flat "under 1 second," regardless of scale/concurrency/region. No benchmark methodology or load-testing assumptions specified.
**Reason:** Mohamed's direction: keep it simple.
**Resolves:** OQ-007

### Items updated
- `01-requirements-structured-v1.md` — OQ-007 marked resolved (§5); REQ-N-017 Notes updated (§3)
- `03-product-backlog-v1.md` — US-204 Notes updated; NFR table row updated
- `04-speckit-specs/epic5-us204-nearby-volunteers-radius-bands.md` — Unresolved section updated
- `05-traceability-matrix.md` — REQ-N-017 row (§2) and OQ-007 row (§5) updated

### Items reviewed — no change needed
- None — this OQ only ever touched US-204.

### Follow-up actions required
- None. US-204 is Phase 2 active — ready to build as originally scoped, now confirmed.

---

## CHG-010 — Resolve AS-001 (does "trained volunteers" include healthcare professionals?)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation OQ clean-up round)
**Change type:** OQ resolved
**Affected item:** AS-001 / REQ-F-008 / REQ-F-032 / US-206
**Old value:** AS-001 assumed "trained volunteers" (the brief's core-flow phrase) meant the same thing as the "certified" tier alone, not a separate/broader category. This was flagged as an unconfirmed standing assumption, not resolved by CHG-003, and was the sole reason US-206 was "Ready (conditional)" rather than fully Ready.
**New value:** The assumption was too narrow. "Trained volunteers" (the first alert wave) means certified/verified CPR-BLS **and** healthcare professional combined, notified together in the same first wave. Willing-but-untrained remains reachable only via widening (US-207).
**Reason:** Mohamed's explicit answer: "getrainde zijn certified plus healthcare samen."
**Resolves:** — (treated as an OQ-style resolution per the change-management skill's step 5, since it unblocks a "Ready (conditional)" story exactly like an OQ would)

### Items updated
- `01-requirements-structured-v1.md` — AS-001 marked resolved (§6); REQ-F-008, REQ-F-032 Notes updated (§2)
- `03-product-backlog-v1.md` — US-206 Story/AC/Grounding/Status updated (conditional → Ready)
- `04-speckit-specs/epic5-us206-tiered-notification-order.md` — Scenario 1, Constraints, and Unresolved sections updated to reflect the confirmed two-tier first wave
- `04-speckit-specs/00-index.md` — US-206 listing updated (no longer "conditional")
- `05-traceability-matrix.md` — REQ-F-008, REQ-F-032 rows (§1) and Story→Requirements US-206 row (§4) updated

### Items reviewed — no change needed
- US-205, US-207 (send alert, widen pool) — operate on whatever tier sequence US-206 defines; no direct edit needed, they already reference US-206 generically.

### Follow-up actions required
- `00-project-home.md` Phase 2 readiness table: recompute — US-206 moves from "Ready (conditional)" to "Ready," so Phase 2 is now 9/9 fully Ready, 0 conditional.

---

## CHG-009 — Rescope Phase 2 to the simple core loop; defer auth/MFA, certification workflow, location consent, and country portability/admin tools to Phase 3
**Date:** 2026-07-13
**Triggered by:** Mohamed, same session as CHG-003..008 — after reviewing the first Phase 2 draft (24 stories), decided it was bigger than intended
**Change type:** Scope change
**Affected item:** 03-product-backlog-v1.md (EPIC-4 through EPIC-8); 02-scope-and-context-v1.md §4; 04-speckit-specs/ (15 spec files marked deferred); 05-traceability-matrix.md; 00-project-home.md
**Old value:** All 24 Phase 2 stories (US-201..US-224) marked Status: Ready (or Ready-conditional) with Phase/Sprint: Phase 2.
**New value:** 9 stories stay in Phase 2 (US-204, 205, 206, 207, 208, 209, 213, 216, 218 — the core loop: find nearby volunteers, send a tiered alert, widen if unanswered, live status, audit trail, availability, real push, delivery tracking). 15 stories reassigned to Phase 3, Status changed to "Deferred to Phase 3 [CHG-009]": US-201, 202, 203 (login/MFA/admin oversight), US-210, 211, 212, 214, 215 (certification workflow, location consent, volunteer history), US-217 (DND bypass), US-219, 220, 221, 222, 223, 224 (country portability + admin tools). No story was deleted; all IDs, content, and spec files are kept intact per CLAUDE.md's "IDs are permanent" rule — only the Status/Phase field and a small number of acceptance criteria referencing now-deferred capabilities were edited (see Items updated).
**Reason:** Mohamed's brief was "keep Phase 2 simple, like the volunteer sets availability and it's respected" — not a full real-auth, real-i18n, real-cert-lifecycle system. The first draft over-applied "grounded in a requirement = must build now": MFA and country configurability are genuinely required by the brief eventually (REQ-N-005, REQ-N-012..016), but being in the brief doesn't mean they have to ship in this round, the same way iOS and e2e-tests were deferred without being cut from the requirements in Phase 1. Deferring is a phasing decision, not a requirements change — nothing in 01-requirements-structured-v1.md was touched.
**Resolves:** —

### Items updated
- `03-product-backlog-v1.md` — Epics table: EPIC-4 and EPIC-8 marked Phase 3 in full; EPIC-6 and EPIC-7 split (partial Phase 2 / partial Phase 3). 15 stories' Status/Phase/Sprint fields changed to "Deferred to Phase 3 [CHG-009]" with a reason noted per story. 3 stories' acceptance criteria simplified to remove per-country-configurability language now that country portability is deferred (US-204, US-206, US-207 — read from one simple system-wide configuration instead). US-209 and US-218's story personas softened from "dispatcher or admin" to "dispatcher" since admin oversight (US-203) is deferred. New "Phase 3 (deferred, CHG-009)" section added with its own suggested build order for later. "Non-functional requirements — Phase 2" table trimmed to only what still applies; deferred NFRs noted as moved with their stories. "Suggested build order — Phase 2" and "Dependencies overview — Phase 2" trimmed to the 9 active stories.
- `02-scope-and-context-v1.md` §4 — added a note pointing to this CHG and the new Phase 2/Phase 3 split; the theme description itself was left as originally scoped (this is a build-order decision, not a scope cut).
- `04-speckit-specs/` — 15 spec files (epic4-us201/202/203, epic6-us210/211/212/214/215, epic7-us217, epic8-us219/220/221/222/223/224) each got a one-line "Status: Deferred to Phase 3 [CHG-009]" banner added under their header — content otherwise untouched. 3 active specs (epic5-us204/206/207) had their per-country-configuration language simplified to match the trimmed backlog ACs. epic5-us209 got a note that its admin consumer is deferred.
- `04-speckit-specs/00-index.md` — reorganized into "Phase 2 (current round)" and "Phase 3 (deferred, CHG-009)" sections.
- `05-traceability-matrix.md` — Phase columns updated for all affected REQ-F/REQ-N rows and the Story→Requirements reverse lookup to show which stories are Phase 2 (active) vs Phase 3 (deferred).
- `00-project-home.md` — Phase 2 backlog-readiness table updated to reflect 9 active stories; added a Phase 3 (deferred) note.

### Items reviewed — no change needed
- `01-requirements-structured-v1.md` — no requirement was added, changed, or removed. This is a phasing/prioritization decision, not a requirements change; REQ-F-001, REQ-N-005, REQ-N-012..016, and all other requirements behind deferred stories remain valid and unchanged, just scheduled for Phase 3.
- Phase 1 backlog (US-001..US-106, ENABLER-001..003) — entirely unaffected, this CHG only touches Phase 2.
- `06-change-log.md` CHG-003 through CHG-008 — the six OQ resolutions stand as written; none of them are reversed or contradicted by this rescoping. OQ-003/004/005 (delegated to dev team) still apply to the Phase 3 stories they were tied to (US-219-221, US-217); OQ-001/006/011 still apply to the Phase 2 stories they unblocked (US-206, US-201 respectively — US-201 itself is now deferred, but the resolution stands).

### Follow-up actions required
- None to build Phase 2 now — the 9 active stories and their specs are ready as-is.
- When Phase 3 is eventually picked up, split US-220 (configure country settings) before sprinting on it — it was already flagged in the original draft as bundling 4 requirements into one oversized story.

**Addendum (2026-07-13, full vault health check):** A full cross-file audit found this rescoping had been applied inconsistently in a few spots and corrected them — no new decision, just finishing CHG-009's own rollout: `05-traceability-matrix.md` §5 (Open Questions table) still tagged US-214/OQ-008, US-201/OQ-010, and US-211+US-222/OQ-014 as "(Phase 2)" — corrected to Phase 3; `02-scope-and-context-v1.md` §2 and §7 still presented the whole Fase-2 theme and its login/MFA, certification, and country-portability/admin rows as undifferentiated current Phase 2 scope with no pointer to the split — added CHG-009 annotations; `04-speckit-specs/epic5-us206-tiered-notification-order.md` and `epic5-us207-widen-alert-pool.md` still instructed devs in their Constitution snippet to read tier order/widening rules from "per-country configuration," contradicting their own (correctly trimmed) Constraints sections — corrected to the system-wide-for-now wording used elsewhere. No IDs, requirements, or story scope changed — bookkeeping only.

---

## CHG-008 — Resolve OQ-005 (country-abstraction technical approach)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation Phase 2 prep)
**Change type:** OQ resolved
**Affected item:** OQ-005
**Old value:** How will country-specific differences (emergency number, regulations, language, integration partners, alert rules) be modelled technically without forking the codebase? — explicitly undecided in the brief.
**New value:** Out of scope for requirements — the technical modelling approach is delegated to the development team's discretion. REQ-N-012 through REQ-N-016 and REQ-F-032 continue to state *what* must be configurable per country; *how* that's implemented is not a BA-level decision.
**Reason:** Mohamed's direction: the BA/vault layer's job is to hand devs functional requirements, not to make technical architecture decisions on their behalf. Devs choose the implementation as long as the functional requirement (configurability per country) is met.
**Resolves:** OQ-005

### Items updated
- `01-requirements-structured-v1.md` — OQ-005 marked resolved (§5); REQ-N-016 Notes updated (§3)
- `05-traceability-matrix.md` — REQ-N-004, REQ-N-012..016 rows (§2) and OQ-005 row (§5) updated
- `02-scope-and-context-v1.md` — risk row for REQ-F-036/REQ-N-004/REQ-N-012..016 (§7), CON-007-adjacent "te beslissen nu" bullet (§8), and open scopingvraag (§9) updated

### Items reviewed — no change needed
- `01-requirements-structured-v1.md` CON-003 (module scaffold) — the six module boundaries, including Countries/Config, are unaffected; only the internal implementation approach was ever undecided, and that was never specified in CON-003 itself.
- `03-product-backlog-v1.md` / `04-speckit-specs/` — no Phase 1 story implements REQ-N-012..016 or REQ-F-032; nothing to edit there yet.

### Follow-up actions required
- REQ-N-012..016 and REQ-F-032 (Phase 2 portability/tiering) can now be drafted into backlog stories; note in any resulting story that the technical abstraction mechanism is a dev decision, not a specified requirement.

---

## CHG-007 — Resolve OQ-004 (push delivery reliability approach)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation Phase 2 prep)
**Change type:** OQ resolved
**Affected item:** OQ-004
**Old value:** What is the technical approach to maximise push delivery reliability (waking a backgrounded or silent Android device)? — explicitly undecided in the brief.
**New value:** Out of scope for requirements — delegated to the development team. Requirements focus on normal-condition device operation; REQ-F-022's do-not-disturb-bypass behaviour remains a best-effort "Should" with no specific mechanism mandated. REQ-F-021 (receive push) and REQ-N-001 (5s/95% delivery) remain the Must-priority baseline, unaffected.
**Reason:** Mohamed's direction: focus purely on functional requirements and normal-device behaviour; the technical mechanism for edge-case reliability is a dev decision, not something the BA layer specifies.
**Resolves:** OQ-004

### Items updated
- `01-requirements-structured-v1.md` — OQ-004 marked resolved (§5); REQ-F-022 Notes updated (§2)
- `05-traceability-matrix.md` — REQ-F-022, REQ-F-033 rows (§1), REQ-N-001 row (§2), and OQ-004 row (§5) updated
- `02-scope-and-context-v1.md` — risk row for REQ-F-021/022/033/034 (§7) and open scopingvraag (§9) updated

### Items reviewed — no change needed
- `01-requirements-structured-v1.md` REQ-F-021 (Phase 1, partial in-app display only) — unaffected; Phase 1 has no real push mechanics to begin with.
- No requirement text was removed or weakened — REQ-F-022 stays a "Should," not dropped, per "never invent scope" (a removal would need its own change record if that's ever wanted).

### Follow-up actions required
- REQ-F-021 (full)/REQ-F-022/REQ-F-033 (Phase 2 real push) can now be drafted into backlog stories, framed as: normal-condition delivery is the Must baseline, DND-bypass is best-effort with the mechanism left to the dev team.

---

## CHG-006 — Resolve OQ-003 (geospatial database/indexing approach)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation Phase 2 prep)
**Change type:** OQ resolved
**Affected item:** OQ-003
**Old value:** What geospatial database and indexing approach will be used to keep nearby-volunteer search fast at country scale? — explicitly undecided in the brief.
**New value:** Out of scope for requirements — technical implementation choice, delegated to the development team's discretion. REQ-F-031 and REQ-N-017 stand as written (the functional/performance outcome); no specific database/indexing technology is mandated.
**Reason:** Mohamed's direction: this is purely a technical implementation decision, not something the BA/vault layer needs to specify — devs choose as long as the functional/performance requirement is met.
**Resolves:** OQ-003

### Items updated
- `01-requirements-structured-v1.md` — OQ-003 marked resolved (§5); CON-007 Notes updated (§4)
- `05-traceability-matrix.md` — REQ-F-031 row (§1), CON-007 row (§3), and OQ-003 row (§5) updated
- `02-scope-and-context-v1.md` — risk row for REQ-F-006/031/REQ-N-017 (§7), CON-007 bullet (§8), and open scopingvraag (§9) updated

### Items reviewed — no change needed
- No Phase 1 story or spec references a specific geospatial database choice — ENABLER-002's Phase 1 CRUD endpoint doesn't implement geospatial search yet, so nothing there needs a change.

### Follow-up actions required
- REQ-F-031 (Phase 2 backend nearby-volunteer search) can now be drafted into a backlog story; note that DB/indexing technology is a dev decision, not specified.

---

## CHG-005 — Resolve OQ-011 (role permission boundaries) — simplify to two roles
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation Phase 2 prep)
**Change type:** OQ resolved
**Affected item:** OQ-011 / REQ-F-001
**Old value:** REQ-F-001: "The dispatcher console shall support login with role-based access for three roles: dispatcher, supervisor, admin." Exact permission boundaries per role not stated.
**New value:** REQ-F-001: "The dispatcher console shall support login with role-based access for two roles: dispatcher (can create/manage/dispatch incidents) and admin (oversight of all dispatchers and incidents across the system)." Supervisor role removed; admin covers the cross-incident oversight need.
**Reason:** Mohamed's decision: pick the most logical simple split — a dispatcher who can dispatch, and an admin who has oversight of all dispatchers. No separate supervisor tier needed.
**Resolves:** OQ-011

### Items updated
- `01-requirements-structured-v1.md` — REQ-F-001 requirement text changed from three roles to two (§2); OQ-011 marked resolved (§5)
- `05-traceability-matrix.md` — REQ-F-001 row (§1), REQ-N-005 row (§2), and OQ-011 row (§5) updated
- `02-scope-and-context-v1.md` — risk row for REQ-F-001/REQ-N-005 (§7) updated

### Items reviewed — no change needed
- `03-product-backlog-v1.md` / `04-speckit-specs/` — no Phase 1 story exists for REQ-F-001 (login/roles is deferred to Phase 2 by the walking-skeleton decision), so there is no existing story or spec to update.

### Follow-up actions required
- REQ-F-001 (Phase 2 login/roles) can now be drafted into a backlog story using the confirmed two-role model (dispatcher, admin).

---

## CHG-004 — Resolve OQ-006 (navigation provider conflict)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation Phase 2 prep)
**Change type:** OQ resolved
**Affected item:** OQ-006 / REQ-F-026 / US-104
**Old value:** The brief's text says "fine to lean on Google Maps"; the architecture diagram shows the volunteer-app's navigation edge going to OpenStreetMap/MapLibre/OSRM instead — conflicting, undecided. US-104 and its spec were built under a stated Google Maps assumption, flagged as needing rework if the diagram's choice was confirmed instead.
**New value:** Navigation provider is a development-team implementation choice, not specified by requirements. REQ-F-026 only requires that turn-by-turn navigation is provided to the volunteer after accepting; which provider/SDK is used is the dev team's call, as long as navigation works. US-104's existing Google Maps implementation stands — no rework needed.
**Reason:** Mohamed's direction: focus on the functional need (volunteer has navigation); which navigation tech stack is used is entirely the developer's choice.
**Resolves:** OQ-006

### Items updated
- `01-requirements-structured-v1.md` — OQ-006 marked resolved (§5); REQ-F-026 Notes updated (§2)
- `03-product-backlog-v1.md` — US-104 AC rule and Status updated (conditional → Ready, no rework needed)
- `04-speckit-specs/epic2-us104-navigate-to-scene.md` — Scenario 1's constraints note, "Unresolved" section, and Constitution snippet updated to reflect resolution
- `04-speckit-specs/blocked-stories.md` — US-104 entry updated
- `05-traceability-matrix.md` — REQ-F-026 row (§1) and OQ-006 row (§5) updated
- `02-scope-and-context-v1.md` — §2 table, §3 bullet, §7 risk row, and §9 open scopingvraag updated

### Items reviewed — no change needed
- US-101, US-102, US-103, US-105, US-106 (volunteer-app) — no dependency on navigation provider choice.

### Follow-up actions required
- None. US-104 is fully Ready as already built; no spec rework required.

---

## CHG-003 — Resolve OQ-001 (final volunteer tier breakdown)
**Date:** 2026-07-13
**Triggered by:** Mohamed, session 2026-07-13 (pre-vacation Phase 2 prep)
**Change type:** OQ resolved
**Affected item:** OQ-001 / REQ-F-008 / REQ-F-015 / REQ-F-032 / US-101
**Old value:** The brief named three provisional tier categories (certified/verified CPR-BLS, healthcare professional, willing-but-untrained) but said the breakdown was "TBD" and that healthcare professional "might be its own tier, might be a flavour of certified." US-101 and its spec were built under this provisional list, flagged as needing rework if the final breakdown differed structurally.
**New value:** Healthcare professional is confirmed as its own separate tier. Final breakdown: (1) certified/verified CPR-BLS, (2) healthcare professional, (3) willing-but-untrained — structurally identical to the provisional list already built, so no rework is needed.
**Reason:** Mohamed's decision: healthcare professional may be a separate tier.
**Resolves:** OQ-001

### Items updated
- `01-requirements-structured-v1.md` — OQ-001 marked resolved (§5); REQ-F-008 and REQ-F-015 Notes updated (§2); AS-001 annotated to note OQ-001's resolution didn't address that specific wording assumption (§6)
- `03-product-backlog-v1.md` — US-101 AC rule and Status updated (conditional → Ready, no rework needed)
- `04-speckit-specs/epic2-us101-sign-up-with-tier.md` — Scenario 4, constraints/assumptions bullet, "Unresolved" section, and Constitution snippet updated to reflect resolution
- `04-speckit-specs/blocked-stories.md` — US-101 entry updated
- `05-traceability-matrix.md` — REQ-F-008, REQ-F-015, REQ-F-032 rows (§1) and OQ-001 row (§5) updated
- `02-scope-and-context-v1.md` — §2 table, §3 bullet, §7 risk row, and §9 open scopingvraag updated

### Items reviewed — no change needed
- `01-requirements-structured-v1.md` REQ-F-032 (§2) — Notes column was already blank; no textual note existed to update. Its Phase-2 blocked-status is tracked in the traceability matrix and scope doc instead.
- US-102, US-103, US-105, US-106, ENABLER-001..003 — no dependency on tier breakdown.

### Follow-up actions required
- REQ-F-008 (tiered order) and REQ-F-032 (backend tiered alert logic) can now be drafted into Phase 2 backlog stories using the confirmed three-tier structure.

---

## CHG-002 — Add coordinate-range validation to US-001 (create) and US-004 (update)
**Date:** 2026-07-09
**Triggered by:** GitHub Issue #25 opened by @pepe-feliu; follow-up comments by @SaadiMoh requesting extension to US-004 and consolidation into a single proposal scoped to the dispatcher-web form layer
**Change type:** Requirement modified
**Affected item:** US-001 (03-product-backlog-v1.md); 04-speckit-specs/epic1-us001-create-incident.md; US-004 (03-product-backlog-v1.md); 04-speckit-specs/epic1-us004-update-incident.md
**Old value:** Neither US-001 nor US-004 constrained the numeric range of latitude/longitude. US-001's Scenario 2 (typed coordinates) required only that the incident is created with those coordinates — no bounds check. US-004's Scenario 4 covered clearing the location entirely (not submitting an out-of-range value); the US-004 Constitution snippet stated the location rule is shared with US-001 but said nothing about coordinate range.
**New value:** One new negative scenario added to each of the four artefacts. US-001 (backlog AC + spec Scenario 7): "Given the incident form is open, when the dispatcher submits with a latitude outside [-90, 90] or a longitude outside [-180, 180], then the incident is not created and a validation message states the coordinates are out of range." US-004 (backlog AC + spec Scenario 5): "Given an existing incident, when the dispatcher edits its location to a latitude outside [-90, 90] or a longitude outside [-180, 180] and saves, then the save is rejected and a validation message states the coordinates are out of range — same range rule as US-001." Constitution snippets in both spec files updated to make explicit that the shared location rule covers both presence (not null/empty) and valid range (latitude ∈ [-90, 90], longitude ∈ [-180, 180]).
**Reason:** The dispatcher-web incident form accepted and stored geographically impossible coordinates (e.g. lat 999, lng -200) with no rejection on either the create or edit path, making affected incidents silently unusable (cannot be plotted on the map or routed to by volunteers). The "location is required" rule is already explicitly shared between US-001 and US-004 via the spec's Constitution snippet; coordinate-range validation is a direct extension of that same shared rule. Gap identified via a @known-gap-tagged test scenario and confirmed by direct POST /api/incidents calls always returning 201.
**Resolves:** —

### Items updated
- `03-product-backlog-v1.md` — US-001 AC list: added out-of-range coordinates negative AC (tagged [CHG-002])
- `03-product-backlog-v1.md` — US-004 AC list: added out-of-range coordinates negative AC on edit (tagged [CHG-002])
- `04-speckit-specs/epic1-us001-create-incident.md` — Added Scenario 7 (out-of-range coordinates rejected); updated Constitution snippet to state the shared rule covers both presence and valid range (tagged [CHG-002])
- `04-speckit-specs/epic1-us004-update-incident.md` — Added Scenario 5 (out-of-range coordinates rejected on edit); updated Constitution snippet to state the shared rule covers both presence and valid range (tagged [CHG-002])
- `05-traceability-matrix.md` — US-001 and US-004 rows in Section 4 annotated to record the AC/spec extension (tagged [CHG-002])
- `00-project-home.md` — Recent changes line added

### Items reviewed — no change needed
- `01-requirements-structured-v1.md` — REQ-F-002, REQ-F-003, REQ-F-004 (US-001's parent requirements) and REQ-F-005 (US-004's parent requirement) remain valid as-is. Coordinate-range validation is an AC-level gap-fill on the stories implementing those requirements, not a new top-level requirement. No edit needed.
- `02-scope-and-context-v1.md` — Phasing and scope boundaries unaffected. The change is confined to the dispatcher-web form layer within the already-agreed Phase 1 scope.
- `03-product-backlog-v1.md` — US-002, US-003, US-005, US-006: none of these stories create or edit incident coordinates; no AC is affected.
- `03-product-backlog-v1.md` — US-101..US-106 (volunteer-app) and ENABLER-001..003 (backend-api): no dependency on dispatcher-web incident-location validation logic.
- `05-traceability-matrix.md` — REQ-F rows for REQ-F-002..005: the requirements themselves are unchanged; only the story/AC level changes. No row-level edit beyond the annotation already made.
- `00-project-home.md` — Backlog readiness table: US-001 and US-004 both remain **Ready**; no status field changed, so counts are unchanged.

### Follow-up actions required
- None. Both stories are already Ready and their spec files are updated. No new spec file is needed. Implementation team should ensure `LocationSchema` (or equivalent form-validation layer) enforces `.min()`/`.max()` on `lat` and `lng` to match the new ACs — but that is a delivery-team decision, not a BA action.

<!-- SKILL: insert new entries above this line, newest first -->
