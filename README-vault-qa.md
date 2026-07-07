# vault-qa — setup

## Wat je krijgt

- `00-pipeline-skills/vault-qa/` — de zesde skill, zelfde structuur als de andere vijf. Nu met
  drie modi: gewoon antwoord, voorgesteld-wijziging, en "vraag is ambigu" (relevant vooral voor
  agents die vragen stellen — zie hieronder).
- `.github/workflows/vault-qa.yml` — de trigger, inclusief follow-up via comments.
- `scripts/vault_qa_handler.py` — het script dat de skill uitvoert, op de issue reageert, en een
  globale rate limit afdwingt.

## Gebouwd met agents als vragenstellers in het achterhoofd

Dit systeem wordt niet alleen door mensen gebruikt, ook door dev/test-agents die tijdens hun werk
info nodig hebben. Twee dingen zijn daarom expliciet ingebouwd, niet later toegevoegd:

- **Elke comment begint met een machine-leesbare `STATUS:`-regel** (`answered`,
  `proposed_change`, `needs_clarification`, of `rate_limited`). Een agent kan hierop matchen met
  een simpele string-check in plaats van de tekst te moeten "begrijpen". Deze regel wordt door het
  script zelf gegenereerd op basis van de `mode` die het model teruggeeft — nooit door het model
  zelf geschreven, zodat de regel nooit per ongeluk anders geformuleerd wordt dan verwacht.
- **Een globale rate limit** (standaard 20 bot-comments per uur, repo-breed) voorkomt dat een
  agent die in een lus terechtkomt (bijv. herhaaldelijk dezelfde vraag stelt) ongemerkt je
  API-kosten laat oplopen. Bij overschrijding wordt Claude niet eens aangeroepen — er komt direct
  een `STATUS: rate_limited` comment terug.

## Installatie (eenmalig)

1. Kopieer deze drie dingen naar de root van je vault-repo, op dezelfde plek als je bestaande
   `00-pipeline-skills/` map en `github-sync/` script.
2. Maak in GitHub een label aan genaamd `vault-question` (Settings → Labels). De vier
   triage-labels (`status:answered`, `status:possible-change`, `status:needs-clarification`,
   `status:rate-limited`) hoef je niet zelf aan te maken, het script maakt ze zelf aan bij eerste
   gebruik als ze nog niet bestaan — je kan ze daarna wel zelf een kleur geven.
3. Voeg een repo secret toe: Settings → Secrets and variables → Actions → New repository secret
   → naam `ANTHROPIC_API_KEY`, waarde je API key. `GITHUB_TOKEN` heb je niet zelf nodig aan te
   maken, die levert GitHub Actions automatisch.
4. Klaar. Vanaf nu: iemand (of iets) opent een issue, labelt het `vault-question`, en binnen een
   minuut of twee verschijnt er een comment met het antwoord.

## Hoe het werkt, stap voor stap

1. Developer/agent opent een GitHub Issue met een vraag, en zet er het label `vault-question` op
   (of voegt het label toe aan een bestaande issue).
2. De workflow start, checkt de repo uit (dus de volledige vault, inclusief de laatst
   gesynchroniseerde staat).
3. Het script checkt eerst de rate limit (max 20 bot-comments in het afgelopen uur, repo-breed).
   Bij overschrijding stopt het hier met een `STATUS: rate_limited` comment, zonder Claude aan te
   roepen.
4. Het script leest `00-pipeline-skills/vault-qa/SKILL.md` als instructie. Voor context haalt het
   niet de hele vault op, maar zoekt gericht: het herkent ID's (`US-012`, `REQ-F-003`, ...) in de
   volledige thread en trefwoorden uit de laatste vraag, splitst elk vaultdocument in secties per
   kop, scoort elke sectie op treffers, en stuurt alleen de best scorende secties mee (tot een
   tekengrens). Als niets matcht, valt het terug op de openingssectie van elk kerndocument, en
   zegt dat expliciet in het antwoord.
5. Bij een vervolgvraag (iemand reageert met een comment op een issue die al het label
   `vault-question` heeft) leest het script ook de eerdere comments in de thread mee als
   geheugen, en behandelt het meest recente menselijke bericht als de eigenlijke vraag. De bot
   herkent zijn eigen eerdere antwoorden en reageert daar niet opnieuw op (geen oneindige lus).
