---
name: product-backlog
description: Turn a scope and context document (or structured requirements) into a real Agile/Scrum product backlog — epics, INVEST user stories in the "As a [role], I want [capability], so that [benefit]" format, and testable acceptance criteria a QA team can write test cases from, plus priority, relative sizing, epic links, dependencies and traceability — the fields you would actually populate in Jira or Azure DevOps. Use this after scope and phasing are set and before development, or whenever someone needs to write epics, user stories or acceptance criteria, split large items into small stories, or build a backlog. It crafts stories and acceptance criteria grounded in the existing requirements and scope; it does not invent new scope, it writes spikes for genuine unknowns, and it does not silently resolve open questions.
---

# Product Backlog (epics, user stories, acceptance criteria)

This skill takes a scope and context document (and the structured requirements behind it) and produces a real, refinement-ready product backlog: epics, user stories, and acceptance criteria, with the metadata a team needs in Jira or Azure DevOps. It is the last analysis step before development picks the work up.

Three readers this time: the PO/BA who reviews it, the developers who build from it, and the testers who write test cases from the acceptance criteria. So every item must be unambiguous, independently understandable, and testable.

## The craft line it must not cross

This step is creative — it writes story text and acceptance criteria, which the upstream steps did not. But it crafts only from what scope and requirements already contain. It **does not invent new scope.** Every story traces back to a requirement ID.

When the work surfaces something that isn't covered by the requirements (a missing capability, a prerequisite nobody specified), do not write a story for it — flag it back to the requirements/scope step. When something is a genuine unknown (a technical approach nobody has decided, an unresolved open question), write a **spike**, not a fake story that pretends the unknown is solved. And never write an acceptance criterion that silently resolves an open question — mark the story blocked or state the assumption instead.

## Core principles

**Epics group stories toward an outcome.** Each epic has an ID, a title, a one-line outcome, the requirement IDs it covers, and a phase. Epics usually map to the scope's themes.

**User stories use the standard format and are vertical slices of value.** "As a [role], I want [capability], so that [benefit]." A story delivers something a user values — not a technical task ("build the database" is not a story; it may be an enabler or a spike). The role must be a real user role; the benefit must be a real reason, not a restatement of the capability.

**Check the benefit clause — it's the most-skipped quality bar.** The "so that..." must express why the *user* cares, in their terms. Reject three weak patterns: (a) restating the capability ("so that I can [the capability again]"), (b) a system outcome ("so that the system records it"), and (c) a vague consequence ("so that things don't go wrong"). Test it: would the role say this out loud as their reason? "So that I can reschedule in minutes instead of a morning of phone calls" passes; "so that appointments aren't disrupted" is a consequence, not their benefit. A weak benefit usually means the story was written from the system's perspective — rewrite it from the user's.

