// Convierte SVG a PNG con Chromium. Uso: node scripts/svg2png.mjs figuras/ [escala]
// Variable opcional: CHROMIUM_PATH
import { readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { chromium } from 'playwright-chromium'

const dir = process.argv[2]
const scale = Number(process.argv[3] ?? 2.5)
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {})
const page = await browser.newPage({ deviceScaleFactor: scale })
for (const f of readdirSync(dir).filter((f) => f.endsWith('.svg'))) {
  const svg = readFileSync(join(dir, f), 'utf8')
  await page.setContent(`<body style="margin:0;background:#fff">${svg}</body>`)
  await page.locator('svg').first().screenshot({ path: join(dir, f.replace(/\.svg$/, '.png')) })
}
await browser.close()
