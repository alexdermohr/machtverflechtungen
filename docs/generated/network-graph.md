# Netzwerkdiagramm

**344 Beziehungen** als grafische Gesamtübersicht. Die [alphabetische Relationstabelle](network.md) zeigt zusätzlich Evidenzstufen und Quellen.

## Direkte Verbindungen im Fokus

Diese Ausschnitte zeigen nur die unmittelbar dokumentierten Beziehungen des gewählten Akteurs. Weitere Beziehungen oder eine gemeinsame Steuerung sind daraus nicht automatisch ableitbar.

- [Atlantik-Brücke](network-focus-atlantik-bruecke.md) — 49 direkte Beziehungen
- [Bilderberg Meetings](network-focus-bilderberg.md) — 10 direkte Beziehungen
- [Organisation Gehlen](network-focus-organisation-gehlen.md) — 6 direkte Beziehungen
- [Bund Deutscher Jugend](network-focus-bdj.md) — 6 direkte Beziehungen
- [BAFISUD](network-focus-bafisud.md) — 5 direkte Beziehungen
- [BIZ / BIS](network-focus-biz.md) — 7 direkte Beziehungen
- [I.G. Farben](network-focus-ig-farben.md) — 6 direkte Beziehungen
- [ENI / Tradinvest](network-focus-tradinvest.md) — 7 direkte Beziehungen
- [M.M.Warburg / Eigentum & Aufsicht](network-focus-warburg-kontrolle.md) — 9 direkte Beziehungen
- [Warburg Pincus / ERISA 1979](network-focus-warburg-pincus-erisa.md) — 2 direkte Beziehungen
- [Döpfner / Springer](network-focus-springer-doepfner.md) — 8 direkte Beziehungen
- [P2 / Loge](network-focus-p2.md) — 3 direkte Beziehungen
- [Rizzoli / Corriere](network-focus-rizzoli.md) — 9 direkte Beziehungen
- [UBS Genf / Bologna 1980](network-focus-ubs-genf-1980.md) — 3 direkte Beziehungen

