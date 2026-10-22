# 0004 – Speicher: SPI-NOR oder SPI-NAND

| | |
|---|---|
| **Status** | vorgeschlagen (Entwurf, Bewertung offen) |
| **Datum** | 22.10.2026 |
| **AP** | AP3 |
| **Beteiligt** | Jan Thiedmann |
| **Anforderungen** | F4, F5, F11, NF3, NF4 |

## Kontext

Die Messdaten werden nichtflüchtig in einem externen Flash über SPI abgelegt
(Pflichtenheft 3.2.1, 3.4). Zur Wahl stehen SPI-NOR und SPI-NAND. Die Kapazität
bestimmt zusammen mit der Abtastrate die Aufzeichnungsdauer (Pflichtenheft Tabelle 2,
[`docs/budgets/budget.py`](../budgets/budget.py)): Ein kleiner NOR-Flash reicht bei
50 Hz für weniger als einen Tag, mehrtägige Aufnahmen brauchen NAND, eine geringere
Abtastrate oder Datenreduktion (F11).

Randbedingungen:

- **Zielwerte fehlen noch:** Abtastrate und Aufzeichnungsdauer kommen aus AP0 (O3).
  Daraus folgt die Mindestkapazität.
- **Versorgung direkt aus der Zelle** (Pflichtenheft 3.2): Der Speicher muss bis zur
  Entladeschlussspannung der gewählten Zelle spezifiziert sein. Spannungsbereich der
  Zelle kommt aus AP1 [offen].
- **Energie:** Ströme je Zustand gehen ins Energiebudget von AP1. Während der Aufnahme
  liegt der Flash die meiste Zeit im Power-Down (Pflichtenheft 3.3), der Power-Down-Strom
  zählt also über die gesamte Laufzeit.
- **NF4:** Ein Spannungseinbruch darf gespeicherte Daten nicht unbrauchbar machen.

## Grundsätzliche Unterschiede

Qualitativ; Zahlen stehen in den Kandidatentabellen mit Quelle.

| Kriterium | SPI-NOR | SPI-NAND |
|---|---|---|
| Typische Kapazität | klein bis mittel | groß |
| Schreiben/Löschen | seitenweise schreiben, sektorweise (4 KB) löschen | seitenweise schreiben, nur blockweise (128 KB) löschen |
| Fehlerbehandlung | keine nötig | ECC und Verwaltung defekter Blöcke (Bad Blocks) nötig; bei allen drei Kandidaten ECC im Chip |
| Nutzbare Kapazität | Nennkapazität | Nennkapazität abzüglich ungültiger Blöcke (garantiert sind mindestens 1004 von 1024) |
| Ruhezustand | Power-down-Modus | bei allen drei Kandidaten kein Power-down-Modus im Datenblatt, niedrigster Zustand ist Standby |
| Zephyr-Unterstützung | generischer Treiber `jedec,spi-nor` vorhanden | [offen: prüfen, ob es in der verwendeten NCS-Version einen Treiber gibt; sonst eigener Treiber] |
| Firmware-Aufwand | gering | höher (Bad-Block-Tabelle, ECC-Status auswerten, größere Löschblöcke im Datenformat berücksichtigen) |

## Kandidaten

Datenblätter liegen unter [`docs/datasheets/`](../datasheets/). **Seitenangaben sind
die im Datenblatt gedruckten Seitenzahlen** (bei Winbond eins weniger als die
PDF-Seitenzahl). Ströme als „typ. / max.“; Bedingungen für typische Werte stehen in
der Fußnote der jeweiligen DC-Tabelle (meist 25 °C, Nennspannung). Max.-Werte für
Standby/Power-down bei Industrial-Temperaturbereich bis 85 °C.

### SPI-NOR

