# Plan Arquitectónico: wikiSI

Base de conocimiento curricular, prácticas de aula y banco de evaluación para el módulo **Sistemas Informáticos (Código 0483 - 1º DAM)**, siguiendo el patrón **LLM Wiki** de Andrej Karpathy.

- **Referencia curricular oficial:** [dam_si_relaciones.html](https://mosqueteroweb.github.io/ismie01/DAM/dam_si_relaciones.html) (7 Resultados de Aprendizaje, RA1–RA7).
- **Inspiración metodológica:** [LLM Wiki Gist (Andrej Karpathy)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

## 1. Infraestructura y Orquestación (100% Centralizada en Mac M2 Pro)

Se elimina la Raspberry Pi para evitar duplicidad de máquinas y conflictos de sincronización Git. Todo corre centralizado en el **Mac M2 Pro (24x7)** con **Antigravity**:

- **Control desde el móvil:** Permite enviar enlaces, PDFs, apuntes propios o instrucciones de corrección/publicación desde cualquier lugar directamente al agente en Antigravity.
- **Modelos por fase (optimización de coste y calidad):**
  - **Gemini Flash / Hydrogen (rápidos y económicos):** Búsqueda web (*scouting*), extracción y limpieza a Markdown, comprobación de credibilidad de fuentes y tareas rutinarias de mantenimiento (*lint*).
  - **Gemini Argon (Orchestrator):** Compilación pedagógica en `wiki/`, creación de ejercicios y prácticas integradoras, generación de imágenes explicativas y redacción de pruebas de evaluación.
- **Gestión 100% por IA:** No es necesario instalar ni gestionar Obsidian manualmente. El agente mantiene los archivos Markdown, los enlaces cruzados, el índice, el registro cronológico y la compilación de la web pública.

---

## 2. Entorno Técnico del Aula (Restricciones en `SCHEMA.md`)

Todas las explicaciones, guías paso a paso y prácticas de laboratorio se adaptan obligatoriamente al hardware y software real del aula:

- **Sistema anfitrión (Host):** **MAX (MAdrid_linuX)** de la Comunidad de Madrid (base Ubuntu/Debian).
- **Software de virtualización:** **VirtualBox** sobre MAX.
- **Presupuesto de RAM (equipos de 16 GB):** Ninguna práctica simultánea puede superar un consumo total de **10–12 GB de RAM asignados a las VMs**, reservando memoria suficiente para el host MAX. Se indicará explícitamente la RAM asignada por máquina en cada enunciado.
- **Sistemas operativos invitados (Guests):** Variedad real según el objetivo didáctico del RA/CE:
  - **Windows:** Windows 10, Windows 11.
  - **Linux:** Ubuntu (Desktop/Server), Linux Mint, Puppy Linux (ideal para prácticas ligeras o multi-VM con poca RAM).

---

## 3. Estructura de la Web Pública vs. Carpeta Privada

```text
wikiSI/
├── PLAN_WIKISI.md            # Este documento de arquitectura
├── SCHEMA.md                 # Reglas permanentes del agente (curriculum, aula, formato, SEO/credibilidad)
├── raw/                      # CAPA 1: INMUTABLE (fuentes originales)
│   ├── propios/              # Material del profesor (apuntes, PDFs, enlaces enviados desde el móvil)
│   ├── inbox/                # Fuentes recolectadas y pre-filtradas pendientes de ingesta
│   ├── procesados/           # Fuentes ya integradas en la wiki
│   └── descartados.txt       # Lista negra de URLs/dominios rechazados (para no volver a descargarlos)
├── wiki/                     # CAPA 2: WEB PÚBLICA (compilada para alumnos en GitHub Pages)
│   ├── index.md              # Catálogo maestro e índice por RA y Criterios de Evaluación (CE)
│   ├── log.md                # Registro cronológico (ingest, lint, revisiones)
│   ├── assets/               # Imágenes locales (diagramas, gráficos generados o abiertos)
│   ├── ra/                   # 7 páginas Hub (RA1.md .. RA7.md) con cobertura por CE
│   ├── conceptos/            # Páginas teóricas con imágenes y recursos adicionales
│   ├── ejercicios/           # Ejercicios prácticos sencillos resueltos (paso a paso)
│   └── practicas/            # Prácticas integradoras de clase (enunciado + guía de resolución)
└── privado_evaluacion/       # CAPA PRIVADA (.gitignore - NUNCA se sube al repo público)
    ├── examenes/             # Pruebas escritas, prácticas evaluables y bancos Moodle/GIFT
    ├── soluciones/           # Solucionarios de examen
    └── rubricas/             # Rúbricas trazadas por RAx.CEy
```

> **Seguridad anti-filtraciones:** `privado_evaluacion/` permanece excluida del repositorio público mediante `.gitignore` (o alojada en un repositorio privado distinto). Antigravity puede leer `wiki/` y `privado_evaluacion/` a la vez en el Mac para alinear los exámenes con lo dado en clase sin riesgo de exposición pública.

---

## 4. Progresión Pedagógica y Ritmo de Construcción

### Orden de desarrollo
Construcción **secuencial por Resultados de Aprendizaje**: se completa e integra `RA1` (conceptos + ejercicios + práctica + validación) antes de avanzar con `RA2`, y así sucesivamente hasta `RA7`.

### Estructura de los 4 niveles por bloque/RA

1. **Conceptos (`wiki/conceptos/`):**
   - Explicación clara con comparativas entre sistemas libres y propietarios cuando aplique.
   - **Imágenes explicativas obligatorias:**
     - Diagramas técnicos editables en **Mermaid** o **SVG**.
     - Ilustraciones conceptuales generadas con **Gemini (`image-generator`)** guardadas en `wiki/assets/`.
     - Imágenes de webs con licencia abierta que lo permitan (Wikimedia Commons, documentación oficial CC/MIT, etc.), descargadas en local en `wiki/assets/` con atribución para evitar enlaces rotos.
   - **Sección final obligatoria `## Recursos para profundizar`:**
     - Enlaces a artículos técnicos de referencia para ampliar.
     - Enlaces a vídeos explicativos de YouTube relevantes al concepto tratado.

2. **Ejercicios prácticos sencillos resueltos (`wiki/ejercicios/`):**
   - Píldoras cortas enfocadas en una destreza concreta (p. ej., comando, particionado, permisos, configuración de red).
   - Incluyen enunciado breve y **resolución paso a paso** (pensados para ejecutarse en MAX / VirtualBox con los SO invitados).

3. **Práctica de clase integradora (`wiki/practicas/`):**
   - Diseñada para que el alumno la resuelva apoyándose directamente en los ejercicios sencillos previos.
   - Dividida siempre en **dos documentos enlazados**:
     - **Enunciado (`pXX-enunciado.md`):** con frontmatter `publicar: true` desde el inicio, indicando requisitos de VM (RAM, SO invitado), tareas y evidencias a entregar en el Aula Virtual.
     - **Guía de resolución paso a paso (`pXX-solucion.md`):** con frontmatter `publicar: false` por defecto. El sistema de publicación oculta las páginas con `publicar: false` hasta que el profesor indique al agente cambiarlo a `publicar: true` tras la clase.

4. **Evaluación privada (`privado_evaluacion/`):**
   - Exámenes teóricos/prácticos y solucionarios alineados con los `RA` y `CE` cubiertos en la wiki pública.

---

## 5. Protocolo de Credibilidad de Fuentes y Reversibilidad

### Verificación de reputación en 3 niveles (antes de ingestar en `raw/`)
1. **Nivel 1 (Autoridad máxima):** Documentación oficial de fabricantes y proyectos (Microsoft Learn, Debian/Ubuntu/Arch Wiki, Red Hat Docs, Kernel.org, VirtualBox Manual, RFCs/IETF, guías oficiales de MAX/EducaMadrid).
2. **Nivel 2 (Reputación técnica contrastada):** Universidades, instituciones educativas públicas, libros técnicos reconocidos y medios/portales de ingeniería sin granjas de contenido SEO.
3. **Nivel 3 (Descarte automático):** Blogs anónimos generados por IA, portales con errores técnicos detectados, páginas sin fecha o con contenido contradictorio sin respaldo.

### Trazabilidad inversa y borrado limpio
- Toda página de `wiki/` lista sus fuentes en el frontmatter YAML (`fuentes: [...]`) y marca afirmaciones o bloques clave con comentarios de trazabilidad (`<!-- fuente: raw/procesados/... -->`).
- Cada compilación genera un **commit atómico en Git**.
- Si el profesor pide *"quita esta fuente"* o *"corrige este dato"*:
  1. El agente localiza todas las páginas afectadas en `wiki/` mediante búsqueda de referencias.
  2. Reescribe/limpia el contenido afectado manteniendo la coherencia del grafo.
  3. Añade la URL o dominio a `raw/descartados.txt` para que no vuelva a ser seleccionada en futuras búsquedas automáticas.

---

## 6. Stack de Publicación Web (Visual y Mantenido por IA)

Para transformar los `.md` en una web moderna, rápida y visualmente agradable sin gestión manual:

- **Opciones recomendadas para implementar en el siguiente paso:**
  - **MkDocs con tema Material (`mkdocs-material`):** Ideal para entornos educativos; soporta nativamente bloques desplegables (`??? note "Ver solución"`), pestañas por sistema operativo (`=== "Ubuntu" / === "Windows 10"`), diagramas Mermaid, modo claro/oscuro, buscador instantáneo y filtro de publicación (`publicar: false`) mediante plugin o script previo al build en GitHub Actions.
  - **Astro Starlight:** Estética muy cuidada, alto rendimiento y componentes interactivos modernos en MDX/Markdown.
- El despliegue se automatizará mediante **GitHub Actions -> GitHub Pages**, permitiendo al profesor enlazar directamente cada página de conceptos, ejercicios o prácticas desde el Aula Virtual.
