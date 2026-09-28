# Beitragen

Beiträge sind willkommen, wenn sie die Nachprüfbarkeit erhöhen. Machtverflechtungen ist kein Anschuldigungsarchiv: Eine starke Behauptung muss so formuliert und belegt sein, dass auch ein skeptischer Leser ihre Grundlage prüfen kann.

## Grundregeln

- Konkrete Tatsachenbehauptungen brauchen nachvollziehbare Quellen.
- Primärquellen und amtliche Originaldokumente werden bevorzugt.
- Hypothesen müssen ausdrücklich als Hypothesen oder offene Fragen markiert werden.
- Gegenbelege, alternative Erklärungen und widersprüchliche Quellen dürfen nicht unterschlagen werden.
- Eine Mitgliedschaft, Bekanntschaft, Konferenzteilnahme oder institutionelle Nähe ist für sich genommen kein Nachweis für Einfluss, Fehlverhalten, Rechtsbruch oder Steuerung.
- Politischer oder institutioneller Nutzen beweist weder Motiv noch Absicht noch Urheberschaft.
- Keine Schuldbehauptungen über Personen ohne belastbare Grundlage.
- Personenkritik sachlich und quellengebunden formulieren.
- Keine Doxxing-Inhalte, privaten Adressen, Zugangsdaten oder nichtöffentlichen personenbezogenen Daten.
- Keine urheberrechtlich problematischen Volltexte. Bei Zweifeln nur Metadaten, zulässige Kurzzitate und externe Fundstellen erfassen.
- Stabile IDs nicht ohne dokumentierte Migration ändern.
- Stufe-E-Leads dürfen Fundstellen liefern, aber niemals allein einen Fakt tragen.

## Neuer Fall

1. Fallakte unter `docs/faelle/<land>/` anlegen.
2. Frontmatter vollständig ausfüllen.
3. Zentrale Aussagen als Claims erfassen.
4. Quellen zuerst in `data/sources.yml` registrieren.
5. Neue Akteure in `data/entities.yml` anlegen.
6. Neue Mechanismen nur bei tatsächlichem Bedarf in `data/mechanisms.yml` ergänzen.
7. Beziehungen ausschließlich quellengebunden in `data/relations.yml` eintragen.
8. Befunde, Gegenbefunde, alternative Erklärungen und offene Prüfungen im Falltext sichtbar machen.
9. `python scripts/validate.py` ausführen.
10. `python scripts/build_indexes.py` und anschließend `python scripts/build_indexes.py --check` ausführen.
11. `mkdocs build --strict` ausführen.

## Evidenz

Die verbindliche Methodik steht in `METHODOLOGY.md`. Besonders wichtig:

- `established` ist nicht dasselbe wie `strong`;
- eine Primärquelle kann eine institutionelle oder politische Bewertung enthalten;
- eine Relation im Netzwerk ist selbst eine prüfbare Behauptung und benötigt Quellen;
- Gegenbelege werden nicht entfernt, nur weil sie eine attraktive Gesamterklärung schwächen.

## Nicht ausreichend

- „Das ist allgemein bekannt.“
- Screenshots ohne Herkunft.
- bloße Namensgleichheit.
- gemeinsame Vereinsmitgliedschaft als Beweis für Steuerung.
- ein einzelner Social-Media-Post als Faktengrundlage.
- Sekundärartikel, wenn eine leicht zugängliche Primärquelle existiert.
- Zitate ohne Kontext oder Fundstelle.
- die Ableitung von Absicht aus bloßem Nutzen.
- die Ableitung zentraler Steuerung aus bloßer Infiltration.

## Gute Issues

Ein gutes Issue enthält:

- die konkrete prüfbare Behauptung oder Frage;
- mögliche Primärquellen;
- die Relevanz für einen Fall, Mechanismus oder eine Relation;
- erkennbare Gegenargumente;
- die Information, die noch fehlt;
- einen sinnvollen nächsten Prüfschritt.
