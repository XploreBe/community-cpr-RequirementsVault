---
name: requirements-structuring
description: Turn messy, unstructured input (meeting notes, transcripts, emails, slide text, scattered bullet points) into a clean, consistently formatted structured requirements document that downstream agents and analysts can rely on. Use this whenever someone has raw or informal requirement input and wants it organised, or mentions structuring requirements, cleaning notes into requirements, preparing requirements for user stories, a requirements intake step, or a "step 0" before scope and story work. Assigns stable IDs for traceability, separates functional requirements, non-functional requirements and constraints, and flags ambiguities as open questions instead of inventing answers.
---

# Requirements Structuring

This skill takes raw, messy input about what a system should do and turns it into a clean, predictable requirements document. The point is that everything downstream — scope mapping, epics, user stories, acceptance criteria, test cases — depends on this being accurate and consistently formatted. If this step invents, misreads, or loses things, those errors quietly spread through the whole project and are expensive to catch later.

The output is for two readers at once: a human analyst who reviews and approves it, and the next AI agent that consumes it. So it must be both trustworthy and rigidly consistent in structure.

## Core principles

These are the rules that make the output trustworthy. Follow them strictly.

**Never invent.** Only capture requirements that are actually present in the input. Do not add "obvious" requirements, fill in industry-standard features, or smooth over gaps with assumptions presented as fact. If the input does not say it, it is not a requirement. This is the single most important rule: a reviewer must be able to trust that every line traces back to something real in the source. If you find yourself adding something the source did not mention, stop — that belongs in Open Questions or Assumptions, clearly labelled, not in the requirements.

**Trace everything to its source.** Every requirement records where it came from (which note, email, slide, or meeting). This is what makes later impact analysis possible — when a requirement changes, you need to know what it touched.

**One requirement per entry (atomic).** Split compound statements. "Dispatchers log in with MFA and see a live map" is two requirements, not one. Atomic requirements are easier to test, prioritise, and trace.

**Phrase for testability.** Write each requirement so it could later become a testable acceptance criterion. Prefer "The system shall send the alert to the volunteer's phone within 5 seconds" over "alerts should be fast." If the source only gives a vague version ("fast", "easy", "user-friendly"), capture what was said, then add a note that it needs a measurable definition and raise an open question. Do not invent the number yourself.

**Separate what you know from what you don't.** Three different buckets, never blurred:
- **Requirements** — what the input actually states.
- **Open questions** — gaps, ambiguities, contradictions, and vague terms that need a stakeholder to resolve.
- **Assumptions** — things you are provisionally taking as true to make progress, clearly flagged so a human can confirm or reject them.

**Implied is not the same as stated.** If something is only implied — a logical consequence of what was said, a pain point that hints at a feature, an "obvious" need — it does not belong in the requirements tables. Put it in Assumptions if you are provisionally treating it as true, or in Open Questions if it needs confirming. The requirements tables hold only what the input actually states, so the reviewer can always tell fact from inference at a glance. (Do not record a derived item as a requirement "with a note" — that blurs the line this whole skill exists to keep sharp.)

## How to do it

1. **Read all the input fully before writing anything.** Get the whole picture first; requirements in one note often clarify or contradict another.
2. **Extract candidate requirements.** Pull out every statement about what the system should do, be, or not do.
3. **Make them atomic.** Split anything compound into separate entries.
4. **Classify each one:**
   - **Functional** — something the system does (a behaviour, action, or capability).
   - **Non-functional** — a quality the system must have (performance, security, privacy, reliability, scalability, portability, etc.).
   - **Constraint** — a fixed decision or limit (a mandated technology, platform, regulation, "use X instead of building our own").
   - **Out of scope** — anything the source explicitly says is not being built now / is for later.
