// Estilos y utilidades compartidos por la página principal y los apuntes.
import { copyFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'
import { ROOT } from './lib.mjs'

const FONTS = [
  ['source-sans-3', 'Source Sans 3', 'normal', 'source-sans-3-latin-wght-normal.woff2'],
  ['source-sans-3', 'Source Sans 3', 'italic', 'source-sans-3-latin-wght-italic.woff2'],
  ['source-serif-4', 'Source Serif 4', 'normal', 'source-serif-4-latin-wght-normal.woff2'],
  ['source-serif-4', 'Source Serif 4', 'italic', 'source-serif-4-latin-wght-italic.woff2'],
  ['jetbrains-mono', 'JetBrains Mono', 'normal', 'jetbrains-mono-latin-wght-normal.woff2'],
]

/** Copia las tipografías a dist/fonts. */
export function copyFonts(dist) {
  const out = join(dist, 'fonts')
  mkdirSync(out, { recursive: true })
  for (const [pkg, , , file] of FONTS) {
    copyFileSync(join(ROOT, 'node_modules', '@fontsource-variable', pkg, 'files', file), join(out, file))
  }
}

export function fontFaces(fontBase) {
  return FONTS.map(
    ([, family, style, file]) =>
      `@font-face{font-family:'${family}';font-style:${style};font-weight:200 900;font-display:swap;src:url('${fontBase}${file}') format('woff2')}`,
  ).join('\n')
}

export const TOKENS = `
:root{--font-display:'Source Serif 4',Georgia,serif;--font-body:'Source Sans 3',system-ui,sans-serif;--font-mono:'JetBrains Mono',ui-monospace,monospace;
--ink:#1b1b1d;--muted:#5a5557;--paper:#fff;--rojo:#b4182d;--bordo:#6d1327;--rosa:#fbe9eb;--rosa-borde:#7a1f2b;--gris:#f1efef;--gris-borde:#3b3b3f}
*{box-sizing:border-box}
body{margin:0;font-family:var(--font-body);color:var(--ink);background:var(--paper);line-height:1.6}
a{color:var(--rojo)}
`

export const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