| Kriterium | Macronix MX25R6435F | Winbond W25Q64JW | Winbond W25Q256JW |
|---|---|---|---|
| Datenblatt | [`mx25r6435f_rev1.6.pdf`](../datasheets/mx25r6435f_rev1.6.pdf), Rev. 1.6, 08.08.2022 | [`w25q64jw_revg.pdf`](../datasheets/w25q64jw_revg.pdf), Rev. G, 28.04.2026 | [`w25q256jw_revk.pdf`](../datasheets/w25q256jw_revk.pdf), Rev. K |
| Kapazität | 64 Mbit = 8 MiB (S. 1) | 64 Mbit = 8 MiB (S. 4) | 256 Mbit = 32 MiB (S. 5) |
| Versorgungsspannung | 1,65–3,6 V (S. 1, S. 66 Anm. 1) | 1,7–1,95 V (S. 58) | 1,7–1,95 V (S. 78) |
| Strom Power-down | 0,007 / 0,35 µA (S. 66) | 0,1 / 5 µA (S. 61) | 1 / 15 µA (S. 81) |
| Strom Standby | 5 / 24 µA (S. 66) | 5 / 25 µA (S. 61) | 10 / 35 µA (S. 81) |
| Strom Lesen | 2,2 / 4 mA bei 33 MHz (S. 66) | 8 / 10 mA bei 50 MHz (S. 61) | 6 / 8 mA bei 50 MHz (S. 81) |
| Strom Seite schreiben | 3,5 / 6 mA (S. 66) | 15 / 20 mA (S. 61) | 12 / 20 mA (S. 81) |
| Zeit Seite schreiben | 3,2 / 10 ms (S. 75) | 0,8 / 3 ms (S. 64) | 0,8 / 5 ms (S. 84) |
| Strom Sektor löschen | 3,1 / 6 mA (S. 66) | 15 / 20 mA (S. 61) | 12 / 20 mA (S. 81) |
| Zeit Sektor (4 KB) löschen | 58 / 240 ms (S. 75) | 45 / 400 ms (S. 64) | 50 / 400 ms (S. 84) |
| Seitengröße / Sektorgröße | 256 B (S. 50) / 4 KB (S. 6) | 256 B / 4 KB (S. 4) | 256 B / 4 KB (S. 5) |
| Aufwachzeit aus Power-down | tRDP 35 µs (S. 68) | tRES1 max. 30 µs (S. 64) | tRES1 max. 30 µs (S. 84) |
| Gehäuse | 8-WSON 6×5 mm, 8-USON 4×4 mm und 4×3 mm, 8-SOP 200 mil, 22-WLCSP (S. 5) | u. a. 8-USON 4×3 mm, 8-XSON 4×4 mm, 8-WSON 6×5/8×6 mm, 24-TFBGA 8×6 mm (S. 4) | 8-WSON 6×5/8×6 mm, 24-TFBGA 8×6 mm (S. 5) |
| Bemerkung | Werte für Ultra-Low-Power-Modus (Werkseinstellung laut Bestellcode „…IL0“, S. 77); typ. bei 1,8 V. Im Zephyr-Boardfile des nRF54L15 DK als `jedec,spi-nor` eingetragen (siehe Folgen) | typ. bei 1,8 V | typ. bei 1,8 V |

### SPI-NAND

| Kriterium | Winbond W25N01GW | Winbond W25N01GV | GigaDevice GD5F1GQ5UE |
|---|---|---|---|
| Datenblatt | [`w25n01gw_revg.pdf`](../datasheets/w25n01gw_revg.pdf), Rev. G, 17.05.2021 | [`w25n01gv_revq.pdf`](../datasheets/w25n01gv_revq.pdf), Rev. Q, 17.05.2021 | [`gd5f1gq5ue_rev1.6.pdf`](../datasheets/gd5f1gq5ue_rev1.6.pdf), Rev. 1.6, August 2024 |
| Kapazität nominal | 1 Gbit, 1024 Blöcke (S. 6) | 1 Gbit, 1024 Blöcke (S. 6) | 1 Gbit, 1024 Blöcke (S. 10, S. 58) |
| Garantiert gültige Blöcke | mind. 1004 (S. 63) | mind. 1004 (S. 63) | mind. 1004 (S. 58) |
| Versorgungsspannung | 1,70–1,95 V (S. 56) | 2,7–3,6 V (S. 56) | 2,7–3,6 V (S. 4, S. 6) |
| Strom Power-down | kein Power-down-Modus | kein Power-down-Modus | kein Power-down-Modus |
| Strom Standby | 10 / 50 µA (S. 58) | 10 / 50 µA (S. 58) | 15 / 50 µA (S. 66) |
| Strom Lesen | 25 / 35 mA (S. 58) | 25 / 35 mA (S. 58) | 15 / 30 mA bei 133 MHz (S. 66) |
| Strom Seite schreiben | 25 / 35 mA (S. 58) | 25 / 35 mA (S. 58) | 15 / 30 mA (S. 66) |
| Zeit Seite schreiben | 250 / 700 µs (S. 61) | 250 / 700 µs (S. 61) | 400 / 600 µs mit ECC (S. 68) |
| Strom Block löschen | 25 / 35 mA (S. 58) | 25 / 35 mA (S. 58) | 15 / 30 mA (S. 66) |
| Zeit Block löschen | 2 / 10 ms (S. 61) | 2 / 10 ms (S. 61) | 3 / 10 ms (S. 68) |
| Seitengröße / Blockgröße | 2048 B (+ 64 B Spare, 2112-B-Puffer, S. 39) / 64 Seiten = 128 KB (S. 6) | 2048 B (+ 64 B Spare, S. 39) / 128 KB (S. 6) | 2048 B + 64 B (ECC an) bzw. + 128 B (ECC aus) / 64 Seiten (S. 4, S. 10) |
| ECC im Chip / Bad-Block-Verwaltung | 1 Bit ECC, Bad-Block-Management mit LUT (S. 6) | 1 Bit ECC (S. 6) | 4 Bit je 528 B (S. 4) |
| Gehäuse | 8-WSON 8×6 mm, 16-SOIC 300 mil, 24-TFBGA 8×6 mm (S. 7) | 8-WSON 8×6 mm, 16-SOIC 300 mil, 24-TFBGA 8×6 mm (S. 7) | 8-WSON 8×6 mm (S. 6) |
| Bemerkung | typ. bei 1,8 V | typ. bei 3,0 V | 1,8-V-Variante GD5F1GQ5RE existiert, Datenblatt nicht geladen |

