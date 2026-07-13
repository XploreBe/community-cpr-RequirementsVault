# CLAUDE.md — BA Pipeline Vault

This file is instructions for Claude. Read it fully before doing anything in this workspace.

---

## What this workspace is

This is an AI-assisted Business Analysis pipeline vault. It turns unstructured project briefs (PDFs, notes, transcripts, meeting notes) into a full set of BA artefacts: structured requirements, scope document, product backlog, and dev-ready spec files — all linked by stable IDs and a traceability matrix. It also handles mid-project requirement changes surgically via a change log.

The vault is self-contained. All skill instructions live in `00-pipeline-skills/`. You do not need any installed Claude skills — read the SKILL.md files from the vault instead.

**Vault path:** derive it from the location of this CLAUDE.md file. All file saves go relative to the folder containing this file.

---

## Vault structure

When the pipeline runs for the first time, it creates these files:

```
[project-folder]/                    ← root (where this file lives)
├── CLAUDE.md                        ← you are here
├── 00-how-to-use.md                 ← human guide
├── 00-project-home.md               ← project overview + recent changes (created by pipeline)
├── 01-requirements-structured-v1.md ← structured requirements (created by pipeline)
├── 02-scope-and-context-v1.md       ← phasing, build order, risk (created by pipeline)
├── 03-product-backlog-v1.md         ← epics, stories, acceptance criteria (created by pipeline)
├── 04-speckit-specs/                ← one spec file per ready story (created by pipeline)
│   ├── 00-index.md
│   └── blocked-stories.md
├── 05-traceability-matrix.md        ← REQ → Story → Spec lookup (created by pipeline)
├── 06-change-log.md                 ← permanent change history (created by pipeline)
└── 00-pipeline-skills/              ← skill instructions — DO NOT MODIFY during a run
    ├── requirements-structuring/SKILL.md
    ├── scope-and-context/SKILL.md
    ├── product-backlog/SKILL.md
    ├── speckit-spec/SKILL.md
    └── change-management/SKILL.md
```

---

## ID scheme — memorise this

| Prefix | Meaning | Assigned in |
|--------|---------|-------------|
| `REQ-F-xxx` | Functional requirement | Step 1 |
| `REQ-N-xxx` | Non-functional requirement | Step 1 |
| `CON-xxx` | Constraint | Step 1 |
| `OQ-xxx` | Open question needing a stakeholder decision | Step 1 |
| `AS-xxx` | Assumption | Step 1 |
| `EPIC-x` | Epic | Step 3 |
| `US-xxx` | User story | Step 3 |
| `CHG-xxx` | Change record | Change management |

IDs are permanent once assigned. A changed requirement keeps its ID — only its content changes.

**Note on `SPIKE-xxx` / `ENABLER-xxx`:** these prefixes exist only in Phase 1 (the first pipeline run, single-team, multi-repo era). Since the team consolidated into one repo and moved to spec-driven development at pickup time, backlog work from Phase 2 onward does not use spikes or enablers, and does not split stories by repo — see the updated Step 3 and Step 4 below. Do not add new spikes/enablers to Phase 2+ backlog items; if something looks like it needs one, raise it as an `OQ-xxx` instead or write it as a plain user story.

---

## Trigger 1 — Run the pipeline

**When to activate:** The user attaches a PDF, pastes raw notes or a transcript, and asks to run the pipeline, fill the vault, structure the requirements, or anything equivalent.

**What to do — run these 7 steps in order. Do not skip steps or run them out of order.**

### Step 1 — Requirements structuring
1. Read `00-pipeline-skills/requirements-structuring/SKILL.md` fully
2. Read `00-pipeline-skills/requirements-structuring/assets/structured-requirements-template.md` for the exact output format
3. Run the skill on the user's input
4. Save output as `01-requirements-structured-v1.md`

### Step 2 — Scope and context
1. Read `00-pipeline-skills/scope-and-context/SKILL.md` fully
2. Read `00-pipeline-skills/scope-and-context/assets/scope-and-context-template.md`
3. Run the skill using `01-requirements-structured-v1.md` as input
4. Save output as `02-scope-and-context-v1.md`

### Step 3 — Product backlog
1. Read `00-pipeline-skills/product-backlog/SKILL.md` fully
2. Read `00-pipeline-skills/product-backlog/assets/product-backlog-template.md`
3. Run the skill using `02-scope-and-context-v1.md` and `01-requirements-structured-v1.md` as input
4. Save output as `03-product-backlog-v1.md`

