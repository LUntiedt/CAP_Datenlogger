#!/usr/bin/env bash
# Erzeugt .docx (und optional .pdf) aus den Markdown-Spezifikationen.
# Voraussetzung: pandoc (macOS: brew install pandoc). Für PDF zusätzlich LibreOffice.
# Aufruf aus beliebigem Ordner:  docs/spec/export.sh          -> nur docx
#                                docs/spec/export.sh --pdf    -> docx + pdf
# Ergebnis liegt in docs/spec/export/ (wird nicht committet, siehe .gitignore).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p export
for doc in lastenheft pflichtenheft; do
  # Kopfblock (H1 + Zeilen darunter) und die kursiven Bildunterschriften entfernen:
  # Titel kommt aus den Metadaten, Bildunterschriften aus dem Alt-Text der Bilder.
  awk 'BEGIN{skip=0} /^# /&&!done{skip=1;done=1;next} skip&&/^## /{skip=0} !skip && !/^\*Abbildung/' "$doc.md" |
  pandoc - \
    --from markdown \
    --shift-heading-level-by=-1 \
    --reference-doc=vorlage/reference.docx \
    --resource-path=. \
    --toc --toc-depth=3 \
    -o "export/$doc.docx"
  echo "export/$doc.docx erstellt"
done
if [[ "${1:-}" == "--pdf" ]]; then
  SOFFICE=$(command -v soffice || echo /Applications/LibreOffice.app/Contents/MacOS/soffice)
  "$SOFFICE" --headless --convert-to pdf --outdir export export/*.docx
fi
