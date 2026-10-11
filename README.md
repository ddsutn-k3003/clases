<div align="center">

# 📚 Clases de Diseño de Sistemas de Información

**Curso K3003 · DDSI · UTN FRBA**

[**Ver las clases online →**](https://ddsutn-k3003.github.io/clases/)

</div>

---

Este repositorio reúne **todas las clases del curso** en un solo lugar. Cada clase es una presentación que se abre en el navegador y también se puede descargar en PDF.

## 👩‍🎓 Si sos alumno

Entrá a **https://ddsutn-k3003.github.io/clases/**. Vas a ver el índice con todas las clases, ordenadas por número.

- Hacé clic en una clase para abrirla.
- Navegá con las flechas del teclado (← →) o haciendo clic en los bordes de la pantalla.
- Apretá `o` para ver un resumen con todas las diapositivas, y `f` para pantalla completa.
- Si preferís leerla sin conexión, cada clase tiene su **PDF** al lado del título.

No necesitás instalar nada.

## 🧱 Cómo está armado

```
clases/
├── clases/                  una carpeta por clase (C01-uml, C02-recursos, ...)
│   └── C01-uml/slides.md
├── shared/                  componentes, estilos y configuración comunes
│   ├── components/
│   └── styles/
├── scripts/                 comandos de desarrollo, construcción y creación de clases
└── .github/workflows/       publicación automática
```

**Tecnologías**

- [Slidev](https://sli.dev): presentaciones en Markdown
- [Vue](https://vuejs.org): componentes interactivos y animados
- [Mermaid](https://mermaid.js.org): diagramas dentro de las diapositivas
- [Node.js](https://nodejs.org) y [npm](https://www.npmjs.com): herramientas de construcción
- [GitHub Actions](https://docs.github.com/actions) y [GitHub Pages](https://pages.github.com): construcción y publicación automáticas
