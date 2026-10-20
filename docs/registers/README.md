# Registertabellen

Die Register, die die Firmware braucht, werden **einmal** aus dem Datenblatt in eine
Markdown-Datei pro Bauteil übertragen (z. B. `lsm6dsv16x.md`, `<flash>.md`). Firmware
und KI arbeiten gegen diese Dateien statt gegen das ganze PDF.

Pro Register: Adresse, Name, Bitfelder, Reset-Wert, Bedeutung, **Quelle (Datenblatt-Revision, Seite)**.

```markdown
## 0x10 CTRL1 (Quelle: LSM6DSV16X Datenblatt Rev. X, S. NN)
| Bit | Name | Bedeutung |
|---|---|---|
| 3:0 | ODR_XL | ... |
```

Fehlt ein Register, wird es zuerst hier ergänzt und dann im Code verwendet.
Prüfen mit `/datasheet-check <Bauteil>`.
