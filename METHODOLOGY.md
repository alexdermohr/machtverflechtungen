# Methodik

## Ziel

Das Projekt macht schwierige, politisch aufgeladene Hypothesen prüfbar. Amtliche Darstellungen werden nicht automatisch übernommen; Verdachtsmomente werden nicht automatisch zu Tatsachen erklärt.

Das Erkenntnisziel lautet: **möglichst weitreichende Zusammenhänge finden können, ohne sie bereits vorauszusetzen.**

## Evidenzstufen

- **`established` — belegt:** direkter Primärbeleg oder mehrere voneinander unabhängige hochwertige Belege tragen die konkrete Aussage.
- **`strong` — stark gestützt:** starke Indizienkette, aber mindestens ein relevantes Glied bleibt indirekt.
- **`plausible` — plausible Hypothese:** erklärt vorhandene Befunde gut, ernsthafte Alternativerklärungen bleiben möglich.
- **`speculative` — spekulativ/offen:** prüfbarer Verdacht mit noch unzureichender Beleglage.
- **`contradicted` — widersprochen:** die konkrete Form der Behauptung kollidiert mit höher gewichteter Evidenz.

Eine Evidenzstufe bewertet immer **eine konkrete Aussage**, nicht pauschal eine Person, Organisation oder Gesamterzählung.

## Quellenhierarchie

1. **A — Primärquellen:** Urteile, parlamentarische Untersuchungsausschüsse, amtliche Akten, deklassifizierte Dokumente, Kabinettsprotokolle, diplomatische Dokumente, zeitgenössische Originalunterlagen.
2. **B — hochwertige Forschung:** wissenschaftliche Monografien, Peer Review, unabhängige Historikerkommissionen, wissenschaftliche Editionsprojekte.
3. **C — investigative Recherche:** nachvollziehbar belegte journalistische Arbeiten, dokumentierte Interviews und investigative Bücher.
4. **D — Hinweise:** Presse ohne zugänglichen Originalbeleg, Memoiren, einzelne Zeugenaussagen, Blogs und Enzyklopädien.
5. **E — Leads:** Foren, Social Media und unbestätigte Behauptungen. Sie dienen zum Finden, nicht zum Beweisen.

Gewichtet wird nach Primärnähe, Methodik, Replizierbarkeit, Aktualität und Kontextpassung — nicht nach publizistischer Lautstärke.

### Strukturelle Mindestschwelle für `established`

Der V1-Validator operationalisiert die stärkste Evidenzstufe konservativ: Eine als `established` markierte Aussage braucht mindestens entweder

- eine registrierte Tier-A-Quelle, die zugleich als Primärquelle markiert ist; oder
- mindestens zwei Tier-B/C-Quellen aus unterschiedlichen Institutionen.

Diese Regel ist eine **strukturelle Mindestschwelle**, kein Beweis semantischer Unabhängigkeit oder direkter Belegkraft. Unterschiedliche Institutionen sind nur eine maschinenprüfbare Näherung. Ob eine Quelle die konkrete Aussage tatsächlich direkt trägt und ob mehrere Quellen voneinander unabhängig sind, bleibt zusätzlich Gegenstand der inhaltlichen Prüfung.

## Claim-Regeln

Zentrale Aussagen werden nach Möglichkeit als eigenständige Claims mit stabiler ID erfasst. Ein Claim enthält Wortlaut, Klassifikation, Evidenzstufe und Quellen sowie gegebenenfalls Gegenbelege und offene Fragen.

Die erste Version erzwingt atomare Claims noch nicht für jeden Nebensatz. Schema-Pflege soll Recherche nicht verdrängen. Die Struktur muss aber eine spätere Atomisierung erlauben.

Quellenlos dürfen in V1 nur ausdrücklich als `speculative` markierte Hypothesen oder offene Fragen bleiben. Sobald eine Hypothese oder offene Frage eine stärkere bzw. widersprechende Evidenzstufe trägt, gelten die normalen Quellenanforderungen.

Klassifikationen unterscheiden mindestens:

- **fact:** positive Tatsachenbehauptung;
- **counterevidence:** belastbarer Gegenbefund zu einer weitergehenden These;
- **hypothesis:** ausdrücklich zu prüfende Erklärung;
- **interpretation:** quellengebundene Einordnung;
- **open_question:** noch offene, operationalisierbare Prüfungsfrage.

## Relationen

Auch eine Kante im Netzwerkgraphen ist eine Behauptung. Eine Relation wie

`Person A -- erhielt Zahlungen von --> Behörde B`

muss Quellen besitzen.

Zu unterscheiden sind insbesondere:

- bloße Mitgliedschaft;
- Kontakt oder Nähe;
- Finanzierung;
- organisatorische Rolle;
- dokumentierte Intervention;
- Interessenkonflikt;
- Einfluss;
- Steuerung;
- rechtswidriges Verhalten.

Bloße Ko-Präsenz in einem Gremium wird nicht als Einfluss- oder Steuerungsverhältnis modelliert.

## Korrelation, Verbindung, Einfluss, Steuerung

- **Korrelation:** zwei Vorgänge treten gemeinsam oder zeitnah auf.
- **Verbindung:** eine dokumentierte Beziehung zwischen Akteuren besteht.
- **Einfluss:** es gibt Evidenz dafür, dass diese Beziehung Entscheidungen oder Verhalten mitprägt.
- **Steuerung:** ein Akteur gibt Ziele, Mittel oder konkrete Handlungen eines anderen Akteurs maßgeblich vor.

Jede Stufe verlangt zusätzliche Evidenz. Eine Verbindung beweist keinen Einfluss; Einfluss beweist keine Steuerung.

