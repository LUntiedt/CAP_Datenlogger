#!/usr/bin/env python3
"""Baut Lasten- und Pflichtenheft als .docx aus den Markdown-Quellen.

Das Layout (Deckblatt, Kopf-/Fußzeile, Schriften, Tabellenoptik) stammt aus den
Vorlagen in vorlage/<dokument>-vorlage.docx. Der Inhalt kommt vollständig aus
<dokument>.md. Markdown wird mit pandoc nach JSON übersetzt und hier in Word-XML
umgesetzt. Nur Python-Standardbibliothek, keine Zusatzpakete.

Aufruf (aus docs/spec/):  python3 build_docx.py lastenheft [pflichtenheft ...]
Voraussetzung:            pandoc >= 2.10, python3 >= 3.8
Ergebnis:                 export/<dokument>.docx
"""
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Layout-Konstanten
TEXT_WIDTH = 9070                     # nutzbare Breite in twips (A4, Ränder der Vorlage)
BORDER = "A6A6A6"
HEAD_FILL = "DCE9F2"
CELL_SZ = 19                          # halbe Punkte
GANTT_COLORS = ["DCE9F2", "F8DCDC", "FCEFD9", "E8DAEF", "D6EAF8", "E3EFE3", "E5E7E9"]
NUM_BULLET, NUM_CELL_BULLET, NUM_DECIMAL_ABS = 2, 3, 4
IMAGE_WIDTH_EMU = {"abb1_blockdiagramm.png": 4000500, "abb2_betriebszustaende.png": 3810000}
DEFAULT_IMAGE_WIDTH_EMU = 3810000

# Spaltenbreiten und fette erste Spalte je Tabelle (Schlüssel: Kopfzeile),
# übernommen aus den ursprünglichen Word-Dokumenten.
TABLE_LAYOUT = {
    ("Version", "Änderungen", "Datum", "Geändert von"): ([1000, 4870, 1500, 1700], False),
    ("Begriff", "Erläuterung"): ([2300, 6770], True),
    ("Zielwert", "Hergeleitet aus", "AP"): ([2700, 5170, 1200], True),
    ("Testgruppe", "Inhalt", "Anforderungen"): ([1900, 5170, 2000], True),
    ("Block", "Kandidaten", "Kriterien", "AP"): ([1900, 2970, 3500, 700], True),
    ("Risiko", "Gegenmaßnahme"): ([4000, 5070], False),
    ("AP", "Arbeitspaket", "Inhalt / Ergebnis", "Verantwortlich"): ([650, 2150, 4570, 1700], True),
    ("Rolle", "Name", "Datum", "Unterschrift"): ([1800, 3870, 1500, 1900], False),
    ("Prio", "Stufe", "Bedeutung"): ([800, 1200, 7070], False),
    ("ID", "Prio", "Anforderung"): ([900, 700, 7470], True),
    ("MS", "Ergebnis", "Termin"): ([800, 6270, 2000], True),
    ("Nr.", "Offener Punkt", "Klärung bis"): ([700, 6370, 2000], True),
}
FIRST_COL_BOLD_PREFIX = ("Zelle", "Speicher")       # Budget-Tabellen 1 und 2
BULLET_COLUMNS = {"Kandidaten"}                      # "A; B" wird zur Aufzählung in der Zelle


# ---------------------------------------------------------------- pandoc-AST -> Text/Runs
def stringify(inlines):
    out = []
    for el in inlines:
        t, c = el["t"], el.get("c")
        if t == "Str":
            out.append(c)
        elif t in ("Space", "SoftBreak", "LineBreak"):
            out.append(" ")
        elif t in ("Strong", "Emph", "Underline", "Strikeout", "SmallCaps", "Superscript", "Subscript"):
            out.append(stringify(c))
        elif t in ("Link", "Image"):
            out.append(stringify(c[1]))
        elif t == "Quoted":
            q = "„“" if c[0]["t"] == "DoubleQuote" else "‚‘"
            out.append(q[0] + stringify(c[1]) + q[1])
        elif t in ("Code", "Math", "RawInline"):
            out.append(c[1])
        elif t == "Span":
            out.append(stringify(c[1]))
    return "".join(out)


