# AGENTS.md – CAP Datenlogger

> Gemeinsame Arbeitsregeln für **alle Teammitglieder und ihre KI-Assistenten**.
> - **Codex** liest diese Datei automatisch.
> - **Claude Code** liest sie über `CLAUDE.md` (enthält nur `@AGENTS.md`).
>
> Hier steht, **wie** wir arbeiten. **Was** wir bauen, steht in `docs/` und wird
> von hier nur verlinkt, nicht kopiert. Bei Widerspruch gilt: für Abläufe diese
> Datei, für technische Inhalte das Pflichtenheft bzw. die Entscheidungen in
> `docs/decisions/`. Widersprüche immer melden, nicht stillschweigend auflösen.

---

## 1. Projekt in drei Sätzen

Wir entwickeln einen kleinen, batteriebetriebenen Datenlogger, der am Halsband oder
Geschirr eines Zootiers dreiachsige Beschleunigungsrohdaten aufzeichnet und sie
danach per Bluetooth Low Energy bereitstellt. Auftraggeber ist das ERTS Lab
(Prof. Dr. Markus Cremer, TH Köln), Anwendungspartner der Zoo Wuppertal. Kern der
Arbeit ist der Zielkonflikt zwischen Abtastrate, Energie, Zellgröße, Speicher und
Aufzeichnungsdauer.

## 2. Zuerst lesen (in dieser Reihenfolge)

1. **`STATUS.md`** – aktuelle Phase, nächster Meilenstein, Blocker.
2. **`docs/ap/<eigenes AP>.md`** – Aufgaben, Stand und offene Fragen des Arbeitspakets,
   an dem gerade gearbeitet wird. Fragt die KI nach, welches AP gemeint ist, wenn unklar.
3. Bei Bedarf: `docs/PLAN.md` (Meilensteine, Zeitplan, Abhängigkeiten),
   `docs/spec/pflichtenheft.md` (verbindliche Spezifikation),
   `docs/spec/lastenheft.md` (Anforderungen F1–F11, NF1–NF6),
   `docs/decisions/` (getroffene Entscheidungen).

Die KI liest **nicht** pauschal alle Dateien oder ganze Datenblatt-PDFs, sondern
gezielt das, was für die Aufgabe nötig ist.

## 3. Repository-Aufbau

```
├── AGENTS.md / CLAUDE.md   Arbeitsregeln (diese Datei) / Brücke für Claude Code
├── README.md               Überblick und Einstieg
├── STATUS.md               aktueller Projektstand (1 Seite)
├── .claude/commands/       Slash-Commands für Claude Code (Texte in docs/prompts/)
├── docs/
│   ├── PLAN.md             Meilensteine M0–M5, Zeitplan, Abhängigkeiten
│   ├── spec/               Lastenheft, Pflichtenheft, Themenbeschreibung (Markdown = Original)
│   ├── ap/                 eine Datei pro Arbeitspaket AP0–AP6
│   ├── decisions/          Entscheidungen (ADR), fortlaufend nummeriert
│   ├── architecture/       Systemüberblick, Firmware, Datenformat, BLE-Protokoll
│   ├── budgets/            Energie- und Speicherbudget als Skript
│   ├── components.md       Bauteil-Kandidaten und -Auswahl
│   ├── registers/          Registertabellen aus Datenblättern (Markdown)
│   ├── datasheets/         Datenblätter (PDF)
│   ├── prompts/            tool-neutrale Prompt-Texte
│   ├── meetings/           Protokolle
│   └── report/             Projektbericht, Poster
├── hardware/               KiCad-Projekt, Bibliotheken, BOM, Fertigung, Gehäuse
├── firmware/               nRF-Connect-SDK-/Zephyr-Anwendung (C)
├── tools/readout/          Python-Auslesewerkzeug (BLE, Export)
└── measurements/           Messprotokolle und Messdaten
```

## 4. Sprache

- **Deutsch:** Kommunikation, gesamte Dokumentation, Code-Kommentare, Commit-Beschreibungen.
- **Englisch nur, wo technisch nötig:** Bezeichner im Code (Funktionen, Variablen,
  Dateinamen), Commit-Typen (`feat`, `fix`, …), Branch-Präfixe. Bezeichner ohne Umlaute.
- Die KI antwortet auf Deutsch und erklärt Fachbegriffe beim ersten Auftreten kurz.

## 5. Arbeitsablauf (für jede Sitzung)

