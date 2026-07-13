# Full dispatch audit trail

**Story:** US-209 — Full dispatch audit trail
**Epic:** EPIC-5 — Volunteer matching & alerting
**Traces to:** REQ-F-012 (full)
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

After (or during) a dispatch, the team needs a complete, reviewable record of what happened — who was notified, when, and what the outcome was — for accountability and after-action review.

---

## User scenarios

### Scenario 1 — Full chronological record
Given an incident has been through any dispatch activity, when the audit trail is viewed, then it shows who was notified, when, who responded and how, and the final outcome, in chronological order.

### Scenario 2 — Live incident (edge case)
Given an incident is still open, when the audit trail is viewed, then it reflects events up to the current moment, not just a post-closure summary.

### Scenario 3 — No activity yet (edge case)
Given an incident has just been created with no dispatch activity yet, when the audit trail is viewed, then it shows only the creation event, not an empty or broken screen.

---

## Constraints and assumptions

- Requires US-205 (send alert) — the trail records events starting from alert send onward, building on the incident-creation record already in Phase 1's US-003.
- This is distinct from REQ-N-008's security audit logging (logins, role changes, admin actions) — this trail is specifically the per-incident dispatch record.

---

## Out of scope

- Security/admin action logging (logins, role changes, cert verification) — tracked separately under REQ-N-008 in 03-product-backlog-v1.md's NFR table, not part of this story.
- Automatic deletion of patient location data after a retention period — see Unresolved.

**Unresolved:**
- OQ-009 (precise retention period for patient location data once an incident is closed) — REQ-N-010 requires location data isn't kept longer than necessary, but the exact period isn't defined. Build the audit trail itself now; do not implement an automatic-deletion job against a guessed number.

---

## Constitution snippet

- Append-only event log for the audit trail — never overwrite or delete a past entry, even when an incident is closed.