## Gesamtnetzwerk

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
    N_ORG_DE_HH_FINANZVERWALTUNG["Hamburger Finanzverwaltung"]
    N_ORG_DE_MM_WARBURG["M. M. Warburg & CO"]
    N_ORG_DE_HH_FINANZVERWALTUNG -->|"forderte Cum-Ex-Steuererstattungen 2020 vollständig zurück"| N_ORG_DE_MM_WARBURG
    N_PER_DE_OLAF_SCHOLZ["Olaf Scholz"]
    N_PER_DE_CHRISTIAN_OLEARIUS["Christian Olearius"]
    N_PER_DE_OLAF_SCHOLZ -->|"Treffen am 10. November 2017 (Inhalt nicht dokumentiert)"| N_PER_DE_CHRISTIAN_OLEARIUS
    N_ORG_DE_BERLIN_VERFASSUNGSSCHUTZ["West-Berliner Landesamt für Verfassungsschutz"]
    N_PER_DE_PETER_URBACH["Peter Urbach"]
    N_ORG_DE_BERLIN_VERFASSUNGSSCHUTZ -->|"führte Urbach als Quelle im Umfeld der frühen Mahler-Baader-Meinhof-Gruppe; Nollau beschrieb den Informationswert 1972"| N_PER_DE_PETER_URBACH
    N_PER_DE_GUNDOLF_KOEHLER["Gundolf Köhler"]
    N_ORG_DE_WSG_HOFFMANN["Wehrsportgruppe Hoffmann"]
    N_PER_DE_GUNDOLF_KOEHLER -->|"Briefkontakt ab 1976 und zwei Übungen; kein bis 1980 reichender Kontakt belegt"| N_ORG_DE_WSG_HOFFMANN
    N_ORG_DE_BFV["Bundesamt für Verfassungsschutz"]
    N_CASE_DE_NSU_AKTEN_2011["NSU: Quellenführung, Operation Rennsteig und Aktenvernichtung 2011"]
    N_ORG_DE_BFV -->|"vernichtete nach der NSU-Aufdeckung mehrere V-Mann-Akten"| N_CASE_DE_NSU_AKTEN_2011
    N_PER_DE_ANDREAS_TEMME["Andreas Temme"]
    N_ORG_DE_LFV_HESSEN["Landesamt für Verfassungsschutz Hessen"]
    N_PER_DE_ANDREAS_TEMME -->|"war Mitarbeiter und V-Mann-Führer"| N_ORG_DE_LFV_HESSEN
    N_CASE_DE_NSU_YOZGAT_2006["NSU-Mord an Halit Yozgat: Andreas Temme, Quellenschutz und Ermittlungen"]
    N_ORG_DE_LFV_HESSEN -->|"verweigerte Aussagegenehmigungen für V-Personen im Zuge der Kasseler Mordermittlungen"| N_CASE_DE_NSU_YOZGAT_2006
    N_PER_DE_HANS_LANGEMANN["Hans Langemann"]
    N_PER_DE_WALTER_H_JONAS["Walter H. Jonas"]
    N_PER_DE_HANS_LANGEMANN -->|"veranlasste laut Minderheitenbericht 1977 drei Überweisungen über 17.000 DM für Jonas, davon 4.000 DM auf das von-Corneli-Konto"| N_PER_DE_WALTER_H_JONAS
    N_PER_DE_ARISTIDE_BRUNELLO["Aristide Brunello"]
    N_PER_DE_HANS_LANGEMANN -->|"überwies laut Minderheitenbericht 1978/1979 in drei Zuwendungen insgesamt 14.500 DM auf das Brunello-Konto"| N_PER_DE_ARISTIDE_BRUNELLO
    N_PER_DE_HANS_C_STAUFFENBERG["Hans C. Freiherr von Stauffenberg"]
    N_PER_DE_HANS_C_STAUFFENBERG -->|"waren laut Minderheitenbericht beide für das Brunello-Konto verfügungsberechtigt"| N_PER_DE_ARISTIDE_BRUNELLO
    N_PER_DE_HANS_C_STAUFFENBERG -->|"war laut Minderheitenbericht später anstelle Langemanns neben Jonas für dessen Konto verfügungsberechtigt"| N_PER_DE_WALTER_H_JONAS
    N_PER_DE_MANFRED_ROEDER["Manfred Roeder"]
    N_ORG_DE_DEUTSCHE_AKTIONSGRUPPEN["Deutsche Aktionsgruppen"]
    N_PER_DE_MANFRED_ROEDER -->|"leitete laut archivalischer Rekonstruktion die Anschlagsgruppe 1980"| N_ORG_DE_DEUTSCHE_AKTIONSGRUPPEN
    N_ORG_DE_DEUTSCHE_BUERGERINITIATIVE["Deutsche Bürgerinitiative"]
    N_PER_DE_MANFRED_ROEDER -->|"als Akteur der Deutschen Bürgerinitiative und ihrer berichteten Konteneingänge 1979/80 genannt"| N_ORG_DE_DEUTSCHE_BUERGERINITIATIVE
    N_PER_DE_HEINZ_LEMBKE["Heinz Lembke"]
    N_PER_DE_HEINZ_LEMBKE -->|"Kontakt zur Deutschen Bürgerinitiative laut Bundesregierung 1981"| N_ORG_DE_DEUTSCHE_BUERGERINITIATIVE
    N_PER_DE_ODFRIED_HEPP["Odfried Hepp"]
    N_PER_DE_HEINZ_LEMBKE -->|"Kontakt laut Bundestagsauskunft vom 25.11.1981"| N_PER_DE_ODFRIED_HEPP
    N_ORG_DE_DEUTSCH_RUSS_GEMEINSCHAFTSWERK["Deutsch-Russisches Gemeinschaftswerk"]
    N_PER_DE_MANFRED_ROEDER -->|"bei Gründung am 20.02.1993 laut Untersuchungsausschuss zum zweiten Vorsitzenden gewählt"| N_ORG_DE_DEUTSCH_RUSS_GEMEINSCHAFTSWERK
    N_ORG_DE_BUNDESWEHR["Bundeswehr"]
    N_ORG_DE_BUNDESWEHR -->|"überließ laut Ausschussbericht 1994 drei ausgesonderte Fahrzeuge und Werkzeuge unentgeltlich"| N_ORG_DE_DEUTSCH_RUSS_GEMEINSCHAFTSWERK
    N_PER_DE_MANFRED_ROEDER -->|"hielt laut Untersuchungsausschuss am 24.01.1995 Vortrag an der Führungsakademie"| N_ORG_DE_BUNDESWEHR
    N_PER_DE_NGUYEN_NGOC_CHAU["Nguyễn Ngọc Châu"]
    N_PER_DE_NGUYEN_NGOC_CHAU -->|"wurde am 22.08.1980 Opfer des Brandanschlags der Deutschen Aktionsgruppen in Hamburg-Billbrook"| N_ORG_DE_DEUTSCHE_AKTIONSGRUPPEN
    N_PER_DE_DO_ANH_LAN["Đỗ Anh Lân"]
    N_PER_DE_DO_ANH_LAN -->|"wurde Opfer des Brandanschlags am 22.08.1980; starb neun Tage später"| N_ORG_DE_DEUTSCHE_AKTIONSGRUPPEN
    N_ORG_DE_BDJ["Bund Deutscher Jugend"]
    N_ORG_DE_BDJ_TD["Technischer Dienst des Bundes Deutscher Jugend"]
    N_ORG_DE_BDJ -->|"Bundestagsausschuss bewertete 1953 die personelle und ideelle Überschneidung als weitgehend"| N_ORG_DE_BDJ_TD
    N_ORG_DE_BMG["Bundesministerium für gesamtdeutsche Fragen (1952)"]
    N_ORG_DE_BMG -->|"10.000 DM Bundeszuwendung für das BDJ-Pfingsttreffen 1952"| N_ORG_DE_BDJ
    N_ORG_DE_BMI["Bundesministerium des Innern (1952)"]
    N_ORG_DE_BMI -->|"6.000 DM aus BMI-Mitteln für den BDJ, laut Egidi 21.10.1952"| N_ORG_DE_BDJ
    N_ORG_DE_BFV -->|"BfV hatte laut Egidi seit September 1951 Berichte über TD-Übungen bei Wald-Michelbach"| N_ORG_DE_BDJ_TD
    N_ORG_US_US_ARMY_GERMANY["US-amerikanische Armeestellen in Deutschland (1952)"]
    N_ORG_US_US_ARMY_GERMANY -->|"Hoegner berichtete Ausbildung und Unterstützung des TD durch US-Armeestellen, nicht durch die US-Zivilverwaltung"| N_ORG_DE_BDJ_TD
    N_ORG_DE_STOSSTRUPP_BZ["Stoßtrupp gegen bolschewistische Zersetzung"]
    N_ORG_DE_DHS["Deutscher Heimatschutz (Erlangen, 1951–1953)"]
    N_ORG_DE_STOSSTRUPP_BZ -->|"Hoegner bezeichnete den Deutschen Heimatschutz am 29.10.1952 als Unterorganisation des eigenständigen Stoßtrupps"| N_ORG_DE_DHS
    N_ORG_DE_STOSSTRUPP_BZ -->|"Laut Hoegner waren führende Funktionäre des Stoßtrupps zugleich Funktionäre des BDJ"| N_ORG_DE_BDJ
    N_ORG_US_CIC["U.S. Counter Intelligence Corps (CIC)"]
    N_ORG_DE_DHS -->|"Bayerische Ermittler ordneten 1952 eine bei DHS-Werbung genannte Referenznummer einer CIC-Dienststelle zu"| N_ORG_US_CIC
    N_ORG_DE_HE_LANDESREGIERUNG["Hessische Landesregierung"]
    N_ORG_DE_HE_LANDESREGIERUNG -->|"Verbot des BDJ im hessischen Landesgebiet am 8. Januar 1953"| N_ORG_DE_BDJ
    N_ORG_DE_BY_MINISTERRAT["Bayerischer Ministerrat"]
    N_ORG_DE_BY_MINISTERRAT -->|"Bayerischer Ministerratsbeschluss 13.01.1953 gegen den Stoßtrupp; Vollzug gesondert nachprüfen"| N_ORG_DE_STOSSTRUPP_BZ
    N_ORG_DE_BY_MINISTERRAT -->|"Bayerischer Ministerratsbeschluss 13.01.1953 gegen den Deutschen Heimatschutz"| N_ORG_DE_DHS
    N_ORG_DE_BY_MINISTERRAT -->|"Bayerischer Ministerrat erklärte am 20.01.1953 den TD zur verfassungswidrigen Organisation, BDJ-Entscheidung vertagt"| N_ORG_DE_BDJ_TD
    N_ORG_DE_BUNDESANWALTSCHAFT["Bundesanwaltschaft (1952–1953)"]
    N_CASE_DE_BDJ_TD_1950S["Technischer Dienst des Bundes Deutscher Jugend"]
    N_ORG_DE_BUNDESANWALTSCHAFT -->|"Laut bayerischem Ministerratsprotokoll 20.01.1953 erwog der Bundesanwalt eine Verfahrenseinstellung"| N_CASE_DE_BDJ_TD_1950S
    N_ORG_DE_FRANKFURT_GSTA["Generalstaatsanwaltschaft Frankfurt am Main (1952–1953)"]
    N_ORG_DE_FRANKFURT_GSTA -->|"Laut bayerischem Ministerratsprotokoll beantragte die Generalstaatsanwaltschaft Frankfurt eine Voruntersuchung"| N_CASE_DE_BDJ_TD_1950S
    N_ORG_US_OPC["Office of Policy Coordination (OPC)"]
    N_ORG_US_OPC -->|"CIA-Projektbericht vom 24.01.1951 beschreibt OPC-Subvention des BDJ, nach außen als private und industrielle Geldgeberbeiträge dargestellt"| N_ORG_DE_BDJ
    N_ORG_DE_LFV_BRANDENBURG["Landesamt für Verfassungsschutz Brandenburg"]
    N_PER_DE_CARSTEN_SZCZEPANSKI["Carsten Szczepanski (Piatto)"]
    N_ORG_DE_LFV_BRANDENBURG -->|"Führte Piatto 1994–2000 als Informanten; sein formalrechtlicher V-Mann-Verpflichtungsstatus ist davon getrennt"| N_PER_DE_CARSTEN_SZCZEPANSKI
    N_ORG_GB_NSM_1990S["National Socialist Movement (britische C18-Abspaltung)"]
    N_PER_DE_CARSTEN_SZCZEPANSKI -->|"PSF 2224 der staatlich geführten Quelle wurde laut Parlament als deutsche Kontaktstelle des britischen NSM beworben; keine MI5-Kante"| N_ORG_GB_NSM_1990S
    N_ORG_DE_COMBAT18_2013["Combat 18 Deutschland (Vereinsstruktur ab 2013)"]
    N_PER_GB_WILLIAM_BROWNING["William Wilf Browning"]
    N_ORG_DE_COMBAT18_2013 -->|"BVerwG berücksichtigte 2020 regelmäßige Kontakte zu William Browning, keine britische Dienstanweisung"| N_PER_GB_WILLIAM_BROWNING
    N_ORG_US_CIA -->|"übernahm 1949 die amerikanische Aufsicht und Unterstützung"| N_ORG_DE_ORGANISATION_GEHLEN
    N_PER_DE_EMIL_AUGSBURG["Emil Augsburg"]
    N_PER_DE_EMIL_AUGSBURG -->|"war nach seiner SS-/RSHA-Tätigkeit im Gehlen-Netz beschäftigt"| N_ORG_DE_ORGANISATION_GEHLEN
    N_PER_DE_HEINZ_FELFE["Heinz Felfe"]
    N_PER_DE_HEINZ_FELFE -->|"arbeitete im Dienst und zugleich als sowjetischer Doppelagent"| N_ORG_DE_BND
    N_ORG_DE_SPD["Sozialdemokratische Partei Deutschlands (SPD)"]
    N_ORG_DE_ORGANISATION_GEHLEN -->|"spähte nach archivgestützter Forschung die politische Opposition aus"| N_ORG_DE_SPD
    N_ORG_US_CIG["Central Intelligence Group (CIG)"]
    N_ORG_US_CIG -->|"bezeichnete Operation Rusty 1947 als potenzielle Widerstandsgruppe und empfahl Auflösung"| N_ORG_DE_ORGANISATION_GEHLEN
    N_PRG_DE_ATLANTIK_BRUECKE_NEW_BRIDGE["Atlantik-Brücke New Bridge Program"]
    N_ORG_DE_ATLANTIK_BRUECKE -->|"betreibt New Bridge Program (New Bridge to Germany seit 2021)"| N_PRG_DE_ATLANTIK_BRUECKE_NEW_BRIDGE
    N_ORG_US_HALLE_FOUNDATION["The Halle Foundation"]
    N_ORG_US_HALLE_FOUNDATION -->|"bewilligte 47.525 USD für New Bridge 2022; keine ausgezahlte Summe nachgewiesen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_US_HALLE_FOUNDATION -->|"bewilligte 40.000 USD für New Bridge 2023; keine ausgezahlte Summe nachgewiesen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_JOACHIM_HERZ_STIFTUNG["Joachim Herz Stiftung"]
    N_ORG_DE_JOACHIM_HERZ_STIFTUNG -->|"fördert New Bridge to the U.S. und gemeinsam mit ERP New Bridge to Germany; Einzelbetrag offen"| N_PRG_DE_ATLANTIK_BRUECKE_NEW_BRIDGE
    N_PRG_US_CIA_KMMANLY["CIA/OPC-Projekt KMMANLY"]
    N_ORG_US_OPC -->|"führte laut CIA-Akten das übergeordnete verdeckte Einflussprojekt"| N_PRG_US_CIA_KMMANLY
    N_PRG_US_CIA_QKSNITCH["CIA-Teilprojekt QKSNITCH"]
    N_PRG_US_CIA_KMMANLY -->|"umfasste das GfW-Teilprojekt QKSNITCH"| N_PRG_US_CIA_QKSNITCH
    N_ORG_DE_GFW_1952["Gesellschaft für Wehrkunde (historischer Verein)"]
    N_PRG_US_CIA_QKSNITCH -->|"CIA-Abschlussbericht beziffert die projektbezogene Förderung auf insgesamt 240.858 DM; Einzelbuchungen und Anlage D offen"| N_ORG_DE_GFW_1952
    N_ORG_DE_DSZ_1952["Deutsche Soldaten-Zeitung (1952/53)"]
    N_PRG_US_CIA_KMMANLY -->|"CIA-Monatsberichte schildern verdeckte Unterstützung und redaktionelle Leitlinien"| N_ORG_DE_DSZ_1952
    N_ORG_DE_EWK_1952["Europäische Wehr-Korrespondenz (1952)"]
    N_PRG_US_CIA_KMMANLY -->|"CIA-Monatsbericht dokumentiert drei Auflagen zu je 5.000 und behauptet acht Zeitungsnachdrucke; Redaktionen unbekannt"| N_ORG_DE_EWK_1952
    N_ORG_DE_WWR_1952["Wehrwissenschaftliche Rundschau (1952)"]
    N_PRG_US_CIA_KMMANLY -->|"CIA-Monatsbericht beschreibt die finanzierte Publikation und Weiterverteilung"| N_ORG_DE_WWR_1952
    N_PER_DE_WILHELM_CLASSEN["Wilhelm Classen"]
    N_ORG_DE_STIFTERVERBAND_1952["Stifterverband für die Deutsche Wissenschaft (1952/53)"]
    N_PER_DE_WILHELM_CLASSEN -->|"laut CIA-QKSNITCH-Abschlussbericht Mittelsmann einer verdeckten Weiterleitung, nicht unabhängig bankgeprüft"| N_ORG_DE_STIFTERVERBAND_1952
    N_ORG_DE_STIFTERVERBAND_1952 -->|"CIA berichtet eine verdeckte Geldweiterleitung an das Münchner GfW-Konto; originale Kontoauszüge offen"| N_ORG_DE_GFW_1952
    N_ORG_DE_BUNDESPRESSEAMT_1953["Presse- und Informationsamt der Bundesregierung (1953)"]
    N_ORG_DE_WWR_1952 -->|"laut CIA-Monatsbericht 300 Exemplare des zwölfseitigen Nachdrucks an das Bundespresseamt verteilt"| N_ORG_DE_BUNDESPRESSEAMT_1953
    N_PER_DE_OTTO_LENZ["Otto Lenz"]
    N_PER_DE_OTTO_LENZ -->|"CIA-Bericht Februar 1953 nennt erneute Zusage von 10.000 DM monatlich; Auszahlung nicht nachgewiesen"| N_ORG_DE_DSZ_1952
    N_ORG_DE_BUNDESPRESSEAMT_1953 -->|"heutige GSP beschreibt einen Finanzierungsvertrag von Januar 1953; Originalvertrag und Auszahlungen noch ungeprüft"| N_ORG_DE_GFW_1952
    N_ORG_US_WASHINGTON_POST_COMPANY["The Washington Post Company (historischer Rechtsträger)"]
    N_ORG_US_AMERICAN_FRIENDS_BILDERBERG["American Friends of Bilderberg Inc."]
    N_ORG_US_WASHINGTON_POST_COMPANY -->|"Form 990-PF Schedule B: Unternehmenszahlung 25.000 USD im Steuerjahr 2008; PDF-Spenderzeile bildseitig noch nicht unabhängig bestätigt"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_ORG_US_WASHINGTON_POST_COMPANY -->|"Form 990-PF Schedule B: Unternehmenszahlung 25.000 USD im Steuerjahr 2009; PDF-Spenderzeile bildseitig noch nicht unabhängig bestätigt"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_PER_US_DONALD_E_GRAHAM["Donald E. Graham"]
    N_PER_US_DONALD_E_GRAHAM -->|"2010er Steuererklärung nennt Donald Graham als individuellen Geldgeber von 25.000 USD; Namensidentität mit SEC-CEO nicht eindeutig codiert"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_PER_US_DONALD_E_GRAHAM -->|"Chairman und CEO laut SEC Form 10-K 2010"| N_ORG_US_WASHINGTON_POST_COMPANY
    N_PER_US_PETER_THIEL["Peter Thiel"]
    N_PER_US_PETER_THIEL -->|"NCCS-Version des IRS Schedule B 2025: namentliche Zuwendung 1.000.000 USD"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_PER_US_ALEXANDER_KARP["Alexander Karp"]
    N_PER_US_ALEXANDER_KARP -->|"NCCS-Version des IRS Schedule B 2025: namentliche Zuwendung 500.000 USD"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_PER_GB_JOHN_MICKLETHWAIT["John Micklethwait"]
    N_PER_GB_JOHN_MICKLETHWAIT -->|"Director in der US-Form-990-PF-Organliste 2025; keine eigene Geldzuwendung daraus abgeleitet"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_PER_GB_JOHN_MICKLETHWAIT -->|"Auf offizieller Bilderberg-Steering-Committee-Seite am 29.10.2026 genannt; konkrete Berufungsdaten offen"| N_ORG_INT_BILDERBERG_MEETINGS
    N_ORG_US_BLOOMBERG_LP["Bloomberg L.P."]
    N_PER_GB_JOHN_MICKLETHWAIT -->|"Editor-in-Chief von Bloomberg, laut offizieller Bilderberg-Gremienliste am 29.10.2026"| N_ORG_US_BLOOMBERG_LP
    N_PER_US_PETER_THIEL -->|"Originalbild Form 990-PF 2010, Schedule B Part I Position 5: namentlich Peter Thiel, 50.000 USD; keine individuelle Ausweisnummer"| N_ORG_US_AMERICAN_FRIENDS_BILDERBERG
    N_ORG_GB_BILDERBERG_CHARITY_272706["The Bilderberg Association (Charity 272706, historisch)"]
    N_ORG_GB_BILDERBERG_CHARITY_272706 -->|"Bilanz 2013er UK-Konferenz: £459.839 Aufwendungen, davon £320.000 Security und £139.839 Organisation; konkrete Empfänger offen"| N_ORG_INT_BILDERBERG_MEETINGS
    N_ORG_GB_HERTFORDSHIRE_POLICE["Hertfordshire Constabulary"]
    N_ORG_GB_HOME_OFFICE["UK Home Office"]
    N_ORG_GB_HERTFORDSHIRE_POLICE -->|"FOI 29091: £527.762 Sonderförderung für Op Discuss/Bilderberg 2013/14 beantragt; Decision Pending, keine Auszahlung nachgewiesen"| N_ORG_GB_HOME_OFFICE
    N_PER_GB_JOHN_SAWERS["Sir John Sawers"]
    N_ORG_GB_NEWBRIDGE_ADVISORY_LTD_11853148["Newbridge Advisory Limited (11853148)"]
    N_PER_GB_JOHN_SAWERS -->|"Director seit Unternehmensgründung am 28.02.2019, Companies House"| N_ORG_GB_NEWBRIDGE_ADVISORY_LTD_11853148
    N_ORG_GB_BILDERBERG_UK_LTD_12988319["The Bilderberg Association UK Limited (12988319)"]
    N_PER_GB_JOHN_SAWERS -->|"Director seit 02.11.2020; 2023 ebenfalls durch BP-AGM-Governancebericht bestätigt"| N_ORG_GB_BILDERBERG_UK_LTD_12988319
    N_PER_GB_SUSAN_JEAN_MINTON_BEDDOES["Susan Jean Minton Beddoes (Zanny Minton Beddoes)"]
    N_PER_GB_SUSAN_JEAN_MINTON_BEDDOES -->|"Susan Jean Minton Beddoes: Director seit 02.11.2020 laut Companies House"| N_ORG_GB_BILDERBERG_UK_LTD_12988319
    N_ORG_GB_THE_ECONOMIST["The Economist"]
    N_PER_GB_SUSAN_JEAN_MINTON_BEDDOES -->|"Zanny Minton Beddoes als Economist-Chefredakteurin; Zuordnung zur Register-Namensform Susan Jean stark gestützt"| N_ORG_GB_THE_ECONOMIST
    N_PER_GB_SUSAN_JEAN_MINTON_BEDDOES -->|"Als Zanny Minton Beddoes in aktueller offizieller Steering-Liste; Startdatum und exakte amtliche Identitätskennung offen"| N_ORG_INT_BILDERBERG_MEETINGS
    N_ORG_GB_NEWBRIDGE_2022_SPONSOR_UNKNOWN["Newbridge Advisory (Sponsorbezeichnung im Lammy-Register 2022)"]
    N_PER_GB_DAVID_LAMMY["David Lammy"]
    N_ORG_GB_NEWBRIDGE_2022_SPONSOR_UNKNOWN -->|"Parlamentsakte: 'Newbridge Advisory' erstattet am 08.06.2022 £5.669,57 für Bilderberg-Flug und Unterkunft; konkrete Ltd-Firmennummer im Sponsoreneintrag fehlt"| N_PER_GB_DAVID_LAMMY
    N_ORG_GB_BILDERBERG_2022_SPONSOR_UNKNOWN["Bilderberg Association (Sponsorbezeichnung im Lammy-Register 2022)"]
    N_ORG_GB_BILDERBERG_2022_SPONSOR_UNKNOWN -->|"2022er 'Bilderberg Association': geschätzte £536,58 für Transfers und Mahlzeiten, kein Geldtransfer; juristischer Sponsor unbestimmt"| N_PER_GB_DAVID_LAMMY
    N_PER_GB_DAVID_LAMMY -->|"Bilderberg-Konferenz Washington, 02.–05.06.2022, im House-of-Commons-Register erklärt"| N_ORG_INT_BILDERBERG_MEETINGS
    N_ORG_GB_COMMONS_STANDARDS_COMMISSIONER["Parliamentary Commissioner for Standards (House of Commons)"]
    N_ORG_GB_COMMONS_STANDARDS_COMMISSIONER -->|"2022: verspätete Bilderberg-Reiseangabe verletzt Paragraph 14 Commons Code; unbeabsichtigt, geringes Gewicht, per Rectification erledigt"| N_PER_GB_DAVID_LAMMY
    N_PER_GB_JOHN_SAWERS -->|"Companies House PSC: seit 02.11.2020 mehr als 25 bis höchstens 50 Prozent Stimmrechte sowie Recht auf Bestellung und Abberufung von Directors"| N_ORG_GB_BILDERBERG_UK_LTD_12988319
    N_PER_GB_SUSAN_JEAN_MINTON_BEDDOES -->|"Companies House PSC: seit 02.11.2020 mehr als 25 bis höchstens 50 Prozent Stimmrechte sowie Recht auf Bestellung und Abberufung von Directors"| N_ORG_GB_BILDERBERG_UK_LTD_12988319
    N_ORG_IT_BANCO_AMBROSIANO_SPA_1979["Banco Ambrosiano S.p.A. (Mailand; historische Gesellschaft)"]
    N_ORG_INT_INTERALPHA_BANKENKOOPERATION["Inter-Alpha Group (Gruppo di Banche Inter-Alpha)"]
    N_ORG_IT_BANCO_AMBROSIANO_SPA_1979 -->|"Februar/März 1979 als Mitglied des Inter-Alpha-Bankenverbunds im eigenen historischen Werbeinserat benannt; unabhängiger Rechtsstatus der Banken"| N_ORG_INT_INTERALPHA_BANKENKOOPERATION
    N_ORG_NL_NEDERLANDSCHE_MIDDENSTANDSBANK["Nederlandsche Middenstandsbank N.V. (NMB)"]
    N_ORG_NL_NEDERLANDSCHE_MIDDENSTANDSBANK -->|"NMB Amsterdam im Banco-Ambrosiano-Inserat 1979 ausdrücklich als selbständiges Inter-Alpha-Mitglied aufgeführt"| N_ORG_INT_INTERALPHA_BANKENKOOPERATION
    N_ORG_UY_BANCO_FINANCIERO_SUDAMERICANO["Banco Financiero Sudamericano (BAFISUD)"]
    N_ORG_NL_NEDERLANDSCHE_MIDDENSTANDSBANK -->|"NMB-Mehrheitserwerb im März 1983; Carrió zitiert 78,79 Prozent Aktien und N$ 1 nominellen Anteilspreis, Bank 1984 beansprucht inzwischen 100 Prozent"| N_ORG_UY_BANCO_FINANCIERO_SUDAMERICANO
    N_ORG_UY_BANCO_CENTRAL_URUGUAY["Banco Central del Uruguay (BCU)"]
    N_ORG_UY_BANCO_CENTRAL_URUGUAY -->|"BCU-Kauf von Problemforderungen: Carrió nennt Vertrag 09.01.1984 über rund 93,7 Mio. USD nach seiner Umrechnung; Vaz/Banda nennen rund 106 Mio. USD Nominalforderungen 1982/83; Beträge nicht als identisch bewiesen"| N_ORG_UY_BANCO_FINANCIERO_SUDAMERICANO
    N_ORG_FR_CREDIT_COMMERCIAL_DE_FRANCE_SA["Crédit Commercial de France S.A. (Paris)"]
    N_ORG_FR_CREDIT_COMMERCIAL_DE_FRANCE_SA -->|"Crédit Commercial de France S.A. Paris als selbständige Mitgliedsbank im Banco-Ambrosiano-Inserat 1979 benannt; nicht die spätere Schweizer Aktiehalterin"| N_ORG_INT_INTERALPHA_BANKENKOOPERATION
    N_ORG_CH_CREDIT_COMMERCIAL_DE_FRANCE_SUISSE_SA["Crédit Commercial de France (Suisse) S.A. (Genf)"]
    N_ORG_FR_CREDIT_COMMERCIAL_DE_FRANCE_SA -->|"Banca d'Italia bezeichnet den Genfer Rechtsträger Crédit Commercial de France (Suisse) S.A. ausdrücklich als schweizerische Tochter der französischen Bank; direkte Stimmrechtsquote nicht veröffentlicht"| N_ORG_CH_CREDIT_COMMERCIAL_DE_FRANCE_SUISSE_SA
    N_ORG_LU_BANCO_AMBROSIANO_HOLDING_SA["Banco Ambrosiano Holding S.A. (Luxemburg)"]
    N_ORG_IT_BANCO_AMBROSIANO_SPA_1979 -->|"Banco-Ambrosiano-Eigeninserat 1979 listet die Luxemburger Holding in gesonderter Rubrik Controllate; nicht als Inter-Alpha-Mitglied"| N_ORG_LU_BANCO_AMBROSIANO_HOLDING_SA
    N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS["Banco Ambrosiano Overseas (Nassau; vormals Cisalpine Overseas Bank)"]
    N_ORG_LU_BANCO_AMBROSIANO_HOLDING_SA -->|"Banca-d'Italia-Inspektionsmaterial bezeichnet den Banco Ambrosiano Overseas Nassau (früher Cisalpine Overseas) als von der Luxemburger Ambrosiano-Holding kontrolliert; Eigentumsregister nicht separat eingesehen"| N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS
    N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS -->|"Banca d'Italia: Cisalpine/Banco Ambrosiano Overseas Nassau hielt etwa 1978 und noch im geschilderten Interbankenkontext Juni 1980 5,5 Prozent am Kapital von BAFISUD Montevideo; Minderheit ist keine belegte Mehrheitskontrolle"| N_ORG_UY_BANCO_FINANCIERO_SUDAMERICANO
    N_ORG_PA_BAFISUD_CORPORATION_SA["BAFISUD Corporation S.A. (Panama)"]
    N_ORG_UY_BANCO_FINANCIERO_SUDAMERICANO -->|"Die Bankaufsicht nennt BAFISUD Corporation Panama eine mit BAFISUD Montevideo verbundene Finanzgesellschaft; Eigentumsquote, Treuhandgeber und effektiver Finanzierer blieben ungeklärt"| N_ORG_PA_BAFISUD_CORPORATION_SA
    N_ORG_IT_LA_CENTRALE_FINANZIARIA_SPA["La Centrale Finanziaria S.p.A. (Mailand)"]
    N_ORG_IT_BANCO_AMBROSIANO_SPA_1979 -->|"Banca d'Italia nennt La Centrale als Finanzgesellschaft des Ambrosiano-Umfelds; kein hier separat ermittelter direkter 100-Prozent-Beteiligungsvertrag"| N_ORG_IT_LA_CENTRALE_FINANZIARIA_SPA
    N_ORG_IT_LA_CENTRALE_FINANZIARIA_SPA -->|"September/Oktober 1978: La Centrale verkauft 4,5 Mio. Credito-Varesino-Aktien (12,5 Prozent des Varesino-Kapitals) für laut Banca d'Italia 26,6 Mrd. Lire; der tatsächliche Geldgeber hinter der Panama-Gesellschaft ist unbekannt"| N_ORG_PA_BAFISUD_CORPORATION_SA
    N_ORG_IT_CREDITO_VARESINO_SPA["Credito Varesino S.p.A. (Varese)"]
    N_ORG_PA_BAFISUD_CORPORATION_SA -->|"4,5 Mio. Aktien entsprechend 12,5 Prozent des Credito-Varesino-Kapitals auf BAFISUD Corporation Panama 1978 indossiert; Banca d'Italia hält treuhänderische Namenshaltung für möglich"| N_ORG_IT_CREDITO_VARESINO_SPA
    N_ORG_PA_BAFISUD_CORPORATION_SA -->|"31.03.1981: 44 Zertifikate Nr. 00204-00247 zu je 100.000 Credito-Varesino-Aktien (4,4 Mio.) auf Schweizer CCF umgeschrieben; deren Brief vom 01.04. behauptet fehlendes Finanzgeschäft, nicht unabhängig geprüft"| N_ORG_CH_CREDIT_COMMERCIAL_DE_FRANCE_SUISSE_SA
    N_ORG_CH_CREDIT_COMMERCIAL_DE_FRANCE_SUISSE_SA -->|"Schweizer CCF ab 31.03.1981 eingetragene Halterin von 4,4 Mio. Credito-Varesino-Aktien; im Laufe 1981/82 teilweise veräußert; wirtschaftlicher Auftraggeber nicht identifiziert"| N_ORG_IT_CREDITO_VARESINO_SPA
    N_ORG_IT_CREDITO_VARESINO_SPA -->|"Zwei unterschiedliche Credito-Varesino-Interbankeinlagen bei BAFISUD: 200.000 USD ab 20.06.1980 (3 Monate) und 300.000 USD ab 25.09.1980 bis 29.12.1980; keine zeitgleiche 500.000-USD-Position ableitbar"| N_ORG_UY_BANCO_FINANCIERO_SUDAMERICANO
    N_ORG_INT_BCCI["BCCI-Gruppe (Bank of Credit and Commerce International)"]
    N_ORG_AN_CCAH["Credit and Commerce American Holdings N.V. (CCAH)"]
    N_ORG_INT_BCCI -->|"verdeckte wirtschaftliche Beteiligung über Treuhänder; 1998 gerichtlich auf 61,156 % der CCAH-Anteile rekonstruiert, 1991 Fed-Mindestbefund 25 %"| N_ORG_AN_CCAH
    N_ORG_US_FIRST_AMERICAN_BANKSHARES["First American Bankshares"]
    N_ORG_AN_CCAH -->|"CCAH war die Mutterholding von First American Bankshares; Beteiligung nicht als unmittelbares BCCI-Eigentum der Bank ausweisen"| N_ORG_US_FIRST_AMERICAN_BANKSHARES
    N_ORG_US_TREASURY["U.S. Department of the Treasury"]
    N_ORG_US_CIA -->|"Senatsrekonstruktion: CIA-Erkenntnisse zum BCCI-/First-American-Eigentum Anfang 1985 an Treasury-Nachrichtendienstkontakte; Originalmemorandum fehlt"| N_ORG_US_TREASURY
    N_ORG_US_OCC["Office of the Comptroller of the Currency (OCC)"]
    N_ORG_US_CIA -->|"US-Senat rekonstruierte OCC als Empfänger früher CIA-Erkenntnisse zu BCCIs verdecktem US-Bankeigentum; tatsächliche Weiterverarbeitung ungeklärt"| N_ORG_US_OCC
    N_ORG_US_FEDERAL_RESERVE["Federal Reserve System (US-Bankaufsicht)"]
    N_ORG_US_FEDERAL_RESERVE -->|"29.07.1991 formelle Aufsichtsverfahren wegen verheimlichter CCAH-Beteiligungen angekündigt; angestrebte 200 Mio. USD Geldbuße nicht mit Zahlung gleichsetzen"| N_ORG_INT_BCCI
    N_ORG_US_DOJ["U.S. Department of Justice"]
    N_ORG_US_DOJ -->|"US-Justiz gab Dezember 1991 BCCI-Schuldbekenntnisvereinbarung bekannt; Gericht nahm am 24.01.1992 Schuldbekenntnisse von vier Gesellschaften an"| N_ORG_INT_BCCI
    N_PER_DE_HERMANN_SCHMITZ["Hermann Schmitz (1881–1960)"]
    N_ORG_DE_IG_FARBEN["I.G. Farbenindustrie AG (historischer Konzern)"]
    N_PER_DE_HERMANN_SCHMITZ -->|"1925 Finanz- und Auslandschef, 1935 bis 1945 Vorstandsvorsitzender; nicht jede Einzelentscheidung persönlich zurechenbar"| N_ORG_DE_IG_FARBEN
    N_PER_DE_AUGUST_VON_KNIERIEM["August von Knieriem (1887–1978)"]
    N_PER_DE_AUGUST_VON_KNIERIEM -->|"laut Nürnberger Protokoll Unterzeichner der beiden I.G.-Verträge NI-10550 und NI-10430 vom 09.11.1929"| N_ORG_DE_IG_FARBEN
    N_ORG_US_STANDARD_OIL_NEW_JERSEY["Standard Oil Company of New Jersey (historisch)"]
    N_ORG_DE_IG_FARBEN -->|"09.11.1929 Four-Party Agreement und Division of Fields Agreement über Patente, Technologien und Geschäftsfelder; durch Nürnberger Prozessakten dokumentiert"| N_ORG_US_STANDARD_OIL_NEW_JERSEY
    N_PER_DE_HERMANN_SCHMITZ -->|"unterzeichnete laut Prozessprotokoll 1929 als I.G.-Vertreter die Standard-Oil-Vertragsdokumente; kein privates Finanzierungsverhältnis daraus abgeleitet"| N_ORG_US_STANDARD_OIL_NEW_JERSEY
    N_PER_DE_AUGUST_VON_KNIERIEM -->|"war laut Prozessprotokoll 1929 im Namen von IG Farben Mitunterzeichner des Standard-IG-Vertrags und der Geschäftsfeld-Abgrenzung"| N_ORG_US_STANDARD_OIL_NEW_JERSEY
    N_ORG_CH_IG_CHEMIE_INTERHANDEL["IG Chemie Basel / Interhandel (historische Schweizer Holding)"]
    N_ORG_DE_IG_FARBEN -->|"1928/29 Gründung und durch Optionen, Dividenden- und Vorzugsstimmrechte wirksame IG-Bindung; laut UEK im Mai 1940 bedingungslos aufgehoben"| N_ORG_CH_IG_CHEMIE_INTERHANDEL
    N_PER_DE_HERMANN_SCHMITZ -->|"als IG-Finanzchef Initiator der Gründung der Basler Finanzholding 1928/29, laut unabhängiger Schweizer Expertenkommission"| N_ORG_CH_IG_CHEMIE_INTERHANDEL
    N_ORG_US_GAF_HISTORIC["General Aniline & Film Corporation (GAF, historisch)"]
    N_ORG_CH_IG_CHEMIE_INTERHANDEL -->|"hielt US-Chemiefabriken, ab 1939 zu General Aniline & Film zusammengefasst; 1942 in den USA beschlagnahmt"| N_ORG_US_GAF_HISTORIC
    N_ORG_CH_SBG_HISTORIC["Schweizerische Bankgesellschaft (SBG, historisch)"]
    N_ORG_CH_SBG_HISTORIC -->|"seit 1961 alleinige Kontrolle laut UEK, 1967 Fusion mit Interhandel; keine Fortsetzung deutschen IG-Eigentums daraus abgeleitet"| N_ORG_CH_IG_CHEMIE_INTERHANDEL
    N_ORG_INT_BIS["Bank für Internationalen Zahlungsausgleich (BIZ/BIS)"]
    N_PER_DE_HERMANN_SCHMITZ -->|"US National Archives führen Schmitz im historischen BIZ-Verwaltungsrat; genaue Amtsjahre und Beschlüsse nicht daraus ermittelt"| N_ORG_INT_BIS
    N_ORG_DE_DRESDNER_BANK_1933["Dresdner Bank (historische Bank, Frankfurt 1933)"]
    N_ORG_DE_IG_FARBEN -->|"Schreiben IG-Farben-Bankabteilung vom 27.02.1933 wies die Dresdner Bank zur Zahlung von 400.000 Reichsmark an"| N_ORG_DE_DRESDNER_BANK_1933
    N_ORG_DE_DELBRUECK_SCHICKLER_1933["Delbrück, Schickler & Co. (historisches Bankhaus)"]
    N_ORG_DE_DRESDNER_BANK_1933 -->|"laut Nürnberger Exhibit NI-391 400.000 RM für das Nationale-Treuhand-Konto bei Delbrück, Schickler & Co. als Zahlung angewiesen"| N_ORG_DE_DELBRUECK_SCHICKLER_1933
    N_PRG_DE_NATIONALE_TREUHAND_1933["Konto Nationale Treuhand (Wahlkampffonds 1933)"]
    N_ORG_DE_DELBRUECK_SCHICKLER_1933 -->|"Bankhaus als Empfänger für das Konto Nationale Treuhand bezeichnet; Konto der Wahlkampffinanzierung im Februar 1933"| N_PRG_DE_NATIONALE_TREUHAND_1933
    N_ORG_DE_ANORGANA["Anorgana GmbH (historische IG-Farben-Gesellschaft)"]
    N_PER_DE_AUGUST_VON_KNIERIEM -->|"laut eigener Aussage ab Frühjahr 1940 Aufsichtsratsmitglied, 1943er Protokoll NI-7377 behandelt; konkrete Produktionsweisungen nicht belegt"| N_ORG_DE_ANORGANA
    N_ORG_US_DOD["U.S. Department of Defense"]
    N_PRG_UA_BIOSAFETY_COOP["USA–Ukraine: biologische Gefahrenabwehr und Laborsicherheit (historisches Kooperationsprogramm)"]
    N_ORG_US_DOD -->|"US-Verteidigungsministerium erklärte am 09.06.2022, es habe über zwei Jahrzehnte 46 ukrainische Labor-, Gesundheits- und Diagnostikstellen bei Biosicherheit/Krankheitsüberwachung unterstützt; ukrainischer Betrieb laut US-Angabe, kein SARS-CoV-2-Transferbeleg"| N_PRG_UA_BIOSAFETY_COOP
    N_ORG_GB_COUNCIL_OF_STATE_1649["Englischer Council of State (1649)"]
    N_PER_GB_ANTONIO_FERNANDES_CARVAJAL["António Fernandes Carvajal (gest. 1659)"]
    N_ORG_GB_COUNCIL_OF_STATE_1649 -->|"1649 erhielt Carvajal laut archivnaher Edition als einer von fünf Londoner Kaufleuten einen staatlichen Getreideliefervertrag für die Armee; keine belegte Finanzierung der Hinrichtung Karls I."| N_PER_GB_ANTONIO_FERNANDES_CARVAJAL
    N_PER_GB_OLIVER_CROMWELL["Oliver Cromwell (1599–1658)"]
    N_ORG_GB_PROTECTORATE_1653["Englisches Protektorat unter Oliver Cromwell (1653–1658)"]
    N_PER_GB_OLIVER_CROMWELL -->|"Am 16.12.1653 als Lord Protector eingesetzt; keine aus dem Amt allein ableitbare Weisung über einzelne Handelsverträge"| N_ORG_GB_PROTECTORATE_1653
    N_ORG_GB_PROTECTORATE_1653 -->|"Im Juli 1655 erhielten Carvajal und seine zwei Söhne laut Wolf-Edition im Protektorat einen Denization-Status; keine bewiesene Gegenleistung für die Hinrichtung von 1649"| N_PER_GB_ANTONIO_FERNANDES_CARVAJAL
    N_PER_DE_FRIEDRICH_MERZ["Friedrich Merz"]
    N_ORG_US_ATLANTIK_BRUECKE_FRIENDS_EIN202174611["Friends of the Atlantik-Bruecke Ev Inc (New York, EIN 20-2174611)"]
    N_PER_DE_FRIEDRICH_MERZ -->|"IRS-abgeleitete 2021er US-990-EZ-Auswertung nennt Friedrich Merz als Director des rechtlich eigenständigen US-Friends-Vereins; Originalzeile hier nicht bildgeprüft, laut 2022er Erfassung bis Mai 2022; keine heutige Funktion belegt"| N_ORG_US_ATLANTIK_BRUECKE_FRIENDS_EIN202174611
    N_PER_DE_WALTHER_FUNK["Walther Funk (1890–1960)"]
    N_PER_DE_WALTHER_FUNK -->|"BIZ-Jahresbericht 1939: Reichsbankpräsident Walther Funk war ex-officio Verwaltungsrat; kein Beleg einer individuellen BIZ-Goldweisung daraus"| N_ORG_INT_BIS
    N_PER_DE_KURT_VON_SCHROEDER["Kurt Freiherr von Schröder (1889–1966)"]
    N_PER_DE_KURT_VON_SCHROEDER -->|"1939 ausdrücklich im BIZ-Verwaltungsrat gelistet; seine separate SS-Finanzvermittlung 1943 ist damit nicht als BIZ-Beschluss bewiesen"| N_ORG_INT_BIS
    N_PER_DE_EMIL_PUHL["Emil Puhl (1889–1962)"]
    N_PER_DE_EMIL_PUHL -->|"BIZ-Jahresbericht 1939 nennt Emil Puhl nur unter Stellvertreter, nicht unter ordentlichen Verwaltungsräten"| N_ORG_INT_BIS
    N_PER_DE_WALTHER_FUNK -->|"Funk berief laut 9. BIZ-Jahresbericht nach Übernahme des Reichsbankpräsidiums 1939 den IG-Farben-Chef Schmitz anstelle von Paul Reusch in den BIZ-Verwaltungsrat; kein Beleg eines gemeinsamen SS-Zahlungsentscheids"| N_PER_DE_HERMANN_SCHMITZ
    N_ORG_DE_REICHSBANK_HISTORIC["Deutsche Reichsbank (historisch, 1933–1945)"]
    N_PER_DE_WALTHER_FUNK -->|"Funk wurde im Januar 1939 Reichsbankpräsident, im selben Bericht als BIZ-Mitglied von Amts wegen bezeichnet"| N_ORG_DE_REICHSBANK_HISTORIC
    N_PER_DE_EMIL_PUHL -->|"Puhl 1939 kommissarischer Reichsbank-Stellvertreter, am 08.08.1940 formell Vizepräsident; von seinem BIZ-Stellvertretermandat getrennt"| N_ORG_DE_REICHSBANK_HISTORIC
    N_ORG_GB_BANK_OF_ENGLAND_HISTORIC["Bank of England (historische Kontenfunktion 1939)"]
    N_ORG_GB_BANK_OF_ENGLAND_HISTORIC -->|"Bei der Bank of England geführtes BIZ-Goldkonto: tschechoslowakisches Zentralbankgold wurde im März 1939 nach unter Zwang erteilter Anweisung auf ein Reichsbankkonto umgebucht; keine freiwillige Schenkung"| N_ORG_INT_BIS
    N_ORG_INT_BIS -->|"BIZ veranlasste März 1939 nach deutscher Besetzung Prags die Umbuchung tschechoslowakischer Goldreserven von ihrem Bank-of-England-Konto zur Reichsbank; BIS erkennt die später festgestellte Nötigung an"| N_ORG_DE_REICHSBANK_HISTORIC
    N_ORG_DE_REICHSBANK_HISTORIC -->|"BIS-Archivrekonstruktion: von der Reichsbank stammende Goldzahlungen 1939–45 enthielten ca. 3,7 Tonnen später als geraubtes belgisches/niederländisches Notenbankgold ermittelte Reserven; BIS restituierte 1948, nicht mit Melmer-Opfergold gleichgesetzt"| N_ORG_INT_BIS
    N_ORG_CH_SNB_HISTORIC["Schweizerische Nationalbank (SNB, historische Goldgeschäfte)"]
    N_ORG_DE_REICHSBANK_HISTORIC -->|"UEK: Reichsbank lieferte während des Kriegs Gold im Wert von 1,6–1,7 Mrd. CHF an SNB; 1,2 Mrd. auf SNB-Eigenrechnung, übriges teils Depotgold; nicht jede Lieferung war Raubgold"| N_ORG_CH_SNB_HISTORIC
    N_PRG_DE_HIMMLER_SONDERKONTO_S_1943["Sonderkonto S des Himmler-Freundeskreises (1943)"]
    N_PER_DE_KURT_VON_SCHROEDER -->|"Schröders Schreiben an Himmler EC-453 vom 21.09.1943 übermittelte eine Sonderkonto-S-Beitragsliste von insgesamt 1.100.000 RM; getrennte Einzelkontobelege liegen hier nicht vor"| N_PRG_DE_HIMMLER_SONDERKONTO_S_1943
    N_ORG_DE_IG_FARBEN -->|"EC-453 weist für 1943 über Bütefisch und Hermann Schmitz 100.000 RM der IG Farben als beim Sonderkonto S eingegangenen Beitrag aus; kein unabhängig eingesehener Einzelbankbeleg und keine belegte konkrete Verwendung"| N_PRG_DE_HIMMLER_SONDERKONTO_S_1943
    N_PER_DE_HEINRICH_HIMMLER["Heinrich Himmler (1900–1945)"]
    N_PRG_DE_HIMMLER_SONDERKONTO_S_1943 -->|"Schröders Brief EC-453: 1943 auf Sonderkonto S gesammelte 1,1 Mio. RM für besondere Aufgaben Himmlers bereitgestellt; konkreter Endverwendungsnachweis offen"| N_PER_DE_HEINRICH_HIMMLER
    N_ORG_DE_DEST_SS_HISTORIC["Deutsche Erd- und Steinwerke GmbH (DEST, SS-Betrieb)"]
    N_PER_DE_WALTHER_FUNK -->|"Ministerien-Urteil: Funk bewilligte 1939 einen 8-Mio.-RM-DEST-Finanzierungsrahmen und unterzeichnete am 19.05.1941 weiteren 8-Mio.-RM-Kreditauftrag; Kreditrahmen nicht mit vollständiger Auszahlung gleichgesetzt"| N_ORG_DE_DEST_SS_HISTORIC
    N_ORG_DE_DEGO_HISTORIC["Deutsche Golddiskontbank (DEGO, historisch)"]
    N_ORG_DE_DEGO_HISTORIC -->|"1939 laut Ministerien-Urteil: 8 Mio. RM aus Mitteln des Reichswirtschaftsministeriums bei der DEGO als Sicherheit für DEST-Finanzierung deponiert, nicht Nachweis des ganzen ausgezahlten Darlehens"| N_ORG_DE_DEST_SS_HISTORIC
    N_PER_DE_OSWALD_POHL["Oswald Pohl (1892–1951)"]
    N_PER_DE_EMIL_PUHL -->|"Puhl berichtet 1946 über heimlich organisierte Reichsbank-Annahme von SS-Gold, KZ-Opfer-Schmuck, Zahngold und Devisen nach Abstimmung mit Oswald Pohl; Tribunal verurteilte Puhl wegen wissender Verwertung unter Count 5, nicht wegen Tötungen"| N_PER_DE_OSWALD_POHL
    N_ORG_IT_ENI_1978["Ente Nazionale Idrocarburi (ENI, historisch 1978–1982)"]
    N_ORG_BS_TRADINVEST_ENI["Tradinvest Bank and Trust Company of Nassau Ltd. (ENI)"]
    N_ORG_IT_ENI_1978 -->|"ENI-Originalauskunft 1982 benennt Tradinvest Nassau als eigene Finanztochter; Darlehensentscheidungen formal durch deren Verwaltungsrat, nicht unmittelbar der ENI-Giunta zugeschrieben"| N_ORG_BS_TRADINVEST_ENI
    N_ORG_NI_AMBROSIANO_MANAGUA["Ambrosiano Group Banco Comercial S.A., Managua"]
    N_ORG_BS_TRADINVEST_ENI -->|"ENI-Unterlagen: 31.05.1979 12,5 Mio. USD-Darlehen an Ambrosiano Managua, am 30.10.1979 in 6,5 Mio. Andino und 6 Mio. Overseas umverteilt; dies sind keine drei addierbaren Darlehenszahlungen"| N_ORG_NI_AMBROSIANO_MANAGUA
    N_ORG_PE_AMBROSIANO_ANDINO["Banco Ambrosiano Andino S.A., Lima"]
    N_ORG_BS_TRADINVEST_ENI -->|"1979er Tradinvest-Darlehensposition aus 12,5 Mio. USD an Managua laut ENI-Abrechnung auf 6,5 Mio. USD für Banco Ambrosiano Andino Lima aufgeteilt, keine zusätzliche zweite 6,5-Mio.-Auszahlung"| N_ORG_PE_AMBROSIANO_ANDINO
    N_ORG_BS_TRADINVEST_ENI -->|"1979er Tradinvest-Darlehensposition aus 12,5 Mio. USD an Managua laut ENI-Abrechnung zu 6 Mio. USD auf Ambrosiano Overseas Nassau umgeordnet; Umverteilung ist kein dritter Zahlungseingang"| N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS
    N_ORG_BS_TRADINVEST_ENI -->|"Teodori-P2-Minderheitsbericht 1984 führt getrennt von der 6-Mio.-Umverteilung einen Tradinvest-Overseas-Vertrag über 25 Mio. USD vom 31.05.1979 und eine Valuta 11.06.1979 auf; vollständiges Bankjournal hier nicht geprüft"| N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS
    N_ORG_BS_TRADINVEST_ENI -->|"ENI-Dokumente und Teodori-Tabelle: eigenständiger Andino-Vertrag 01.12.1980 über 50 Mio. USD Nominalanleihe, angegebene Auszahlung 08.12.1980; ENI-Risikoposition 48 Mio., kein Beleg für spätere PSI-Zahlung"| N_ORG_PE_AMBROSIANO_ANDINO
    N_PER_INT_PIERRE_W_SIEGENTHALER["Pierre W. Siegenthaler"]
    N_PER_INT_PIERRE_W_SIEGENTHALER -->|"ENI-Originalunterlagen nennen Pierre W. Siegenthaler in Tradinvest-Verwaltungsratslisten 1979 und 1980; Teilnahme an konkreter Abstimmung oder Sondervorteil nicht einzeln belegt"| N_ORG_BS_TRADINVEST_ENI
    N_PER_INT_PIERRE_W_SIEGENTHALER -->|"Banca-d'Italia-Inspektionsanhang 1978 führt Pierre W. Siegenthaler als Präsidenten der Cisalpine Overseas Bank Nassau; Amtszeit nach 1978 bedarf gesonderter Prüfung"| N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS
    N_PER_INT_PIERRE_W_SIEGENTHALER -->|"Banca-d'Italia-Inspektionsanhang 1978 nennt Siegenthaler als Secretary von Ambrosiano Group Banco Comercial Managua; keine persönliche Zahlungsausführung daraus bewiesen"| N_ORG_NI_AMBROSIANO_MANAGUA
    N_ORG_IT_MAE_1982["Italienisches Außenministerium (Ministero degli Affari Esteri, 1982)"]
    N_PER_INT_PIERRE_W_SIEGENTHALER -->|"Italienisches Ministerialdekret 30.06.1982 benennt Siegenthaler bereits als ehrenamtlichen Konsularagenten in Nassau mit begrenzten Befugnissen; keine nachgewiesene Nutzung des Amtes für Ambrosiano-Kredite"| N_ORG_IT_MAE_1982
    N_ORG_BS_BANCO_AMBROSIANO_OVERSEAS -->|"P2-Minderheitsbericht 1984 beschreibt für 1980 einen mit 'Sudam' verbundenen 21-Mio.-USD-Kredit Overseas Nassau zu BAFISUD Corporation; Zeuge Botta erinnerte Nassau/Managua. Vertrag, Valuta, Identität letzter Begünstigter und PSI-Endzahlung nicht durch Bankkonto belegt"| N_ORG_PA_BAFISUD_CORPORATION_SA
    N_ORG_DE_LANDESREGIERUNG_BRANDENBURG["Landesregierung Brandenburg (Aktenzugangsverfahren 2003/04)"]
    N_PER_DE_KERSTIN_KAISER_NICHT["Kerstin Kaiser-Nicht"]
    N_ORG_DE_LANDESREGIERUNG_BRANDENBURG -->|"Innenministerium verweigerte am 06.11.2003 PKK-Mitglied Kerstin Kaiser-Nicht Akteneinsicht im Fall Toni S.; VerfGBbg 6/04 stellte am 09.12.2004 wegen fehlender einzelfallbezogener Abwägung eine Verletzung von Art. 56 Abs. 3 LV fest; keine automatische Herausgabe angeordnet"| N_PER_DE_KERSTIN_KAISER_NICHT
    N_PER_DE_HEINZ_VIETZE["Heinz Vietze"]
    N_ORG_DE_LANDESREGIERUNG_BRANDENBURG -->|"Innenministerium verweigerte am 06.11.2003 auch Heinz Vietze Akteneinsicht; VerfGBbg 6/04 bestätigte 2004 die Verweigerung für den nicht zur PKK gehörenden Abgeordneten als verfassungsgemäß"| N_PER_DE_HEINZ_VIETZE
    N_ORG_DE_VERFG_BRANDENBURG["Verfassungsgericht des Landes Brandenburg"]
    N_ORG_DE_VERFG_BRANDENBURG -->|"Urteil VfGBbg 6/04 vom 09.12.2004: unzureichend begründete Verweigerung gegenüber Kaiser-Nicht verfassungswidrig; Ablehnung gegenüber Vietze hatte Bestand; keine Beurteilung der NaBe-Warnkette oder eines 2003er Strafurteils"| N_ORG_DE_LANDESREGIERUNG_BRANDENBURG
    N_PER_DE_CHRISTIAN_K_2001["Christian K. (anonymisierte Quelle Brandenburg, 2001)"]
    N_ORG_DE_LFV_BRANDENBURG -->|"Brandenburger grünes Sondervotum 2019 beschreibt Christian K. 2001 als LfV-Quelle; vor der Durchsuchung 17.02. sollte sein Quellenführer warnen; ob die Nennung des konkreten Termins behördlich angeordnet wurde, blieb streitig"| N_PER_DE_CHRISTIAN_K_2001
    N_PER_DE_SVEN_SCH_2001["Sven Sch. (anonymisierter Adressat einer Warnung, 2001)"]
    N_PER_DE_CHRISTIAN_K_2001 -->|"Laut grünem Sondervotum/rekonstruierter TKÜ warnte Christian K. Sven Sch. am 06.02.2001 15:54 vor einer für 17.02. geplanten Durchsuchung; diese wurde auf 07.02. vorgezogen. Originalmitschnitt und tatsächlicher Beweismittelverlust hier nicht nachgewiesen"| N_PER_DE_SVEN_SCH_2001
    N_PER_DE_KARLHEINZ_SCHREIBER["Karlheinz Schreiber"]
    N_PER_DE_WALTHER_LEISLER_KIEP["Walther Leisler Kiep (1926–2016)"]
    N_PER_DE_KARLHEINZ_SCHREIBER -->|"Bundestagsbericht 14/9300 rekonstruiert Schreibers Bitte vom 20.02.1991 an CDU-Schatzmeister Kiep, vor der Entscheidung über Fuchs-Spürpanzer an Saudi-Arabien politisch bei Kohl einzuwirken; keine nachgewiesene Atlantik-Brücke-Briefkopfverwendung 1991"| N_PER_DE_WALTHER_LEISLER_KIEP
    N_PER_DE_KARLHEINZ_SCHREIBER -->|"Schreiber bat Kiep mit Schreiben vom 23.04.1993 als Bear-Head/Thyssen-Lobbyist, Kohl um politische Unterstützung des kanadischen TH-495-Vorhabens zu ersuchen; kein erfolgreicher Beschaffungsauftrag aus dieser Anfrage belegt"| N_PER_DE_WALTHER_LEISLER_KIEP
    N_PER_DE_HELMUT_KOHL["Helmut Kohl (1930–2017)"]
    N_PER_DE_WALTHER_LEISLER_KIEP -->|"Kiep leitete am 27.04.1993 Schreibers TH-495-Vorstoß auf Briefkopf der Atlantik-Brücke an Kohl weiter (eigene Zeugenaussage). Brief vom 28.05.1993 verweist auf eine von Kohl vorgelesene Stellungnahme; keine vereinsseitige Autorisierung oder erfolgreiches Rüstungsgeschäft dadurch bewiesen"| N_PER_DE_HELMUT_KOHL
    N_PER_DE_WALTHER_LEISLER_KIEP -->|"Atlantik-Brücke-Jahresbericht zum 30.06.2009 trägt die Unterschrift Walther Leisler Kieps als Ehrenvorsitzendem; nicht gleichbedeutend mit einem Vorstandsbeschluss über seinen TH-495-Lobbybrief von 1993"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PER_DE_KARLHEINZ_SCHREIBER -->|"Bundestags-Untersuchungsausschuss Drs. 14/9300 nennt Schreiber im Zusammenhang mit den frühen 1990er Jahren Mitglied der Atlantik-Brücke; Höhe eines Vereinsbeitrags oder Vorstandsvollmacht nicht nachgewiesen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_THYSSEN_1991["Thyssen-Konzern (historisch, 1991–1993)"]
    N_ORG_PA_ATG_1991["A.T.G. (panamaische Gesellschaft, 1991)"]
    N_ORG_DE_THYSSEN_1991 -->|"Bundestagsausschuss Drs. 14/9300 S. 374 stellte 11 Mio. DM Thyssen-Zufluss vom 02.08.1991 auf A.T.G.-Schweizer Bankkonto fest, aus Saudi-Arabien-Geschäft für 36 Fuchs-Spürpanzer; nicht 11 Mio. DM Vereinszuwendung"| N_ORG_PA_ATG_1991
    N_ORG_PA_ATG_1991 -->|"Bundestagsbericht 14/9300 bezeichnet Schreiber als wirtschaftlich Berechtigten hinter der panamaischen A.T.G. mit Konto beim Schweizerischen Bankverein; keine rechtliche Eigentümerschaft von Atlantik-Brücke oder CDU an der A.T.G. daraus abgeleitet"| N_PER_DE_KARLHEINZ_SCHREIBER
    N_PER_DE_KARLHEINZ_SCHREIBER -->|"Bundestagsbericht 14/9300 S. 374 stellt Übergabe von 1 Mio. DM in bar durch Schreiber an CDU-Schatzmeister Kiep am 26.08.1991 in St. Margrethen fest; dies ist derselbe CDU-Parteispendevorgang, keine unabhängige Atlantik-Brücke-Spende"| N_PER_DE_WALTHER_LEISLER_KIEP
    N_ORG_DE_CDU_1991["Christlich Demokratische Union Deutschlands (CDU, 1991)"]
    N_PER_DE_WALTHER_LEISLER_KIEP -->|"Bundestagsbericht: 1 Mio. DM aus dem Schreiber/Thyssen-Geldweg gelangten 1991 über Kiep und den Treuhänder Weyrauch verdeckt zur CDU. Identisch mit der Schreiber-Kiep-Bargeldübergabe, nicht erneut zu addieren und keine nachgewiesene Vereinszuwendung"| N_ORG_DE_CDU_1991
    N_ORG_DE_AUSWAERTIGES_AMT_2008["Auswärtiges Amt (Sponsor 2008/09)"]
    N_ORG_DE_AUSWAERTIGES_AMT_2008 -->|"Atlantik-Brücke-Jahresbericht Juni 2008–Juni 2009 nennt das Auswärtige Amt ausdrücklich unter den Sponsoren; konkrete Haushaltsstelle, Zahlbetrag und Gegenleistungen im Beleg offen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_DEUTSCHE_BANK_2008["Deutsche Bank (Sponsor im Atlantik-Brücke-Jahresbericht 2008/09)"]
    N_ORG_DE_DEUTSCHE_BANK_2008 -->|"Atlantik-Brücke-Jahresbericht 2008/09 nennt Deutsche Bank als Sponsor; Betrag, Rechtsform der Unterstützung und konkrete Gegenleistung nicht angegeben"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_DZ_BANK_2008["DZ BANK (Sponsor 2008/09)"]
    N_ORG_DE_DZ_BANK_2008 -->|"Jahresbericht Atlantik-Brücke 2008/09 nennt DZ BANK ausdrücklich unter acht Sponsoren, ohne individuellen Betrag oder Zweckvertrag"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_MM_WARBURG -->|"Atlantik-Brücke-Jahresbericht 2008/09 nennt M. M. Warburg Bank unter den Sponsoren; Sponsorennennung beweist keinen bezifferten Geldtransfer oder Einfluss auf konkrete Politikentscheidungen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_BUNDESBANK_2008["Deutsche Bundesbank (Sponsor 2008/09)"]
    N_ORG_DE_BUNDESBANK_2008 -->|"Jahresbericht Atlantik-Brücke 2008/09 nennt Deutsche Bundesbank als Sponsor; genaue Unterstützungsart und Betrag sowie heutige Förderung nicht daraus ableitbar"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_VOLKSWAGEN_2008["Volkswagen (Sponsor 2008/09)"]
    N_ORG_DE_VOLKSWAGEN_2008 -->|"Atlantik-Brücke bezeichnet Volkswagen im historischen Jahresbericht 2008/09 ausdrücklich als Sponsor; kein dokumentierter Einzelbetrag oder Kauf politischer Entscheidungen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_STIFTUNG_VAN_MEETEREN["Stiftung van Meeteren (Sponsor 2008/09)"]
    N_ORG_DE_STIFTUNG_VAN_MEETEREN -->|"Atlantik-Brücke-Jahresbericht 2008/09 nennt Stiftung van Meeteren als Sponsor; Stiftungsbewilligung und individueller Geldfluss nicht ausgewiesen"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_BERTELSMANN_STIFTUNG_2008["Bertelsmann Stiftung (Sponsor 2008/09)"]
    N_ORG_DE_BERTELSMANN_STIFTUNG_2008 -->|"Bertelsmann Stiftung wird in der Sponsorenliste des Atlantik-Brücke-Jahresberichts 2008/09 genannt, ohne ausgewiesenen Förderbetrag und ohne Beleg einer konkreten Einflussanweisung"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_DE_DEUTSCHE_BANK_2008 -->|"Atlantik-Brücke-Jahresbericht 2008/09 S. 82–83: XVII. Expertengespräch mit U.S. European Command und Bundeswehrführung am 16.09.2008 auf Einladung der Deutschen Bank in ihrer Berliner Hauptstadtrepräsentanz; Gastgeberrolle ist kein Beleg einer Waffenbeschaffungsentscheidung"| N_ORG_DE_ATLANTIK_BRUECKE
    N_PRG_DE_AB_JOURNALISTS_1983_1992["Atlantik-Brücke-Journalistenreisen für US-Medienschaffende 1983–1992"]
    N_ORG_DE_ATLANTIK_BRUECKE -->|"Pechels Brief vom 23.01.1992 als Atlantik-Brücke-Kuratoriumsmitglied beschreibt seit 1983 organisierte US-Journalistenreisen mit laut Organisator 121 Teilnehmenden bis 1991; vollständige Namens- und Artikelprüflisten liegen hier nicht vor"| N_PRG_DE_AB_JOURNALISTS_1983_1992
    N_ORG_DE_ZEIT_STIFTUNG_1991["ZEIT-Stiftung Ebelin und Gerd Bucerius (Förderbericht 1991)"]
    N_ORG_DE_ZEIT_STIFTUNG_1991 -->|"ZEIT-Stiftungs-Chronik führt für 1991 eine Unterstützung des Atlantik-Brücke-Journalistenreiseprogramms über 10.000 DM auf; nicht mit Zahlungen von Bosch oder GMF zu addieren, die im Brief ohne Betrag erwähnt werden"| N_PRG_DE_AB_JOURNALISTS_1983_1992
    N_ORG_DE_ROBERT_BOSCH_STIFTUNG["Robert Bosch Stiftung"]
    N_ORG_DE_ROBERT_BOSCH_STIFTUNG -->|"Pechel nennt die Robert Bosch Stiftung im reproduzierten Schreiben vom Januar 1992 als Förderer des Atlantik-Brücke-Journalistenreiseprogramms; Einzeljahr, Geldsumme und tatsächlicher Zahlungslauf nicht dokumentiert"| N_PRG_DE_AB_JOURNALISTS_1983_1992
    N_ORG_US_GMF_2012["German Marshall Fund of the United States (GMF)"]
    N_ORG_US_GMF_2012 -->|"Pechel nennt German Marshall Fund 1992 als Förderer des Atlantik-Brücke-Journalistenreiseprogramms; der Betrag und das genaue Zuwendungsjahr dieser historischen Förderung sind nicht beziffert und nicht mit IRS-Grants von 2012 gleichzusetzen"| N_PRG_DE_AB_JOURNALISTS_1983_1992
    N_PER_DE_PETER_E_PECHEL["Peter E. Pechel"]
    N_PER_DE_PETER_E_PECHEL -->|"Peter E. Pechel nennt sich im am 23.01.1992 reproduzierten Schreiben Mitglied des Kuratoriums der Atlantik-Brücke; seine Angaben zu Teilnehmerzahlen bleiben Organisatorberichte"| N_ORG_DE_ATLANTIK_BRUECKE
    N_ORG_US_ACG_2012["American Council on Germany (ACG)"]
    N_ORG_US_GMF_2012 -->|"GMF meldete in IRS Form 990 Schedule I für 2012 50.000 USD Geldzuschuss an American Council on Germany (EIN 13-1889074), Zweck Transatlantic Dialogue; keine direkte Atlantik-Brücke-Zahlung aus dieser Zeile"| N_ORG_US_ACG_2012
    N_ORG_US_AICGS_2012["American Institute for Contemporary German Studies (AICGS)"]
    N_ORG_US_GMF_2012 -->|"GMF Form 990 Schedule I 2012 nennt 50.000 USD Geldzuschuss an AICGS (EIN 52-1309525), Zweck Transatlantic Dialogue; getrennt vom gleich hohen ACG-Zuschuss"| N_ORG_US_AICGS_2012
    N_ORG_US_FORMER_CONGRESS_MEMBERS_2012["U.S. Association of Former Members of Congress"]
    N_ORG_US_GMF_2012 -->|"GMF Form 990 Schedule I 2012 nennt 90.000 USD Geldzuschuss an U.S. Association of Former Members of Congress (EIN 54-0883744) für Transatlantic Dialogue; keine Zahlung an deutsches Journalistenreiseprogramm hieraus abgeleitet"| N_ORG_US_FORMER_CONGRESS_MEMBERS_2012
    N_PRG_US_ARTHUR_BURNS_FELLOWSHIP_2012["Arthur Burns Fellowship (2012, US-Steuerfall)"]
    N_ORG_US_GMF_2012 -->|"GMF Form 990 Schedule I 2012 erfasst 20.000 USD Geldzuschuss an Arthur Burns Fellowship (EIN 54-1629976) für Transatlantic Dialogue; kein Beleg einer inhaltlich beauftragten journalistischen Veröffentlichung"| N_PRG_US_ARTHUR_BURNS_FELLOWSHIP_2012
    N_PER_IT_LICIO_GELLI["Licio Gelli (1919–2015)"]
    N_ORG_IT_LOGGIA_P2_1970_1981["Loggia massonica Propaganda 2 (P2, historisch)"]
    N_PER_IT_LICIO_GELLI -->|"Der P2-Untersuchungsbericht 1984 beschreibt Licio Gelli als maßgeblichen Leiter der historischen Loge; daraus folgt kein individueller Beweis für jeden bei Rizzoli untersuchten Bankvorgang oder für Anschlagsweisungen"| N_ORG_IT_LOGGIA_P2_1970_1981
    N_ORG_IT_RIZZOLI_EDITORE_1975_1984["Rizzoli Editore S.p.A. (Verlagsgruppe historisch 1975–1984)"]
    N_ORG_IT_LOGGIA_P2_1970_1981 -->|"Die Anselmi-Kommission beschreibt für 1975–1981 Gelli und Ortolani als Koordinatoren eines Finanzierungs- und Einflussmechanismus im Rizzoli-Konzern; dies ist ihr Befund, kein hier unabhängig bewiesener Einzelbefehl an Journalisten"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_ORG_IT_CORRIERE_DELLA_SERA_1980["Corriere della Sera (italienische Zeitung, 1980)"]
    N_ORG_IT_RIZZOLI_EDITORE_1975_1984 -->|"Historische Rizzoli-Verlagsgruppe als Trägerin des Corriere della Sera; die Anselmi-Kommission bewertet den finanziellen Druck und die redaktionelle Einwirkung im konkreten historischen Zeitraum, nicht eine ständige Weisung an jeden Artikel"| N_ORG_IT_CORRIERE_DELLA_SERA_1980
    N_PER_IT_ANGELO_RIZZOLI["Angelo Rizzoli (1943–2013)"]
    N_PER_IT_ANGELO_RIZZOLI -->|"Angelo Rizzoli als historischer Verlagsvertreter an der Kapital- und Sanierungsstruktur beteiligt; Originalvertrag vom 18.09.1980 und Paraphengutachten nennen ihn unter den beteiligten Personen"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_PER_IT_BRUNO_TASSAN_DIN["Bruno Tassan Din"]
    N_PER_IT_BRUNO_TASSAN_DIN -->|"Bruno Tassan Din wird von der P2-Kommission als Generaldirektor der Rizzoli-Gruppe und Beteiligter an der Vereinbarung 1980 aufgeführt; die Rolle belegt keine einzelne Kontotransaktion"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_PER_IT_UMBERTO_ORTOLANI["Umberto Ortolani (1913–2002)"]
    N_PER_IT_UMBERTO_ORTOLANI -->|"Nach Anselmi-Mehrheitsbericht trat Umberto Ortolani 1978 in den Rizzoli-Verwaltungsrat ein; diese Organrolle beweist allein keine konkrete Auslandszahlung"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_PER_IT_ROBERTO_CALVI["Roberto Calvi (1920–1982)"]
    N_PER_IT_ROBERTO_CALVI -->|"Die parlamentarische P2-Untersuchung beschreibt Roberto Calvi als Bankmanager und Finanzierungsakteur im Banco-Ambrosiano-Komplex; seine Signatur 1980 ist von einem separat ausgezahlten Kredit zu unterscheiden"| N_ORG_IT_BANCO_AMBROSIANO_SPA_1979
    N_ORG_IT_AMBROSIANO_BANKS_1980["Banken des Banco-Ambrosiano-Konzerns (historisch 1980)"]
    N_ORG_IT_AMBROSIANO_BANKS_1980 -->|"Anselmi-Bericht 1984, gedruckte S. 122: Banken des Ambrosiano-Verbunds gewährten Rizzoli Editore Finanzierung über 22,5 Milliarden Lire zur Rückzahlung älterer Agnelli-Verpflichtungen. Einzelbank und tatsächliche Valuta hier nicht durch separate Bankbelege geprüft"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_ORG_IT_LA_CENTRALE_FINANZIARIA_SPA -->|"Die Anselmi-Kommission schildert im Rizzoli-Sanierungsprozess eine auf La Centrale Finanziaria S.p.A. lautende 40-Prozent-Aktienposition; der genaue Vollzug jeder wirtschaftlichen Eigentümerstufe ist nur mit Aktienbuch und Treuhandverträgen prüfbar"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_ORG_IT_LOGGIA_P2_1970_1981 -->|"Anselmi-Bericht 1984 bezeichnet die von Gelli und Ortolani betriebene Bestellung des Chefredakteurs Di Bella sowie redaktionelle Einwirkungen als Teil des P2-Einflusses; Beweisrang parlamentarische Bewertung, keine nachgewiesene Steuerung jedes Corriere-Beitrags"| N_ORG_IT_CORRIERE_DELLA_SERA_1980
    N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980["Rizzoli-P2-Sanierungsvereinbarung vom 18.09.1980 (Reperto 1/C)"]
    N_PER_IT_LICIO_GELLI -->|"Original Sanierungsvereinbarung vom 18.09.1980 und Perrella-Gutachten ordnen die Paraphen Licio Gelli zu; intern abweichende Januar-Angaben im Gutachten, September durch Vertragsdatum und Dezembernachtrag gestützt; kein Kontobeleg"| N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980
    N_PER_IT_UMBERTO_ORTOLANI -->|"Perrella-Gutachten ordnet Umberto Ortolani zu den fünf Paraphierenden des Sanierungsdokuments 18.09.1980; die Unterschrift bedeutet keinen unabhängig verifizierten späteren Mitteltransfer"| N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980
    N_PER_IT_ROBERTO_CALVI -->|"Originalvertrag 18.09.1980 und Paraphengutachten führen Roberto Calvi als Beteiligten; vertragliche Mitwirkung und finanzielle Auszahlung sind zwei unterschiedliche Beweisfragen"| N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980
    N_PER_IT_ANGELO_RIZZOLI -->|"Angelo Rizzoli wurde vom Originalvertrag und Sachverständigen den Paraphen des Sanierungsentwurfs vom 18.09.1980 zugeordnet; ohne damit die tatsächliche Durchführung der geplanten Aktienverteilung zu behaupten"| N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980
    N_PER_IT_BRUNO_TASSAN_DIN -->|"Original-Paraphenbefund zu Bruno Tassan Din auf Sanierungsvereinbarung vom 18.09.1980; November-/Dezember-Umsetzung und gezahlte Kautionssumme nicht aus der Paraphe selbst abgeleitet"| N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980
    N_DOC_IT_RIZZOLI_P2_AGREEMENT_1980 -->|"Reperto 1/C: Rizzoli-Sanierungsplan 18.09.1980 mit vorgesehenem Aktienmodell 40/10,2/40/9,8 Prozent und geplantem Premio; Nachtrag 18.12.1980 verlängerte bis 31.03.1981, ohne vollständigen Nachweis aller Geld- und Eigentumsübertragungen"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_DOC_IT_RIZZOLI_CARACCIOLO_SCALFARI_PACT_1979["Pressevereinbarung Rizzoli–Caracciolo–Scalfari vom 05.07.1979"]
    N_PER_IT_ANGELO_RIZZOLI -->|"Unterzeichnete Rizzoli–Caracciolo–Scalfari-Pressevereinbarung vom 05.07.1979 benennt Angelo Rizzoli als Partei; die Vereinbarung über nicht-feindliche Darstellung ersetzt keinen Nachweis der späteren redaktionellen Durchführung"| N_DOC_IT_RIZZOLI_CARACCIOLO_SCALFARI_PACT_1979
    N_PER_IT_BRUNO_TASSAN_DIN -->|"Bruno Tassan Din ist auf dem 05.07.1979 unterzeichneten Pressevertrag als Rizzoli-Vertreter beteiligt; der gezeichnete Wortlaut belegt keine von Gelli vermittelte Banco-Ambrosiano-Zusage"| N_DOC_IT_RIZZOLI_CARACCIOLO_SCALFARI_PACT_1979
    N_PER_IT_CARLO_CARACCIOLO["Carlo Caracciolo (1925–2008)"]
    N_PER_IT_CARLO_CARACCIOLO -->|"Carlo Caracciolo unterzeichnete am 05.07.1979 eine verlagsübergreifende Pressekooperationsvereinbarung; seine spätere Aussage 1983 über bestrittenen Vollzug und fehlende Gelli-Kontakte ist davon getrennt"| N_DOC_IT_RIZZOLI_CARACCIOLO_SCALFARI_PACT_1979
    N_PER_IT_EUGENIO_SCALFARI["Eugenio Scalfari (1924–2022)"]
    N_PER_IT_EUGENIO_SCALFARI -->|"Eugenio Scalfari war 1979 Vertragsunterzeichner. In seiner Aussage vom 13.05.1981 bestritt er, dass Bankzugangs- und Wettbewerbsverbotszusätze aus einer Gelli-Notiz Teil des unterzeichneten Endtextes waren"| N_DOC_IT_RIZZOLI_CARACCIOLO_SCALFARI_PACT_1979
    N_DOC_IT_RIZZOLI_CARACCIOLO_SCALFARI_PACT_1979 -->|"Unterzeichneter Vertrag 05.07.1979 regelt gegebenenfalls gemeinsame Presseinvestitionen, Konsultationen und Bemühen um objektive nicht-feindliche Berichterstattung zwischen Verlagen; unbewiesene redaktionelle Weisung und bestrittene Banco-Ambrosiano-Zusatzklausel nicht als Vertragsinhalt modelliert"| N_ORG_IT_RIZZOLI_EDITORE_1975_1984
    N_ORG_DE_BMWI_2019["Bundesministerium für Wirtschaft und Energie (BMWi, 2019)"]
    N_PRG_DE_ERP_TRANSATLANTIK_2019["Deutsches Programm für transatlantische Begegnung (ERP-Sondervermögen)"]
    N_ORG_DE_BMWI_2019 -->|"ERP-Wirtschaftsplangesetz 2019 Titel 681 03-029: BMWi bewilligt im Einvernehmen mit interministeriellem Ausschuss; Bundesansatz 3,6 Mio. EUR für das gesamte Transatlantik-Begegnungsprogramm, weder ACG-Bewilligung noch tatsächlich ausgezahlter ACG-Betrag"| N_PRG_DE_ERP_TRANSATLANTIK_2019
    N_PRG_DE_ERP_TRANSATLANTIK_2019 -->|"ACG-Jahresbericht 2018 gedruckte S. 19 führt European Recovery Program – Transatlantic Program in Kategorie '$50,000 and above' als Institutional/Grant Support (blauer Punkt); Kategoriebetrag ist kein geprüfter Kontotransfer und keinem einzelnen Projekt zugeordnet"| N_ORG_US_ACG_2012
    N_PRG_US_ACG_CITIES_2019["ACG Transatlantic Cities of Tomorrow – Digitalization and Future of Work (2019)"]
    N_PRG_DE_ERP_TRANSATLANTIK_2019 -->|"ACG nennt für das 2019er Transatlantic Cities of Tomorrow-Programm in USA (29.04.–04.05.) und Deutschland (30.06.–06.07.) Unterstützung über das Bundes-ERP-Programm des BMWi; beide Reisen gehören zu einem Förderprogramm, nicht zu zwei nachgewiesenen Bundesüberweisungen"| N_PRG_US_ACG_CITIES_2019
    N_ORG_US_ACG_2012 -->|"ACG organisierte laut zwei offiziellen Eigenberichten 2019 das Austauschprogramm mit 16 Teilnehmenden bei einer USA-Reise Ende April/Anfang Mai und einem Gegenbesuch in Deutschland Anfang Juli; Teilnehmerzahl nicht doppelt als 32 individuelle Personen gezählt"| N_PRG_US_ACG_CITIES_2019
    N_PRG_US_ACG_CITIES_2019 -->|"ACG-Gegenbesuchsbericht 2019 beschreibt Delegationskontakt mit Vertretern des BMWi zu Digitalisierung und Industrie 4.0 in Berlin; kein Nachweis einer Gesetzesänderung, Förderentscheidung im Gespräch oder individuellen Gegenleistung"| N_ORG_DE_BMWI_2019
    N_ORG_DE_BDI_2019["Bundesverband der Deutschen Industrie (BDI, 2019)"]
    N_PRG_US_ACG_CITIES_2019 -->|"ACG berichtet einen Berliner Austausch der 16-köpfigen Delegation mit Vertretern des Bundesverbands der Deutschen Industrie zur Digitalisierungsstrategie 2019; kein belegter Lobbyerfolg oder gemeinsam formulierter Gesetzestext"| N_ORG_DE_BDI_2019
    N_PER_DE_MARJA_LIISA_VOELLERS_2019["Marja-Liisa Völlers (Bundestagsabgeordnete 2019)"]
    N_PER_DE_MARJA_LIISA_VOELLERS_2019 -->|"Die damalige Bundestagsabgeordnete Marja-Liisa Völlers diskutierte laut ACG-Projektbericht im Juli 2019 mit Austauschdelegierten die Modernisierung beruflicher Bildung in digitalisierter Arbeitswelt; kein Nachweis einer dadurch ausgelösten parlamentarischen Initiative"| N_PRG_US_ACG_CITIES_2019
    N_PRG_US_ACG_WARBURG_2018["ACG Eric M. Warburg Chapters – ERP-finanzierte Rednertouren (2018)"]
    N_PRG_DE_ERP_TRANSATLANTIK_2019 -->|"ACG-Jahresbericht 2018, gedruckte S. 9: ERP Program for Transatlantic Encounters unterstützte ausdrücklich zehn Rednertouren der Warburg-Chapters-Reihe Restoring Trust Through Dialogue; mehr als 70 Chapters-Veranstaltungen sind keine 70 ERP-finanzierten Reisen"| N_PRG_US_ACG_WARBURG_2018
    N_ORG_US_ACG_2012 -->|"ACG-Jahresbericht 2018 dokumentiert eigene Eric-M.-Warburg-Chapters mit 21 regionalen Gruppen und zehn ERP-geförderten Speaker Tours. Nennung eines einzelnen Referenten auf derselben Seite beweist keine persönliche öffentliche Zahlung"| N_PRG_US_ACG_WARBURG_2018
    N_ORG_CH_UBS_GENEVA_1980["Union de Banques Suisses (UBS Genf, historische Kontoführung 1980/81)"]
    N_ORG_CH_UBS_GENEVA_1980 -->|"UBS Genf bestätigte im am 11.05.1981 veröffentlichten Rechtshilfe-Originalbrief Licio Gelli als Inhaber der Kontenkennungen 596.757.K.J. 60 T und 525.779.X.S. 60 R; keine Anschlagsfinanzierungs-Zweckbindung durch diese Kontoinhabernennung"| N_PER_IT_LICIO_GELLI
    N_PER_IT_MARCO_CERUTI_1980["Marco Ceruti (historischer UBS-Kontoinhaber)"]
    N_ORG_CH_UBS_GENEVA_1980 -->|"UBS Genf nannte Marco Ceruti im Originalbrief 11.05.1981 als Kontoinhaber 525.366.B.W. 60 A und 525.367.B.X. 60 D, die laut Brief geschlossen waren; diese Kontokennungen nicht ohne Stammblatt mit anderen Bukada-/Tortuga-Formaten gleichsetzen"| N_PER_IT_MARCO_CERUTI_1980
    N_ORG_PE_AMBROSIANO_ANDINO -->|"Bologna-Gerichtstext im 2024er Domani-Auszug rekonstruiert 20 Mio. USD aus Banco Ambrosiano Andino an UBS Genf ab 22.08.1980, also NACH dem Anschlag 02.08.1980. 15 Mio. USD gelten darin als Teilmenge, nicht zusätzliche Zahlung; endgültige Anschlagsfinanzierung hieraus nicht bewiesen"| N_ORG_CH_UBS_GENEVA_1980
    N_DOC_IT_DOCUMENTO_BOLOGNA_1982["Documento Bologna (bei Licio Gelli 1982 sichergestellte Banknotiz)"]
    N_PER_IT_LICIO_GELLI -->|"Laut öffentlich reproduziertem Bellini-Gerichtstext wurde das später als documento Bologna bezeichnete gefaltete Bankdokument bei Gellis Festnahme am 13.09.1982 in Genf aus seiner Brieftasche sichergestellt und am 18.02.2019 erneut archivisch erhoben; Dokumentbesitz ist nicht der Nachweis einer konkreten Bombenfinanzierungsanweisung"| N_DOC_IT_DOCUMENTO_BOLOGNA_1982
    N_ORG_IT_PROCURA_GENERALE_BOLOGNA_2024["Procura Generale della Repubblica Bologna (2024)"]
    N_ORG_IT_PROCURA_GENERALE_BOLOGNA_2024 -->|"Generalstaatsanwaltschaft Bologna berichtete am 27.01.2024 über die erstinstanzliche Zuschreibung einer Anschlagsfinanzierungsrolle an Licio Gelli und kennzeichnet die Deutung des documento Bologna als Anschlagsbuchhaltung ausdrücklich als eigene Auffassung; kein neuer persönlicher Schuldspruch wegen des Anschlags"| N_PER_IT_LICIO_GELLI
    N_PER_IT_FEDERICO_UMBERTO_DAMATO["Federico Umberto D'Amato (1919–1996)"]
    N_ORG_IT_PROCURA_GENERALE_BOLOGNA_2024 -->|"Amtlicher Bericht der Generalstaatsanwaltschaft 2024 bezeichnet Federico Umberto D'Amato im Bellini-Prozess als mutmaßlichen Empfänger einer 850.000-USD-Position des documento Bologna; individuelle Kontogutschrift und Verfügungsberechtigung an Originalbanken hier nicht nachgewiesen; keine persönliche neue Verurteilung"| N_PER_IT_FEDERICO_UMBERTO_DAMATO
    N_PER_IT_ROBERTO_CALVI -->|"Bellini-Gerichtsurteil diskutiert und verweist auf Mailänder Bankrotturteil 1992: Calvi soll rund 20 Mio. USD in Erwartung unzulässigen Einflusses auf seine Gerichtsverfahren Gelli zur Verfügung gestellt haben; Alternative zur gewöhnlichen Anwaltsgebühr und keine durch diesen Absatz nachgewiesene identische Finanzierung des Bologna-Anschlags"| N_PER_IT_LICIO_GELLI
    N_PER_IT_LICIO_GELLI -->|"Bellini-Erstinstanzurteil Druck-S. 751 deutet die im Dokument MC vermerkte Position über 1 Mio. USD Bargeld für Marco Ceruti auf 20.–30.07.1980 als auffälligen VOR-Anschlags-Vorgang; Original-Kassenbeleg und tatsächlicher Bombenfinanzierungszweck bleiben ungeklärt"| N_PER_IT_MARCO_CERUTI_1980
    N_ORG_DE_BUNDESREGIERUNG_1975["Bundesregierung der Bundesrepublik Deutschland (1975)"]
    N_PRG_US_MCCLOY_FUND_1975["John J. McCloy Fund for German-American Exchanges (1975)"]
    N_ORG_DE_BUNDESREGIERUNG_1975 -->|"Bundesregierung der Bundesrepublik stellte nach Scheels öffentlicher Erklärung im Weißen Haus vom 16.06.1975 einen Kapitalstock von 1.000.000 USD für den John-J.-McCloy-Austauschfonds bereit; ACG bestätigte 2025 die Zuwendung. Kein selbst eingesehener individueller Zahlungs- oder Verwendungs-Kontoauszug"| N_PRG_US_MCCLOY_FUND_1975
    N_PRG_US_MCCLOY_FUND_1975 -->|"Das 1-Mio.-USD-Fondsvorhaben wurde am 16.06.1975 ausdrücklich unter dem Dach des American Council on Germany (ACG) angesiedelt; die Organisation beschreibt 2025 dessen institutionelle Annahme. Einzelne Publikationsausgaben nicht dadurch bewiesen"| N_ORG_US_ACG_2012
    N_PER_US_JOHN_J_MCCLOY["John J. McCloy (1895–1989)"]
    N_PER_US_JOHN_J_MCCLOY -->|"Präsident Gerald Fords Daily Diary für 16.06.1975 nennt John J. McCloy ausdrücklich Chairman of the Board des American Council on Germany; Vorstandsfunktion allein belegt keine individuelle Weisung an publizierende Journalisten"| N_ORG_US_ACG_2012
    N_PER_DE_WALTER_SCHEEL["Walter Scheel (1919–2016)"]
    N_PER_DE_WALTER_SCHEEL -->|"Bundespräsident Walter Scheel stellte den John-J.-McCloy-Fonds am 16.06.1975 im Weißen Haus öffentlich vor, benannte 1 Mio. USD staatliches Fondsvermögen und die Zwecke Nachwuchsaustausch, Konferenzen und Publikationen; Scheel war nicht Privatspender"| N_PRG_US_MCCLOY_FUND_1975
    N_PER_US_GERALD_FORD["Gerald R. Ford (1913–2006)"]
    N_PER_US_GERALD_FORD -->|"US-Präsident Gerald Ford war laut seinem Tageskalender am 16.06.1975 von 13:01 bis 13:20 Uhr Gastgeber der Rose-Garden-Zeremonie für den von der Bundesrepublik bereitgestellten Fonds; die Gastgeberrolle beweist keine Auswahl einzelner Austauschstipendien"| N_PRG_US_MCCLOY_FUND_1975
    N_ORG_US_ACG_2012 -->|"ACG-Geschichte und Zetsches Archivstudie dokumentieren den gemeinsamen Start der American-German Young Leaders Conference 1973 durch ACG und Atlantik-Brücke in Hamburg; dies war zwei Jahre VOR der McCloy-Bundesdotierung 1975"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_ORG_US_FORD_FOUNDATION_1973["Ford Foundation (historische Förderakten 1973)"]
    N_ORG_US_FORD_FOUNDATION_1973 -->|"Zetsche (2016), S. 172 FN 157, weist unter Rockefeller Archive Center Ford Foundation Grant Files 1239, ACG & 7300512 eine TEILförderung der ersten ACG/Atlantik-Brücke-Young-Leaders-Konferenz vom 27.–30.06.1973 nach; Original Grant Action Form und Fördersumme hier nicht selbst eingesehen"| N_PRG_DE_ATLANTIK_BRUECKE_YOUNG_LEADERS
    N_PRG_US_ACG_MCCLOY_FELLOWSHIPS_1976["ACG McCloy Fellowships (Beginn 1976)"]
    N_ORG_US_ACG_2012 -->|"ACG-Jahresbericht 2017 datiert Beginn der McCloy Fellowships auf 1976; geförderte Austauschberufe einschließlich Journalismus, Recht, Gewerkschaften und Kommunalverwaltung. Direkter Geldtransfer aus dem 1975er Fonds in ein einzelnes Stipendium nicht vorgelegt"| N_PRG_US_ACG_MCCLOY_FELLOWSHIPS_1976
    N_ORG_DE_WARBURG_FMWV_2013["Familie Max Warburg Vermögensverwaltung KG (FMWV)"]
    N_ORG_DE_WARBURG_MWB1_2023["1. Max Warburg Beteiligungsgesellschaft mbH (MWB 1)"]
    N_ORG_DE_WARBURG_FMWV_2013 -->|"EuG T-366/23 Rn. 4: 2013 gingen 87,5 % des MWB-1-Kapitals zugunsten der Kinder auf FMWV über; ein anonymisierter Altinhaber behielt 12,5 % Kapital und über Golden Share 51 % Stimmen, außerdem Pooling/Nießbrauch. Keine Gleichsetzung von 87,5 % Kapital mit 87,5 % Stimmen oder aktuelle 2026er Quote"| N_ORG_DE_WARBURG_MWB1_2023
    N_ORG_DE_WARBURG_GRUPPE_2023["M.M.Warburg & CO Gruppe GmbH (Eigentumsstand im EuG-Verfahren 2023)"]
    N_ORG_DE_WARBURG_MWB1_2023 -->|"EuG T-366/23 Rn. 5: MWB 1 hielt laut Urteil für den 2023er Sachstand 40,24 % Kapital an der Warburg-Gruppe; weiterer 41,25-%-Block im Urteil nicht namentlich bezeichnet. Keine ungeprüfte Aktualisierung auf 2026"| N_ORG_DE_WARBURG_GRUPPE_2023
    N_ORG_DE_WARBURG_GRUPPE_2023 -->|"EuG T-366/23 Rn. 6: Die Finanzholding Warburg-Gruppe hielt zum entscheidungserheblichen historischen Sachstand 2023 unmittelbar 100 % des Kapitals von M.M.Warburg & CO (AG & Co.) KGaA; nicht als unveränderte 2026er Registerlage behauptet"| N_ORG_DE_MM_WARBURG
    N_ORG_DE_MARCARD_STEIN_2023["Marcard, Stein & Co AG (Warburg-Tochter 2023)"]
    N_ORG_DE_MM_WARBURG -->|"EuG T-366/23 Rn. 6: Marcard, Stein & Co AG war zum Stand der EZB-Entscheidung vom 05.05.2023 100-%-Tochter der Warburg-Bank; 2026er Veräußerungsankündigung nicht als bereits vollzogener Verkauf oder fortbestehendes Eigentum interpretiert"| N_ORG_DE_MARCARD_STEIN_2023
    N_ORG_DE_WARBURG_HYPO_2023["M.M.Warburg & CO Hypothekenbank AG (historische Beteiligung 2023)"]
    N_ORG_DE_MM_WARBURG -->|"EuG T-366/23 Rn. 6: 60-%-Beteiligung der Warburg-Bank an der Hypothekenbank im historischen Verfahren; Verkauf am 03.11.2022 vereinbart, zum 01.06.2023 wirksam. Keine über diesen Zeitpunkt fortdauernde Warburg-Eigentümerschaft"| N_ORG_DE_WARBURG_HYPO_2023
    N_ORG_DE_BAFIN_2023["Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin, im Verfahren 2023)"]
    N_ORG_DE_BAFIN_2023 -->|"EuG T-366/23 Rn. 2: BaFin beaufsichtigte das im Verfahren als weniger bedeutend eingestufte Kreditinstitut Warburg unmittelbar; der 2023er Zuständigkeitsbefund ist keine Feststellung einer strafbaren Gegenleistung"| N_ORG_DE_MM_WARBURG
    N_ORG_EU_ECB_2023["Europäische Zentralbank (EZB)"]
    N_ORG_EU_ECB_2023 -->|"EuG T-366/23 Rn. 2: Die EZB übte beim weniger bedeutenden Warburg-Kreditinstitut 2023 mittelbare Aufsicht aus; von der direkten BaFin-Aufsicht und der gesonderten Erwerbsuntersagung zu unterscheiden"| N_ORG_DE_MM_WARBURG
    N_ORG_DE_WARBURG_MWB1_2023 -->|"EuG T-366/23 Rn. 9: Im Rahmen der BaFin-Prüfung 2019 vereinbarte MWB 1 zwei seit Februar 2020 eingesetzte Bevollmächtigte zur Ausübung der Stimmrechte an der Warburg-Gruppe. Kein Beleg, dass die Vollmachten unverändert bis 2026 fortbestanden oder kapitalrechtliche Anteile übertrugen"| N_ORG_DE_WARBURG_GRUPPE_2023
    N_ORG_EU_ECB_2023 -->|"EZB-Beschluss vom 05.05.2023 untersagte laut EuG T-366/23 Rn. 1 und 19–23 einen geplanten qualifizierten indirekten Erwerb einer Beteiligung am Warburg-Institut; die Übertragung des Golden Share an die Ehefrau war nur beabsichtigt, keine vollzogene Eigentumsübertragung"| N_ORG_DE_MM_WARBURG
    N_ORG_EU_GENERAL_COURT_2025["Gericht der Europäischen Union (EuG, Urteil 19.11.2025)"]
    N_ORG_EU_GENERAL_COURT_2025 -->|"EuG T-366/23 wies am 19.11.2025 die Klage gegen den EZB-Erwerbsbeschluss vom 05.05.2023 ab; laut amtlichem InfoCuria-Register ist das am 27.01.2026 eingelegte Rechtsmittel C-39/26 P am 21.11.2026 noch anhängig. Keine letztinstanzliche Bestätigung, neue Eigentumsübertragung oder persönliche Straftat daraus ableiten"| N_ORG_EU_ECB_2023
    N_DOC_DE_SPRINGER_VINKULIERUNG_2006["Vinkulierungsvereinbarung Döpfner–Brilliant–Springer–Warburg vom 31.07./04.08.2006"]
    N_ORG_DE_MM_WARBURG -->|"Axel-Springer-Originalgeschäftsbericht 2006 S. 37 nennt M.M.Warburg & Co. KGaA neben Döpfner, Brilliant 310. GmbH und Axel Springer AG als Partei der Vinkulierungsvereinbarung vom 31.07./04.08.2006. Dies belegt den Vertragskontakt, NICHT individuelle Kredithöhe, Auszahlung oder redaktionelle Weisung"| N_DOC_DE_SPRINGER_VINKULIERUNG_2006
    N_PER_DE_MATHIAS_DOEPFNER -->|"Mathias Döpfner ist laut Axel-Springer-Geschäftsbericht 2006 namentliche Partei des 31.07./04.08.2006 geschlossenen vierseitigen Aktien-Vinkulierungsvertrags mit Brilliant 310. GmbH, Axel Springer AG und M.M.Warburg & Co.; Bankkreditkonditionen daraus nicht ersichtlich"| N_DOC_DE_SPRINGER_VINKULIERUNG_2006
    N_ORG_DE_BRILLIANT_310_2006["Brilliant 310. GmbH (im Springer-Vertrag 2006)"]
    N_ORG_DE_BRILLIANT_310_2006 -->|"Brilliant 310. GmbH ist im Axel-Springer-Originalgeschäftsbericht 2006 als beteiligte Gesellschaft an der am 31.07./04.08.2006 geschlossenen Vinkulierungsvereinbarung genannt; der Vertrag regelt mittelbare und unmittelbare Aktienverfügungen unter Zustimmungsvorbehalt"| N_DOC_DE_SPRINGER_VINKULIERUNG_2006
    N_ORG_DE_AXEL_SPRINGER -->|"Axel Springer AG war laut eigenem Geschäftsbericht 2006 Partei des Vinkulierungsvertrags mit Döpfner, Brilliant 310. GmbH und Warburg; direkte und indirekte Verfügungen über die betroffenen Namensaktien verlangten ihre satzungsgemäße Zustimmung. Kein Vertrag über redaktionelle Entscheidungen"| N_DOC_DE_SPRINGER_VINKULIERUNG_2006
    N_PER_DE_MATHIAS_DOEPFNER -->|"Axel-Springer-Mitteilung 20.07.2006 nennt mittelbaren Erwerb von 680.000 damaligen Namensaktien zu je 77 EUR (2 %), Kaufpreis rechnerisch 52,36 Mio. EUR; andere Größe als der 2023 journalistisch berichtete rund 60-Mio.-EUR-Kredit. Der Emittent nennt keine Darlehenssumme"| N_ORG_DE_AXEL_SPRINGER
    N_PER_DE_FRIEDE_SPRINGER -->|"Axel-Springer-Geschäftsbericht 2012 gedruckte S. 57 dokumentiert, dass Friede Springer Döpfner am 14.08.2012 insgesamt 1.978.800 Aktien schenkte; keine Übertragung des gesamten Stimmrechtspools und kein Beleg einer bankbezogenen Gegenleistung"| N_PER_DE_MATHIAS_DOEPFNER
    N_DOC_DE_SPRINGER_VOTING_POOL_2012["Axel-Springer-Stimmrechtspool (2012, 52.826.967 Aktien)"]
    N_PER_DE_MATHIAS_DOEPFNER -->|"Döpfner trat laut Geschäftsbericht 2012 am 14.08.2012 nach der Schenkung von 1.978.800 Aktien dem von Friede Springer und Friede Springer GmbH & Co KG getragenen Pool bei; 52.826.967 poolgebundene Aktien sind NICHT Döpfners persönliche Eigentumsaktien"| N_DOC_DE_SPRINGER_VOTING_POOL_2012
    N_PER_DE_FRIEDE_SPRINGER -->|"Der Axel-Springer-Geschäftsbericht 2012 nennt Friede Springer und Friede Springer GmbH & Co. KG als Parteien des Stimmrechtspools, dem Döpfner am 14.08.2012 beitrat; keine Warburg-Bankbeteiligung an diesem späteren Poolvertrag belegt"| N_DOC_DE_SPRINGER_VOTING_POOL_2012
    N_DOC_DE_SPRINGER_VOTING_POOL_2012 -->|"Axel Springer 2012 gedruckte S. 57: Poolvereinbarung umfasste 52.826.967 stimmberechtigte Aktien. Poolmitglieder stimmen in der Hauptversammlung gemäß Poolbeschlüssen, auch wenn sie intern dagegen votierten; Aggregat nicht als unmittelbarer persönlicher Döpfner- oder Warburg-Aktienbesitz ausgeben"| N_ORG_DE_AXEL_SPRINGER
    N_ORG_DE_BRILLIANT_310_2006 -->|"Axel-Springer-Jahresbericht 2006 S. 115 dokumentiert Brilliant 310. GmbHs gemeldeten Erwerb von 680.000 Stückaktien am 13.07.2006 für 104,10 EUR je Aktie. Gesondert meldete der Emittent am 20.07.2006 Döpfners mittelbaren Erwerb von 680.000 Aktien zu 77 EUR; verschiedene gemeldete Rechtsvorgänge und Bewertungsgegenstände nicht ohne Transaktionsakten gleichsetzen oder Aktien zweimal addieren"| N_ORG_DE_AXEL_SPRINGER
    N_PER_DE_MATHIAS_DOEPFNER -->|"Axel-Springer-Jahresbericht 2006 S. 115 nennt Mathias Döpfner zugleich als Vorstandsvorsitzenden der Springer AG und Geschäftsführer von Brilliant 310. GmbH; historische Organrolle belegt nicht, dass er sämtliche Kaufpreis- oder Kreditbedingungen persönlich vereinbarte"| N_ORG_DE_BRILLIANT_310_2006
    N_ORG_US_WARBURG_PINCUS_1978["Warburg Pincus / E.M. Warburg & Co. (US-Investmenthaus, 1978)"]
    N_ORG_US_NVCA_1973["National Venture Capital Association (NVCA, 1973)"]
    N_ORG_US_WARBURG_PINCUS_1978 -->|"Warburg Pincus bezeichnet sich in der eigenen heutigen Firmengeschichte als Gründungsmitglied der National Venture Capital Association 1973. Diese Eigenangabe belegt keine individuelle Mitautorenschaft an der späteren US-ERISA-Regel von 1979"| N_ORG_US_NVCA_1973
    N_ORG_US_DOL_ERISA_1979["U.S. Department of Labor (ERISA-Pensionsaufsicht 1978–1979)"]
    N_ORG_US_WARBURG_PINCUS_1978 -->|"Warburg Pincus erklärt retrospektiv, 1978 Gespräche mit dem U.S. Department of Labor zur Öffnung von Pensionsanlagen für alternative Vermögensklassen mit angeführt zu haben. Das ist eine Firmen-Selbstaussage, keine unabhängig verifizierte Teilnehmerliste, Übernahme eines Wortlautentwurfs oder persönliche Bestechung"| N_ORG_US_DOL_ERISA_1979
    N_DOC_US_DOL_ERISA_PROPOSAL_1978["US-DOL-ERISA-Regelungsentwurf vom 25.04.1978 (43 FR 17480)"]
    N_ORG_US_DOL_ERISA_1979 -->|"Die DOL-Endbegründung im Federal Register 44 FR 37222 bestätigt die öffentliche Ankündigung des Regelungsentwurfs 29 CFR 2550.404a-1 am 25.04.1978 (43 FR 17480); namentliche Warburg-Pincus-Eingaben oder konkrete Entwurfsübernahmen daraus nicht gesichert"| N_DOC_US_DOL_ERISA_PROPOSAL_1978
    N_DOC_US_DOL_ERISA_RULE_1979["ERISA-Investment-Prudence-Verordnung 29 CFR 2550.404a-1 (1979)"]
    N_ORG_US_DOL_ERISA_1979 -->|"Das U.S. Department of Labor veröffentlichte am 26.06.1979 die finale ERISA-Treuhänder-Anlageauslegung unter 29 CFR 2550.404a-1, wirksam am 23.07.1979. Die Amtsbegründung berücksichtigt branchenweite Stellungnahmen, benennt Warburg Pincus aber nicht als alleinigen Urheber"| N_DOC_US_DOL_ERISA_RULE_1979
    N_PRG_US_ERISA_PENSION_PLANS_1979["ERISA-betroffene US-Pensionspläne (historisch 1979)"]
    N_DOC_US_DOL_ERISA_RULE_1979 -->|"Die am 23.07.1979 wirksame DOL-Regel bewertet Anlagesorgfalt im Kontext des gesamten Pensionsportfolios. Weder risikoreiche Unternehmensanteile noch alternative Anlagen sind allein wegen ihrer Anlageklasse per se unzulässig; dies ist KEINE generelle Erlaubnis beliebiger Private-Equity-Investments"| N_PRG_US_ERISA_PENSION_PLANS_1979
    N_DOC_US_FED_PRIVATE_EQUITY_1995["Federal Reserve Staff Study 168 – The Economics of the Private Equity Market (1995)"]
    N_ORG_US_FEDERAL_RESERVE -->|"Eine unter dem Dach des Federal Reserve System publizierte Staff Study 168 (Dezember 1995) analysiert Struktur und regulatorischen Wandel des Private-Equity-Markts. Die Autorenmeinungen sind keine automatische amtliche Billigung sämtlicher Schlussfolgerungen durch den Gouverneursrat"| N_DOC_US_FED_PRIVATE_EQUITY_1995
    N_ORG_US_VENTURE_CAPITAL_PARTNERSHIPS_1979["US-Venture-Capital-Partnerships (ERISA-Kapitalmarkt 1976–1979)"]
    N_PRG_US_ERISA_PENSION_PLANS_1979 -->|"Federal-Reserve-Staff-Studie 1995: VC-Partnerships erhielten von ERISA-Pensionsplänen 1976–1978 jeweils weniger als 5 Mio. USD jährlich, dagegen 50 Mio. USD im ERSTEN HALBJAHR 1979. Unterschiedliche Zeiträume, keine addierbaren Jahressummen und KEIN nachgewiesener individueller Geldfluss zu Warburg Pincus; DOL-Gegenregulierung folgte August 1979"| N_ORG_US_VENTURE_CAPITAL_PARTNERSHIPS_1979
    N_PER_US_JEFFREY_SACHS["Jeffrey D. Sachs"]
    N_ORG_PL_SOLIDARNOSC["Solidarność / Solidarity"]
    N_PER_US_JEFFREY_SACHS -->|"beriet 1989 Vertreter der Solidarność über das marktwirtschaftliche Reformprogramm"| N_ORG_PL_SOLIDARNOSC
    N_PER_US_DAVID_LIPTON["David Lipton"]
    N_PER_US_DAVID_LIPTON -->|"erarbeitete 1989 gemeinsam mit Sachs Reformvorschläge für Solidarność"| N_ORG_PL_SOLIDARNOSC
    N_PER_US_GEORGE_SOROS["George Soros"]
    N_ORG_PL_STEFAN_BATORY_FOUNDATION["Stefan Batory Foundation"]
    N_PER_US_GEORGE_SOROS -->|"gründete und unterstützte die polnische Stefan-Batory-Stiftung"| N_ORG_PL_STEFAN_BATORY_FOUNDATION
    N_ORG_PL_STEFAN_BATORY_FOUNDATION -->|"finanzierte 1989 Reisen/Arbeit des Sachs-Beraterteams in Polen; kein nachgewiesenes persönliches Honorar oder Weisungsverhältnis"| N_PER_US_JEFFREY_SACHS
    N_ORG_RU_YELTSIN_GOVERNMENT_1991_1994["Regierung Boris Jelzin (Russland, 1991–1994)"]
    N_PER_US_JEFFREY_SACHS -->|"wirtschaftspolitischer Berater der Jelzin-Regierung von Ende 1991 bis Ende 1993; Rücktritt Januar 1994 dokumentiert"| N_ORG_RU_YELTSIN_GOVERNMENT_1991_1994
    N_ORG_US_HIID["Harvard Institute for International Development (HIID)"]
    N_PER_US_JEFFREY_SACHS -->|"Direktor des HIID ab 1995, einschließlich der Schlussphase des USAID-Russlandprogramms; keine aus der Leitung allein folgende Schuld am Interessenkonfliktfall"| N_ORG_US_HIID
    N_ORG_US_USAID["U.S. Agency for International Development (USAID)"]
    N_ORG_US_USAID -->|"stellte für HIID-Russlandprogramme seit 1992 bis 1997 mehr als 40 Mio. USD bereit; von 300 Mio. USD unter HIID-Aufsicht getrennt halten"| N_ORG_US_HIID
    N_PRG_US_USAID_RUSSIA_AID_1992_1997["USAID-Russlandhilfeprogramme im HIID-Betreuungsportfolio (1992–1997)"]
    N_ORG_US_HIID -->|"beaufsichtigte laut GAO strategisch 300 Mio. USD US-Russlandhilfe bei relativ geringer USAID-Aufsicht; Portfolio, nicht Harvard-Einnahmen"| N_PRG_US_USAID_RUSSIA_AID_1992_1997
    N_PER_US_ANDREI_SHLEIFER["Andrei Shleifer"]
    N_PER_US_ANDREI_SHLEIFER -->|"leitete HIID-Russlandprogramm und wurde 1997 nach Konfliktregelverletzungen aus dem Programm entfernt"| N_ORG_US_HIID
    N_PER_US_JONATHAN_HAY["Jonathan Hay"]
    N_PER_US_JONATHAN_HAY -->|"leitete operative Programmteile in Moskau und wurde 1997 nach Konfliktregelverletzungen entfernt"| N_ORG_US_HIID
    N_ORG_INT_SDSN["UN Sustainable Development Solutions Network (SDSN)"]
    N_PER_US_JEFFREY_SACHS -->|"Präsident des Sustainable Development Solutions Network, laut SDSN-Website 2026"| N_ORG_INT_SDSN
    N_ORG_INT_UN_SECRETARIAT["UN-Generalsekretariat"]
    N_ORG_INT_UN_SECRETARIAT -->|"UN-Generalsekretär Ban Ki-moon lancierte 2012 das unabhängige SDSN; rechtlich kein UN-Organ"| N_ORG_INT_SDSN
    N_ORG_US_SDSN_ASSOCIATION["SDSN Association, Inc."]
    N_ORG_US_SDSN_ASSOCIATION -->|"eigenständiger US-501(c)(3)-Rechtsträger betreibt SDSN-Sekretariat"| N_ORG_INT_SDSN
    N_ORG_US_GATES_FOUNDATION["Gates Foundation"]
    N_ORG_US_GATES_FOUNDATION -->|"auf SDSN-Partnerseite 2026 als finanzieller Unterstützer gelistet; keine Höhe oder individuelle Zuwendung an Sachs ausgewiesen"| N_ORG_INT_SDSN
    N_ORG_US_BEZOS_EARTH_FUND["Bezos Earth Fund"]
    N_ORG_US_BEZOS_EARTH_FUND -->|"auf SDSN-Partnerseite 2026 als finanzieller Unterstützer gelistet; Betrag ungenannt"| N_ORG_INT_SDSN
    N_ORG_DE_BMWK_IKI["BMWK / Internationale Klimaschutzinitiative (IKI)"]
    N_ORG_DE_BMWK_IKI -->|"BMWK und IKI auf SDSN-Partnerseite als finanzielle Unterstützer gelistet, Abruf 2026; ohne belegte Einzelzahlung"| N_ORG_INT_SDSN
    N_ORG_INT_UNDP["United Nations Development Programme (UNDP)"]
    N_ORG_INT_UNDP -->|"UNDP auf SDSN-Partnerseite als finanzieller Unterstützer gelistet, Abruf 2026"| N_ORG_INT_SDSN
    N_ORG_US_COLUMBIA_CSD["Center for Sustainable Development, Columbia University"]
    N_PER_US_JEFFREY_SACHS -->|"Direktor des Center for Sustainable Development an der Columbia University laut aktueller SDSN-Biografie"| N_ORG_US_COLUMBIA_CSD
    N_ORG_INT_LANCET_COVID_COMMISSION["Lancet COVID-19 Commission"]
    N_PER_US_JEFFREY_SACHS -->|"Vorsitzender der Lancet-COVID-19-Kommission 2020–2022"| N_ORG_INT_LANCET_COVID_COMMISSION
    N_PER_US_PETER_DASZAK["Peter Daszak"]
    N_ORG_US_ECOHEALTH_ALLIANCE["EcoHealth Alliance"]
    N_PER_US_PETER_DASZAK -->|"leitete die EcoHealth Alliance; im Jahr 2021 durch Lancet-Taskforce-Interessenkonfliktdebatte relevant"| N_ORG_US_ECOHEALTH_ALLIANCE
```

[Zur Relationstabelle](network.md)
