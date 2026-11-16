---
title: "Registro Cronológico (Log)"
tipo: "indice"
publicar: true
ultima_revision: "2026-11-15"
---

# Registro Cronológico (`log.md`)

Bitácora de operaciones (*ingest*, *compile*, *lint*, *publish*) ejecutadas sobre la base de conocimiento `wikiSI`, siguiendo el patrón LLM Wiki.

---

## [2026-11-16] Ingesta curada del `.mbz` del curso y paneles laterales colapsables en la web

- **Interfaz web (`wiki/assets/` y `mkdocs.yml`):** añadidos controles CSS/JS (`layout-colapsable.css` y `layout-colapsable.js`) para colapsar de forma independiente o conjunta la barra de navegación izquierda (`[`) y la tabla de contenidos derecha (`]`), ampliando el ancho útil de lectura (`94vw` en ancho completo).
- **Enriquecimiento curado en `wiki/` (`RA1`–`RA7`):** integrados en la documentación de alumnos y profesores los recursos prácticos rescatados del `.mbz` y Google Drive (Placa Base Explorable, ciclo de instrucción máquina y tabla de variables Java/IEEE 754 en `RA1`; bypass TPM y `ms-cxh:localonly` para Windows 11, USB Ventoy y 6 vías de paquetería en `RA2`; Storage Spaces Windows + Clonezilla multicast + `rclone` en `RA3`; Registro de Windows + 6 ejercicios, `Monitor de Confiabilidad`, `winscript`/`PowerToys`, filtros `cut`/`sed`/`awk` y taller Docker en `RA4`; emulador TP-Link + CG-NAT/DDNS en `RA5`; experimento EFS Pedro/Luis y acceso remoto con RustDesk en `RA6`; modelos Cloud, VPS LAMP, TiddlyWiki y manual de aplicaciones comunes en `RA7`).
- **Catálogo de tareas entregables (`p08`):** creado el enunciado público (`p08-tareas-curso-aula-virtual-enunciado.md`) y los solucionarios privados (`p08-tareas-curso-aula-virtual-solucion.md` con solución PRL-FFE y caso EFS Pedro/Luis).
- **Capa exclusiva del Portal Docente (`privado_evaluacion/`):** incorporada la Guía Docente en PDF (`IFCS02_0483_2026_2027.pdf` y `2024_2025`), el examen real de consola Linux de 3.ª EV con solucionario, el banco depurado de preguntas Moodle para 1.º DAM (`questions.xml` sin legado SMR1 CRT/polímetros, acompañado de sus láminas mudas) y la auditoría de enlaces Drive `404`.

---

## [2026-11-15] Compilación completa del bloque RA7 (6 conceptos, 5 SVGs, 5 ejercicios `e31`–`e35`, práctica `p07` y banco de evaluación privado)

- **Fuentes procesadas en `raw/procesados/`:** 3 síntesis técnicas de RA7 (clasificación de software y licencias en entornos productivos; ofimática, Markdown, Pandoc y flujo *docs-as-code* con Git; correo electrónico seguro SPF/DKIM/DMARC, transferencia de ficheros SFTP/`rsync` y utilidades de propósito general).
- **Diagramas SVG propios (5 archivos validados en XML):** taxonomía de software y licencias, pipeline *docs-as-code* con Markdown y Git, arquitectura de correo SMTP/IMAP y seguridad DNS, protocolos de transferencia segura (SFTP/SCP/`rsync`), y ecosistema de utilidades, compresión, antimalware y recuperación.
- **Conceptos teóricos (6 páginas en `wiki/conceptos/`):** cobertura íntegra de `RA7.a`–`RA7.g`.
- **Ejercicios resueltos (`e31`–`e35`, ≤ 6 GB RAM en host de 16 GB):** auditoría de licencias y selección de stack (`e31`), documentación técnica Markdown/Pandoc/Git (`e32`), cliente de correo y verificación SPF/DKIM/DMARC (`e33`), transferencia segura SFTP/`rsync`/SHA-256 (`e34`) y utilidades de compresión, ClamAV y mantenimiento (`e35`).
- **Práctica integradora `p07` (`DAM-Doc-Ubuntu` 2 GB + `DAM-Oficina-Win10` 4 GB = 6 GB):** enunciado público (`publicar: true`) y solución privada (`publicar: false`).
- **Evaluación privada (`privado_evaluacion/`):** examen teórico-práctico RA7 (14 preguntas tipo test + banco GIFT + 3 casos de laboratorio), solucionario docente y rúbrica analítica `RA7.a`–`RA7.g`.

---

## [2026-11-15] Compilación completa del bloque RA6 (6 conceptos, 5 SVGs, 5 ejercicios `e26`–`e30`, práctica `p06` y banco de evaluación privado)

