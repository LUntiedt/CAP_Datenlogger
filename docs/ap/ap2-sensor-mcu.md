# AP2 – Sensor und Mikrocontroller

| | |
|---|---|
| **Verantwortlich** | Peter Wienken, Erik Bremersmann |
| **Zeitraum** | W1–W7 |
| **Bezug** | F1, F2, F3, F8, F9, F10 · Pflichtenheft 3.2.1 (MCU, Antenne, Sensor, Weckmechanismus), 3.3, 3.4 |
| **Schaltplanblatt** | `hardware/digital.kicad_sch` · Symbole in `hardware/lib/CAP_Digital.kicad_sym` |
| **Firmware** | Firmware-Basis: `firmware/src/drivers/` (Sensor), `firmware/src/app/` (Zustandsautomat), Zeitstempel |

## Ziel

Der Sensor tastet mit der festgelegten Abtastrate ab, puffert im FIFO und weckt den
Mikrocontroller per Watermark-Interrupt; jeder Messwert hat einen Zeitbezug; der
Zustandsautomat steuert Lagerung, Bereitschaft, Aufzeichnung und Auslesen.

Forschungsfrage aus der Themenbeschreibung, die hier (mit AP0) beantwortet wird:

- Welche Kombination aus Abtastrate, Auflösung und Duty Cycle erfüllt ODBA/VeDBA und die Gangperiodizitätsanalyse bei geringstem Energie- und Speicherbedarf?

## Aufgaben

### Bis M1 – Auswahl

- [ ] Abtastrate, Auflösung und Messbereich aus ODBA/VeDBA, Gangperiodizität und Bewegungsprofil der Tierart herleiten (mit AP0, O3); Referenzaufnahmen nutzen
- [ ] Sensorkandidaten vergleichen: LSM6DSV16X (Referenz aus dem Vorgängerprojekt) gegen reine Beschleunigungssensoren mit FIFO – Strom bei der gewählten ODR, FIFO-Tiefe und Watermark, Rauschen, Gehäusegröße, Versorgungsspannungsbereich
- [ ] ADR: Sensor (`/decision`). Die Wahl des LSM6DSV16X ist zu begründen, nicht vorauszusetzen
- [ ] ADR 0001 (nRF54L15) vervollständigen: Begründung aus dem Gespräch mit Prof. Cremer eintragen
- [ ] Antenne: Funkmodul mit integrierter Antenne vs. SoC mit Chip-Antenne und Anpassnetzwerk – Fläche, HF-Risiko, Zulassungsfrage (O5); mit AP4 entscheiden, ADR
- [ ] Weckmechanismus: Reed-Kontakt vs. Bewegungsmuster über Sensor-Interrupt; mit AP5 entscheiden, ADR
- [ ] Ströme von MCU und Sensor je Betriebszustand an AP1 (mit Datenblattquelle)
- [ ] Registertabellen des Sensors, die die Firmware braucht, nach `docs/registers/<sensor>.md` übertragen
- [ ] Prüfen, ob der Zephyr-Treiber des gewählten Sensors FIFO mit Watermark-Interrupt unterstützt → ADR „Zephyr-Treiber oder eigener Treiber“

### Bis M2 – Schaltplan

- [ ] `digital.kicad_sch`: nRF54L15 (bzw. Modul) mit Beschaltung laut Referenzdesign, 32,768-kHz-Quarz, Sensor mit Interrupt-Leitung, Weckquelle, SWD-Anschluss, ggf. Status-LED
- [ ] Pinbelegung mit AP3 (SPI für Flash) und AP1 (Batteriemessung) abstimmen und in `docs/architecture/system.md` dokumentieren
- [ ] Symbole/Footprints in `CAP_Digital.kicad_sym` bzw. `CAP.pretty`; ERC ohne Fehler; MR/PR an AP4

### Bis M3 – Firmware-Basis (zuerst auf dem DK mit Breakout-Board)

- [ ] Firmware-Skelett auf dem DK bauen und flashen (`firmware/README.md`)
- [ ] Sensor in Betrieb nehmen: Chip-ID lesen → ODR/Messbereich setzen → Einzelwerte lesen
- [ ] FIFO mit Watermark-Interrupt, Burst-Auslesen in einen RAM-Puffer
- [ ] Zeitbezug: RTC-Zeitstempel je Block, Startzeit vom BLE-Client übernehmen (mit AP3)
- [ ] Sync-Marker zu Beginn der Aufnahme (F9)
- [ ] Zustandsautomat (Pflichtenheft 3.3, Abbildung 2 ist ein Entwurf) in `firmware/src/app/`
- [ ] Übergabeformat RAM-Puffer → Datenablage mit AP3 in `docs/architecture/datenformat.md` festlegen
- [ ] Portierung vom DK auf den Prototyp: eigene Board-Definition unter `firmware/boards/`

### Bis M4 – Messungen

- [ ] Gleichmäßigkeit der Abtastung prüfen (Abstände der Zeitstempel, verlorene Samples)
- [ ] Vergleichsmessung FIFO-Betrieb vs. Wecken pro Messwert (mit AP1)

## Schnittstellen

- **Braucht:** Zielwerte (AP0), Spannungsbereich (AP1), Platz/Antennenfreiraum (AP4), Gehäuse/Weckkonzept (AP5)
- **Liefert:** Ströme an AP1, Datenformat des RAM-Puffers an AP3, Pinbelegung an AP3/AP4

## Ergebnisse

- Entscheidungen: `docs/decisions/0001-mcu-nrf54l15.md`, weitere offen
- Registertabellen: `docs/registers/`
- Schaltplan: `hardware/digital.kicad_sch`
- Firmware: `firmware/src/`

## Stand

Nicht begonnen.

## Offene Fragen

- 

## Log

- 
