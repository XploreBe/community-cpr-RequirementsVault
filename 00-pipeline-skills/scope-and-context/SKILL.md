---
name: scope-and-context
description: Turn a structured requirements document into a clear scope and context document for an Agile/Scrum project — what is in scope for the first release, what is deferred to later phases, what is out of scope, how requirements depend on each other (build order), and a lightweight effort, risk and priority assessment to support phasing. Use this after requirements have been structured (the "step 0" output) and before writing epics and user stories, or whenever someone needs to define release scope, map dependencies, plan phasing, or separate an MVP from later work. It maps and assesses what the requirements say and proposes phasing for review; it does not invent new requirements and does not silently resolve open conflicts.
---

# Scope & Context

This skill takes a structured requirements document (the output of the requirements-structuring step) and turns it into a scope and context document: the framing of the project, what goes in the first release, what is deferred, what is excluded, how the pieces depend on each other, and a first read on effort, risk and priority. It is the bridge between "we know what's being asked for" and "we can write epics and stories." The next step (epic/story writing) consumes this directly.

Two readers again: a human analyst who reviews and decides, and the next agent that writes stories. So it must be honest about what is fact versus proposal, and consistent in structure.

## What this step adds — and the line it must not cross

Unlike the structuring step, which only captures, this step is allowed to add analytical judgement: it proposes phasing, and it assesses effort, risk and priority. That judgement is the analyst's value.

But there is a hard line: **the scope document organises and assesses the existing requirements; it never invents new ones.** Every scope item traces back to a requirement ID from the structured requirements. If the analysis surfaces something genuinely new, that is a finding to send back to the requirements step, not a requirement to add here.

And a second line: **separate what stakeholders decided from what the analyst proposes.** If stakeholders fixed something ("the portal is a later phase"), record it as their decision. Everything else — the phase you suggest, the effort size, the risk rating — is a proposal for review and must be labelled as such, so no one mistakes the analyst's draft phasing for an agreed plan.

## Core principles

**Trace to requirement IDs.** Every in-scope, deferred, or out-of-scope item references the REQ/CON IDs it covers. This continues the traceability chain (requirement → scope → story → acceptance criteria → test → spec).

**Phase 1 is the smallest coherent slice that delivers value.** Think Agile/MVP: not "every Must dumped together," but the minimum that works end to end and is worth shipping as a first increment. A Must-have whose prerequisite is unbuilt cannot be in Phase 1 on its own.

**Dependencies drive build order.** Surface feature-to-feature dependencies and dependencies on data, infrastructure, or external services. State the direction ("X requires Y first") and the reason. Where a dependency is uncertain, raise it as an open scoping question rather than guessing.

**Do not resolve open conflicts to make scoping cleaner.** If the requirements carry an unresolved conflict (two stakeholders wanting different things) or an undecided phase boundary, the scope that depends on it is itself an open question. Carry it forward; never pick a side silently just to produce a tidy phase plan.

**Effort and risk are signals, not estimates.** Effort is relative t-shirt sizing (S / M / L) — you cannot give time estimates without the delivery team. Risk is Low / Medium / High with a one-line reason. Both are inputs to phasing and must be marked as analyst assessment to be validated with the team. Use this rubric so the ratings stay consistent across requirements and across runs:
- **Effort** — S: a well-bounded piece, roughly a sprint or less. M: a few sprints, some moving parts. L: spans a release cycle, or has substantial unknowns in its own right.
- **Risk** — Low: well-understood, no new technology, no dependency on an open question. Medium: real complexity, or it depends on another item or an external service. High: new or unproven technology, a major unknown, or it is blocked by an unresolved conflict or open question.

**Nothing deferred gets lost.** Later-phase and out-of-scope items are documented with a reason, even when the later phase is still vague. Architecture-relevant "not now" items especially must stay visible.

## How to do it

1. **Read the whole structured requirements document first**, including its open questions and assumptions — they directly affect what can be scoped cleanly.
2. **Write the context** from the requirements' summary and sources: the problem, the goal, the stakeholders (and any tensions between them), and the as-is situation in a line or two. No new facts.
3. **List every requirement with its stated priority** and any phase or deferral the stakeholders already fixed.
4. **Derive dependencies** — which requirements need another requirement, or some data/infrastructure/external service, in place first. Note direction and reason.
5. **Assess effort (S/M/L) and risk (Low/Med/High + reason)** for each requirement. Mark these clearly as analyst assessment.
6. **Propose the phasing.** Phase 1 = the coherent value-delivering slice: the Musts plus their prerequisites, biased toward lower risk where there's a choice. Defer the rest into later phases with reasons. Respect anything stakeholders already fixed as later or out of scope.
7. **Sanity-check the size of Phase 1.** Ask whether the proposed Phase 1 could realistically ship as a first release in a reasonable window (a quarter or less is a useful yardstick). If it is too big — for example most requirements are Must and they all landed in Phase 1 — do not just list them all. Propose a thinner "walking skeleton": the narrowest path that still works end to end and delivers value, and state explicitly what you moved out of Phase 1 and why. "It's a Must" is a reason to ship it early, not a reason it must be in the very first release.
8. **Carry forward unresolved conflicts and undecided boundaries** as open scoping questions. For every Phase 1 item whose scope rests on an unanswered open question, say so inline in the Phase 1 section — either state the assumption you are scoping under ("Phase 1 assumes specialisation does not affect assignment; confirm") or mark the item's Phase 1 scope as conditional on that question. A reviewer should never have to wonder why something is in Phase 1 when the decision behind it isn't made yet.
9. **Identify hard constraints and the architectural decisions that should be made early** because they affect several requirements (for example an offline sync strategy, or which external package to integrate).
10. **Fill the template** in `assets/scope-and-context-template.md` exactly, so the next step can consume it reliably.

## Output format

Always use `assets/scope-and-context-template.md` and keep the section order. The sections are:

1. Header (based-on requirements doc, date, status)
2. Context (problem, goal, stakeholders, as-is)
3. Scope overview at a glance (phase / theme / requirement IDs)
4. In scope — Phase 1
5. Later phases
6. Out of scope
7. Dependencies & build order
8. Effort, risk & priority (analyst assessment — for review)
9. Constraints & early architectural decisions
10. Open scoping questions

Output Markdown. Keep the proposal sections (phasing, effort, risk) clearly marked as the analyst's assessment for review.

## Common traps to avoid

- Inventing a requirement while scoping. Only organise and assess what the structured requirements contain; new findings go back to the requirements step.
- Presenting analyst proposals (phasing, effort, risk) as if the stakeholders had decided them.
- Silently resolving a stakeholder conflict to make the phase plan tidy. Carry it forward as an open question.
- Putting an item in Phase 1 while its dependency sits in a later phase — a broken build order.
- Giving effort as time estimates ("2 weeks") instead of relative sizing (S/M/L). You don't have the team yet.
- Dropping deferred or out-of-scope items instead of documenting them with a reason.
- Treating Phase 1 as "all the Musts." It is the smallest coherent slice that ships value, constrained by dependencies and risk — and if it's too big, it gets trimmed to a walking skeleton with the cuts justified.
- Leaving a Phase 1 item silently resting on an unanswered open question. Say what you're assuming, or mark the item conditional.

## Example

A worked example shows the expected output and how it chains from the previous step:
- `examples/example-input-structured-requirements.md` — a structured requirements document (the kind the requirements-structuring skill produces).
- `examples/example-output-scope-context.md` — the scope and context document produced from it, showing phasing, dependency-driven build order, the effort/risk/priority assessment marked as analyst judgement, and open scoping questions where unresolved conflicts block a clean decision.
