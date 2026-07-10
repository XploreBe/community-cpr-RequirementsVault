# Example 4 — Mode B with an explicitly-declared sibling rule

This example is based on a real run against this vault (Issue #25). It's included specifically
to lock in the "check declared siblings" behavior described in the SKILL, after that run needed
two follow-up comments to get there manually. The goal now is that a single pass produces what
took three rounds here.

## Incoming GitHub Issue (abridged)

**Title:** Bug: US-001 never validates lat/lng range

**Body (tester-authored, structured bug report):**
> US-01 ("Create incident") never specifies a valid lat/lng range — the incident form currently
> accepts and stores geographically impossible coordinates (e.g. lat 999) with no rejection, and
> there's no written Acceptance Criteria to say it shouldn't. ... Suggested Clarification:
> latitude outside [-90, 90] or longitude outside [-180, 180] should be rejected.

## What happened the first time (without this check)

1. The skill answered correctly for US-001 only: confirmed the gap, proposed a CHG covering
   `03-product-backlog-v1.md` (US-001 AC) and `04-speckit-specs/epic1-us001-create-incident.md`.
2. A human follow-up comment had to point out that US-004 ("Update incident") explicitly mirrors
   US-001's "location is required" rule via a Constitution snippet ("implement it once, shared,
   not duplicated per form") — and has the exact same coordinate-range gap on the edit path.
3. A second follow-up comment had to ask for the two proposals to be consolidated into one CHG.

Three rounds to reach the right answer. Nothing wrong happened — the skill never edited a file
without approval — but a human had to do the cross-referencing the skill could have done itself.

## What should happen now, in one pass

Reading US-001, the skill finds the gap as before. Before finalizing, it checks whether anything
in the vault text explicitly declares a shared rule with another ID. `03-product-backlog-v1.md`
(US-004) says *"location remains required (same rule as US-001)"*, and
`04-speckit-specs/epic1-us004-update-incident.md`'s Constitution snippet says the location rule
"applies uniformly to create and edit — implement it once, shared, not duplicated per form." That
is a literal, written declaration — not an inference — so the skill checks US-004 for the same
gap category (coordinate range, not just "location required"), finds it's equally missing there,
and folds both into one `chg_proposal`.

```json
{
  "mode": "proposed_change",
  "answer": "US-001 (`03-product-backlog-v1.md`, `04-speckit-specs/epic1-us001-create-incident.md`) has six ACs/scenarios covering map-click, typed coordinates, address, missing-location, optional country, and the one-location rule — none constrain the numeric range of latitude or longitude. US-001's AC explicitly states its 'location is required' rule is shared with US-004 ('same rule as US-001' / Constitution snippet: 'implement it once, shared, not duplicated per form'), so I checked US-004 (`03-product-backlog-v1.md`, `04-speckit-specs/epic1-us004-update-incident.md`) for the same gap category too: it has the same 'location required' negative scenario but the same missing coordinate-range constraint. Note: `04-speckit-specs/epic3-enabler002-incident-crud-endpoints.md` also mirrors US-001's location rule and likely has the same gap at the API layer — flagging this but not resolving it here, since it's a separate layer (backend vs. dispatcher-web form) and would need its own scoping decision.",
  "chg_proposal": "## Possible change detected — draft CHG proposal\n\n**Affected IDs:** US-001 (`03-product-backlog-v1.md`); `04-speckit-specs/epic1-us001-create-incident.md`; US-004 (`03-product-backlog-v1.md`); `04-speckit-specs/epic1-us004-update-incident.md`\n\n**Current value:** Neither US-001 nor US-004 constrains the numeric range of latitude/longitude, even though their 'location is required' rule is already explicitly shared between them.\n\n**Proposed new value:** Add one negative scenario to each of the four artefacts: reject latitude outside [-90, 90] or longitude outside [-180, 180], with a validation message, on both create (US-001) and edit (US-004) — same range, same wording, consistent with how the two stories already share the presence rule.\n\n**Reason:** The incident form accepts and stores geographically impossible coordinates with no rejection on either path, making affected incidents silently unusable on the map and for volunteer routing. The two stories already declare their location rule as shared, so range validation is a natural, minimal extension of that same rule rather than a new decision.\n\n**Source:** GitHub Issue (this issue).\n\n---\nThis is a proposal only. No vault file has been changed. Mohamed needs to review and approve before this is processed via change-management."
}
```

Two things worth naming explicitly about this "improved" output:

- It resolves the US-001/US-004 pair in one pass because the cross-reference is direct and explicit
  in both directions (US-004's AC and spec both name US-001 by ID).
- It does **not** silently fold in ENABLER-002, even though that file also says "mirrors US-001."
  ENABLER-002 sits at a different layer (backend API vs. dispatcher-web form), so whether it
  should be included is a scoping call, not something to decide unasked — it's named in `answer`
  as worth checking, per the "three or more files" guidance in the SKILL, and left for a human (or
  a follow-up comment) to decide, exactly as the real Issue #25 thread did when it was deliberately
  scoped out.