def run(text, bold=False, italic=False, sz=None, color=None, mono=False):
    if not text:
        return ""
    rpr = ""
    if mono:
        rpr += '<w:rFonts w:ascii="Menlo" w:hAnsi="Menlo" w:cs="Menlo"/>'
    if bold:
        rpr += "<w:b/><w:bCs/>"
    if italic:
        rpr += "<w:i/><w:iCs/>"
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    if sz:
        rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def runs(inlines, bold=False, italic=False, sz=None, color=None):
    out = []
    for el in inlines:
        t, c = el["t"], el.get("c")
        if t == "Str":
            out.append(run(c, bold, italic, sz, color))
        elif t in ("Space", "SoftBreak"):
            out.append(run(" ", bold, italic, sz, color))
        elif t == "LineBreak":
            out.append("<w:r><w:br/></w:r>")
        elif t == "Strong":
            out.append(runs(c, True, italic, sz, color))
        elif t == "Emph":
            out.append(runs(c, bold, True, sz, color))
        elif t in ("Underline", "Strikeout", "SmallCaps", "Span"):
            out.append(runs(c if t != "Span" else c[1], bold, italic, sz, color))
        elif t == "Superscript":
            out.append(run(stringify(c), bold, italic, sz, color).replace(
                "<w:rPr>", '<w:rPr><w:vertAlign w:val="superscript"/>', 1))
        elif t == "Subscript":
            out.append(run(stringify(c), bold, italic, sz, color).replace(
                "<w:rPr>", '<w:rPr><w:vertAlign w:val="subscript"/>', 1))
        elif t == "Link":            # Links auf Repo-Dateien sind in Word sinnlos: nur Text
            out.append(runs(c[1], bold, italic, sz, color))
        elif t == "Quoted":
            q = "„“" if c[0]["t"] == "DoubleQuote" else "‚‘"
            out.append(run(q[0], bold, italic, sz, color) + runs(c[1], bold, italic, sz, color)
                       + run(q[1], bold, italic, sz, color))
        elif t == "Code":
            out.append(run(c[1], bold, italic, sz, color, mono=True))
        elif t in ("Math", "RawInline"):
            out.append(run(c[1], bold, italic, sz, color))
    return "".join(out)


def para(inner, ppr='<w:spacing w:after="120" w:line="276"/>'):
    return f"<w:p><w:pPr>{ppr}</w:pPr>{inner}</w:p>"


