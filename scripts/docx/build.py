#!/usr/bin/env python3
"""Genera apunte.docx y apunte.pdf de una clase a partir de apunte.md.

Usa como plantilla un documento final de la cátedra (shared/plantillas/catedra.docx):
conserva portada, encabezado, pie "N de M", estilos y numeración, y reemplaza el cuerpo.

Uso: python3 scripts/docx/build.py C01 [--revisor "Nombre"] [--fecha "Octubre 2026"]
Requiere: python-docx, LibreOffice (soffice), pdftotext, Node con playwright-chromium (figuras).
"""
import argparse
import copy
import glob
import os
import re
import subprocess
import sys
import tempfile

from docx import Document
from docx.oxml.ns import qn
from lxml import etree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PLANTILLA = os.path.join(ROOT, "shared", "plantillas", "catedra.docx")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def w(tag):
    return "{%s}%s" % (W, tag)


def parse(xml):
    return etree.fromstring(
        '<root xmlns:w="%s" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">%s</root>' % (W, xml)
    )[0]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- runs
def runs(texto, base=""):
    """Convierte **negrita**, *cursiva* y `código` en runs. base: propiedades extra (por ejemplo tamaño)."""
    out = []
    for tok in re.split(r"(\*\*.+?\*\*|`.+?`|\*[^*\s][^*]*?\*)", texto):
        if not tok:
            continue
        props = base
        if tok.startswith("**"):
            props += '<w:b w:val="1"/><w:bCs w:val="1"/>'
            tok = tok[2:-2]
        elif tok.startswith("`"):
            props = '<w:rFonts w:ascii="Courier New" w:cs="Courier New" w:eastAsia="Courier New" w:hAnsi="Courier New"/>' + (
                base if base else '<w:sz w:val="20"/><w:szCs w:val="20"/>'
            )
            tok = tok[1:-1]
        elif tok.startswith("*"):
            props += '<w:i w:val="1"/><w:iCs w:val="1"/>'
            tok = tok[1:-1]
        out.append('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (props, esc(tok)))
    return "".join(out)


# ---------------------------------------------------------------- bloques (copiados de la plantilla)
class Cuerpo:
    def __init__(self, doc):
        self.doc = doc
        self.items = []
        self.bm = 100
        self.headings = []  # (nivel, texto, bookmark)
        self.fig = 0
        self.next_num = 50

    def add(self, xml):
        self.items.append(parse(xml))

    def h(self, nivel, texto):
        self.bm += 1
        name = "_h%d" % self.bm
        self.headings.append((nivel, texto, name))
        if nivel == 1:
            ppr = ('<w:pStyle w:val="Heading1"/><w:widowControl w:val="1"/><w:keepNext w:val="1"/>'
                   '<w:spacing w:after="200" w:before="280" w:lineRule="auto"/>'
                   '<w:ind w:left="-283.46456692913375" w:right="-182.5984251968498" w:firstLine="0"/>'
                   '<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>')
            rpr = '<w:sz w:val="24"/><w:szCs w:val="24"/>'
        else:
            ppr = ('<w:pStyle w:val="Heading2"/><w:widowControl w:val="1"/><w:keepNext w:val="1"/>'
                   '<w:spacing w:after="0" w:lineRule="auto"/>'
                   '<w:ind w:left="0" w:right="0" w:firstLine="0"/><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>')
            rpr = '<w:sz w:val="22"/><w:szCs w:val="22"/>'
        self.add('<w:p><w:pPr>%s</w:pPr><w:bookmarkStart w:id="%d" w:name="%s"/><w:bookmarkEnd w:id="%d"/>'
                 '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (ppr, self.bm, name, self.bm, rpr, esc(texto)))

    def p(self, texto):
        self.add('<w:p><w:pPr><w:widowControl w:val="1"/><w:spacing w:after="200" w:before="0" w:lineRule="auto"/>'
                 '<w:ind w:left="-283.46456692913375" w:right="-182.5984251968498" w:firstLine="0"/><w:jc w:val="both"/></w:pPr>%s</w:p>' % runs(texto))

    def lista(self, items, numerada=False):
        num = 3
        if numerada:
            self.next_num += 1
            num = self.next_num
            self.doc.part.numbering_part.element.append(parse(
                '<w:num w:numId="%d"><w:abstractNumId w:val="2"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>' % num))
        for i, it in enumerate(items):
            after = 200 if i == len(items) - 1 else 120
            self.add('<w:p><w:pPr><w:widowControl w:val="1"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="%d"/></w:numPr>'
                     '<w:spacing w:after="%d" w:before="0" w:lineRule="auto"/><w:ind w:left="720" w:right="0" w:hanging="360"/><w:jc w:val="both"/></w:pPr>%s</w:p>'
                     % (num, after, runs(it)))

    def figura(self, caption, path):
        from PIL import Image

        im = Image.open(path)
        wpx, hpx = im.size
        # El ancho en el documento sigue el tamaño natural del diagrama (se dibujan a ~760 px de ancho máximo).
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(path.replace(".png", ".svg"), encoding="utf8").read()) if os.path.exists(path.replace(".png", ".svg")) else None
        ancho_in = min(5.6, (int(vb.group(1)) / 760.0) * 5.6) if vb else 5.0
        cx = int(ancho_in * 914400)
        cy = int(cx * hpx / wpx)
        rid, _ = self.doc.part.get_or_add_image(path)
        self.bm += 1
        self.add(
            '<w:p><w:pPr><w:keepNext w:val="1"/><w:widowControl w:val="1"/><w:spacing w:after="60" w:before="120" w:lineRule="auto"/>'
            '<w:ind w:left="0" w:right="0" w:firstLine="0"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            '<wp:inline distB="0" distT="0" distL="114300" distR="114300"><wp:extent cx="%d" cy="%d"/><wp:effectExtent b="0" l="0" r="0" t="0"/>'
            '<wp:docPr id="%d" name="%s"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
            '<pic:nvPicPr><pic:cNvPr id="0" name="%s"/><pic:cNvPicPr preferRelativeResize="0"/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:srcRect b="0" l="0" r="0" t="0"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"/><a:ln/></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
            % (cx, cy, self.bm, os.path.basename(path), os.path.basename(path), rid, cx, cy)
        )
        self.epigrafe(caption)

    def epigrafe(self, caption):
        self.add('<w:p><w:pPr><w:widowControl w:val="1"/><w:spacing w:after="240" w:before="0" w:lineRule="auto"/>'
                 '<w:ind w:left="0" w:right="0" w:firstLine="0"/><w:jc w:val="center"/></w:pPr>'
                 '<w:r><w:rPr><w:i w:val="1"/><w:iCs w:val="1"/><w:color w:val="595959"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
                 '<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % esc(caption))

    def tabla(self, filas):
        n = len(filas[0])
        total = 9335
        anchos = {2: [3000, 6335], 3: [2100, 3000, 4235]}.get(n, [total // n] * n)
        grid = "".join('<w:gridCol w:w="%d"/>' % a for a in anchos)
        mar = '<w:tcMar><w:top w:w="80.0" w:type="dxa"/><w:left w:w="110.0" w:type="dxa"/><w:bottom w:w="80.0" w:type="dxa"/><w:right w:w="110.0" w:type="dxa"/></w:tcMar>'
        rows = []
        for ri, fila in enumerate(filas):
            cells = []
            for ci, celda in enumerate(fila):
                shd = '<w:shd w:fill="f3e4e6" w:val="clear"/>' if ri == 0 else ""
                base = '<w:sz w:val="20"/><w:szCs w:val="20"/>'
                if ri == 0 or ci == 0:
                    base = '<w:b w:val="1"/><w:bCs w:val="1"/>' + base
                cells.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s%s</w:tcPr><w:p><w:pPr><w:widowControl w:val="1"/>'
                             '<w:spacing w:after="0" w:before="0" w:line="252" w:lineRule="auto"/><w:ind w:left="0" w:right="0" w:firstLine="0"/><w:jc w:val="left"/></w:pPr>%s</w:p></w:tc>'
                             % (anchos[ci], shd, mar, runs(celda, base)))
            rows.append('<w:tr><w:trPr><w:cantSplit w:val="1"/><w:tblHeader w:val="%d"/></w:trPr>%s</w:tr>' % (1 if ri == 0 else 0, "".join(cells)))
        b = lambda s: '<w:%s w:color="b7b7b7" w:space="0" w:sz="4" w:val="single"/>' % s
        self.add('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="left"/><w:tblBorders>%s</w:tblBorders><w:tblLayout w:type="fixed"/>'
                 '<w:tblLook w:val="0400"/></w:tblPr><w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
                 % (total, "".join(b(x) for x in ("top", "left", "bottom", "right", "insideH", "insideV")), grid, "".join(rows)))
        self.add('<w:p><w:pPr><w:spacing w:after="0" w:before="0"/></w:pPr></w:p>')


# ---------------------------------------------------------------- markdown
def leer_md(cuerpo, md, base):
    lines = md.split("\n")
    i = 0
    titulo = None
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("# "):
            titulo = ln[2:].strip()
            i += 1
        elif ln.startswith("## "):
            cuerpo.h(1, ln[3:].strip()); i += 1
        elif ln.startswith("### "):
            cuerpo.h(2, ln[4:].strip()); i += 1
        elif ln.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", ln)
            cuerpo.figura(m.group(1), os.path.join(base, m.group(2))); i += 1
        elif ln.startswith("|"):
            filas = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s\-|]+\|$", lines[i]):
                    filas.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            cuerpo.tabla(filas)
        elif re.match(r"^\*[^*].*\*$", ln.strip()) and re.match(r"^\*(Tabla|Figura)", ln.strip()):
            cuerpo.epigrafe(ln.strip()[1:-1]); i += 1
        elif ln.startswith("- "):
            it = []
            while i < len(lines) and lines[i].startswith("- "):
                it.append(lines[i][2:].strip()); i += 1
            cuerpo.lista(it)
        elif re.match(r"^\d+\. ", ln):
            it = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                it.append(re.sub(r"^\d+\. ", "", lines[i]).strip()); i += 1
            cuerpo.lista(it, numerada=True)
        else:
            par = [ln.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|!\[|\||- |\d+\. |\*(Tabla|Figura))", lines[i]):
                par.append(lines[i].strip()); i += 1
            cuerpo.p(" ".join(par))
    return titulo


# ---------------------------------------------------------------- documento
def set_text(el, nuevo):
    """Reemplaza el texto de un párrafo conservando el formato del primer run con texto."""
    ts = el.findall(".//w:t", NS)
    ts[0].text = nuevo
    for t in ts[1:]:
        t.text = ""


def indice(doc, headings, paginas):
    """Entradas del TOC con páginas en caché (campo real, se actualiza en Word)."""
    paras = []
    for k, (nivel, texto, name) in enumerate(headings):
        bold = "1" if nivel == 1 else "0"
        ind = 0 if nivel == 1 else 360
        rpr = ('<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/><w:b w:val="%s"/><w:bCs w:val="%s"/>'
               '<w:color w:val="000000"/><w:sz w:val="22"/><w:szCs w:val="22"/>' % (bold, bold))
        ini = ('<w:r><w:fldChar w:fldCharType="begin"/><w:instrText xml:space="preserve"> TOC \\h \\u \\z \\t "Heading 1,1,Heading 2,2,"</w:instrText>'
               '<w:fldChar w:fldCharType="separate"/></w:r>') if k == 0 else ""
        fin = '<w:r><w:fldChar w:fldCharType="end"/></w:r>' if k == len(headings) - 1 else ""
        paras.append(
            '<w:p><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9000"/></w:tabs><w:spacing w:after="0" w:before="60" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="%d" w:right="0" w:firstLine="0"/><w:jc w:val="left"/></w:pPr>%s<w:hyperlink w:anchor="%s"><w:r><w:rPr>%s</w:rPr>'
            '<w:t xml:space="preserve">%s</w:t><w:tab/><w:t xml:space="preserve">%s</w:t></w:r></w:hyperlink>%s</w:p>'
            % (ind, ini, name, rpr, esc(texto), paginas.get(name, ""), fin)
        )
    return paras


def construir(clase_dir, salida, titulo_md, args, paginas):
    doc = Document(PLANTILLA)
    body = doc.element.body
    els = list(body.iterchildren())
    sect = els[-1]
    titulo = None

    # portada: título, autor, revisor, fecha
    if len(args.titulo or titulo_md) > 24:  # un título largo ocupa dos líneas: se quita un espaciador
        body.remove(els[4])
    set_text(els[2], args.titulo or titulo_md)
    set_text(els[12], args.autor)
    set_text(els[14], args.revisor)
    set_text(els[16], args.fecha)
    set_text(els[15], "Versión 1.0")

    # encabezado
    for part in doc.part.package.iter_parts():
        if part.partname.endswith(("header1.xml", "header2.xml")):
            for t in part._element.iter(qn("w:t")):
                if t.text and "Secuencia" in t.text:
                    t.text = (args.titulo or titulo_md)
                elif t.text and t.text.strip() in ("Diagramas", "de"):
                    t.text = ""

    # cuerpo nuevo
    cuerpo = Cuerpo(doc)
    leer_md(cuerpo, open(os.path.join(clase_dir, "apunte.md"), encoding="utf8").read(), clase_dir)

    sdt = els[18]
    for el in els[21:-1]:
        body.remove(el)
    # índice
    contenido = sdt.find(qn("w:sdtContent"))
    for p in list(contenido):
        contenido.remove(p)
    for p in indice(doc, cuerpo.headings, paginas):
        contenido.append(parse(p))
    for it in cuerpo.items:
        sect.addprevious(it)
    doc.save(salida)
    return cuerpo.headings


def paginas_de(pdf, headings):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    textos = []
    for pg in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(pg), "-l", str(pg), "-layout", pdf, "-"], capture_output=True, text=True).stdout
        textos.append(t)
    res = {}
    pg_act, ln_act = 3, -1  # portada e índice no cuentan; los títulos aparecen en orden
    for nivel, texto, name in headings:
        hallado = False
        for pg in range(pg_act, n + 1):
            lineas = [l.strip() for l in textos[pg - 1].split("\n")]
            desde = ln_act + 1 if pg == pg_act else 0
            for k in range(desde, len(lineas)):
                if lineas[k] == texto:
                    res[name] = str(pg)
                    pg_act, ln_act = pg, k
                    hallado = True
                    break
            if hallado:
                break
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clase")
    ap.add_argument("--autor", default="Santino Lautaro Carrizo")
    ap.add_argument("--revisor", default="A definir")
    ap.add_argument("--fecha", default="Octubre 2026")
    ap.add_argument("--titulo", default=None)
    args = ap.parse_args()

    dirs = glob.glob(os.path.join(ROOT, "clases", args.clase + "*"))
    if not dirs:
        sys.exit("No existe la clase " + args.clase)
    d = dirs[0]
    chromium = os.environ.get("CHROMIUM_PATH")
    fig = os.path.join(d, "figuras.py")
    if os.path.exists(fig):
        subprocess.run([sys.executable, fig], check=True)
        subprocess.run(["node", os.path.join(ROOT, "scripts", "svg2png.mjs"), os.path.join(d, "figuras")], check=True, cwd=ROOT)
    md = open(os.path.join(d, "apunte.md"), encoding="utf8").read()
    titulo_md = re.match(r"# (.+)", md).group(1).strip()
    out = os.path.join(d, "apunte.docx")
    paginas = {}
    for _ in range(3):  # a lo sumo tres pasadas: la numeración converge enseguida
        headings = construir(d, out, titulo_md, args, paginas)
        tmp = tempfile.mkdtemp()
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, out], check=True, capture_output=True)
        pdf = os.path.join(tmp, "apunte.pdf")
        nuevas = paginas_de(pdf, headings)
        if nuevas == paginas:
            break
        paginas = nuevas
    os.replace(pdf, os.path.join(d, "apunte.pdf"))
    print("Listo:", out)


if __name__ == "__main__":
    main()
