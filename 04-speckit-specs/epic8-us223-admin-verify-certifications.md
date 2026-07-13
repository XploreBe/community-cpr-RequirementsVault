# Admin verifies volunteer certifications

**Story:** US-223 — Admin verifies volunteer certifications
**Epic:** EPIC-8 — Country portability & admin tools
**Traces to:** REQ-F-038
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

A volunteer's uploaded certification is just a claim until someone checks it, so an admin reviews and formally approves or rejects it.

---

## User scenarios

### Scenario 1 — Approve a certification
Given a volunteer has uploaded a certification with status "pending verification" (US-210), when the admin reviews it and approves, then it's marked "verified."

### Scenario 2 — Reject a certification
Given a volunteer has uploaded a certification with status "pending verification," when the admin reviews it and rejects it, then it's marked "rejected" with an optional reason, and the volunteer is notified to re-upload.

### Scenario 3 — Verified certification updates tier status
Given a certification is marked "verified" and the volunteer's declared tier depends on it, when verification completes, then the volunteer's tier status reflects "verified" rather than "pending."

---

## Constraints and assumptions

- Requires US-210 (upload) — nothing to verify until a certification exists.
- Admin-only (least-privilege, REQ-N-007).

---

## Out of scope

- The upload flow itself — US-210.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Store the verification decision (approved/rejected) with the admin's identity and timestamp, feeding into the volunteer's history view (US-215) and the security audit log (REQ-N-008).
