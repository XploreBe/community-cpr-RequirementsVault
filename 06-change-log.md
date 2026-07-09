# Change Log — Community CPR Volunteer Dispatch

**Project:** Community CPR Volunteer Dispatch
**Pipeline initial run:** 2026-07-06
**Maintained by:** change-management skill

Changes are listed newest first. Each entry is permanent — never deleted or edited after creation.

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
