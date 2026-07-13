# View volunteer status and certification history (admin)

**Story:** US-215 — View volunteer status and certification history (admin)
**Epic:** EPIC-6 — Certification, availability & privacy
**Traces to:** REQ-F-035 (full)
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

An admin sometimes needs to understand not just where a volunteer stands today, but how they got there, so they can review changes to tier, status, or certification over time.

---

## User scenarios

### Scenario 1 — History shown
Given a volunteer has had tier, status, or certification changes over time, when an admin opens their profile, then a chronological history of those changes is shown, not just the current values.

### Scenario 2 — New volunteer, no history yet (edge case)
Given a volunteer has no history yet beyond signing up, when an admin views their profile, then the history shows only the sign-up event.

---

## Constraints and assumptions

- Extends Phase 1's ENABLER-003 (read-only volunteer endpoint, no history) — this story is the Phase 2 upgrade adding the history dimension.
- Admin-only view (least-privilege, REQ-N-007).

---

## Out of scope

- Editing history entries — this is a read-only view of what already happened.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Store volunteer status/tier/certification changes as an append-only history log, not just overwritten current-state fields, so this view has real data to show.
