import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

export const ROOT = resolve(fileURLToPath(import.meta.url), '..', '..')
export const CLASES_DIR = join(ROOT, 'clases')

/** Devuelve las clases (carpetas C01-nombre con slides.md), ordenadas por número. */
export function listClasses() {
  if (!existsSync(CLASES_DIR)) return []
  return readdirSync(CLASES_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory() && /^C\d{2}-/.test(d.name))
    .filter((d) => existsSync(join(CLASES_DIR, d.name, 'slides.md')))
    .map((d) => {
      const entry = join(CLASES_DIR, d.name, 'slides.md')
      const text = readFileSync(entry, 'utf8')
      const m = text.match(/^---\n([\s\S]*?)\n---/)
      const title = m?.[1].match(/^title:\s*(.+)$/m)?.[1]?.trim() ?? d.name
      return { id: d.name, entry, title }
    })
    .sort((a, b) => a.id.localeCompare(b.id))
}

/** Resuelve "C01" o "C01-uml" a una clase. */
export function findClass(query) {
  const all = listClasses()
  return all.find((c) => c.id === query || c.id.startsWith(`${query}-`))
}