- **Fuentes procesadas (`raw/procesados/`):** `ra6-recursos-compartidos-permisos-red-servidores.md`, `ra6-acceso-remoto-cortafuegos-seguridad-red.md`, `ra6-dominios-active-directory-ldap-integracion.md`.
- **Conceptos publicados (`wiki/conceptos/`):** 6 páginas completas cubriendo `RA6.a`–`RA6.g` con tabs duales MAX/Ubuntu y Windows 10/11, más 5 diagramas SVG locales (`wiki/assets/ra6-*.svg`).
- **Ejercicios resueltos (`wiki/ejercicios/`):** `e26`–`e30` con presupuesto de RAM entre 4 GB y 6 GB sobre hosts MAX de 16 GB.
- **Práctica Integradora (`wiki/practicas/`):** Enunciado público `p06` (`DAM-Corp-Srv` 2 GB + `DAM-Corp-Win10` 4 GB = 6 GB) y solución docente marcada con `publicar: false`.
- **Evaluación privada (`privado_evaluacion/`):** Examen teórico-práctico RA6 (14 preguntas + bloque Moodle GIFT + 3 supuestos), solucionario y rúbrica `RA6.a`–`RA6.g` (excluido de Git vía `.gitignore`).

---

## [2026-11-15] Compilación completa del bloque RA5 (6 conceptos, 5 SVGs, 5 ejercicios `e21`–`e25`, práctica `p05` y banco de evaluación privado)

- **Fuentes procesadas (`raw/procesados/`):** `ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md`, `ra5-lan-cableada-inalambrica-enrutamiento-wan.md`, `ra5-puertos-diagnostico-protocolos-seguros.md`.
- **Conceptos publicados (`wiki/conceptos/`):** 6 páginas completas cubriendo `RA5.a`–`RA5.h` con tabs duales MAX/Ubuntu y Windows 10/11, más 5 diagramas SVG locales (`wiki/assets/ra5-*.svg`).
- **Ejercicios resueltos (`wiki/ejercicios/`):** `e21`–`e25` con presupuesto de RAM entre 2 GB y 6 GB sobre hosts MAX de 16 GB.
- **Práctica Integradora (`wiki/practicas/`):** Enunciado público `p05` (`DAM-Router-Gate` 1 GB + `DAM-Net-Ubuntu` 2 GB + `DAM-Net-Win10` 4 GB = 7 GB) y solución docente marcada con `publicar: false`.
- **Evaluación privada (`privado_evaluacion/`):** Examen teórico-práctico RA5 (16 preguntas + bloque Moodle GIFT + 3 supuestos), solucionario y rúbrica `RA5.a`–`RA5.h` (excluido de Git vía `.gitignore`).

---

## [2026-11-15] Compilación completa del bloque RA4 (6 conceptos, 5 SVGs, 5 ejercicios `e16`–`e20`, práctica `p04` y banco de evaluación privado)

- **Fuentes procesadas (`raw/procesados/`):** `ra4-usuarios-grupos-directivas-seguridad.md`, `ra4-permisos-locales-acls-herencia.md`, `ra4-procesos-servicios-monitorizacion-desarrollo.md`.
- **Conceptos publicados (`wiki/conceptos/`):** 6 páginas completas cubriendo `RA4.a`–`RA4.h` con tabs duales MAX/Ubuntu y Windows 10/11, más 5 diagramas SVG locales (`wiki/assets/ra4-*.svg`).
- **Ejercicios resueltos (`wiki/ejercicios/`):** `e16`–`e20` con presupuesto de RAM $\le 6\text{ GB}$ sobre hosts MAX de 16 GB.
- **Práctica Integradora (`wiki/practicas/`):** Enunciado público `p04` (`DAM-Srv-Ubuntu` 2 GB + `DAM-Workstation-Win10` 4 GB = 6 GB) y solución docente marcada con `publicar: false`.
- **Evaluación privada (`privado_evaluacion/`):** Examen teórico-práctico RA4 (16 preguntas + bloque Moodle GIFT + 3 supuestos), solucionario y rúbrica `RA4.a`–`RA4.h` (excluido de Git vía `.gitignore`).

---

## [2026-11-15] Compilación completa del bloque RA3 (6 conceptos, 5 SVGs, 5 ejercicios `e11`–`e15`, práctica `p03` y banco de evaluación privado)

- **Fuentes procesadas (`raw/procesados/`):** `ra3-sistemas-archivos-directorios-busqueda.md`, `ra3-particiones-volumenes-lvm-raid-cifrado.md`, `ra3-copias-seguridad-automatizacion-tareas.md`.
- **Conceptos publicados (`wiki/conceptos/`):** 6 páginas completas cubriendo `RA3.a`–`RA3.h` con tabs duales MAX/Ubuntu y Windows 10/11, más 5 diagramas SVG locales (`wiki/assets/ra3-*.svg`).
- **Ejercicios resueltos (`wiki/ejercicios/`):** `e11`–`e15` con presupuesto de RAM $\le 6\text{ GB}$ sobre hosts MAX de 16 GB.
- **Práctica Integradora (`wiki/practicas/`):** Enunciado público `p03` (`DAM-Storage-Ubuntu` 2 GB + `DAM-Client-Win10` 4 GB = 6 GB) y solución docente marcada con `publicar: false`.
- **Evaluación privada (`privado_evaluacion/`):** Examen teórico-práctico RA3 (16 preguntas + bloque Moodle GIFT + 3 supuestos), solucionario y rúbrica `RA3.a`–`RA3.h` (excluido de Git vía `.gitignore`).

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
