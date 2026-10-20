# datasheet-check

Prüfe alle Werte zu **<ARG>**, die im Repository verwendet werden.

1. Suche nach <ARG> in `firmware/`, `docs/budgets/`, `docs/architecture/`, `docs/components.md`
   und den AP-Dateien.
2. Prüfe jeden gefundenen Wert (Registeradresse, Bitfeld, Strom, Spannung, Zeit) gegen
   `docs/registers/<bauteil>.md` bzw. das Datenblatt in `docs/datasheets/`
   (gezielt die betreffenden Seiten, nicht das ganze PDF).
3. Ausgabe als Tabelle: Fundstelle | Wert | Quelle | Status (✅ belegt / ❌ abweichend / ⚠️ ohne Quelle).
4. Ändere nichts automatisch. Schlage Korrekturen vor und frage nach.
