# Kickoff meeting notes — CPR dispatch thing — 29 May

- ok so the basic idea: someone has a cardiac arrest, the 911/112 operator recognises it, pins the patient on a map, the app finds nearby volunteers, pings them, the volunteer taps "I'm going" and gets directions to the scene. they start CPR before the ambulance arrives.
- needs to work in different countries from day one. don't hardcode the country-specific stuff (emergency number, language, address format, local rules). this is basically the whole point of the project
- volunteer app = Android only for now. iOS maybe later
- dispatcher uses a web console: login, see the map, see nearby volunteers, hit send, watch who's responding live, and be able to stand everyone down when EMS is on scene
- speed matters a LOT. someone said the notification should reach the volunteer's phone in about 5 seconds. 95% of the time? something like that
- volunteer types: people with a current CPR/BLS certification, healthcare professionals, and willing-but-untrained bystanders. who gets alerted first and at what distance should be configurable per country. final tier breakdown still TBD
- certified people get alerted first, then widen the net if nobody accepts after a while
- background location, but only with the volunteer's consent, and it has to be battery-friendly. don't keep the patient's location around longer than needed (privacy)
- MFA for dispatchers. encryption everywhere. audit log of everything that happens
- navigation — just lean on Google Maps, no need to build our own
- in-app CPR reference the volunteer can look at during a live event
- LATER, not now: sending a second volunteer to grab a nearby AED (defibrillator) on the way. and where AED locations even come from is an open question — official government registry? crowdsourced? a mix? nobody knows yet
- also later: reporting and analytics dashboards for EMS partners
- uptime should be high — like 99.9% on the dispatch path. and if something like maps or the cert service breaks, the rest should keep working
- has to scale to multiple countries without re-platforming, with data isolated per country

Follow-up email from the PM (paraphrased):
"Don't forget volunteers need to upload their certification and we track its expiry and remind them to re-verify. They should also be able to set availability — always on, scheduled, or do-not-disturb. And there should be a quick check-in after an event: did you arrive, were you stood down, plus an optional wellbeing follow-up."

Stray note someone added at the bottom: "should be user friendly and fast" (?)
