<div align="center">

# 📚 Clases de Diseño de Sistemas de Información

**Curso K3003 · DDSI · UTN FRBA**

[**Ver las clases online →**](https://ddsutn-k3003.github.io/clases/)

</div>

---

Este repositorio reúne **todas las clases del curso** en un solo lugar. Cada clase tiene sus **diapositivas** (se abren en el navegador) y un **apunte** con la teoría completa, en PDF.

## 👩‍🎓 Si sos alumno

Entrá a **https://ddsutn-k3003.github.io/clases/**. Vas a ver el índice con todas las clases, ordenadas por número.

- Cada clase tiene las diapositivas, el apunte en PDF y el PDF de las diapositivas.
- Para estudiar podés usar el apunte, los complementos del cronograma, la bibliografía del final y tus notas de clase.
- Navegá con las flechas del teclado (← →) o haciendo clic en los bordes de la pantalla.
- Apretá `o` para ver un resumen con todas las diapositivas, y `f` para pantalla completa.
- Si preferís leer sin conexión, descargá los **PDF**.

No necesitás instalar nada.

## 🧱 Cómo está armado

```
clases/
├── clases/                  una carpeta por clase (C01-uml, C02-recursos, ...)
│   └── C01-uml/             slides.md, apunte.md, apunte.pdf y figuras/
├── shared/                  componentes, estilos y configuración comunes
│   ├── components/
│   ├── layouts/
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
