"""Diagramas UML con la estética de los documentos de la cátedra (SVG).

Paleta: elementos con degradé rosado y borde #7a5f6a, texto #222, notas y marcos grises,
callouts numerados en azul #1f4e79. El texto lleva halo blanco hecho con dos elementos text.
"""
from xml.sax.saxutils import escape

FONT = "Liberation Sans, Helvetica, Arial, sans-serif"
BORDE = "#7a5f6a"
TEXTO = "#222"
LINEA = "#222"
GRIS = "#6f6f6f"


class Svg:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []
        self.boxes = {}

    # ---------- primitivas ----------
    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=15, bold=False, italic=False, anchor="start", underline=False, color=TEXTO, halo=True):
        attrs = (
            f'x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{"700" if bold else "400"}" font-style="{"italic" if italic else "normal"}"'
            + (' text-decoration="underline"' if underline else "")
        )
        s = escape(s)
        if halo:
            self.add(f'<text {attrs} fill="#fff" stroke="#fff" stroke-width="5" stroke-linejoin="round">{s}</text>')
        self.add(f'<text {attrs} fill="{color}">{s}</text>')

    def line(self, pts, dashed=False, color=LINEA, width=1.6, start=None, end=None):
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        extra = ' stroke-dasharray="8 6"' if dashed else ""
        ms = f' marker-start="url(#{start})"' if start else ""
        me = f' marker-end="url(#{end})"' if end else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{extra}{ms}{me}/>')

    # ---------- clases y objetos ----------
    def class_box(self, key, x, y, w, name, attrs=(), methods=(), stereotype=None, abstract=False, obj=False):
        head = 34 + (14 if stereotype else 0)
        line_h = 20

        def comp(n):
            return 14 if n == 0 else 12 + n * line_h

        ha, hm = comp(len(attrs)), comp(len(methods))
        if obj:
            hm = 0
        h = head + ha + hm
        self.boxes[key] = (x, y, w, h)
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#rosa)" stroke="{BORDE}" stroke-width="2"/>')
        self.add(f'<line x1="{x}" y1="{y + head}" x2="{x + w}" y2="{y + head}" stroke="{BORDE}" stroke-width="2"/>')
        if not obj:
            self.add(f'<line x1="{x}" y1="{y + head + ha}" x2="{x + w}" y2="{y + head + ha}" stroke="{BORDE}" stroke-width="2"/>')
        cy = y + 22
        if stereotype:
            self.text(x + w / 2, y + 17, f"«{stereotype}»", size=13, italic=True, anchor="middle")
            cy = y + 36
        self.text(x + w / 2, cy, name, bold=True, anchor="middle", underline=obj, italic=abstract)
        for i, a in enumerate(attrs):
            self.text(x + 8, y + head + 22 + i * line_h - 2, a, size=14)
        for i, m in enumerate(methods):
            self.text(x + 8, y + head + ha + 22 + i * line_h - 2, m, size=14)
        return self.boxes[key]

    # ---------- dibujo final ----------
    def defs(self):
        return f"""<defs>
<linearGradient id="rosa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3f3"/><stop offset="1" stop-color="#f1d0d3"/></linearGradient>
<linearGradient id="rosaClaro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3f3"/><stop offset="1" stop-color="#f7e6e7"/></linearGradient>
<marker id="tri" viewBox="0 0 20 20" refX="19" refY="10" markerWidth="20" markerHeight="20" orient="auto" markerUnits="userSpaceOnUse"><path d="M2 2 L19 10 L2 18 Z" fill="#fff" stroke="{BORDE}" stroke-width="1.8"/></marker>
<marker id="rombo" viewBox="0 0 24 16" refX="1" refY="8" markerWidth="24" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse"><path d="M1 8 L12 1.5 L23 8 L12 14.5 Z" fill="{BORDE}" stroke="{BORDE}" stroke-width="1.5"/></marker>
<marker id="romboVacio" viewBox="0 0 24 16" refX="1" refY="8" markerWidth="24" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse"><path d="M1 8 L12 1.5 L23 8 L12 14.5 Z" fill="#fff" stroke="{BORDE}" stroke-width="1.8"/></marker>
<marker id="abierta" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse"><path d="M1 1.5 L15 8 L1 14.5" fill="none" stroke="{BORDE}" stroke-width="1.8"/></marker>
<marker id="sync" viewBox="0 0 16 14" refX="15" refY="7" markerWidth="16" markerHeight="14" orient="auto" markerUnits="userSpaceOnUse"><path d="M1 1 L15 7 L1 13 Z" fill="{LINEA}"/></marker>
<marker id="abiertaN" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" orient="auto" markerUnits="userSpaceOnUse"><path d="M1 1.5 L15 8 L1 14.5" fill="none" stroke="{LINEA}" stroke-width="1.8"/></marker>
</defs>"""

    def render(self):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="{FONT}">'
            f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>{self.defs()}' + "".join(self.parts) + "</svg>"
        )

    def save(self, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(self.render())


# ---------- diagramas de secuencia ----------
def actor(svg, x, y, nombre):
    """Figura de palo con la cabeza en y; el nombre va debajo."""
    c = BORDE
    svg.add(f'<circle cx="{x}" cy="{y + 9}" r="9" fill="url(#rosa)" stroke="{c}" stroke-width="2"/>')
    svg.add(f'<path d="M{x} {y + 18} L{x} {y + 42} M{x - 15} {y + 27} L{x + 15} {y + 27} M{x} {y + 42} L{x - 13} {y + 60} M{x} {y + 42} L{x + 13} {y + 60}" stroke="{c}" stroke-width="2" fill="none"/>')
    svg.text(x, y + 78, nombre, bold=True, anchor="middle")


def cabecera(svg, x, y, texto, w=None):
    w = w or (len(texto) * 8.6 + 28)
    svg.add(f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="32" fill="url(#rosa)" stroke="{BORDE}" stroke-width="2"/>')
    svg.text(x, y + 21, texto, bold=True, anchor="middle", halo=False)


def marco_sd(svg, nombre, x=8, y=8, w=None, h=None):
    w = w or svg.w - 16
    h = h or svg.h - 16
    svg.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#555" stroke-width="2"/>')
    pw = len(nombre) * 8.4 + 44
    svg.add(f'<path d="M{x} {y} L{x + pw} {y} L{x + pw} {y + 16} L{x + pw - 14} {y + 30} L{x} {y + 30} Z" fill="#f3e4e6" stroke="#555" stroke-width="2"/>')
    svg.text(x + 12, y + 21, f"sd {nombre}", bold=True, halo=False)


def linea_vida(svg, x, y0, y1):
    svg.add(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{GRIS}" stroke-width="1.6" stroke-dasharray="8 6"/>')


def activacion(svg, x, y0, y1):
    svg.add(f'<rect x="{x - 6}" y="{y0}" width="12" height="{y1 - y0}" fill="#f7e6e7" stroke="{BORDE}" stroke-width="1.6"/>')


def mensaje(svg, x0, x1, y, texto, tipo="sync"):
    """x0 y x1 ya están desplazados al borde de la activación."""
    if tipo == "sync":
        svg.line([(x0, y), (x1, y)], end="sync")
    elif tipo == "return":
        svg.line([(x0, y), (x1, y)], dashed=True, end="abiertaN")
    else:
        svg.line([(x0, y), (x1, y)], end="abiertaN")
    svg.text((x0 + x1) / 2, y - 8, texto, anchor="middle")


def fragmento(svg, x, y, w, h, op, guarda):
    svg.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#555" stroke-width="1.8"/>')
    ow = len(op) * 9 + 26
    svg.add(f'<path d="M{x} {y} L{x + ow} {y} L{x + ow} {y + 12} L{x + ow - 11} {y + 24} L{x} {y + 24} Z" fill="#f3e4e6" stroke="#555" stroke-width="1.8"/>')
    svg.text(x + 9, y + 17, op, bold=True, halo=False)
    svg.text(x + ow + 8, y + 17, guarda)


def callout(svg, x, y, n):
    svg.add(f'<circle cx="{x}" cy="{y}" r="11" fill="#1f4e79"/>')
    svg.add(f'<text x="{x}" y="{y + 5}" font-size="14" font-weight="700" text-anchor="middle" fill="#fff">{n}</text>')
