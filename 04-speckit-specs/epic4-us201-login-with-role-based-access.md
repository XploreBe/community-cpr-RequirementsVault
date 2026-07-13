# Log in with role-based access

**Story:** US-201 — Log in with role-based access
**Epic:** EPIC-4 — Authentication & roles
**Traces to:** REQ-F-001, REQ-N-007
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — not part of the current Phase 2 round (the simple core notification loop). Kept as-is, ready to pick up when auth is prioritized.

---

## Overview

Dispatchers and admins need their own accounts so the console knows who's using it and what they're allowed to do. This feature lets either role log in and reach only the parts of the console their role covers.

---

## User scenarios

### Scenario 1 — Dispatcher logs in
Given valid credentials for a dispatcher account, when the user logs in, then they reach the console with dispatcher-level access: they can create, view, update, and manage incidents, but do not see the cross-incident oversight view.

### Scenario 2 — Admin logs in
Given valid credentials for an admin account, when the user logs in, then they reach the console with admin-level access, including oversight of all dispatchers and incidents.

### Scenario 3 — Invalid credentials (negative)
Given incorrect credentials, when the user attempts to log in, then access is denied with a generic "invalid credentials" message that does not reveal whether the username or the password was wrong.

### Scenario 4 — Role boundary enforced (least-privilege)
Given a dispatcher account, when that user attempts to reach an admin-only screen or API endpoint directly (e.g. by URL), then access is denied, regardless of how the request was made.

---

## Constraints and assumptions

- Two roles only: dispatcher and admin (REQ-F-001, confirmed via OQ-011 resolution — CHG-005). No supervisor role.
- Least-privilege applies at both the UI and API layer, not just by hiding menu items (REQ-N-007).

---

## Out of scope

- MFA (a second verification step) — separate story, US-202.
- Cross-incident oversight UI details — separate story, US-203.
- Encryption scope and security audit logging for this login flow — tracked as cross-cutting NFRs in 03-product-backlog-v1.md ("Non-functional requirements — Phase 2"), not specified here.

**Unresolved:**
- OQ-010 (precise scope of "encryption everywhere") — affects how login credentials/tokens are protected in transit and at rest. Build at minimum HTTPS in transit (already required by CON-004/005); do not guess at broader scope (at-rest encryption, key management) until OQ-010 is answered.

---

## Constitution snippet

- Enforce role checks server-side on every request, not just by hiding UI elements for a role.
- Never reveal in an error message which part of a login attempt (username vs. password) was wrong.
