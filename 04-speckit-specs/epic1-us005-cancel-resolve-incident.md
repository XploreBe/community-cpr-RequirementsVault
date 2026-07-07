# Cancel / resolve incident

**Story:** US-005 — Cancel / resolve incident
**Epic:** EPIC-1 — Incident record management (dispatcher-web)
**Traces to:** REQ-F-011, REQ-F-010 (simplified)
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

Once a situation is over — EMS arrived, or the incident turns out to be a false alarm — a dispatcher needs a fast, unambiguous way to close it out so it stops cluttering the active view. This feature lets a dispatcher mark an incident resolved or cancelled.

---

## User scenarios

### Scenario 1 — Resolve an active incident
Given an incident with status "open" or "in progress," when the dispatcher marks it "resolved," then its status updates and it no longer appears in the default active list (still reachable via detail/search).

### Scenario 2 — Cancel an active incident
Given an incident with status "open" or "in progress," when the dispatcher marks it "cancelled," then its status updates and it no longer appears in the default active list.

### Scenario 3 — Closing an already-closed incident is a no-op
Given an incident already "resolved" or "cancelled," when the dispatcher repeats the close action, then no further change is recorded and the current closed state is shown as-is (idempotent).

### Scenario 4 — Active set definition
The "active set" shown by default (e.g. in US-002's list/map) consists of incidents with status "open" or "in progress" only.

---

## Constraints and assumptions

- This story reuses the same status field as US-004; it's a guided shortcut to two of its four possible values, with its own explicit action/confirmation rather than the general edit form.
- Mocked/local data source, no auth.
- Built in Next.js (CON-002).

---

## Out of scope

- Notifying any volunteers of the stand-down — no volunteers are attached to incidents in Phase 1 (Phase 2 — REQ-F-011's full "stand down responders" behaviour).
- Reopening a closed incident — not requested; if needed, treat as a new story rather than assuming it belongs here.

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- Closing an incident must be idempotent — repeating the action on an already-closed incident is never an error.
