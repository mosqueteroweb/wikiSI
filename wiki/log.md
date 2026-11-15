---
title: "Registro Cronológico (Log)"
tipo: "indice"
publicar: true
ultima_revision: "2026-11-15"
---

# Registro Cronológico (`log.md`)

Bitácora de operaciones (*ingest*, *compile*, *lint*, *publish*) ejecutadas sobre la base de conocimiento `wikiSI`, siguiendo el patrón LLM Wiki.

---

## [2026-11-15] Inicialización de la Arquitectura `wikiSI` y Despliegue en GitHub Pages

- **Tipo:** `init` · `schema` · `publish`
- **Resumen:**
  - Creada la estructura de tres capas: `raw/` (`propios/`, `inbox/`, `procesados/`, `descartados.txt`), `wiki/` (`assets/`, `ra/`, `conceptos/`, `ejercicios/`, `practicas/`) y `privado_evaluacion/` (excluida en `.gitignore`).
  - Redactado `SCHEMA.md` con las restricciones del aula (MAX + VirtualBox + límite total de 10–12 GB de RAM por sesión + SO invitados Windows 10/11, Ubuntu, Linux Mint y Puppy Linux) y la matriz curricular completa RA1–RA7 extraída de [dam_si_relaciones.html](https://mosqueteroweb.github.io/ismie01/DAM/dam_si_relaciones.html).
  - Creadas las 7 páginas Hub (`wiki/ra/RA1.md` a `wiki/ra/RA7.md`), los índices por nivel y `wiki/index.md` con la identidad de **Pedro Mosqueteroweb**.
  - Configurado **MkDocs Material** (`mkdocs.yml`) con soporte Mermaid, pestañas de sistemas operativos, bloques desplegables, filtro automático de frontmatter `publicar: false` (`scripts/filter_unpublished.py`) y flujo CI/CD en `.github/workflows/deploy.yml` para GitHub Pages.
- **Siguiente hito:** Ingesta de fuentes de Nivel 1/2 para iniciar el desarrollo secuencial completo de **RA1**.
