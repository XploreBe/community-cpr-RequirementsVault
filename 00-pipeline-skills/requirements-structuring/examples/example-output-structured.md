# Structured Requirements — Community CPR Volunteer Dispatch

**Source(s):** Kickoff notes (29 May); PM follow-up email; stray note
**Date structured:** 2026-06-16
**Produced by:** requirements-structuring skill
**Status:** Draft — needs human review

## 1. Summary

The system alerts nearby trained volunteers to an out-of-hospital cardiac arrest so they can start CPR before the ambulance arrives. A 911/112 operator locates the patient on a map in a web console and sends an alert; nearby volunteers are notified on an Android app, accept, and navigate to the scene. The system must work across countries from day one, with country-specific behaviour configurable rather than hard-coded.

## 2. Functional requirements

| ID | Requirement | Priority | Source | Notes |
|----|-------------|----------|--------|-------|
| REQ-F-001 | The system shall let the operator pin the patient's location on a map. | Must | Kickoff notes | Notes assume the operator recognises the cardiac arrest and starts the flow (see AS-002). |
| REQ-F-002 | The system shall identify volunteers near the patient's location. | Must | Kickoff notes | Depends on a volunteer registry (see AS-001). |
| REQ-F-003 | The system shall send an alert to nearby volunteers. | Must | Kickoff notes | |
| REQ-F-004 | The system shall let a volunteer accept an alert with one tap ("I'm going"). | Must | Kickoff notes | Notes only mention accepting; explicit decline is not stated — see OQ-007. |
| REQ-F-005 | The system shall provide the volunteer with navigation to the scene. | Must | Kickoff notes | Delivered via Google Maps — see CON-002. |
| REQ-F-006 | The dispatcher console shall require login. | Must | Kickoff notes | Roles not specified in this input. |
| REQ-F-007 | The dispatcher console shall display a map. | Must | Kickoff notes | |
| REQ-F-008 | The dispatcher console shall display nearby volunteers. | Must | Kickoff notes | |
| REQ-F-009 | The dispatcher console shall let the dispatcher trigger the alert ("send"). | Must | Kickoff notes | |
| REQ-F-010 | The dispatcher console shall show live response status (who is responding). | Must | Kickoff notes | Exact statuses not enumerated in this input. |
| REQ-F-011 | The dispatcher shall be able to stand all responders down when EMS is on scene. | Must | Kickoff notes | |
| REQ-F-012 | The system shall alert certified volunteers first and widen the net if nobody accepts after a delay. | Must | Kickoff notes | Delay duration ("after a while") undefined — see OQ-008. |
| REQ-F-013 | The system shall make the alert order and distance configurable per country. | Must | Kickoff notes | Who configures this and how is not stated — see AS-002. |
| REQ-F-014 | The system shall let volunteers set availability (always on, scheduled, or do-not-disturb). | Unspecified | PM email | No priority signal given. |
| REQ-F-015 | The system shall let volunteers upload their certification. | Unspecified | PM email | |
| REQ-F-016 | The system shall track certification expiry and remind volunteers to re-verify. | Unspecified | PM email | |
| REQ-F-017 | The volunteer app shall provide an in-app CPR reference usable during a live event. | Unspecified | Kickoff notes | |
| REQ-F-018 | The system shall provide a post-event check-in capturing whether the volunteer arrived and whether they were stood down. | Unspecified | PM email | |
| REQ-F-019 | The system shall offer an optional wellbeing follow-up after an event. | Unspecified | PM email | Stated as optional. |
| REQ-F-020 | The system shall capture the volunteer's location in the background to determine who is nearby. | Must | Kickoff notes | Governed by consent and efficiency requirements — see REQ-N-009, REQ-N-010. |

## 3. Non-functional requirements

