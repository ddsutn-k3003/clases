// Genera la página principal (dist/index.html).
import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { fontFaces, TOKENS, escapeHtml } from './site.mjs'

const CSS = `
body{background:#fff}
header.hero{border-bottom:6px solid var(--rojo);padding:56px 24px 40px;background:linear-gradient(180deg,#fff 0%,var(--rosa) 100%)}
.inner{max-width:1040px;margin:0 auto}
.kicker{font-size:14px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--rojo)}
h1{font-family:var(--font-display);font-size:clamp(34px,6vw,58px);line-height:1.08;color:var(--bordo);margin:10px 0 12px}
.meta{font-size:19px;color:var(--muted);margin:0}
main{max-width:1040px;margin:0 auto;padding:36px 24px 72px}
h2{font-family:var(--font-display);font-size:28px;color:var(--bordo);margin:44px 0 6px;padding-bottom:8px;border-bottom:3px solid var(--rosa)}
h2:first-child{margin-top:0}
.sub{color:var(--muted);margin:0 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin-top:18px}
.card{border:3px solid var(--rosa-borde);border-radius:12px;background:#fff;padding:18px 20px 16px;display:flex;flex-direction:column;gap:10px}
.card .num{font-family:var(--font-display);font-weight:700;color:var(--rojo);font-size:15px;letter-spacing:.08em}
.card h3{font-family:var(--font-display);font-size:23px;line-height:1.2;margin:0;color:var(--ink)}
.links{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto}
.links a{font-size:15px;font-weight:600;text-decoration:none;border:2px solid var(--rosa-borde);border-radius:999px;padding:3px 14px;color:var(--bordo)}
.links a.main{background:var(--rojo);border-color:var(--rojo);color:#fff}
.links a:hover{background:var(--bordo);border-color:var(--bordo);color:#fff}
.help{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:14px}
.help div{background:var(--gris);border-left:5px solid var(--rojo);padding:10px 14px;border-radius:4px}
kbd{font-family:var(--font-mono);font-size:.85em;background:#fff;border:1.5px solid var(--gris-borde);border-bottom-width:3px;border-radius:5px;padding:0 6px}
.note{color:var(--muted);font-size:16px;margin-top:28px}
footer{border-top:1px solid #ddd;padding:22px 24px 40px;text-align:center;color:var(--muted);font-size:15px}
`

function links(c, dist) {
  const l = [`<a class="main" href="${c.id}/">Diapositivas</a>`]
  if (existsSync(join(dist, c.id, 'apunte.pdf'))) l.push(`<a href="${c.id}/apunte.pdf">Apunte (PDF)</a>`)
  if (existsSync(join(dist, c.id, 'diapositivas.pdf'))) l.push(`<a href="${c.id}/diapositivas.pdf">Diapositivas (PDF)</a>`)
  return l.join('')
}

const card = (c, dist) => `<article class="card"><span class="num">${c.num}</span><h3>${escapeHtml(c.title)}</h3><div class="links">${links(c, dist)}</div></article>`

export function renderLanding(clases, dist) {
  const reg = clases.filter((c) => !c.extra)
  return `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clases · Diseño de Sistemas de Información · K3003</title>
<style>
${fontFaces('fonts/')}
${TOKENS}
${CSS}
</style>
</head>
<body>
<header class="hero"><div class="inner">
<div class="kicker">UTN FRBA · Curso K3003 · Sábados por la mañana · 2027</div>
<h1>Diseño de Sistemas de Información</h1>
<p class="meta">Diapositivas y apuntes de cada clase.</p>
</div></header>
<main>
<h2>Cómo usar las diapositivas</h2>
<div class="help">
<div><kbd>←</kbd> <kbd>→</kbd> para avanzar y retroceder. Cada pulsación revela el siguiente paso.</div>
<div><kbd>o</kbd> muestra todas las diapositivas en una grilla.</div>
<div><kbd>f</kbd> pasa a pantalla completa.</div>
<div>El apunte de cada clase se descarga en PDF.</div>
</div>

<h2>Clases</h2>
<p class="sub">Cada clase tiene sus diapositivas y un apunte con la teoría completa. Las clases restantes se publican a medida que avanza la cursada.</p>
<div class="grid">
${reg.map((c) => card(c, dist)).join('\n')}
</div>
<p class="note">Para estudiar se puede usar el apunte, los complementos del cronograma, la bibliografía que figura al final de cada clase y las notas tomadas en clase.</p>
</main>
<footer>Cátedra de Diseño de Sistemas de Información · UTN FRBA · <a href="https://github.com/ddsutn-k3003">github.com/ddsutn-k3003</a></footer>
</body>
</html>
`
}
