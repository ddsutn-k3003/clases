// Uso: npm run dev -- C01   (abre la clase en modo desarrollo)
import { spawn } from 'node:child_process'
import { findClass, listClasses, ROOT } from './lib.mjs'

const query = process.argv[2]
const clase = query ? findClass(query) : undefined
if (!clase) {
  console.log('Indicá la clase. Clases disponibles:')
  for (const c of listClasses()) console.log(`  ${c.id}  ${c.title}`)
  process.exit(query ? 1 : 0)
}
spawn('npx', ['slidev', clase.entry, '--open'], { cwd: ROOT, stdio: 'inherit' })