1. `git pull` auf `main`, dann eigenen Branch anlegen oder aktualisieren.
2. `STATUS.md` und eigene AP-Datei lesen (Abschnitt 2).
3. Arbeiten. Größere Schritte vorher kurz erklären lassen bzw. erklären.
4. **Vor dem Commit:** eigene AP-Datei aktualisieren (Abschnitt „Stand“, Checkboxen,
   offene Fragen). Wurde etwas entschieden → neue Datei in `docs/decisions/`.
5. Commit, Push, Merge Request bzw. Pull Request nach `main`.

Abkürzung für Schritt 4: `/session-end` (Claude Code) bzw. „Führe `docs/prompts/session-end.md` aus“ (Codex).

Abkürzung: `/ap-start <AP>` (Claude Code) bzw. „Führe `docs/prompts/ap-start.md` für
`<AP>` aus“ (Codex) erledigt Schritt 2 und fasst den Stand zusammen.

### Wer pflegt was

| Datei/Ordner | Wer ändert |
|---|---|
| `docs/ap/apN-*.md` | Verantwortliche/r des AP (andere nur über Kommentar im MR/PR) |
| `STATUS.md` | Laurenz Untiedt, nach Teamterminen und Meilensteinen (`/status-update`) |
| `docs/spec/*` | nur per MR/PR mit Versionssprung und Eintrag im Änderungsprotokoll |
| `docs/decisions/*` | jede/r; einmal angenommene Entscheidungen werden nicht umgeschrieben, sondern durch eine neue ersetzt |
| Schaltplanblatt + Symbolbibliothek eines Blocks | Verantwortliche/r des Blocks (siehe Abschnitt 7) |
| `hardware/*.kicad_pcb`, Root-Schaltplan | AP4 |

## 6. Regeln für die KI

- **Keine geratenen Werte.** Registeradressen, Bitfelder, Stromaufnahmen, Spannungsgrenzen,
  Kapazitäten usw. nur mit Quelle: `docs/registers/…` oder Datenblatt mit Seitenzahl.
  Ist ein Wert nicht belegbar, sagt die KI das und hört an der Stelle auf.
- **Ein Wert, eine Quelle.** Zahlen aus Budgets stehen in `docs/budgets/` und werden
  verlinkt, nicht in mehreren Dateien abgeschrieben.
- **Entscheidungen festhalten.** Jede Bauteil-, Architektur- oder Formatentscheidung
  bekommt einen ADR (`/decision`). Begründungen nicht erfinden: Fehlen sie, als
  `[offen]` markieren und nachfragen.
- **Verstehen vor Übernehmen.** Jede/r muss den eigenen Teil in der Abschlusspräsentation
  erklären können. Die KI erklärt deshalb vor nicht trivialem Code bzw. Schaltungsteilen
  kurz die Logik und die Alternativen; nichts übernehmen, was man nicht erklären kann.
- **Keine Anforderungen erfinden.** Unklares als offene Frage in die AP-Datei eintragen.
- **Nicht in fremden Bereichen arbeiten**, ohne es im MR/PR zu nennen (siehe Abschnitt 5).
- **Diagramme im Pflichtenheft sind Entwürfe.** Abbildung 1 und 2 zeigen eine mögliche
  Umsetzung, keine Vorgabe. Verbindlich sind die Anforderungen und die ADRs.

## 7. Hardware (KiCad)

- **Einheitliche KiCad-Version:** `[in AP0 festlegen, z. B. 9.0.x]`. Dateien, die mit
  einer neueren Version gespeichert wurden, öffnen ältere Versionen nicht.
- **Ein Projekt, ein Schaltplanblatt pro Block:**

  | Blatt | Inhalt | Verantwortlich | Symbolbibliothek |
  |---|---|---|---|
  | `power.kicad_sch` | Zelle, Pufferung, Messshunt, Testpunkte | AP1 (Simon Schiefer) | `lib/CAP_Power.kicad_sym` |
  | `digital.kicad_sch` | nRF54L15, Sensor, Antenne, Weckquelle, Quarz, SWD | AP2 (Peter Wienken, Erik Bremersmann) | `lib/CAP_Digital.kicad_sym` |
  | `memory.kicad_sch` | Flash-Speicher | AP3 (Jan Thiedmann) | `lib/CAP_Memory.kicad_sym` |
  | Root-Blatt + `.kicad_pcb` | Zusammenführung, Layout | AP4 (Laurenz Untiedt) | – |

