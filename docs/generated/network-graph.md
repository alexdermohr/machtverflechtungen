# Netzwerkdiagramm

**127 Beziehungen** als interaktive Übersicht. Die [alphabetische Relationstabelle](network.md) zeigt zusätzlich Evidenzstufen und Quellen.

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
```

[Zur Relationstabelle](network.md)
