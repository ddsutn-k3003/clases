import { defineMermaidSetup } from '@slidev/types'

// Mermaid con la paleta de la cátedra y trazos gruesos, pensado para proyectar.
export default defineMermaidSetup(() => ({
  theme: 'base',
  themeVariables: {
    fontFamily: "'Source Sans 3', system-ui, sans-serif",
    fontSize: '22px',
    primaryColor: '#fbe9eb',
    primaryBorderColor: '#7a1f2b',
    primaryTextColor: '#1b1b1d',
    lineColor: '#7a1f2b',
    secondaryColor: '#f1efef',
    tertiaryColor: '#ffffff',
  },
}))
