# Methodik

## Ziel

Machtverflechtungen macht politisch aufgeladene und historisch schwierige Hypothesen prüfbar. Amtliche Darstellungen werden nicht automatisch übernommen; Verdachtsmomente werden nicht automatisch zu Tatsachen erklärt.

Das Erkenntnisziel lautet: **möglichst weitreichende Zusammenhänge finden können, ohne sie bereits vorauszusetzen.**

Die Hypothesenbildung darf weit sein. Die Evidenzklassifikation bleibt eng.

## Bewertete Einheit: der Claim

Im Fallmodell ist die kleinste bewertete Erkenntniseinheit ein **konkreter Claim**. Eine Claim-Evidenzstufe bewertet weder den Fall pauschal noch eine daraus abgeleitete Gesamterzählung. Bestehende Organisationsprofile verwenden derzeit noch eine separate profilweite Evidenzstufe; bis zu ihrer eigenen Claim-Migration ist dieses Legacy-Feld auf die Beleglage des Profils beschränkt und kein Ersatz für fallinterne Claim-Bewertungen.

Ein Fall besitzt deshalb keinen globalen Wahrheits- oder Evidenzwert. Sein `status` beschreibt ausschließlich den Forschungsstand:

- `draft` — strukturell angelegt, noch nicht vollständig geprüft;
- `developing` — substantiell bearbeitet, wichtige Prüfungen bleiben offen;
- `reviewed` — das verpflichtende Prüfschema wurde für den aktuellen Datenstand durchlaufen.

`reviewed` bedeutet nicht „wahr“ oder „abgeschlossen“. Neue Quellen können Claims verändern.

Auch der sichtbare **gesicherte Ereigniskern** bildet keine freie Faktenschicht neben den Claims. `event_claims` darf ausschließlich auf Claims desselben Falls verweisen, die als `fact` klassifiziert und `established` oder `strong` bewertet sind. Der Falltext darf diesen Ereigniskern nur aus diesen Claims ableiten; der Validator prüft, dass Claim-ID und Claim-Wortlaut im sichtbaren Falltext gespiegelt bleiben.

Auch die fallweiten Synthesen **„Was folgt?“** und **„Was folgt nicht?“** dürfen keine quellenlose Nebenargumentation bilden. Jeder Syntheseeintrag verweist deshalb auf die Claims desselben Falls, aus denen er abgeleitet wird. Die Referenz macht die Ableitung prüfbar; sie beweist nicht automatisch, dass der Synthesetext logisch aus den Claims folgt.

## Evidenzstufen für Claims

- **`established` — belegt:** direkter Primärbeleg oder mehrere voneinander unabhängige hochwertige Belege tragen die konkrete Aussage.
- **`strong` — stark gestützt:** starke Indizienkette, aber mindestens ein relevantes Glied bleibt indirekt.
- **`plausible` — plausible Hypothese:** erklärt vorhandene Befunde gut; ernsthafte Alternativerklärungen bleiben möglich.
- **`speculative` — spekulativ/offen:** prüfbarer Verdacht mit noch unzureichender Beleglage.
- **`contradicted` — widersprochen:** die konkrete Form der Behauptung kollidiert mit höher gewichteter Evidenz.

Plausibilität und Beweisstärke sind nicht dasselbe. Eine mechanistisch plausible Hypothese kann schwach belegt sein; ein gut belegter Einzelbefund kann nur eine sehr enge Aussage tragen.

## Claim-Klassifikationen

- **`fact`** — positive Tatsachenbehauptung;
- **`counterevidence`** — belastbarer Gegenbefund zu einer weitergehenden These;
- **`hypothesis`** — ausdrücklich zu prüfende Erklärung;
- **`interpretation`** — quellengebundene Einordnung;
- **`open_question`** — operationalisierbare offene Prüfungsfrage.

## Verpflichtender Challenge-Layer

Jeder Claim enthält neben seiner Stütze dieselben Prüffelder:

1. **Evidenz dafür** — welche Quelle trägt genau welche Aussage?
2. **Evidenz dagegen** — welche belastbare Quelle spricht gegen den Claim oder seine Reichweite?
3. **Alternativerklärungen** — welche andere Erklärung ist mit denselben Beobachtungen vereinbar?
4. **Beweislücken** — was fehlt für eine stärkere Aussage?
5. **Aussagegrenze** — was trägt die Evidenz und was ausdrücklich nicht?
6. **Falsifikation** — welcher Befund würde den Claim materiell schwächen oder widerlegen?