5. **Assign stable IDs** using the scheme in the template (REQ-F-001, REQ-N-001, CON-001, OQ-001, AS-001). IDs never change once assigned — downstream artefacts will reference them.
6. **Set priority only if the source indicates it.** Use MoSCoW (Must / Should / Could / Won't). If the source gives no signal, mark it `Unspecified` — do not guess.
7. **Record the source** for every entry.
8. **Flag ambiguities.** Vague wording, contradictions between notes, or missing detail go in the Notes column and, where a decision is needed, become an Open Question. Never resolve an ambiguity by inventing an answer.
9. **List assumptions separately**, each linked to the requirement(s) it affects.
10. **Build a glossary** of domain terms as used in the source. If a term is used inconsistently or unclearly, say so and raise an open question rather than picking a definition.
11. **Sweep for silent gaps** (see the next section), then **fill the template** in `assets/structured-requirements-template.md` exactly. The consistent structure is what lets the next agent consume the output reliably.

## Sweep for silent gaps

Faithfully capturing what was said is only half the job. The requirement problems that hurt most are usually things nobody said — gaps that stay invisible until build or testing. So after structuring what the input states, do a deliberate gap sweep: walk the categories below and, for each, ask whether the input addresses it. Where it does not, and the gap is materially relevant to what is being built, raise a neutral Open Question. Do not invent a requirement to fill the gap, and do not raise questions about things clearly irrelevant to this system — the goal is to surface real holes, not to pad the document.

Common gap categories to check:
- **Access and roles** — who uses the system in which role, and what may each person see or do? Often left unstated in small-team projects.
- **Connectivity and sync** — if anything works offline or on mobile, when and how does data sync back, and what happens if it never does? "Offline" almost always hides a sync decision and downstream effects (e.g. on anything that depends on that data arriving).
- **Data lifecycle** — for data that is created or migrated: how long is it kept and what is archived? For migration specifically: what is in scope to migrate, and how is poor-quality source data (missing fields, inconsistent formats) handled?
- **Failure and edge cases** — device loss, partial completion, a step abandoned halfway, a refusal (e.g. no signature), bad or rejected input. What should the system do?
- **Cross-entity integrity** — entities that are inactive, changed, or removed (e.g. a former employee, a cancelled record) and how references to them behave.
- **Oversight and visibility** — does someone responsible need a view of status, delays, or what happened — separate from any reporting/dashboards that were explicitly deferred?
- **Measurement of stated targets** — if the input sets a target (a response time, a service level), how does the system know whether it is being met, and is the target precisely defined?
- **Stakeholder conflicts** — where two people want different things, even subtly. Always surface these rather than quietly picking a side.

Treat this list as prompts, not a checklist to fill. Only raise what is genuinely relevant and genuinely absent. A good gap sweep turns "the notes didn't mention it" into an explicit question the stakeholders can answer, instead of a surprise three weeks into the build.

## Output format

Always produce the document using `assets/structured-requirements-template.md`. Keep the section order and the table columns exactly as given. The sections are:

1. Header (project/feature, sources, date, status)
2. Summary (plain, no new information)
3. Functional requirements (table)
4. Non-functional requirements (table)
5. Constraints (table)
6. Open questions (need stakeholder input)
7. Assumptions
8. Glossary
9. Out of scope (explicitly stated)

Output Markdown. The strict, repeatable structure is deliberate — it is what makes the document both human-reviewable and machine-readable for the next step, without needing a separate format.

## Handling different input types

- **Meeting / kickoff notes** — informal and elliptical. Watch for decisions stated in passing ("just use Google Maps") and for things marked TBD.
- **Emails** — often add requirements on top of an earlier discussion. Treat each distinct point as a candidate requirement and attribute it to the email.
- **Slide text** — terse. A bullet may compress several requirements; expand and split them.
- **Transcripts** — verbose and repetitive. The same requirement may be restated several ways; capture it once, pick the clearest phrasing, and note if speakers disagreed.

## Common traps to avoid

- Turning a vague phrase into a precise requirement by inventing the precision. Capture the vagueness, flag it.
- Merging two requirements because they appeared in the same sentence.
- Dropping things that are "obviously later" instead of recording them under Out of scope — later-phase items still matter for architecture and traceability.
- Quietly resolving a contradiction between two notes. Record both and raise an open question.
- Adding security/privacy/performance requirements from general best practice that the source never mentioned. If it matters and isn't there, that's an open question for stakeholders.
- Recording an implied or derived item as a requirement, even "with a note". Implied items go in Assumptions or Open Questions, never in the requirements tables.
- Finishing without a gap sweep. Capturing only what was said is the most common way to miss the holes that surface later in build or testing.

## Example

A worked example is included so the expected style is concrete:
- `examples/example-input-messy-notes.md` — realistic messy input (kickoff notes + a follow-up email + a stray vague line).
- `examples/example-output-structured.md` — the structured document produced from it, showing atomic splitting, classification, IDs, sources, open questions for the TBD/vague items, assumptions, glossary, and out-of-scope handling.

Read both when you need a reference for the level of detail and the treatment of ambiguity.