**Phase 2 onward — format changes from Phase 1:**
- **No repo-tagging.** The team works out of one consolidated repo now. Do not group or tag stories by dispatcher-web / volunteer-app / backend-api. One flat backlog, organised by epic only.
- **No enablers, no spikes.** Write everything as a plain `US-xxx` user story. If a genuine unknown blocks a story, raise it as an `OQ-xxx` in the requirements doc (via change-management if requirements are already published) rather than writing a `SPIKE-xxx`.
- **Keep stories simple and purely functional.** Ground every story in what the requirements actually say. Do not add unrequested complexity (e.g. MFA, rate limiting, audit logging) unless a `REQ-F-xxx`/`REQ-N-xxx`/`CON-xxx` calls for it. When in doubt, leave it out and raise an OQ instead of gold-plating.
- Phase 1 stories already in `03-product-backlog-v1.md` keep their old repo-tagged/enabler format as historical record — don't rewrite them to match. Only new Phase 2+ stories use the new format.

### Step 4 — Speckit specs
1. Read `00-pipeline-skills/speckit-spec/SKILL.md` fully
2. Read `00-pipeline-skills/speckit-spec/assets/speckit-spec-template.md`
3. For every story marked Ready in the backlog: produce a spec file
4. For every story marked Not Ready: add an entry to `blocked-stories.md`
5. Save spec files to `04-speckit-specs/[epic-id]-[story-id]-[slug].md`
6. Save `04-speckit-specs/00-index.md` listing all spec files with wikilinks
7. Save `04-speckit-specs/blocked-stories.md`

Still generated automatically from Phase 2 onward, same as Phase 1 — the only Phase 2+ change is in Step 3 (no repo-tagging, no enablers/spikes). Specs continue to be produced per Ready story as before.

### Step 5 — Traceability matrix
Build `05-traceability-matrix.md` with five tables:
- **Functional Requirements → Story → Spec** (REQ-F-xxx | short description | Phase | Epic | Story | Spec)
- **Non-functional Requirements → Story/Enabler** (REQ-N-xxx | description | implemented in)
- **Constraints → Implementation** (CON-xxx | constraint | applied in)
- **Story → Requirements (reverse lookup)** (Story | requirement IDs covered | Spec)
- **Open Questions → What they block** (OQ-xxx | question short | blocks)

Where a spec file exists, link it with Obsidian wikilink format: `[[04-speckit-specs/filename|Spec]]`.

### Step 6 — Change log
Create `06-change-log.md`:

```markdown
# Change Log — [Project Name]

**Project:** [project name from brief]
**Pipeline initial run:** [today's date]
**Maintained by:** change-management skill

Changes are listed newest first. Each entry is permanent — never deleted or edited after creation.

---

*No changes yet.*

<!-- SKILL: insert new entries above this line, newest first -->
```

### Step 7 — Project home
Create `00-project-home.md` as a navigation hub containing:
- Project title, pipeline run date, status line
- A callout: `> **New here?** → [[00-how-to-use|How to use this vault]]`
- 2-3 sentence summary of what the project is (from the brief)
- Wikilinks to all pipeline documents with a one-line description of each
- A "Recent changes" section: `*No changes yet*` + `Full change history: [[06-change-log]]`
- A "Phase 1 blockers" table: the OQs that block Phase 1 stories
- Links to `[[05-traceability-matrix]]` and `[[00-pipeline-skills/00-skills-index]]`

Use Obsidian wikilink format throughout: `[[filename]]` or `[[filename|display text]]`. Filenames only — no full paths in wikilinks.

---

## Trigger 2 — Handle a change

**When to activate:** The user provides a block of text with a `CHG-ID:` field, or says a requirement changed, an open question was resolved, or asks to use change management.

**What to do:**
1. Read `00-pipeline-skills/change-management/SKILL.md` fully before touching any file
2. Read `00-pipeline-skills/change-management/assets/change-record-template.md`
3. Follow the skill instructions exactly

**The change record format the user will provide:**
```
CHG-ID:        CHG-xxx
Date:          YYYY-MM-DD
Triggered by:  [who / what meeting]
Change type:   [OQ resolved | Requirement modified | New requirement | Requirement removed]
Affected item: [REQ-F-xxx or OQ-xxx]
Old value:     [exact old text]
New value:     [exact new text]
Reason:        [one sentence]
Resolves OQ:   [OQ-xxx or —]
Notes:         [anything extra]
```

If the change record is incomplete or ambiguous, stop and ask before touching any file.

---

## Rules that apply to everything

**Never invent scope.** If the brief doesn't say it, it is not a requirement. Gaps go in Open Questions, not in requirements.

**Preserve history.** Once an ID is assigned, it stays forever. Changed content keeps its ID. Removed content is struck through (`~~like this~~`), never deleted.

**Read before writing.** When editing an existing vault document, always read the current file first, then make surgical edits. Never overwrite a document from scratch if it already has content.

**Wikilinks, not paths.** Internal document references use `[[filename]]` format so Obsidian renders them as clickable links.

**Traceability chain:** `REQ-F-xxx` -> `US-xxx` -> spec file. Every story traces to at least one requirement ID. Every spec traces to a story.

**When in doubt, raise an OQ.** Never invent an answer to fill a gap. Open questions drive the right stakeholder conversations before build.
