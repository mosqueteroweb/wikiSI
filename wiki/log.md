---
title: "Registro Cronológico (Log)"
tipo: "indice"
publicar: true
ultima_revision: "2026-11-15"
---

# Registro Cronológico (`log.md`)

Bitácora de operaciones (*ingest*, *compile*, *lint*, *publish*) ejecutadas sobre la base de conocimiento `wikiSI`, siguiendo el patrón LLM Wiki.

---

## [2026-11-15] Compilación completa del bloque RA2 (6 conceptos, 6 SVGs, 5 ejercicios `e06`–`e10`, práctica `p02` y banco de evaluación privado)

- **Fuentes procesadas (`raw/procesados/`):** `ra2-arquitectura-so-licencias.md`, `ra2-virtualizacion-planificacion-instalacion.md`, `ra2-arranque-aplicaciones-recuperacion-doc.md`.
- **Conceptos publicados (`wiki/conceptos/`):** 6 páginas completas cubriendo `RA2.a`–`RA2.i` con tabs duales MAX/Ubuntu y Windows 10/11, plus 6 diagramas SVG locales (`wiki/assets/ra2-*.svg`).
- **Ejercicios resueltos (`wiki/ejercicios/`):** `e06`–`e10` con presupuesto de RAM $\le 6\text{ GB}$ sobre hosts MAX de 16 GB.
- **Práctica Integradora (`wiki/practicas/`):** Enunciado público `p02` (`DAM-Estacion-Dual` 4 GB + `DAM-Rescate-Puppy` 1 GB = 5 GB) y solución docente marcada con `publicar: false`.
- **Evaluación privada (`privado_evaluacion/`):** Examen teórico-práctico RA2 (18 preguntas + bloque Moodle GIFT + 3 supuestos), solucionario y rúbrica `RA2.a`–`RA2.i` (excluido de Git vía `.gitignore`).

---

## [2026-11-15] Compilación completa del bloque RA1 (6 conceptos, 6 SVGs, 5 ejercicios, práctica p01 y banco de evaluación privado)

- **Tipo:** `ingest` · `compile` · `publish`
- **Resumen:**
  - Documentadas 3 fuentes técnicas de Nivel 1/2 en `raw/procesados/` (`ra1-hardware-cpu-placas.md`, `ra1-memorias-arranque-perifericos.md`, `ra1-redes-fisica-topologias-prl.md`).
  - Generadas 6 ilustraciones vectoriales SVG locales en `wiki/assets/` cubriendo Von Neumann/placas base, pirámide de memorias, arranque BIOS/UEFI, buses PCIe/NVMe/USB, código de colores T568A/B y ergonomía PVD/ESD.
  - Compilados los 6 conceptos teóricos en `wiki/conceptos/` (`RA1.a`–`RA1.h`), los 5 ejercicios sencillos resueltos (`e01`–`e05`) en `wiki/ejercicios/` y la práctica integradora `p01` (enunciado público + solución privada con `publicar: false`).
  - Creado el banco privado de evaluación de RA1 en `privado_evaluacion/` (examen teórico-práctico con bloque GIFT Moodle, solucionario completo y rúbrica por criterio `RA1.a`–`RA1.h`).
  - Actualizados `wiki/ra/RA1.md`, índices, navegación en `mkdocs.yml` y desplegado en GitHub Pages.

---

## [2026-11-15] Inicialización de la Arquitectura `wikiSI` y Despliegue en GitHub Pages

- **Tipo:** `init` · `schema` · `publish`
- **Resumen:**
  - Creada la estructura de tres capas: `raw/` (`propios/`, `inbox/`, `procesados/`, `descartados.txt`), `wiki/` (`assets/`, `ra/`, `conceptos/`, `ejercicios/`, `practicas/`) y `privado_evaluacion/` (excluida en `.gitignore`).
  - Redactado `SCHEMA.md` con las restricciones del aula (MAX + VirtualBox + límite total de 10–12 GB de RAM por sesión + SO invitados Windows 10/11, Ubuntu, Linux Mint y Puppy Linux) y la matriz curricular completa RA1–RA7 extraída de [dam_si_relaciones.html](https://mosqueteroweb.github.io/ismie01/DAM/dam_si_relaciones.html).
  - Creadas las 7 páginas Hub (`wiki/ra/RA1.md` a `wiki/ra/RA7.md`), los índices por nivel y `wiki/index.md` con la identidad de **Pedro Mosqueteroweb**.
  - Configurado **MkDocs Material** (`mkdocs.yml`) con soporte Mermaid, pestañas de sistemas operativos, bloques desplegables, filtro automático de frontmatter `publicar: false` (`scripts/filter_unpublished.py`) y flujo CI/CD en `.github/workflows/deploy.yml` para GitHub Pages.
- **Siguiente hito:** Ingesta de fuentes de Nivel 1/2 para iniciar el desarrollo secuencial completo de **RA1**.
