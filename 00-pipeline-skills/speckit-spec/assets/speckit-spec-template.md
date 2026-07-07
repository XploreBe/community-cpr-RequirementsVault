<!--
Spec Kit spec file — output template.
One file per story. Keep it focused: one to two pages.
This file feeds into /speckit.plan → /speckit.tasks → /speckit.implement.
Delete these comments in the final file.

File naming: specs/[epic-id]-[story-id]-[short-slug].md
-->

# [Short feature name]

**Story:** [US-xxx] — [story title]
**Epic:** [EPIC-x] — [epic title]
**Traces to:** [REQ-IDs]
**Date:** [YYYY-MM-DD]
**Produced by:** speckit-spec skill

---

## Overview

[One paragraph: what this feature is, who it's for, and why it exists. Written from the user's perspective, not the system's. Drawn from the story's role, capability, and benefit clause. No technical detail here.]

---

## User scenarios

[Translate each AC criterion into a scenario. Include ALL scenarios — happy path, negative, edge cases. Do not drop edge cases for brevity. Use Given/When/Then where it adds clarity; plain prose rules where the criterion is a simple invariant.]

### Scenario 1 — [short title]
[Given/When/Then or plain prose rule]

### Scenario 2 — [short title]
[...]

### Scenario N — [edge/negative case title]
[...]

---

## Constraints and assumptions

[Hard limits the implementation must respect. Keep each short and actionable.]

- [CON-xxx / scope constraint / assumption] — [what it means for implementation]
- [If provisional: "Provisional assumption (to confirm): ..."]

---

## Out of scope

[What this spec explicitly does not cover. Protects the developer from scope creep.]

- [deferred item / item sent back / explicit exclusion]

**Unresolved — dev should not implement until confirmed:**
- [open question] — [which scenario / constraint it affects]

---

## Constitution snippet

[Two to five governing principles to add to /speckit.constitution for this feature. Drawn from non-functional requirements and constraints. Add only what is new — do not repeat principles already in the project constitution.]

- [principle]
- [principle]
