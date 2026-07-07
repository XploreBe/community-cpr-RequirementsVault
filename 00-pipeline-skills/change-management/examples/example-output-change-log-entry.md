# Example Output — Change Log Entry

This is the change log entry the skill produces for the example input. It shows the level of detail expected and what "items reviewed — no change needed" looks like.

---

## CHG-001 — OQ-004 resolved: tier escalation timeouts set to 30s / 60s
**Date:** 2026-07-01
**Triggered by:** Stakeholder call — EMS partner (Belgium) + product owner
**Change type:** OQ resolved
**Affected item:** OQ-004
**Old value:** N-seconds escalation timeout — value unresolved, shipped as required config with no default
**New value:** 30 seconds (first tier), 60 seconds (second tier). Configurable per country; these are system defaults.
**Reason:** Belgian EMS protocol requires 30-second window for certified first responders. 60-second second tier aligns with HartslagNu practice.
**Resolves:** OQ-004

### Items updated

- `01-requirements-structured-v1.md` — Section 5 (Open questions): OQ-004 struck through and marked `RESOLVED [CHG-001]: 30s first tier, 60s second tier, configurable per country` [CHG-001]
- `02-scope-and-context-v1.md` — Section 9 (Open scoping questions): OQ-004 entry updated to `RESOLVED — see CHG-001` [CHG-001]
- `03-product-backlog-v1.md` — US-008 status: changed from `Not Ready — blocked on SPIKE-002 (tier taxonomy) and OQ-004` to `Not Ready — blocked on SPIKE-002 (tier taxonomy) only` [CHG-001]. OQ-004 is no longer a blocker.
- `03-product-backlog-v1.md` — US-011 status: same update as US-008 [CHG-001]
- `03-product-backlog-v1.md` — US-013 Notes: updated escalation timeout reference from "OQ-004 unresolved — no default" to "30 seconds (system default, configurable)" [CHG-001]
- `03-product-backlog-v1.md` — US-008 AC criterion: "The value of N (tier escalation timeout) is a per-country configurable value; no hardcoded default ships in code" updated to "The value of N defaults to 30 seconds (first tier) and 60 seconds (second tier), both configurable per country" [CHG-001]
- `04-speckit-specs/epic5-us013-accept-decline.md` — Constraints section: escalation timeout note updated from "OQ-004 unresolved" to "30 seconds (system default, configurable per country)" [CHG-001]
- `05-traceability-matrix.md` — OQ-004 row: changed from "Blocks US-008, US-011, US-013" to "RESOLVED CHG-001 — 30s/60s defaults" [CHG-001]
- `06-change-log.md` — This entry added [CHG-001]
- `00-project-home.md` — Recent changes section: CHG-001 entry added [CHG-001]

### Items reviewed — no change needed

- `US-009` (live status view) — References dispatch status states but not the escalation timeout value. Unaffected.
- `US-010` (stand-down) — References FCM stand-down push. No dependency on escalation timeout. Unaffected.
- `US-014` (navigation) — No dependency on escalation timing. Unaffected.
- `US-015` (CPR guide) — Static content. No dependency on escalation timing. Unaffected.
- `04-speckit-specs/epic3-us010-stand-down.md` — Reviewed. Stand-down spec does not reference escalation timeout. Unaffected.
- `OQ-013` — Tier ordering. Discussed in same call but explicitly not resolved. Not updated per change record notes.

### Follow-up actions required

- [ ] US-008 and US-011 remain blocked on SPIKE-002 (tier taxonomy). OQ-004 is now resolved but SPIKE-002 must still happen before their specs can be written. No spec work yet.
- [ ] US-013 spec (`epic5-us013-accept-decline.md`) previously had "OQ-004 — do not implement until confirmed." That constraint is now resolved. The spec can be handed to dev. No edits needed to the spec itself — the constraint note has been updated.
- [ ] Confirm with product owner whether the 30s/60s defaults should also be documented in the country configuration guide (if that document exists).