# ---------------------------------------------------------------- Builder
class Builder:
    def __init__(self, workdir):
        self.workdir = workdir
        self.images = []            # (rid, ziel-dateiname, quellpfad)
        self.bookmarks = []         # (level, text, name)
        self.extra_nums = []        # zusätzliche <w:num> für neu startende Nummerierungen
        self.next_num_id = 100
        self.bm_id = 0
        self.img_id = 10

    # ---- Überschriften mit Textmarke für das Inhaltsverzeichnis
    def heading(self, level, inlines):
        text = stringify(inlines)
        self.bm_id += 1
        name = f"_Toc{self.bm_id:06d}"
        self.bookmarks.append((level, text, name))
        style = f"Heading{level}"
        return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
                f'<w:bookmarkStart w:id="{self.bm_id}" w:name="{name}"/>{run(text)}'
                f'<w:bookmarkEnd w:id="{self.bm_id}"/></w:p>')

    # ---- Bilder
    def image(self, src):
        path = os.path.join(HERE, src)
        with open(path, "rb") as f:
            head = f.read(24)
        w, h = struct.unpack(">II", head[16:24])
        fname = os.path.basename(src)
        cx = IMAGE_WIDTH_EMU.get(fname, DEFAULT_IMAGE_WIDTH_EMU)
        cy = int(cx * h / w)
        rid = f"rIdImg{len(self.images) + 1}"
        target = f"img{len(self.images) + 1}_{fname}"
        self.images.append((rid, target, path))
        self.img_id += 1
        n = self.img_id
        return (
            '<w:p><w:pPr><w:keepNext/><w:spacing w:after="60" w:before="120"/><w:jc w:val="center"/></w:pPr>'
            f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:effectExtent t="0" r="0" b="0" l="0"/><wp:docPr id="{n}" name="Bild {n}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{n}" name="{escape(fname)}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

    # ---- Listen
    def lst(self, items, ordered, in_cell=False):
        if ordered:
            num = self.next_num_id
            self.next_num_id += 1
            self.extra_nums.append(
                f'<w:num w:numId="{num}"><w:abstractNumId w:val="{NUM_DECIMAL_ABS}"/>'
                '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>')
        else:
            num = NUM_BULLET
        out = []
        for item in items:
            for blk in item:
                if blk["t"] in ("Plain", "Para"):
                    out.append(para(runs(blk["c"]),
                                    f'<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/>'
                                    f'<w:numId w:val="{num}"/></w:numPr><w:spacing w:after="60" w:line="264"/>'))
                else:
                    out.extend(self.blocks([blk]))
        return out

    # ---- Infokasten (Markdown-Zitat, z. B. "> **Stand:** ...")
    def infobox(self, blocks):
        inner = "".join(
            para(runs(b["c"], sz=CELL_SZ), '<w:spacing w:after="0" w:line="252"/>')
            for b in blocks if b["t"] in ("Para", "Plain"))
        return [
            f'<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="{TEXT_WIDTH}"/></w:tblPr>'
            f'<w:tblGrid><w:gridCol w:w="{TEXT_WIDTH}"/></w:tblGrid><w:tr><w:tc><w:tcPr>'
            f'<w:tcW w:type="dxa" w:w="{TEXT_WIDTH}"/><w:tcBorders>'
            '<w:top w:val="single" w:color="2E6E8E" w:sz="6"/><w:left w:val="single" w:color="2E6E8E" w:sz="24"/>'
            '<w:bottom w:val="single" w:color="2E6E8E" w:sz="6"/><w:right w:val="single" w:color="2E6E8E" w:sz="6"/>'
            '</w:tcBorders><w:shd w:fill="EEF4F8" w:color="auto" w:val="clear"/><w:tcMar>'
            '<w:top w:type="dxa" w:w="80"/><w:left w:type="dxa" w:w="140"/><w:bottom w:type="dxa" w:w="80"/>'
            f'<w:right w:type="dxa" w:w="140"/></w:tcMar></w:tcPr>{inner}</w:tc></w:tr></w:tbl>',
            para("", '<w:spacing w:after="120"/>')]

    # ---- Tabellen
    @staticmethod
    def table_rows(tbl):
        """Liefert (kopfzeile, zeilen) als Listen von Zellen (Liste von Blöcken). pandoc >= 2.10."""
        _attr, _caption, _colspecs, head, bodies, _foot = tbl

        def cells(row):
            return [cell[4] for cell in row[1]]
        head_rows = [cells(r) for r in head[1]]
        body_rows = []
        for body in bodies:
            body_rows += [cells(r) for r in body[2]] + [cells(r) for r in body[3]]
        return (head_rows[0] if head_rows else None), body_rows

    def cell_xml(self, blocks, width, header, bold, fill, bullets):
        tcpr = (f'<w:tcW w:type="dxa" w:w="{width}"/><w:tcBorders>'
                f'<w:top w:val="single" w:color="{BORDER}" w:sz="4"/><w:left w:val="single" w:color="{BORDER}" w:sz="4"/>'
                f'<w:bottom w:val="single" w:color="{BORDER}" w:sz="4"/><w:right w:val="single" w:color="{BORDER}" w:sz="4"/>'
                '</w:tcBorders>')
        if fill:
            tcpr += f'<w:shd w:fill="{fill}" w:color="auto" w:val="clear"/>'
        tcpr += ('<w:tcMar><w:top w:type="dxa" w:w="50"/><w:left w:type="dxa" w:w="90"/>'
                 '<w:bottom w:type="dxa" w:w="50"/><w:right w:type="dxa" w:w="90"/></w:tcMar><w:vAlign w:val="top"/>')
        ppr = '<w:spacing w:after="30" w:before="30" w:line="252"/>'
        paras = []
        for b in blocks:
            if b["t"] in ("Plain", "Para"):
                text = stringify(b["c"])
                if bullets and "; " in text:
                    for part in text.split("; "):
                        paras.append(para(run(part, sz=CELL_SZ),
                                          f'<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/>'
                                          f'<w:numId w:val="{NUM_CELL_BULLET}"/></w:numPr>{ppr}'))
                else:
                    paras.append(para(runs(b["c"], bold=bold or header, sz=CELL_SZ), ppr))
        if not paras:
            paras.append(para("", ppr))
        return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{''.join(paras)}</w:tc>"

    def table(self, tbl):
        head, rows = self.table_rows(tbl)
        ncol = len(head if head else rows[0])
        head_txt = tuple(stringify_blocks(c) for c in head) if head else ()
        widths, first_bold = TABLE_LAYOUT.get(head_txt, (None, None))
        gantt = len(head_txt) > 2 and head_txt[1] == "W1"
        if widths is None:
            if gantt:
                first = 2206
                widths = [first] + [(TEXT_WIDTH - first) // (ncol - 1)] * (ncol - 1)
                first_bold = True
            else:
                widths = proportional_widths([head] + rows, ncol)
                first_bold = head_txt[0].startswith(FIRST_COL_BOLD_PREFIX) if head_txt else False
        bullet_cols = {i for i, h in enumerate(head_txt) if h in BULLET_COLUMNS}

        xml = [f'<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="{sum(widths)}"/><w:tblLayout w:type="fixed"/></w:tblPr>'
               "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"]
        if head:
            xml.append("<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>" + "".join(
                self.cell_xml(c, widths[i], True, True, HEAD_FILL, False) for i, c in enumerate(head)) + "</w:tr>")
        for r_i, row in enumerate(rows):
            cells = []
            for i, c in enumerate(row):
                fill, blocks = None, c
                if gantt and i > 0 and stringify_blocks(c).strip() == "■":
                    fill, blocks = GANTT_COLORS[r_i % len(GANTT_COLORS)], []
                cells.append(self.cell_xml(blocks, widths[i], False, first_bold and i == 0, fill,
                                           i in bullet_cols))
            xml.append("<w:tr><w:trPr><w:cantSplit/></w:trPr>" + "".join(cells) + "</w:tr>")
        xml.append("</w:tbl>")
        return ["".join(xml), para("", '<w:spacing w:after="120"/>')]

    # ---- Blöcke
    def blocks(self, blocks):
        out = []
        for blk in blocks:
            t, c = blk["t"], blk.get("c")
            if t == "Header":
                level = c[0] - 1                 # "## A …" -> Überschrift 1
                if level >= 1:
                    out.append(self.heading(min(level, 3), c[2]))
            elif t in ("Para", "Plain"):
                if len(c) == 1 and c[0]["t"] == "Image":
                    out.append(self.image(c[0]["c"][2][0]))
                elif all(el["t"] in ("Emph", "Space", "SoftBreak") for el in c) and c:
                    text = stringify(c)
                    if text.startswith("Abbildung"):
                        out.append(para(run(text, italic=True, sz=18, color="595959"),
                                        '<w:spacing w:after="200"/><w:jc w:val="center"/>'))
                    else:                        # Tabellenüberschrift
                        out.append(para(run(text, italic=True, sz=18, color="595959"),
                                        '<w:keepNext/><w:spacing w:after="120" w:line="276"/>'))
                else:
                    out.append(para(runs(c)))
            elif t == "Figure":                  # pandoc 3: Bild mit Alt-Text
                for b in c[2]:
                    for el in (b["c"] if b["t"] in ("Plain", "Para") else []):
                        if el["t"] == "Image":
                            out.append(self.image(el["c"][2][0]))
            elif t == "BulletList":
                out += self.lst(c, ordered=False)
            elif t == "OrderedList":
                out += self.lst(c[1], ordered=True)
            elif t == "BlockQuote":
                out += self.infobox(c)
            elif t == "Table":
                out += self.table(c)
            elif t == "HorizontalRule":
                out.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        return out


def stringify_blocks(blocks):
    return " ".join(stringify(b["c"]) for b in blocks if b["t"] in ("Plain", "Para")).strip()


def proportional_widths(rows, ncol):
    score = [4] * ncol
    for row in rows:
        if not row:
            continue
        for i, cell in enumerate(row[:ncol]):
            text = stringify_blocks(cell)
            longest = max((len(w) for w in text.split()), default=0)
            score[i] = max(score[i], min(max(len(text), longest * 1.6), 60))
    total = sum(score)
    widths = [max(int(TEXT_WIDTH * s / total), 650) for s in score]
    widths[-1] += TEXT_WIDTH - sum(widths)
    return widths


# ---------------------------------------------------------------- Inhaltsverzeichnis
def toc_block(bookmarks, pages):
    out = ['<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/><w:docPartUnique/>'
           '</w:docPartObj></w:sdtPr><w:sdtContent>']
    first = True
    for level, text, name in bookmarks:
        pg = str(pages.get(name, "")) if pages else ""
        begin = ('<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
                 '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
                 '<w:r><w:fldChar w:fldCharType="separate"/></w:r>') if first else ""
        first = False
        out.append(
            f'<w:p><w:pPr><w:pStyle w:val="TOC{level}"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_WIDTH}"/></w:tabs></w:pPr>'
            f'{begin}<w:hyperlink w:anchor="{name}" w:history="1">{run(text)}<w:r><w:tab/></w:r>'
            f'<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGEREF {name} \\h </w:instrText></w:r>'
            f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>{run(pg)}<w:r><w:fldChar w:fldCharType="end"/></w:r>'
            '</w:hyperlink></w:p>')
    out.append('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:sdtContent></w:sdt>')
    return "".join(out)


TOC_STYLES = "".join(
    f'<w:style w:type="paragraph" w:styleId="TOC{i}"><w:name w:val="toc {i}"/><w:basedOn w:val="Normal"/>'
    f'<w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr>'
    f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_WIDTH}"/></w:tabs>'
    f'<w:spacing w:before="{80 if i == 1 else 0}" w:after="40"/><w:ind w:left="{(i - 1) * 240}"/></w:pPr>'
    f'{"<w:rPr><w:b/><w:bCs/></w:rPr>" if i == 1 else ""}</w:style>'
    for i in (1, 2, 3))


# ---------------------------------------------------------------- Dokument zusammensetzen
def meta_str(meta, key):
    v = meta.get(key)
    if not v:
        return ""
    if v["t"] == "MetaInlines":
        return stringify(v["c"])
    if v["t"] == "MetaString":
        return v["c"]
    return ""


def build(doc, pages=None):
    src = os.path.join(HERE, f"{doc}.md")
    tpl = os.path.join(HERE, "vorlage", f"{doc}-vorlage.docx")
    ast = json.loads(subprocess.check_output(["pandoc", src, "-f", "markdown", "-t", "json"]))
    meta, blocks = ast["meta"], ast["blocks"]

    # Kopfbereich der .md (H1 + Zeilen bis zur ersten "##"-Überschrift) gehört aufs Deckblatt
    start = next(i for i, b in enumerate(blocks) if b["t"] == "Header" and b["c"][0] == 2)
    body_blocks = blocks[start:]

    zin = zipfile.ZipFile(tpl)
    files = {n: zin.read(n) for n in zin.namelist()}
    docxml = files["word/document.xml"].decode("utf-8")

    b = Builder(tempfile.mkdtemp())
    # Teil A (bis zur zweiten Hauptüberschrift), dann "B Inhalt" mit Verzeichnis, dann der Rest
    h2 = [i for i, blk in enumerate(body_blocks) if blk["t"] == "Header" and blk["c"][0] == 2]
    split = h2[1] if len(h2) > 1 else len(body_blocks)
    part_a = b.blocks(body_blocks[:split])
    toc_heading_idx = len(b.bookmarks)
    b_heading = b.heading(1, [{"t": "Str", "c": "B"}, {"t": "Space"}, {"t": "Str", "c": "Inhalt"}])
    part_c = b.blocks(body_blocks[split:])
    toc_marks = list(b.bookmarks)

    toc = ('<w:p><w:pPr><w:spacing w:after="120" w:before="200"/></w:pPr>'
           + run("Inhaltsverzeichnis", bold=True, sz=26, color="1F4E6B") + "</w:p>"
           + toc_block(toc_marks, pages) + '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # Deckblatt aus der Vorlage übernehmen (alles bis einschließlich des ersten Seitenumbruchs)
    body_start = docxml.index("<w:body>") + len("<w:body>")
    sect = docxml.rindex("<w:sectPr")
    old_body = docxml[body_start:sect]
    pb = old_body.index('<w:br w:type="page"/>')
    cover = old_body[:old_body.index("</w:p>", pb) + len("</w:p>")]

    subtitle = meta_str(meta, "subtitle")
    version = meta_str(meta, "version")
    date = meta_str(meta, "date")
    author = meta_str(meta, "author")
    cover = re.sub(r">\[Miniaturisierter[^<]*\]<", f">{escape(subtitle)}<", cover)
    cover = re.sub(r">Version [^<]*<", f">Version {escape(version)}<", cover)
    cover = re.sub(r">\[\d{2}\.\d{2}\.\d{4}\]<", f">{escape(date)}<", cover)
    cover = re.sub(r">\[Laurenz Untiedt[^<]*\]<", f">{escape(author)}<", cover)

    new_body = cover + "".join(part_a) + b_heading + toc + "".join(part_c)
    docxml = docxml[:body_start] + new_body + docxml[sect:]
    files["word/document.xml"] = docxml.encode("utf-8")

    # Kopfzeile: Team-Platzhalter durch Nachnamen ersetzen
    lastnames = ", ".join(n.strip().split()[-1] for n in author.split(","))
    for name in [n for n in files if re.match(r"word/header\d+\.xml", n)]:
        files[name] = files[name].decode("utf-8").replace(
            "Team: [Gruppenname]", f"Team: {escape(lastnames)}").encode("utf-8")

    # Formatvorlagen: doppelte Überschriften-Definitionen entfernen (Ursache des kaputten
    # Inhaltsverzeichnisses), Verzeichnis-Formatvorlagen ergänzen
    styles = files["word/styles.xml"].decode("utf-8")
    for lvl in (1, 2, 3):
        defs = list(re.finditer(rf'<w:style [^>]*w:styleId="Heading{lvl}">.*?</w:style>', styles, re.S))
        for d in defs[:-1]:
            styles = styles.replace(d.group(0), "", 1)
    styles = re.sub(r'<w:style [^>]*w:styleId="TOC\d">.*?</w:style>', "", styles, flags=re.S)
    styles = styles.replace("</w:styles>", TOC_STYLES + "</w:styles>")
    files["word/styles.xml"] = styles.encode("utf-8")

    # Nummerierungen für neu startende Aufzählungen
    numbering = files["word/numbering.xml"].decode("utf-8")
    files["word/numbering.xml"] = numbering.replace(
        "</w:numbering>", "".join(b.extra_nums) + "</w:numbering>").encode("utf-8")

    # Bilder: alte Bilder der Vorlage raus, neue rein
    rels = files["word/_rels/document.xml.rels"].decode("utf-8")
    rels = re.sub(r'<Relationship [^>]*Target="media/[^"]*"/>', "", rels)
    for n in [n for n in files if n.startswith("word/media/")]:
        del files[n]
    for rid, target, path in b.images:
        with open(path, "rb") as f:
            files[f"word/media/{target}"] = f.read()
        rels = rels.replace("</Relationships>",
                            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{target}"/></Relationships>')
    files["word/_rels/document.xml.rels"] = rels.encode("utf-8")

    # Word soll Felder (Verzeichnis, Seitenzahlen) beim Öffnen aktualisieren
    settings = files["word/settings.xml"].decode("utf-8")
    if "<w:updateFields" not in settings:
        settings = re.sub(r"(<w:settings[^>]*>)", r'\1<w:updateFields w:val="true"/>', settings, 1)
    files["word/settings.xml"] = settings.encode("utf-8")

    os.makedirs(os.path.join(HERE, "export"), exist_ok=True)
    out = os.path.join(HERE, "export", f"{doc}.docx")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        if "[Content_Types].xml" in files:
            z.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
        for name, data in files.items():
            z.writestr(name, data)
    return out, toc_marks


def page_numbers(docx, marks):
    """Optional: Seitenzahlen über LibreOffice + pdftotext ermitteln, damit das Verzeichnis
    auch in Programmen ohne Feldaktualisierung vollständig aussieht. Word aktualisiert sie
    beim Öffnen ohnehin."""
    soffice = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if not (os.path.exists(soffice) and shutil.which("pdftotext")):
        return None
    tmp = tempfile.mkdtemp()
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, docx],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(docx))[0] + ".pdf")
    if not os.path.exists(pdf):
        return None
    text = subprocess.check_output(["pdftotext", "-layout", pdf, "-"]).decode("utf-8")
    pages = text.split("\f")
    result, start = {}, 1                       # Deckblatt überspringen
    for level, heading, name in marks:
        for p in range(start, len(pages)):
            lines = [ln.strip() for ln in pages[p].splitlines()]
            if heading in lines:
                result[name] = p + 1
                start = p
                break
    return result


if __name__ == "__main__":
    docs = sys.argv[1:] or ["lastenheft", "pflichtenheft"]
    for d in docs:
        path, marks = build(d)
        pages = page_numbers(path, marks)
        if pages:
            build(d, pages)
        print(f"export/{d}.docx erstellt" + ("" if pages else " (Seitenzahlen im Verzeichnis aktualisiert Word beim Öffnen)"))
