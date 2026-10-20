#!/usr/bin/env python3
"""Energie- und Speicherbudget des CAP-Datenloggers.

Reproduziert Tabelle 1 und 2 des Pflichtenhefts (Abschnitt 3.2.2) und ist der Ort,
an dem AP1 (Energie) und AP3 (Speicher) ihre Budgets weiter ausbauen.

Regel: Jeder Bauteilwert bekommt eine Quelle (Datenblatt + Seite) im Kommentar.
Aufruf: python3 docs/budgets/budget.py
"""

# --- Zellen: Nennkapazität in mAh (Quelle: Themenbeschreibung, Richtwerte) ---------
CELLS_MAH = {
    "CR2032": 225,   # ca.-Wert laut Themenbeschreibung; Datenblatt der gewählten Zelle nachtragen
    "CR2450": 620,   # ca.-Wert laut Themenbeschreibung; Datenblatt nachtragen
}
RUNTIMES_H = {"24 h": 24, "7 Tage": 7 * 24, "30 Tage": 30 * 24}

# --- Speicher: Kapazität in Byte (Nennwert, ohne Bad Blocks / Spare-Bereich) -------
MIB = 1024 * 1024
MEMORIES_BYTE = {
    "8 MiB SPI-NOR": 8 * MIB,
    "32 MiB SPI-NOR": 32 * MIB,
    "128 MiB SPI-NAND": 128 * MIB,
}

# --- Datenrate: 3 Achsen x 16 Bit = 6 Byte pro Abtastung, ohne Zeitstempel/Header ---
AXES = 3
BYTES_PER_AXIS = 2
RATES_HZ = [25, 50, 100]


def allowed_current_ma(capacity_mah: float, runtime_h: float) -> float:
    """Zulässiger mittlerer Strom für eine Laufzeit (ohne Abschläge)."""
    return capacity_mah / runtime_h


def bytes_per_second(rate_hz: float) -> float:
    return rate_hz * AXES * BYTES_PER_AXIS


def recording_hours(capacity_byte: float, rate_hz: float) -> float:
    return capacity_byte / bytes_per_second(rate_hz) / 3600


def fmt_duration(hours: float) -> str:
    """Wie im Pflichtenheft: ab 48 h in Tagen, sonst in Stunden."""
    if hours >= 48:
        return f"{hours / 24:.1f} Tage".replace(".", ",")
    return f"{hours:.1f} h".replace(".", ",")


def table1() -> None:
    print("Tabelle 1: Zulässiger mittlerer Strom je Zelle und Laufzeit")
    print("| Zelle | " + " | ".join(RUNTIMES_H) + " |")
    print("|---" * (len(RUNTIMES_H) + 1) + "|")
    for cell, mah in CELLS_MAH.items():
        cols = [f"{allowed_current_ma(mah, h):.2f} mA".replace(".", ",") for h in RUNTIMES_H.values()]
        print(f"| {cell} ({mah} mAh) | " + " | ".join(cols) + " |")
    print()


def table2() -> None:
    print("Tabelle 2: Aufzeichnungsdauer ohne Kompression (3 Achsen x 16 Bit)")
    print("| Speicher | " + " | ".join(f"{r} Hz ({bytes_per_second(r):.0f} B/s)" for r in RATES_HZ) + " |")
    print("|---" * (len(RATES_HZ) + 1) + "|")
    for mem, cap in MEMORIES_BYTE.items():
        cols = [fmt_duration(recording_hours(cap, r)) for r in RATES_HZ]
        print(f"| {mem} | " + " | ".join(cols) + " |")
    print()
    for r in RATES_HZ:
        print(f"Datenmenge pro Tag bei {r} Hz: {bytes_per_second(r) * 86400 / 1e6:.1f} MB")


# --- Platz für AP1: Strom je Betriebszustand (alle Werte mit Quelle!) -------------
# STATES = {
#     # Zustand: (Strom in mA, Zeitanteil 0..1)   # Quelle
#     "Schlafen + Sensor aktiv": (None, None),      # [offen]
#     "FIFO auslesen":            (None, None),      # [offen]
#     "Flash schreiben":          (None, None),      # [offen]
# }

if __name__ == "__main__":
    table1()
    table2()
