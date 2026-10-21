# CAP Datenlogger – Miniaturisierter Beschleunigungs-Datenlogger für Tiere

Capstone-Projekt (CAP), WS 26/27, TH Köln · Auftraggeber: ERTS Lab, Prof. Dr. Markus Cremer · Anwendungspartner: Zoo Wuppertal

Ein kleiner, batteriebetriebener Datenlogger zeichnet am Halsband oder Geschirr eines
Tieres dreiachsige Beschleunigungsrohdaten auf und stellt sie anschließend per
Bluetooth Low Energy bereit. Die Daten dienen der Berechnung von ODBA/VeDBA und der
Analyse der Gangperiodizität.

| | |
|---|---|
| Mikrocontroller | Nordic nRF54L15 (BLE) |
| Sensor | Kandidat LSM6DSV16X (Auswahl bis M1) |
| Speicher | SPI-NOR oder SPI-NAND (Auswahl bis M1) |
| Energie | Knopfzelle CR2032/CR2450 oder LiPo (Auswahl bis M1) |
| Werkzeuge | KiCad, nRF Connect SDK (Zephyr), Python |

**Aktueller Stand:** siehe [`STATUS.md`](STATUS.md)

## Einstieg

1. Repository klonen (vorerst GitHub, später ggf. GitLab der TH):
   ```bash
   git clone https://github.com/LUntiedt/CAP_Datenlogger.git cap-datenlogger
   cd cap-datenlogger
   ```
2. [`AGENTS.md`](AGENTS.md) lesen – Arbeitsregeln für Team und KI.
3. Eigene AP-Datei in [`docs/ap/`](docs/ap/) öffnen – dort steht, was zu tun ist.
4. KI im Repo-Ordner starten (`claude` oder `codex`). Sie liest `AGENTS.md` bzw.
   `CLAUDE.md` automatisch. Erster Befehl: `/ap-start AP<n>` (Claude Code) bzw.
   „Führe `docs/prompts/ap-start.md` für AP<n> aus“ (Codex).

## Inhalt

| Ordner | Inhalt |
|---|---|
| [`docs/spec/`](docs/spec/) | Lastenheft, Pflichtenheft, Themenbeschreibung |
| [`docs/PLAN.md`](docs/PLAN.md) | Meilensteine und Zeitplan |
| [`docs/ap/`](docs/ap/) | Arbeitspakete AP0–AP6 |
| [`docs/decisions/`](docs/decisions/) | getroffene Entscheidungen |
| [`hardware/`](hardware/) | KiCad-Projekt, Bibliotheken, Gehäuse |
| [`firmware/`](firmware/) | Firmware (C, Zephyr) |
| [`tools/readout/`](tools/readout/) | Auslesewerkzeug (Python) |
| [`measurements/`](measurements/) | Messprotokolle und Daten |

## Dokumente als Word/PDF

Lasten- und Pflichtenheft werden in Markdown gepflegt. Word-Dateien erzeugt
`docs/spec/export.sh` im Layout der Originalvorlagen (benötigt `pandoc` und `python3`,
für PDF zusätzlich LibreOffice; siehe ADR 0003).