Diese Felder dürfen inhaltlich leer sein, aber nicht strukturell fehlen. Eine leere Liste bedeutet nur: **im aktuellen Datensatz ist nichts registriert**. Sie beweist weder die Abwesenheit von Gegenbelegen noch die Vollständigkeit der Recherche.

Damit wird Gegenprüfung nicht als nachträgliche Relativierung einer bereits gesetzten Erzählung behandelt, sondern gleichzeitig mit der Behauptung gespeichert.

## Quellenhierarchie

1. **A — Primärquellen:** Urteile, parlamentarische Untersuchungsausschüsse, amtliche Akten, deklassifizierte Dokumente, Kabinettsprotokolle, diplomatische Dokumente, zeitgenössische Originalunterlagen.
2. **B — hochwertige Forschung:** wissenschaftliche Monografien, Peer Review, unabhängige Historikerkommissionen, wissenschaftliche Editionsprojekte.
3. **C — investigative Recherche:** nachvollziehbar belegte journalistische Arbeiten, dokumentierte Interviews und investigative Bücher.
4. **D — Hinweise:** Presse ohne zugänglichen Originalbeleg, Memoiren, einzelne Zeugenaussagen, Blogs und Enzyklopädien.
5. **E — Leads:** Foren, Social Media und unbestätigte Behauptungen. Sie dienen zum Finden, nicht zum Beweisen.

Gewichtet wird nach Primärnähe, Methodik, Replizierbarkeit, Aktualität und Kontextpassung — nicht nach publizistischer Lautstärke.

### Strukturelle Mindestschwelle für `established`

Der Validator operationalisiert die stärkste Evidenzstufe konservativ. Ein als `established` markierter Claim braucht mindestens entweder:

- eine registrierte Tier-A-Quelle, die zugleich als Primärquelle markiert ist; oder
- mindestens zwei Tier-B/C-Quellen aus unterschiedlichen Institutionen.

Das ist nur eine maschinenprüfbare Mindestschwelle. Unterschiedliche Institutionen beweisen keine semantische Unabhängigkeit. Ob eine Quelle die konkrete Aussage tatsächlich trägt, wird zusätzlich durch die Claim-spezifische Belegnotiz und die inhaltliche Prüfung bewertet. Für Claims zählt `context` nicht zu dieser Mindestschwelle. Eine einzelne Tier-A-Primärquelle erfüllt sie nur mit `direct`; in der Mehrquellenroute zählen `direct` und `indirect`.

Auch `strong` braucht mindestens einen tragenden Stützbeleg mit `direct` oder `indirect`; reine `context`-Einträge dürfen den Kontext erklären, tragen aber keine `strong`-Evidenzstufe.

## Claim-spezifische Quellenbindung

Eine Quelle wird nicht nur über ihre stabile `SRC-...`-ID genannt. Jeder Claim beschreibt für seine Stütz- und Gegenbelege:

- die Quelle;
- die Direktheit: `direct`, `indirect` oder `context`;
- die relevante Fundstelle, soweit vorhanden;
- eine kurze Notiz, was die Quelle für diesen Claim tatsächlich trägt.

Die zentrale Quellenliste bleibt der Katalog der bibliografischen Wahrheit. Die Claim-Ebene dokumentiert ihre konkrete argumentative Verwendung.

Quellenlos dürfen nur `speculative` Hypothesen oder offene Fragen bleiben. Tatsachenbehauptungen, Interpretationen und Gegenbefunde benötigen Quellen. Tier-E-Leads dürfen niemals allein eine nicht-spekulative Aussage tragen.

## Relationen

Auch eine Kante im Netzwerkgraphen ist eine Behauptung und benötigt Quellen.

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

Jede Stufe verlangt zusätzliche Evidenz. Verbindung beweist keinen Einfluss; Einfluss beweist keine Steuerung.

## Verlinkungen zwischen Fällen

Fallverweise werden in zwei Klassen getrennt:

### Vergleich

`comparison` bedeutet, dass zwei Fälle für eine gemeinsame Fragestellung, einen Mechanismus, einen Akteur oder eine Struktur sinnvoll nebeneinander gelesen werden können.

Ein Vergleich behauptet **keine** operative Verbindung, gemeinsame Urheberschaft oder Kausalität.

### Dokumentierte Verbindung

`documented_connection` behauptet eine konkrete Verbindung zwischen zwei Fällen. Sie darf nur gesetzt werden, wenn eine quellengebundene Relation in `data/relations.yml` beide Fall-IDs direkt verbindet.

