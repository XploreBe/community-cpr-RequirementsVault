# Admin: cross-incident oversight

**Story:** US-203 — Admin: cross-incident oversight
**Epic:** EPIC-4 — Authentication & roles
**Traces to:** REQ-F-001
**Date:** 2026-07-13
**Produced by:** speckit-spec skill

---

## Overview

An admin needs to see the bigger picture across the whole system, not just one incident at a time, so they can oversee how dispatchers are handling incidents system-wide.

---

## User scenarios

### Scenario 1 — View all dispatchers and incidents
Given the admin is logged in, when they open the oversight view, then they see a list of all dispatchers and, for each, their currently open and recently closed incidents.

### Scenario 2 — Drill into an incident
Given the admin selects a specific incident from the oversight view, when they open it, then they see the same incident detail a dispatcher would see, including the full dispatch audit trail (REQ-F-012 full, US-209).

### Scenario 3 — Dispatcher cannot reach this view (negative)
Given a dispatcher (not admin) account, when they attempt to reach the oversight view directly (e.g. by URL), then access is denied.

### Scenario 4 — No incidents yet (edge case)
Given no dispatcher currently has any open or recently closed incidents, when the admin opens the oversight view, then a neutral "no incidents to show" state is displayed instead of an empty or broken screen.

---

## Constraints and assumptions

- Requires US-201 (login) and US-209 (full audit trail) to exist first — this view surfaces the same incident detail US-209 produces.
- Least-privilege: this view is admin-only (REQ-N-007).

---

## Out of scope

- The incident detail layout itself — reused from US-209's audit trail, not redesigned here.
- Real-time push notifications to admins about incident activity — not requested anywhere upstream.

**Unresolved:**
- None blocking.

---

## Constitution snippet

- Reuse the existing incident-detail component from the dispatcher view rather than building a second, parallel implementation for admins.
