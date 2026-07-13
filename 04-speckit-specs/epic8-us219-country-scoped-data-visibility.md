# Country-scoped data visibility

**Story:** US-219 — Country-scoped data visibility
**Epic:** EPIC-8 — Country portability & admin tools
**Traces to:** REQ-F-036, REQ-N-004
**Date:** 2026-07-13
**Produced by:** speckit-spec skill
**Status:** Deferred to Phase 3 [CHG-009, 2026-07-13] — country portability, whole of EPIC-8, is explicitly deferred; system runs single-country for now. Kept as-is, ready to pick up later.

---

## Overview

As the system spreads across countries, a user in one country shouldn't see or manage data that belongs to another jurisdiction.

---

## User scenarios

### Scenario 1 — Scoped to own country
Given a user's account is tied to a country, when they view incidents or volunteers, then only records from their own country are shown.

### Scenario 2 — Cross-country access denied (negative)
Given a user attempts to access an incident or volunteer record belonging to a different country (e.g. by direct link/ID), when they try, then access is denied.

---

## Constraints and assumptions

- Data is partitioned per country at the storage level (CON-007), extending Phase 1's ENABLER-002 datastore shape (built with this partitioning in mind but not enforced).
- The specific database/indexing technology is a development-team decision (OQ-003 resolved — CHG-006).

---

## Out of scope

- Cross-country admin roles / a "global admin" who sees all countries — not requested anywhere upstream; if needed later, that's new scope to raise, not assumed here.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Enforce country scoping at the data-access layer itself, not just by filtering what the UI displays — a direct API call must be scoped the same way.
