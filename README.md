# Machtverflechtungen

**Quellengebundene Dokumentation staatlicher, geheimdienstlicher, politischer und wirtschaftlicher Machtverflechtungen.**

Machtverflechtungen ist ein öffentliches Rechercheprojekt. Es sammelt überprüfbare Fälle, Akteure, Organisationen, Mechanismen, Beziehungen und Quellen zu Staatskriminalität, verdeckten Operationen, staatlich beeinflussten Extremismusmilieus, Überwachung, Lobbyismus, wirtschaftlich-politischen Verflechtungen und informellen Einflussnetzwerken.

> Eine interessante Hypothese ist ein Forschungsauftrag, kein Beweis.

## Website

https://alexdermohr.github.io/machtverflechtungen/

## Arbeitsregeln

- Die bewertete Einheit ist der konkrete Claim, nicht der Fall als Ganzes.
- Der gesicherte Ereigniskern verweist nur auf fallinterne `fact`-Claims mit `established` oder `strong`.
- Fallweite Synthesen („folgt / folgt nicht“) nennen die Claims, aus denen sie abgeleitet werden.
- Primärquellen zuerst; jede registrierte Quelle bleibt über eine reale Seite oder ein PDF prüfbar.
- Tatsache, Interpretation, Gegenbeleg, Hypothese und offene Frage werden getrennt.
- Belegt / stark gestützt / plausibel / spekulativ / widersprochen werden nicht vermischt.
- Jeder Claim führt Stütze, Gegenbelege, Alternativerklärungen, Beweislücken, Aussagegrenze und Falsifikationskriterium mit.
- Leere Gegenprüfungsfelder bedeuten nur „im Datensatz nicht registriert“, nicht „existiert nicht“.
- Mitgliedschaft, Bekanntschaft oder Netzwerknähe beweisen keine Steuerung, Korruption oder Straftat.
- Politischer oder institutioneller Nutzen beweist weder Motiv noch Absicht noch Urheberschaft.
- Eine dokumentierte Fall-zu-Fall-Verbindung braucht eine quellengebundene Relation. Ein Vergleichslink behauptet keine Kausalität.
- Das Frontmatter ist die kanonische Bewertungsstruktur; der Validator erzwingt, dass Claim-ID und Claim-Wortlaut im sichtbaren Falltext gespiegelt bleiben.
- Timeline, Netzwerk und weitere Indizes werden aus denselben strukturierten Forschungsdaten erzeugt und von CI auf Drift geprüft.

## Startbestand

Die erste Version testet das Modell an bewusst unterschiedlichen Gegenständen:

1. Celler Loch / Aktion Feuerzauber
2. Technischer Dienst des Bund Deutscher Jugend
3. Organisation Gehlen und früher BND
4. Thüringer Heimatschutz / Tino Brandt
5. Piazza Fontana / Strategie der Spannung

Zusätzlich zeigt die Atlantik-Brücke exemplarisch, wie ein legales transnationales Kontakt- und Austauschnetzwerk modelliert werden kann, ohne aus Vernetzung automatisch illegitime Steuerung abzuleiten.

## Architektur

```text
Fallakte (Markdown + Frontmatter)
        │
        ├── Claims ─────────────> Stütze · Gegenbeleg · Alternativen · Grenzen
        ├── Quellen-IDs ────────> data/sources.yml
        ├── Akteur-IDs ─────────> data/entities.yml
        ├── Mechanismen ────────> data/mechanisms.yml
        └── Beziehungen ────────> data/relations.yml
                                  │
                         scripts/validate.py
                                  │
                         scripts/build_indexes.py
                                  │
               Timeline · Netzwerk · weitere Indizes
                                  │
                             MkDocs Material
```

Git bleibt die kanonische Wahrheit. Das Frontmatter trägt die maschinenlesbare Bewertung; der Falltext bleibt die lesbare Darstellung. Der Validator koppelt beide Ebenen über Claim-ID und normalisierten Claim-Wortlaut. Abgeleitete Übersichten werden aus denselben Daten erzeugt.

## Evidenz und Quellen

Die ausführliche Methodik steht in [METHODOLOGY.md](METHODOLOGY.md). Kurz:

- **established / belegt** — direkter Primärbeleg oder mehrere unabhängige hochwertige Belege;
- **strong / stark gestützt** — starke Indizienkette mit mindestens einem indirekten Glied;
- **plausible / plausibel** — gute Erklärung, ernsthafte Alternativen bleiben;
- **speculative / offen** — prüfbarer Verdacht mit unzureichender Evidenz;
- **contradicted / widersprochen** — die konkrete Behauptung kollidiert mit höher gewichteter Evidenz.

Quellen werden von **A (Primärquelle)** bis **E (Lead)** klassifiziert. Stufe E darf Fundstellen liefern, aber niemals allein einen nicht-spekulativen Claim tragen.

## Lokal prüfen

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build_indexes.py
python scripts/build_indexes.py --check
python -m unittest discover -s tests -p 'test_*.py'
mkdocs build --strict
```

## Mitwirken

Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Neue Behauptungen brauchen nachvollziehbare Quellen; Hypothesen müssen als solche markiert und Gegenbelege sichtbar gehalten werden.

## Lizenz

Forschungsdokumentation und strukturierte Daten: **CC BY 4.0**.

Code und technische Konfiguration: **MIT**.

Siehe [LICENSE](LICENSE). Rechte Dritter an verlinkten Quellen und Materialien bleiben unberührt.
