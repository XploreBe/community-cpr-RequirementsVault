# Structured Requirements — Community CPR Volunteer Dispatch (condensed)

**Source(s):** Project brief; kickoff notes
**Status:** Draft — reviewed
*(Condensed for the scope example; a real structured-requirements doc would be fuller.)*

## 2. Functional requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| REQ-F-001 | The operator can pin the patient's location on a map. | Must | |
| REQ-F-002 | The system identifies volunteers near the patient. | Must | Needs fast geospatial lookup at city scale. |
| REQ-F-003 | The system sends an alert to nearby volunteers. | Must | |
| REQ-F-004 | A volunteer accepts an alert with one tap ("I'm going"). | Must | Decline action not stated — see OQ-04. |
| REQ-F-005 | The volunteer gets navigation to the scene. | Must | Via Google Maps — see CON-002. |
| REQ-F-006 | The dispatcher console requires login with roles. | Must | |
| REQ-F-007 | The dispatcher console shows live response status. | Must | |
| REQ-F-008 | The dispatcher can stand responders down. | Must | |
| REQ-F-009 | Tiered alerting: certified volunteers first, widen the net if nobody accepts after a delay. | Must | Tier breakdown TBD (OQ-01); delay undefined (OQ-02). |
| REQ-F-010 | Volunteers upload certification; the system tracks expiry and reminds them to re-verify. | Should | |
| REQ-F-011 | Volunteers set availability (always on, scheduled, do-not-disturb). | Should | |
| REQ-F-012 | In-app CPR reference usable during a live event. | Should | |
| REQ-F-013 | Post-event check-in (arrived, stood down) plus optional wellbeing follow-up. | Could | |

## 3. Non-functional requirements

| ID | Requirement | Category | Priority | Notes |
|----|-------------|----------|----------|-------|
| REQ-N-001 | Notification reaches the volunteer's phone within ~5 seconds, 95% of the time. | Performance | Must | Confirm exact target — OQ-03. |
| REQ-N-002 | 99.9% uptime on the dispatch path. | Reliability | Must | |
| REQ-N-003 | If a dependency (maps, cert service) fails, the rest keeps working. | Reliability | Must | |
| REQ-N-004 | Scales to multiple countries without re-platforming; data isolated per country. | Scalability | Must | |
| REQ-N-005 | MFA for dispatchers, encryption everywhere, full audit log. | Security | Must | |
| REQ-N-006 | Country-specific elements (emergency number, language, rules) configurable, not hard-coded. | Portability | Must | |
| REQ-N-007 | Background volunteer location only with explicit consent; battery-friendly. | Privacy | Must | |

## 4. Constraints

| ID | Constraint | Notes |
|----|------------|-------|
| CON-001 | The volunteer app is Android only for now. | iOS later/undecided. |
| CON-002 | Navigation uses Google Maps. | |
| CON-003 | The dispatcher interface is a web console. | |

## 5. Open questions

- **OQ-01:** Final volunteer tier breakdown is TBD. — affects REQ-F-009.
- **OQ-02:** Delay before widening the net is undefined. — affects REQ-F-009.
- **OQ-03:** Exact alert-speed target and percentile. — affects REQ-N-001.
- **OQ-04:** Does the volunteer need an explicit decline action, or only "I'm going"? — affects REQ-F-004.

## 8. Out of scope (explicitly stated)

- AED-fetch flow (sending a second volunteer for a defibrillator). Later phase; architecture should leave room.
- AED registry / source of AED locations. Open.
- Reporting and analytics dashboards for EMS partners. Later.
- iOS volunteer app. Later/undecided.
