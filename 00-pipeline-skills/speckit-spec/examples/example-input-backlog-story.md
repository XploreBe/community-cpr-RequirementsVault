# Example input — single backlog story

*(Extracted from InstallPro Product Backlog v3)*

### US-003 — Job herplannen bij uitval
- **Type:** Story
- **Story:** Als bureaumedewerker wil ik de jobs van een uitgevallen technicus snel herplannen, zodat ik dit in enkele minuten kan regelen in plaats van een halve ochtend te bellen.
- **Acceptatiecriteria:**
  - Gegeven een technicus wordt voor een dag op "afwezig" gezet, wanneer ik dat bevestig, dan worden al zijn jobs van die dag gemarkeerd als "te herplannen".
  - Gegeven een te herplannen job, wanneer ik een andere beschikbare technicus kies, dan wordt de job aan die technicus toegewezen en verdwijnt ze uit "te herplannen".
  - Gegeven geen andere technicus beschikbaar is, wanneer ik de lijst bekijk, dan blijft de job in "te herplannen" staan met een waarschuwing.
- **Prioriteit:** Must · **Grootte:** M (voorlopig) · **Fase:** Fase 1
- **Epic:** EPIC-1 · **Traceert naar:** REQ-F-003 · **Grounding:** Direct
- **Hangt af van:** US-001 (job aanmaken), US-002 (technicus voorstellen)
- **Status:** Nieuw
- **Definitie van "beschikbaar"** (from US-002, provisional): de technicus is die dag ingeroosterd, niet als afwezig gemarkeerd, en heeft nog vrije ruimte in zijn dagplanning.

**Upstream constraints relevant to this story:**
- CON-001: planning blijft centraal bij het bureau; technici plannen niet zelf hun dag.
- From scope: user roles (OQ-13) not yet defined — stories assume basic roles (bureau, technicus).
