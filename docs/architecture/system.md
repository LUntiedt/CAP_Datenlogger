# Systemüberblick

> **Entwurf, nicht bindend.** Die Diagramme entsprechen Abbildung 1 und 2 des
> Pflichtenhefts und zeigen eine mögliche Umsetzung. Wie die Blöcke tatsächlich
> umgesetzt werden, legen die APs fest; Änderungen hier nachziehen und per ADR
> begründen. Für die AP-Zuordnung gilt Pflichtenheft 3.2.1.

## Hardware-Blöcke

```mermaid
flowchart TB
  subgraph AP1[AP1 Energieversorgung]
    CELL[Zelle<br/>CR2032 / CR2450 / LiPo] -->|VBAT| CAP[Pufferkapazität]
    CAP -->|VBAT| SHUNT[Messshunt + Testpunkte]
  end
  subgraph AP2[AP2 Sensor und Mikrocontroller]
    IMU[Beschleunigungssensor<br/>mit FIFO]
    MCU[nRF54L15<br/>BLE, RTC, Deep Sleep]
    XTAL[32,768-kHz-Quarz] --> MCU
    SWD[SWD] --> MCU
    WAKE[Weckquelle<br/>Reed / Sensor-INT] --> MCU
    ANT[2,4-GHz-Antenne]
  end
  subgraph AP3[AP3 Speicher]
    FLASH[Flash<br/>SPI-NOR / SPI-NAND]
  end
  SHUNT -->|VDD| MCU
  SHUNT -->|VDD| IMU
  SHUNT -->|VDD| FLASH
  IMU <-->|SPI/I²C + INT Watermark| MCU
  MCU <-->|SPI| FLASH
  MCU --- ANT
  ANT -.->|BLE-Download| PC[PC-Auslesewerkzeug]
```

## Betriebszustände

```mermaid
stateDiagram-v2
  LAGERUNG: LAGERUNG (System OFF, Sensor/Flash Power-Down)
  BEREIT: BEREIT (BLE aktiv: Status, Konfiguration)
  AUFZEICHNUNG: AUFZEICHNUNG (BLE aus, MCU schläft, Weckung per FIFO-INT)
  ENDE: ENDE (Speicher voll / Unterspannung)
  AUSLESEN: AUSLESEN (BLE-Download aktiv)
  LAGERUNG --> BEREIT: Weckereignis
  BEREIT --> LAGERUNG: Timeout
  BEREIT --> AUFZEICHNUNG: Start + Zeitstempel + Sync-Marker
  AUFZEICHNUNG --> ENDE: Speicher voll / VBAT < Schwelle
  AUFZEICHNUNG --> AUSLESEN: Weckereignis
  ENDE --> AUSLESEN: Weckereignis
  AUSLESEN --> BEREIT: Download abgeschlossen
```

## Datenpfad

Sensor-FIFO → Interrupt bei Watermark → Burst-Auslesen in RAM-Puffer → blockweises
Schreiben in den Flash → (nach der Aufnahme) BLE-Download → PC-Werkzeug → Export.

## Pinbelegung

| Signal | nRF54L15-Pin | Block | Festgelegt von |
|---|---|---|---|
| [offen] | | | AP2/AP3/AP1 |
