# Example 2 — Mode B (implied change)

## Incoming GitHub Issue

**Title:** Notification SLA — client changed their mind?

**Body:**
> Talked to the client yesterday, they said 5 seconds for the FCM push is way too aggressive for
> the rural regions with bad connectivity, they're fine with 15 seconds there. Can we just bump
> the number in the spec?

## Vault excerpt found (02-scope-and-context-v1.md, constraint C-003; referenced in REQ-N-002)

> REQ-N-002: The system must deliver an FCM push notification to eligible volunteers within 5
> seconds of dispatch creation, under normal network conditions.

## Skill output

```json
{
  "mode": "proposed_change",
  "answer": "Currently, REQ-N-002 (02-scope-and-context-v1.md) specifies a 5-second FCM delivery SLA under normal network conditions — there's no separate threshold for low-connectivity/rural regions. So no, there's currently no distinction in the vault between region types for this SLA.",
  "chg_proposal": "# Draft Change Proposal — CHG-xxx (draft — not yet assigned)\n\n**Status:** Awaiting approval\n\n**Affected ID(s):** REQ-N-002\n\n**Current value (quoted from vault):**\n> The system must deliver an FCM push notification to eligible volunteers within 5 seconds of dispatch creation, under normal network conditions.\n\n**Proposed new value:**\n> Deliver within 5 seconds under normal network conditions; within 15 seconds for rural/low-connectivity regions (region distinction not yet defined in the vault).\n\n**Reason given:**\nClient told the reporting dev that 5 seconds is too aggressive for rural regions with poor connectivity and agreed to 15 seconds there.\n\n**Source:**\nGitHub Issue #47, reported by @devuser, relaying a verbal conversation with the client (not yet independently confirmed in writing).\n\n**Requested by:** devuser\n\n---\n\n**Next step:** If this looks right, approve it and hand it to the change-management skill as a normal CHG record. If it's wrong, incomplete, or premature, reply on the issue to say so — nothing happens to the vault either way until this is explicitly approved."
}
```

Why this is Mode B: the asker asserts a new fact ("client said 15s is fine for rural") that
contradicts an existing requirement, and asks to act on it directly ("can we just bump the
number"). The skill answers the literal question, then drafts a proposal — it does **not** edit
REQ-N-002, does not confirm the change happened, and explicitly flags that the client's comment
was relayed verbally rather than confirmed in writing, which is exactly the kind of detail
Mohamed needs before approving.
