# Update incident

**Story:** US-004 — Update incident
**Epic:** EPIC-1 — Incident record management (dispatcher-web)
**Traces to:** REQ-F-005, REQ-F-010 (simplified)
**Date:** 2026-07-06
**Produced by:** speckit-spec skill
**Last updated:** 2026-07-09 (CHG-002)

---

## Overview

Details often change after an incident is first logged — the notes get more precise, the pin needs correcting, or the situation moves forward. This feature lets a dispatcher edit any field on an existing incident, including its status, so the record always reflects reality.

---

## User scenarios

### Scenario 1 — Edit general fields
Given an existing incident, when the dispatcher edits its type, notes, country, or location and saves, then the incident reflects the new values and its updated timestamp changes.

### Scenario 2 — Change status
Given an existing incident, when the dispatcher sets its status to "open," "in progress," or "resolved," then the new status is saved and reflected wherever the incident is shown (list, map, detail).

### Scenario 3 — Status transitions are not enforced (assumption, to confirm)
Given an existing incident, when the dispatcher sets its status to any of the four values (open / in progress / resolved / cancelled) regardless of the current value, then the change is accepted. Phase 1 does not enforce a sequential open → in progress → resolved order. This is a stated assumption, not a confirmed decision — flag to the BA if strict workflow enforcement turns out to be required.

### Scenario 4 — Location cannot be cleared (negative)
Given an existing incident, when the dispatcher edits it so that it would end up with no location, then the save is rejected with the same "location is required" message used at creation (US-001).

### Scenario 5 — Out-of-range coordinates rejected on edit (negative) [CHG-002]
Given an existing incident, when the dispatcher edits its location to a latitude outside [-90, 90] or a longitude outside [-180, 180] and saves, then the save is rejected and a validation message states the coordinates are out of range — same range rule as US-001.

---

## Constraints and assumptions

- Mocked/local data source, no auth (same as the rest of EPIC-1).
- Provisional assumption (to confirm): status transitions are unrestricted in Phase 1 — see Scenario 3.
- Built in Next.js (CON-002).

---

## Out of scope

- Cancel/resolve as a distinct guided action with its own confirmation — that's epic1-us005-cancel-resolve-incident.md; this story is the general-purpose edit form, which happens to include status as one of the editable fields.
- Any volunteer-facing effect of a status change (Phase 2 — no volunteers are attached to incidents yet in Phase 1).

**Unresolved — dev should not implement until confirmed:**
- Whether status transitions must be sequential — see Scenario 3. Currently implemented as unrestricted; do not add extra validation logic for this without confirming with the BA first, to avoid guessing at a rule nobody has stated.

---

## Constitution snippet

- The shared location rule applies uniformly to create and edit — implement it once, shared, not duplicated per form. The rule covers both presence (not null/empty) and valid range (latitude ∈ [-90, 90], longitude ∈ [-180, 180]). [CHG-002]
