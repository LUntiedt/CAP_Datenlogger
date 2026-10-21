# AP3 – Speicher und Datenübertragung

| | |
|---|---|
| **Verantwortlich** | Jan Thiedmann |
| **Zeitraum** | W1–W8 |
| **Bezug** | F4, F5, F6, F7, F10, F11, NF4 · Pflichtenheft 3.2.1 (Speicher), 3.2.2 (Tabelle 2), 3.4, 3.6 |
| **Schaltplanblatt** | `hardware/memory.kicad_sch` · Symbole in `hardware/lib/CAP_Memory.kicad_sym` |
| **Firmware** | `firmware/src/drivers/` (Flash), `firmware/src/services/` (Datenablage, BLE) |
| **Werkzeug** | `tools/readout/` (PC-Auslesewerkzeug) |

## Ziel

Die Messdaten werden blockweise, mit Zeitstempel und Prüfsumme, ausfallsicher im
Flash abgelegt, per BLE vollständig an ein PC-Werkzeug übertragen und in einem
Format exportiert, das die Analysewerkzeuge des Labors direkt verarbeiten.

Forschungsfragen aus der Themenbeschreibung, die hier beantwortet werden:

- Welche Speichertechnologie bietet den besten Kompromiss aus Kapazität, Schreibenergie und Firmware-Aufwand für mehrtägige Aufnahmen an einer Knopfzelle?
- Verlängert verlustfreie Kompression oder reduzierte Auflösung die Aufzeichnungsdauer genug, um den Mehraufwand und die Rechenenergie zu rechtfertigen?

## Aufgaben

### Bis M1 – Auswahl

- [ ] Speicherbedarf aus Abtastrate × Dauer in `docs/budgets/budget.py` (Tabelle 2) mit den Zielwerten aus AP0 rechnen; nutzbare Kapazität bei NAND (Bad Blocks, Spare-Bereich) berücksichtigen
- [ ] Kandidaten SPI-NOR vs. SPI-NAND vergleichen: Kapazität, Versorgungsspannungsbereich (muss zur Zelle passen, siehe AP1), Schreib-/Löschstrom und -zeit, Power-Down-Strom, Gehäuse, Firmware-Aufwand (Zephyr-Unterstützung, Bad-Block-Management)
- [ ] Ströme des Speichers je Zustand an AP1 (mit Datenblattquelle)
- [ ] ADR: Speicher (`/decision`)
- [ ] Mit Prof. Cremer klären, welches Format die Analysewerkzeuge des Labors einlesen (F7) → Exportformat
- [ ] Registertabellen/Befehlssatz des Speichers nach `docs/registers/<speicher>.md`

### Bis M2 – Schaltplan

- [ ] `memory.kicad_sch`: Flash mit SPI, Abblockkondensatoren, ggf. Write-Protect/Hold-Beschaltung
- [ ] Pinbelegung mit AP2 abstimmen
- [ ] Symbole/Footprints in `CAP_Memory.kicad_sym` bzw. `CAP.pretty`; ERC ohne Fehler; MR/PR an AP4

### Bis M3 – Firmware und Werkzeug (zuerst auf dem DK mit Breakout-Board)

- [ ] Datenformat im Flash festlegen: Blockaufbau, Header mit Zeitstempel, Prüfsumme, Wiederaufsetzen nach Neustart (NF4) → `docs/architecture/datenformat.md`
- [ ] ADR: einfaches Log vs. Dateisystem
- [ ] Flash in Betrieb nehmen: JEDEC-ID lesen → Seite schreiben/lesen → Sektor löschen → Power-Down
- [ ] Datenablage: Blöcke aus dem RAM-Puffer von AP2 schreiben, Füllstand verwalten
- [ ] BLE-Service: Status (Batterie, Speicher), Steuerung (Start, Uhrzeit setzen, Löschen), Daten-Download → `docs/architecture/ble-protokoll.md`
- [ ] PC-Auslesewerkzeug in Python: verbinden, Status abfragen, Aufnahme starten, Download mit Vollständigkeitsprüfung, Export
- [ ] Kurze Bedienanleitung für Labor und Tierpflege (Pflichtenheft 3.5)

### Bis M4 – Messungen

- [ ] Download-Dauer und Vollständigkeit messen, Datenerhalt nach Spannungsunterbrechung testen (NF4)
- [ ] Kompression/reduzierte Auflösung bewerten (F11): Gewinn an Aufzeichnungsdauer vs. Aufwand

## Schnittstellen

- **Braucht:** Zielwerte (AP0), Spannungsbereich (AP1), Format des RAM-Puffers und Zeitstempel (AP2)
- **Liefert:** Ströme an AP1, Auslesewerkzeug und Export an AP5 (Validierung), Pinbelegung an AP4

## Ergebnisse

- Entscheidung Speicher: `docs/decisions/` (noch offen)
- Datenformat: `docs/architecture/datenformat.md`
- BLE-Protokoll: `docs/architecture/ble-protokoll.md`
- Schaltplan: `hardware/memory.kicad_sch`
- Auslesewerkzeug: `tools/readout/`

## Stand

Nicht begonnen.

## Offene Fragen

- 

## Log

- 