- **Bibliotheken projektlokal** unter `hardware/lib/`, eingebunden über `${KIPRJMOD}`
  in `sym-lib-table`/`fp-lib-table`. Keine Bauteile aus persönlichen Bibliotheken.
  Footprints liegen gemeinsam in `lib/CAP.pretty/` (eine Datei pro Footprint),
  3D-Modelle in `lib/3d/`.
- **Review:** Jedes Schaltplanblatt, jede Bibliotheksänderung und das Layout gehen per MR/PR
  an AP4 (Laurenz Untiedt).
- **Fertigungsdaten** (Gerber, Bohrdaten, Bestückdaten, BOM) nur bei Freigabe unter
  `hardware/production/vX.Y/`, nicht lose im Projektordner.
- Details: `hardware/README.md`.

## 8. Firmware (nRF Connect SDK / Zephyr)

- **Sprache C**, Zephyr-APIs. Keine Arduino-Bibliotheken, kein C++.
- **NCS-Version:** `[in AP0 festlegen, z. B. v3.x.y]`, alle nutzen dieselbe.
- **Build:** `west build -b nrf54l15dk/nrf54l15/cpuapp firmware` (DK) bzw. später das
  eigene Board; Flashen mit `west flash`. Alternativ über die nRF-Connect-Erweiterung in VS Code.
- **Schichten** laut Pflichtenheft 3.3: `src/drivers/` (Sensor, Flash, Batteriemessung),
  `src/services/` (Datenablage, BLE, Power-Management), `src/app/` (Zustandsautomat).
  Nur der jeweilige Treiber spricht mit seinem Chip.
- **Zephyr-Treiber vs. eigener Treiber** wird je Bauteil per ADR entschieden.
- **Inbetriebnahme in kleinen Schritten:** erst Chip-ID lesen, dann ein Register, dann
  eine Funktion. Nie einen ganzen ungetesteten Treiber auf einmal.
- Details: `docs/architecture/firmware.md`, `firmware/README.md`.

## 9. Git und Merge Requests bzw. Pull Requests

- **Hosting:** vorerst GitHub (https://github.com/LUntiedt/CAP_Datenlogger), später ggf. GitLab der TH.
  „MR/PR“ steht für Merge Request (GitLab) bzw. Pull Request (GitHub).
- `main` ist geschützt; Änderungen nur per MR/PR mit mindestens einem Review.
  Hardware-Review durch AP4, sonst durch eine zweite Person aus dem Team.
- **Branches:** `<typ>/<ap>-<kurz>`, z. B. `feat/ap2-fifo-auslesen`, `docs/ap1-zellauswahl`,
  `hw/ap3-flash-schaltplan`. Kurzlebig, ein Thema pro Branch.
- **Commits:** `typ(bereich): Beschreibung auf Deutsch`
  - Typen: `feat`, `fix`, `docs`, `hw`, `refactor`, `test`, `chore`
  - Bereiche: `ap0`–`ap6`, `power`, `sensor`, `flash`, `ble`, `pcb`, `lib`, `enclosure`, `readout`, `spec`
  - Beispiel: `hw(power): Messshunt mit Testpunkten ergänzt`
- Eine logische Änderung pro Commit. Keine Build-Ausgaben, Backups oder persönlichen
  Einstellungen committen (siehe `.gitignore`).

## 10. Prompts und Commands

| Zweck | Claude Code | Codex |
|---|---|---|
| Arbeit an einem AP beginnen | `/ap-start AP2` | „Führe `docs/prompts/ap-start.md` für AP2 aus“ |
| Entscheidung festhalten | `/decision <Thema>` | „Führe `docs/prompts/decision.md` aus: <Thema>“ |
| Datenblattwerte prüfen | `/datasheet-check <Bauteil>` | „Führe `docs/prompts/datasheet-check.md` für <Bauteil> aus“ |
| Sitzung beenden, AP-Datei aktualisieren | `/session-end` | „Führe `docs/prompts/session-end.md` aus“ |
| Projektstand zusammenfassen | `/status-update` | „Führe `docs/prompts/status-update.md` aus“ |

Die Texte stehen nur einmal in `docs/prompts/`; die Dateien in `.claude/commands/`
verweisen darauf.

## 11. Definition of Done

Eine Aufgabe ist fertig, wenn
- das Ergebnis im Repo liegt (Code baut, Schaltplan besteht ERC, Dokument ist verlinkt),
- verwendete Datenblattwerte belegt sind,
- die AP-Datei aktualisiert und Entscheidungen als ADR festgehalten sind,
- die verantwortliche Person das Ergebnis erklären kann,
- der MR/PR reviewt und nach `main` gemergt ist.
