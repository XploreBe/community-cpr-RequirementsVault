<!--
Structured Requirements — output template.
Fill every section. Keep the section order and table columns exactly as below.
Delete these HTML comments in the final document.

ID scheme (IDs never change once assigned):
  REQ-F-NNN  functional requirement
  REQ-N-NNN  non-functional requirement
  CON-NNN    constraint
  OQ-NNN     open question
  AS-NNN     assumption

Priority: MoSCoW (Must / Should / Could / Won't). Use "Unspecified" if the source gives no signal — do not guess.
-->

# Structured Requirements — [Project / Feature name]

**Source(s):** [list the inputs this was built from, e.g. "Kickoff notes 29 May", "PM follow-up email"]
**Date structured:** [YYYY-MM-DD]
**Produced by:** requirements-structuring skill
**Status:** Draft — needs human review

## 1. Summary

[2–4 plain sentences describing what this input is about. No new information, no requirements that aren't below.]

## 2. Functional requirements

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| REQ-F-001 | The system shall ... | Must / Should / Could / Won't / Unspecified | [source] | [ambiguity flags, links to OQ-xxx, etc.] |

## 3. Non-functional requirements

| ID | Requirement | Category | Priority | Source | Notes |
|----|-------------|----------|----------|--------|-------|
| REQ-N-001 | The system shall ... | Performance / Security / Privacy / Reliability / Scalability / Portability / ... | Must / Should / Could / Won't / Unspecified | [source] | [notes] |

## 4. Constraints

| ID | Constraint | Source | Notes |
|----|------------|--------|-------|
| CON-001 | [fixed decision or limit, e.g. "Use Google Maps for navigation rather than building in-house"] | [source] | [notes] |

## 5. Open questions (need stakeholder input)

[Gaps, ambiguities, contradictions, and vague terms that a stakeholder must resolve. Link each to the requirement(s) it affects.]

- **OQ-001:** [question] — affects [REQ-x-xxx]

## 6. Assumptions

[Things provisionally taken as true to make progress. Each must be confirmable by a human.]

- **AS-001:** [assumption] — affects [REQ-x-xxx]

## 7. Glossary

[Domain terms as used in the source. If a term is unclear or used inconsistently, say so and link an open question.]

- **[Term]** — [definition as used in the source, or "unclear — see OQ-xxx"]

## 8. Out of scope (explicitly stated)

[Anything the source explicitly says is not being built now or is for a later phase. Keep it — it matters for architecture and traceability.]

- [item] — [source, and any note such as "architecture should leave room for this"]
