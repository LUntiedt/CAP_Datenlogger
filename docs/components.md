# Bauteile

Kandidaten und Auswahl je Funktionsblock (Pflichtenheft 3.2.1). Die Auswahl selbst
wird in `docs/decisions/` begründet; hier steht der Überblick mit Datenblatt-Links.

| Block | Kandidaten | Gewählt | ADR | AP |
|---|---|---|---|---|
| Mikrocontroller | nRF54L15 | nRF54L15 | [0001](decisions/0001-mcu-nrf54l15.md) | AP2 |
| Antenne | Funkmodul mit integrierter Antenne; SoC mit Chip-Antenne und Anpassnetzwerk | [offen] | | AP2/AP4 |
| Beschleunigungssensor | LSM6DSV16X (Referenz); reine Beschleunigungssensoren mit FIFO | [offen] | | AP2 |
| Speicher | SPI-NOR; SPI-NAND (Kandidaten im ADR) | [offen] | [0004](decisions/0004-speicher.md) (Entwurf) | AP3 |
| Energiespeicher | CR2032; CR2450; LiPo mit Laderegler | [offen] | | AP1 |
| Pufferung | Kondensatoren, aus gemessenem Pulsstrom dimensioniert | [offen] | | AP1 |
| Weckmechanismus | Reed-Kontakt; Bewegungsmuster über Sensor-Interrupt | [offen] | | AP2/AP5 |
| Zellenhalter | [offen] | [offen] | | AP1 |

## Kandidatenliste mit Eckdaten

Pro Kandidat eine Zeile, Werte mit Quelle (Datenblatt, Seite).

| Bauteil | Hersteller-Nr. | Block | Versorgung | Strom (relevante Zustände) | Gehäuse | Datenblatt | Bemerkung |
|---|---|---|---|---|---|---|---|
| nRF54L15 | | MCU | | | | | |
| LSM6DSV16X | | Sensor | | | | | |
