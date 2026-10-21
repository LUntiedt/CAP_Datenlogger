#!/usr/bin/env bash
# Erzeugt Lasten- und Pflichtenheft als .docx (optional zusätzlich .pdf) aus den
# Markdown-Quellen in diesem Ordner.
#
# Voraussetzungen: pandoc (Installer: github.com/jgm/pandoc/releases) und python3.
# Für --pdf zusätzlich LibreOffice. Besser: .docx in Word öffnen und dort als PDF speichern.
#
# Aufruf:  docs/spec/export.sh          -> export/lastenheft.docx, export/pflichtenheft.docx
#          docs/spec/export.sh --pdf    -> zusätzlich PDF
#
# Layout (Deckblatt, Kopf-/Fußzeile, Tabellen) kommt aus vorlage/<dokument>-vorlage.docx,
# der Inhalt aus <dokument>.md. Umsetzung: build_docx.py.
# Ergebnis liegt in docs/spec/export/ (wird nicht committet, siehe .gitignore).
set -euo pipefail
cd "$(dirname "$0")"
python3 build_docx.py lastenheft pflichtenheft
if [[ "${1:-}" == "--pdf" ]]; then
  SOFFICE=$(command -v soffice || echo /Applications/LibreOffice.app/Contents/MacOS/soffice)
  "$SOFFICE" --headless --convert-to pdf --outdir export export/*.docx
fi
