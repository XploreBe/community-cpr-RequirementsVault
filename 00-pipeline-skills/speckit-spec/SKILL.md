---
name: speckit-spec
description: Turn a product backlog story (with acceptance criteria, constraints, and traceability) into a Spec Kit spec file ready for spec-driven development — the artifact that feeds into /speckit.plan, /speckit.tasks, and /speckit.implement. Use this after the product backlog is produced and before the development team starts building, or whenever a backlog story needs to be handed off to a Spec Kit project. It produces one spec file per story, grounded in the story's acceptance criteria and upstream requirements; it does not invent new scope and does not silently resolve open questions.
---

# Spec Kit Spec File

This skill bridges the analysis pipeline (structured requirements → scope → backlog) to the Spec Kit spec-driven development workflow. It takes a single backlog story — with its acceptance criteria, constraints, grounding, and open questions — and produces a well-formed spec file that a developer can drop into a Spec Kit project and immediately run `/speckit.plan` against.

The value: instead of a developer writing a vague `/speckit.specify "build the technician suggestion feature"` prompt, they get a precise spec grounded in analyzed requirements, testable scenarios from the AC, and explicit constraints. The AI coding tool has far more to work with, and the output is more predictable.

## What this step does and does not do

**Does:** translate the story's AC into Spec Kit scenarios, surface constraints and assumptions the dev needs to know, and flag any open questions that could affect implementation.

**Does not:** invent new requirements, add technical implementation detail (that is `/speckit.plan`'s job), or resolve open questions that the BA left open. If the story is Not Ready (blocked), note it and do not produce a spec — send it back.

## One spec file per story

Produce one spec file per backlog story. Epic-level specs are too large for an AI coding tool to act on cleanly and undermine the incremental Spec Kit workflow. Each spec should be completable in a single `/speckit.implement` run.

## What goes in the spec file

A Spec Kit spec file (the output of `/speckit.specify`) is a Markdown document with four parts:

**1. Overview** — what this feature is, who it's for, and why it exists. Drawn from the story's role, capability, and benefit clause. One short paragraph. No technical detail.

**2. User scenarios** — the behavioral requirements in scenario format. These come directly from the story's Given/When/Then acceptance criteria, translated into plain prose scenarios or kept as Given/When/Then. Include the negative and edge cases — they are requirements, not optional. Do not drop them for brevity. Each scenario has a short title.

Before writing a scenario, ask: can this situation actually be reached by a user through normal interaction? A scenario for a state the UI makes unreachable (e.g. a referential-integrity error that can only occur via a direct API call, not through the UI) misleads the AI coding tool into building unnecessary guard code. If the scenario is only reachable outside the UI (API, data race, direct database access), note that in the scenario title — "Scenario N — [case] (API/data layer only)" — and keep it only if the system genuinely needs to defend against it.

**3. Constraints and assumptions** — hard limits the implementation must respect. Sources: the story's upstream constraints (CON-xxx), the scope document's architectural decisions, and the story's stated assumptions. Keep each constraint short and actionable. Where an assumption is provisional (marked in the backlog), say so. Do not present assumptions as decisions.

**4. Out of scope** — what this spec explicitly does not cover, drawn from the story's notes (deferred items, items sent back, open questions). This protects the developer from scope creep and tells the AI coding tool what not to build.

## The constitution snippet

Alongside the spec file, produce a short constitution snippet — two to five bullet points of governing principles specific to this story that should be added to the project's `/speckit.constitution`. These come from the non-functional requirements and constraints that apply to this feature (usability, offline behaviour, security, performance). Do not repeat principles already in the project constitution if one exists; add only what is new for this story.

## Handling open questions

If the story has open questions that could affect implementation (e.g. a definition not yet confirmed, a decision not yet made), list them in the spec's out-of-scope section under "Unresolved — dev should not implement until confirmed." Do not invent an answer to make the spec look complete.

**Open questions that affect a scenario's behaviour must also be visible in that scenario.** If you write a scenario that says "when the overview refreshes" but the refresh mechanism is an open question, the scenario is hiding an assumption. Either (a) remove the assumption from the scenario wording ("when the overview is viewed"), or (b) mark the scenario explicitly conditional ("assumes polling — to confirm"). A scenario and an unresolved note about that same decision must never silently contradict each other.

If the story is marked **Not Ready (blocked)** in the backlog, do not produce a spec. Return a one-line note: "Story [US-xxx] is blocked on [reason]. Spec will be produced once the blocker is resolved."

## Format and file naming

- File: `specs/[epic-id]-[story-id]-[short-slug].md` (e.g. `specs/epic1-us002-suggest-technician.md`)
- Output Markdown, clean and readable — the AI coding tool will ingest this directly.
- Keep it focused: a good spec is one to two pages. If it's longer, the story probably needs splitting.

## How to do it

1. Read the story fully — role, benefit, all AC including edge/negative cases, grounding, status, and notes.
2. If the story is Not Ready (blocked), stop and return the blocker note.
3. Write the overview from the role + benefit clause.
4. Translate each AC criterion into a scenario. Keep Given/When/Then where it adds clarity; flatten to prose where the criterion is a simple rule. Do not omit edge and negative cases.
5. Extract constraints from upstream CON-xxx, scope constraints, and the story's assumptions. Mark provisional ones as provisional.
6. List out-of-scope items from the story's notes and from any open questions that could affect implementation.
7. Write the constitution snippet from relevant non-functional requirements.
8. Fill the template in `assets/speckit-spec-template.md`.

## Common traps to avoid

- Dropping edge cases and negative scenarios to keep the spec short. They are requirements; the AI coding tool needs them to build the right thing.
- **Missing input-validation scenarios.** If the feature accepts user input (a form, a registration, an import), always include at least one scenario for what happens when required input is missing or invalid. A spec with only a happy-path scenario for an input feature is incomplete — the AI coding tool will not know what to validate.
- A scenario and an unresolved open question that contradict each other. If a scenario assumes an answer to an open question, either neutralise the assumption in the scenario wording or mark it conditional. See "Handling open questions" above.
- Adding technical implementation detail (database schema, API design, framework choice). That is `/speckit.plan`'s job, not the spec's.
- Inventing a resolution for an open question. List it as unresolved.
- Producing a spec for a Not Ready story. Return the blocker note instead.
- Writing an overview that describes the system instead of the user's experience.
- Writing a scenario for a state the user cannot reach through normal interaction without flagging it as API/data-layer only.

## Example

A worked example shows the translation from backlog to spec:
- `examples/example-input-backlog-story.md` — a single story extracted from a product backlog.
- `examples/example-output-spec.md` — the Spec Kit spec file produced from it, plus the constitution snippet.
