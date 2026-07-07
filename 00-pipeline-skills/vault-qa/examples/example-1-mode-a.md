# Example 1 — Mode A (informational question)

## Incoming GitHub Issue

**Title:** What counts as "nearby" in US-014?

**Body:**
> The AC says "nearby available volunteers" get notified first. Is there an actual distance
> defined anywhere, or do we just pick something on the dev side?

## Vault excerpt found (03-product-backlog-v1.md, US-014)

> AC-2: Given a new dispatch request, when no volunteer within the defined radius has responded
> within 90 seconds, then the system escalates to the next radius tier. [Radius value: OQ-021 —
> not yet confirmed by ops]

## Skill output

```json
{
  "mode": "qa",
  "answer": "There's no fixed distance defined yet. Per US-014 (03-product-backlog-v1.md), AC-2 references a radius tier but the actual value is tracked as OQ-021, which is still open — 'not yet confirmed by ops'. So this isn't a dev-side decision to make freely; it needs to go back to ops via OQ-021 before it's picked. Worth flagging to Mohamed that this is blocking implementation of AC-2.",
  "chg_proposal": null
}
```

Why this is Mode A: the question asks what the vault says, and the honest answer is "it doesn't
say yet — here's the open question tracking it." No content was claimed to be wrong or outdated,
so no change proposal is generated. Note that the answer still surfaces the blocker rather than
inventing a plausible-sounding radius (e.g. "probably 5km") to be helpful.
