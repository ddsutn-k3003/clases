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

## 👨‍🏫 Si sos docente

### Una sola vez: preparar tu computadora

Necesitás tener instalados [Node.js](https://nodejs.org) (versión 20 o superior) y [Git](https://git-scm.com).

```bash
git clone https://github.com/ddsutn-k3003/clases.git
cd clases
npm install
```

### Trabajar en una clase

```bash
npm run dev -- C01
```

Se abre la clase en el navegador y se actualiza sola cada vez que guardás el archivo.

### Crear una clase nueva

```bash
npm run new -- C02 recursos "Recursos y Diagramas de Despliegue y Componentes"
```

Esto crea la carpeta `clases/C02-recursos/` con una presentación lista para completar.

### Publicar los cambios

```bash
git add .
git commit -m "Actualizo la clase C01"
git push
```

Al subir los cambios a `main`, el sitio se reconstruye solo y en unos minutos queda actualizado para los alumnos. No hay que hacer nada más.

### Comandos disponibles

| Comando | Qué hace |
| --- | --- |
| `npm run dev -- C01` | Abre la clase en modo edición |
| `npm run new -- C02 nombre "Título"` | Crea una clase nueva |
| `npm run build` | Construye todas las clases en la carpeta `dist/` |
| `npm run export` | Construye todo y además genera un PDF por clase |

## ✍️ Cómo se escribe una clase

Cada clase es un archivo `slides.md` escrito en Markdown. Las diapositivas se separan con una línea `---`:

````markdown
# Título de la diapositiva

- Un punto
- Otro punto

---

# Otra diapositiva

<DataFlow :nodes="['Cliente', 'API', 'Base de datos']" />
````

Además de texto, se pueden usar diagramas (Mermaid), aparición de elementos paso a paso y los componentes de la carpeta `shared/`, que sirven para todas las clases. Por ejemplo, `DataFlow` dibuja un flujo de datos animado. La clase `C01-uml` es un ejemplo para copiar.

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
