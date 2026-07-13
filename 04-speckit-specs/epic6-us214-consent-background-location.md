# Give consent for background location collection

**Story:** US-214 — Give consent for background location collection
**Epic:** EPIC-6 — Certification, availability & privacy
**Traces to:** REQ-F-020, REQ-F-023, REQ-N-011
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — continuous background-location tracking is real infrastructure, not needed for the simple core loop. US-204's nearby search uses each volunteer's registered/last-known location in the meantime. Kept as-is, ready to pick up later.

---

## Overview

Tracking a volunteer's location is sensitive, so the app asks explicitly before collecting it and gives the volunteer real control over that choice.

---

## User scenarios

### Scenario 1 — Consent granted
Given the volunteer is asked for background-location consent, when they grant it, then a consent record is stored with a timestamp and location collection begins only from that point onward.

### Scenario 2 — Consent declined
Given the volunteer declines consent, when they do, then no background location is collected, and the app states this may limit how they're matched to nearby incidents.

### Scenario 3 — Consent withdrawn later (edge case)
Given a volunteer previously granted consent, when they withdraw it in settings, then background location collection stops from that point and the withdrawal is recorded with a timestamp, same as the original grant.

### Scenario 4 — Location only while relevant
Location is collected only while an incident/event is active for that volunteer, or with their explicit opt-in otherwise — never silently in the background outside those cases.

---

## Constraints and assumptions

- Android-only, React Native (CON-001).
- Consent record must include a timestamp for both grant and any later withdrawal (REQ-F-023).

---

## Out of scope

- The specific sampling interval or battery-drain budget for background tracking — see Unresolved.

**Unresolved:**
- None blocking. OQ-008 resolved [CHG-015]: no concrete number — "reasonable battery use, no aggressive constant GPS polling," left to the dev team's discretion.

---

## Constitution snippet

- Every consent grant and withdrawal is an immutable, timestamped record — never overwritten, so the system can always show what was consented to and when.
- Default to no background collection until consent is explicitly granted — never opt a volunteer in silently.
