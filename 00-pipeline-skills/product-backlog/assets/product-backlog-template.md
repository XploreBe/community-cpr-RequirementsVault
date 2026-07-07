<!--
Product Backlog — output template. Fill every section; keep the structure.
Delete these comments in the final document.

Trace every story to requirement IDs (REQ-F-xxx / REQ-N-xxx) and to an epic.
Priority: MoSCoW (Must / Should / Could / Won't), carried from requirements/scope.
Size: S / M / L (relative, provisional — final pointing happens with the team).
Type: Story / Spike / Enabler.
Status: New / Backlog / Not Ready (with reason).
Acceptance criteria: Given/When/Then and/or rule checklist. Always include edge/negative cases.
A tester must be able to write a test case from each criterion with no follow-up question.
-->

# Product Backlog — [Project / Feature name]

**Based on:** [scope & context document + version]
**Date:** [YYYY-MM-DD]
**Produced by:** product-backlog skill
**Status:** Draft — for refinement with the team

## Legend

- **Priority:** MoSCoW (Must / Should / Could / Won't)
- **Size:** S / M / L — relative, provisional (confirm in refinement)
- **Type:** Story / Spike / Enabler
- **Status:** New · Backlog · Ready (conditional — assumption stated) · Not Ready (reason)
- **Grounding:** Direct (traces to a stated requirement) · Derived (rests on an assumption/inference — say which)

## Epics

| Epic ID | Title | Outcome | Requirement IDs | Phase |
|---------|-------|---------|-----------------|-------|
| EPIC-1 | [title] | [one-line outcome] | REQ-F-xxx, ... | Phase 1 |

---

## EPIC-1 — [title]

### US-001 — [short title]
- **Type:** Story
- **Story:** As a [role], I want [capability], so that [benefit].
- **Acceptance criteria:**
  - Given [context], when [action], then [observable outcome].
  - Given [context], when [edge/invalid action], then [outcome].
  - Rule: [invariant / constraint with concrete values].
- **Priority:** [MoSCoW] · **Size:** [S/M/L, provisional] · **Phase/Sprint:** [phase]
- **Epic:** EPIC-1 · **Traces to:** [REQ-IDs]
- **Grounding:** Direct / Derived (if Derived: which assumption or inference)
- **Depends on / Blocked by:** [US-xxx / external / —]
- **Status:** [New / Ready (conditional) / Not Ready — reason]
- **Notes:** [assumptions, open questions this rests on]

### SPIKE-001 — [question to resolve]
- **Type:** Spike (timeboxed)
- **Goal:** [the decision or feasibility answer to produce — not software]
- **Done when:** [a recommendation/decision is documented]
- **Priority:** [MoSCoW] · **Phase/Sprint:** [phase]
- **Traces to:** [REQ-IDs / OQ-xx]

---

## Suggested build order (this phase)

[Enablers and de-risking spikes first, then stories in dependency order, then by value. A starting sequence for the team, not a fixed plan.]

1. [ENABLER / SPIKE]
2. [US-xxx] — [why here]
3. ...

## Dependencies overview (optional)

| Story | Depends on | Reason |
|-------|-----------|--------|
| US-xxx | US-yyy / external | [reason] |

## Items sent back (not turned into stories)

[Anything that would need new scope to become a story — flagged back to the requirements/scope step rather than invented here.]

- [item] — [why it needs scope first]

## Definition of Ready / Done

- **Ready (per story):** clear role + benefit; testable acceptance criteria incl. edge cases; provisional size; dependencies identified; no blocking open question.
- **Done:** defined by the delivery team (placeholder — to be set with the team).
