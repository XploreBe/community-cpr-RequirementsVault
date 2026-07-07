# Example 3 — Mode C (ambiguous question, asked by an agent)

## Incoming GitHub Issue

**Title:** What's the sync timeout?

**Body:**
> (opened programmatically by test-agent-07 while preparing a test case)
> Need the timeout value for the sync job before I can write the assertion.

## Vault excerpt found

`REQ-N-002` (02-scope-and-context-v1.md): FCM push notification delivery, 5-second SLA.
`REQ-N-009` (02-scope-and-context-v1.md): offline response sync retry interval, 30-second backoff.

Both are plausibly "the sync job" — nothing in the question narrows it down, and the two values
are different enough that guessing wrong would produce a wrong test assertion.

## Skill output

```json
{
  "mode": "needs_clarification",
  "answer": "This could refer to two different things in the vault, and they have different values, so I don't want to guess:\n\n1. **REQ-N-002** — FCM push notification delivery SLA: 5 seconds.\n2. **REQ-N-009** — offline response sync retry backoff: 30 seconds.\n\nWhich one is 'the sync job' in this context? If it's about volunteers receiving dispatch notifications, it's REQ-N-002. If it's about a volunteer's offline responses being retried until they reconnect, it's REQ-N-009.",
  "chg_proposal": null
}
```

## What the calling script does with this

Posts the comment with `STATUS: needs_clarification` prepended. An agent reading this via the
GitHub API can match on that literal string and pause its task (e.g. flag the test case as
blocked) instead of picking one of the two numbers at random to keep moving.
