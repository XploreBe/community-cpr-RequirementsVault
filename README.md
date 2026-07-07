# BA Pipeline Template

A reusable Claude-driven Business Analysis pipeline for Obsidian vaults. Drop these files into any project folder and Claude turns a raw project brief (PDF, notes, transcript) into a full, traceable set of BA artefacts:

```
raw brief → structured requirements → scope & phasing → product backlog → dev-ready specs → traceability matrix
```

It also handles mid-project requirement changes surgically, through a permanent, append-only change log.

## What's in this repo

```
CLAUDE.md                  Pipeline instructions for Claude — read this first
00-how-to-use.md           Human-facing guide to running the pipeline
00-pipeline-skills/        The 5 skills that do the actual work
├── 00-skills-index.md
├── requirements-structuring/   raw input → structured requirements (REQ-F, REQ-N, CON, OQ, AS)
├── scope-and-context/          requirements → phasing, dependencies, effort/risk
├── product-backlog/            scope → epics, user stories, acceptance criteria
├── speckit-spec/                backlog story → dev-ready Spec Kit file
└── change-management/          mid-project change record → surgical edits + change log
github-sync/               Optional: one-way sync from the backlog to GitHub Issues — see github-sync/README.md
```

Each skill folder contains `SKILL.md` (the instructions), `assets/` (the output template), and `examples/` (a worked input/output pair).

This repo intentionally contains **only** the pipeline mechanics. No project content, no generated output files, no personal Obsidian settings. Those get created fresh the first time you run the pipeline on a real project.

## How to use it

1. Copy all of these files into a new project folder (this becomes your vault root).
2. Open the folder in Claude / Cowork with file access to that folder.
3. Give Claude your project brief (attach a PDF, paste notes, paste a transcript) and ask it to run the pipeline.
4. Claude reads `CLAUDE.md`, runs the 7 pipeline steps in order, and creates these files in your vault root:

```
00-project-home.md                 navigation hub
01-requirements-structured-v1.md
02-scope-and-context-v1.md
03-product-backlog-v1.md
04-speckit-specs/                  one file per ready story
05-traceability-matrix.md
06-change-log.md
```

5. When a requirement changes mid-project, give Claude a change record (see `00-pipeline-skills/change-management/assets/change-record-template.md`) and it updates only the affected items across every document, and logs the change.

## Opening the vault in Obsidian

The documents use Obsidian wikilinks (`[[filename]]`) for cross-references, so the vault is meant to be browsed in Obsidian, not just edited by Claude.

1. Install [Obsidian](https://obsidian.md) (free).
2. In Obsidian: **Open folder as vault** → select your project folder (the one containing this `README.md` and `CLAUDE.md`).
3. Start from `00-project-home.md` (created after the first pipeline run) or `00-how-to-use.md` — both are navigation hubs with clickable links to every other document.
4. Wikilinks only render as clickable links inside Obsidian. Viewing the raw `.md` files in another editor or on GitHub will show the literal `[[filename]]` syntax instead of a link.

You don't need Obsidian to run the pipeline — Claude reads and writes the files directly. Obsidian is for *reading* the vault comfortably afterwards.

## Syncing to GitHub

`github-sync/` is an optional, one-way sync tool: it pushes the vault's product backlog (`03-product-backlog-v1.md`) to GitHub Issues, so a dev team can work from Issues instead of the vault. It never syncs back or closes issues automatically. See `github-sync/README.md` for setup and usage.

## ID scheme

IDs are assigned once and never reused or deleted. Changed content keeps its ID; removed content is struck through, never deleted.

| Prefix | Meaning | Assigned in |
|---|---|---|
| `REQ-F-xxx` | Functional requirement | Requirements structuring |
| `REQ-N-xxx` | Non-functional requirement | Requirements structuring |
| `CON-xxx` | Constraint | Requirements structuring |
| `OQ-xxx` | Open question for a stakeholder | Requirements structuring |
| `AS-xxx` | Assumption | Requirements structuring |
| `EPIC-x` | Epic | Product backlog |
| `US-xxx` | User story | Product backlog |
| `SPIKE-xxx` | Research spike | Product backlog |
| `ENABLER-xxx` | Technical enabler | Product backlog |
| `CHG-xxx` | Change record | Change management |

## Rules the pipeline follows

- **Never invents scope.** If the brief doesn't say it, it isn't a requirement — gaps become Open Questions, not assumptions.
- **Never silently resolves an open question.** Only a stakeholder decision, fed in through the change-management workflow, resolves an `OQ-xxx`.
- **Preserves history.** Every cross-document reference is an Obsidian wikilink (`[[file#heading|display]]`), and every story traces back to at least one requirement ID.
- **Edits surgically.** Existing vault documents are read before being edited, and only the affected lines change — never a full rewrite.

## Notes for template maintainers

A couple of files under `00-pipeline-skills/` still reference the original project this template was extracted from (a CPR/emergency-response volunteer app) as illustrative example content — this is intentional, it's just worked examples showing the skills' input/output format, not real project data. `change-management/HOW-TO-TEST.md` in particular assumes a populated vault from that original project exists, so its test scenarios won't run as-is in a fresh template checkout; treat it as a reference for how to test the skill, not a script to run directly.
# community-cpr-RequirementsVault
