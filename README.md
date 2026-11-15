# wikiSI · Sistemas Informáticos (0483 · 1º DAM)

[![Autor](https://img.shields.io/badge/Autor-Mosqueteroweb-FF6F00?style=flat&logo=github)](https://github.com/mosqueteroweb)
[![GitHub Pages](https://img.shields.io/badge/Web-GitHub%20Pages-2ea44f?style=flat&logo=githubpages)](https://mosqueteroweb.github.io/wikiSI/)

Base de conocimiento curricular, píldoras prácticas y laboratorios de aula para el módulo **Sistemas Informáticos (Código 0483 - 1º DAM)**, siguiendo el patrón **LLM Wiki** y adaptada al entorno del aula (**MAX + VirtualBox**, límite de 10–12 GB de RAM para VMs).

- **Web pública:** [https://mosqueteroweb.github.io/wikiSI/](https://mosqueteroweb.github.io/wikiSI/)
- **Referencia curricular:** [dam_si_relaciones.html](https://mosqueteroweb.github.io/ismie01/DAM/dam_si_relaciones.html)

---

## Estructura del Repositorio

- `PLAN_WIKISI.md`: Plan arquitectónico y metodología de trabajo.
- `SCHEMA.md`: Reglas permanentes del agente, restricciones del aula y matriz curricular completa (RA1–RA7).
- `raw/`: Capa inmutable de fuentes (`propios/`, `inbox/`, `procesados/`, `descartados.txt`).
- `wiki/`: Capa pública compilada con **MkDocs Material** (`index.md`, `log.md`, `ra/`, `conceptos/`, `ejercicios/`, `practicas/`, `assets/`).
- `scripts/filter_unpublished.py`: Hook de MkDocs que excluye del build cualquier página con `publicar: false` (por ejemplo, soluciones de prácticas antes de terminar la clase).
- `privado_evaluacion/`: Capa privada local (exámenes, soluciones y rúbricas), **excluida del repositorio mediante `.gitignore`**.

---

## Desarrollo y Compilación Local

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Para validar el build de producción (omitiendo páginas con `publicar: false`):

```bash
.venv/bin/mkdocs build --strict
```

---

## 👤 Autor

Desarrollado por **Pedro Mosqueteroweb**  
- GitHub: [@mosqueteroweb](https://github.com/mosqueteroweb)  
- Contacto: `mosqueteroweb@gmail.com`
