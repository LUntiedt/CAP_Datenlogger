# Hardware

KiCad-Projekt des Datenloggers. Regeln: `AGENTS.md` Abschnitt 7.

**KiCad-Version:** KiCad 10.0.x (alle bleiben bei 10.0, kein Wechsel auf eine neue Hauptversion während des Projekts).

## Aufbau

```
hardware/
├── datenlogger.kicad_pro      Projekt (legt AP4 an)
├── datenlogger.kicad_sch      Root-Blatt mit den hierarchischen Blättern (AP4)
├── power.kicad_sch            AP1 Energieversorgung
├── digital.kicad_sch          AP2 Sensor und Mikrocontroller
├── memory.kicad_sch           AP3 Speicher
├── datenlogger.kicad_pcb      Layout (AP4)
├── sym-lib-table              bindet lib/00_CAP_*_SYM.kicad_sym über ${KIPRJMOD} ein
├── fp-lib-table               bindet lib/00_CAP_FTP.pretty über ${KIPRJMOD} ein
├── lib/                       Präfix 00_ sortiert die Projektbibliotheken in KiCad nach oben
│   ├── 00_CAP_3D/                     3D-Modelle (STEP), gemeinsam
│   ├── 00_CAP_FTP.pretty/             Footprints (eine Datei pro Footprint, gemeinsam)
│   ├── 00_CAP_Common_SYM.kicad_sym    gemeinsame Bauteile: Passive, Stecker, Taster (AP4)
│   ├── 00_CAP_Power_SYM.kicad_sym     Symbole AP1
│   ├── 00_CAP_Digital_SYM.kicad_sym   Symbole AP2
│   └── 00_CAP_Memory_SYM.kicad_sym    Symbole AP3
├── bom/                       Stückliste mit Bezugsquellen
├── production/vX.Y/           Fertigungsdaten, nur bei Freigabe
└── enclosure/                 Gehäuse (AP5)
```

## Projekt anlegen (einmalig, AP4)

1. In KiCad *Neues Projekt* → Ordner `hardware/`, Name `datenlogger`.
   Danach prüfen, dass `sym-lib-table` und `fp-lib-table` noch die Einträge oben
   enthalten (Einstellungen → Symbolbibliotheken verwalten → Projektspezifisch).
2. Im Root-Blatt drei hierarchische Blätter mit den Dateinamen `power.kicad_sch`,
   `digital.kicad_sch`, `memory.kicad_sch` anlegen.
3. Committen; ab dann arbeitet jede/r nur im eigenen Blatt.

## Bauteile anlegen

- Erst in `00_CAP_Common_SYM` nachsehen, ob es das Bauteil schon gibt (Würth-Passive u. a.).
- Sonst Symbol in die eigene Bibliothek `00_CAP_<Block>_SYM`, Footprint in `00_CAP_FTP.pretty`,
  3D-Modell nach `lib/00_CAP_3D/` und im Footprint über `${KIPRJMOD}/lib/00_CAP_3D/<datei>.step` verknüpfen.
- Felder pflegen: Hersteller, Hersteller-Nr., Datenblatt-Link.
- Footprints aus Herstellerquellen gegen die Maßzeichnung im Datenblatt prüfen.

## Warum eine Symbolbibliothek pro Block?

Eine `.kicad_sym` ist eine einzige Textdatei. Legen zwei Personen auf verschiedenen
Branches gleichzeitig Symbole an, kann Git das beim Mergen oft automatisch
zusammenführen, aber nicht immer (z. B. wenn beide an derselben Stelle einfügen).
Ein Konflikt in dieser Datei ist von Hand mühsam aufzulösen. Mit einer Bibliothek pro
Block kann das nicht passieren. Footprints sind ohnehin einzelne Dateien.

## Was nicht ins Repo gehört

Backups (`*-backups/`), `*.kicad_prl` (persönliche Ansicht), `fp-info-cache`, Lock-Dateien,
lose Gerber-/ZIP-Dateien. Siehe `.gitignore`.

## Freigabe (M2)

1. ERC und DRC ohne Fehler, Review per MR/PR.
2. Gerber, Bohrdaten, Bestückdaten und BOM nach `production/vX.Y/` exportieren.
3. Commit + Git-Tag `hw-vX.Y`.

## Errata

Fehler und Änderungswünsche am gefertigten Prototyp:

- 
