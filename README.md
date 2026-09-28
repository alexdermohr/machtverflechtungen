# Machtverflechtungen

**Quellengebundene Dokumentation staatlicher, geheimdienstlicher, politischer und wirtschaftlicher Machtverflechtungen.**

Machtverflechtungen ist ein öffentliches Rechercheprojekt. Es sammelt überprüfbare Fälle, Akteure, Organisationen, Mechanismen, Beziehungen und Quellen zu Staatskriminalität, verdeckten Operationen, staatlich beeinflussten Extremismusmilieus, Überwachung, Lobbyismus, wirtschaftlich-politischen Verflechtungen und informellen Einflussnetzwerken.

> Eine interessante Hypothese ist ein Forschungsauftrag, kein Beweis.

## Website

https://alexdermohr.github.io/machtverflechtungen/

## Arbeitsregeln

- Primärquellen zuerst.
- Tatsache, Interpretation, Gegenbeleg und Hypothese werden getrennt.
- Belegt / stark gestützt / plausibel / spekulativ / widersprochen werden nicht vermischt.
- Gegenbelege und alternative Erklärungen gehören zur Fallakte.
- Mitgliedschaft, Bekanntschaft oder Netzwerknähe beweisen keine Steuerung, Korruption oder Straftat.
- Politischer oder institutioneller Nutzen beweist weder Motiv noch Absicht noch Urheberschaft.
- Jede belastende Netzwerkrelation benötigt mindestens eine Quelle.
- Die Website ist Darstellung; Markdown/YAML im Repository bleibt die nachvollziehbare Forschungsgrundlage.

## Startbestand

Die erste Version testet das Modell an bewusst unterschiedlichen Gegenständen:

1. Celler Loch / Aktion Feuerzauber
2. Technischer Dienst des Bund Deutscher Jugend
3. Organisation Gehlen und früher BND
4. Thüringer Heimatschutz / Tino Brandt
5. Piazza Fontana / Strategie der Spannung

Zusätzlich zeigt die Atlantik-Brücke exemplarisch, wie ein legales transnationales Kontakt- und Einflussnetzwerk modelliert werden kann, ohne aus Vernetzung automatisch illegitime Steuerung abzuleiten.

## Architektur

```text
Fallakte (Markdown + Frontmatter)
        │
        ├── Quellen-IDs ───────> data/sources.yml
        ├── Akteur-IDs ────────> data/entities.yml
        ├── Mechanismen ───────> data/mechanisms.yml
        └── Beziehungen ───────> data/relations.yml
                                  │
                         scripts/validate.py
                                  │
                         scripts/build_indexes.py
                                  │
                  Timeline · Netzwerk · Indizes
                                  │
                             MkDocs Material
```

Git bleibt zunächst die kanonische Wahrheit. Die öffentliche Seite, Timeline und das Netzwerk werden aus denselben Forschungsdaten erzeugt. Spätere Karten oder interaktive Graphen sollen ebenfalls daraus entstehen, statt eine zweite Datenwahrheit aufzubauen.

## Evidenz und Quellen

Die ausführliche Methodik steht in [METHODOLOGY.md](METHODOLOGY.md). Kurz:

- **established / belegt** — direkter Primärbeleg oder mehrere unabhängige hochwertige Belege;
- **strong / stark gestützt** — starke Indizienkette mit mindestens einem indirekten Glied;
- **plausible / plausibel** — gute Erklärung, ernsthafte Alternativen bleiben;
- **speculative / offen** — prüfbarer Verdacht mit unzureichender Evidenz;
- **contradicted / widersprochen** — die konkrete Behauptung kollidiert mit höher gewichteter Evidenz.

Quellen werden von **A (Primärquelle)** bis **E (Lead)** klassifiziert. Stufe E darf Fundstellen liefern, aber niemals allein einen Fakt tragen.

## Lokal prüfen

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build_indexes.py
python scripts/build_indexes.py --check
mkdocs build --strict
```

## Mitwirken

Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Neue Behauptungen brauchen nachvollziehbare Quellen; Hypothesen müssen als solche markiert und Gegenbelege sichtbar gehalten werden.

## Lizenz

Forschungsdokumentation und strukturierte Daten: **CC BY 4.0**.

Code und technische Konfiguration: **MIT**.

Siehe [LICENSE](LICENSE). Rechte Dritter an verlinkten Quellen und Materialien bleiben unberührt.