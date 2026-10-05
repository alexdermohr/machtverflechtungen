# Netzwerk

_Automatisch aus data/relations.yml erzeugt. Jede Kante besitzt mindestens eine Quelle._

```mermaid
flowchart LR
    N_ORG_DE_NI_VERFASSUNGSSCHUTZ["Niedersächsischer Verfassungsschutz"]
    N_CASE_DE_CELLER_LOCH_1978["Celler Loch / Aktion Feuerzauber"]
    N_ORG_DE_NI_VERFASSUNGSSCHUTZ -->|"führte Aktion Feuerzauber durch"| N_CASE_DE_CELLER_LOCH_1978
    N_ORG_DE_ORGANISATION_GEHLEN["Organisation Gehlen"]
    N_ORG_DE_BND["Bundesnachrichtendienst"]
    N_ORG_DE_ORGANISATION_GEHLEN -->|"wurde 1956 in den BND überführt"| N_ORG_DE_BND
    N_PER_DE_REINHARD_GEHLEN["Reinhard Gehlen"]
    N_PER_DE_REINHARD_GEHLEN -->|"leitete"| N_ORG_DE_ORGANISATION_GEHLEN
    N_PER_DE_REINHARD_GEHLEN -->|"erster Präsident"| N_ORG_DE_BND
    N_ORG_DE_TLFV["Thüringer Landesamt für Verfassungsschutz"]
    N_PER_DE_TINO_BRANDT["Tino Brandt"]
    N_ORG_DE_TLFV -->|"führte und bezahlte als V-Mann"| N_PER_DE_TINO_BRANDT
    N_ORG_DE_THS["Thüringer Heimatschutz"]
    N_PER_DE_TINO_BRANDT -->|"setzte Geld und Sachmittel für Aufbau und Funktionieren ein"| N_ORG_DE_THS
    N_ORG_DE_ATLANTIK_BRUECKE["Atlantik-Brücke e.V."]
    N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS["Atlantik-Brücke Young Leaders Program"]
    N_ORG_DE_ATLANTIK_BRUECKE -->|"betreibt"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_MATHIAS_DOEPFNER["Mathias Döpfner"]
    N_ORG_INT_BILDERBERG_MEETINGS["Bilderberg Meetings"]
    N_PER_DE_MATHIAS_DOEPFNER -->|"Teilnehmer 2017"| N_ORG_INT_BILDERBERG_MEETINGS
    N_ORG_DE_AXEL_SPRINGER["Axel Springer SE"]
    N_PER_DE_MATHIAS_DOEPFNER -->|"CEO"| N_ORG_DE_AXEL_SPRINGER
    N_PER_DE_MATTHIAS_NASS["Matthias Naß"]
    N_PER_DE_MATTHIAS_NASS -->|"moderierte NATO-Diskussion"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_DIE_ZEIT["DIE ZEIT"]
    N_PER_DE_MATTHIAS_NASS -->|"Internationaler Korrespondent"| N_ORG_DE_DIE_ZEIT
    N_PER_DE_TINA_HASSEL["Tina Hassel"]
    N_PER_DE_TINA_HASSEL -->|"Gesprächspartnerin bei Deutsch-Amerikanischer Konferenz"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_ARD["ARD"]
    N_PER_DE_TINA_HASSEL -->|"Chefin des Hauptstadtbüros"| N_ORG_DE_ARD
    N_PER_DE_GEORG_MASCOLO["Georg Mascolo"]
    N_PER_DE_GEORG_MASCOLO -->|"Panelteilnehmer Deutsch-Amerikanische Konferenz"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_RECHERCHEVERBUND_NDR_WDR_SZ["Rechercheverbund NDR/WDR/Süddeutsche Zeitung"]
    N_PER_DE_GEORG_MASCOLO -->|"Leiter des investigativen Rechercheverbundes"| N_ORG_DE_RECHERCHEVERBUND_NDR_WDR_SZ
    N_PER_DE_TOM_BUHROW["Tom Buhrow"]
    N_PER_DE_TOM_BUHROW -->|"in Emersons Abschiedsrede direkt angesprochen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_GABOR_STEINGART["Gabor Steingart"]
    N_PER_DE_GABOR_STEINGART -->|"moderierte Gespräch zur US-Präsidentschaftswahl"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_HANDELSBLATT["Handelsblatt"]
    N_PER_DE_GABOR_STEINGART -->|"Vorsitzender der Geschäftsführung der Verlagsgruppe Handelsblatt"| N_ORG_DE_HANDELSBLATT
    N_PER_DE_SVEN_AFHUEPPE["Sven Afhüppe"]
    N_PER_DE_SVEN_AFHUEPPE -->|"als Mitglied bezeichnet"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_SVEN_AFHUEPPE -->|"moderierte Industrie-4.0-Veranstaltung"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_SVEN_AFHUEPPE -->|"Chefredakteur"| N_ORG_DE_HANDELSBLATT
    N_PER_DE_STEFAN_KORNELIUS["Stefan Kornelius"]
    N_PER_DE_STEFAN_KORNELIUS -->|"Gastredner bei Young Leaders-Konferenz"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_SUEDDEUTSCHE_ZEITUNG["Süddeutsche Zeitung"]
    N_PER_DE_STEFAN_KORNELIUS -->|"Ressortleiter Außenpolitik"| N_ORG_DE_SUEDDEUTSCHE_ZEITUNG
    N_PER_DE_KLAUS_DIETER_FRANKENBERGER["Klaus-Dieter Frankenberger"]
    N_PER_DE_KLAUS_DIETER_FRANKENBERGER -->|"Redner bei Deutsch-Amerikanischer Konferenz"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_FAZ["Frankfurter Allgemeine Zeitung"]
    N_PER_DE_KLAUS_DIETER_FRANKENBERGER -->|"Verantwortlicher Redakteur für Außenpolitik"| N_ORG_DE_FAZ
    N_PER_DE_KAI_DIEKMANN["Kai Diekmann"]
    N_PER_DE_KAI_DIEKMANN -->|"Vorstandsmitglied"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_KAI_DIEKMANN -->|"BILD-Chefredakteur und Herausgeber der BILD-Gruppe"| N_ORG_DE_AXEL_SPRINGER
    N_PER_DE_ELMAR_THEVESSEN["Elmar Theveßen"]
    N_PER_DE_ELMAR_THEVESSEN -->|"als Mitglied bezeichnet"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_ZDF["ZDF"]
    N_PER_DE_ELMAR_THEVESSEN -->|"Leiter ZDF-Studio Washington"| N_ORG_DE_ZDF
    N_PER_DE_CLAUS_KLEBER["Claus Kleber"]
    N_PER_DE_CLAUS_KLEBER -->|"als Moderator der Diskussion angekündigt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_MATTHIAS_NASS -->|"Teilnehmer des Young-Leaders-Jahrgangs 1984"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_THEO_KOLL["Theo Koll"]
    N_PER_DE_THEO_KOLL -->|"Teilnehmer des Young-Leaders-Jahrgangs 1988"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_PAUL_BERNHARD_KALLEN["Paul-Bernhard Kallen"]
    N_PER_DE_PAUL_BERNHARD_KALLEN -->|"Teilnehmer des Young-Leaders-Jahrgangs 1991"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_KAI_DIEKMANN -->|"Teilnehmer des Young-Leaders-Jahrgangs 1995"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_JOERG_SCHOENENBORN["Jörg Schönenborn"]
    N_PER_DE_JOERG_SCHOENENBORN -->|"Teilnehmer des Young-Leaders-Jahrgangs 2000"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_JULIA_JAEKEL["Julia Jäkel"]
    N_PER_DE_JULIA_JAEKEL -->|"Teilnehmerin des Young-Leaders-Jahrgangs 2002"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_ELMAR_THEVESSEN -->|"Teilnehmer des Young-Leaders-Jahrgangs 2003"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PER_DE_HUBERT_BURDA["Hubert Burda"]
    N_PER_DE_HUBERT_BURDA -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_JOSEF_JOFFE["Josef Joffe"]
    N_PER_DE_JOSEF_JOFFE -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_DIETER_VON_HOLTZBRINCK["Dieter von Holtzbrinck"]
    N_PER_DE_DIETER_VON_HOLTZBRINCK -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_STEFAN_VON_HOLTZBRINCK["Stefan von Holtzbrinck"]
    N_PER_DE_STEFAN_VON_HOLTZBRINCK -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_FRIEDE_SPRINGER["Friede Springer"]
    N_PER_DE_FRIEDE_SPRINGER -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_MATHIAS_DOEPFNER -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_KAI_DIEKMANN -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_JULIA_JAEKEL -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_THEO_KOLL -->|"im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_THOMAS_RABE["Thomas Rabe"]
    N_PER_DE_THOMAS_RABE -->|"bei gemeinsamem Atlantik-Brücke/Bertelsmann-Format dokumentiert"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_LIZ_MOHN["Liz Mohn"]
    N_PER_DE_LIZ_MOHN -->|"erhielt den XIV. Vernon A. Walters Award"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_ULRICH_WILHELM["Ulrich Wilhelm"]
    N_PER_DE_ULRICH_WILHELM -->|"Gastredner beim World-Young-Leaders-Treffen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_PETER_FREY["Peter Frey"]
    N_PER_DE_PETER_FREY -->|"Redner beim Frankfurt Luncheon zum Fernsehen in der digitalen Öffentlichkeit"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_JOERG_SCHOENENBORN -->|"Gesprächspartner des US-Botschafters Philip D. Murphy"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_KLAUS_DIETER_FRANKENBERGER -->|"gab eine Einführung bei der 79. Sitzung des Arbeitskreises USA"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_JOERG_QUOOS["Jörg Quoos"]
    N_PER_DE_JOERG_QUOOS -->|"Gesprächspartner einer von der Atlantik-Brücke organisierten Journalistenreise"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_INGO_ZAMPERONI["Ingo Zamperoni"]
    N_PER_DE_INGO_ZAMPERONI -->|"Teilnehmer eines Working Lunch mit Admiral James G. Stavridis"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_THOMAS_ROTH["Thomas Roth"]
    N_PER_DE_THOMAS_ROTH -->|"in der Dokumentation der Deutsch-Amerikanischen Konferenz 2015 aufgeführt"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_THEO_SOMMER["Theo Sommer"]
    N_PER_DE_THEO_SOMMER -->|"Gesprächspartner einer von der Atlantik-Brücke organisierten Journalistenreise"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_CLAUS_KLEBER -->|"hielt die XX. Karl-Heinz-Beckurts-Gedächtnisrede"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_THOMAS_EBELING["Thomas Ebeling"]
    N_PER_DE_THOMAS_EBELING -->|"Teilnehmer 2016"| N_ORG_INT_BILDERBERG_MEETINGS
    N_PER_DE_THEO_SOMMER -->|"früheres deutsches Steering-Committee-Mitglied; regelmäßige Teilnahme laut Interview von 2007"| N_ORG_INT_BILDERBERG_MEETINGS
    N_PER_DE_HUBERT_BURDA -->|"Teilnehmer der Bilderberg-Konferenz 2007"| N_ORG_INT_BILDERBERG_MEETINGS
    N_PER_DE_JOSEF_JOFFE -->|"Teilnehmer der Bilderberg-Konferenz 2006"| N_ORG_INT_BILDERBERG_MEETINGS
    N_PER_DE_MATTHIAS_NASS -->|"Teilnehmer der Bilderberg-Konferenz 2012"| N_ORG_INT_BILDERBERG_MEETINGS
    N_ORG_INT_TRILATERAL_COMMISSION["The Trilateral Commission"]
    N_PER_DE_KLAUS_DIETER_FRANKENBERGER -->|"in der Mitgliederliste der Trilateral Commission geführt"| N_ORG_INT_TRILATERAL_COMMISSION
    N_PER_DE_ERICH_SCHMIDT_EENBOOM["Erich Schmidt-Eenboom"]
    N_ORG_DE_BND -->|"Ausschussmehrheit bewertete die Observationen 1993 bis 1996 wegen Dauer und Intensität als unverhältnismäßig und rechtswidrig"| N_PER_DE_ERICH_SCHMIDT_EENBOOM
    N_PER_DE_VOLKER_FOERTSCH["Volker Foertsch"]
    N_CASE_DE_MEDIEN_NACHRICHTENDIENST_CROSSLAYER["Deutsche Medien: nachrichtendienstliche Eingriffe und verdeckte Finanzierung"]
    N_PER_DE_VOLKER_FOERTSCH -->|"Ausschuss stellte fest, dass er Einfluss auf Medienberichterstattung nahm; offenbar ohne Kenntnis und Billigung der BND-Hausleitung"| N_CASE_DE_MEDIEN_NACHRICHTENDIENST_CROSSLAYER
    N_ORG_DE_BND -->|"Sondervotum zitiert Foertsch/Schäfer zu Kontakt mit Mascolo, um BND-schädliche Veröffentlichungen verhindern zu können"| N_PER_DE_GEORG_MASCOLO
    N_ORG_US_CIA["Central Intelligence Agency"]
    N_ORG_INT_CONGRESS_CULTURAL_FREEDOM["Congress for Cultural Freedom"]
    N_ORG_US_CIA -->|"CIA-Hausgeschichte beschreibt den Congress for Cultural Freedom als verdeckte CIA-Operation"| N_ORG_INT_CONGRESS_CULTURAL_FREEDOM
    N_ORG_DE_DER_MONAT["Der Monat"]
    N_ORG_INT_CONGRESS_CULTURAL_FREEDOM -->|"laut Forschung wurden Zuschüsse aus CIA-Mitteln über den Congress an Der Monat geleitet"| N_ORG_DE_DER_MONAT
    N_ORG_DE_BND -->|"Ausschuss stellte in Einzelfällen Versuche fest, Journalisten von Veröffentlichungen abzuhalten; keine Anhaltspunkte für vom BND lancierte Zeitungsbeiträge"| N_CASE_DE_MEDIEN_NACHRICHTENDIENST_CROSSLAYER
```

