# Basic volunteer read endpoint

**Story:** ENABLER-003 — Basic volunteer read endpoint
**Epic:** EPIC-3 — API & module scaffold (backend-api)
**Traces to:** REQ-F-035 (partial)
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

This enabler gives the Volunteers + Accounts module a minimal, real, read-only endpoint listing volunteers, so dispatcher-web's volunteer view (US-006) and future volunteer-app sign-up work have real data to eventually integrate with, instead of only a mock.

---

## User scenarios

Framed at the API level:

### Scenario 1 — List volunteers
Given registered volunteers exist in the datastore, when a client requests the list, then each volunteer's name, tier, and status are returned.

### Scenario 2 — Empty list
Given no volunteers exist, when a client requests the list, then an empty list is returned (not an error).

### Scenario 3 — Read-only
This endpoint is read-only in Phase 1 — no create/update/delete operations are exposed here. Sign-up persistence (US-101) is still a volunteer-app-local mock in Phase 1, not wired to this endpoint yet.

---

## Constraints and assumptions

- No authentication on this endpoint in Phase 1.
- Fields returned are limited to name, tier, and status — no location, no availability, no certification detail (matches US-006's Phase 1 scope exactly).
- Lives inside the Volunteers + Accounts module scaffolded by ENABLER-001.

---

## Out of scope

- Write operations (create/update volunteer records) — Phase 2, once sign-up (US-101) is wired to a real backend.
- Certification, expiry, history, or location fields (Phase 2 — REQ-F-016..020).
- Any use of this endpoint by dispatcher-web or volunteer-app in Phase 1 — both still use their own local mocks; real integration is a Phase 2 task.

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- Keep the response shape minimal and additive — new fields (location, availability, certification) should be addable in Phase 2 without breaking Phase 1 consumers, since none exist yet, but the habit starts here.