Fallverweise werden strukturell im Frontmatter gepflegt. Bei `documented_connection` prüft der Validator die direkte Relation zwischen beiden Fällen; sichtbare Verweise können im redaktionellen Falltext ergänzt werden.

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

## Terrorismus und politische Gewalt: getrennte Ebenen

Bei Terrorismus oder politischer Gewalt werden mindestens vier qualitativ verschiedene Ebenen unterschieden:

1. **Verwertung:** autonom entstandene Gewalt wird politisch für Sicherheitsbefugnisse, Überwachung, Repression oder institutionelle Veränderungen genutzt.
2. **Penetration / Management:** Dienste infiltrieren Milieus, führen Quellen, bezahlen Informanten oder schützen operative Zugänge.
3. **Provokation / Inszenierung:** staatliche Stellen erzeugen, provozieren oder imitieren einen Vorgang.
4. **Steuerung:** terroristische Akteure oder konkrete Anschläge werden aktiv dirigiert.

Ein Beleg für Ebene 1 oder 2 beweist nicht Ebene 3 oder 4.

## Prüfmatrix für einschlägige Fälle

Nach Relevanz werden getrennt geprüft:

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

Die Matrix ist ein Suchraster, keine Vorannahme, dass alle Punkte in einem Fall vorkommen.

## Strategie der Spannung

Der Begriff ist ein Hypothesen- und Vergleichsrahmen, keine universelle Erklärung. Er darf nicht als Abkürzung für die Behauptung dienen, ein bestimmter Staat, Dienst oder ausländischer Akteur habe jeden einzelnen Anschlag angeordnet.

Konkrete Täterschaft, Mitwisserschaft, Deckung, Depistaggio, Nachrichtendienstbeziehungen und politische Verwertung müssen getrennt belegt werden.

## Widersprüchliche Quellen

Widersprüche werden nicht geglättet.

Parlamentarische, behördliche oder politische Wertungen sind zunächst Aussagen der jeweiligen Institution. Eine Primärquelle belegt sicher, dass die Institution diese Aussage getroffen hat; sie ersetzt nicht automatisch die unabhängige Prüfung jedes historischen Sachverhalts innerhalb dieser Aussage.

Historische Quellen belegen zunächst den damaligen Wissens- und Entscheidungsstand. Spätere Aktenfunde oder Forschung können ihn korrigieren.

## Personen und Organisationen

Mitgliedschaften und Kontakte sind zunächst deskriptive Daten. Für Vorwürfe wie Korruption, Steuerung, illegale Einflussnahme oder Beteiligung an Gewalt gelten dieselben Quellenstandards wie für andere Tatsachenbehauptungen.

Bei Netzwerken, Vereinen, Thinktanks, Stiftungen und Konferenzen untersucht das Projekt konkrete Mitgliedschaften, Überschneidungen, Finanzierung, Drehtüren, Lobbykontakte, Interventionen und gegebenenfalls nachweisbare Interessenkonflikte.

## Ausführbare Methodik

Die Methodik ist nicht nur ein Styleguide.

- `schemas/` erzwingt die erforderlichen Felder;
- `scripts/validate.py` prüft Quellenbindung, Claim-Regeln, Fallverweise, Relationstypen sowie die sichtbare Spiegelung von Claim-ID und Claim-Wortlaut im Falltext;
- `scripts/build_indexes.py` erzeugt die abgeleiteten Indizes aus denselben strukturierten Daten;
- Tests prüfen auch negative Fälle und Umgehungsversuche;
- CI blockiert Änderungen, wenn Daten, generierte Seiten oder Website nicht konsistent sind.

Damit kann ein späterer Thread oder Autor die Gegenprüfung nicht versehentlich durch eine andere Seitendramaturgie verdrängen.

## Reproduzierbarkeit

Git ist die kanonische Wahrheit.

- Fallakten: Markdown mit maschinenlesbarem Frontmatter;
- Quellen: `data/sources.yml`;
- Entitäten: `data/entities.yml`;
- Mechanismen: `data/mechanisms.yml`;
- Relationen: `data/relations.yml`;
- Schemas: `schemas/`;
- Validator: `scripts/validate.py`;
- Indexgenerator: `scripts/build_indexes.py`.

Das Frontmatter ist die kanonische Bewertungsstruktur. Falltexte bleiben redaktionelle Darstellung, müssen aber Claim-IDs und Claim-Aussagen daraus sichtbar spiegeln. Timeline, Netzwerk und weitere Indizes werden aus denselben strukturierten Daten erzeugt.
