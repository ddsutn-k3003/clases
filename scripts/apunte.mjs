// Convierte apunte.md en una página HTML autocontenida (con figuras SVG en línea).
import { readFileSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import MarkdownIt from 'markdown-it'
import { fontFaces, TOKENS, escapeHtml } from './site.mjs'

const slug = (s) =>
  s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')

const CSS = `
.top{position:sticky;top:0;z-index:5;background:#fff;border-bottom:4px solid var(--rojo);display:flex;justify-content:space-between;align-items:center;padding:12px 28px;font-size:15px;color:var(--muted)}
.top a{font-weight:700;text-decoration:none}
.wrap{display:grid;grid-template-columns:280px minmax(0,1fr);gap:56px;max-width:1180px;margin:0 auto;padding:36px 28px 80px}
nav.indice{position:sticky;top:84px;align-self:start;max-height:calc(100vh - 110px);overflow:auto;font-size:15.5px}
nav.indice h2{font-family:var(--font-display);font-size:20px;color:var(--bordo);margin:0 0 10px}
nav.indice ul{list-style:none;margin:0;padding:0}
nav.indice li{margin:6px 0}
nav.indice li.l3{padding-left:16px;font-size:14.5px}
nav.indice a{color:var(--ink);text-decoration:none}
nav.indice a:hover{color:var(--rojo)}
main.doc{font-size:18px;max-width:780px}
.portada .kicker{font-size:14px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--rojo)}
.portada .meta{color:var(--muted);margin:6px 0 0}
h1,h2,h3{font-family:var(--font-display);color:var(--bordo);line-height:1.15}
h1{font-size:42px;margin:8px 0 6px}
h2{font-size:29px;margin:44px 0 12px;padding-bottom:8px;border-bottom:3px solid var(--rosa)}
h3{font-size:22px;margin:30px 0 8px}
p,li{text-align:justify;hyphens:auto}
li{margin:5px 0}
code{font-family:var(--font-mono);font-size:.84em;background:#f4f4f4;padding:1px 6px;border-radius:4px}
table{border-collapse:collapse;width:100%;margin:18px 0 6px;font-size:16px;break-inside:avoid}
th{background:#f3e4e6;text-align:left}
th,td{border:1px solid #b7b7b7;padding:7px 12px;vertical-align:top}
figure{margin:26px 0;text-align:center;break-inside:avoid}
figure svg{width:100%;height:auto;max-height:520px}
figure figcaption,p>em:only-child{display:block;text-align:center;font-style:italic;color:#555;font-size:15px;margin-top:6px}
svg.uml text{font-family:var(--font-body);fill:var(--ink)}
svg.uml .halo{stroke:#fff;stroke-width:7px;paint-order:stroke;stroke-linejoin:round}
svg.uml .t-name{font-size:28px;font-weight:700}
svg.uml .t-mem,svg.uml .t-lbl,svg.uml .t-mult{font-size:24px}
svg.uml .t-mult{font-weight:700}
.print-only{display:none}
@media (max-width:900px){.wrap{grid-template-columns:1fr;gap:12px}nav.indice{position:static;max-height:none}}
@media print{
  @page{size:A4;margin:20mm 18mm}
  .top{display:none}
  .wrap{display:flex;flex-direction:column;padding:0;max-width:none}
  main.doc{display:contents;font-size:11pt}
  .wrap>*,main.doc>*{order:3}
  main.doc>.portada{order:1;padding:30mm 0 14mm}
  .wrap>nav.indice{order:2;position:static;max-height:none;page-break-after:always;font-size:14px}
  main.doc>*{font-size:11pt}
  h2,h3{break-after:avoid;page-break-after:avoid}
  p,li{orphans:3;widows:3}
}
`

export function renderApunte(file, { id, title }) {
  const dir = dirname(file)
  const md = new MarkdownIt({ html: false, typographer: false })

  // Figuras SVG en línea con epígrafe
  md.renderer.rules.image = (tokens, idx) => {
    const t = tokens[idx]
    const src = t.attrGet('src')
    const caption = t.content
    const path = join(dir, src)
    if (src.endsWith('.svg') && existsSync(path)) {
      let svg = readFileSync(path, 'utf8')
      // Los diagramas se dibujan para proyectar (letra grande): en el apunte se reducen según su tamaño.
      const vb = svg.match(/viewBox="0 0 (\d+(?:\.\d+)?) /)
      if (vb) svg = svg.replace('<svg ', `<svg style="width:min(100%,${Math.round(Number(vb[1]) * 0.7)}px)" `)
      return `<figure>${svg}<figcaption>${escapeHtml(caption)}</figcaption></figure>`
    }
    return `<img src="${escapeHtml(src)}" alt="${escapeHtml(caption)}">`
  }

  const tokens = md.parse(readFileSync(file, 'utf8'), {})
  const toc = []
  let docTitle = title
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i]
    if (t.type === 'heading_open') {
      const text = tokens[i + 1].content
      if (t.tag === 'h1') {
        docTitle = text
      } else {
        const sid = slug(text)
        t.attrSet('id', sid)
        toc.push({ level: t.tag === 'h2' ? 2 : 3, id: sid, text })
      }
    }
  }
  // La figura sola en un párrafo no debe quedar dentro de <p>
  const body = md
    .renderer.render(tokens, md.options, {})
    .replace(/<p>(<figure>[\s\S]*?<\/figure>)<\/p>/g, '$1')
    .replace(/<h1>[\s\S]*?<\/h1>/, '')

  const indice = `<nav class="indice"><h2>Índice</h2><ul>${toc
    .map((e) => `<li class="l${e.level}"><a href="#${e.id}">${escapeHtml(e.text)}</a></li>`)
    .join('')}</ul></nav>`

  return `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(docTitle)} · Apunte · DDSI K3003</title>
<style>
${fontFaces('../../fonts/')}
${TOKENS}
${CSS}
</style>
</head>
<body>
<header class="top"><a href="../../">← Todas las clases</a><span>Diseño de Sistemas de Información · K3003 · UTN FRBA</span></header>
<div class="wrap">
${indice}
<main class="doc">
<div class="portada"><div class="kicker">Apunte · ${escapeHtml(id.slice(0, 3))}</div><h1>${escapeHtml(docTitle)}</h1><p class="meta">Diseño de Sistemas de Información · K3003 · UTN FRBA · <a href="../diapositivas.pdf">Diapositivas en PDF</a></p></div>
${body}
</main>
</div>
</body>
</html>
`
}
