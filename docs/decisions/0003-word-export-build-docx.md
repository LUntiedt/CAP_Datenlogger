# 0003 – Word-Export über build_docx.py mit den Originalvorlagen

| | |
|---|---|
| **Status** | angenommen |
| **Datum** | 21.10.2026 |
| **AP** | AP0 |
| **Beteiligt** | Laurenz Untiedt |
| **Anforderungen** | – |
| **Ersetzt** | ADR 0002 im Punkt Export-Vorlage (Markdown bleibt das Original) |

## Kontext

Nach ADR 0002 ist Markdown in `docs/spec/` das Original; Word/PDF wurde mit pandoc
und der Vorlage `docs/spec/vorlage/reference.docx` erzeugt. ADR 0002 nimmt dabei in
Kauf, dass das Deckblatt vor einer Abgabe von Hand nachgearbeitet werden muss.
Lasten- und Pflichtenheft gehen als PDF an den Auftraggeber (Version 0.2); das PDF
wird aus dem exportierten Word-Dokument erzeugt.

## Optionen

| Kriterium | pandoc mit `reference.docx` (bisher) | `build_docx.py` mit Originalvorlagen |
|---|---|---|
| Deckblatt, Kopf-/Fußzeile | Nacharbeit von Hand nötig (ADR 0002) | aus `vorlage/<dokument>-vorlage.docx` |
| Gesamteindruck | sah nicht sauber aus (Einschätzung LU) | Layout der ursprünglichen Word-Dokumente |
| Inhaltsverzeichnis | baute nicht korrekt, Ursache lag bei den Überschriften (Einzelheiten nicht dokumentiert) | wird erzeugt; Seitenzahlen aktualisiert Word beim Öffnen |
| Abhängigkeiten | pandoc | pandoc ≥ 2.10, python3 ≥ 3.8, nur Standardbibliothek |
| Pflegeaufwand | gering (nur Vorlage) | eigenes Skript (ca. 520 Zeilen), muss bei neuen Markdown-Elementen ggf. erweitert werden |

## Entscheidung

`docs/spec/export.sh` ruft `docs/spec/build_docx.py` auf. Das Skript übersetzt das
Markdown mit pandoc nach JSON und setzt es in die Vorlagen
`docs/spec/vorlage/lastenheft-vorlage.docx` bzw. `pflichtenheft-vorlage.docx` ein.
`reference.docx` entfällt. Das Ergebnis liegt weiterhin unter `docs/spec/export/`
und wird nicht committet.

## Begründung

Die exportierten Dokumente sollen ohne Nacharbeit dem Layout der ursprünglichen
Word-Dokumente entsprechen (Deckblatt, Kopf-/Fußzeile, Tabellenoptik), und das
Inhaltsverzeichnis soll korrekt sein. Der pandoc-Export mit `reference.docx` sah
nicht sauber aus (Einschätzung Laurenz Untiedt).

In Kauf genommen: eigener Code, der gepflegt werden muss; Spaltenbreiten und
Bildbreiten stehen als Konstanten im Skript.

## Folgen

- Export braucht zusätzlich `python3` (siehe `README.md`).
- Neue Tabellen im Lasten-/Pflichtenheft bekommen proportionale Spaltenbreiten; feste
  Breiten bei Bedarf in `TABLE_LAYOUT` in `build_docx.py` ergänzen.
- Layoutänderungen am Deckblatt oder an Kopf-/Fußzeile in den `*-vorlage.docx`
  vornehmen, nicht im Markdown.
