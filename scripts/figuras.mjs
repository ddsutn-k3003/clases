// Extrae los diagramas de las diapositivas como SVG para reutilizarlos en el apunte.
// Uso: npm run figuras -- C01   (lee clases/C01-*/figuras.json y escribe clases/C01-*/figuras/*.svg)
// Variable opcional: CHROMIUM_PATH para usar un Chromium ya instalado.
import { spawnSync } from 'node:child_process'
import http from 'node:http'
import { existsSync, mkdirSync, mkdtempSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { extname, join } from 'node:path'
import { chromium } from 'playwright-chromium'
import { findClass, ROOT } from './lib.mjs'

const clase = findClass(process.argv[2] ?? '')
if (!clase) {
  console.error('Uso: npm run figuras -- C01')
  process.exit(1)
}
const specPath = join(clase.dir, 'figuras.json')
if (!existsSync(specPath)) {
  console.error(`No existe ${specPath}`)
  process.exit(1)
}
const spec = JSON.parse(readFileSync(specPath, 'utf8'))

const out = mkdtempSync(join(tmpdir(), 'figuras-'))
const base = '/x/'
const r = spawnSync('npx', ['slidev', 'build', clase.entry, '--base', base, '--out', out], { cwd: ROOT, stdio: 'inherit' })
if (r.status !== 0) process.exit(r.status ?? 1)

const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png' }
const server = http
  .createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]).replace(/^\/x\//, '/')
    let f = join(out, p)
    if (!existsSync(f) || statSync(f).isDirectory()) f = join(out, 'index.html')
    res.writeHead(200, { 'content-type': types[extname(f)] ?? 'application/octet-stream' })
    res.end(readFileSync(f))
  })
  .listen(0)
const port = server.address().port

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {})
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } })
const dest = join(clase.dir, 'figuras')
mkdirSync(dest, { recursive: true })
for (const f of spec) {
  await page.goto(`http://localhost:${port}${base}${f.slide}?clicks=99`, { waitUntil: 'networkidle' })
  await page.waitForTimeout(800)
  let svg = await page.evaluate(([n, i]) => document.querySelectorAll(`.slidev-page-${n} svg.uml`)[i]?.outerHTML ?? null, [f.slide, f.index])
  if (!svg) throw new Error(`No se encontró el diagrama ${f.index} en la diapositiva ${f.slide}`)
  svg = svg
    .replace(/\sdata-v-[a-z0-9]+(="")?/g, '')
    .replace(/\sclass="slidev-vclick-[^"]*"/g, '')
    .replace(/\sstyle="opacity: ?1;?"/g, '')
  writeFileSync(join(dest, `${f.name}.svg`), svg)
  console.log(`figuras/${f.name}.svg`)
}
await browser.close()
server.close()
