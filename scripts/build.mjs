// Construye todas las clases en dist/<id>/ y genera dist/index.html.
// Uso: npm run build            -> HTML de todas las clases
//      npm run export          -> además exporta PDF de cada clase
//      BASE=/clases/ npm run build   (base de GitHub Pages; por defecto /clases/)
import { spawnSync } from 'node:child_process'
import { mkdirSync, writeFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import { listClasses, ROOT } from './lib.mjs'

const withPdf = process.argv.includes('--pdf')
const base = (process.env.BASE ?? '/clases/').replace(/\/?$/, '/')
const dist = join(ROOT, 'dist')
mkdirSync(dist, { recursive: true })

const clases = listClasses()
if (clases.length === 0) {
  console.error('No hay clases en clases/')
  process.exit(1)
}

for (const c of clases) {
  console.log(`\n== ${c.id} ==`)
  const out = join(dist, c.id)
  let r = spawnSync(
    'npx',
    ['slidev', 'build', c.entry, '--base', `${base}${c.id}/`, '--out', out],
    { cwd: ROOT, stdio: 'inherit' },
  )
  if (r.status !== 0) process.exit(r.status ?? 1)
  if (withPdf) {
    r = spawnSync(
      'npx',
      ['slidev', 'export', c.entry, '--output', join(dist, `${c.id}.pdf`)],
      { cwd: ROOT, stdio: 'inherit' },
    )
    if (r.status !== 0) process.exit(r.status ?? 1)
  }
}

const rows = clases
  .map((c) => {
    const pdf = existsSync(join(dist, `${c.id}.pdf`)) ? ` · <a href="${c.id}.pdf">PDF</a>` : ''
    return `<li><a href="${c.id}/">${c.title}</a>${pdf}</li>`
  })
  .join('\n      ')

writeFileSync(
  join(dist, 'index.html'),
  `<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>DDSI K3003 - Clases</title>
    <style>
      body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1rem; line-height: 1.6; }
      li { margin: .35rem 0; }
    </style>
  </head>
  <body>
    <h1>Diseño de Sistemas de Información</h1>
    <p>Curso K3003 · UTN FRBA</p>
    <ul>
      ${rows}
    </ul>
  </body>
</html>
`,
)
console.log('\nListo: dist/index.html')
