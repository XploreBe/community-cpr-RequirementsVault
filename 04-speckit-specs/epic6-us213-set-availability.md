# Set availability

**Story:** US-213 — Set availability
**Epic:** EPIC-6 — Certification, availability & privacy
**Traces to:** REQ-F-019
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

A volunteer isn't available around the clock, so they need a way to tell the system when they can and can't be alerted.

---

## User scenarios

### Scenario 1 — Set always on
Given the volunteer opens availability settings, when they select "always on," then the selection is saved and takes effect immediately.

### Scenario 2 — Set scheduled availability
Given the volunteer opens availability settings, when they select "scheduled" and provide a time range, then the selection is saved and the volunteer is only considered available within that range.

### Scenario 3 — Set do-not-disturb
Given the volunteer opens availability settings, when they select "do-not-disturb," then the selection is saved and takes effect immediately.

### Scenario 4 — Do-not-disturb excludes from search
Given a volunteer is set to "do-not-disturb," when a nearby-volunteer search runs (US-204), then they are excluded from the results.

---

## Constraints and assumptions

- Android-only, React Native (CON-001).
- Interacts directly with US-204's exclusion logic — the two must use the same availability state.

---

## Out of scope

- Automatic switching between scheduled windows without volunteer action beyond the initial schedule set-up — not requested anywhere upstream.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Availability state must be the single source of truth consulted by the nearby-volunteer search (US-204) — no separate, potentially inconsistent copy of this state.