## Staatliche Kenntnis, Infiltration, Duldung, Unterstützung, Steuerung

Diese Begriffe dürfen nicht ineinanderfallen:

1. **Kenntnis:** eine staatliche Stelle besitzt relevante Informationen.
2. **Infiltration:** eine Quelle, V-Person oder ein verdeckter Mitarbeiter befindet sich in einer Zielstruktur.
3. **Duldung / Nicht-Eingreifen:** eine reale Eingriffsmöglichkeit bestand möglicherweise, wurde aber nicht oder nur begrenzt genutzt.
4. **Unterstützung:** Geld, Sachmittel, Schutz, Logistik oder operative Hilfe wirken zugunsten eines Akteurs oder einer Struktur.
5. **Steuerung:** Ziele oder konkrete Handlungen werden aktiv dirigiert.

Vorwissen ist keine Tatbeteiligung. Infiltration ist keine Steuerung. Materielle Unterstützung kann eine Struktur stabilisieren, ohne dass der Unterstützer sämtliche Ziele oder Handlungen kontrolliert.

## Politischer Nutzen, Motiv, Absicht, Urheberschaft

Ein Ereignis kann Folgen haben, von denen Institutionen oder politische Akteure profitieren.

Daraus folgt nicht automatisch:

`Nutzen → Motiv → Absicht → Urheberschaft`

Jeder Übergang ist eine zusätzliche Kausalbehauptung und braucht eigene Evidenz.

## Terrorismus: vier getrennte Untersuchungsebenen

Bei Terrorismus oder politischer Gewalt werden vier qualitativ verschiedene Ebenen unterschieden:

1. **Verwertung:** autonom entstandene Gewalt wird politisch für Sicherheitsbefugnisse, Überwachung, Repression oder institutionelle Veränderungen genutzt.
2. **Penetration / Management:** Dienste infiltrieren Milieus, führen Quellen, bezahlen Informanten oder schützen operative Zugänge.
3. **Provokation / Inszenierung:** staatliche Stellen erzeugen, provozieren oder imitieren einen Vorgang.
4. **Steuerung:** terroristische Akteure oder konkrete Anschläge werden aktiv dirigiert.

Ein Beleg für Ebene 1 oder 2 beweist nicht Ebene 3 oder 4.

## Prüfmatrix für einschlägige Fälle

Nach Möglichkeit werden getrennt geprüft:

1. Vorwissen;
2. Infiltration;
3. Eingriffsmöglichkeiten;
4. Nicht-Eingreifen;
5. materielle Unterstützung;
6. Täuschung oder Provokation;
7. Ermittlungsmanipulation / Depistaggio;
8. Vertuschung;
9. politische Verwertung;
10. neue Befugnisse, Überwachung oder Repression;
11. Gegenbelege;
12. konkurrierende Erklärungen.

## Strategie der Spannung

Der Begriff ist ein Hypothesen- und Vergleichsrahmen, keine universelle Erklärung. Er darf nicht als Abkürzung für die Behauptung dienen, ein bestimmter Staat, Dienst oder ausländischer Akteur habe jeden einzelnen Anschlag angeordnet.

Konkrete Täterschaft, Mitwisserschaft, Deckung, Depistaggio, Nachrichtendienstbeziehungen und politische Verwertung müssen getrennt belegt werden.

## Widersprüchliche Quellen

Widersprüche werden nicht geglättet.

Eine belastbare Fallakte soll möglichst sichtbar machen:

- Befunde;
- Hypothesen;
- Evidenz dafür;
- Evidenz dagegen;
- alternative Erklärungen;
- Widersprüche zwischen Quellen;
- fehlende Belege;
- nächste Prüfung.

Parlamentarische, behördliche oder politische Wertungen sind zunächst **Aussagen der jeweiligen Institution**. Eine Primärquelle belegt sicher, dass die Institution diese Aussage getroffen hat; sie ersetzt nicht automatisch die unabhängige Prüfung jedes historischen Sachverhalts innerhalb dieser Aussage.

## Historische Kontextabhängigkeit

Institutionen, Rechtslagen und Begriffe ändern sich. Ein Dokument belegt zunächst den damaligen Wissens- und Entscheidungsstand. Spätere Aktenfunde oder Forschung können ihn korrigieren oder anders einordnen.

## Personen und Organisationen

Mitgliedschaften und Kontakte sind zunächst deskriptive Daten. Für Vorwürfe wie Korruption, Steuerung, illegale Einflussnahme oder Beteiligung an Gewalt gelten dieselben Quellenstandards wie für andere Tatsachenbehauptungen.

Atlantik-Brücke, Trilaterale Kommission, Bilderberg, Stiftungen, Thinktanks und vergleichbare Netzwerke werden deshalb nicht automatisch unter Staatskriminalität eingeordnet. Untersucht werden konkrete Mitgliedschaften, Überschneidungen, Finanzierung, Drehtüren, Lobbykontakte, Interventionen und gegebenenfalls nachweisbare Interessenkonflikte.

## Reproduzierbarkeit

Git ist in V1 die kanonische Wahrheit.

- Fallakten: Markdown mit maschinenlesbarem Frontmatter;
- Quellen: `data/sources.yml`;
- Entitäten: `data/entities.yml`;
- Mechanismen: `data/mechanisms.yml`;
- Relationen: `data/relations.yml`;
- Schemas: `schemas/`;
- Validator: `scripts/validate.py`;
- abgeleitete Übersichten: `scripts/build_indexes.py`.

Timeline, Netzwerk und weitere Indizes werden aus denselben Daten erzeugt. Dadurch entsteht keine zweite, versteckte Datenwahrheit neben den Fallakten.
