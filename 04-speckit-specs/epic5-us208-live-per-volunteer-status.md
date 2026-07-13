# Live per-volunteer status view

**Story:** US-208 — Live per-volunteer status view
**Epic:** EPIC-5 — Volunteer matching & alerting
**Traces to:** REQ-F-010 (full)
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

A dispatcher managing a live incident needs to know exactly where each notified volunteer stands, without having to ask, so they can judge whether the response is on track.

---

## User scenarios

### Scenario 1 — Status per volunteer
Given an incident has notified volunteers, when the dispatcher views it, then each volunteer shows one of: notified, accepted, declined, en route, arrived, stood down.

### Scenario 2 — Live update, no manual refresh
Given a volunteer's status changes, when it changes, then the dispatcher's view updates live (via the WebSocket channel, CON-005), without the dispatcher needing to refresh the page.

### Scenario 3 — No notified volunteers yet (edge case)
Given no volunteers have been notified for this incident yet, when the dispatcher views it, then a neutral "no responders notified yet" state is shown instead of an empty table.

---

## Constraints and assumptions

- Requires US-205 (send alert) — this view only has data once an alert has gone out.
- Live updates use the REST + WebSocket integration already fixed for dispatcher-web (CON-005).

---

## Out of scope

- Whether a volunteer can back out after already accepting (as opposed to declining before accepting) — see Unresolved.

**Unresolved:**
- OQ-013 (can a volunteer back out after accepting, and if so does the dispatcher get notified / does the pool widen again) — carried over from Phase 1's US-103 spec, still open. Do not build "back out" handling; if this status view needs to reflect it, that's a follow-up once OQ-013 is answered.

---

## Constitution snippet

- Drive this view from the same live event stream that feeds the audit trail (US-209), rather than maintaining two separate sources of truth for what happened during a dispatch.
