---
tema: "Documentación Técnica con Ofimática, Markdown, Docs-as-Code, Trabajo Colaborativo y Búsqueda Técnica"
ra: RA7
ce:
  - RA7.c
  - RA7.f
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA7 (2/3) · Ofimática, Documentación Markdown y Trabajo Colaborativo

## 1. Suites Ofimáticas y Trabajo Colaborativo (`RA7.c`)

- **LibreOffice (MAX / Ubuntu / Windows):** Suite FOSS estándar (Writer, Calc, Impress, Base, Draw) con formatos nativos abiertos **ODF (`.odt`, `.ods`, `.odp`)**, exportación nativa **PDF/A** y control de cambios colaborativo.
- **Colaboración en tiempo real y control documental:** plataformas como **Nextcloud + Collabora Online**, **Google Workspace** o **Microsoft 365** añaden edición concurrente, historial de versiones, comentarios con menciones y permisos granulares (solo lectura / comentar / editar).
- **Buenas prácticas de maquetación corporativa:** uso estricto de **estilos** (`Título 1`, `Título 2`, `Cuerpo de texto`) en lugar de formato manual para generar **tablas de contenido automáticas**, numeración coherente, cabeceras/pies institucionales y exportación accesible a PDF.

## 2. Documentación Técnica Moderna: **Markdown y *Docs-as-Code*** (`RA7.c`)

- En entornos **DAM / DevOps**, la documentación técnica vive junto al código fuente (`README.md`, `CHANGELOG.md`, wikis en **MkDocs** o **GitHub Pages**):
  - Sintaxis ligera legible en plano (`#`, listas, tablas GFM, bloques de código con lenguaje ```` ```bash ````, diagramas **Mermaid**, enlaces relativos).
  - Versionable en **Git** (*pull requests*, revisión por pares, *diffs* claros, despliegue automático mediante CI/CD).
  - Conversión universal de formatos con **`pandoc`**: transformar Markdown en `.pdf`, `.docx`, `.odt` o HTML de un solo comando.

## 3. Búsqueda Eficaz de Documentación Técnica y Contraste de Fuentes (`RA7.f`)

- **Fuentes primarias oficiales frente a foros antiguos:** priorizar páginas `man` (`man <cmd>`, `tldr`), `--help`, documentación oficial de proyecto (Microsoft Learn, Ubuntu Docs, ArchWiki, MDN, Python Docs, IETF RFCs) frente a blogs sin fecha o respuestas obsoletas.
- **Técnicas de búsqueda avanzada en web y documentación:** operadores (`site:learn.microsoft.com`, `"mensaje exacto de error"`, `filetype:pdf`, `-pinterest`), lectura crítica de fechas de versión y validación en laboratorio VirtualBox aislado antes de ejecutar comandos destructivos extraídos de Internet.