6. Claude antwoordt in het vaste JSON-format uit de skill, in een van drie modi: gewoon antwoord,
   antwoord + CHG-voorstel, of "de vraag zelf is ambigu, hier zijn de mogelijke lezingen."
7. Het script prepend een machine-leesbare `STATUS:`-regel en post het geheel als comment op de
   issue. Daarnaast zet het één triage-label op de issue dat de laatste status weergeeft:
   `status:answered`, `status:possible-change`, `status:needs-clarification`, of
   `status:rate-limited`. Verschuift een thread van mode (bijvoorbeeld eerst gewoon beantwoord,
   later alsnog een CHG-signaal), dan verwijdert het script het oude statuslabel en zet het
   nieuwe — een issue draagt dus altijd precies één statuslabel, dat de huidige stand weergeeft,
   niet de hele geschiedenis. Labels buiten deze reeks (`vault-question`, of iets dat jij zelf
   toevoegt) blijven onaangeroerd.
8. Jij filtert op `status:possible-change` of `status:needs-clarification` wanneer het je uitkomt
   om te zien wat nog iets van jou nodig heeft, en beslist: goedkeuren (en dan normaal via de
   change-management skill verwerken) of afwijzen. Er verandert niets aan de vault totdat jij dat
   expliciet doet.

## Wat dit NIET doet, expliciet

- Het wijzigt nooit een vaultbestand. Alleen leesrechten op de repo, schrijfrechten alleen op
  issues/comments/labels.
- Het sluit nooit een issue, en het kent nooit automatisch een echt CHG-nummer toe.
- Het beantwoordt vervolgvragen via nieuwe comments op een reeds gelabeld issue (zie hierboven) —
  maar niet via edits aan een oud comment, en niet over meerdere issues heen.

## Bekende beperkingen (eerlijk gezegd)

- **Keyword-matching is geen semantisch zoeken.** De retrieval werkt op letterlijke ID's en
  woorden, niet op betekenis. "Wat gebeurt er als een vrijwilliger offline gaat" vindt een sectie
  die het woord "offline" bevat, maar een vraag die hetzelfde bedoelt met heel andere woorden
  (bijv. "verbinding kwijtraakt") kan gemist worden als het exacte woord nergens in de vault
  staat. Voor een echte semantische zoekfunctie zou je embeddings nodig hebben — bewust niet
  gebouwd, dat is een hele volgende laag complexiteit voor een probleem dat met keyword-matching
  in de praktijk al grotendeels wordt opgelost gezien hoe consistent je ID-schema en terminologie
  al zijn.
- **Follow-up via comments werkt nu, maar blijft éénregelig.** Elke run gebruikt het meest recente
  menselijke bericht als "de vraag" en de rest van de thread als geheugen. Als iemand in één
  comment twee losse vragen door elkaar stelt, wordt dat als één vraag behandeld.
- **Rate limit is globaal en grof, niet per-agent.** Het telt alle bot-comments in de repo van
  het afgelopen uur, ongeacht wie of wat de vraag stelde, en kijkt alleen naar de eerste 100
  comments van de API-call (paginering wordt niet gevolgd). Bij één zeer actieve legitieme agent
  én een tweede die vastloopt in een lus, deelt de tweede dus de limiet met de eerste — er is geen
  onderscheid per bron. Voor de eerste testfase is dat een aanvaardbare grove rem; als je meerdere
  agents parallel laat draaien, is per-agent tracking (bijv. op basis van wie de issue opende) de
  logische volgende stap.
- **De STATUS-regel dekt geen deelgevallen.** Een antwoord is altijd één van de vier statussen; er
  is geen "gedeeltelijk beantwoord, gedeeltelijk onduidelijk" tussenvorm. In de praktijk komt dat
  zelden voor omdat Mode C net bestaat om die situaties expliciet als "onduidelijk" te labelen in
  plaats van een halfslachtig antwoord te geven.
- **`labeled`/`edited`/`created`, niet `opened`.** Bewust: dit voorkomt dat elke issue die per
  ongeluk zonder label wordt geopend meteen een API-call triggert. Bijeffect: als iemand het label
  meteen bij het openen zet, telt dat als een "labeled" event en werkt het gewoon.
