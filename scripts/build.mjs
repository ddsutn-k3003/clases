// Construye todas las clases en dist/<id>/ y genera dist/index.html.
// Uso: npm run build                 -> HTML de diapositivas y apuntes
//      npm run export                -> además PDF de diapositivas y de apuntes
//      node scripts/build.mjs C01    -> solo una clase
//      BASE=/clases/ npm run build   (base de GitHub Pages; por defecto /clases/)
//      CHROMIUM_PATH=...             (navegador para los PDF de apuntes, opcional)
import { spawnSync } from 'node:child_process'
import { mkdirSync, writeFileSync, existsSync, rmSync } from 'node:fs'
import { join } from 'node:path'
import { listClasses, ROOT } from './lib.mjs'
import { copyFonts } from './site.mjs'
import { renderApunte } from './apunte.mjs'
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

let browser = null
async function apuntePdf(htmlPath, pdfPath) {
  const { chromium } = await import('playwright-chromium')
  browser ??= await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined })
  const page = await browser.newPage()
  await page.goto(`file://${htmlPath}`)
  await page.evaluate(() => document.fonts.ready)
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate:
      '<div style="width:100%;font-size:9px;font-family:sans-serif;text-align:center;color:#555"><span class="pageNumber"></span> de <span class="totalPages"></span></div>',
    margin: { top: '20mm', bottom: '22mm', left: '18mm', right: '18mm' },
  })
  await page.close()
}

for (const c of clases) {
  console.log(`\n== ${c.id} ==`)
  const out = join(dist, c.id)
  let r = spawnSync('npx', ['slidev', 'build', c.entry, '--base', `${base}${c.id}/`, '--out', out], {
    cwd: ROOT,
    stdio: 'inherit',
  })
  if (r.status !== 0) process.exit(r.status ?? 1)

  if (c.apunte) {
    const dir = join(out, 'apunte')
    mkdirSync(dir, { recursive: true })
    writeFileSync(join(dir, 'index.html'), renderApunte(c.apunte, { id: c.id, title: c.title }))
    console.log(`Apunte: ${c.id}/apunte/`)
  }

  if (withPdf) {
    // Un PDF que falla no debe impedir publicar el sitio.
    r = spawnSync('npx', ['slidev', 'export', c.entry, '--output', join(out, 'diapositivas.pdf')], {
      cwd: ROOT,
      stdio: 'inherit',
    })
    if (r.status !== 0) console.warn(`(!) No se pudo exportar el PDF de diapositivas de ${c.id}`)
    if (c.apunte) {
      try {
        await apuntePdf(join(out, 'apunte', 'index.html'), join(out, 'apunte.pdf'))
      } catch (e) {
        console.warn(`(!) No se pudo exportar el PDF del apunte de ${c.id}: ${e.message}`)
      }
    }
  }
}
if (browser) await browser.close()

writeFileSync(join(dist, 'index.html'), renderLanding(todas, dist))
console.log('\nListo: dist/index.html')
