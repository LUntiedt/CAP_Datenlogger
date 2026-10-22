# AP1 – Energieversorgung

| | |
|---|---|
| **Verantwortlich** | Simon Schiefer |
| **Zeitraum** | W1–W3, W5–W6, W8–W9 |
| **Bezug** | NF3, NF4 · Pflichtenheft 3.2, 3.2.1 (Energiespeicher, Pufferung), 3.2.2 (Tabelle 1) |
| **Schaltplanblatt** | `hardware/power.kicad_sch` · Symbole in `hardware/lib/00_CAP_Power_SYM.kicad_sym` |
| **Firmware** | `firmware/src/services/power*` (Power-Management), `firmware/src/drivers/battery*` (Batteriemessung) |

## Ziel

Das Gerät läuft die geforderte Aufzeichnungsdauer aus seiner Zelle, übersteht die
Stromspitzen beim BLE-Download ohne Brown-out, und der Strombedarf jedes
Betriebszustands ist gemessen und mit dem Budget abgeglichen.

Forschungsfragen aus der Themenbeschreibung, die hier beantwortet werden:

- Reicht eine Primär-Knopfzelle für einen sinnvollen Feldeinsatz, oder erzwingt die Laufzeit einen Akku mit dem zugehörigen Größennachteil?
- Welche Pufferung braucht eine Knopfzelle, um den BLE-Download ohne Brown-out zu überstehen?
- Wie viel Energie spart der Sensor-FIFO gegenüber dem Wecken pro Messwert? (gemeinsam mit AP2)

## Aufgaben

### Bis M1 – Auswahl und Budget

- [ ] Energiebudget in `docs/budgets/budget.py` aufbauen: Strom je Betriebszustand (Schlafen, Sensor aktiv, FIFO auslesen, Flash schreiben, BLE) × Zeitanteil → mittlerer Strom → Laufzeit. Werte nur aus Datenblättern mit Seitenangabe
- [ ] Ströme von AP2 (MCU, Sensor) und AP3 (Speicher) einsammeln
- [ ] Zellkandidaten vergleichen: CR2032, CR2450, LiPo mit Laderegler – Kapazität bei realistischem Entladestrom, Innenwiderstand/Pulsbelastbarkeit, Entladeschlussspannung, Masse, Maße, Temperatur
- [ ] Spannungsbereich der Zelle über die Entladung an AP3 und AP2 melden (bestimmt, ob alle Bauteile direkt aus der Zelle versorgt werden können)
- [ ] Erste Abschätzung der Pufferkapazität für BLE-Pulse (Strom, Dauer, zulässiger Einbruch), Leckstrom der Kondensatoren berücksichtigen
- [ ] ADR: Wahl des Energiespeichers (`/decision`)
- [ ] Zellenhalter auswählen und Maße an AP4/AP5 geben

### Bis M2 – Schaltplan

- [ ] `power.kicad_sch` zeichnen: Zellenhalter, Verpolschutz falls nötig, Pufferkapazität, Messshunt mit Jumper/Testpunkten, ggf. Batteriespannungsmessung (Spannungsteiler mit schaltbarem Pfad o. Ä.)
- [ ] Symbole/Footprints in `00_CAP_Power_SYM.kicad_sym` bzw. `00_CAP_FTP.pretty` anlegen
- [ ] ERC ohne Fehler, MR/PR an AP4

### Bis M3 – Firmware

- [ ] Batteriespannung messen (SAADC des nRF54L15) und als Status bereitstellen (F10)
- [ ] Unterspannungsschwelle: Aufnahme sauber beenden, bevor Daten gefährdet sind (NF4)
- [ ] Power-Management mit AP2 abstimmen: Peripherie abschalten, Schlafmodi

### Bis M4 – Messungen

- [ ] Strom je Betriebszustand über den Messshunt messen (Strommesstechnik des Labors), Protokoll in `measurements/protocols/`
- [ ] Spannungseinbruch beim BLE-Download messen, Pufferung ggf. anpassen
- [ ] Laufzeit hochrechnen und – wenn zeitlich möglich – an der Zelle bestätigen; Abgleich mit dem Budget
- [ ] Vergleichsmessung FIFO-Betrieb vs. Wecken pro Messwert (mit AP2)

## Schnittstellen

- **Braucht:** Zielwerte (AP0), Ströme der Bauteile (AP2, AP3), Platz auf der Platine (AP4)
- **Liefert:** Spannungsbereich an AP2/AP3, Zellenmaße an AP4/AP5, Energiebudget an alle

## Ergebnisse

- Budget: `docs/budgets/`
- Entscheidung Energiespeicher: `docs/decisions/` (noch offen)
- Schaltplan: `hardware/power.kicad_sch`
- Messprotokolle: `measurements/protocols/`

## Stand

Nicht begonnen.

## Offene Fragen

- 

## Log

- 
