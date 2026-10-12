// Construye todas las clases en dist/<id>/ y genera dist/index.html.
// Uso: npm run build                 -> diapositivas (HTML) y apuntes publicados
//      npm run export                -> además el PDF de las diapositivas
//      node scripts/build.mjs C01    -> solo una clase
//      BASE=/clases/ npm run build   (base de GitHub Pages; por defecto /clases/)
import { spawnSync } from 'node:child_process'
import { mkdirSync, writeFileSync, existsSync, rmSync, copyFileSync } from 'node:fs'
import { join } from 'node:path'
import { listClasses, ROOT } from './lib.mjs'
import { copyFonts } from './site.mjs'
import { renderLanding } from './landing.mjs'

const args = process.argv.slice(2)
const withPdf = args.includes('--pdf')
const only = args.find((a) => /^[CX]\d{2}/.test(a))
const base = (process.env.BASE ?? '/clases/').replace(/\/?$/, '/')
const dist = join(ROOT, 'dist')
rmSync(dist, { recursive: true, force: true })
mkdirSync(dist, { recursive: true })
copyFonts(dist)

const todas = listClasses()
if (todas.length === 0) {
  console.error('No hay clases en clases/')
  process.exit(1)
}
const clases = only ? todas.filter((c) => c.id.startsWith(only)) : todas

for (const c of clases) {
  console.log(`\n== ${c.id} ==`)
  const out = join(dist, c.id)
  let r = spawnSync('npx', ['slidev', 'build', c.entry, '--base', `${base}${c.id}/`, '--out', out], {
    cwd: ROOT,
    stdio: 'inherit',
  })
  if (r.status !== 0) process.exit(r.status ?? 1)

  // El apunte (PDF) se genera aparte con `npm run apunte -- C01` y se sube al repositorio.
  if (c.apunte) copyFileSync(c.apunte, join(out, 'apunte.pdf'))

  if (withPdf) {
    // Un PDF que falla no debe impedir publicar el sitio.
    r = spawnSync('npx', ['slidev', 'export', c.entry, '--output', join(out, 'diapositivas.pdf')], {
      cwd: ROOT,
      stdio: 'inherit',
    })
    if (r.status !== 0) console.warn(`(!) No se pudo exportar el PDF de diapositivas de ${c.id}`)
  }
}

writeFileSync(join(dist, 'index.html'), renderLanding(todas, dist))
console.log('\nListo: dist/index.html')
