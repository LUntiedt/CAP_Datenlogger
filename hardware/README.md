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

## Einstieg für AP1–AP3

### Was ist jetzt dran?

Für AP1, AP2 und AP3 stehen zuerst **Schaltplan und Bauteilpflege** an: die eigenen
Bauteile anlegen (siehe [Bauteile anlegen](#bauteile-anlegen)) und das eigene
Schaltplanblatt zeichnen. Das Layout (`datenlogger.kicad_pcb`) liegt bei AP4. Wer Lust hat,
kann aber gerne Teile davon übernehmen, z. B. die Platzierung und das Routing des eigenen
Blocks. Einfach bei Laurenz melden, dann teilen wir das in AP4 auf.

### Projekt öffnen

1. `git pull`, eigenen Branch anlegen (AGENTS.md §9), z. B. `hw/ap3-flash-schaltplan`.
2. KiCad **10.0** starten → *Datei → Projekt öffnen* → **`hardware/datenlogger.kicad_pro`**.
   Immer die Projektdatei öffnen, nicht die `.kicad_sch` direkt. Nur dann lädt KiCad die
   Projektbibliotheken (`00_CAP_*`) und die Blatthierarchie.
3. Im Schaltplaneditor das eigene Blatt öffnen: im Root-Blatt doppelt auf den Kasten
   `Power` / `Digital` / `Memory` klicken oder links im Hierarchie-Navigator auswählen.
4. Vor einem Branchwechsel oder `git pull` KiCad schließen. KiCad lädt geänderte Dateien
   nicht neu und überschreibt sie sonst beim nächsten Speichern.

### Was öffnet sich wo? (KiCad-Projektfenster)

| Werkzeug | Bearbeitet | Wer |
|---|---|---|
| **Schaltplaneditor** | `datenlogger.kicad_sch` (Root) und die Blätter `power`/`digital`/`memory` | jede/r im eigenen Blatt, Root: AP4 |
| **Symboleditor** | Symbole in `lib/00_CAP_*_SYM.kicad_sym` | jede/r in der eigenen Bibliothek |
| **Leiterplatteneditor** (PCB) | `datenlogger.kicad_pcb` | AP4 (bzw. nach Absprache) |
| **Footprint-Editor** | Footprints in `lib/00_CAP_FTP.pretty/` | jede/r, für die eigenen Bauteile |
| Gerber-Viewer | fertige Gerberdateien ansehen | bei Freigabe |
| Rechner für Leiterplatten | Leiterbahnbreiten, Spannungsteiler, E-Reihen usw. | bei Bedarf |
| Bild-Konverter, Zeichnungsvorlagen-Editor | Logos, Schriftfeld-Vorlage | nicht nötig |
| Plugin- und Inhaltsverwaltung | Erweiterungen installieren | nicht nötig |

**Wichtig:** Im Schaltplaneditor *nicht* „Leiterplatte aus Schaltplan aktualisieren“ (F8)
ausführen und keine Änderungen an der `.kicad_pcb` committen. Das macht AP4 beim
Zusammenführen, sonst gibt es Konflikte in der Layoutdatei.

### Verbindungen und Netznamen

- **Lokale Labels und Drähte gelten nur auf dem eigenen Blatt.** Ein Label `SCK` auf
  `memory` und ein Label `SCK` auf `digital` sind zwei verschiedene Netze. Netznamen auf dem
  eigenen Blatt können also frei gewählt werden, ohne mit anderen Blättern zu kollidieren.
- **Ausnahme Versorgungssymbole:** `GND`, `VDD`, `VBAT` usw. (Power-Symbole) sind
  **global**, gleichnamige Power-Symbole sind auf allen Blättern verbunden. Namen der
  Versorgungsnetze deshalb mit AP1/AP4 abstimmen, nicht eigene Varianten erfinden
  (`3V3` vs. `+3.3V`).
- **Signale zwischen Blättern** (z. B. SPI zwischen nRF54L15 auf `digital` und dem Flash
  auf `memory`) laufen über die Hierarchie, **nur dann** braucht man das:
  1. Im eigenen Blatt an das Signal ein **hierarchisches Label** setzen
     (*Platzieren → Hierarchisches Label*, Taste `H`), z. B. `SPI_SCK`.
  2. Im Root-Blatt erscheint dazu am Blattkasten ein **Blattanschluss** (Sheet Pin),
     der über *Blattanschlüsse aus hierarchischen Labels importieren* übernommen wird.
     Die Blattanschlüsse beider Blätter werden im Root-Blatt mit einem Draht verbunden.
  3. Das Root-Blatt pflegt AP4. Im MR/PR deshalb angeben, welche hierarchischen Labels
     neu sind und wohin sie sollen; AP4 verbindet sie im Root-Blatt. So arbeiten nicht
     mehrere Leute gleichzeitig in derselben Datei.
- **Keine globalen Labels** verwenden. Sie verbinden blattübergreifend „unsichtbar“ und
  umgehen die Hierarchie, Fehler fallen dann erst spät auf.
- Signalnamen: Großbuchstaben, Unterstrich, keine Umlaute, Funktion vor Nummer, aktiv-low
  mit `_N` (z. B. `SPI_MOSI`, `ACC_INT1`, `FLASH_CS_N`).

### Bauteilbezeichner (Annotation)

Damit sich `R1` auf zwei Blättern nicht doppelt, beim Annotieren
(*Werkzeuge → Schaltplan annotieren*) **„Erste freie Nummer nach Blattnummer × 100“**
wählen. Dann bekommt `power` R201 ff., `digital` R301 ff., `memory` R401 ff.
(Blattnummern: Root 1, Power 2, Digital 3, Memory 4).

### Ein gutes Schaltplanblatt

- Signalfluss von links nach rechts, Versorgung oben, Masse unten.
- Funktionsgruppen räumlich zusammenfassen und mit einem Rahmen bzw. Text beschriften
  („Entkopplung nRF54L15“, „SWD“), Hinweise für das Layout als Text dazuschreiben
  (z. B. „C nah an Pin 12“).
- Lieber Labels als lange, kreuzende Drähte; Drähte nur auf dem Raster.
- Werte und MPN sichtbar bzw. im Feld `Manufacturer_Part_Number` gefüllt.
- Schriftfeld ausfüllen (*Datei → Seiteneinstellungen*: Titel, Name, Datum, Revision).
- Vor dem MR/PR: **ERC** (*Prüfen → Elektrische Regeln prüfen*) für das eigene Blatt ohne
  ungeklärte Fehler. Bewusst ignorierte Warnungen im MR/PR begründen.
- Anschauen: [Phil's Lab auf YouTube](https://www.youtube.com/@PhilsLab), v. a. das
  zweiteilige KiCad-9-Tutorial (Teil 1: Schaltplan) und die Design-Reviews
  (z. B. #70 „Design Review – Schematic & PCB“). Zeigt gut, wie ein aufgeräumtes
  Schaltplanblatt aussieht. KiCad 9 und 10 unterscheiden sich dabei kaum.

## Projekt anlegen (einmalig, AP4)

1. In KiCad *Neues Projekt* → Ordner `hardware/`, Name `datenlogger`.
   Danach prüfen, dass `sym-lib-table` und `fp-lib-table` noch die Einträge oben
   enthalten (Einstellungen → Symbolbibliotheken verwalten → Projektspezifisch).
2. Im Root-Blatt drei hierarchische Blätter mit den Dateinamen `power.kicad_sch`,
   `digital.kicad_sch`, `memory.kicad_sch` anlegen.
3. Committen; ab dann arbeitet jede/r nur im eigenen Blatt.

## Bauteile anlegen

Ablage: Symbol in die eigene Bibliothek `00_CAP_<Block>_SYM`, Footprint in
`00_CAP_FTP.pretty`, 3D-Modell nach `lib/00_CAP_3D/`.

### Ablauf

**0. Vorher prüfen**

- In `00_CAP_Common_SYM` nachsehen, ob es das Bauteil schon gibt (Würth-Passive u. a.).
- Bei [Mouser](https://www.mouser.de) die vollständige MPN (Hersteller-Teilenummer) heraussuchen
  und Verfügbarkeit prüfen: Lagerbestand, Status (aktiv / nicht für Neuentwicklungen / abgekündigt),
  Preis. MPN und Verfügbarkeit mit Datum in den ADR bzw. `docs/components.md` (AGENTS.md §6).
- Datenblatt herunterladen; für Kandidaten nach `docs/datasheets/`.

**1. Dateien holen**

- Auf Mouser beim Bauteil „ECAD-Modell“ bzw. direkt bei
  [Component Search Engine](https://componentsearchengine.com) nach der MPN suchen und das
  KiCad-Paket herunterladen. Es enthält Symbol, Footprint und meist ein 3D-Modell.
- ZIP außerhalb des Repos entpacken; nur die benötigten Dateien übernehmen.

**2. Symbol importieren, anpassen, gegenchecken**

- Symboleditor → **zuerst links die eigene Bibliothek `00_CAP_<Block>_SYM` anklicken**, dann
  *Datei → Importieren → Symbol*. Sonst landet das Symbol in der falschen Bibliothek.
- Name = MPN.
- Felder wie bei den vorhandenen Symbolen: `Manufacturer`, `Manufacturer_Part_Number`,
  `Datasheet` (Link zum Herstellerdatenblatt), `Description`. Gleiche Feldnamen sind wichtig,
  damit die Stückliste (BOM) einheitliche Spalten bekommt.
- **Gegenchecken mit dem Datenblatt:** jede Pin-Nummer und jeder Pin-Name, Pin-Typ
  (Eingang, Ausgang, Versorgung, passiv – wichtig für den ERC), keine fehlenden oder doppelten Pins,
  Exposed Pad / Thermal Pad als eigener Pin vorhanden. Anordnung lesbar (Versorgung oben,
  Masse unten, Eingänge links, Ausgänge rechts).

**3. Footprint importieren, anpassen, gegenchecken**

- Footprinteditor → **zuerst links `00_CAP_FTP` anklicken**, dann *Datei → Importieren → Footprint*
  (die `.kicad_mod` aus dem Paket).
- Name = Gehäusebezeichnung oder MPN, wie bei den vorhandenen Footprints.
- **Gegenchecken mit der Maßzeichnung bzw. dem empfohlenen Land Pattern im Datenblatt:**
  Pad-Größen, Rastermaß, Pad-Nummerierung (passt zur Pin-Nummer im Symbol), Lage von Pin 1,
  Exposed Pad inkl. Lötpastenaufteilung, Courtyard, Bestückungsdruck (Pin-1-Markierung,
  nicht auf Pads), Fab-Layer mit Referenz.
- **SMD-Pads mit abgerundeten Ecken** (Padform „Rechteck, abgerundet“ / roundrect) statt
  scharfkantiger Rechtecke, für bessere Fertigbarkeit. Importierte Footprints haben oft
  eckige Pads, dann umstellen.

**4. 3D-Modell importieren und mit dem Footprint verknüpfen**

- STEP-Datei nach `lib/00_CAP_3D/` kopieren.
- Im Footprint unter *Eigenschaften → 3D-Modelle* den Pfad
  `${KIPRJMOD}/lib/00_CAP_3D/<datei>.step` eintragen, **nie einen absoluten Pfad**.
- In der 3D-Vorschau Lage, Drehung und Höhe gegen die Pads prüfen, ggf. Offset/Rotation korrigieren.

**5. Symbol mit dem Footprint verknüpfen**

- Im Symbol das Feld `Footprint` auf `00_CAP_FTP:<footprintname>` setzen
  (Bibliotheksname davor, sonst findet KiCad ihn nicht).
- Im Schaltplan prüfen: Bauteil platzieren, *Footprints zuordnen* zeigt den richtigen Footprint,
  im Layout erscheinen Pads und 3D-Modell.

**6. Committen**

- Symbolbibliothek, `.kicad_mod` und STEP-Datei in einem Commit, z. B.
  `hw(lib): MX25R6435FZNIL0 angelegt`. Review per MR/PR an AP4.

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
