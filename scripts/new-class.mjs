// Uso: npm run new -- C02 recursos "Recursos y Diagramas de Despliegue y Componentes"
import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { CLASES_DIR } from './lib.mjs'

const [num, slug, ...rest] = process.argv.slice(2)
if (!/^C\d{2}$/.test(num ?? '') || !slug) {
  console.error('Uso: npm run new -- C02 recursos "Título de la clase"')
  process.exit(1)
}
const title = rest.join(' ') || slug
const dir = join(CLASES_DIR, `${num}-${slug}`)
if (existsSync(dir)) {
  console.error(`Ya existe ${dir}`)
  process.exit(1)
}
mkdirSync(dir, { recursive: true })
writeFileSync(
  join(dir, 'slides.md'),
  `---
theme: none
colorSchema: light
routerMode: hash
addons:
  - slidev-addon-ddsi
title: ${num} - ${title}
info: |
  Diseño de Sistemas de Información - K3003 - UTN FRBA
canvasWidth: 1280
aspectRatio: 16/9
transition: fade
layout: cover
---

<div class="kicker">Clase ${Number(num.slice(1))}</div>

# ${title}

<div class="sub">Subtítulo de la clase</div>

---

# Primera diapositiva

<p class="lead">Una idea por diapositiva.</p>
`,
)
writeFileSync(
  join(dir, 'apunte.md'),
  `# ${title}

## Objetivo

Una oración que diga qué se busca comprender con esta clase.

## Introducción

## Resumen

## Referencias
`,
)
console.log(`Creada ${dir} (slides.md y apunte.md)`)
