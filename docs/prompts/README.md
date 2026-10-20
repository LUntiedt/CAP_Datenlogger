# Prompts

Tool-neutrale Prompt-Texte. Sie stehen **nur hier**; die Dateien in `.claude/commands/`
verweisen darauf.

| Prompt | Claude Code | Codex | Zweck |
|---|---|---|---|
| [ap-start.md](ap-start.md) | `/ap-start AP2` | „Führe `docs/prompts/ap-start.md` für AP2 aus“ | Sitzung an einem AP beginnen |
| [decision.md](decision.md) | `/decision Speicherwahl` | „Führe `docs/prompts/decision.md` aus: Speicherwahl“ | ADR anlegen |
| [datasheet-check.md](datasheet-check.md) | `/datasheet-check LSM6DSV16X` | „Führe `docs/prompts/datasheet-check.md` für LSM6DSV16X aus“ | verwendete Datenblattwerte prüfen |
| [status-update.md](status-update.md) | `/status-update` | „Führe `docs/prompts/status-update.md` aus“ | `STATUS.md` aus den AP-Dateien neu vorschlagen |
| [session-end.md](session-end.md) | `/session-end` | „Führe `docs/prompts/session-end.md` aus“ | AP-Datei vor dem Commit aktualisieren |

`<ARG>` im Text steht für das Argument (AP, Thema, Bauteil).
