# Beitragen

Beiträge sind willkommen, wenn sie die Nachprüfbarkeit erhöhen. Eine starke Behauptung muss so formuliert und belegt sein, dass ihre Grundlage und ihre Grenzen geprüft werden können.

## Grundregeln

- Die Evidenzstufe gehört zum Claim, nicht zum Fall als Ganzes.
- Konkrete Tatsachenbehauptungen brauchen nachvollziehbare Quellen.
- Primärquellen und amtliche Originaldokumente werden bevorzugt.
- Hypothesen müssen ausdrücklich als Hypothesen oder offene Fragen markiert werden.
- Gegenbelege, alternative Erklärungen und widersprüchliche Quellen dürfen nicht unterschlagen werden.
- Jeder Claim führt Stütze, Gegenbelege, Alternativerklärungen, Beweislücken, Aussagegrenze und ein prüfbares Falsifikationskriterium.
- Eine leere Gegenbeleg- oder Alternativenliste behauptet keine Vollständigkeit der Recherche.
- Eine Mitgliedschaft, Bekanntschaft, Konferenzteilnahme oder institutionelle Nähe ist für sich genommen kein Nachweis für Einfluss, Fehlverhalten, Rechtsbruch oder Steuerung.
- Politischer oder institutioneller Nutzen beweist weder Motiv noch Absicht noch Urheberschaft.
- Keine Schuldbehauptungen über Personen ohne belastbare Grundlage.
- Personenkritik sachlich und quellengebunden formulieren.
- Keine Doxxing-Inhalte, privaten Adressen, Zugangsdaten oder nichtöffentlichen personenbezogenen Daten.
- Keine urheberrechtlich problematischen Volltexte. Bei Zweifeln nur Metadaten, zulässige Kurzzitate und externe Fundstellen erfassen.
- Stabile IDs nicht ohne dokumentierte Migration ändern.
- Stufe-E-Leads dürfen Fundstellen liefern, aber niemals allein einen nicht-spekulativen Claim tragen.

## Neuer Fall

1. Fallakte unter `docs/faelle/<land>/` anlegen.
2. Forschungsfrage erfassen und zentrale Aussagen atomar als Claims anlegen.
3. Den gesicherten Ereigniskern ausschließlich über `event_claims` auf fallinterne `fact`-Claims mit `established` oder `strong` verweisen lassen.
4. Für jeden Claim Stütze, Gegenbelege, Alternativerklärungen, Beweislücken, Aussagegrenze und Falsifikation ausfüllen.
5. Fallweite Synthesen unter `what_follows` und `what_does_not_follow` an die fallinternen Claims binden, aus denen sie abgeleitet werden.
6. Quellen zuerst in `data/sources.yml` registrieren und im Claim ihre konkrete Rolle beschreiben.
7. Neue Akteure in `data/entities.yml` anlegen.
8. Neue Mechanismen nur bei tatsächlichem Bedarf in `data/mechanisms.yml` ergänzen.
9. Beziehungen ausschließlich quellengebunden in `data/relations.yml` eintragen.
10. Fallverweise als `comparison` oder `documented_connection` klassifizieren. Letztere brauchen eine direkte Relation zwischen beiden Fall-IDs.
11. Den redaktionellen Falltext so schreiben, dass jede Claim-ID und die zugehörige Claim-Aussage sichtbar gespiegelt werden.
12. `python scripts/build_indexes.py` ausführen, um die abgeleiteten Übersichten zu aktualisieren.
13. `python scripts/validate.py`, Tests, `python scripts/build_indexes.py --check` und `mkdocs build --strict` ausführen.

## Fallverknüpfungen

**Vergleich:** macht eine relevante Ähnlichkeit oder gemeinsame Untersuchungsachse sichtbar. Er behauptet keine Kausalität oder gemeinsame Steuerung.

**Dokumentierte Verbindung:** behauptet eine konkrete Verbindung und muss über `relation_id` an eine quellengebundene CASE→CASE-Relation gebunden sein.

## Evidenz

Die verbindliche Methodik steht in `METHODOLOGY.md`. Besonders wichtig:

- `established` ist nicht dasselbe wie `strong`;
- eine Primärquelle kann eine institutionelle oder politische Bewertung enthalten;
- eine Relation im Netzwerk ist selbst eine prüfbare Behauptung und benötigt Quellen;
- Gegenbelege werden nicht entfernt, nur weil sie eine attraktive Gesamterklärung schwächen;
- Plausibilität und Beweisstärke bleiben getrennte Fragen.

## Nicht ausreichend

- „Das ist allgemein bekannt.“
- Screenshots ohne Herkunft.
- bloße Namensgleichheit.
- gemeinsame Vereinsmitgliedschaft als Beweis für Steuerung.
- ein einzelner Social-Media-Post als Faktengrundlage.
- Sekundärartikel, wenn eine leicht zugängliche Primärquelle existiert.
- Zitate ohne Kontext oder Fundstelle.
- die Ableitung von Absicht aus bloßem Nutzen.
- die Ableitung zentraler Steuerung aus bloßer Infiltration;
- ein gemeinsamer Mechanismus in zwei Fällen als Beweis einer operativen Verbindung.

## Gute Issues

Ein gutes Issue enthält:

- die konkrete prüfbare Behauptung oder Frage;
- mögliche Primärquellen;
- die Relevanz für einen Fall, Mechanismus oder eine Relation;
- erkennbare Gegenargumente;
- die Information, die noch fehlt;
- einen sinnvollen nächsten Prüfschritt.
