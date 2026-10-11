# Clases · Diseño de Sistemas de Información

Material de clase del curso **K3003** de **Diseño de Sistemas de Información (DDSI)** · UTN FRBA.

Las clases publicadas están en: **https://ddsutn-k3003.github.io/clases/**

## Estructura

```
clases/
├── clases/                 una carpeta por clase: C01-uml, C02-recursos, ...
│   └── C01-uml/slides.md
├── shared/                 componentes, estilos y configuración comunes a todas las clases
│   └── components/
├── scripts/                dev, build y creación de clases nuevas
└── .github/workflows/      publicación automática en GitHub Pages
```

## Trabajar en una clase

Requiere Node.js 20 o superior.

```bash
npm install                 # una sola vez
npm run dev -- C01          # abre la clase C01 en modo desarrollo
npm run new -- C02 recursos "Recursos y Diagramas de Despliegue y Componentes"
npm run build               # construye todas las clases en dist/
npm run export              # además genera un PDF por clase
```

Cada clase se escribe en `slides.md`. Los componentes de `shared/components` se pueden usar en cualquier clase sin importarlos.

## Publicación

Cada push a `main` construye todas las clases y las publica en GitHub Pages. Para activarlo, en **Settings → Pages** elegir como fuente **GitHub Actions**.