| ID | Requirement | Category | Priority | Source | Notes |
|----|-------------|----------|----------|--------|-------|
| REQ-N-001 | The system shall deliver the notification to the volunteer's phone within about 5 seconds, 95% of the time. | Performance | Must | Kickoff notes | Stated with uncertainty ("something like that") — confirm exact target and percentile, see OQ-003. |
| REQ-N-002 | The dispatch path shall achieve 99.9% uptime. | Reliability | Must | Kickoff notes | |
| REQ-N-003 | If a dependency such as maps or the certification service fails, the rest of the system shall keep working. | Reliability | Must | Kickoff notes | Graceful degradation. |
| REQ-N-004 | The system shall scale to multiple countries without re-platforming. | Scalability | Must | Kickoff notes | |
| REQ-N-005 | The system shall keep data isolated per country. | Security / Privacy | Must | Kickoff notes | |
| REQ-N-006 | The system shall require MFA for dispatchers. | Security | Must | Kickoff notes | |
| REQ-N-007 | The system shall encrypt data everywhere. | Security | Must | Kickoff notes | "Everywhere" not scoped further in this input. |
| REQ-N-008 | The system shall keep an audit log of everything that happens. | Security / Auditability | Must | Kickoff notes | |
| REQ-N-009 | The system shall capture volunteer background location only with the volunteer's explicit consent. | Privacy | Must | Kickoff notes | |
| REQ-N-010 | Background location capture shall be battery-friendly. | Performance / Efficiency | Must | Kickoff notes | "Battery-friendly" is not measurable — see OQ-004. |
| REQ-N-011 | The system shall not retain the patient's location longer than needed. | Privacy | Must | Kickoff notes | "Longer than needed" undefined — see OQ-005. |
| REQ-N-012 | Country-specific elements (emergency number, language, address format, local rules) shall be configurable, not hard-coded. | Portability | Must | Kickoff notes | Described as the central goal of the project. |

## 4. Constraints

| ID | Constraint | Source | Notes |
|----|------------|--------|-------|
| CON-001 | The volunteer app is Android only for now. | Kickoff notes | iOS described as "maybe later" — see OQ-009 and Out of scope. |
| CON-002 | Navigation uses Google Maps rather than a built-in solution. | Kickoff notes | |
| CON-003 | The dispatcher interface is a web console. | Kickoff notes | |

## 5. Open questions (need stakeholder input)

- **OQ-001:** What is the final volunteer tier breakdown? — affects REQ-F-012, REQ-F-013, and the glossary tiers.
- **OQ-002:** Where do AED locations come from (official registry, crowdsourced, or a mix)? — affects the out-of-scope AED-fetch flow; architecture must leave room for it.
- **OQ-003:** Is the alert-speed target exactly 5 seconds at the 95th percentile? Confirm both numbers. — affects REQ-N-001.
- **OQ-004:** What does "battery-friendly" mean in measurable terms (e.g. max battery drain per hour)? — affects REQ-N-010.
- **OQ-005:** What is the retention period for patient location ("longer than needed")? — affects REQ-N-011.
- **OQ-006:** The stray note "should be user friendly and fast" — what does "user-friendly" mean here, and is "fast" the same as the 5-second alert target or something else such as app responsiveness? Needs measurable criteria. — affects REQ-N-001 and possibly new requirements.
- **OQ-007:** Does the volunteer need an explicit "decline" action, or only "I'm going"? The input mentions only accepting. — affects REQ-F-004.
- **OQ-008:** After the first tier, what is the delay ("after a while") before widening the net to the next tier? — affects REQ-F-012.
- **OQ-009:** Is iOS a planned later phase or simply undecided? "Maybe later" is ambiguous. — affects CON-001.

## 6. Assumptions

- **AS-001:** A volunteer registry (storing each volunteer's tier, certification, availability, and location) is in scope, since the system must find and alert nearby volunteers even though the input does not describe the registry directly. — affects REQ-F-002, REQ-F-012, REQ-F-015.
- **AS-002:** "Configurable per country" implies an admin capability to set per-country rules; the input does not say who configures these or how. — affects REQ-F-013, REQ-N-012.

## 7. Glossary

- **AED** — automated external defibrillator; the device a second volunteer might fetch in the later AED-fetch flow.
- **BLS** — basic life support; referenced as a certification type alongside CPR certification. Whether CPR and BLS certification are one category or distinct is unclear — see OQ-001.
- **Certified volunteer / healthcare professional / willing-but-untrained bystander** — the three volunteer types named in the input; exact breakdown TBD — see OQ-001.
- **Dispatch path** — the critical flow from the operator's alert to the volunteer's notification, referenced by the uptime requirement (REQ-N-002). Definition inferred from context; confirm.
- **EMS** — emergency medical services (the ambulance service and partner organisations).
- **Stand down** — instructing responding volunteers to stop because EMS is on scene or the situation is over (REQ-F-011).

## 8. Out of scope (explicitly stated)

- AED-fetch flow — sending a second volunteer to grab a defibrillator. Later phase; the architecture should leave room for it (AED location source is OQ-002).
- Reporting and analytics dashboards for EMS partners. Later phase.
- iOS volunteer app — described as "maybe later"; timing unclear (OQ-009).
