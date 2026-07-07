<!--
Scope & Context — output template.
Fill every section, keep the order. Delete these comments in the final document.

Trace everything to requirement IDs (REQ-F-xxx, REQ-N-xxx, CON-xxx) from the structured requirements.
Mark phasing, effort and risk clearly as analyst assessment for review — not as agreed decisions,
unless the stakeholders fixed them (say so explicitly).

Effort: relative t-shirt size — S / M / L (not a time estimate).
Risk: Low / Medium / High, with a one-line reason.
Priority: MoSCoW (Must / Should / Could / Won't), carried from the requirements.
-->

# Scope & Context — [Project / Feature name]

**Gebaseerd op / Based on:** [structured requirements document + version]
**Datum / Date:** [YYYY-MM-DD]
**Produced by:** scope-and-context skill
**Status:** Concept — voorgestelde scope ter review / Draft — proposed scope for review

## 1. Context

- **Probleem / waarom:** [the problem this solves]
- **Doel:** [the goal / what success looks like]
- **Stakeholders:** [who, and any tensions between them]
- **Huidige situatie (as-is):** [one or two lines]

[All grounded in the structured requirements and its sources. No new facts.]

## 2. Scope-overzicht (at a glance)

| Fase | Thema | Requirement-IDs | Korte motivatie |
|------|-------|-----------------|-----------------|
| Fase 1 | [theme] | REQ-F-001, ... | [why now] |
| Fase 2 | [theme] | ... | [why later] |
| Later / TBD | ... | ... | ... |
| Buiten scope | ... | ... | ... |

## 3. In scope — Fase 1 (eerste release)

[The smallest coherent slice that delivers value. For each item: requirement ID(s), what it is, why it's in Phase 1. If Phase 1 looks too big for a first release, trim to a walking skeleton and state what was moved out and why. Where a Phase 1 item's scope rests on an unanswered open question, state the assumption you're scoping under, or mark it conditional.]

- **[REQ-IDs]** — [item] — [why in Phase 1: Must + prerequisite + value] — [if relevant: "conditional on OQ-xx" or "scoped under assumption: ..."]

## 4. Latere fases

[Phase 2, Phase 3, deferred. What and why deferred. Document even if the later phase is still vague.]

- **Fase 2:** [REQ-IDs] — [item] — [why deferred]
- **Later / TBD:** [REQ-IDs] — [item] — [why]

## 5. Buiten scope

[Explicitly excluded — carried from the requirements' out-of-scope plus anything excluded by a phasing decision. Give the reason and note if the architecture should leave room.]

- [item] — [reason / source]

## 6. Dependencies & build-volgorde

[Feature-to-feature and data/infrastructure/external dependencies. State direction and reason. These drive the order work can be picked up.]

| Item | Hangt af van | Reden | Effect op volgorde |
|------|--------------|-------|--------------------|
| REQ-F-xxx | REQ-F-yyy / [data/infra/external] | [reason] | [e.g. blocker for Phase 1] |

## 7. Effort, risico & prioriteit (analyse-inschatting — ter review)

[Analyst assessment to validate with the delivery team. Effort = S/M/L (relative). Risk = Low/Med/High + reason.]

| Requirement | Prioriteit | Effort (S/M/L) | Risico | Reden risico |
|-------------|------------|----------------|--------|--------------|
| REQ-F-001 | Must | M | Laag | ... |

## 8. Constraints & vroege architectuurbeslissingen

[Hard constraints that shape scope, plus decisions to take early because they affect multiple requirements.]

- **[CON-xxx]** — [constraint] — [effect on scope]
- **Te beslissen nu:** [decision] — [why it can't wait, which requirements it touches]

## 9. Open scopingvragen

[What blocks a clean scope decision — especially unresolved conflicts and undecided phase boundaries carried from the requirements. Flag any Phase 1 item whose scope depends on an open answer.]

- **[question]** — [which requirements/phase it blocks]
