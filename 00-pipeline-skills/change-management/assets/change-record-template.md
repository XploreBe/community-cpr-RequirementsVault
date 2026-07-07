# Change Record Template

Copy this block and fill it in. Paste it into the chat to trigger the change-management skill.
Every field is required. Use "—" only for "Resolves OQ" if the change does not resolve an open question.

---

```
CHG-ID:        CHG-[next number — leave blank, the skill assigns it]
Date:          YYYY-MM-DD
Triggered by:  [name of stakeholder / meeting title / decision reference]
Change type:   [pick one: Requirement modified | New requirement | Requirement removed | Priority change | OQ resolved | Scope change | Story modified]
Affected item: [REQ-F-xxx / REQ-N-xxx / OQ-xxx / US-xxx / CON-xxx — use the exact ID from the documents]
Old value:     [copy the exact current text, or "none" if this is a new item]
New value:     [the new text exactly as it should read, or "removed" if deleting]
Reason:        [one or two sentences — why this changed]
Resolves OQ:   [OQ-xxx if this answers an open question, else "—"]
Notes:         [anything else relevant — context, related items to check, follow-up concerns]
```

---

## Examples

### Example 1 — Resolving an open question (OQ-004)
```
CHG-ID:        CHG-001
Date:          2026-07-01
Triggered by:  Stakeholder call with EMS partners — product owner decision
Change type:   OQ resolved
Affected item: OQ-004
Old value:     N-seconds escalation timeout — unresolved
New value:     30 seconds for first tier, 60 seconds for second tier, both configurable per country
Reason:        EMS partners confirmed 30 seconds is sufficient for certified volunteers to respond; 60 seconds before widening to untrained bystanders aligns with international CPR dispatch protocols.
Resolves OQ:   OQ-004
Notes:         Also check OQ-013 — the meeting touched on tier ordering but no decision was made yet.
```

### Example 2 — Modifying an acceptance criterion
```
CHG-ID:        CHG-002
Date:          2026-07-05
Triggered by:  UX review session — volunteer app team
Change type:   Requirement modified
Affected item: REQ-F-021
Old value:     The volunteer shall be able to accept or decline an alert with a single tap.
New value:     The volunteer shall be able to accept or decline an alert with a single tap. If the volunteer does not respond within 20 seconds of the notification appearing on screen, the app shall auto-display a "Still available?" prompt before the system marks them as No Response.
Reason:        User testing showed volunteers sometimes miss the notification but are still available. The 20-second prompt reduces false No Response statuses.
Resolves OQ:   —
Notes:         This adds a new AC to US-013 and a new scenario to its spec. Also check US-009 (live status view) — dispatcher sees No Response status, timing now has a defined 20-second window.
```

### Example 3 — New requirement added
```
CHG-ID:        CHG-003
Date:          2026-07-10
Triggered by:  Legal review — GDPR counsel
Change type:   New requirement
Affected item: none (new)
Old value:     none
New value:     The system shall provide a volunteer with the ability to request deletion of their personal data, with the request fulfilled within 30 days, subject to retention obligations for active audit log entries.
Reason:        GDPR Article 17 right to erasure. Legal review flagged this as mandatory for EU deployment.
Resolves OQ:   OQ-020 (partially)
Notes:         This likely needs a new REQ-F (after REQ-F-036). Does not block any current story but must be planned into Phase 2.
```
