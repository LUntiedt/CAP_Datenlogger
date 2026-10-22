# AP4 – Leiterplatte

| | |
|---|---|
| **Verantwortlich** | Laurenz Untiedt |
| **Zeitraum** | W3–W7 (Vorbereitung ab W1) |
| **Bezug** | NF1, NF6 · Pflichtenheft 3.1, 3.2, 2.5 (Inbetriebnahme) |
| **Dateien** | `hardware/datenlogger.kicad_pro`, Root-Schaltplan, `hardware/datenlogger.kicad_pcb`, `hardware/lib/`, `hardware/production/` |

## Ziel

Eine kompakte, fertigbare Leiterplatte mit allen Funktionsblöcken ist entworfen,
gefertigt, bestückt und in Betrieb genommen.

## Aufgaben

### Bis M1 – Vorbereitung

- [x] KiCad-Projekt `hardware/datenlogger.kicad_pro` anlegen, hierarchische Blätter `power`, `digital`, `memory` einbinden, Bibliothekstabellen prüfen (`hardware/README.md`)
- [ ] Fertiger festlegen (Unterstützung durch das Labor klären) und dessen Designregeln/Lagenaufbau als DRC-Regeln hinterlegen
- [ ] Mit AP2 Antennenkonzept entscheiden (Modul vs. Chip-Antenne) und Freiraum im Layout vorsehen
- [ ] Mit AP1/AP5 Platinenumriss und Zellenhalter festlegen

### Bis M2 – Zusammenführung und Layout

- [ ] Schaltplanblätter von AP1, AP2, AP3 reviewen (MR/PR), Netznamen und Schnittstellen zwischen den Blättern prüfen
- [ ] ERC des Gesamtschaltplans ohne Fehler
- [ ] Layout: minimale Fläche und Masse, Antennenbereich frei von Kupfer/Metall, Messshunt und Testpunkte zugänglich, SWD erreichbar, Achsrichtungen des Sensors im Bestückungsdruck
- [ ] DRC ohne Fehler, Review mit mindestens einer weiteren Person
- [ ] BOM mit Bezugsquellen und Verfügbarkeit in `hardware/bom/`
- [ ] Fertigungsdaten nach `hardware/production/v1.0/`, Git-Tag `hw-v1.0`, Bestellung (M2)

### Bis M3 – Bestückung und Inbetriebnahme

- [ ] Bestückung (mit Unterstützung des Labors)
- [ ] Inbetriebnahme laut Pflichtenheft 2.5: Sichtprüfung, Smoke-Test am strombegrenzten Netzteil, Programmierung über SWD
- [ ] Fehler und Änderungswünsche für eine mögliche Revision in `hardware/README.md` (Abschnitt Errata) sammeln

## Schnittstellen

- **Braucht:** Schaltplanblätter von AP1, AP2, AP3; Gehäusemaße von AP5
- **Liefert:** Platinenmaße an AP5, bestückten Prototyp an alle

## Ergebnisse

- KiCad-Projekt: `hardware/`
- BOM: `hardware/bom/`
- Fertigungsdaten: `hardware/production/`

## Stand

KiCad-Projekt (10.0) mit Root-Blatt und den Blättern `power`, `digital`, `memory` angelegt. Projektbibliotheken auf `00_CAP_*` umbenannt, gemeinsame Bibliothek `00_CAP_Common_SYM` aus dem PowerBank-Projekt übernommen, Ablauf zum Anlegen von Bauteilen in `hardware/README.md` beschrieben (PR #2).

## Offene Fragen

- Fertiger und Bestückung über das Labor?
- `00_CAP_Common_SYM` enthält auch PowerBank-spezifische Teile (ESP32-C3, BQ25792, FUSB302 …). Aussortieren, sobald klar ist, was im Datenlogger gebraucht wird. Beim CSD17581Q3A fehlt im Footprint-Feld der Bibliotheksname, ein Symbol hat keinen Footprint.

## Log

- 22.10.2026: KiCad-Projekt mit hierarchischen Blättern angelegt, Bibliotheken auf `00_CAP_*` umbenannt, Bauteil-Ablauf ins Hardware-README (PR #2).
