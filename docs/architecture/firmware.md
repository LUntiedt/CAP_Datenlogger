# Firmware-Architektur

> Wird von AP2 und AP3 gefüllt. Grundlage: Pflichtenheft 3.3.

## Schichten

| Schicht | Ordner | Inhalt | AP |
|---|---|---|---|
| Plattform | Zephyr, Devicetree (`firmware/boards/`) | Hardware-Abstraktion, Board-Definition | AP2 |
| Treiber | `firmware/src/drivers/` | Sensor, Flash, Batteriemessung | AP2, AP3, AP1 |
| Dienste | `firmware/src/services/` | Datenablage, BLE, Power-Management | AP3, AP1 |
| Anwendung | `firmware/src/app/` | Zustandsautomat | AP2 |

Regel: Nur ein Treiber spricht mit seinem Chip. Andere Module nutzen die Treiber-API.

## Entscheidungen

- Zephyr-Treiber oder eigener Treiber je Bauteil: [offen, ADR]
- Log vs. Dateisystem: [offen, ADR, AP3]

## Threads, Interrupts, Energiesparen

[offen]