## Relationen

| ID | Von | Beziehung | Zu | Evidenz | Quellen |
|---|---|---|---|---|---|
| REL-DE-CELLER-001 | Niedersächsischer Verfassungsschutz | führte Aktion Feuerzauber durch | Celler Loch / Aktion Feuerzauber | established | SRC-DE-NI-MJ-CELLER-2015 |
| REL-DE-GEHLEN-001 | Organisation Gehlen | wurde 1956 in den BND überführt | Bundesnachrichtendienst | strong | SRC-DE-BPB-BND-2026 |
| REL-DE-GEHLEN-002 | Reinhard Gehlen | leitete | Organisation Gehlen | strong | SRC-DE-BPB-BND-2026 |
| REL-DE-GEHLEN-003 | Reinhard Gehlen | erster Präsident | Bundesnachrichtendienst | strong | SRC-DE-BPB-BND-2026 |
| REL-DE-THS-001 | Thüringer Landesamt für Verfassungsschutz | führte und bezahlte als V-Mann | Tino Brandt | established | SRC-DE-THLT-NSU-UA-2014 |
| REL-DE-THS-002 | Tino Brandt | setzte Geld und Sachmittel für Aufbau und Funktionieren ein | Thüringer Heimatschutz | established | SRC-DE-THLT-NSU-UA-2014 |
| REL-DE-AB-001 | Atlantik-Brücke e.V. | betreibt | Atlantik-Brücke Young Leaders Program | established | SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-001 | Mathias Döpfner | Teilnehmer 2017 | Bilderberg Meetings | established | SRC-INT-BILDERBERG-2017 |
| REL-DE-TMN-002 | Mathias Döpfner | CEO | Axel Springer SE | established | SRC-INT-BILDERBERG-2017 |
| REL-DE-TMN-003 | Matthias Naß | moderierte NATO-Diskussion | Atlantik-Brücke e.V. | established | SRC-DE-AB-NASS-NATO-2016, SRC-INT-NATO-WARSAW-SUMMIT-2016 |
| REL-DE-TMN-004 | Matthias Naß | Internationaler Korrespondent | DIE ZEIT | established | SRC-DE-AB-NASS-NATO-2016, SRC-INT-NATO-WARSAW-SUMMIT-2016 |
| REL-DE-TMN-005 | Tina Hassel | Gesprächspartnerin bei Deutsch-Amerikanischer Konferenz | Atlantik-Brücke e.V. | established | SRC-DE-AB-CONFERENCE-2017 |
| REL-DE-TMN-006 | Tina Hassel | Chefin des Hauptstadtbüros | ARD | established | SRC-DE-AB-CONFERENCE-2017 |
| REL-DE-TMN-007 | Georg Mascolo | Panelteilnehmer Deutsch-Amerikanische Konferenz | Atlantik-Brücke e.V. | established | SRC-DE-AB-CONFERENCE-2017 |
| REL-DE-TMN-008 | Georg Mascolo | Leiter des investigativen Rechercheverbundes | Rechercheverbund NDR/WDR/Süddeutsche Zeitung | established | SRC-DE-AB-CONFERENCE-2017 |
| REL-DE-TMN-009 | Tom Buhrow | in Emersons Abschiedsrede direkt angesprochen | Atlantik-Brücke e.V. | established | SRC-DE-AB-BUHROW-2017 |
| REL-DE-TMN-010 | Gabor Steingart | moderierte Gespräch zur US-Präsidentschaftswahl | Atlantik-Brücke e.V. | established | SRC-DE-AB-STEINGART-2016 |
| REL-DE-TMN-011 | Gabor Steingart | Vorsitzender der Geschäftsführung der Verlagsgruppe Handelsblatt | Handelsblatt | established | SRC-DE-AB-STEINGART-2016 |
| REL-DE-TMN-012 | Sven Afhüppe | als Mitglied bezeichnet | Atlantik-Brücke e.V. | established | SRC-DE-HMG-AFHUEPPE-2014 |
| REL-DE-TMN-013 | Sven Afhüppe | moderierte Industrie-4.0-Veranstaltung | Atlantik-Brücke e.V. | established | SRC-DE-AB-AFHUEPPE-2016 |
| REL-DE-TMN-014 | Sven Afhüppe | Chefredakteur | Handelsblatt | established | SRC-DE-AB-AFHUEPPE-2016 |
| REL-DE-TMN-015 | Stefan Kornelius | Gastredner bei Young Leaders-Konferenz | Atlantik-Brücke e.V. | established | SRC-DE-AB-KORNELIUS-YL-2016 |
| REL-DE-TMN-016 | Stefan Kornelius | Ressortleiter Außenpolitik | Süddeutsche Zeitung | established | SRC-DE-AB-KORNELIUS-YL-2016 |
| REL-DE-TMN-017 | Klaus-Dieter Frankenberger | Redner bei Deutsch-Amerikanischer Konferenz | Atlantik-Brücke e.V. | established | SRC-DE-AB-FRANKENBERGER-2018, SRC-US-ACG-ANNUAL-2018 |
| REL-DE-TMN-018 | Klaus-Dieter Frankenberger | Verantwortlicher Redakteur für Außenpolitik | Frankfurter Allgemeine Zeitung | established | SRC-DE-AB-FRANKENBERGER-2018, SRC-US-ACG-ANNUAL-2018 |
| REL-DE-TMN-019 | Kai Diekmann | Vorstandsmitglied | Atlantik-Brücke e.V. | established | SRC-DE-AB-DIEKMANN-2021 |
| REL-DE-TMN-020 | Kai Diekmann | BILD-Chefredakteur und Herausgeber der BILD-Gruppe | Axel Springer SE | established | SRC-DE-AXELSPRINGER-DIEKMANN-2015 |
| REL-DE-TMN-021 | Elmar Theveßen | als Mitglied bezeichnet | Atlantik-Brücke e.V. | established | SRC-DE-AB-THEVESSEN-2024 |
| REL-DE-TMN-022 | Elmar Theveßen | Leiter ZDF-Studio Washington | ZDF | established | SRC-DE-AB-THEVESSEN-2024 |
| REL-DE-TMN-023 | Claus Kleber | als Moderator der Diskussion angekündigt | Atlantik-Brücke e.V. | established | SRC-DE-AB-KLEBER-2026 |
| REL-DE-TMN-024 | Matthias Naß | Teilnehmer des Young-Leaders-Jahrgangs 1984 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-025 | Theo Koll | Teilnehmer des Young-Leaders-Jahrgangs 1988 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-026 | Paul-Bernhard Kallen | Teilnehmer des Young-Leaders-Jahrgangs 1991 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-027 | Kai Diekmann | Teilnehmer des Young-Leaders-Jahrgangs 1995 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-028 | Jörg Schönenborn | Teilnehmer des Young-Leaders-Jahrgangs 2000 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-029 | Julia Jäkel | Teilnehmerin des Young-Leaders-Jahrgangs 2002 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-030 | Elmar Theveßen | Teilnehmer des Young-Leaders-Jahrgangs 2003 | Atlantik-Brücke Young Leaders Program | established | SRC-US-ACG-YL-LIST-1973-2025, SRC-DE-ATLANTIKBRUECKE-YL |
| REL-DE-TMN-031 | Hubert Burda | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-032 | Josef Joffe | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-033 | Dieter von Holtzbrinck | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-034 | Stefan von Holtzbrinck | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-035 | Friede Springer | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-036 | Mathias Döpfner | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-037 | Kai Diekmann | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-038 | Julia Jäkel | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-039 | Theo Koll | im 2003-Faksimile als beitragende Person im Kreis von Mitgliedern und Freunden aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-MESSAGE-2003-MIRROR |
| REL-DE-TMN-040 | Thomas Rabe | bei gemeinsamem Atlantik-Brücke/Bertelsmann-Format dokumentiert | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2014-2015 |
| REL-DE-TMN-041 | Liz Mohn | erhielt den XIV. Vernon A. Walters Award | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2008-2009 |
| REL-DE-TMN-042 | Ulrich Wilhelm | Gastredner beim World-Young-Leaders-Treffen | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2006-2007 |
| REL-DE-TMN-043 | Peter Frey | Redner beim Frankfurt Luncheon zum Fernsehen in der digitalen Öffentlichkeit | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2014-2015 |
| REL-DE-TMN-044 | Jörg Schönenborn | Gesprächspartner des US-Botschafters Philip D. Murphy | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2011-2012 |
| REL-DE-TMN-045 | Klaus-Dieter Frankenberger | gab eine Einführung bei der 79. Sitzung des Arbeitskreises USA | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2009-2010 |
| REL-DE-TMN-046 | Jörg Quoos | Gesprächspartner einer von der Atlantik-Brücke organisierten Journalistenreise | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2009-2010 |
| REL-DE-TMN-047 | Ingo Zamperoni | Teilnehmer eines Working Lunch mit Admiral James G. Stavridis | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2011-2012 |
| REL-DE-TMN-048 | Thomas Roth | in der Dokumentation der Deutsch-Amerikanischen Konferenz 2015 aufgeführt | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2015-2016 |
| REL-DE-TMN-049 | Theo Sommer | Gesprächspartner einer von der Atlantik-Brücke organisierten Journalistenreise | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2009-2010 |
| REL-DE-TMN-050 | Claus Kleber | hielt die XX. Karl-Heinz-Beckurts-Gedächtnisrede | Atlantik-Brücke e.V. | strong | SRC-DE-AB-JB-2006-2007 |
| REL-DE-TMN-051 | Thomas Ebeling | Teilnehmer 2016 | Bilderberg Meetings | strong | SRC-INT-BILDERBERG-2016-ARCHIVE |
| REL-DE-TMN-052 | Theo Sommer | früheres deutsches Steering-Committee-Mitglied; regelmäßige Teilnahme laut Interview von 2007 | Bilderberg Meetings | strong | SRC-INT-BILDERBERG-FORMER-STEERING, SRC-DE-MESSAGE-SOMMER-BILDERBERG-2007 |
| REL-DE-TMN-053 | Hubert Burda | Teilnehmer der Bilderberg-Konferenz 2007 | Bilderberg Meetings | strong | SRC-INT-BILDERBERG-2007-ARCHIVE |
| REL-DE-TMN-054 | Josef Joffe | Teilnehmer der Bilderberg-Konferenz 2006 | Bilderberg Meetings | strong | SRC-INT-BILDERBERG-2006-ARCHIVE |
| REL-DE-TMN-055 | Matthias Naß | Teilnehmer der Bilderberg-Konferenz 2012 | Bilderberg Meetings | strong | SRC-INT-BILDERBERG-2012-ARCHIVE |
| REL-DE-TMN-056 | Klaus-Dieter Frankenberger | in der Mitgliederliste der Trilateral Commission geführt | The Trilateral Commission | strong | SRC-INT-TRILATERAL-2017-MIRROR |
| REL-DE-MNI-001 | Bundesnachrichtendienst | Ausschussmehrheit bewertete die Observationen 1993 bis 1996 wegen Dauer und Intensität als unverhältnismäßig und rechtswidrig | Erich Schmidt-Eenboom | established | SRC-DE-BT-UA-BND-JOURNALISTEN-2009 |
| REL-DE-MNI-004 | Volker Foertsch | Ausschuss stellte fest, dass er Einfluss auf Medienberichterstattung nahm; offenbar ohne Kenntnis und Billigung der BND-Hausleitung | Deutsche Medien: nachrichtendienstliche Eingriffe und verdeckte Finanzierung | established | SRC-DE-BT-UA-BND-JOURNALISTEN-2009 |
| REL-DE-MNI-005 | Bundesnachrichtendienst | Sondervotum zitiert Foertsch/Schäfer zu Kontakt mit Mascolo, um BND-schädliche Veröffentlichungen verhindern zu können | Georg Mascolo | strong | SRC-DE-BT-UA-BND-JOURNALISTEN-2009 |
| REL-DE-MNI-006 | Central Intelligence Agency | CIA-Hausgeschichte beschreibt den Congress for Cultural Freedom als verdeckte CIA-Operation | Congress for Cultural Freedom | strong | SRC-US-CIA-CCF-HISTORY-1995 |
| REL-DE-MNI-008 | Congress for Cultural Freedom | laut Forschung wurden Zuschüsse aus CIA-Mitteln über den Congress an Der Monat geleitet | Der Monat | strong | SRC-INT-SCOTT-SMITH-DER-MONAT-2000 |
| REL-DE-MNI-012 | Bundesnachrichtendienst | Ausschuss stellte in Einzelfällen Versuche fest, Journalisten von Veröffentlichungen abzuhalten; keine Anhaltspunkte für vom BND lancierte Zeitungsbeiträge | Deutsche Medien: nachrichtendienstliche Eingriffe und verdeckte Finanzierung | established | SRC-DE-BT-UA-BND-JOURNALISTEN-2009 |
