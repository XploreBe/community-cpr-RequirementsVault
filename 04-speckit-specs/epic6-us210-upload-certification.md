# Upload certification documentation

**Story:** US-210 — Upload certification documentation
**Epic:** EPIC-6 — Certification, availability & privacy
**Traces to:** REQ-F-016
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — not part of the current Phase 2 round (tiered alerting works off self-declared tier from Phase 1 for now). Kept as-is, ready to pick up later.

---

## Overview

A volunteer's claimed training tier needs to be backed by real proof, so the system lets them upload their certification for later verification.

---

## User scenarios

### Scenario 1 — Successful upload
Given the volunteer is signed up, when they upload a certification document (image or PDF), then it is stored against their account with status "pending verification."

### Scenario 2 — Unsupported file type (negative)
Given the volunteer attempts to upload an unsupported file type, when they try, then the upload is rejected with a message stating the supported formats.

### Scenario 3 — Re-upload replaces pending certification (edge case)
Given a volunteer already has a certification with status "pending verification," when they upload a new document before the first is reviewed, then the new upload replaces the pending one rather than creating a duplicate pending record.

---

## Constraints and assumptions

- Android-only, React Native (CON-001).
- Verification itself is a separate story (US-223) — this story only covers the upload and pending state.

---

## Out of scope

- Reviewing/approving the certification — US-223.
- What happens if a certification later expires — US-211.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Store the original uploaded document, not just a "verified: yes/no" flag, so an admin can review the actual evidence in US-223.
