# Netzwerkdiagramm

**805 Beziehungen** als grafische Gesamtübersicht. Die [alphabetische Relationstabelle](network.md) zeigt zusätzlich Evidenzstufen und Quellen.

## Direkte Verbindungen im Fokus

Diese Ausschnitte zeigen nur die unmittelbar dokumentierten Beziehungen des gewählten Akteurs. Weitere Beziehungen oder eine gemeinsame Steuerung sind daraus nicht automatisch ableitbar.

- [Atlantik-Brücke](network-focus-atlantik-bruecke.md) — 49 direkte Beziehungen
- [Bilderberg Meetings](network-focus-bilderberg.md) — 10 direkte Beziehungen
- [Organisation Gehlen](network-focus-organisation-gehlen.md) — 8 direkte Beziehungen
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
    N_ORG_INT_SHELL_GROUP_1996["Shell (Konzern und Deutschland-Niederlassung, Reisefinanzierung 1996)"]
    N_PER_DE_UDO_ULFKOTTE["Udo Ulfkotte (1960–2017)"]
    N_ORG_INT_SHELL_GROUP_1996 -->|"Shell organisierte und finanzierte nach zeitgenössischer taz-Recherche die Niger-Delta-Reise des FAZ-Korrespondenten Ulfkotte im Oktober 1996 einschließlich Hubschrauberflügen; dies belegt eine Zuwendung, nicht Bestechungsstraftat oder diktierte Berichterstattung"| N_PER_DE_UDO_ULFKOTTE
    N_ORG_INT_SHELL_GROUP_1996 -->|"Nach zeitgenössischer taz-Berichterstattung verwendete Shell Ulfkottes nach der 1996er Reise erschienenen FAZ-Artikel in einem firmeneigenen Werbevideo; daraus ist kein redaktioneller Auftrag und kein ausdrückliches FAZ-Einverständnis ableitbar"| N_ORG_DE_FAZ
    N_ORG_DE_BKA["Bundeskriminalamt (BKA)"]
    N_ORG_DE_BKA -->|"BKA lud Ulfkotte nach der Bundesregierung für eine einzelne ressortübergreifende Mykonos-Gefährdungslagebesprechung am 27.11.1996 als Experten für inneriranische Verhältnisse und ausdrücklich nicht als Pressevertreter ein; keine amtlich bestätigte Übergabe geheimer Verschlusssachen oder Agentenrolle"| N_PER_DE_UDO_ULFKOTTE
    N_ORG_DE_BMVG_PSV_1981_1990["Bundesministerium der Verteidigung (BMVg, Psychologische Verteidigung 1981–1990)"]
    N_ORG_DE_STUDIENGESELLSCHAFT_ZEITPROBLEME_1961_1990["Studiengesellschaft für Zeitprobleme e. V. (Bonn/Bad Godesberg)"]
    N_ORG_DE_BMVG_PSV_1981_1990 -->|"Bundesregierung nennt für 1981–1988 ca. eine Million DM jährlich aus BMVg-Mitteln an die Studiengesellschaft für Zeitprobleme; näherungsweiser Jahreswert, nicht exakt belegte acht Einzelzahlungen und kein BND-Rekrutierungsauftrag"| N_ORG_DE_STUDIENGESELLSCHAFT_ZEITPROBLEME_1961_1990
    N_ORG_DE_BMVG_PSV_1981_1990 -->|"Bundesregierung meldet 1.449.200 DM Gesamtzuwendungen an die Studiengesellschaft vom 01.01.1989 bis August 1990; ein Gesamtwert für 20 Monate und keine Einzeljahreszahlung oder Leistung an Ulfkotte"| N_ORG_DE_STUDIENGESELLSCHAFT_ZEITPROBLEME_1961_1990
    N_ORG_DE_DGFSB_1989_1990["Deutsche Gesellschaft für Sozialbeziehungen e. V. (Bonn, Förderzeitraum 1989–1990)"]
    N_ORG_DE_BMVG_PSV_1981_1990 -->|"Von den für 1989–1990 amtlich gemeldeten 515.171 DM Zuwendungen an sechs andere zivile Organisationen erhielt die Deutsche Gesellschaft für Sozialbeziehungen e. V. 385.000 DM; Studiengesellschaft in dieser Gesamtsumme ausdrücklich nicht enthalten"| N_ORG_DE_DGFSB_1989_1990
    N_PER_DE_WERNER_MARX_CDU_1965_1972["Werner Marx (1924–1985, CDU)"]
    N_PER_DE_WERNER_MARX_CDU_1965_1972 -->|"Werner Marx war laut institutioneller CDU-Biografie erster Vorsitzender der Studiengesellschaft 1965–1972 und zuvor im BMVg-Referat psychologische Kriegsführung tätig; keine persönliche Budgetweisung für Förderungen 1981–1990 nachgewiesen"| N_ORG_DE_STUDIENGESELLSCHAFT_ZEITPROBLEME_1961_1990
    N_PER_DE_UDO_ULFKOTTE -->|"Nur Ulfkottes retrospektive Eigenaussage (2014): Teilnahme an einem SfZ-Seminar am 25.02.1980 in Bonn-Bad Godesberg; keine unabhängig gesicherte Teilnehmerliste, BND-Anwerbung oder individuelle Spesenabrechnung"| N_ORG_DE_STUDIENGESELLSCHAFT_ZEITPROBLEME_1961_1990
    N_ORG_US_ARMY["United States Army"]
    N_ORG_US_PALANTIR_TECH["Palantir Technologies (Unternehmensgruppe)"]
    N_ORG_US_ARMY -->|"Army-OTA 06.03.2024 an Palantir: TITAN-Phase 3 über 178,4 Mio. USD für zehn Prototypen; Auftragswert, keine Auszahlung"| N_ORG_US_PALANTIR_TECH
    N_ORG_US_ARMY -->|"Army-Delivery-Order 31.08.2026 an Palantir über 127 Mio. USD als TITAN-Produktions-/Systemintegrationsauftrag; nicht als ausgezahlter Gewinn behandeln"| N_ORG_US_PALANTIR_TECH
    N_ORG_US_ANDURIL["Anduril Industries"]
    N_ORG_US_ARMY -->|"Army-Delivery-Order 31.08.2026 an Anduril über 65 Mio. USD für TITAN-Hardware-/Shelter-Integration; von Palantir 127 Mio. USD getrennt"| N_ORG_US_ANDURIL
    N_PRG_US_ARMY_TITAN["Tactical Intelligence Targeting Access Node (TITAN)"]
    N_ORG_US_PALANTIR_TECH -->|"Palantir soll laut Army bei der 2026er TITAN-Produktion federführend integrieren; Programmrolle, keine politische Weisung"| N_PRG_US_ARMY_TITAN
    N_ORG_US_ANDURIL -->|"Anduril liefert im TITAN-Produktionsauftrag 2026 insbesondere Hardware-/Shelter-Integration; Auftragssumme gesondert modelliert"| N_PRG_US_ARMY_TITAN
    N_ORG_US_ANDURIL -->|"US Army bestätigt Anduril-Lattice-/Palantir-Foundry-Zusammenarbeit für NGC2 Edge-to-Cloud Data Mesh; ohne ausgewiesene Einzelvergabe"| N_ORG_US_PALANTIR_TECH
    N_ORG_US_RAFT_TECH["Raft"]
    N_PRG_US_ARMY_NGC2["Next Generation Command and Control (NGC2)"]
    N_ORG_US_RAFT_TECH -->|"Army nennt Raft für NGC2 Datenregistrierung/-transformation/-föderation, ohne belegte Einzelvergütung"| N_PRG_US_ARMY_NGC2
    N_ORG_UA_MINDEF["Ministry of Defence of Ukraine"]
    N_ORG_UA_MINDEF -->|"Ukrainisches Verteidigungsministerium und Palantir starteten Brave1-Dataroom-Technologieprojekt mit realen Drohnen-/Gefechtsdaten; kein Projektbetrag genannt"| N_ORG_US_PALANTIR_TECH
    N_PRG_UA_BRAVE1_DATAROOM["Brave1 Dataroom"]
    N_PRG_UA_BRAVE1_DATAROOM -->|"Brave1 Dataroom nutzt Palantir-Software als Basis zum Training/Validieren militärischer KI; keine belegte Datenverkaufssumme"| N_ORG_US_PALANTIR_TECH
    N_ORG_US_ARMY_SETAF_AF["U.S. Army Southern European Task Force, Africa (SETAF-AF)"]
    N_ORG_US_ARMY_SETAF_AF -->|"Army SETAF-AF beschreibt 22.12.2025 offenes Experiment ihrer Public-Affairs-Stelle mit Palantirs Maven Smart System zur Lageauswertung/Narrativkommunikation; kein verdeckter Einfluss belegt"| N_ORG_US_PALANTIR_TECH
    N_ORG_US_PALANTIR_USG["Palantir USG Inc."]
    N_ORG_US_ARMY -->|"Army vergab 17.09.2026 48.094.071 USD Delivery Order an Palantir USG zur Modernisierung des Munitionsmanagements, getrennt von TITAN"| N_ORG_US_PALANTIR_USG
    N_ORG_US_ARMY -->|"USAspending W56KGY25F0090 ab 01.06.2025: Army Intelligence Data Platform AI-Platform-Lizenz, 1.166.666,69 USD obligated laut Register; keine Auszahlung"| N_ORG_US_PALANTIR_USG
    N_ORG_CL_CHRISTIAN_DEMOCRATS_1964["Partido Demócrata Cristiano de Chile (PDC)"]
    N_ORG_US_CIA -->|"CIA finanzierte 1964 verdeckt etwas mehr als die Hälfte des christdemokratischen Präsidentschaftswahlkampfes; Kandidat Frei sollte über Herkunft nicht informiert werden"| N_ORG_CL_CHRISTIAN_DEMOCRATS_1964
    N_PER_US_JOHN_A_MCCONE["John A. McCone"]
    N_PER_US_JOHN_A_MCCONE -->|"John McCone war 29.11.1961–28.04.1965 Director of Central Intelligence; ITT-Vorstandsbrief 1970 bestätigt frühere Leitungsfunktion"| N_ORG_US_CIA
    N_ORG_US_ITT_1970["International Telephone and Telegraph (ITT; 1970)"]
    N_PER_US_JOHN_A_MCCONE -->|"McCone war laut eigenem Brief 14.09.1970 ITT-Director und Mitglied des Executive Committee; Konzern- und Geheimdiensterfahrung hier persönlich verbunden"| N_ORG_US_ITT_1970
    N_ORG_US_CIA -->|"CIA gab 1970 ITT Hinweise auf sichere Kanäle der Anti-Allende-Wahlkampffinanzierung; angebotene 1 Mio. USD über CIA wurden explizit abgelehnt"| N_ORG_US_ITT_1970
    N_PRG_CL_ANTI_ALLENDE_1970["Anti-Allende-Wahlkampf Chile 1970"]
    N_ORG_US_ITT_1970 -->|"ITT leitete 1970 laut Church-Ausschuss mindestens 350.000 USD zur Anti-Allende-Kampagne; CIA beriet Übermittlung, nahm aber die angebotene 1-Mio.-CIA-Durchleitung nicht an"| N_PRG_CL_ANTI_ALLENDE_1970
    N_PRG_CL_CIA_TRACK_II_1970["CIA Track II: Chile 1970"]
    N_ORG_US_CIA -->|"Track II war CIA-seitig für militärische Lösung gegen Allendes Amtsantritt 1970 organisiert, unter Ausschluss von Botschafter und State; nicht Beweis direkter Führung des Putsches 1973"| N_PRG_CL_CIA_TRACK_II_1970
    N_ORG_CL_EL_MERCURIO_1971["El Mercurio (Chile)"]
    N_ORG_US_CIA -->|"CIA-Memo 10.04.1972: 700.000 USD für El Mercurio September 1971 bewilligt/ausgegeben, weitere 300.000 USD bis Januar 1972 bewilligt/ausgegeben; zusätzliche 1972er Bewilligung kein Zahlungsbeleg"| N_ORG_CL_EL_MERCURIO_1971
    N_ORG_CL_MILITARY_JUNTA_1973["Chilenische Militärjunta ab September 1973"]
    N_ORG_US_CIA -->|"Church-Ausschuss dokumentiert nach Putsch 1973 fortgeführtes CIA-Propagandaprogramm zugunsten des Junta-Ansehens; kein direkter Putschbefehl dadurch erwiesen"| N_ORG_CL_MILITARY_JUNTA_1973
    N_PRG_GT_CIA_PBSUCCESS_1954["Operation PBSUCCESS: Guatemala 1954"]
    N_ORG_US_CIA -->|"Operation PBSUCCESS als CIA-geführte verdeckte US-Intervention gegen Regierung Árbenz in Guatemala 1954 offiziell in FRUS dokumentiert"| N_PRG_GT_CIA_PBSUCCESS_1954
    N_ORG_US_UNITED_FRUIT_1952["United Fruit Company (1952)"]
    N_ORG_GT_CASTILLO_ARMAS_GROUP["Gruppe um Carlos Castillo Armas (1952)"]
    N_ORG_US_UNITED_FRUIT_1952 -->|"FRUS-Editorial Note: United Fruit gehörte 1952 zur finanziellen Unterstützergruppe potentieller Rebellen um Castillo Armas; Summe, Überweisungsweg und CIA-Direktzahlung ungeklärt"| N_ORG_GT_CASTILLO_ARMAS_GROUP
    N_ORG_DE_BND -->|"Das Grünen-Sondervotum in BT-Drs 16/13400, S. 963, referiert einen BND-Pressestellenvermerk an den BND-Präsidenten vom 10.11.1997 über den Journalisten Ulfkotte und angeblich bei ihm vorhandene BND-Dokumente (MAT A 374/1, Ordner 42, Bl. 183–186); kein eigener BND-Aktenvolltext oder Beleg der tatsächlichen Aktenübergabe eingesehen"| N_PER_DE_UDO_ULFKOTTE
    N_ORG_DE_ANNETTE_BARTHELT_STIFTUNG["Annette Barthelt-Stiftung e. V."]
    N_ORG_DE_ANNETTE_BARTHELT_STIFTUNG -->|"Annette Barthelt-Stiftung dokumentiert Verleihung ihres staatsbürgerlichen Preises an Udo Ulfkotte am 12.12.2003 im Presse-Club Bonn; unizeit nannte eine angekündigte Dotierung von 6.000 EUR, aber eine individuelle Auszahlung ist nicht geprüft"| N_PER_DE_UDO_ULFKOTTE
    N_PER_DE_GUENTHER_BECKSTEIN["Günther Beckstein"]
    N_PER_DE_GUENTHER_BECKSTEIN -->|"Der damalige bayerische Innenminister Günther Beckstein hielt laut eigener Preisträgerchronik der Annette Barthelt-Stiftung die Laudatio auf Udo Ulfkotte bei der Preisverleihung am 12.12.2003; dokumentierte öffentliche Anerkennung, keine belegte Weisung an journalistische Veröffentlichungen"| N_PER_DE_UDO_ULFKOTTE
    N_ORG_DE_NETZWERK_RECHERCHE_2005["Netzwerk Recherche (Konferenzveranstalter 2005)"]
    N_PRG_DE_NR_INTELLIGENCE_MEDIA_PANEL_2005["Netzwerk Recherche Forum 5: Zwischen Wahrheit und Abhängigkeit (04.06.2005)"]
    N_ORG_DE_NETZWERK_RECHERCHE_2005 -->|"Netzwerk Recherche organisierte die öffentlich angekündigte Jahrestagungsdiskussion 'Zwischen Wahrheit und Abhängigkeit – Zur Kooperation von Geheimdiensten und Journalisten' beim NDR Hamburg am 04.06.2005, Forum 5 (15:45–17:00); keine institutionelle BND-Weisung oder Finanzierung aus Programm ableitbar"| N_PRG_DE_NR_INTELLIGENCE_MEDIA_PANEL_2005
    N_PER_DE_UDO_ULFKOTTE -->|"Originalprogramm führt Udo Ulfkotte als Teilnehmer des öffentlichen Geheimdienste-und-Journalisten-Panels am 04.06.2005; message 1/2006 berichtet rückblickend über ein Instrumentalisierungseingeständnis Ulfkottes auf jener Jahrestagung, aber kein Tonmitschnitt und keine Lokalisierung des Zitats gerade in Forum 5 gesichtet"| N_PRG_DE_NR_INTELLIGENCE_MEDIA_PANEL_2005
    N_PER_DE_ERNST_UHRLAU["Ernst Uhrlau"]
    N_PER_DE_ERNST_UHRLAU -->|"Originalprogramm 2005 listet Ernst Uhrlau für dasselbe öffentlich angekündigte Forum 5 als damaligen Nachrichtendienstkoordinator im Kanzleramt, nicht als 2005 bereits amtierenden BND-Präsidenten; tatsächliche Anwesenheit und ein persönlicher Kontakt zu Ulfkotte ohne Mitschnitt hier nicht eigenständig gesichert"| N_PRG_DE_NR_INTELLIGENCE_MEDIA_PANEL_2005
    N_PER_US_THOMAS_CORCORAN_UFCO_1954["Thomas G. Corcoran (United-Fruit-Verbindung 1954)"]
    N_PER_US_THOMAS_CORCORAN_UFCO_1954 -->|"Thomas Corcoran trat am 22.07.1954 gemeinsam mit Joe Montgomery in einem vertraulichen CIA-Gespräch als United-Fruit-Vertreter auf; kein nachgewiesenes Anstellungsverhältnis oder CIA-Operativbefehl"| N_ORG_US_UNITED_FRUIT_1952
    N_PER_US_JOE_MONTGOMERY_UFCO_1954["Joe Montgomery (United Fruit 1954)"]
    N_PER_US_JOE_MONTGOMERY_UFCO_1954 -->|"Joe Montgomery sprach laut dem CIA-Protokoll vom 22.07.1954 persönlich für die United Fruit Company; die berichtete Einflussnahme auf einen Polizeichef ist nicht unabhängig bestätigt"| N_ORG_US_UNITED_FRUIT_1952
    N_ORG_US_CIA -->|"CIA-Western-Hemisphere-Chef J. C. King protokollierte am 22.07.1954 vertrauliche Gespräche mit United-Fruit-Vertretern Montgomery/Corcoran zu Politik, Personalfragen und US-Kartellklage; keine Unternehmensleitung der CIA belegt"| N_ORG_US_UNITED_FRUIT_1952
    N_PER_US_THOMAS_CORCORAN_UFCO_1954 -->|"CIA-interne Sitzungsnotiz vom 09.06.1954 beschreibt Corcorans Versuche, Informationen zu PBSUCCESS zu erhalten und politischen Druck auszuüben; CIA wies Kontakte ohne DCI-Genehmigung zurück, tatsächlicher Erfolg nicht belegt"| N_ORG_US_CIA
    N_ORG_US_DOJ -->|"US-DOJ reichte am 02.07.1954 tatsächlich Zivilkartellklage gegen United Fruit ein; am 04.02.1958 folgte ein Consent Judgment mit Wettbewerbs-/Entflechtungsauflagen ohne Prozess oder Schuldanerkenntnis, 1978 modifiziert"| N_ORG_US_UNITED_FRUIT_1952
    N_PRG_GT_CIA_SHERWOOD_1954["CIA-gesteuerte Radiostruktur SHERWOOD (Guatemala 1954)"]
    N_ORG_US_CIA -->|"CIA-Planungsdepesche 04.06.1954 ordnet SHERWOOD zu CIA-kontrollierten Medien; Telegramm 27.06.1954 empfiehlt bestimmte UFCO-Bezüge für SHERWOOD; keine generelle Aussage über Ausstrahlung jedes Plans"| N_PRG_GT_CIA_SHERWOOD_1954
    N_PRG_GT_CIA_SHERWOOD_1954 -->|"CIA-Zentrale empfahl 27.06.1954, SHERWOOD solle United Fruit ausdrücklich kritisch darstellen, damit Castillo Armas nicht als Mann des Konzerns gelte. Weist Kommunikationsabsicht nach, nicht tatsächlich erfolgte Sendung"| N_ORG_US_UNITED_FRUIT_1952
    N_PER_US_ROBERT_CUTLER_1953["Robert Cutler (NSC-Sicherheitsberater 1953)"]
    N_ORG_US_OLD_COLONY_TRUST_1953["Old Colony Trust Company (1953)"]
    N_PER_US_ROBERT_CUTLER_1953 -->|"NSC-Protokoll vom 04.06.1953 bezeichnet Robert Cutler als ehemaligen Präsidenten der Old Colony Trust Company; eine konkrete Weisung oder Zahlung im UFCO-Kartellverfahren wird nicht behauptet"| N_ORG_US_OLD_COLONY_TRUST_1953
    N_ORG_US_OLD_COLONY_TRUST_1953 -->|"NSC-Protokoll vom 04.06.1953 benennt Verbindungen Old Colony Trust–United Fruit als Grund für Cutlers Selbstenthaltung; Art, Kapitalanteile und Finanzflüsse sind in der Akte nicht spezifiziert"| N_ORG_US_UNITED_FRUIT_1952
    N_ORG_US_NSC_1953["National Security Council (USA, 1953–1954)"]
    N_ORG_US_NSC_1953 -->|"National Security Council beschloss am 04.06.1953 einjährige Verschiebung der vorbereiteten United-Fruit-Kartellklage mit Auftrag an den Attorney General zur Verhandlung; Präsidentengenehmigung ist ediert"| N_ORG_US_DOJ
    N_ORG_US_STATE_DEPARTMENT_1954["U.S. Department of State (1954)"]
    N_ORG_US_UNITED_FRUIT_1952 -->|"State-Memorandum vom 03.12.1954 beschreibt wiederholte United-Fruit-Bitten um diplomatische Einflussnahme zunächst gegen Klage, dann für günstige Einigung; eine tatsächliche DOJ-Weisung oder erreichte Wirkung ist nicht nachgewiesen"| N_ORG_US_STATE_DEPARTMENT_1954
    N_ORG_US_USAID_CHILE_1967["U.S. Agency for International Development (politische Risikoversicherung Chile, 1967)"]
    N_ORG_US_USAID_CHILE_1967 -->|"CRS-House-Bericht 1973: AID versicherte Ende 1967 u.a. ITT-Risiken in Chile; 0,9 Mrd. USD sind länderweites Quartalsvolumen und keine ITT-Einzelsumme"| N_ORG_US_ITT_1970
    N_ORG_US_OPIC_1971["Overseas Private Investment Corporation (OPIC, USA)"]
    N_ORG_US_USAID_CHILE_1967 -->|"DFC-Nachfolgeregister: AID verwaltete staatliche Risikoversicherung bis OPIC 1971 den Betrieb aufnahm; institutionelle Nachfolge, keine ITT-Einzelzahlung"| N_ORG_US_OPIC_1971
    N_ORG_US_OPIC_1971 -->|"OPIC Board lehnte am 09.04.1973 eine rund 92,5 Mio. USD ITT-Forderung mit behaupteten Vertragsverletzungen ab; streitiger Vorwurf, kein gerichtliches Schuldurteil"| N_ORG_US_ITT_1970
    N_ORG_US_OPIC_1971 -->|"OPIC-Anwalt erklärte im US-Kongress 1976, ein einstimmiges dreiköpfiges Schiedsgericht habe zugunsten ITTs OPIC-Haftung festgestellt; vollständiger Schiedsspruch noch nicht eingesehen"| N_ORG_US_ITT_1970
    N_ORG_US_OPIC_1971 -->|"DFC-FY75-Register: 34.706.917 USD Cash als Teil der ITT-Versicherungsregelung zu Chile; keine Zahlung der zusätzlich garantierten Schuldverschreibungen zu unterstellen"| N_ORG_US_ITT_1970
    N_ORG_US_OPIC_1971 -->|"DFC-FY75-Register: 59.384.614 USD OPIC-Garantie chilenischer Regierungsverpflichtungen im ITT-Vergleich, nicht als sofortige Barzahlung; FRUS-Fußnote nennt abweichend 59.384.697 USD"| N_ORG_US_ITT_1970
    N_ORG_INT_PARIS_CLUB_CHILE_1972["Pariser Club: Gläubigerverhandlungen mit Chile (1972–1975)"]
    N_ORG_CL_ALLENDE_GOVERNMENT_1972["Regierung Salvador Allende (Chile, 1970–1973)"]
    N_ORG_INT_PARIS_CLUB_CHILE_1972 -->|"UNTS 967: Pariser Gläubiger mit Chile am 19.04.1972 Grundsatz zur Konsolidierung von 70% bestimmter Fälligkeiten vereinbart, Bilateralverträge nötig; kein 70%-Schuldenerlass."| N_ORG_CL_ALLENDE_GOVERNMENT_1972
    N_ORG_DE_FRG_CREDITOR_GOVERNMENT_1972_1975["Bundesrepublik Deutschland als Gläubigerstaat Chiles (1972–1975)"]
    N_ORG_DE_FRG_CREDITOR_GOVERNMENT_1972_1975 -->|"Bundesrepublik Deutschland war 1972 und 1974 Gläubigerstaat in multilateralen Verhandlungen zur chilenischen Umschuldung, laut UNTS-Verträgen; keine Weisung an US-Dienststellen daraus ableitbar."| N_ORG_INT_PARIS_CLUB_CHILE_1972
    N_ORG_INT_PARIS_CLUB_CHILE_1972 -->|"Pariser Abkommen 25.03.1974 sah für ausgewählte 1973/74 fällige chilenische Verpflichtungen 80% Umschuldung und IMF-Stand-by-Bedingung vor, nicht pauschalen Schuldenerlass."| N_ORG_CL_MILITARY_JUNTA_1973
    N_ORG_INT_PARIS_CLUB_CHILE_1972 -->|"Laut Kissinger-Memo 28.04.1972 fragten Pariser Gläubiger die chilenische Delegation ausdrücklich, ob ITT unter Entschädigungsregeln falle; keine belegte ITT-Weisung und kein Kausalbeweis für Umschuldungsbeginn."| N_ORG_CL_ALLENDE_GOVERNMENT_1972
    N_ORG_US_BANK_OF_AMERICA_1974["Bank of America (Chile-Kredite und Versicherungsfälle 1970–1978)"]
    N_ORG_CL_PETROQUIMICA_DOW_1974["Petroquímica Dow S.A. (Chile, 1974)"]
    N_ORG_US_BANK_OF_AMERICA_1974 -->|"UNTS 967 Nr. 13947 §8-9 nennt Bank-of-America-Darlehensverträge mit Petroquímica Dow S.A.; betroffene Fälligkeiten 1971–1972 und OPIC-Bezug, keine Eigentumskontrolle nachgewiesen."| N_ORG_CL_PETROQUIMICA_DOW_1974
    N_ORG_CL_INDUSTRIAS_ARAUCO_1974["Industrias de Celulosa Arauco S.A. (Chile, 1974)"]
    N_ORG_US_BANK_OF_AMERICA_1974 -->|"UNTS 967 Nr. 13947 §8-9 nennt Bank-of-America-Darlehensverträge mit Industrias de Celulosa Arauco S.A.; keine Einzelkreditsumme oder spätere Ownership aus diesem Text belegt."| N_ORG_CL_INDUSTRIAS_ARAUCO_1974
    N_ORG_US_OPIC_1971 -->|"US–Chile-Memorandum 17.06.1974 §8–9: OPIC-Zahlung bezüglich Bank-of-America-Industriekrediten für etwa 30.06.1974 vorgesehen; keine verifizierte fristgerechte Auszahlung."| N_ORG_US_BANK_OF_AMERICA_1974
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"UNTS 967 Nr. 13947 §10: Chile erklärte bereits 15.05.1974 1.226.443,63 USD an OPIC überwiesen; separat von ITT FY1975; Vertrag druckt Gesamtbetrag 1 USD unter Summe der Einzelpositionen."| N_ORG_US_OPIC_1971
    N_ORG_US_EXIMBANK_1974["Export–Import Bank of the United States (Chile, 1974)"]
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"US–Chile-Schuldenvertrag 17.06.1974 §10 nennt 12 Mio. USD bereits 15.05.1974 an US Export–Import Bank gezahlt; von OPIC-Zahlung und anderen Kategorien getrennt."| N_ORG_US_EXIMBANK_1974
    N_ORG_US_COMMERCIAL_BANKS_CHILE_1975["US-Geschäftsbanken als berichtete Kreditgeber Chiles (1975)"]
    N_ORG_US_COMMERCIAL_BANKS_CHILE_1975 -->|"US-Botschaft Santiago 04.04.1975 referiert Minister Saez: nicht namentlich genannte US-Banken hielten neue Kurzfristkredite bis Pariser-Club-Vereinbarung zurück; keine individuelle Bankweisung geprüft."| N_ORG_CL_MILITARY_JUNTA_1973
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"US-Botschaft Bonn 06.05.1975: Chilenische Botschaft übergab am 02.05.1975 deutschem Ministerialbeamten Müller-Thuns Forderungs-/Zahlungsplanliste u.a. ITT und OPIC; Anlage liegt nicht vor."| N_ORG_DE_FRG_CREDITOR_GOVERNMENT_1972_1975
    N_PER_INT_BERGE_BALANIAN["Berge Aris Balanian"]
    N_ORG_DE_BND -->|"Neun amtlich bestätigte Gespräche ab September 1992; formeller Quellenstatus offen"| N_PER_INT_BERGE_BALANIAN
    N_ORG_US_STATE_DEPARTMENT["US Department of State"]
    N_ORG_US_STATE_DEPARTMENT -->|"Sanktionsbescheid wirksam ab 09.02.1998; kein Strafurteil"| N_PER_INT_BERGE_BALANIAN
    N_PER_DE_HANS_JOACHIM_ROSE["Hans-Joachim Rose"]
    N_ORG_US_STATE_DEPARTMENT -->|"Adressat der Public Notice 2614; wirksam ab 25.09.1997"| N_PER_DE_HANS_JOACHIM_ROSE
    N_ORG_DE_ROSE_IMPORT_EXPORT["Rose Import-Export GmbH"]
    N_ORG_US_STATE_DEPARTMENT -->|"Weiterer Adressat derselben Public Notice 2614; wirksam ab 25.09.1997"| N_ORG_DE_ROSE_IMPORT_EXPORT
    N_PER_US_SUZANNE_WOOLSEY["Suzanne H. Woolsey"]
    N_PER_US_SUZANNE_WOOLSEY -->|"GMF-Kuratorium 1992–2000"| N_ORG_US_GMF_2012
    N_PER_US_SUZANNE_WOOLSEY -->|"GMF-Kuratorium 2002–2010"| N_ORG_US_GMF_2012
    N_ORG_US_FLUOR["Fluor Corporation"]
    N_PER_US_SUZANNE_WOOLSEY -->|"Verwaltungsratsmandat 2004–2014"| N_ORG_US_FLUOR
    N_ORG_US_IDA["Institute for Defense Analyses"]
    N_PER_US_SUZANNE_WOOLSEY -->|"IDA-Mandat in SEC-Offenlegung 2005"| N_ORG_US_IDA
    N_ORG_US_RMI["Rocky Mountain Institute"]
    N_PER_US_SUZANNE_WOOLSEY -->|"RMI-Mandat in SEC-Offenlegung 2005"| N_ORG_US_RMI
    N_PER_US_JAMES_WOOLSEY["R. James Woolsey"]
    N_PER_US_SUZANNE_WOOLSEY -->|"Öffentlich dokumentiertes Eheverhältnis, Stand 2004"| N_PER_US_JAMES_WOOLSEY
    N_PER_DE_KLAUS_DIETER_FRANKENBERGER -->|"Teilnehmer Brussels Forum 2007 (FAZ)"| N_ORG_US_GMF_2012
    N_PRG_US_GMF_MARSHALL_MEMORIAL["Marshall Memorial Fellowship"]
    N_ORG_US_GMF_2012 -->|"Betreibt Austauschprogramm Marshall Memorial Fellowship"| N_PRG_US_GMF_MARSHALL_MEMORIAL
    N_PRG_US_GMF_JOURNALISM["GMF Journalism Fellowship"]
    N_ORG_US_GMF_2012 -->|"Journalism Fellowship seit 1999, getrennt vom MMF"| N_PRG_US_GMF_JOURNALISM
    N_ORG_US_NATIONAL_FORUM_FOUNDATION["National Forum Foundation"]
    N_ORG_US_GMF_2012 -->|"In externer Programminventur 1990 genannte Förderung; keine Zahlungsabrechnung"| N_ORG_US_NATIONAL_FORUM_FOUNDATION
    N_PER_IR_ALI_FALLAHIAN["Ali Fallahian"]
    N_PER_DE_BERND_SCHMIDBAUER["Bernd Schmidbauer"]
    N_PER_IR_ALI_FALLAHIAN -->|"Eingeräumte Forderung zur Einflussnahme auf Mykonos-Verfahren 1993; laut Schmidbauer sofort zurückgewiesen"| N_PER_DE_BERND_SCHMIDBAUER
    N_ORG_DE_BUNDESKANZLERAMT["Bundeskanzleramt"]
    N_DOC_DE_MYKONOS_ERMITTLUNG_1992["Sperrerklärung im Mykonos-Ermittlungsverfahren (04.12.1992)"]
    N_ORG_DE_BUNDESKANZLERAMT -->|"Sperrerklärung 04.12.1992 und ersetztes BND-Schreiben; keine belegte Verbindung zum späteren Fallahian-Treffen"| N_DOC_DE_MYKONOS_ERMITTLUNG_1992
    N_ORG_DE_THYSSENKRUPP["ThyssenKrupp AG"]
    N_ORG_DE_THYSSENKRUPP -->|"Vom DRPR dokumentierte Einladung von Medienvertretern zu firmenfinanzierten Pressereisen; keine redaktionelle Weisung belegt"| N_ORG_DE_FAZ
    N_ORG_DE_THYSSENKRUPP -->|"Vom DRPR dokumentierte Einladung von Medienvertretern zu firmenfinanzierten Pressereisen; keine redaktionelle Weisung belegt"| N_ORG_DE_SUEDDEUTSCHE_ZEITUNG
    N_ORG_DE_TAGESSPIEGEL["Der Tagesspiegel"]
    N_ORG_DE_THYSSENKRUPP -->|"Vom DRPR dokumentierte Einladung von Medienvertretern zu firmenfinanzierten Pressereisen; keine redaktionelle Weisung belegt"| N_ORG_DE_TAGESSPIEGEL
    N_ORG_DE_RHEINISCHE_POST["Rheinische Post"]
    N_ORG_DE_THYSSENKRUPP -->|"Vom DRPR dokumentierte Einladung von Medienvertretern zu firmenfinanzierten Pressereisen; keine redaktionelle Weisung belegt"| N_ORG_DE_RHEINISCHE_POST
    N_ORG_DE_NRZ["Neue Ruhr / Neue Rhein Zeitung"]
    N_ORG_DE_THYSSENKRUPP -->|"Vom DRPR dokumentierte Einladung von Medienvertretern zu firmenfinanzierten Pressereisen; keine redaktionelle Weisung belegt"| N_ORG_DE_NRZ
    N_ORG_DE_DRPR["Deutscher Rat für Public Relations"]
    N_ORG_DE_DRPR -->|"Ermahnung wegen unverhältnismäßiger Pressereisen; ausdrücklich keine formelle Rüge"| N_ORG_DE_THYSSENKRUPP
    N_PER_DE_JUERGEN_CLAASSEN["Jürgen Claassen"]
    N_PER_DE_JUERGEN_CLAASSEN -->|"Vorstandsmitglied 21.01.2011–31.12.2012; Geschäftsbericht 2011/12 nennt Recht, Compliance, Kommunikation und Politik im selben Ressort"| N_ORG_DE_THYSSENKRUPP
    N_PER_DE_ALEXANDER_WILKE["Alexander Wilke"]
    N_PER_DE_ALEXANDER_WILKE -->|"Kommunikationsverantwortung und Aufarbeitung gegenüber DRPR"| N_ORG_DE_THYSSENKRUPP
    N_ORG_DE_PARK_AVENUE["Park Avenue (Gruner + Jahr)"]
    N_PER_DE_UDO_ULFKOTTE -->|"Zeitgenössisch als Chefreporter bezeichnet; Ausscheiden bis 30.06.2006 berichtet"| N_ORG_DE_PARK_AVENUE
    N_ORG_DE_GRUNER_JAHR["Gruner + Jahr (historischer Verlag)"]
    N_ORG_DE_GRUNER_JAHR -->|"Verlag zur Testausgabe Juni und zum regulären Start Oktober 2005"| N_ORG_DE_PARK_AVENUE
    N_PER_DE_HOLGER_CHRISTMANN["Holger Christmann"]
    N_PER_DE_HOLGER_CHRISTMANN -->|"Von zeitgenössischem Branchenbericht als berufliche Vermittlung zum Magazin Park Avenue beschrieben; kein Geheimdienstbezug belegt"| N_PER_DE_UDO_ULFKOTTE
    N_ORG_US_ANACONDA_COPPER_1972["Anaconda Company (Chile-Kupferbeteiligungen 1972–1977)"]
    N_ORG_US_OPIC_1971 -->|"GAO 1976: OPIC wies September 1972 zwei Anaconda/Chile-Copper-Enteignungsforderungen zusammen ca. 154 Mio USD wegen streitiger Policendeckung zurück; keine akzeptierte Leistung."| N_ORG_US_ANACONDA_COPPER_1972
    N_ORG_CL_CHILE_COPPER_ANACONDA_1972["Chile Copper Company (Anaconda-Tochter, 1972)"]
    N_ORG_US_ANACONDA_COPPER_1972 -->|"GAO-Bilanzbericht benennt Chile Copper Company ausdrücklich als Tochter der Anaconda Company in 1972er gemeinsamen OPIC-Versicherungsforderungen."| N_ORG_CL_CHILE_COPPER_ANACONDA_1972
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"GAO 1976: Chile vereinbarte Juli 1974 mit Anaconda ca. 65 Mio USD Cash und chilenische Schuldscheine Nominalwert 188 Mio USD; nicht mit OPIC-1977-Abwicklung addieren."| N_ORG_US_ANACONDA_COPPER_1972
    N_ORG_US_OPIC_1971 -->|"Dreierschiedsgericht 17.07.1975 bejahte laut US-GAO und Gericht OPIC-Haftung gegenüber Anaconda, bestimmte jedoch noch keinen Zahlbetrag; Ablehnung von 1972 nicht Endstand."| N_ORG_US_ANACONDA_COPPER_1972
    N_ORG_US_DISTRICT_COURT_DC_1976["U.S. District Court for the District of Columbia (Anaconda-Urteil 1976)"]
    N_ORG_US_DISTRICT_COURT_DC_1976 -->|"418 F. Supp. 107 vom 20.07.1976: Gericht wies OPIC-Antrag zur Aufhebung des Anaconda-Schiedsspruchs wegen behaupteter Befangenheit ab; kein Korruptionsbefund gegen Anaconda."| N_ORG_US_OPIC_1971
    N_ORG_US_OPIC_1971 -->|"GAO-Bilanz zum 30.06.1975: 128.659.383 USD Chile-bezogene Eventualgarantien auf von Chile übernommene Entschädigungs-/Schuldverpflichtungen; einschliesslich Zinsen, keine Barauszahlung."| N_ORG_CL_MILITARY_JUNTA_1973
    N_ORG_US_OPIC_1971 -->|"GAO 1977 und DFC FY77: OPIC-Anaconda-Vergleich 31.03.1977, Cashanteil exakt 47.504.034 USD; OPIC erhielt zudem laut GAO ca. 27,5 Mio USD Chile-Notes als Gegenwert, keine Nettoverlustbehauptung."| N_ORG_US_ANACONDA_COPPER_1972
    N_ORG_US_OPIC_1971 -->|"DFC FY77: 47.588.104 USD Garantieanteil von insgesamt 95.092.138 USD im Anaconda-Vergleich; Eventualhaftung auf Chile-Notes, keine sofortige Barauszahlung."| N_ORG_US_ANACONDA_COPPER_1972
    N_ORG_US_OPIC_1971 -->|"DFC FY78: Bank of America/Petrodow II, Chile, Versicherungsart A Unkonvertierbarkeit, exakt 868.642 USD Garantie, 0 USD Cash. Keine Datierung auf im UN-Vertrag geplante Zahlung Juni 1974."| N_ORG_US_BANK_OF_AMERICA_1974
    N_ORG_US_OPIC_1971 -->|"DFC FY78: Bank of America/Arauco III, Chile, Versicherungsart A Unkonvertierbarkeit, exakt 4.397.727 USD Garantie, 0 USD Cash; Kreditprojekt laut UNTS 1974 namentlich zuordenbar, Policenidentität offen."| N_ORG_US_BANK_OF_AMERICA_1974
    N_ORG_INT_OVERSEAS_INVESTMENT_INSURANCE_GROUP_1975["Overseas Investment Insurance Group (OPIC-Mitversicherer 1975)"]
    N_ORG_US_OPIC_1971 -->|"GAO ID-77-24: private Unternehmen in OIIG traten seit 01.01.1975 als Mitversicherer neu ausgestellter OPIC-Policen und als Rückversicherer älterer Verträge auf; keine konkrete Chile-Payout-Zuordnung."| N_ORG_INT_OVERSEAS_INVESTMENT_INSURANCE_GROUP_1975
    N_ORG_GB_LLOYDS_LONDON_1976["Lloyd's of London (OPIC-Rückversicherung 1976)"]
    N_ORG_US_OPIC_1971 -->|"US-GAO ID-77-24 Druckseite 8: OPIC unterhielt 1976 eigenen Rückversicherungsvertrag mit Lloyd's of London, getrennt von OIIG; keine bewiesene Zahlung an Anaconda, ITT oder BoFA."| N_ORG_GB_LLOYDS_LONDON_1976
    N_ORG_DE_THYSSENKRUPP -->|"Geschäftsbericht 2012/13 weist vertraglichen Ausgleich von 3.754.000 EUR aus; keine nachgewiesene unzulässige Gegenleistung"| N_PER_DE_JUERGEN_CLAASSEN
    N_ORG_DE_KPMG_AG["KPMG AG Wirtschaftsprüfungsgesellschaft"]
    N_ORG_DE_THYSSENKRUPP -->|"Vorstandsauftrag zur CMS-Prüfung 2011; Wirksamkeitszeitraum April–September, begrenzter Prüfungsumfang"| N_ORG_DE_KPMG_AG
    N_ORG_DE_BDO_AG["BDO AG Wirtschaftsprüfungsgesellschaft"]
    N_ORG_DE_THYSSENKRUPP -->|"Freiwillige Sonderprüfung 2013: Weiterentwicklung des internen Kontrollsystems, Prüfungsgegenstand 1"| N_ORG_DE_BDO_AG
    N_PER_DE_HANS_JOACHIM_BOECKING["Hans-Joachim Böcking"]
    N_ORG_DE_THYSSENKRUPP -->|"Freiwillige Sonderprüfung 2013: KPMG-Empfehlungen, Investitionscontrolling und Informationswege, Prüfungsgegenstände 2–4"| N_PER_DE_HANS_JOACHIM_BOECKING
    N_ORG_DE_DSW["Deutsche Schutzvereinigung für Wertpapierbesitz e.V."]
    N_ORG_DE_THYSSENKRUPP -->|"Vereinbarung zur freiwilligen Sonderprüfung vom 16.07.2013, nach zuvor abgelehntem Antrag laut Unternehmen"| N_ORG_DE_DSW
    N_PER_DE_CHRISTIAN_STRENGER["Christian Strenger"]
    N_ORG_DE_THYSSENKRUPP -->|"Aktionär als Mitvereinbarungspartner der freiwilligen Sonderprüfung vom 16.07.2013"| N_PER_DE_CHRISTIAN_STRENGER
    N_ORG_US_FEDERAL_FINANCING_BANK_1973["Federal Financing Bank (FFB)"]
    N_ORG_US_OPIC_1971 -->|"FY1977 ca. 36 Mio. USD Zahlungen auf direkte Schadenverbindlichkeiten über Verkauf chilenischer Schuldverschreibungen mit Rückgriff finanziert; keine Zuordnung zu einzelnen Konzernfällen."| N_ORG_US_FEDERAL_FINANCING_BANK_1973
    N_ORG_US_TREASURY -->|"Treasury beaufsichtigte die staatseigene FFB und finanzierte sie nach anfänglicher öffentlicher Finanzierung über Treasury-Kredite; Jahresbericht FY1977 S. 33–35."| N_ORG_US_FEDERAL_FINANCING_BANK_1973
    N_ORG_US_OPIC_1971 -->|"Chile-bezogene OPIC-Eventualgarantien zum 30.09.1977 190,778 Mio. USD und zum 30.09.1978 166,624 Mio. USD; Bestände, keine addierbaren Zahlungen."| N_ORG_CL_MILITARY_JUNTA_1973
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"Forderungen OPIC gegen Chile: 1977 Kapital 130,349 Mio./Zinsen 41,716 Mio.; 1978 Kapital 74,836 Mio./Zinsen 24,197 Mio. USD. Bis Berichtszeitpunkt fällige neu vereinbarte Raten geleistet; keine vollständige Tilgung belegt."| N_ORG_US_OPIC_1971
    N_ORG_GB_LLOYDS_LONDON_1976 -->|"GAO-Aussage 08.09.1977: Lloyd's 12,5 % am Gruppenportfolio, OPIC 74,5 %, übrige private Beteiligung 13 %; individuelle Chile-Policenzuordnung offen."| N_ORG_INT_OVERSEAS_INVESTMENT_INSURANCE_GROUP_1975
    N_ORG_CL_CAP_STEEL_1971["Compañía de Acero del Pacífico (CAP, 1971)"]
    N_ORG_US_BETHLEHEM_STEEL_1971["Bethlehem Steel (Chile-Eisenerzinteressen 1971)"]
    N_ORG_CL_CAP_STEEL_1971 -->|"FRUS 30.03.1971: Vereinbarung über Übernahme chilenischer Eisenerzinteressen, erwartete Entschädigung 20–23 Mio. USD abhängig von Bewertung, 15 Jahresraten ab Juni 1973 zu 5¾ %."| N_ORG_US_BETHLEHEM_STEEL_1971
    N_ORG_US_OPIC_1971 -->|"OPIC garantierte Bethlehem laut FRUS 30.03.1971 mindestens 18 Mio. USD bei Nichterfüllung durch CAP; kein nachgewiesener Garantieabruf."| N_ORG_US_BETHLEHEM_STEEL_1971
    N_ORG_US_OPIC_1971 -->|"OPIC bat Juli 1975 um Neuverhandlung der Chile-Investitionsgarantieregeln; State Department stimmte Verhandlungen zu, Unterzeichnungsfreigabe separat. Kein belegter Vertragsschluss 1975/76."| N_ORG_US_STATE_DEPARTMENT
    N_PER_US_C_FRED_BERGSTEN["C. Fred Bergsten"]
    N_PER_US_C_FRED_BERGSTEN -->|"GAO ID-78-36 Appendix I S. 15 und Appendix II S. 17: C. Fred Bergsten ab 24.05.1977 OPIC-Boardmitglied; kein Nachweis individueller Anordnung der FFB-Transaktion."| N_ORG_US_OPIC_1971
    N_PER_US_C_FRED_BERGSTEN -->|"Assistant Secretary of the Treasury for International Affairs im Jahr 1977, gleichzeitig OPIC-Boardmitglied ab 24.05.; Kongressaussage zur Teilprivatisierung 27.07.1977."| N_ORG_US_TREASURY
    N_ORG_CL_CHAMBER_OF_DEPUTIES["Cámara de Diputados de Chile"]
    N_ORG_CL_ALLENDE_GOVERNMENT_1972 -->|"Oficio 13.794 vom 07.07.1971: Allende/Almeyda ziehen die Genehmigungsvorlage zum US-Investitionsgarantie-Zusatzabkommen vom 03.12.1963 (Boletín 2268) zurück; Kammer stimmt am 13.07.1971 zu. Kein Nachweis damaliger Ratifikation."| N_ORG_CL_CHAMBER_OF_DEPUTIES
    N_ORG_CL_EXOTICA_COPPER_1971["Compañía Minera Exótica (Chile)"]
    N_ORG_CL_CHILE_COPPER_ANACONDA_1972 -->|"DL821: Chile Copper Company hielt historisch 75% an Exótica; keine heutige Beteiligung abgeleitet."| N_ORG_CL_EXOTICA_COPPER_1971
    N_ORG_CL_CORPORACION_DEL_COBRE_1974["Corporación del Cobre (Chile, 1974)"]
    N_ORG_CL_CORPORACION_DEL_COBRE_1974 -->|"DL821: Corporación del Cobre hielt 25% an Exótica; eigene Ansprüche getrennt."| N_ORG_CL_EXOTICA_COPPER_1971
    N_ORG_US_OPIC_1971 -->|"BCCh Acta87 und CRS: 11.890.000 USD Exótica-Eigenkapitalentschädigung bezahlt; Bankkreditdeckung separat bestritten."| N_ORG_CL_CHILE_COPPER_ANACONDA_1972
    N_ORG_CL_CHILE_COPPER_ANACONDA_1972 -->|"DL821: vertragliche Forderungsabtretung an OPIC 06.10.1972; spätere Tilgungen offen."| N_ORG_US_OPIC_1971
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"Vergleich 24.12.1974: 11,25 Mio. Kapital + 2,7 Mio. Zinsen = 13,95 Mio. USD; 4,575 Mio. sofort vorgesehen, 9,375 Mio. Noten; vollständige Zahlung offen."| N_ORG_US_OPIC_1971
    N_ORG_CL_CORPORACION_DEL_COBRE_1974 -->|"Corporación del Cobre war mit Chile und OPIC Vertragspartnerin der Exótica-Vereinbarung; eigene 25%-Ansprüche separat."| N_ORG_US_OPIC_1971
    N_ORG_US_RIGGS_NATIONAL_BANK["Riggs National Bank (Washington, D.C.)"]
    N_ORG_CL_MILITARY_JUNTA_1973 -->|"BCCh 26.12.1974: Zahlungsanweisung Chiles an Riggs bis 31.12. für 4,575 Mio. USD vorgesehen; keine Bankbuchung belegt."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_CL_BANCO_CENTRAL_1974["Banco Central de Chile"]
    N_ORG_CL_BANCO_CENTRAL_1974 -->|"BCCh beschloss Mithaftung für fünf OPIC-Noten à 1,875 Mio. USD, zusammen 9,375 Mio., 8,3% Zins; keine Tilgungsableitung."| N_ORG_US_OPIC_1971
    N_PER_CL_AUGUSTO_PINOCHET["Augusto Pinochet"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"US-Senatsbericht 2005 identifiziert 28 Riggs-Konten/CDs in Pinochet-Komplex 1979–2004, darunter Konten im Namen von Dritten. Keine Herkunft aus Exótica 1974 nachgewiesen."| N_PER_CL_AUGUSTO_PINOCHET
    N_ORG_CL_ARMED_FORCES_HISTORICAL["Chilenische Streitkräfte (historischer Kontext 1972–2002)"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Senatsbericht 2005, IV.B: Riggs hatte langjährige Beziehungen zu chilenischen Militärinstitutionen, stellte 1994 etliche Konten wieder her; Militär und Botschaft zusammen 2002 ca.100 Mio. USD Einlagen. Keine Privatvermögenssumme, keine OPIC-Zahlungsidentität."| N_ORG_CL_ARMED_FORCES_HISTORICAL
    N_ORG_US_OPIC_1971 -->|"DFC FY74 Anaconda Chile 13.640.000 USD Cash, keine Garantie; nicht mit Exótica 11,89 Mio. oder späterer Abwicklung gleichsetzen."| N_ORG_US_ANACONDA_COPPER_1972
    N_ORG_US_OPIC_1971 -->|"DFC FY74 Chile Typ A: 463.207 und 2.633.876 USD Cash, keine Garantien; zweite Zahl Textansicht, letzte Ziffer Faksimile angeschnitten; Policenidentität offen."| N_ORG_US_BANK_OF_AMERICA_1974
    N_ORG_US_OPIC_1971 -->|"DFC FY75 Chile Typ B: 3.010.272 USD Cash, keine Garantie; nicht als Petrodow/Arauco FY78 identifizieren."| N_ORG_US_BANK_OF_AMERICA_1974
    N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971["First National City Bank / Citibank, N.A. (Umbenennung 1976)"]
    N_ORG_US_OPIC_1971 -->|"DFC FY73 Typ B 66.503 USD Cash, CRS 1973 S.75 gerundet 66.500 USD. Keine Identität mit El Mercurio."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_ORG_US_OPIC_1971 -->|"GAO: Chile-Garantiebestand FY82 60,2 Mio. und FY84 9,8 Mio. USD inkl. Zinsen; Differenz keine Barzahlung."| N_ORG_CL_MILITARY_JUNTA_1973
    N_ORG_CL_BANCO_CENTRAL_1974 -->|"Acta1648 Anlage Blatt23: Kontrolle/Registrierung von OPIC-Mitteilungen nach Abkommen 1983/84; keine neue Einzelpolice belegt."| N_ORG_US_OPIC_1971
    N_ORG_US_CHILE_PRIVATE_CREDITOR_BANKS_1971["US-Privatbank-Gläubigerverhandlungen mit Chile (1971–1972)"]
    N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971 -->|"FRUS Dok95: FNCB leitete mit Bank of America 14.12.1971 Zusammenkunft von 43 US-Privatbanken in New York."| N_ORG_US_CHILE_PRIVATE_CREDITOR_BANKS_1971
    N_ORG_US_BANK_OF_AMERICA_1974 -->|"FRUS Dok95: Bank of America leitete mit FNCB 14.12.1971 Zusammenkunft von 43 US-Privatbanken; Einzelverträge nicht identifiziert."| N_ORG_US_CHILE_PRIVATE_CREDITOR_BANKS_1971
    N_ORG_US_STATE_DEPARTMENT -->|"FRUS 12.01.1972: State-Kontakt mit Privatbanken; restriktive Kreditstrategie und Verzögerungsüberlegungen; keine Weisungsausführung belegt."| N_ORG_US_CHILE_PRIVATE_CREDITOR_BANKS_1971
    N_ORG_US_CHILE_CREDITO2_LENDERS_1972["US-Privatbanken des chilenischen Zusatzkredits Crédito 2 (1972)"]
    N_ORG_CL_BANCO_CENTRAL_1974 -->|"Acta87 S.2–3: fünf Ersatznoten zum Zusatzkredit 1972, Plansumme 72.362.886,16 USD; Bankliste fehlt, nicht Exótica-Noten."| N_ORG_US_CHILE_CREDITO2_LENDERS_1972
    N_PER_US_EDWARD_KORRY["Edward M. Korry"]
    N_PER_US_EDWARD_KORRY -->|"Korry bat Washington 16.09.1970 um Lockerung von FNCB-Einziehungsforderungen gegenüber El Mercurio; keine Befolgung belegt."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_PER_US_EDWARD_KORRY -->|"Korry 25.09.1970 nennt BoA bei Vorschlägen wirtschaftlicher Druckmittel; keine Umsetzung/Bankzustimmung nachgewiesen."| N_ORG_US_BANK_OF_AMERICA_1974
    N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971 -->|"CIA/State 23.02. und CIA 10.04.1972 nennen FNCB als Auslandsgläubigerin; Einzelbetrag und OPIC-Identität offen."| N_ORG_CL_EL_MERCURIO_1971
    N_ORG_US_FIRST_WISCONSIN_NATIONAL_BANK_1972["First Wisconsin National Bank (Milwaukee, 1972)"]
    N_ORG_US_FIRST_WISCONSIN_NATIONAL_BANK_1972 -->|"Februar 1972 rund 293.000 USD Schuld bei Bank of Wisconsin; CIA April identifiziert First Wisconsin National Bank; Einziehungslockerung erfolglos."| N_ORG_CL_EL_MERCURIO_1971
    N_ORG_CL_BANCO_CENTRAL_1974 -->|"CIA 10.04.1972: Zentralbankzahlung hing an privater US-Bankenumschuldung und Pariser Abkommen; keine erfolgte Überweisung belegt."| N_ORG_US_FIRST_WISCONSIN_NATIONAL_BANK_1972
    N_ORG_US_STATE_DEPARTMENT -->|"CIA-Vorlage beschreibt erfolglose diplomatische Intervention zur Lockerung der First-Wisconsin-Einziehung."| N_ORG_US_FIRST_WISCONSIN_NATIONAL_BANK_1972
    N_ORG_US_SUN_CHEMICAL_1972["Sun Chemical Company (El-Mercurio-Lieferantin, 1972)"]
    N_ORG_US_SUN_CHEMICAL_1972 -->|"CIA-Akten: US-Lieferkosten ca. 500.000 USD jährlich, Kredit 100.000, Ausweitung auf 300.000 vorgeschlagen, nicht als ausgeführt belegt."| N_ORG_CL_EL_MERCURIO_1971
    N_ORG_US_CIA -->|"CIA-Vorlage 10.04.1972 sah Ablösung der First-Wisconsin-Forderung vor, u.a. durch Beschaffung chilenischer Escudos am Schwarzmarkt. Keine konkret ausgeführte Zahlung oder bewusste CIA-Kooperation der Bank belegt."| N_ORG_US_FIRST_WISCONSIN_NATIONAL_BANK_1972
    N_ORG_US_CIA -->|"CIA 10.04.1972: vorgeschlagene Absicherung zur Ausweitung Lieferantenkredit 100.000 auf 300.000 USD; keine ausgeführte Garantie belegt."| N_ORG_US_SUN_CHEMICAL_1972
    N_ORG_US_40_COMMITTEE_1972["40 Committee (1972)"]
    N_ORG_US_40_COMMITTEE_1972 -->|"965.000 USD Zusatzhilfe gebilligt, einschließlich Schuldendienst und Lieferkredit. Editionsanmerkung Dok108: 11.04.1972; CIA-Rückblick Dok145: 12.04.1972. Keine weitere Auszahlung oder Einzelbankzahlung."| N_ORG_CL_EL_MERCURIO_1971
    N_ORG_US_CITIGROUP_2004["Citigroup Inc. und im Senatsbericht erfasste Vorgänger/Verbundunternehmen (2004)"]
    N_ORG_US_CITIGROUP_2004 -->|"SEC-Prospekt 2004: Citibank, N.A. vollständig im Eigentum von Citicorp, dieses indirekte 100%-Tochter von Citigroup; Bankname seit 01.03.1976. Nicht gleichbedeutend mit identischer Rechtsperson."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_ORG_US_CITIGROUP_2004 -->|"Senatsbericht V.A: 63 US-Konten/CDs 1981–2004 für Pinochet und Familie/verbundene Strukturen; 15 persönliche, 19 Familien-, 29 Offshore-Konten. 1960er-Konto nur Erinnerung, nicht belegt."| N_PER_CL_AUGUSTO_PINOCHET
    N_ORG_US_CITIGROUP_2004 -->|"Senatsbericht V.A dokumentiert am 25.04.1996 403.000 USD von Meritor Investments (Marco Pinochet) über Citi an Pinochet-bezogenes Riggs-Konto. Kein Nachweis OPIC-Herkunft oder Strafbarkeit aller Beteiligten."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_CL_AUGUSTO_PINOCHET_UGARTE_FOUNDATION["Fundación Augusto Pinochet Ugarte (1997)"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Riggs spendete 1997 laut Senat 5.000 USD auf Anfrage General Izurietas; Dankschreiben 22.04.1997. Keine nachgewiesene Gegenleistung."| N_ORG_CL_AUGUSTO_PINOCHET_UGARTE_FOUNDATION
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"DOJ 27.01.2005: Riggs bekannte sich schuldig wegen systematischer strafbarer Nichtmeldung verdächtiger Transaktionen bei Pinochet-/Äquatorialguinea-Konten; 16 Mio. USD vereinbarte Geldstrafe. Keine Rückprojektion auf 1974."| N_ORG_US_DOJ
    N_ORG_US_KENNECOTT_COPPER_CORP_1971["Kennecott Copper Corporation / Braden Copper (Chile-Fall)"]
    N_ORG_US_OPIC_1971 -->|"FRUS 29.09.1971 und Anlage 12.01.1972: 85 Mio. USD OPIC-Deckung bei Kennecott, 88 Mio. Kreditforderung umstritten; Deckung keine Auszahlung."| N_ORG_US_KENNECOTT_COPPER_CORP_1971
    N_ORG_US_OPIC_1971 -->|"DFC FY73 Braden Copper/Kennecott: 66.908.494 USD Vergleich/Garantie, 38.709.753 USD später Cash unter Garantie laut Fn.1; nicht addieren, Abrufdatum/Policenidentität offen. CRS 1973 ca.67 Mio. Garantie."| N_ORG_US_KENNECOTT_COPPER_CORP_1971
    N_ORG_US_OPIC_1971 -->|"DFC FY72 Bethlehem: 17.365.721 USD Vergleich/Garantie, 3.076.820 USD später Cash unter Garantie laut Fn.1; nicht addieren, nicht identisch mit 1971 geplanter Mindestdeckung bewiesen."| N_ORG_US_BETHLEHEM_STEEL_1971
    N_ORG_US_OPIC_1971 -->|"DFC Denial Table: Bank of America Chile Typ A, Anspruch 2.913.021 USD, abgelehnt 26.03.1973. Keine Schiedszahlung in Zeile ausgewiesen; keine Identität mit anderen BoA-Policen."| N_ORG_US_BANK_OF_AMERICA_1974
    N_PER_US_PAUL_VOLCKER["Paul A. Volcker (Treasury/OPIC, 1971)"]
    N_PER_US_PAUL_VOLCKER -->|"GAO FY1971 Appendix I/II: Paul Volcker seit 19.01.1971 OPIC-Boardmitglied, gleichzeitig Under Secretary of Treasury for Monetary Affairs. Kein Nachweis individueller Chile-Fallweisung."| N_ORG_US_OPIC_1971
    N_PER_US_PAUL_VOLCKER -->|"GAO FY1971 Appendix II nennt Paul Volcker als Under Secretary of Treasury for Monetary Affairs (Stand 30.06.1971) und OPIC-Boardmitglied."| N_ORG_US_TREASURY
    N_ORG_US_CIA -->|"CIA Dok108, 10.04.1972: Beschaffung chilenischer Escudos am Schwarzmarkt zur Tilgung der First-Wisconsin-Schuld vorgesehen; Decktransaktionen diskutiert. Keine Ausführung oder strafgerichtliche Bewertung belegt."| N_ORG_CL_EL_MERCURIO_1971
    N_ORG_CL_EL_MERCURIO_1971 -->|"CIA Dok108 berichtet, El Mercurio habe bei First Wisconsin den Eindruck einer erfolgten Hinterlegung bei der Zentralbank erweckt, obwohl Mittel fehlten; CIA-Bericht, kein eigenständiges Bank-/Gerichtsdokument."| N_ORG_US_FIRST_WISCONSIN_NATIONAL_BANK_1972
    N_ORG_US_STATE_DEPARTMENT -->|"CIA/State 23.02.1972 diskutierten politische Instrumentalisierung einer möglichen Zeitungseinstellung; NSC 10.04.1972 erwog Pressefreiheitsthema. Keine ausgeführte Schließungsinszenierung belegt."| N_ORG_CL_EL_MERCURIO_1971
    N_PER_US_EDWARD_KORRY -->|"Korry 25.09.1970, Abs.8–14: Kreditbeschränkung, wirtschaftliche Negativpublizistik über Geschäftsleute ohne sichtbare USG, Unternehmensschließung und wirtschaftliche Druckoptionen erwogen; Umsetzung nicht belegt."| N_ORG_CL_ALLENDE_GOVERNMENT_1972
    N_ORG_US_STATE_DEPARTMENT -->|"Anlage 12.01.1972: US-Planung wollte Schuldenerleichterungen politisch begrenzen und Gläubiger schützen, harte Bedingungen, ggf. verzögerte Unterschrift bei zunehmender innerer Unzufriedenheit. Keine pauschale tatsächliche Kreditverweigerung abgeleitet."| N_ORG_CL_ALLENDE_GOVERNMENT_1972
    N_ORG_US_STATE_DEPARTMENT -->|"Anlage 12.01.1972 S.499: State/Defense befürworteten Fortführung noch nicht ausgezahlter 8 Mio. USD Militärkredite im rechtlich möglichen Umfang wegen oppositionellen Potenzials der Streitkräfte; keine neue Auszahlung."| N_ORG_CL_ARMED_FORCES_HISTORICAL
    N_ORG_US_DOD -->|"Anlage 12.01.1972 S.499/511ff: Defense befürwortete mit State Erhalt des FMS-Kreditprogramms für Chile aus politischer Erwägung; 8 Mio. USD ausstehende Auszahlung, keine zusätzliche Summe."| N_ORG_CL_ARMED_FORCES_HISTORICAL
    N_ORG_US_IC_1990S["US Intelligence Community (Wirtschaftsaufklärung 1993–1995)"]
    N_ORG_US_IC_1990S -->|"Wirtschaftsaufklärung für staatliche Entscheidungsträger; SSCI berichtet Juli 1994 über wirtschaftlichen Nutzen"| N_ORG_US_STATE_DEPARTMENT
    N_ORG_US_COMMERCE["US Department of Commerce"]
    N_ORG_US_IC_1990S -->|"Commerce als Nutzer; im Juli 1994 berichtete Vorteile aus Geheimdienstinformationen, Einzelfälle nicht offengelegt"| N_ORG_US_COMMERCE
    N_ORG_US_SSCI["Senate Select Committee on Intelligence (SSCI)"]
    N_ORG_US_STATE_DEPARTMENT -->|"Juli 1994: Darstellung wirtschaftlicher Vorteile in nichtöffentlicher Anhörung"| N_ORG_US_SSCI
    N_ORG_US_COMMERCE -->|"Juli 1994: Darstellung wirtschaftlicher Vorteile in nichtöffentlicher Anhörung"| N_ORG_US_SSCI
    N_PER_US_WILLIAM_STUDEMAN["William O. Studeman"]
    N_PER_US_WILLIAM_STUDEMAN -->|"03.04.1995: Übermittlung koordinierter Intelligence-Community-Antworten zur Anhörung vom 10.01.1995"| N_ORG_US_SSCI
    N_ORG_US_OSAC["Overseas Security Advisory Council (OSAC)"]
    N_ORG_US_STATE_DEPARTMENT -->|"1985 eingerichtetes Forum für Sicherheits- und Informationsaustausch"| N_ORG_US_OSAC
    N_PER_US_JAMES_WOOLSEY -->|"Treffen mit OSAC-Exekutivkomitee 15.11.1993 laut schriftlichem CIA-Nachtrag 03.04.1995"| N_ORG_US_OSAC
    N_ORG_US_NSA["National Security Agency (NSA)"]
    N_ORG_US_NSA -->|"Technische Beratung des Informations-/Technologieschutz-Fachausschusses laut CIA-Antwort April 1995"| N_ORG_US_OSAC
    N_ORG_US_NACIC_1994["National Counterintelligence Center (NACIC, 1994)"]
    N_ORG_US_NACIC_1994 -->|"Technische Beratung des OSAC-Fachausschusses laut CIA-Antwort April 1995"| N_ORG_US_OSAC
    N_ORG_US_FBI["Federal Bureau of Investigation (FBI)"]
    N_ORG_US_IC_1990S -->|"Koordination der Abwehr fremdstaatlich geförderter Wirtschaftsspionage, wechselseitige Warnungen/Briefings laut CIA"| N_ORG_US_FBI
    N_ORG_US_IBM_1992["IBM Corporation (1992)"]
    N_ORG_US_IBM_1992 -->|"IBM-Sicherheitsdirektor Richard E. Mainey als Vizevorsitzender laut Mitgliederliste November 1992; keine spätere Dauer unterstellt"| N_ORG_US_OSAC
    N_ORG_US_CITICORP_1992["Citicorp/Citibank N.A. (1992)"]
    N_ORG_US_CITICORP_1992 -->|"Citicorp/Citibank N.A., eine Vertretung laut Mitgliederliste November 1992; keine spätere Dauer unterstellt"| N_ORG_US_OSAC
    N_ORG_US_BECHTEL_1992["Bechtel Corporation (1992–1996)"]
    N_ORG_US_BECHTEL_1992 -->|"Bechtel-Sicherheitsvertretung laut Mitgliederliste November 1992; keine spätere Dauer unterstellt"| N_ORG_US_OSAC
    N_ORG_US_MCDONNELL_DOUGLAS_1992["McDonnell Douglas (1992–1996)"]
    N_ORG_US_MCDONNELL_DOUGLAS_1992 -->|"McDonnell-Douglas-Vertretung laut Mitgliederliste November 1992; keine spätere Dauer unterstellt"| N_ORG_US_OSAC
    N_ORG_US_BOEING_1993["Boeing (1993–1996)"]
    N_ORG_US_BOEING_1993 -->|"05.08.1993: Unternehmensvertreter Hayden/Blay wünschen Schutz vor fremder Spionage, lehnen Beschaffung fremder Geschäftsgeheimnisse ab"| N_ORG_US_SSCI
    N_ORG_US_TPCC_ADVOCACY["Advocacy Coordinating Network (1993–1994)"]
    N_ORG_US_COMMERCE -->|"Seit November 1993 Exportförderungskoordination mit 17 Behörden laut National Export Strategy"| N_ORG_US_TPCC_ADVOCACY
    N_ORG_US_STATE_DEPARTMENT -->|"Diplomatische Beteiligung an behördenübergreifender Exportförderung 1994"| N_ORG_US_TPCC_ADVOCACY
    N_ORG_US_EXIMBANK_1994["Export–Import Bank of the United States (Exportfinanzierung 1994–1997)"]
    N_ORG_US_EXIMBANK_1994 -->|"EXIM beteiligt sich laut Regierungsbericht an Exportförderungskoordination"| N_ORG_US_TPCC_ADVOCACY
    N_ORG_US_OPIC_1971 -->|"OPIC in Exportförderungskoordination; mögliche SIVAM-Finanzierung ist keine nachgewiesene Auszahlung"| N_ORG_US_TPCC_ADVOCACY
    N_PRG_BR_SIVAM["Sistema de Vigilância da Amazônia (SIVAM)"]
    N_ORG_US_TPCC_ADVOCACY -->|"National Export Strategy nennt diplomatische und kommerzielle Unterstützung der Raytheon-Auswahl"| N_PRG_BR_SIVAM
    N_ORG_US_EXIMBANK_1994 -->|"4.426 Mio. USD EXIM-Finanzierungszusagen zur Unterstützung des Exporteurs/Auftragnehmers FY1994–96; keine Firmenzahlung"| N_ORG_US_BOEING_1993
    N_ORG_US_RAYTHEON_1994["Raytheon Company (SIVAM 1994–2008)"]
    N_ORG_US_EXIMBANK_1994 -->|"1.923 Mio. USD EXIM-Finanzierungszusagen zur Unterstützung des Exporteurs/Auftragnehmers FY1994–96; keine Firmenzahlung"| N_ORG_US_RAYTHEON_1994
    N_ORG_US_EXIMBANK_1994 -->|"938 Mio. USD EXIM-Finanzierungszusagen zur Unterstützung des Exporteurs/Auftragnehmers FY1994–96; keine Firmenzahlung"| N_ORG_US_BECHTEL_1992
    N_ORG_US_EXIMBANK_1994 -->|"745 Mio. USD EXIM-Finanzierungszusagen zur Unterstützung des Exporteurs/Auftragnehmers FY1994–96; keine Firmenzahlung"| N_ORG_US_MCDONNELL_DOUGLAS_1992
    N_ORG_US_EXIMBANK_1994 -->|"530 Mio. USD EXIM-Finanzierungszusagen zur Unterstützung des Exporteurs/Auftragnehmers FY1994–96; keine Firmenzahlung"| N_ORG_US_FLUOR
    N_ORG_SA_GOVERNMENT_1994["Saudi-Arabien (Flugzeugbeschaffung 1994)"]
    N_ORG_SA_GOVERNMENT_1994 -->|"16.02.1994: angekündigte zivile Flugzeugbeschaffung; beide Firmen zusammen knapp 6 Mrd. USD, keine individuelle Zurechnung"| N_ORG_US_BOEING_1993
    N_ORG_SA_GOVERNMENT_1994 -->|"16.02.1994: angekündigte zivile Flugzeugbeschaffung; beide Firmen zusammen knapp 6 Mrd. USD, keine individuelle Zurechnung"| N_ORG_US_MCDONNELL_DOUGLAS_1992
    N_ORG_BR_SENADO_FEDERAL["Senado Federal (Brasilien)"]
    N_ORG_BR_UNION_SIVAM["Brasilianische Union (SIVAM-Verträge)"]
    N_ORG_BR_SENADO_FEDERAL -->|"Resolution 96: 1.288.255.370 USD genehmigter Kredit über Banco do Brasil Grand Cayman, nicht Auszahlungsnachweis"| N_ORG_BR_UNION_SIVAM
    N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994["Banco do Brasil S.A., Agência Grand Cayman (1994)"]
    N_ORG_US_EXIMBANK_1994 -->|"Resolution 96 genehmigt Weiterleitung von EXIM-Mitteln durch die Grand-Cayman-Niederlassung"| N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994
    N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994 -->|"1.288.255.370 USD genehmigte externe Kreditoperation laut Art. 1; keine tatsächliche Zahlung belegt"| N_ORG_BR_UNION_SIVAM
    N_ORG_US_RAYTHEON_1994 -->|"Resolution 97: 239,2 Mio. USD genehmigter Lieferantenkredit, 9 Prozent Festzins nach ursprünglicher Regelung"| N_ORG_BR_UNION_SIVAM
    N_ORG_BR_SENADO_FEDERAL -->|"Resolutionen 96/97 Art. 3: geplanter CCSIVAM-Vertrag mit ESCA/Raytheon-Konsortium als Finanzierungsbedingung; nicht mit späterem Vertrag 01/95 gleichgesetzt"| N_PRG_BR_SIVAM
    N_ORG_US_EXIMBANK_1994 -->|"EXIM-Rückblick: 1994 ca. 1,3 Mrd. USD bewilligt; GAO AP 67303 bestätigt Datum und spätere Kreditänderung"| N_PRG_BR_SIVAM
    N_ORG_US_EXIMBANK_1994 -->|"04.03.1997: 34 Mio. USD Kreditänderung AP 67303, Raytheon-Lieferungen; nicht zusätzlich zur ursprünglichen Gesamtsumme addieren"| N_PRG_BR_SIVAM
    N_ORG_BR_CCSIVAM["Comissão de Coordenação de Implantação do SIVAM (CCSIVAM)"]
    N_DOC_BR_CCSIVAM_RAYTHEON_0195["Vertrag 01/95 – CCSIVAM/Raytheon"]
    N_ORG_BR_CCSIVAM -->|"Vertrag 01/95 CCSIVAM/Raytheon, aus gerichtlicher Wiedergabe identifiziert; vollständiger Vertragsvolltext fehlt"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_US_RAYTHEON_1994 -->|"Vertrag 01/95 mit CCSIVAM; ursprüngliche Aufgabenabgrenzung gerichtlich beanstandet"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_ESCA["ESCA – Engenharia de Controle e Automação S.A."]
    N_ORG_BR_ESCA -->|"Ursprüngliche nationale Integratorin; später nach Vorwürfen des Sozialversicherungsbetrugs aus Vertrag entfernt"| N_PRG_BR_SIVAM
    N_ORG_BR_ATECH_FOUNDATION["Fundação Aplicações de Tecnologias Críticas (ATECH)"]
    N_ORG_BR_ATECH_FOUNDATION -->|"1997 durch Nachträge 9/10 als nationale Integratorin einbezogen (TRF4 2003); spätere strategische Aufgabenabgrenzung im STJ-Urteil 2008"| N_PRG_BR_SIVAM
    N_ORG_BR_UNION_SIVAM -->|"Luftfahrtministerium meldet dem Senat Vertragswirksamkeit ab 25.07.1997 nach geänderten Resolutionen"| N_PRG_BR_SIVAM
    N_ORG_BR_CPI_SIVAM_2002["CPI SIVAM (Câmara dos Deputados)"]
    N_ORG_BR_CPI_SIVAM_2002 -->|"CPI-Abschluss 04.06.2002: Indizien, fehlende Auslandsbankdaten, keine Strafentscheidung"| N_PRG_BR_SIVAM
    N_ORG_BR_MPF["Ministério Público Federal (Brasilien)"]
    N_ORG_BR_CPI_SIVAM_2002 -->|"Abschlussbericht und gesonderte Gegenunterlagen zur Weitergabe an MPF bestimmt; Eingangsbeleg und Verfahrensausgang offen"| N_ORG_BR_MPF
    N_ORG_BR_TRF4["Tribunal Regional Federal da 4ª Região"]
    N_ORG_BR_TRF4 -->|"2003 bestätigt TRF4 die 1997 ausgesprochene Nichtigkeit; spätere Aufhebung durch STJ beachten"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_STJ["Superior Tribunal de Justiça (STJ)"]
    N_ORG_BR_STJ -->|"03.04.2008 REsp 719.548-PR: Vorentscheidung aufgehoben, Verfahren ohne Sachentscheidung beendet; Vermögensschaden nicht nachgewiesen"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997["Banco do Brasil S.A. (SIVAM, 1997–2006)"]
    N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997 -->|"Grand-Cayman-Niederlassung des vertraglichen SIVAM-Finanzierers Banco do Brasil"| N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994
    N_ORG_US_EXIMBANK_1994 -->|"Vertrag AP067303XX, direktes EXIM-Limit USD1.288.255.370, laut TCU1249/2005; kein Einzelabrufnachweis"| N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994
    N_ORG_US_EXIMBANK_1994 -->|"EXIM-garantierte Linie AP067902XX, Limit USD105.046.668,50; Garantie nicht mit direkter Auszahlung gleichgesetzt"| N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994
    N_ORG_NL_ABN_AMRO_SIVAM_1997["ABN AMRO Bank (SIVAM-Refinanzierung 1997)"]
    N_ORG_NL_ABN_AMRO_SIVAM_1997 -->|"1997 als einer von drei Kreditgebern genannt, durch endgültigen Prospekt bestätigt; exakte einzelne Tranche nicht dokumentiert"| N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997
    N_ORG_SE_SVENSK_EXPORTKREDIT_SIVAM_1997["AB Svensk Exportkredit (SEK, SIVAM)"]
    N_ORG_SE_SVENSK_EXPORTKREDIT_SIVAM_1997 -->|"TCU1249/2005: unterzeichneter SEK-Finanzierungsvertrag mit BB Grand Cayman, Limit USD91.025.000"| N_ORG_BR_BANCO_DO_BRASIL_CAYMAN_1994
    N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997 -->|"Drei Gegenverträge mit der Union; USD1.484.327.038,50 Vertragsvolumen und 1,5 Prozentpunkte jährliche Zinsvergütung laut BCB"| N_ORG_BR_UNION_SIVAM
    N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997 -->|"Endgültiger Prospekt: ca. USD1,3 Mrd. kumulativ ausgezahlt bis 31.03.2006; keine Empfänger-Einzelabrechnung"| N_ORG_BR_UNION_SIVAM
    N_ORG_BR_UNION_SIVAM -->|"72,1% des stimmberechtigten und gesamten Kapitals am 31.03.2006 laut endgültigem Prospekt"| N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997
    N_ORG_BR_BCB["Banco Central do Brasil (BCB)"]
    N_ORG_BR_CMN["Conselho Monetário Nacional (CMN)"]
    N_ORG_BR_BCB -->|"Voto305/97 / CMN129/97 empfiehlt 0 statt 100% Risikogewicht für strategische SIVAM-Kredite"| N_ORG_BR_CMN
    N_ORG_BR_CMN -->|"CMN genehmigt 28.08.1997 Risikogewicht 0% für SIVAM; BCB444/97 bestätigt Eigenkapitalentlastung, keine tatsächliche Risikolosigkeit"| N_ORG_BR_BANCO_DO_BRASIL_SIVAM_1997
    N_ORG_US_RAYTHEON_1994 -->|"Raytheon Credit Facility mit Limit USD239,2 Mio. laut TCU1249/2005; tatsächlicher Einzelabruf offen"| N_ORG_BR_UNION_SIVAM
    N_ORG_INT_SIVAM_VENDOR_TRUST_1994["SIVAM Vendor Trust (Kreditgenehmigung 1994)"]
    N_ORG_INT_SIVAM_VENDOR_TRUST_1994 -->|"Resolution95/1994 genehmigt USD48 Mio. SIVAM Vendor Trust; TCU1249/2005 §15 Fn.3 bestätigt den Vertragspartner der Vendor Facility; Einzelabruf offen"| N_ORG_BR_UNION_SIVAM
    N_ORG_BR_SENADO_FEDERAL -->|"Res.37/1996 hebt Art.3/4 der fünf ursprünglichen Kreditresolutionen auf, Fristen +270 Tage und neue Schutz-/Ausschreibungsbedingungen"| N_PRG_BR_SIVAM
    N_ORG_BR_EMBRAER_SIVAM["Embraer (SIVAM-Verträge, 1990er–2005)"]
    N_ORG_BR_EMBRAER_SIVAM -->|"1997 durch dieselben Nachträge 9/10 als Flugzeuglieferantin in Vertrag 01/95 aufgenommen; exakter Tag nicht belegt"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_ATECH_FOUNDATION -->|"1997 durch Nachträge 9/10 in Vertrag 01/95 aufgenommen, nicht erst 2005/2008; exakter Tag nicht belegt"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_TCU["Tribunal de Contas da União (TCU)"]
    N_ORG_BR_CMO["Comissão Mista de Orçamento (CMO)"]
    N_ORG_BR_TCU -->|"TCU ordnet Warnung vor möglicher vorzeitiger Fälligkeit von rund USD1,5 Mrd. bei Nichtzahlung an; kein Nachweis eingetretener Fälligstellung"| N_ORG_BR_CMO
    N_ORG_BR_TCU -->|"TCU dokumentiert Klausel24.1.18 und verknüpfte Default-Klauseln der fünf Finanzierungen, bei qualifiziertem Zahlungsverzug mögliche Kündigung/Fälligstellung"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_UNION_SIVAM -->|"Lei11.199 vom 24.11.2005: R$70 Mio. Zusatzbewilligung; keine Zahlungsabrechnung"| N_PRG_BR_SIVAM
    N_ORG_BR_UNION_SIVAM -->|"CPI2002 S.126 gibt TCU-Prüfung wieder: R$2 Mio. an ESCA 1994–95 für Beratung/Engineering zur Integrationslogik; keine Bestechungsfeststellung"| N_ORG_BR_ESCA
    N_PER_BR_JOSE_ROBERTO_TOSCANO_DANTAS["José Roberto Toscano Dantas"]
    N_ORG_BR_ESCA -->|"TCU48/2001 erörtert ESCA-Vergütung des Rechtsberaters auf Anregung des Ministeriums; spätere Mehrheit sah Schaden/Bereicherung/bösen Glauben nicht nachgewiesen"| N_PER_BR_JOSE_ROBERTO_TOSCANO_DANTAS
    N_ORG_BR_CISCEA["Comissão de Implantação do Sistema de Controle do Espaço Aéreo (CISCEA)"]
    N_PER_BR_JOSE_ROBERTO_TOSCANO_DANTAS -->|"TCU48/2001 dokumentiert längerfristige juristische Tätigkeit für Luftwaffe/CISCEA neben ESCA-Vergütung; zeitliche Aussage auf Prüfakte beschränkt"| N_ORG_BR_CISCEA
    N_ORG_BR_TCU -->|"Technische Prüfung zu Auswahlsitzung 13.09.1993: sechs von neun Beteiligten mit ESCA-Verbindungen; Mehrheit hob 2001 die Ziffern a–c von 87/96 auf; keine strafrechtliche Entscheidung"| N_ORG_BR_ESCA
    N_ORG_BR_TCU -->|"TCU110/96 bezog ESCA in besondere Rechnungsprüfung ein; TCU48/2001 hob 87/96 a–c später auf, kein Strafurteil"| N_ORG_BR_ESCA
    N_ORG_BR_TCU -->|"TCU82/97: umverteilte Teilkosten USD28.475.782, Bezifferung nicht verifiziert; Konsortienüberschneidung im abweichenden Prüfbeitrag, keine bewiesene Absprache"| N_DOC_BR_CCSIVAM_RAYTHEON_0195
    N_ORG_BR_TCU -->|"17.11.1999: TCU850/99 beurteilt Direktvergabe an Embraer/ATECH als regulär; Entscheidung veröffentlicht, übrige Akten vertraulich"| N_ORG_BR_CCSIVAM
    N_ORG_BR_TCU -->|"TCU850/99 Ziff.8.2–8.3: Übermittlung von Entscheidung und Grundlagen an Senatspräsidentschaft sowie Senatoren Valadares/Amorim unter Vertraulichkeit angeordnet"| N_ORG_BR_SENADO_FEDERAL
    N_ORG_BR_SCHAHIN_SIVAM_1999["Schahin (SIVAM-Bauauftrag 1999)"]
    N_ORG_BR_CCSIVAM -->|"Bauauftrag 001/CCSIVAM/99; CCSIVAM gestattete 20.12.1999 ausnahmsweise Zahlung vor vollständigen Abgabennachweisen, laut TCU2001 später nachgereicht"| N_ORG_BR_SCHAHIN_SIVAM_1999
    N_ORG_BR_UNION_SIVAM -->|"PPA-Auswertung 2004, Aktion5523 Flugzeuge: physisch 2003 abgeschlossen, offene Haushaltsverbindlichkeiten R$4,345 Mio. aus 2003, Budget 2004 R$3 Mio.; keine Auszahlung belegt"| N_PRG_BR_SIVAM
    N_PER_CL_INES_LUCIA_PINOCHET["Inés Lucía Pinochet"]
    N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004["Bank of America – Kontenverbund laut Senatsberichten 2005/2010"]
    N_PER_CL_INES_LUCIA_PINOCHET -->|"Drei US-Konten und zeitweise bis zu sechs CDs; Höchststand ca. 420.000 USD (12/2002)."| N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"300.000 USD aus Riggs-London-Scheck am 30.09.2002 auf Konto von Inés Lucía Pinochet bei Bank of America."| N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004
    N_ORG_US_PINEBANK_MIAMI["PineBank (Miami)"]
    N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004 -->|"130.000 USD über Bank-of-America-Schecks an PineBank ab 09.10.2002; keine gesicherte Identität mit dem vorherigen Riggs-Eingang."| N_ORG_US_PINEBANK_MIAMI
    N_ORG_CL_BANKBOSTON_CHILE_2001["BankBoston Chile (2001)"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Zwei Riggs-Schecks zu je 50.000 USD am 03.01. und 01.10.2001 bei BankBoston Chile eingelöst."| N_ORG_CL_BANKBOSTON_CHILE_2001
    N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004 -->|"FleetBoston-Erwerb 2004; BankBoston Chile erst dadurch dem späteren Bank-of-America-Verbund zugeordnet."| N_ORG_CL_BANKBOSTON_CHILE_2001
    N_ORG_PT_BANCO_ESPIRITO_SANTO_2005["Banco Espírito Santo (Lissabon, 2005)"]
    N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI["Espírito Santo Bank (Miami)"]
    N_ORG_PT_BANCO_ESPIRITO_SANTO_2005 -->|"Miami-Bank im Senatsbericht 2005 als Tochter von Banco Espírito Santo Lissabon bezeichnet."| N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI
    N_PER_CL_AUGUSTO_PINOCHET -->|"Mindestens sechs Konten/CDs im Pinochet-Komplex und mindestens 3,9 Mio. USD Einlagen 1991–2000 (Senatsuntersuchung)."| N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Ehemalige Mitarbeiter von Riggs International Banking Corporation (einschließlich früherem Leiter) bei Espírito Santo; Kundenvermittlung im Bericht rekonstruiert."| N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Ca. 525.000 USD aus einem Riggs-Konto eines Militärangehörigen an Espírito Santo, August 1992 bis August 1994."| N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI
    N_ORG_BS_DELOITTE_TOUCHE_1991["Deloitte & Touche (Bahamas, 1991)"]
    N_ORG_BS_DELOITTE_TOUCHE_1991 -->|"Laut Senatsbericht Vertrag über Dienstleistungen einschließlich Verwaltung der Riggs Bank & Trust Co. (Bahamas)."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Januar 1991: 1,15 Mio. USD vom Riggs-Gemeinschaftskonto Pinochets/Ehefrau über Bank of Bahamas zugunsten Deloitte & Touche."| N_ORG_BS_DELOITTE_TOUCHE_1991
    N_ORG_BS_DELOITTE_TOUCHE_1991 -->|"Oktober 1991: 1,19 Mio. USD über Deloitte & Touche zugunsten Trilateral International Trading bei Espírito Santo. Herkunftsvermutung des Senats, keine exakte Betragsidentität."| N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI
    N_ORG_US_COUTTS_INTERNATIONAL_1999["Coutts & Co. (USA) International (1999)"]
    N_ORG_US_ESPIRITO_SANTO_BANK_MIAMI -->|"Dezember 1999 ca. 2,3 Mio. USD von drei Espírito-Santo-Konten zugunsten Eastview Finance bei Coutts."| N_ORG_US_COUTTS_INTERNATIONAL_1999
    N_ORG_ES_BANCO_SANTANDER_CENTRAL_HISPANO_2004["Banco Santander Central Hispano (2004)"]
    N_ORG_ES_BANCO_SANTANDER_CENTRAL_HISPANO_2004 -->|"2003 Erwerb des betreffenden internationalen Privatbankgeschäfts von RBS; Übertragung der Konten 2004."| N_ORG_US_COUTTS_INTERNATIONAL_1999
    N_ORG_ES_BANCO_ATLANTICO_1981_2000["Banco Atlántico (1981–2000)"]
    N_ORG_ES_BANCO_ATLANTICO_1981_2000 -->|"Über 5,8 Mio. USD an Pinochet-bezogene Riggs-Konten 1981–2000; Herkunft und Endbegünstigte teilweise ungeklärt."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_OCEAN_BANK_MIAMI["Ocean Bank (Miami)"]
    N_ORG_US_CITIGROUP_2004 -->|"Mindestens fünf Überweisungen von Meritor über Cititrust Bahamas an Ocean Bank, zusammen 349.326 USD (10/2003–06/2004); Gruppenzuordnung retrospektiv."| N_ORG_US_OCEAN_BANK_MIAMI
    N_ORG_CL_BANCO_DE_CHILE_2005["Banco de Chile (einschließlich US-Niederlassung)"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"36 Riggs-Schecks über zusammen ca. 1,8 Mio. USD bei Banco de Chile in Chile eingelöst (08/2000–08/2003)."| N_ORG_CL_BANCO_DE_CHILE_2005
    N_ORG_US_FEDERAL_RESERVE -->|"Anordnung zur Verbesserung der Geldwäscheprävention, wirksam 01.02.2005."| N_ORG_CL_BANCO_DE_CHILE_2005
    N_ORG_US_FEDERAL_RESERVE -->|"Beendigung der Aufsichtsanordnung am 02.06.2008."| N_ORG_CL_BANCO_DE_CHILE_2005
    N_PER_US_ASHLEY_LEE["R. Ashley Lee"]
    N_PER_US_ASHLEY_LEE -->|"Leitender Riggs-Prüfer; am 08.08.2002 aus Prüfung zurückgezogen. Persönliche Vorwürfe strittig."| N_ORG_US_OCC
    N_PER_US_ASHLEY_LEE -->|"Wechsel aus OCC zu Riggs im Oktober 2002; OIG 2006 berichtet passenden, nicht namentlich identifizierten Ermittlungsabschluss ohne Belege für untersuchte Straftaten."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_OCC -->|"OCC erklärte am 03.06.2004, seit 1997 erkannte BSA-Mängel nicht früh genug förmlich verfolgt zu haben."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_OCC -->|"25 Mio. USD Geldbuße vom 13.05.2004, koordiniert mit FinCEN; insgesamt eine Zahlung von 25 Mio. USD."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_FINCEN["Financial Crimes Enforcement Network (FinCEN)"]
    N_ORG_US_FINCEN -->|"Koordinierte 25-Mio.-USD-Sanktion mit OCC; durch dieselbe einmalige Treasury-Zahlung zu erfüllen, nicht zusätzlich."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_DOJ -->|"US-Staatsanwalt Wainstein bat am 08.08.2004 um Einstellung bestimmter Riggs-bezogener Reviewaktivitäten; allgemeine QMD-Prüfung lief weiter."| N_ORG_US_OCC
    N_DOC_US_PL108_458_SEC6303["Public Law 108–458, Section 6303 (2004)"]
    N_DOC_US_PL108_458_SEC6303 -->|"Befristete Beschäftigungsbeschränkung für bestimmte leitende Prüfer, wirksam zwölf Monate nach Erlass; keine Rückwirkung auf Lee."| N_ORG_US_OCC
    N_ORG_US_RIGGS_NATIONAL_CORPORATION["Riggs National Corporation"]
    N_ORG_US_RIGGS_NATIONAL_CORPORATION -->|"Riggs Bank als Tochtergesellschaft der Riggs National Corporation im Untersuchungszeitraum."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_PER_US_ROBERT_ALLBRITTON["Robert Allbritton"]
    N_PER_US_ROBERT_ALLBRITTON -->|"CEO und Chairman der Holding bis Rücktritt 07.03.2005."| N_ORG_US_RIGGS_NATIONAL_CORPORATION
    N_PER_US_ROBERT_ALLBRITTON -->|"Chairman von Riggs Bank; Rücktritt 07.03.2005."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_PER_US_LAWRENCE_I_HEBERT["Lawrence I. Hebert"]
    N_PER_US_LAWRENCE_I_HEBERT -->|"Bankpräsident und CEO seit Februar 2001; SEC-Mitteilung vom 11.03.2005 nennt ihn weiterhin in dieser Funktion. Ausscheidensdatum nicht belegt."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_ALLBRITTON_COMMUNICATIONS_2004["Allbritton Communications Company (2004)"]
    N_PER_US_LAWRENCE_I_HEBERT -->|"Weitere Leitungsfunktionen bei Allbritton Communications bis Oktober 2004, parallel zur Bankleitung."| N_ORG_US_ALLBRITTON_COMMUNICATIONS_2004
    N_ORG_US_PERPETUAL_CORPORATION_2004["Perpetual Corporation (2004)"]
    N_PER_US_LAWRENCE_I_HEBERT -->|"Präsident der ACC-Mutter Perpetual Corporation 1981–10/2004."| N_ORG_US_PERPETUAL_CORPORATION_2004
    N_ORG_US_PERPETUAL_CORPORATION_2004 -->|"Perpetual Corporation in SEC-Meldung als Muttergesellschaft von ACC bezeichnet."| N_ORG_US_ALLBRITTON_COMMUNICATIONS_2004
    N_ORG_US_ALLBRITTON_COMMUNICATIONS_2004 -->|"506.160 USD 2004 für Büroräume, Veranstaltungslogen und Kontodienstleistungen, nach SEC-8-K; keine redaktionelle Weisung belegt."| N_ORG_US_RIGGS_NATIONAL_CORPORATION
    N_PER_US_STEVEN_B_PFEIFFER["Steven B. Pfeiffer"]
    N_PER_US_STEVEN_B_PFEIFFER -->|"Direktor der Riggs-Holding laut Senatsbericht 2004 seit 1989."| N_ORG_US_RIGGS_NATIONAL_CORPORATION
    N_ORG_US_FULBRIGHT_JAWORSKI_2004["Fulbright & Jaworski (2004)"]
    N_PER_US_STEVEN_B_PFEIFFER -->|"Gleichzeitig Partner von Fulbright & Jaworski laut Senatsbericht 2004."| N_ORG_US_FULBRIGHT_JAWORSKI_2004
    N_ORG_US_FULBRIGHT_JAWORSKI_2004 -->|"Rechtsdienstleistungen für Riggs laut Senatsbericht 2004, keine strafrechtliche Mitwirkung allein daraus."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_GQ_GOVERNMENT_1995_2004["Regierung Äquatorialguineas (1995–2004)"]
    N_ORG_GQ_GOVERNMENT_1995_2004 -->|"Seit 1995 staatliche und amtsträgerbezogene Konten; mehr als 60 Konten/CDs einschließlich Angehöriger, zeitweise 400–700 Mio. USD Einlagen 2003 im Gesamtkomplex."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_GQ_KALUNGA_COMPANY_SA["Kalunga Company S.A."]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"16 Überweisungen aus staatlichem Öleinnahmenkonto, 26.483.982,57 USD (06/2000–12/2003), laut Senatstabelle."| N_ORG_GQ_KALUNGA_COMPANY_SA
    N_ORG_GQ_KALUNGA_COMPANY_SA -->|"Empfängerkonto der 16 Öleinnahmentransfers bei Santander Madrid; Endbegünstigung ungeklärt."| N_ORG_ES_BANCO_SANTANDER_CENTRAL_HISPANO_2004
    N_ORG_INT_APEXSIDE_TRADING_LTD["Apexside Trading Ltd."]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"10 Überweisungen aus Öleinnahmenkonto, 8.105.491,94 USD (2000–2001); neun CCF Luxemburg, eine HSBC Luxemburg."| N_ORG_INT_APEXSIDE_TRADING_LTD
    N_ORG_LU_CREDIT_COMMERCIAL_DE_FRANCE_2000["Crédit Commercial de France (Luxemburg, 2000–2001)"]
    N_ORG_INT_APEXSIDE_TRADING_LTD -->|"Empfängerkonto für neun der zehn Apexside-Überweisungen; Einzelbetrag nicht gesichert."| N_ORG_LU_CREDIT_COMMERCIAL_DE_FRANCE_2000
    N_ORG_LU_HSBC_LUXEMBOURG_2001["HSBC (Luxemburg, 2001)"]
    N_ORG_INT_APEXSIDE_TRADING_LTD -->|"Empfängerkonto für eine der zehn Apexside-Überweisungen; Einzelbetrag nicht gesichert."| N_ORG_LU_HSBC_LUXEMBOURG_2001
    N_ORG_INT_JADINI_HOLDINGS["Jadini Holdings Ltd."]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"Drei Überweisungen 2001–2002 über insgesamt 1.096.677,78 USD; Kontrolle durch Ehefrau des Riggs-Kundenbetreuers laut Bericht."| N_ORG_INT_JADINI_HOLDINGS
    N_PER_GQ_MELCHOR_ESONO_EDJO["Melchor Esono Edjo"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"499.000 USD an persönliche Konten des damaligen Staatssekretärs 1998–2002 laut Senatsbericht."| N_PER_GQ_MELCHOR_ESONO_EDJO
    N_PER_GQ_TEODORO_OBIANG["Teodoro Obiang Nguema Mbasogo"]
    N_ORG_GQ_ABAYAK_SA["Abayak S.A. (1998–2004)"]
    N_PER_GQ_TEODORO_OBIANG -->|"Kontrolle der Abayak S.A. durch den Präsidenten laut Senatsuntersuchung; vollständige Eigentümerakte offen."| N_ORG_GQ_ABAYAK_SA
    N_ORG_GQ_MOBIL_EQUATORIAL_GUINEA_INC["Mobil Equatorial Guinea Inc. (MEGI)"]
    N_PER_GQ_CONSTANCIA_MANGUE["Constancia Mangue Nsue de Obiang"]
    N_ORG_GQ_MOBIL_EQUATORIAL_GUINEA_INC -->|"Mietverträge 1996–2001 mit Präsidentengattin, im Bericht dokumentierte Einzelzahlungen auf Riggs-Konto."| N_PER_GQ_CONSTANCIA_MANGUE
    N_PER_GQ_CONSTANCIA_MANGUE -->|"Empfang von MEGI-Mietzahlungen auf historisches Riggs-Konto laut Bankunterlagen in Fn. 341."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_GQ_MOBIL_EQUATORIAL_GUINEA_INC -->|"Ab 22.06.2001 Wechsel der Vermieterin von Präsidentengattin zu Abayak S.A."| N_ORG_GQ_ABAYAK_SA
    N_ORG_US_MOBIL_INTERNATIONAL_PETROLEUM["Mobil International Petroleum Corporation (1998)"]
    N_ORG_GQ_MOGE_JOINT_VENTURE["MOGE (Gemeinschaftsunternehmen, 1998)"]
    N_ORG_US_MOBIL_INTERNATIONAL_PETROLEUM -->|"85-%-Beteiligung nach ExxonMobil-Unternehmensantwort im Senatsbericht."| N_ORG_GQ_MOGE_JOINT_VENTURE
    N_ORG_GQ_ABAYAK_SA -->|"15-%-Beteiligung nach ExxonMobil-Unternehmensantwort im Senatsbericht."| N_ORG_GQ_MOGE_JOINT_VENTURE
    N_ORG_GQ_MOGE_JOINT_VENTURE -->|"Ca. 10.500 USD Dividende jährlich 2001–2003 nach Unternehmensantwort."| N_ORG_GQ_ABAYAK_SA
    N_PER_GQ_ARMENGOL_ONDO_NGUEMA["Armengol Ondo Nguema"]
    N_ORG_GQ_SONAVI["Sonavi (Sicherheitsdienst)"]
    N_PER_GQ_ARMENGOL_ONDO_NGUEMA -->|"Sicherheitsgesellschaft im Eigentum des Präsidentenbruders laut Senatsbericht."| N_ORG_GQ_SONAVI
    N_ORG_US_AMERADA_HESS_2004["Amerada Hess (Unternehmensverbund, 2004)"]
    N_ORG_US_AMERADA_HESS_2004 -->|"Ca. 300.500 USD Sicherheitsdienstzahlungen Januar 2000 bis Mai 2004; Hess verwies auf vorgegebene Konditionen."| N_ORG_GQ_SONAVI
    N_ORG_US_EXXONMOBIL_REPORT_2004["ExxonMobil (berichteter Unternehmensverbund 2004)"]
    N_ORG_US_EXXONMOBIL_REPORT_2004 -->|"Zwei getrennte Einheiten: 683.900 USD (08/1997–10/2000) und ca. 26.400 USD (2000–2003); marktübliche Vergütung laut Unternehmensantwort."| N_ORG_GQ_SONAVI
    N_ORG_US_MARATHON_OIL_2004["Marathon Oil (2004)"]
    N_ORG_US_MARATHON_OIL_2004 -->|"Über 611.000 USD Landkaufpreis im Januar 2004 über Abayak an Präsidenten; weiterer ca. 1,4-Mio.-Kauf noch nicht vollzogen (18.06.2004)."| N_ORG_GQ_ABAYAK_SA
    N_ORG_GQ_AMPCO_METHANOL["Atlantic Methanol Production Company (AMPCO)"]
    N_ORG_US_MARATHON_OIL_2004 -->|"45-%-Anteil an Methanol-Gemeinschaftsunternehmen laut Senatsbericht."| N_ORG_GQ_AMPCO_METHANOL
    N_ORG_GQ_GEOGAM["GEOGAM (2004)"]
    N_ORG_GQ_GEOGAM -->|"10-%-Anteil; eigene GEOGAM-Eigentümerstruktur bleibt ungeklärt."| N_ORG_GQ_AMPCO_METHANOL
    N_ORG_GQ_AMPCO_METHANOL -->|"Mehr als 4 Mio. USD Dividenden 2002 bis Mai 2004; keine gesicherte Zurechnung an Präsidentenfamilie."| N_ORG_GQ_GEOGAM
    N_ORG_GQ_ATSIGE["ATSIGE (2000–2004)"]
    N_ORG_GQ_MOGE_JOINT_VENTURE -->|"236.160 USD 2000 bis Mai 2004 an Gesellschaft des Innenministers laut Senatsbericht."| N_ORG_GQ_ATSIGE
    N_PER_US_LAWRENCE_I_HEBERT -->|"Holding-Verwaltungsrat ernannte Hebert am 09.03.2005 zum CEO der Riggs National Corporation, vorbehaltlich der erforderlichen Aufsichtsgenehmigungen; Wirksamkeit nicht durch diese Quelle belegt."| N_ORG_US_RIGGS_NATIONAL_CORPORATION
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE["Teodoro Nguema Obiang Mangue"]
    N_ORG_GQ_SOMAGUI_FORESTAL["Somagui Forestal (historischer Untersuchungszeitraum)"]
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"PSI bezeichnet Somagui als Obiang-Gesellschaft; Urteil Rn.32 bestätigt maßgeblichen Entscheidungseinfluss im historischen Zeitraum."| N_ORG_GQ_SOMAGUI_FORESTAL
    N_ORG_GQ_SOCAGE["Socage (historischer Untersuchungszeitraum)"]
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"PSI bezeichnet Socage als Obiang-Gesellschaft; Urteil Rn.30–32 zur Nutzung von Gesellschaftsmitteln."| N_ORG_GQ_SOCAGE
    N_ORG_GQ_CCEI_BANK_2003_2008["CCEI Bank GE (2003–2008)"]
    N_ORG_GQ_SOMAGUI_FORESTAL -->|"Vier Riggs-Zahlungsaufträge 2003–2004 über CCEI GE, zusammen 3,8 Mio. USD; Teil des gleichen 4,8-Mio.-Transferkomplexes."| N_ORG_GQ_CCEI_BANK_2003_2008
    N_ORG_GQ_SOCAGE -->|"Ein Riggs-Zahlungsauftrag über CCEI GE, 1 Mio. USD am 09.03.2004; Teil derselben fünf Transfers."| N_ORG_GQ_CCEI_BANK_2003_2008
    N_ORG_GQ_CCEI_BANK_2003_2008 -->|"Fünf ausgewiesene Riggs-Überweisungen 2003–04, 4,8 Mio. USD via Citibank; kein zusätzlicher Mittelzufluss pro Zwischenstation."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971 -->|"Dieselben fünf Überweisungen 4,8 Mio. USD an Obiang-bezogene Riggs-Konten, Quelle Citigroup-Tabelle S.102. Fn.563 widerspricht beim Jahr einer Zeile."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"PSI2010 dokumentiert Riggs-Konten des Präsidentensohns u.a. 2001 und 2003–04; getrennt vom Vater und staatlichem Öleinnahmenkonto."| N_ORG_US_RIGGS_NATIONAL_BANK
    N_ORG_US_SIDLEY_AUSTIN_2006["Sidley Austin (2006)"]
    N_ORG_US_SIDLEY_AUSTIN_2006 -->|"Rücküberweisung 19.570.635,18 USD am 24.01.2006 über Citibank, nach im PSI referierter damaliger DOJ-Bestätigung fehlender Sperrgrundlage."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_ORG_US_SOCIETE_GENERALE_NY_2006["Société Générale S.A. (New York, 2006)"]
    N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971 -->|"Zwischenstation derselben Rücküberweisung 19.570.635,18 USD; kein zusätzlicher Zufluss."| N_ORG_US_SOCIETE_GENERALE_NY_2006
    N_ORG_GQ_SOCIETE_GENERALE_DE_BANQUE_2006["Société Générale de Banque – Äquatorialguinea (2006)"]
    N_ORG_US_SOCIETE_GENERALE_NY_2006 -->|"Weiterleitung derselben Rücküberweisung nach EG laut Tabelle S.103."| N_ORG_GQ_SOCIETE_GENERALE_DE_BANQUE_2006
    N_ORG_GQ_SOCIETE_GENERALE_DE_BANQUE_2006 -->|"Empfängerkonto der Rücküberweisung und Ausgangskonto der späteren 14 Überweisungen 2006 laut PSI, keine Mittelidentität allein daraus."| N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE
    N_ORG_US_BEVERLY_HILLS_ESCROW_2001["Beverly Hills Escrow (2001)"]
    N_ORG_US_RIGGS_NATIONAL_BANK -->|"2001 6,2 Mio. USD aus Konto des Präsidentensohns bei Riggs an Beverly Hills Escrow bei UBOC (Bankrückschau 2004)."| N_ORG_US_BEVERLY_HILLS_ESCROW_2001
    N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007["Union Bank of California, N.A. (UBOC)"]
    N_ORG_US_BEVERLY_HILLS_ESCROW_2001 -->|"Empfängerkonto der 6,2-Mio.-USD-Überweisung, kein zweiter Mittelzufluss."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_CM_BEAC_2006["Banque des États de l’Afrique Centrale (BEAC, 2006)"]
    N_ORG_GQ_SOCIETE_GENERALE_DE_BANQUE_2006 -->|"14 Zahlungsaufträge April–Juni 2006 über BEAC/Banque de France/Wachovia; Summe der Textzeilen 73.641.999,99 USD (Fn.553 bestätigt gruppierte Summe)."| N_ORG_CM_BEAC_2006
    N_ORG_FR_BANQUE_DE_FRANCE_2006["Banque de France (2006)"]
    N_ORG_CM_BEAC_2006 -->|"Dieselben 14 Zahlungsaufträge 2006 über Banque de France, kein eigenständiges Zahlungsaggregat."| N_ORG_FR_BANQUE_DE_FRANCE_2006
    N_ORG_US_WACHOVIA_BANK_2006["Wachovia Bank, N.A. (historischer Untersuchungszeitraum)"]
    N_ORG_FR_BANQUE_DE_FRANCE_2006 -->|"Korrespondenzbankweg derselben 14 Zahlungsaufträge; keine Addition der wiederholten Streckenbeträge."| N_ORG_US_WACHOVIA_BANK_2006
    N_ORG_US_MCAFEE_TAFT_2006["McAfee & Taft (2006)"]
    N_ORG_US_WACHOVIA_BANK_2006 -->|"Drei ausgewiesene Zahlungen 05./10.04.2006 an Kanzleikonto bei Bank of America, Textzeilensumme 10,3 Mio. USD."| N_ORG_US_MCAFEE_TAFT_2006
    N_ORG_US_MCAFEE_TAFT_2006 -->|"Empfängerkonto der drei 2006er Treuhandzahlungen laut PSI; keine zusätzlichen Beträge."| N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004
    N_ORG_US_FIRST_AMERICAN_TITLE_2006["First American Title Company (2006)"]
    N_ORG_US_WACHOVIA_BANK_2006 -->|"Fünf Zahlungen April 2006 je 5.908.400 USD, zusammen 29.542.000 USD laut Tabelle und Fn.553; Immobilienerwerb."| N_ORG_US_FIRST_AMERICAN_TITLE_2006
    N_ORG_US_FIRST_AMERICAN_TRUST_2006["First American Trust, F.S.B. (2006)"]
    N_ORG_US_FIRST_AMERICAN_TITLE_2006 -->|"Empfängerkonto der fünf Immobilienzahlungen laut PSI-Tabelle."| N_ORG_US_FIRST_AMERICAN_TRUST_2006
    N_ORG_INT_INSURED_AIRCRAFT_TITLE_SERVICE_2006["Insured Aircraft Title Service(s) (2006)"]
    N_ORG_US_WACHOVIA_BANK_2006 -->|"Sechs Zeilen Mai–Juni 2006, Summe 33.799.999,99 USD an Flugzeug-Titeldienstleister bei UBS London. Vor endgültiger Mittelabrechnung keine zusätzliche Eigentumsbehauptung."| N_ORG_INT_INSURED_AIRCRAFT_TITLE_SERVICE_2006
    N_ORG_GB_UBS_LONDON_2006["UBS London (2006)"]
    N_ORG_INT_INSURED_AIRCRAFT_TITLE_SERVICE_2006 -->|"Empfängerkonto der sechs in PSI-Tabelle ausgewiesenen Zahlungen bei UBS London."| N_ORG_GB_UBS_LONDON_2006
    N_ORG_INT_FORTIS_BANK_2008["Fortis Bank (in PSI-Tabelle 2008)"]
    N_ORG_GQ_CCEI_BANK_2003_2008 -->|"Zwei weitere Überweisungen 2008 (144.017,99 und 1.458,51 USD) über Fortis an Wachovia, getrennt vom 2006er Komplex."| N_ORG_INT_FORTIS_BANK_2008
    N_ORG_INT_FORTIS_BANK_2008 -->|"Dieselben zwei 2008er Überweisungen, Summe 145.476,50 USD; nicht additiv zur vorigen Kante."| N_ORG_US_WACHOVIA_BANK_2006
    N_ORG_US_BERGER_LAW_OFFICE_2004_2007["Kanzlei Michael Berger (2004–2007)"]
    N_ORG_US_BERGER_LAW_OFFICE_2004_2007 -->|"Historische anwaltliche Treuhandkonten und Zahlungsabwicklung für Obiang, dokumentiert 2004–07; kein Strafurteil gegen Anwalt."| N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004
    N_ORG_US_BEAUTIFUL_VISION_INC_2004["Beautiful Vision, Inc. (2004–2005)"]
    N_ORG_US_BEAUTIFUL_VISION_INC_2004 -->|"Beautiful-Vision-Konten ab 19.10.2004; ausgewiesene größere Einzahlungen zusammen 9.729.321,28 USD, darunter interne Umbuchungen und Immobilienerlöse; Schließungen 2005."| N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"Sole signatory eines Beautiful-Vision-Kontos laut PSI; Bank schloss Konten wegen seiner Verbindung. Vollständige Registerakte offen."| N_ORG_US_BEAUTIFUL_VISION_INC_2004
    N_ORG_US_BERGER_LAW_OFFICE_2004_2007 -->|"Treuhandkonto mit acht EG-Überweisungen ab 24.11.2006 bis 06.06.2007, >1,7 Mio. USD aus Somagui/Obiang laut PSI; kein weiteres Summieren mit Ausgängen."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_US_UNLIMITED_HORIZON_INC_2006["Unlimited Horizon, Inc. (2006–2007)"]
    N_ORG_US_UNLIMITED_HORIZON_INC_2006 -->|"Unlimited-Horizon-Konten ab 2006, Weiterleitungen vom Kanzleikonto; PSI rekonstruiert Schließung 12.06.2007."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_US_UNLIMITED_HORIZON_INC_2006 -->|"Spätere Unlimited-Horizon-Konten; 26.07.2007 dokumentierte Weiterzahlung 199.948,82 USD aus Berger-Konto bei BofA nach Socage-Eingang."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004 -->|"23.10.2006 Weiterleitung 199.931,17 USD aus Berger-Treuhandkonto an Unlimited Horizon bei UBOC; Eingangs-/Gebühren- und E-Mail-Angaben abweichend."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_US_BOFA_ACCOUNT_GROUP_1993_2004 -->|"26.07.2007 Weiterleitung des Socage-Eingangs 199.948,82 USD an Unlimited Horizon/Citibank; dieselbe Zahlung wie Kontenbeleg, nicht additiv."| N_ORG_US_FIRST_NATIONAL_CITY_BANK_1971
    N_ORG_US_UNIONBANCAL_2007["UnionBanCal Corporation (2007)"]
    N_ORG_US_UNIONBANCAL_2007 -->|"UBOC als vollständig im Eigentum von UnionBanCal laut FinCEN 2007-02 §II."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_JP_MUFG_2007["Mitsubishi UFJ Financial Group (2007)"]
    N_ORG_JP_MUFG_2007 -->|"UnionBanCal mehrheitlich im Eigentum von MUFG laut FinCEN §II; keine Kenntniszurechnung."| N_ORG_US_UNIONBANCAL_2007
    N_ORG_US_DOJ -->|"DPA 17.09.2007, 21,6 Mio. USD vereinbarter Verfall, mexikanischer Wechselhauskomplex; kein Obiang-Strafurteil."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_US_OCC -->|"Parallele OCC-/FinCEN-Bußen durch eine 10-Mio.-USD-Zahlung an OCC zu erfüllen; nicht doppelt zählen."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_US_FINCEN -->|"Koordinierte 10-Mio.-USD-Buße, dieselbe Zahlung an OCC, nicht zusätzliche 10 Mio.; Consent ohne Anerkennung außer Zuständigkeit."| N_ORG_US_UNION_BANK_OF_CALIFORNIA_2007
    N_ORG_US_DOJ -->|"DPA gerichtlich angenommen 17.03.2010; 110 Mio. USD Verfall und 50 Mio. zusätzliche OCC-Buße. Wechselhäuser/Zahlungsdienstleister, nicht Obiang zugerechnet."| N_ORG_US_WACHOVIA_BANK_2006
    N_ORG_US_FINCEN -->|"110 Mio. USD FinCEN-Buße durch denselben Verfall erfüllt, nicht zusätzlich zu 160 Mio. Gesamtvereinbarung."| N_ORG_US_WACHOVIA_BANK_2006
    N_ORG_US_OCC -->|"Zusätzliche 50 Mio. USD im DPA-/OCC-Komplex 2010."| N_ORG_US_WACHOVIA_BANK_2006
    N_ORG_GQ_EDUM["Edum (historischer Untersuchungszeitraum)"]
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"Gerichtsentscheidung vom 28.07.2021 zur früheren Tätigkeit: Urteil 2021 Rn.30–32: Nutzung und Entscheidungseinfluss über Gesellschaftsmittel; alternative Vertrauensmissbrauchsqualifikation 350.037 EUR."| N_ORG_GQ_EDUM
    N_ORG_INT_FOCH_SERVICES_HISTORICAL["Foch services (historischer Rechtsträger laut Urteil)"]
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"Gerichtsentscheidung vom 28.07.2021 zur früheren Tätigkeit: Urteil Rn.30–31: tatsächliche Leitung der Abschirmgesellschaft durch Angeklagten; keine aus Quelle bewiesene Gründungs-/Registergeschichte."| N_ORG_INT_FOCH_SERVICES_HISTORICAL
    N_ORG_GQ_SOMAGUI_FORESTAL -->|"Gerichtsentscheidung vom 28.07.2021 zur früheren Tätigkeit: Rn.31: Foch services laut Berufungsfeststellung Abschirmgesellschaft und Somagui einzige Finanzierungsquelle; keine konkrete US-Transferidentität."| N_ORG_INT_FOCH_SERVICES_HISTORICAL
    N_ORG_FR_COUR_DE_CASSATION["Cour de cassation (Frankreich)"]
    N_ORG_FR_COUR_DE_CASSATION -->|"Kassationsbeschwerde am 28.07.2021 zurückgewiesen; Geldwäscheverurteilung und Einziehung bestätigt; Teilfreispruch für Geldwäsche aus Korruption ausdrücklich erhalten."| N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE
    N_ORG_INT_INTERNATIONAL_COURT_OF_JUSTICE["Internationaler Gerichtshof (IGH)"]
    N_DOC_INT_ICJ_163_2020["IGH-Urteil 163 zum diplomatischen Status (11.12.2020)"]
    N_ORG_INT_INTERNATIONAL_COURT_OF_JUSTICE -->|"Urteil vom 11.12.2020: umstrittenes Pariser Gebäude erwarb keinen Status diplomatischer Missionsräume; keine Verletzung der Wiener Konvention festgestellt."| N_DOC_INT_ICJ_163_2020
    N_DOC_US_OBIANG_CIVIL_SETTLEMENT_2014["US-Zivilvergleich Obiang Mangue vom 10.10.2014"]
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"Zivilvergleich 10.10.2014 über Verwertung bestimmter Vermögenswerte und Beitrag 1 Mio. USD; Verpflichtung nicht mit Erfüllung gleichsetzen."| N_DOC_US_OBIANG_CIVIL_SETTLEMENT_2014
    N_ORG_US_SWEETWATER_MALIBU_LLC["Sweetwater Malibu LLC"]
    N_ORG_US_SWEETWATER_MALIBU_LLC -->|"Vergleichspartei und von Parteien bezeichnete eingetragene Immobilieneigentümerin, §§2–6; keine Identität mit älterem Immobilienvorgang."| N_DOC_US_OBIANG_CIVIL_SETTLEMENT_2014
    N_ORG_US_DOJ -->|"US-Seite: §27 Verfall 10,3 Mio. USD nach Verwertungskosten, Rest zugunsten Bevölkerung, §28 weiterer Beitrag und Verwertung; §30 Rechnungslegung."| N_DOC_US_OBIANG_CIVIL_SETTLEMENT_2014
    N_ORG_INT_UNITED_NATIONS_2021["Vereinte Nationen (Zuwendungsvereinbarung 2021)"]
    N_ORG_US_DOJ -->|"Ankündigung vom 20.09.2021: Zuwendungsvereinbarung 19,25 Mio. USD für Impfprogramm in EG. Tatsächliche Einzahlungen getrennt in REL-RIGGS-POST-2004-054; nicht additiv."| N_ORG_INT_UNITED_NATIONS_2021
    N_ORG_US_MCDI_GLOBAL_HEALTH["Medical Care Development International / MCD Global Health"]
    N_ORG_US_DOJ -->|"Ankündigung 20.09.2021: Vereinbarung über 6,35 Mio. USD für Medikamente und medizinischen Bedarf; spätere Berichte, kein vollständiger Zahlungs-/Ausgabennachweis."| N_ORG_US_MCDI_GLOBAL_HEALTH
    N_PRG_GQ_GOOD_WILL_FUND_2021_2025["Good Will Fund (Äquatorialguinea, 2021–2025)"]
    N_ORG_US_MCDI_GLOBAL_HEALTH -->|"MCD berichtet Good Will Fund 2021–2025, medizinische Lieferungen und Aufbau der Logistik in 19 Distrikten; Eigenauskunft."| N_PRG_GQ_GOOD_WILL_FUND_2021_2025
    N_DOC_INT_ICJ_163_2020 -->|"Der zwischenstaatliche Immunitätsstreit betraf die Immobilie im Zusammenhang mit französischen Ermittlungen gegen den Präsidentensohn; keine Strafverurteilung durch den IGH."| N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE
    N_PER_GQ_TEODORO_NGUEMA_OBIANG_MANGUE -->|"Sohn des Präsidenten Teodoro Obiang Nguema Mbasogo; Verwandtschaft belegt, keine Zurechnung der jeweiligen Geldströme oder Delikte."| N_PER_GQ_TEODORO_OBIANG
    N_ORG_US_FEDERAL_GOVERNMENT["Regierung der Vereinigten Staaten"]
    N_PRG_GQ_MPTF_GNQ00["Equatorial Guinea Multi-Partner Trust Fund (GNQ00)"]
    N_ORG_US_FEDERAL_GOVERNMENT -->|"10 Mio. USD Einzahlung 2021 und 9,225 Mio. USD 2023; kumuliert 19,225 Mio. USD bis 2025. Nicht additiv zur DOJ-Zusage 19,25 Mio.; Differenz 25.000 USD ungeklärt."| N_PRG_GQ_MPTF_GNQ00
    N_ORG_INT_UNDP["United Nations Development Programme (UNDP)"]
    N_PRG_GQ_MPTF_GNQ00 -->|"7.632.981 USD Nettofinanzierung bis 31.12.2025, davon gemeldete Ausgaben 4.670.867 USD; Programm 00129191."| N_ORG_INT_UNDP
    N_ORG_INT_UNICEF["United Nations Children's Fund (UNICEF)"]
    N_PRG_GQ_MPTF_GNQ00 -->|"7.746.761 USD Nettofinanzierung bis 31.12.2025, davon gemeldete Ausgaben 4.356.419 USD; Programm 00129191."| N_ORG_INT_UNICEF
    N_ORG_INT_WHO["World Health Organization (WHO)"]
    N_PRG_GQ_MPTF_GNQ00 -->|"8.190.430 USD Bruttoübertragungen, 4.560.042 USD Rückzahlungen an Fonds, netto 3.630.388 USD bis 31.12.2025; gemeldete Ausgaben 3.630.387 USD."| N_ORG_INT_WHO
    N_ORG_US_DOJ -->|"Terms of Reference August 2021 und Revision Dezember 2025: DOJ formales Mitglied des Lenkungsausschusses des Impf-Fensters; EG-Regierungsvertreter beratend ohne Stimmrecht. Keine Aussage zur tatsächlichen Besetzung oder zu einzelnen Beschlüssen."| N_PRG_GQ_MPTF_GNQ00
    N_ORG_INT_UNDP -->|"UNDP MPTF Office verwaltet Fonds, erhält Einzahlungen und überträgt Mittel nach Ausschussbeschlüssen; 1% Verwaltungsgebühr. Von UNDP als programmumsetzender Organisation unterscheiden."| N_PRG_GQ_MPTF_GNQ00
    N_ORG_DE_INSM["Initiative Neue Soziale Marktwirtschaft (INSM)"]
    N_ORG_DE_HS_2002["H.+S. Unternehmensberatung (München, 2002)"]
    N_ORG_DE_INSM -->|"DRPR dokumentiert Beauftragung der H.+S. mit bezahlten Marienhof-Themenplatzierungen 2002; laut INSM nach wenigen Monaten beendet."| N_ORG_DE_HS_2002
    N_ORG_DE_HS_2002 -->|"H.+S. legte der INSM vor der Platzierung Themenvorschläge und Treatments zur Abstimmung vor; kein Nachweis der Mitwirkung anderer Netzwerke."| N_ORG_DE_INSM
    N_ORG_DE_KW_2002["Kultur + Werbung (K+W, 2002–2005)"]
    N_ORG_DE_HS_2002 -->|"DRPR nennt K+W als Schwesterfirma der H.+S.; genaue Eigentumsquoten nicht ausgewiesen."| N_ORG_DE_KW_2002
    N_ORG_DE_BAVARIA_SONOR_2005["Bavaria Sonor (Placement-Abwicklung 2002–2005)"]
    N_ORG_DE_KW_2002 -->|"Laut DRPR leitete H.+S. über K+W insgesamt 58.670,14 EUR an Bavaria Sonor weiter; ein einziger berichteter Gesamtbetrag, keine unabhängigen Kontoauszüge."| N_ORG_DE_BAVARIA_SONOR_2005
    N_PRG_DE_MARIENHOF_2002["ARD-Serie Marienhof (Placement-Untersuchung 2002–2005)"]
    N_ORG_DE_INSM -->|"INSM räumte acht bezahlte Themenplatzierungen 2002 ein, Clearingstelle nennt sieben. DRPR stellt unzulässige verdeckte Werbung fest; keine politische Wirkungsmessung."| N_PRG_DE_MARIENHOF_2002
    N_ORG_DE_DRPR -->|"Öffentliche Rüge vom 09.05.2006; DRPR würdigt zugleich Aufklärungskooperation und Distanzierung. Keine strafgerichtliche Verurteilung."| N_ORG_DE_INSM
    N_ORG_DE_BAVARIA_FILM_2005["Bavaria Film GmbH (2005)"]
    N_ORG_DE_BAVARIA_FILM_2005 -->|"Bavaria beschreibt ARD-Auftragsproduktionen und vertragliche Trennung von Werbung und Programm; keine pauschale Kenntnis der ARD von Placements."| N_ORG_DE_ARD
    N_ORG_DE_BAVARIA_FILM_2005 -->|"Bavaria veröffentlichte Sonderprüfbefunde: 19 Verträge, 117 realisierte und 76 nicht realisierte Placements bei Marienhof. Alle Auftraggeber, nicht allein INSM."| N_PRG_DE_MARIENHOF_2002
    N_ORG_DE_BAVARIA_SONOR_2005 -->|"Bavaria-Prüfauszug nennt Sonor als Abwicklungsstelle von Placement-Verträgen und Rechnungen. Prüfung beschreibt nicht erkennbare Leistungsart im Buchungssystem; kein Strafurteil."| N_PRG_DE_MARIENHOF_2002
    N_ORG_DE_BR["Bayerischer Rundfunk"]
    N_ORG_DE_BR -->|"Bavaria nennt BR-Vorabendredaktion als abnehmende Redaktion. Prüfauszug entlastet sie hinsichtlich Erkennbarkeit integrierter Themen; keine bewusste Kollaboration festgestellt."| N_PRG_DE_MARIENHOF_2002
    N_ORG_DE_WDR["Westdeutscher Rundfunk"]
    N_ORG_DE_WDR -->|"Bavaria-Erklärung vom 01.07.2005 nennt WDR unter den Gesellschaftern; genaue Quote und Kenntnis von einzelnen Placements daraus nicht ableitbar."| N_ORG_DE_BAVARIA_FILM_2005
    N_ORG_DE_MDR["Mitteldeutscher Rundfunk"]
    N_ORG_DE_MDR -->|"Bavaria-Erklärung vom 01.07.2005 nennt MDR unter den Gesellschaftern; genaue Quote und Kenntnis von einzelnen Placements daraus nicht ableitbar."| N_ORG_DE_BAVARIA_FILM_2005
    N_ORG_DE_SWR["Südwestrundfunk"]
    N_ORG_DE_SWR -->|"Bavaria-Erklärung vom 01.07.2005 nennt SWR unter den Gesellschaftern; genaue Quote und Kenntnis von einzelnen Placements daraus nicht ableitbar."| N_ORG_DE_BAVARIA_FILM_2005
    N_ORG_DE_BR -->|"Bavaria-Erklärung vom 01.07.2005 nennt BR unter den Gesellschaftern; genaue Quote und Kenntnis von einzelnen Placements daraus nicht ableitbar."| N_ORG_DE_BAVARIA_FILM_2005
    N_ORG_DE_SWR -->|"SWR-Revision untersuchte laut Bavaria 2005 die Schnittstelle von abnehmenden Redaktionen und Auftragsproduktion; veröffentlichter Prüfauszug, nicht vollständige Akte."| N_ORG_DE_BAVARIA_FILM_2005
    N_PER_DE_GERHARD_WESSEL["Gerhard Wessel"]
    N_PER_DE_ROLF_KAUKA["Rolf Kauka"]
    N_PER_DE_GERHARD_WESSEL -->|"BND bestätigte enges persönliches Verhältnis zwischen Wessel und Kauka; im Beschluss 6 A 9.19 amtlich protokolliert. Keine festgestellte Agentenrolle."| N_PER_DE_ROLF_KAUKA
    N_PER_DE_GERHARD_WESSEL -->|"In 6 A 9.19 als späterer BND-Präsident bezeichnet; keine Datierung seiner Amtszeit aus diesem Beschluss."| N_ORG_DE_BND
    N_PER_DE_GERHARD_WESSEL -->|"Spionagemuseum berichtet unter Bezug auf Hechelhammer über durch Wessels Kontakte vermittelte Ausbildungsfilmaufträge Mitte der 1950er Jahre. Originalverträge und Beträge fehlen."| N_PER_DE_ROLF_KAUKA
    N_ORG_DE_BUNDESWEHR -->|"Bericht des Spionagemuseums über Ausbildungsfilmaufträge an Kauka Mitte der 1950er Jahre. Kein unabhängig belegter Geldfluss und keine Aussage zu Comicfinanzierung."| N_PER_DE_ROLF_KAUKA
    N_PER_DE_ROLF_KAUKA -->|"Bundesarchiv nennt eine mögliche Informantentätigkeit ab 1950 unter der Bezeichnung BND; wegen der institutionellen Chronologie ist die Zuordnung zur Vorgängerorganisation eine Recherchehypothese. Keine eingesehene Quellenverpflichtung."| N_ORG_DE_ORGANISATION_GEHLEN
    N_DOC_DE_KAUKA_BND_AKTENKOMPLEX["BND-Aktenkomplex Kauka-Verlag"]
    N_ORG_DE_BND -->|"Bescheid vom 01.04.2019 gewährte Teilzugang mit Schwärzungen, lehnte weiteren Zugang ab; Urteil 10 A 1.24, Rn. 2."| N_DOC_DE_KAUKA_BND_AKTENKOMPLEX
    N_ORG_DE_BUNDESKANZLERAMT -->|"Sperrerklärung 28.09.2021 im Archivverfahren, bestätigt am 18.02.2022; Fachsenat bestätigte sie 2024. Keine Feststellung rechtswidriger Vertuschung."| N_DOC_DE_KAUKA_BND_AKTENKOMPLEX
    N_ORG_DE_BVERWG["Bundesverwaltungsgericht"]
    N_ORG_DE_BVERWG -->|"Urteil vom 30.04.2025: teilweise Erledigung, im Übrigen Klageabweisung. Geheimhaltungsgründe gerichtlich geprüft, keine öffentliche Feststellung einzelner Zahlungen oder Agentenverpflichtungen."| N_DOC_DE_KAUKA_BND_AKTENKOMPLEX
    N_PRG_DE_BND_UKRAINE_MEDIENKONTAKTE_2024["BND-Einzelhintergrundgespräche zur Ukraine 2024"]
    N_ORG_DE_BND -->|"Am 25.09.2024 mitgeteilte Zahl von acht Einzelhintergrundgesprächen seit Jahresanfang zur militärischen Situation in der Ukraine. Keine Benennung der Teilnehmer oder Feststellung ihrer Berichterstattungswirkung."| N_PRG_DE_BND_UKRAINE_MEDIENKONTAKTE_2024
    N_ORG_DE_BVERWG -->|"Urteil 25.09.2025 weist Klage ab; Recherchegeheimnis schützt betroffene Medien. Gericht bestätigt keine behauptete politische Steuerungsabsicht."| N_PRG_DE_BND_UKRAINE_MEDIENKONTAKTE_2024
    N_ORG_DE_VERLAG_1BVR257519["Nicht namentlich verifizierter Verlag (1 BvR 2575/19)"]
    N_ORG_DE_VERLAG_1BVR257519 -->|"Nach BND-Angaben übermittelte der Beschwerdeführer am 14.11.2019 die Verfassungsbeschwerde vertraulich; weitergehende Kooperation vom BND bestritten."| N_ORG_DE_BND
    N_ORG_DE_BVERFG["Bundesverfassungsgericht"]
    N_ORG_DE_VERLAG_1BVR257519 -->|"Beschwerde 1 BvR 2575/19 gegen Transparenzurteil 6 A 7.18; am 14.11.2019 nicht zur Entscheidung angenommen laut BVerwG."| N_ORG_DE_BVERFG
    N_ORG_DE_BVERWG -->|"Einstweilige Anordnung zur Auskunft über Beschwerdeführer, Anwälte sowie Einladung bzw. Teilnahme an Hintergrundgesprächen; kein Nachweis eines Gegengeschäfts."| N_ORG_DE_BND
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 27.11.2025 über BND-Angaben vier Termine; kein Nachweis einer konkreten redaktionellen Weisung."| N_ORG_DE_ARD
    N_ORG_DE_NDR["Norddeutscher Rundfunk"]
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 27.11.2025 über BND-Angaben vier Termine; kein Nachweis einer konkreten redaktionellen Weisung."| N_ORG_DE_NDR
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 27.11.2025 über BND-Angaben als Teilnehmermedium benannt; kein Nachweis einer konkreten redaktionellen Weisung."| N_ORG_DE_ZDF
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 27.11.2025 über BND-Angaben als Teilnehmermedium benannt; kein Nachweis einer konkreten redaktionellen Weisung."| N_ORG_DE_SWR
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 27.11.2025 über BND-Angaben als Teilnehmermedium benannt; kein Nachweis einer konkreten redaktionellen Weisung."| N_ORG_DE_BR
    N_ORG_DE_DW["Deutsche Welle"]
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 27.11.2025 über BND-Angaben als Teilnehmermedium benannt; kein Nachweis einer konkreten redaktionellen Weisung."| N_ORG_DE_DW
    N_ORG_DE_BND -->|"Tagesspiegel berichtet am 27.11.2025 über eigene Teilnahme an BND-Gesprächen; konkretes Datum nicht belegt; von Gruppeneinladungen unterscheiden."| N_ORG_DE_TAGESSPIEGEL
    N_PRG_DE_BND_EXTERNE_PRESSERECHTSMANDATE_2013_2025["Externe BND-Mandate in Presserechtsverfahren seit 2013"]
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 16.12.2025 knapp 200.000 EUR für externe Anwälte in elf Verfahren, darunter ein Unterlassungsverfahren; drei Kanzleien. Keine Einzelrechnungen eingesehen."| N_PRG_DE_BND_EXTERNE_PRESSERECHTSMANDATE_2013_2025
    N_ORG_DE_RAUE["Raue (Berlin)"]
    N_ORG_DE_BND -->|"Laut Tagesspiegel-Bericht vom 16.12.2025 meist mandatierte Kanzlei in elf Verfahren; genaue Mandatsdauer und eigener Kostenanteil nicht bekannt."| N_ORG_DE_RAUE
    N_ORG_DE_BUNDESKANZLERAMT -->|"Laut Tagesspiegel-Bericht vom 16.12.2025 regelmäßig bei presserechtlichen Auseinandersetzungen mandatiert; keine Einzelverträge, Laufzeit oder Beträge belegt."| N_ORG_DE_RAUE
    N_ORG_DE_BVERWG -->|"Urteil 10 A 2.24 verpflichtet zur Auskunft über Verfahren, Kanzleien und Summen; weitere Teile der Klage abgewiesen."| N_PRG_DE_BND_EXTERNE_PRESSERECHTSMANDATE_2013_2025
    N_ORG_DE_BILD["Bild"]
    N_ORG_DE_BND -->|"Bild laut Tagesspiegel-Bericht vom 10.11.2023 unter den fünf Medien mit den meisten Einzelhintergrundgesprächen 2019/2020 zusammen; keine Einzelzahl, Rangposition oder redaktionelle Weisung belegt."| N_ORG_DE_BILD
    N_ORG_DE_DER_SPIEGEL["Der Spiegel"]
    N_ORG_DE_BND -->|"Spiegel laut Tagesspiegel-Bericht vom 10.11.2023 unter den fünf Medien mit den meisten Einzelhintergrundgesprächen 2019/2020 zusammen; keine Einzelzahl, Rangposition oder redaktionelle Weisung belegt."| N_ORG_DE_DER_SPIEGEL
    N_ORG_DE_BND -->|"NDR laut Tagesspiegel-Bericht vom 10.11.2023 unter den fünf Medien mit den meisten Einzelhintergrundgesprächen 2019/2020 zusammen; keine Einzelzahl, Rangposition oder redaktionelle Weisung belegt."| N_ORG_DE_NDR
    N_ORG_DE_DIE_WELT["Die Welt"]
    N_ORG_DE_BND -->|"Welt laut Tagesspiegel-Bericht vom 10.11.2023 unter den fünf Medien mit den meisten Einzelhintergrundgesprächen 2019/2020 zusammen; keine Einzelzahl, Rangposition oder redaktionelle Weisung belegt."| N_ORG_DE_DIE_WELT
    N_ORG_DE_BND -->|"Zeit laut Tagesspiegel-Bericht vom 10.11.2023 unter den fünf Medien mit den meisten Einzelhintergrundgesprächen 2019/2020 zusammen; keine Einzelzahl, Rangposition oder redaktionelle Weisung belegt."| N_ORG_DE_DIE_ZEIT
    N_ORG_DE_LKA_NRW["Landeskriminalamt Nordrhein-Westfalen"]
    N_PER_DE_VP01_AMRI["VP01 (LKA NRW, Amri-Komplex)"]
    N_ORG_DE_LKA_NRW -->|"führte VP01 im Abu-Walaa-Ermittlungskomplex"| N_PER_DE_VP01_AMRI
    N_PER_DE_VP01_AMRI -->|"lieferte Hinweise zu Amri; Meldungsinhalt nicht automatisch bestätigt"| N_ORG_DE_LKA_NRW
    N_ORG_DE_GBA["Generalbundesanwalt beim Bundesgerichtshof"]
    N_ORG_DE_LKA_NRW -->|"übermittelte Erkenntnisse zu Amri und legte strafrechtlichen Prüfbedarf vor"| N_ORG_DE_GBA
    N_ORG_DE_LFV_NRW["Verfassungsschutz Nordrhein-Westfalen"]
    N_ORG_DE_LKA_NRW -->|"vereinbarte Weiterleitung an das BfV über den LfV NRW zum Schutz von VP01"| N_ORG_DE_LFV_NRW
    N_ORG_DE_BFV -->|"Behördenzeugnis vom 26.01.2016 wurde Grundlage eines GBA-Prüfvorgangs"| N_ORG_DE_GBA
    N_ORG_DE_BKA -->|"übermittelte Gefährdungsbewertungen; anfängliche Zweifel an VP01 später zurückgenommen"| N_ORG_DE_GBA
    N_ORG_MA_DGST["Direction générale de la surveillance du territoire (DGST)"]
    N_ORG_MA_DGST -->|"übermittelte vier Hinweise zu Amri laut BKA-Verbindungsbeamtem"| N_ORG_DE_BKA
    N_ORG_MA_DGST -->|"übermittelte Hinweise parallel laut BKA-Verbindungsbeamtem"| N_ORG_DE_BND
    N_ORG_DE_LFV_MV["Verfassungsschutz Mecklenburg-Vorpommern"]
    N_ORG_DE_LFV_MV -->|"übermittelte nach dem Anschlag nur Teile der Quellenmeldung; Kommissionsbefund"| N_ORG_DE_BFV
    N_ORG_DE_LFV_BERLIN["Verfassungsschutz Berlin"]
    N_ORG_DE_LFV_MV -->|"übermittelte nach dem Anschlag nur Teile der Quellenmeldung; Kommissionsbefund"| N_ORG_DE_LFV_BERLIN
    N_ORG_DE_GENSTA_BERLIN["Generalstaatsanwaltschaft Berlin"]
    N_ORG_DE_LKA_BERLIN["Landeskriminalamt Berlin"]
    N_ORG_DE_GENSTA_BERLIN -->|"beauftragte Zusammenstellung und Weitergabe der Erkenntnisse zum Drogenhandel"| N_ORG_DE_LKA_BERLIN
    N_ORG_DE_STA_BERLIN["Staatsanwaltschaft Berlin"]
    N_ORG_DE_STA_BERLIN -->|"beauftragte Ermittlungen gegen LKA-Beamten; später Verfahren gegen zwei Beamte eingestellt"| N_ORG_DE_LKA_BERLIN
    N_PER_TN_ANIS_AMRI["Anis Amri"]
    N_ORG_DE_GENSTA_BERLIN -->|"leitete Ermittlungsverfahren wegen Verdachts des Versuchs der Beteiligung an einem Tötungsdelikt ein; keine Verurteilung"| N_PER_TN_ANIS_AMRI
    N_ORG_DE_LFV_NRW -->|"als Vermittler zum BfV im vereinbarten Quellenschutz-Informationsweg vorgesehen"| N_ORG_DE_BFV
    N_ORG_DE_BFV -->|"erstellte Behördenzeugnis für Berliner Polizei ohne Nennung von VP01"| N_ORG_DE_LKA_BERLIN
    N_ORG_DE_BFV -->|"führte seit Januar 2016 eine Personenakte; keine Anwerbung als Quelle belegt"| N_PER_TN_ANIS_AMRI
    N_ORG_DE_FUSSILET_MOSCHEE["Fussilet 33 e.V. (Berliner Fussilet-Moschee)"]
    N_ORG_DE_BFV -->|"setzte dort eine V-Person zu einem anderen Sachverhalt ein; persönlicher Kontakt zu Amri nicht belegt"| N_ORG_DE_FUSSILET_MOSCHEE
    N_ORG_DE_BKA -->|"unterrichtete den BND erstmals über Amri"| N_ORG_DE_BND
    N_ORG_DE_BKA -->|"übermittelte ausgelesene Mobiltelefondaten zur Auswertung"| N_ORG_DE_BFV
    N_ORG_DE_BMI_AMRI_2017["Bundesministerium des Innern (Amri-Komplex 2017)"]
    N_ORG_DE_BMJV_AMRI_2017["Bundesministerium der Justiz und für Verbraucherschutz (2017)"]
    N_ORG_DE_BMI_AMRI_2017 -->|"vereinbarte nach Anschlag Vorrang ausländerrechtlicher Maßnahmen, wenn tragfähige Strafhaft nicht erreichbar war"| N_ORG_DE_BMJV_AMRI_2017
    N_ORG_DE_BMVG_1966["Bundesministerium der Verteidigung (1966)"]
    N_ORG_DE_PARNASS_FILM_MUENCHEN["Parnass-Film GmbH (München)"]
    N_ORG_DE_BMVG_1966 -->|"Laut BND-Edition stellte BMVg Unterstützung unter Bedingung von Drehbuchmitsprache und vorheriger Sichtung; keine endgültige Sachhilfezusage (Dok. 6)"| N_ORG_DE_PARNASS_FILM_MUENCHEN
    N_ORG_DE_PARNASS_FILM_MUENCHEN -->|"Werner bestätigte für Parnass die zivile Darstellung des BND und Bereitschaft zur vorherigen Sichtung (Edition S. 14, Dok. 14)"| N_ORG_DE_BMVG_1966
    N_ORG_DE_BMVG_1966 -->|"BMVg bat um BND-Votum, von dem es weitere Unterstützung abhängig machte (Edition Dok. 15)"| N_ORG_DE_BND
    N_ORG_DE_BUNDESPRESSEAMT_1966["Presse- und Informationsamt der Bundesregierung (1966)"]
    N_ORG_DE_PARNASS_FILM_MUENCHEN -->|"Parnass bat um diplomatische Unterstützung für Filmproduktion in Spanien; PA AA B 95, 365, 14668 laut Edition"| N_ORG_DE_BUNDESPRESSEAMT_1966
    N_ORG_DE_AUSWAERTIGES_AMT_1966["Auswärtiges Amt (1966)"]
    N_ORG_DE_BUNDESPRESSEAMT_1966 -->|"Presseamt leitete Film-Anfrage an AA weiter; PA AA B 95, 365, 14668 laut Edition"| N_ORG_DE_AUSWAERTIGES_AMT_1966
    N_ORG_DE_AUSWAERTIGES_AMT_1966 -->|"AA-Filmreferent besprach das Filmvorhaben mit BND (Edition Dok. 10)"| N_ORG_DE_BND
    N_PER_DE_THEO_MARIA_WERNER["Theo Maria Werner"]
    N_PER_DE_THEO_MARIA_WERNER -->|"Laut Edition übergab Werner ein Drehbuch; Originaldrehbuch nicht auffindbar"| N_ORG_DE_BND
    N_PER_DE_REINHARD_GEHLEN -->|"Gehlen gestattete grundsätzlich Außenaufnahmen, untersagte Aufnahmen im Inneren der Zentrale; tatsächliche Nutzung nicht belegt (Edition Dok. 13)"| N_ORG_DE_PARNASS_FILM_MUENCHEN
    N_PER_DE_KURT_WEISS_BND["Kurt Weiß (Winterstein)"]
    N_PER_DE_KURT_WEISS_BND -->|"BND-Vermerk vom 28.11.1966 berichtet über Treffen am 23.11.; Werner bestätigte Rangänderungen und erklärte weitere Änderungsbereitschaft"| N_PER_DE_THEO_MARIA_WERNER
    N_PER_DE_KURT_WEISS_BND -->|"Weiß berichtete Gehlen über Produktionsgespräch und Unterstützungswünsche (Edition Dok. 17)"| N_PER_DE_REINHARD_GEHLEN
    N_PER_DE_KURT_WEISS_BND -->|"Weiß informierte CIA-Verbindungsstab über Filmprojekt (Edition S. 18, Dok. 18)"| N_ORG_US_CIA
    N_ORG_US_CIA -->|"US-Dienst bestritt vorherige Kenntnis und berichtete fehlende Unterstützungszusage amerikanischer Stellen; keine nachgewiesene US-Filmhilfe (Edition Dok. 18)"| N_ORG_DE_BND
    N_PER_DE_THEO_MARIA_WERNER -->|"Filmportal und BND-Edition nennen Werner als Produzenten der Münchner Parnass-Produktion"| N_ORG_DE_PARNASS_FILM_MUENCHEN
    N_PER_DE_KURT_WEISS_BND -->|"Politische/strategische Aufklärung und Pressekontakte laut BND-Edition und editorischer Anm. 10 des Stasi-Unterlagen-Archivs; genaue Funktionsdaten abweichend"| N_ORG_DE_BND
    N_PER_DE_KURT_WEISS_BND -->|"Eintritt 1952 laut BND-Edition S. 15 Fn. 41; historische Funktion vor BND-Gründung"| N_ORG_DE_ORGANISATION_GEHLEN
    N_ORG_DE_BND -->|"BND-Edition S. 18 Fn. 54 berichtet genehmigte Aufnahmen für WDR-Dokumentation 1964; zeitgenössische Originalberichte noch zu prüfen"| N_ORG_DE_WDR
    N_ORG_DE_MFS["Ministerium für Staatssicherheit (MfS)"]
    N_ORG_DE_MFS -->|"MfS-Abteilung Agitation berichtet gezielte Materialsendungen an die Redaktion nach der ersten Folge; beabsichtigte Beeinflussung, keine unabhängige Empfangs- oder Wirkungsbestätigung (K 1/21, 4.1)"| N_ORG_DE_DER_SPIEGEL
    N_ORG_DE_BUNDESTAGSABGEORDNETE_PULLACH_1971["Acht Bundestagsabgeordnete (MfS-Versandliste, 1971)"]
    N_ORG_DE_MFS -->|"MfS berichtet Versand publizistischer Extradrucke an acht namentlich genannte Abgeordnete verschiedener Parteien; keine daraus ableitbare Kooperation (K 1/21, 4.2)"| N_ORG_DE_BUNDESTAGSABGEORDNETE_PULLACH_1971
    N_PER_DE_JULIUS_MADER["Julius Mader"]
    N_ORG_DE_MFS -->|"MfS berichtet Durchführung operativ-publizistischer Maßnahmen in Absprache mit Mader (K 1/21, 4)"| N_PER_DE_JULIUS_MADER
    N_PER_DE_FRITZ_BAIER["Fritz Baier"]
    N_PER_DE_JULIUS_MADER -->|"MfS führt einen polemischen Brief Maders an den CDU-Abgeordneten Baier mit belastendem Material auf; Empfängerreaktion nicht belegt (K 1/21, 4.3)"| N_PER_DE_FRITZ_BAIER
    N_ORG_DE_DDR_PANORAMA_AUSLANDSPRESSEDIENST["Panorama (DDR-Auslandspressedienst, 1971)"]
    N_ORG_DE_MFS -->|"MfS berichtet Verbreitung eines BND-kritischen Artikels über den DDR-Auslandspressedienst in 22 lateinamerikanischen Staaten; Reichweite und tatsächliche Rezeption ungeprüft (K 1/21, 4.4)"| N_ORG_DE_DDR_PANORAMA_AUSLANDSPRESSEDIENST
    N_PER_DE_HERMANN_ZOLLING["Hermann Zolling"]
    N_ORG_DE_BND -->|"Laut archivgestützter Darstellung Dülffers kooperierten BND und SPIEGEL-Journalist Zolling im Vorfeld der 1971 erschienenen Serie; genauer Beginn hier nicht belegt; keine Agenten- oder Zahlungsbeziehung belegt"| N_PER_DE_HERMANN_ZOLLING
    N_ORG_DE_DER_SPIEGEL -->|"Laut Dülffer erhielt der BND vorab Artikelentwürfe zur Durchsicht; erste veröffentlichte Fassung nicht mehr gegengelesen"| N_ORG_DE_BND
    N_ORG_DE_BND -->|"Laut Dülffer versuchte BND bestimmte aus seiner Sicht fehlerhafte oder geheimhaltungsbedürftige Veröffentlichungen zu verhindern; keine generelle redaktionelle Verfügungsmacht"| N_ORG_DE_DER_SPIEGEL
    N_ORG_DE_BUNDESKANZLERAMT -->|"Laut Dülffer versuchte auch das Kanzleramt bestimmte Veröffentlichungen zu verhindern; erste veröffentlichte Fassung war laut Dülffer nicht mehr vom BND gegengelesen"| N_ORG_DE_DER_SPIEGEL
    N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985["Bayerischer Landtag – Untersuchungsausschuss Langemann II (1983–1985)"]
    N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985 -->|"Ausschuss ersuchte laut Schlussbericht um Einsicht in Langemanns beim GBA befindliche Ring- und Tagebücher (S. 5, Abschn. 3)"| N_ORG_DE_GBA
    N_ORG_DE_BND -->|"GBA-Ablehnung vom 28.04.1983 verwies auf den gegen die Einsicht erhobenen Einwand des BND; Einwand spätestens 28.04.1983, genaues Datum unbekannt; Originalschreiben nicht separat geprüft (S. 5, 3 k)"| N_ORG_DE_GBA
    N_ORG_DE_GBA -->|"GBA lehnte laut Schlussbericht Akteneinsicht unter Verweis auf BND-Interessen ab (S. 5, 3 k)"| N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985
    N_ORG_DE_VG_MUENCHEN_1983["Verwaltungsgericht München (1983)"]
    N_PER_DE_HANS_LANGEMANN -->|"Langemann klagte gegen das Einsichtsbegehren unter Berufung auf Privatsphäre; Ausschuss setzte Vollzug mehrheitlich aus, Ergebnis des Verfahrens offen (S. 5, Abschn. 3)"| N_ORG_DE_VG_MUENCHEN_1983
    N_ORG_DE_BAYOBLG_1983["Bayerisches Oberstes Landesgericht (1983)"]
    N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985 -->|"Ausschuss richtete das Einsichtsbegehren nach Übergang der strafgerichtlichen Zuständigkeit an das BayObLG (S. 5, 3 l)"| N_ORG_DE_BAYOBLG_1983
    N_ORG_DE_BAYOBLG_1983 -->|"Vorsitzender des 3. Strafsenats lehnte Einsicht aus Gründen des BND-Geheimschutzes ab; keine gerichtliche Rechtswidrigkeitsfeststellung behauptet (S. 5, 3 l)"| N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985
    N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985 -->|"Ausschuss beschloss Gegenvorstellung mit Angebot der Einsicht in Gerichtsräumen (S. 5, 3 l)"| N_ORG_DE_BAYOBLG_1983
    N_ORG_DE_BAYOBLG_1983 -->|"Erneute Ablehnung; berichtete Begründung: nicht aussonderbare nachrichtendienstliche Informationen und Schutz privater Aufzeichnungen (S. 5, 3 l)"| N_ORG_DE_BAYLT_UA_LANGEMANN_II_1983_1985
    N_ORG_DE_DDR_STAAT["Deutsche Demokratische Republik (1949–1990)"]
    N_ORG_DE_DDR_DEMOCRATIC_GERMAN_REPORT["Democratic German Report (1952–1975)"]
    N_ORG_DE_DDR_STAAT -->|"Howarth berichtet vollständige Finanzierung des DGR durch die DDR; konkrete zahlende Stelle, Haushaltsansätze und Beträge nicht nachgewiesen"| N_ORG_DE_DDR_DEMOCRATIC_GERMAN_REPORT
    N_PER_GB_JOHN_SCOTT_PEET["John Scott Peet"]
    N_PER_GB_JOHN_SCOTT_PEET -->|"Herausgeber und Chefredakteur des englischsprachigen DGR 1952–1975"| N_ORG_DE_DDR_DEMOCRATIC_GERMAN_REPORT
    N_ORG_DE_MFS -->|"Berger/LaPorte S. 65 Fn. 178 berichten Überwachung 1952–1956 und erneut nach 1959; Verdacht britischer Geheimdiensttätigkeit nicht belegt; Originalakte MfS 17752/62 nicht eingesehen"| N_PER_GB_JOHN_SCOTT_PEET
    N_ORG_DE_SED_POLITBUERO["Politbüro des ZK der SED"]
    N_ORG_DE_SED_POLITBUERO -->|"Laut biografischem Handbuch beschloss das Politbüro im Dezember 1975 die Einstellung wegen der nicht mehr gewährleisteten politischen Linie; Originalbeschluss ausstehend"| N_ORG_DE_DDR_DEMOCRATIC_GERMAN_REPORT
    N_ORG_GB_NOTLEYS_ADVERTISING["Notley's Advertising Ltd"]
    N_ORG_DE_DDR_STAAT -->|"Howarth berichtet Londoner DDR-PR-Mandat von Notley im Umfeld der Pressebriefe Dezember 1960; Berger/LaPorte S. 116 nennen berichtete Vergütung bis zu 20.000 GBP jährlich ab 1960; tatsächliche Höhe, Laufzeit und Zahlungsbelege offen"| N_ORG_GB_NOTLEYS_ADVERTISING
    N_PER_GB_BURNABY_DRAYSON["George Burnaby Drayson"]
    N_ORG_GB_NOTLEYS_ADVERTISING -->|"Howarth berichtet Drayson als einen von zwei konservativen Abgeordneten mit Beratungsverhältnis zu Notley; Honorare, Vertragsbeginn und zweiter Name nicht direkt belegt"| N_PER_GB_BURNABY_DRAYSON
    N_ORG_GB_NOTLEYS_ADVERTISING -->|"Howarth berichtet Formulierung von Draysons Pressebriefen zum Fall Franz Krahl im Dezember 1960 durch Notley; keine ursprünglichen Entwürfe eingesehen"| N_PER_GB_BURNABY_DRAYSON
    N_ORG_GB_DOMINION_EXPORT["Dominion Export Ltd"]
    N_PER_GB_BURNABY_DRAYSON -->|"Berger/LaPorte S. 72 beschreiben Drayson als Direktor der Dominion Export Ltd im Zusammenhang mit dem Handelsgeschäft 1953; genaue Amtsdauer offen"| N_ORG_GB_DOMINION_EXPORT
    N_ORG_GB_DOMINION_EXPORT -->|"Berger/LaPorte S. 72: Handelsvereinbarung im Herbst 1953 über rund 3 Mio. GBP, Kalieinfuhr und Lebensmittelexport; Vertragswert, keine tatsächliche Zahlung oder persönliche Vergütung nachgewiesen"| N_ORG_DE_DDR_STAAT
    N_ORG_GB_HOUSE_OF_COMMONS["House of Commons (britisches Unterhaus)"]
    N_PER_GB_BURNABY_DRAYSON -->|"Drayson erklärt am 21.03.1962 öffentlich sein Interesse: eine mit ihm verbundene, im Beitrag nicht namentlich genannte Firma importiere DDR-Ammoniumsulfat und Kali"| N_ORG_GB_HOUSE_OF_COMMONS
    N_PER_DE_JULIUS_MADER -->|"Engelmann/Joestel S. 50 Fn. 189: Mader 1962–1989 Offizier im besonderen Einsatz im MfS-Agitationsbereich, unter Verweis auf Kaderakte KS 25335/90; Originalakte ausstehend"| N_ORG_DE_MFS
    N_PRG_DE_MFS_STURM_1971["MfS-Konzeption Sturm (Bezug April 1971)"]
    N_ORG_DE_MFS -->|"K 1/21 Abschnitt 3.3 d: Plan zur Vortäuschung konspirativer Aktivität; Verweis auf Konzeption Sturm; keine konkret ausgeführte Maßnahme oder Wirkung damit belegt"| N_PRG_DE_MFS_STURM_1971
    N_PER_US_JOHN_HOWARD_LAWSON["John Howard Lawson"]
    N_PER_US_JOHN_HOWARD_LAWSON -->|"Briefkopie vom 18.12.1971: Lawson bittet DGR um Änderung seiner Anschrift; tatsächlicher Empfang und politische Zusammenarbeit nicht belegt"| N_ORG_DE_DDR_DEMOCRATIC_GERMAN_REPORT
    N_PRG_US_FBI_BUREAU_SOURCE_300["Bureau Source 300 (FBI-Quellenbezeichnung)"]
    N_ORG_US_FBI_LEGAT_BONN["FBI Legal Attaché Bonn (1956–1975 belegt)"]
    N_PRG_US_FBI_BUREAU_SOURCE_300 -->|"Legat Bonn berichtet 13.01.1972 Erhalt der Lawson-Adressänderung über Bureau Source 300; Zeitpunkt des vorherigen Erhalts und Beschaffungsmethode offen"| N_ORG_US_FBI_LEGAT_BONN
    N_ORG_US_FBI_LEGAT_BONN -->|"Dienstlicher FBI-Vermerk vom 13.01.1972 an Director, FBI: Lawson-DGR-Korrespondenz mit DGR-Aktenhinweis 105-18093"| N_ORG_US_FBI
    N_PER_US_BERNARD_FENSTERWALD["Bernard Fensterwald Jr."]
    N_PER_DE_JULIUS_MADER -->|"FBI-Vermerk 13.11.1972 berichtet Formularbrief Maders mit Angebot seines Buchs Yellow List: Where is the CIA? und Bestellformular; keine operative Anwerbung belegt"| N_PER_US_BERNARD_FENSTERWALD
    N_PER_US_BERNARD_FENSTERWALD -->|"FBI-Vermerk berichtet Bestellung eines englischen Exemplars mit einem 2-Dollar-Scheck; Einlösung, Lieferung oder weitere Zusammenarbeit nicht nachgewiesen"| N_PER_DE_JULIUS_MADER
    N_PRG_US_FBI_BUREAU_SOURCE_300 -->|"Legat Bonn berichtet 13.11.1972 Erhalt des Materials zur Mader-Fensterwald-Bestellung über Bureau Source 300; keine konkret benannte Beschaffungsstelle"| N_ORG_US_FBI_LEGAT_BONN
    N_ORG_US_FBI_LEGAT_BONN -->|"Dienstlicher FBI-Vermerk vom 13.11.1972 an Acting Director zur Mader-Buchbestellung; Anlage erläutert Quellenschutz und bedingte Weitergabe"| N_ORG_US_FBI
    N_ORG_US_ARMY_66TH_CIC["66th CIC Group (Region VIII, Berlin, 1956)"]
    N_ORG_US_ARMY_66TH_CIC -->|"FBI-Vermerk 19.03.1956: Kopie eines Lawson-Briefs an Schlichting aus technischer Erfassung der 66th CIC Group über G-2 US Army Europe; DGR-Feld unmarkiert"| N_ORG_US_FBI_LEGAT_BONN
    N_ORG_US_HOUSE_SELECT_COMMITTEE_INTELLIGENCE_1975["U.S. House Select Committee on Intelligence Activities (1975)"]
    N_ORG_US_HOUSE_SELECT_COMMITTEE_INTELLIGENCE_1975 -->|"Aktenanforderung vom 26.09.1975 zu drei Organisationen einschließlich AFSC; später präzisierter Zeitraum laut FBI-Antwort"| N_ORG_US_FBI
    N_ORG_US_ARMY -->|"FBI NOTE in der Antwort von 1975, S.197, identifiziert vier im AFSC-Zusammenhang erhaltene Source-300-Berichte als Material der US Army in Deutschland; keine pauschale Zuordnung aller Source-300-Fälle"| N_PRG_US_FBI_BUREAU_SOURCE_300
    N_ORG_US_ARMY -->|"FBI NOTE S.197: Colonel John Heiss, Security Division ACSI, bat laut Liaison Section am 03.11.1975 um Nichtfreigabe der vier AFSC-Berichte an HSC"| N_ORG_US_FBI
    N_ORG_US_FBI -->|"FBI-Antwortunterlagen vom 06.11.1975 nennen vier Source-300-Serien zum AFSC-Besuchsaustausch als nicht zur Ausschusseinsicht vorbereitet; spätere Freigabe und Rechtsgrundlage ungeklärt"| N_ORG_US_HOUSE_SELECT_COMMITTEE_INTELLIGENCE_1975
    N_ORG_US_AMERICAN_FRIENDS_SERVICE_COMMITTEE["American Friends Service Committee (AFSC)"]
    N_ORG_US_FBI_LEGAT_BONN -->|"FBI NOTE S.197: vier über Legat Bonn erhaltene Source-300-Serien behandeln Besuche zwischen AFSC-Mitgliedern und Personen in einem anderen Land; kein Erfassungsdatum, keine Straftat festgestellt"| N_ORG_US_AMERICAN_FRIENDS_SERVICE_COMMITTEE
```

[Zur Relationstabelle](network.md)