**INVEST.** Each story should be Independent (minimise coupling to other stories), Negotiable (the what, not a rigid spec), Valuable (to a user or the business), Estimable (clear enough to size), Small (fits comfortably in a sprint — split if not), and Testable (you can state how you'd verify it). If a story fails one of these, fix or split it.

**Split large items into small stories.** Useful split patterns: by workflow step, by business rule, by CRUD operation, by happy path vs edge/error path, by data or interface variation, by simple-then-enrich. Prefer several thin vertical stories over one fat one.

**Acceptance criteria are the testable contract** — see the quality bar below. Use Given/When/Then scenarios for behaviour and/or a rule checklist for constraints, and always cover the negative and edge cases, not just the happy path.

**Traceability.** Every story records the requirement ID(s) it satisfies (requirement → scope → story → acceptance criteria → test → spec). Every epic records its requirement IDs and phase.

**Priority and sizing.** Carry MoSCoW priority from the requirements/scope. Propose a relative size (S/M/L, or provisional story points) but mark it as provisional — final pointing happens with the delivery team in refinement.

**Order the backlog.** Don't just group stories by epic — propose a suggested build order for the phase, respecting dependencies: enablers and de-risking spikes first, then stories in dependency order, then the rest by value. The team gets a starting sequence, not just a pile.

**Independence and dependencies.** Aim for stories that can be built and tested on their own. Where a real dependency exists (from the scope's build order), record it as a "depends on" / "blocked by" link rather than hiding it. Be careful not to over-couple: depend on the smallest thing that's truly needed (a customer existing, not the entire migration).

**Show each story's grounding.** Mark whether a story traces to a direct requirement, or rests on an assumption or inference. If it rests on an assumption (e.g. an upstream AS-xx) or is inferred rather than stated, tag it so the reviewer can see at a glance which stories stand on solid ground. Anything that would need genuinely new scope is not tagged — it's sent back.

**Respect upstream open questions, and status accordingly.** An open question can land a story in one of two places, and the difference matters:
- **Not Ready (blocked)** — the question could go either way and would materially change the story (or a prerequisite is missing). Don't write speculative criteria; mark it blocked with the reason, or write a spike.
- **Ready (conditional)** — you can proceed under a clearly stated, reasonable assumption and adjust later. Write the story, state the assumption explicitly, and omit any criterion the open question would decide.
Never silently paper over the question, and never mark a story plainly Ready when it secretly rests on an unanswered either/or decision.

## Acceptance criteria — the quality bar

A tester must be able to write a test case from each criterion without asking a follow-up question. Concretely:

- **Testable and observable.** Each criterion describes a verifiable outcome, not an intention.
- **Unambiguous.** No vague adjectives ("fast", "user-friendly", "intuitive"). If the requirement only gave a vague term, reference the measurable definition from the requirements, or mark the story blocked on the open question that defines it — do not invent a number.
- **Pin down decision-driving terms.** Any term in a criterion whose meaning decides pass or fail — "available", "nearby", "valid", "complete", "active" — must be defined inline, point to an upstream definition, or be raised as an open question. It is not enough to avoid adjectives; a noun like "available technician" is untestable until "available" is defined. A tester should never have to guess what the word means.
- **Independently verifiable.** Each criterion stands on its own; a reviewer can mark it pass/fail.
- **Covers the negative and edge cases.** Invalid input, the empty case, the failure case, the boundary (e.g. exactly at a limit). Happy-path-only acceptance criteria are the most common defect source.
- **Concrete about data and limits.** State the actual values, statuses, and boundaries involved.
- **Format:** Given/When/Then for behaviour ("Given [context], when [action], then [outcome]"); a rule checklist for invariants and constraints. Mix as needed.

## How to do it

1. **Read the scope document and the structured requirements fully** — including phasing, dependencies, open questions, and assumptions. They decide what is in this backlog and what is blocked.
2. **Define the epics** from the scope's themes/phases; give each an outcome and its requirement IDs.
3. **Draft the stories.** For each in-scope requirement, write one or more stories in the standard format, splitting large requirements into small vertical slices.
4. **Write the acceptance criteria** to the quality bar above — Given/When/Then and/or rules, happy path plus edge/negative.
5. **Run each story through INVEST.** Split anything too big; rewrite anything not testable.
6. **Set priority (MoSCoW) and a provisional size**, and assign the phase/sprint candidate from the scope.
7. **Record dependencies** as links; keep stories as independent as possible.
8. **Write spikes** for genuine unknowns (open technical questions, high-risk approaches) instead of pretending they're normal stories.
9. **Flag anything needing new scope back to the requirements/scope step** — do not invent it as a story.
10. **Add backlog metadata** — type, epic link, traces-to (and a grounding tag where the story rests on an assumption or inference), and a status from the vocabulary: New/Backlog (ready), Ready (conditional — assumption stated), or Not Ready (blocked — reason). Check each story against the Definition of Ready. Also set **Delivery status** to "Not started" — this is a separate field from Status: Status is BA-readiness (is this ready to be picked up), Delivery status is actual build progress (Not started / In Progress / Done), and it is owned by the delivery team from here on, not by this skill. Always initialise it to "Not started"; never set it to "In Progress" or "Done" yourself, even if a story looks straightforward or its acceptance criteria seem obviously satisfiable.
11. **Propose a suggested build order** for the phase: enablers and spikes first, then stories in dependency order, then by value.
12. **Fill the template** in `assets/product-backlog-template.md` exactly.
13. **If `00-project-home.md` already exists and has a "Current status" section with a backlog-readiness table** (Ready / Ready (conditional) / Not Ready / Won't counts per repo — e.g. from an earlier phase's pipeline run), update that table to include this run's items too, so it still matches the full backlog across all phases. Only touch the readiness counts, never the Delivery status column.

## Definition of Ready (per story)

A story is Ready for a sprint when: it has a clear role and benefit; testable acceptance criteria including edge cases; a provisional size; identified dependencies; and no unresolved open question blocking it. Mark stories that don't yet meet this as "Not Ready" with the reason. (Definition of Done is team-level and set by the delivery team, not here.)

## Common traps to avoid

- Writing technical tasks as user stories ("set up the database"). That's an enabler or a spike, and enablers only exist where an architecture decision in scope demands them.
- Acceptance criteria that only cover the happy path, or that contain vague adjectives a tester can't verify.
- Inventing a story for something the requirements don't cover. Flag it back instead.
- Writing a normal story for a genuine unknown instead of a spike.
- Acceptance criteria that quietly decide an open question. Mark the story blocked or state the assumption.
- A benefit clause that just restates the capability ("so that I can [the capability again]"), describes a system outcome ("so that it gets saved"), or gives a vague consequence ("so that nothing goes wrong") instead of the user's real reason.
- Fat stories that can't fit a sprint. Split them.
- Confusing Status (BA-readiness) with Delivery status (build progress), or setting Delivery status to anything other than "Not started" for a newly written item. Delivery status belongs to the delivery team from the moment a story is added.

## Example

A worked example continues the chain (structured requirements → scope → backlog):
- `examples/example-input-scope-context.md` — a scope and context document (the kind the scope-and-context skill produces).
- `examples/example-output-backlog.md` — the backlog built from it: epics, well-formed stories with Given/When/Then acceptance criteria covering edge cases, a spike for a genuine unknown, a story correctly marked blocked because it needs scope that isn't in the requirements, plus priority, sizing, dependencies and traceability.
