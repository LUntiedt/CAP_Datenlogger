# Entscheidungen (ADR)

Jede Bauteil-, Architektur- oder Formatentscheidung bekommt eine eigene Datei
`NNNN-kurzer-titel.md` (fortlaufend nummeriert, Vorlage: `0000-vorlage.md`).
Anlegen am einfachsten mit `/decision <Thema>`.

Regeln:
- Eine angenommene Entscheidung wird nicht umgeschrieben. Ändert sich etwas, gibt es
  einen neuen ADR, und der alte bekommt den Status `ersetzt durch NNNN`.
- Begründungen nicht erfinden; Fehlendes als `[offen]` markieren.
- Zahlen mit Quelle (Datenblatt + Seite oder `docs/budgets/`).

| Nr. | Titel | Status | AP |
|---|---|---|---|
| 0001 | [Mikrocontroller nRF54L15](0001-mcu-nrf54l15.md) | angenommen, Begründung unvollständig | AP2 |
| 0002 | [Dokumentation in Markdown](0002-dokumentation-markdown.md) | angenommen | AP0 |
