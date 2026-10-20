# 0002 – Dokumentation in Markdown

| | |
|---|---|
| **Status** | angenommen |
| **Datum** | 19.10.2026 |
| **AP** | AP0 |
| **Beteiligt** | Laurenz Untiedt |

## Kontext

Lasten- und Pflichtenheft lagen als Markdown-Entwurf und als .docx vor. Das Team
arbeitet mit KI-Assistenten, die das Repository lesen, und mit Git.

## Optionen

| Kriterium | .docx als Original | Markdown als Original |
|---|---|---|
| Änderungen in Git nachvollziehbar | nein (Binärdatei) | ja, zeilenweise |
| Für KI lesbar | eingeschränkt | ja |
| Gleichzeitiges Bearbeiten | Konflikte nicht auflösbar | normale Merge-Konflikte |
| Formatierung/Deckblatt | voll | über Vorlage, ggf. Nacharbeit |

## Entscheidung

Markdown in `docs/spec/` ist das Original. Word/PDF wird mit `docs/spec/export.sh`
(pandoc, Vorlage `docs/spec/vorlage/reference.docx`) erzeugt und nicht committet.

## Begründung

Nachvollziehbare Versionen und direkte Lesbarkeit für alle KI-Assistenten wiegen
schwerer als das Layout. Das Deckblatt des exportierten Dokuments muss ggf. vor der
Abgabe von Hand nachgearbeitet werden.

## Folgen

- Änderungen an Lasten-/Pflichtenheft nur per MR mit Versionssprung.
- Für Abgaben: `docs/spec/export.sh --pdf`.
