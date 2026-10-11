import { defineConfig } from 'vite'

// Workaround: el minificador de CSS por defecto (lightningcss) falla con los estilos de Slidev.
export default defineConfig({
  build: { cssMinify: false },
})
