# CPR/AED reference

**Story:** US-105 — CPR/AED reference
**Epic:** EPIC-2 — Alert response walking skeleton (volunteer-app)
**Traces to:** REQ-F-027
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

In the middle of an emergency, a volunteer may need a quick refresher on technique. This feature gives them static CPR/AED guidance inside the app, available at any time — not just during an active alert.

---

## User scenarios

### Scenario 1 — Access the reference
Given the app is open, when the volunteer navigates to the reference section, then static CPR/AED guidance content is shown.

### Scenario 2 — Available without an active alert
The reference section is reachable at any time, not gated behind having an active or accepted alert.

### Scenario 3 — Works offline
Given the device is offline, when the volunteer opens the reference section, then the content still loads, because it is bundled with the app rather than fetched from a server. This matters specifically because the brief frames this feature as "for use during a live event," when connectivity can't be assumed.

---

## Constraints and assumptions

- Content is static and bundled with the app build in Phase 1 — no backend/CMS integration (REQ-F-039, admin content management, is Phase 2).
- Android-only, React Native (CON-001).

---

## Out of scope

- Admin tools to edit this content (Phase 2 — REQ-F-039).
- Localised/translated content per country (Phase 2 — REQ-N-012, portability).

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- This content must load without a network connection — do not introduce a server fetch for it in Phase 1.
