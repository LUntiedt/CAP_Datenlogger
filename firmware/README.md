# Firmware

nRF-Connect-SDK-Anwendung (Zephyr, C) für den nRF54L15. Regeln: `AGENTS.md` Abschnitt 8,
Architektur: `docs/architecture/firmware.md`.

**NCS-Version:** [in AP0 festlegen]

## Einrichten

1. VS Code + Erweiterung „nRF Connect for VS Code“ installieren.
2. Darüber Toolchain und nRF Connect SDK in der festgelegten Version installieren.
3. In der Erweiterung *Open an existing application* → Ordner `firmware/`.

## Bauen und Flashen (DK)

In der Erweiterung: *Add build configuration* → Board `nrf54l15dk/nrf54l15/cpuapp` → Build → Flash.

Oder im nRF-Connect-Terminal aus dem Repo-Root:

```bash
west build -b nrf54l15dk/nrf54l15/cpuapp firmware -d firmware/build
west flash -d firmware/build
```

Erwartete Ausgabe auf der seriellen Konsole: `CAP Datenlogger: Firmware-Skelett gestartet`.
Das Skelett ist noch nicht auf echter Hardware getestet – erster Test ist Aufgabe in AP0.

## Aufbau

```
firmware/
├── CMakeLists.txt
├── prj.conf
├── boards/        Devicetree-Overlays (DK) und eigene Board-Definition (Prototyp)
├── src/
│   ├── main.c
│   ├── drivers/   Sensor (AP2), Flash (AP3), Batteriemessung (AP1)
│   ├── services/  Datenablage + BLE (AP3), Power-Management (AP1)
│   └── app/       Zustandsautomat (AP2)
└── tests/
```

Neue `.c`-Dateien in `CMakeLists.txt` unter `target_sources` eintragen.
