# Admin manages in-app reference content

**Story:** US-224 — Admin manages in-app reference content
**Epic:** EPIC-8 — Country portability & admin tools
**Traces to:** REQ-F-039
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

The in-app CPR/AED guidance shouldn't need an app release every time the wording needs an update, so an admin can edit it directly.

---

## User scenarios

### Scenario 1 — Update content
Given the admin opens content management, when they edit the CPR/AED reference text, then the updated content is what volunteers see in the app's reference section (Phase 1's US-105) without an app update.

### Scenario 2 — Invalid/empty save rejected (negative)
Given the admin attempts to save empty or invalid content, when they try, then the save is rejected and the previous content remains live.

---

## Constraints and assumptions

- Admin-only (least-privilege, REQ-N-007).
- Extends Phase 1's US-105, which used static bundled content — this story replaces that with admin-editable content.

---

## Out of scope

- Multi-language content management beyond what US-220's language configuration already covers — not requested as a distinct capability here.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Content changes should apply without requiring a new app release — this is the whole point of moving off Phase 1's bundled-static approach.
