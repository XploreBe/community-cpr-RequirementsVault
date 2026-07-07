# BA Pipeline Skills — Index

These are the four skills that produced the CPR project documents. Each folder contains:
- `SKILL.md` — the full instructions given to the AI (what it does, rules it follows, common traps)
- `assets/` — the output template the skill fills in
- `examples/` — a worked example (input → output) used as a reference

If you want to improve a skill, edit its `SKILL.md` and re-run the pipeline step. If you want to run the pipeline on a new project, the skills are reusable as-is.

---

## Pipeline order

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | [[requirements-structuring/SKILL\|requirements-structuring]] | Raw notes, briefs, emails | Structured requirements (IDs, priorities, open questions) |
| 2 | [[scope-and-context/SKILL\|scope-and-context]] | Structured requirements | Scope doc (phases, dependencies, effort/risk) |
| 3 | [[product-backlog/SKILL\|product-backlog]] | Scope + requirements | Epics, user stories, acceptance criteria |
| 4 | [[speckit-spec/SKILL\|speckit-spec]] | Individual backlog stories | Dev-ready spec files for `/speckit.plan` |
| ∞ | [[change-management/SKILL\|change-management]] | A change record (what changed, why) | Surgical edits to affected docs + change log entry |

The change-management skill runs outside the linear pipeline — any time a requirement, decision, or stakeholder input changes mid-project.

---

## Files per skill

### 1. requirements-structuring
- [[requirements-structuring/SKILL|SKILL.md]] — instructions
- [[requirements-structuring/assets/structured-requirements-template|Output template]]
- [[requirements-structuring/examples/example-input-messy-notes|Example input]] · [[requirements-structuring/examples/example-output-structured|Example output]]

### 2. scope-and-context
- [[scope-and-context/SKILL|SKILL.md]] — instructions
- [[scope-and-context/assets/scope-and-context-template|Output template]]
- [[scope-and-context/examples/example-input-structured-requirements|Example input]] · [[scope-and-context/examples/example-output-scope-context|Example output]]

### 3. product-backlog
- [[product-backlog/SKILL|SKILL.md]] — instructions
- [[product-backlog/assets/product-backlog-template|Output template]]
- [[product-backlog/examples/example-input-scope-context|Example input]] · [[product-backlog/examples/example-output-backlog|Example output]]

### 5. change-management *(mid-project, runs any time a change occurs)*
- [[change-management/SKILL|SKILL.md]] — instructions
- [[change-management/assets/change-record-template|Change record template]] — fill this in to trigger the skill
- [[change-management/assets/change-log-template|Change log template]] — format the skill uses for `06-change-log.md`
- [[change-management/examples/example-input-change-record|Example input]] · [[change-management/examples/example-output-change-log-entry|Example output]]

### 4. speckit-spec
- [[speckit-spec/SKILL|SKILL.md]] — instructions
- [[speckit-spec/assets/speckit-spec-template|Output template]]
- [[speckit-spec/examples/example-input-backlog-story|Example input]] · [[speckit-spec/examples/example-output-spec|Example output]]
