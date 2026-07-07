# Community CPR Volunteer Dispatch — Requirements Vault

This repo is the requirements vault for **Community CPR Volunteer Dispatch**: a system where a
911/112 dispatcher pins a cardiac-arrest patient on a map, finds nearby trained volunteers, and
alerts them with one tap. The volunteer accepts, navigates to the scene, and starts CPR until EMS
arrives.

The vault itself is an AI-driven Business Analysis pipeline built on Claude. It turned the raw
project brief into a full, traceable set of BA documents, keeps them in sync when something
changes, and lets anyone with a GitHub account ask questions about them without pinging Mohamed
for every small clarification.

```
raw brief → structured requirements → scope & phasing → product backlog → dev-ready specs → traceability matrix
```

## What's in here

```
00-project-home.md                 Start here — project status, links to everything
01-requirements-structured-v1.md   REQ-F / REQ-N / CON / OQ / AS, with sources
02-scope-and-context-v1.md         Phase 1 vs Phase 2 vs out of scope, dependencies, risk
03-product-backlog-v1.md           Epics, user stories, acceptance criteria
04-speckit-specs/                  One dev-ready spec file per Phase 1 story
05-traceability-matrix.md          REQ ↔ Story ↔ Spec lookups
06-change-log.md                   Full history of every change, newest first

00-pipeline-skills/                The 6 skills that produced and maintain all of the above
├── requirements-structuring/      raw input → structured requirements
├── scope-and-context/             requirements → phasing, dependencies, effort/risk
├── product-backlog/               scope → epics, stories, acceptance criteria
├── speckit-spec/                  backlog story → dev-ready spec file
├── change-management/             a change record → surgical edits + change log entry
└── vault-qa/                      a GitHub Issue question → a grounded answer (see below)

.github/workflows/vault-qa.yml     Runs vault-qa automatically on labeled issues
scripts/vault_qa_handler.py        The script behind that workflow
github-sync/                       Optional one-way sync: backlog → GitHub Issues
```

Each pipeline skill folder contains `SKILL.md` (its instructions), `assets/` (output templates),
and `examples/` (a worked input/output pair) — open one if you want to see exactly how a document
gets produced, or want to tweak how a step behaves.

## What it can do

**Run the pipeline on a new brief.** Give Claude a project brief (PDF, notes, transcript) and ask
it to run the pipeline. Claude reads `CLAUDE.md`, works through all 6 steps in order, and writes
every document above.

**Handle a change mid-project.** Fill in a change record (see
`00-pipeline-skills/change-management/assets/change-record-template.md`) and Claude updates only
the affected lines across every document, tags them `[CHG-xxx]`, and logs the change — nothing
else gets rewritten.

**Answer questions without you in the loop.** Open a GitHub Issue, label it `vault-question`, and
a bot answers it, grounded in the vault's actual content with citations, within a couple of
minutes. If the question implies something is outdated or wrong, it never edits anything itself —
it posts a draft change proposal for you to approve or reject. If the question itself is
ambiguous, it says so instead of guessing. Works for developers, testers, and other AI agents
alike. Full details, setup, and known limitations: see `README-vault-qa.md`.

**Sync the backlog to GitHub Issues.** `github-sync/` pushes `03-product-backlog-v1.md` to GitHub
Issues one-way, so a dev team can work from Issues instead of the vault. See
`github-sync/README.md`.

## Where to start

- **Browsing the project?** Open `00-project-home.md` in Obsidian — it links to everything else.
- **New here?** `00-how-to-use.md` is a step-by-step cheat sheet.
- **Asking Claude to run or extend the pipeline?** Claude reads `CLAUDE.md` first, always.

The documents use Obsidian wikilinks (`[[filename]]`), so they're meant to be browsed in
[Obsidian](https://obsidian.md) — viewing the raw `.md` files elsewhere (including on GitHub)
shows the literal `[[filename]]` syntax instead of a clickable link.

## ID scheme

IDs are assigned once and never reused or deleted. Changed content keeps its ID; removed content
is struck through, never deleted.

| Prefix | Meaning | Assigned in |
|---|---|---|
| `REQ-F-xxx` | Functional requirement | requirements-structuring |
| `REQ-N-xxx` | Non-functional requirement | requirements-structuring |
| `CON-xxx` | Constraint | requirements-structuring |
| `OQ-xxx` | Open question for a stakeholder | requirements-structuring |
| `AS-xxx` | Assumption | requirements-structuring |
| `EPIC-x` | Epic | product-backlog |
| `US-xxx` | User story | product-backlog |
| `SPIKE-xxx` | Research spike | product-backlog |
| `ENABLER-xxx` | Technical enabler | product-backlog |
| `CHG-xxx` | Change record | change-management |

## Rules the pipeline follows

- **Never invents scope.** If the brief doesn't say it, it isn't a requirement — gaps become Open
  Questions, not assumptions.
- **Never silently resolves an open question.** Only a stakeholder decision, fed in through
  change-management, resolves an `OQ-xxx`.
- **Preserves history.** Every ID is permanent; every story traces back to at least one
  requirement.
- **Edits surgically.** Existing documents are read before being edited, and only the affected
  lines change — never a full rewrite.
- **vault-qa never writes to the vault.** It can only post an answer, or a draft change proposal
  for a human to approve — see `README-vault-qa.md` for the full boundary.
