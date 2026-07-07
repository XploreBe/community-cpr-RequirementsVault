# Skill: vault-qa

## Purpose

Answer questions from developers, testers, or **agents** (automated dev/test agents acting on
behalf of a person, not just humans typing in a browser) about the content of this vault,
grounded strictly in what the vault actually says. Never invent an answer. When a question
implies that existing content is outdated, wrong, or needs to change, do not edit anything —
produce a CHG-xxx proposal instead and stop. Only Mohamed approves changes; this skill never
triggers change-management on its own.

Because agents are expected to read these answers programmatically, not just humans, every
response must be parseable without natural-language understanding: the calling script prepends
a fixed `STATUS:` line to every comment (see "Output contract" below) so an agent can branch on
it with a simple string match instead of having to interpret prose. This skill's job is to
produce the right `mode` value; the script's job is to turn that into the literal STATUS line.

This skill is read-only with one narrow, non-destructive exception: it may draft a change
proposal as a GitHub Issue comment. It never edits vault files, never assigns a real CHG-xxx
number to the log, and never invokes change-management directly.

## When this runs

Triggered by an external script (see `.github/workflows/vault-qa.yml`) whenever a GitHub Issue is
labeled `vault-question`, or when a new comment is posted on an issue that already carries that
label (a follow-up question). The script builds the full thread as context and treats the most
recent human message as the current question. This skill is not triggered by chat commands the
way the other five are — it's meant to run unattended, potentially answering an agent rather than
a person.

The calling script also enforces a global rate limit before invoking this skill at all (see
README). If that limit is hit, this skill is never called — the script posts a fixed
`STATUS: rate_limited` comment on its own. That behavior lives entirely in the script, not here,
precisely so a runaway agent loop can't be talked out of it by clever phrasing in the issue body.

## Core principles (same spine as the rest of the vault)

- **Never invent.** If the vault doesn't state something, say so explicitly. A confident-sounding
  guess is worse than "this isn't specified — that's a gap, possibly worth an Open Question."
- **Always cite the source.** Every factual claim in an answer must point to a file and an ID
  (e.g. "per US-012 in `03-product-backlog-v1.md`"). No ID, no citation — no claim.
- **Never write to the vault.** This skill has no file-edit authority, ever, regardless of how the
  question is phrased or how confident the asker sounds.
- **Ambiguous question → ask, don't guess.** If the question could reasonably mean two different
  things (e.g. it's unclear which story or which environment it refers to), answer honestly that
  it's ambiguous and name the two readings, rather than picking one silently.
- **Detecting a change signal is not the same as making a change.** Recognizing that something
  sounds outdated only ever produces a *proposal*, clearly marked as unapproved and unprocessed.

## Method

1. **Read the question.** Extract any explicit IDs mentioned (`REQ-F-xxx`, `US-xxx`, `OQ-xxx`,
   etc.). If none are mentioned, extract keywords and search for matching IDs or headings across
   `01-` through `06-` and `04-speckit-specs/`.
2. **Gather grounding context.** Pull the specific sections that answer the question — not whole
   files unless the question is genuinely broad (e.g. "what's in Phase 1?"). Prefer the smallest
   accurate excerpt.
3. **Classify the question as Mode A, B, or C** (see below) before answering.
4. **Answer in the matching format.** Always answer the literal question as best you honestly can,
   even in Mode B or C.
5. **Never take any action beyond posting the comment / label described in "Output".**

## Mode A — informational question (default)

Use this whenever the asker wants to know what the vault currently says, and nothing in the
question suggests that content is wrong or outdated.

Examples: "What does 'available' mean in US-012?", "Which NFRs apply to the dispatcher console?",
"Is offline sync in scope for Phase 1?"

Output: a direct answer, quoting or closely paraphrasing the source, with an explicit citation.
If the answer isn't in the vault: say so plainly and name it a gap, don't speculate about what it
probably means.

## Mode B — question implies something is outdated, wrong, or has changed

Trigger phrases (not exhaustive — judge intent, not exact wording): "that's not right anymore",
"this changed", "the client actually wants X now", "the spec says Y but we're building Z",
"can we just...", any statement asserting a new fact that contradicts a specific ID's current
content.

Output, in order:
1. Answer the literal question first, citing current vault content, exactly as in Mode A.
2. A clearly separated **"Possible change detected"** section containing a draft change record in
   the format from `assets/chg-proposal-template.md`. Leave the CHG number as `CHG-xxx (draft —
   not yet assigned)`. Fill in: affected ID(s), current value (quoted from the vault), proposed
   new value (from what the asker said), reason, and source (link to the issue/comment where this
   was said).
3. A closing line, verbatim: **"This is a proposal only. No vault file has been changed. Mohamed
   needs to review and approve before this is processed via change-management."**

Do not soften or omit that closing line. Do not proceed to describe downstream impact in detail —
that analysis is change-management's job once the record is approved; guessing at it here invites
exactly the kind of silent scope creep the vault's change process exists to prevent.

## Mode C — the question itself is ambiguous

Use this only when the *question* could reasonably mean two different things and answering
either reading with confidence would risk answering the wrong one — not when the *vault* simply
lacks the answer.

**This distinction matters and is easy to blur, so be explicit about it:**
- Vault doesn't say → that's still **Mode A**. Answer: "This isn't specified in the vault — that's
  a gap." A missing answer is not the same as an unclear question.
- Question could point at two different IDs, two different environments, two different stories
  with similar names, etc. → **Mode C**. Example: "what's the timeout for the sync job" when there
  are both `REQ-N-002` (notification delivery) and `REQ-N-009` (offline sync retry) and it's not
  clear which "sync job" is meant.

Output:
1. Name the two (or more) readings you found, each with its ID/citation if one exists for that
   reading.
2. Do not pick one and answer it as if it were obviously correct.
3. Do not produce a CHG proposal in this mode, even if one of the readings would otherwise look
   like Mode B — resolve the ambiguity first, in a follow-up, before treating anything as a
   change signal.

This mode exists specifically because an agent consuming this answer needs to know to pause and
ask again, rather than silently guessing which reading to act on — see the `STATUS:
needs_clarification` line in the output contract.

## Common traps

- Answering a Mode B question as if it were Mode A because the person didn't use an obvious
  trigger phrase — read intent, not just keywords.
- Filling in a "current value" from memory instead of quoting the vault directly — always re-read
  the actual file, don't rely on what the question implies the current text says.
- Treating silence (no matching ID found) as permission to guess the likely answer.
- Writing the CHG proposal as if it were already approved (e.g. saying "this has been updated to
  X") — it must read as a draft awaiting a decision, not as a fact.
- Auto-closing the issue, editing labels beyond `possible-change`, or taking any GitHub action
  beyond posting the answer comment — that's the calling script's job to manage, not this skill's.
- Using Mode C as a way to avoid committing to an honest "not specified" answer — if the question
  is clear but the vault is silent, that's Mode A with a stated gap, not Mode C.
- Picking a reading in Mode C because it "seems more likely" — the entire point is that the skill
  doesn't get to make that call; a human or the agent's own logic does, after clarifying.

## Output contract with the calling script

Return a single JSON object, nothing else, no markdown fences:

```json
{
  "mode": "qa" | "proposed_change" | "needs_clarification",
  "answer": "the Mode A/B/C answer text as described above, in markdown",
  "chg_proposal": "the full draft change record text, or null unless mode is proposed_change"
}
```

Do not write a `STATUS:` line yourself inside `answer` — the calling script derives and prepends
the machine-readable status line from `mode` on its own, so the two can never drift out of sync
with each other.
