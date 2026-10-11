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
theme: default
title: ${num} - ${title}
info: |
  Diseño de Sistemas de Información - K3003 - UTN FRBA
class: text-center
transition: slide-left
mdc: true
addons:
  - slidev-addon-ddsi
addons:
  - slidev-addon-ddsi
---

# ${title}

Diseño de Sistemas de Información · K3003 · UTN FRBA

---

# Primera slide
`,
)
console.log(`Creada ${dir}`)
