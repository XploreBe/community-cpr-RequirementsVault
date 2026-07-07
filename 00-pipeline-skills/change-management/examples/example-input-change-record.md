# Example Input — Change Record

This is a realistic change record for a mid-project OQ resolution.
It is used as the worked example for the change-management skill.

---

```
CHG-ID:        CHG-001
Date:          2026-07-01
Triggered by:  Stakeholder call — EMS partner (Belgium) + product owner
Change type:   OQ resolved
Affected item: OQ-004
Old value:     N-seconds escalation timeout — value unresolved, shipped as required config with no default
New value:     30 seconds for first-tier escalation, 60 seconds for second-tier escalation. Both values are configurable per country; these are the system defaults.
Reason:        Belgian EMS protocol requires a minimum 30-second window for certified first responders before bystanders are alerted. The 60-second second tier aligns with Dutch HartslagNu practice, confirmed acceptable by the product owner as a cross-country default.
Resolves OQ:   OQ-004
Notes:         OQ-013 (tier ordering) was discussed in the same call but remains open — no decision. Do not update OQ-013. Also check whether US-008, US-011, US-013 can now move from Not Ready to Ready.
```
