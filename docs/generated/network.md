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
```

## Relationen

| ID | Von | Beziehung | Zu | Evidenz | Quellen |
|---|---|---|---|---|---|
| REL-DE-CELLER-001 | Niedersächsischer Verfassungsschutz | führte Aktion Feuerzauber durch | Celler Loch / Aktion Feuerzauber | established | SRC-DE-NI-MJ-CELLER-2015 |
| REL-DE-GEHLEN-001 | Organisation Gehlen | wurde 1956 in den BND überführt | Bundesnachrichtendienst | established | SRC-DE-BPB-BND-2026 |
| REL-DE-GEHLEN-002 | Reinhard Gehlen | leitete | Organisation Gehlen | established | SRC-DE-BPB-BND-2026 |
| REL-DE-GEHLEN-003 | Reinhard Gehlen | erster Präsident | Bundesnachrichtendienst | established | SRC-DE-BPB-BND-2026 |
| REL-DE-THS-001 | Thüringer Landesamt für Verfassungsschutz | führte und bezahlte als V-Mann | Tino Brandt | established | SRC-DE-THLT-NSU-UA-2014 |
| REL-DE-THS-002 | Tino Brandt | setzte Geld und Sachmittel für Aufbau und Funktionieren ein | Thüringer Heimatschutz | established | SRC-DE-THLT-NSU-UA-2014 |
| REL-DE-AB-001 | Atlantik-Brücke e.V. | betreibt | Atlantik-Brücke Young Leaders Program | established | SRC-DE-ATLANTIKBRUECKE-YL |
