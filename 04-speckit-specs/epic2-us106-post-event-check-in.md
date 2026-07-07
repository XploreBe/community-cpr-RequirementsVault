# Post-event check-in

**Story:** US-106 — Post-event check-in
**Epic:** EPIC-2 — Alert response walking skeleton (volunteer-app)
**Traces to:** REQ-F-028, REQ-F-029, REQ-F-030
**Date:** 2026-07-06
**Produced by:** speckit-spec skill

---

## Overview

After responding to an alert, a volunteer should get a short moment to confirm what happened and, if they want, say how they're doing. This feature prompts a quick check-in once an incident ends.

---

## User scenarios

### Scenario 1 — Check-in prompt after an incident ends
Given a volunteer accepted an alert, when the (mocked) incident ends, then they are prompted with two required questions: "Did you arrive?" and "Were you stood down?" (both yes/no).

### Scenario 2 — Optional wellbeing follow-up
Given the check-in is shown, when the volunteer submits without answering the wellbeing follow-up, then the check-in still completes successfully — this question is optional, unlike the two above.

### Scenario 3 — No check-in for volunteers who declined
Given a volunteer declined the alert (never accepted), when the incident ends, then no check-in is shown to them.

---

## Constraints and assumptions

- "Incident ends" is a mocked/simulated trigger in Phase 1 — there is no real link yet to dispatcher-web's incident status (EPIC-1) or to a real dispatch/stand-down event (Phase 2).
- Android-only, React Native (CON-001).

---

## Out of scope

- Any real connection between this trigger and dispatcher-web's incident lifecycle (Phase 2 — needs real backend integration across repos).
- Aggregating or reporting on check-in answers (Phase 2/Later — reporting & analytics, explicitly out of scope per the brief).

**Unresolved — dev should not implement until confirmed:**
- None blocking this story.

---

## Constitution snippet

- Keep the two required questions (arrived, stood down) and the optional wellbeing question as separately validated fields — don't let the optional one block submission.