## Erste Beobachtungen

Nur aus den Tabellen oben abgeleitet, noch keine Wertung:

1. **Spannung:** Nur der MX25R6435F deckt mit 1,65–3,6 V den Bereich einer Lithium-Knopfzelle
   ab. Die 1,8-V-Typen (W25Q64JW, W25Q256JW, W25N01GW) brauchen einen eigenen Spannungsregler.
   Die 3-V-Typen (W25N01GV, GD5F1GQ5UE) verlangen mindestens 2,7 V; ob das bis zur
   Entladeschlussspannung der Zelle reicht, hängt an AP1.
2. **Ruhestrom:** Die NAND-Kandidaten haben keinen Power-down-Modus. Ihr Standby-Strom
   (typ. 10–15 µA, max. 50 µA) liegt um Größenordnungen über dem Power-down-Strom der
   NOR-Kandidaten und fließt über die ganze Aufnahme. Eine Möglichkeit wäre, den Speicher
   zwischen den Schreibvorgängen über einen Lastschalter abzuschalten (mit AP1 klären).
3. **Kapazität:** Die NOR-Kandidaten haben 8 oder 32 MiB, die NAND-Kandidaten 1 Gbit,
   davon mindestens 1004 von 1024 Blöcken nutzbar. Die nutzbare NAND-Kapazität gehört
   noch in `budget.py`.
4. **Schreibenergie:** NAND schreibt eine 2-KB-Seite in 250–700 µs, NOR eine 256-B-Seite
   in 0,8–10 ms. Energie je geschriebenem Byte erst im Budget vergleichen.

## Bewertung

[offen: erst nach den Zielwerten aus AP0 und dem Spannungsbereich aus AP1.
Vorgehen: Mindestkapazität aus `budget.py` → Kandidaten mit passendem Spannungsbereich
→ Energie je geschriebenem Byte und Ruhestrom im Energiebudget → Firmware-Aufwand.]

## Entscheidung

[offen]

## Begründung

[offen]

## Folgen

- AP1: Ströme je Zustand des gewählten Speichers gehen ins Energiebudget.
- AP2/AP4: SPI-Pinbelegung und Platzbedarf des Gehäuses.
- AP3: Treiber (Zephyr oder eigener, siehe AGENTS.md §8), Blockgröße im Datenformat
  (`docs/architecture/datenformat.md`), Registertabelle in `docs/registers/`.
- Inbetriebnahme auf dem DK: Das Zephyr-Boardfile des nRF54L15 DK
  (`boards/nordic/nrf54l15dk/nrf54l_05_10_15_cpuapp_common.dtsi`, Zephyr `main`,
  Stand 22.10.2026) enthält einen MX25R6435F als `jedec,spi-nor`. Damit lässt sich
  der Flash-Treiber für NOR ohne Breakout-Board testen. In der festgelegten NCS-Version
  und am DK im Labor prüfen.
