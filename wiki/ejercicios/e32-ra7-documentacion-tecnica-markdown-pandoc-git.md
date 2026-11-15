---
ra: RA7
ce:
  - RA7.c
  - RA7.f
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra7-ofimatica-colaboracion-documentacion-markdown.md
ultima_revision: "2026-11-15"
---

# e32 · Documentación Técnica *Docs-as-Code*: Markdown, `pandoc`, Estilos ODF y Control en Git

<!-- fuente: raw/procesados/ra7-ofimatica-colaboracion-documentacion-markdown.md -->

## Escenario y Topología VirtualBox

Debemos redactar el manual de puesta en marcha de una aplicación de clase en **Markdown** con diagramas y tablas, contrastar comandos directamente en páginas `man` / `tldr`, generar automáticamente salidas corporativas en **OpenDocument (`.odt`)** y **PDF**, y versionar todo en **Git**.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e32-Ubuntu-Doc`** | Ubuntu Desktop / Server 24.04 | **2 GB** | Edición Markdown, `pandoc`, LibreOffice *headless*, `man`/`tldr` y Git |
| **Total activo** | **1 VM ligera** | **2 GB** | Holgado margen libre sobre anfitrión **MAX (16 GB)** |

## Objetivos

1. Consultar documentación primaria con `man` y `--help` verificando flags exactos sin depender de blogs desactualizados (`RA7.f`).
2. Escribir un documento estructurado en **Markdown GFM** con tabla comparativa, bloque de código y metadatos YAML.
3. Convertir automáticamente a `.odt`, `.html` y `.pdf` mediante **`pandoc`** + LibreOffice CLI (`soffice --headless`) y registrar el historial en **Git** (`RA7.c`).

---

## Enunciado Detallado

1. **Verificación de fuentes primarias (`RA7.f`):**
   - Consulta en consola las opciones oficiales de `tar` (`man tar` / `tar --help`) y `rsync` (`man rsync`) comprobando qué hace exactamente el flag `-a` (*archive*) y el flag `--numeric-ids`.
2. **Pipeline *Docs-as-Code* (`RA7.c`):**
   - En **`e32-Ubuntu-Doc`**, crea un repositorio local `~/doc_dam_proyecto` inicializado con `git init`.
   - Redacta un fichero `manual_despliegue.md` que contenga: encabezados `#`/`##`, tabla de requisitos hardware, bloque de código Bash con comandos verificados en el paso 1 y lista de comprobación de entrega.
   - Instala `pandoc` y genera un documento `.odt` (con `--toc` tabla de contenido automática) y un HTML autocontenido; conviértelo a PDF sin entorno gráfico usando `libreoffice --headless --convert-to pdf` (si está LibreOffice Writer instalado).
   - Realiza un commit en Git y comprueba la limpieza de *diffs* realizando una pequeña corrección y ejecutando `git diff`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Contraste en documentación primaria (`man` / `--help`) y creación del repositorio

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Consultar documentación oficial integrada antes de redactar manuales
        man rsync | grep -A 5 -- "-a, --archive"
        tar --help | grep -E -- "--create|--gzip|--extract"

        # Instalar git, pandoc y LibreOffice Writer (o solo pandoc si ya está LibreOffice en MAX)
        sudo apt-get update && sudo apt-get install -y git pandoc libreoffice-writer

        mkdir -p ~/doc_dam_proyecto && cd ~/doc_dam_proyecto
        git init
        git config user.name "Alumno DAM"
        git config user.email "alumno@dam.local"
        ```

    === "Windows 10 / 11"

        ```powershell
        # Consultar ayuda oficial nativa en PowerShell y preparar carpeta Git
        Get-Help Compress-Archive -Full | Select-Object -First 25
        winget install --id JohnMacFarlane.Pandoc -e --accept-package-agreements --accept-source-agreements
        mkdir C:\Proyectos\doc_dam_proyecto; cd C:\Proyectos\doc_dam_proyecto; git init
        ```

    ### 2. Redacción Markdown, conversión automática y versionado Git (`RA7.c`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        cat <<'EOF' > manual_despliegue.md
        ---
        title: "Manual de Despliegue · Proyecto Aurora DAM"
        author: "Equipo Sistemas 1.º DAM"
        ---

        # Guía de Despliegue Rápido

        ## 1. Requisitos Mínimos de Sistema

        | Recurso | Mínimo Pruebas | Recomendado Producción |
        | :--- | :---: | :---: |
        | CPU | 2 vCPU | 4 vCPU |
        | RAM | 2 GB | 4 GB |

        ## 2. Sincronización de Copias Verificada

        ```bash
        rsync -avz --delete /var/www/app/ backup@192.168.50.10:/srv/backups/app/
        ```
        EOF

        # Convertir Markdown en ODT (con estilos nativos e índice automático) y HTML
        pandoc manual_despliegue.md -o manual_despliegue.odt --toc
        pandoc manual_despliegue.md -o manual_despliegue.html --standalone --toc

        # Generar PDF corporativo desde el ODT sin abrir ventana gráfica
        soffice --headless --convert-to pdf manual_despliegue.odt

        # Versionar únicamente el fuente Markdown en Git (manteniendo binarios generados en .gitignore)
        printf "*.pdf\n*.odt\n*.html\n" > .gitignore
        git add .gitignore manual_despliegue.md
        git commit -m "docs: initial deployment manual in Markdown"
        ```

    === "Windows 10 / 11"

        ```powershell
        # Convertir el mismo Markdown desde PowerShell hacia Word (.docx) o OpenDocument (.odt)
        pandoc .\manual_despliegue.md -o .\manual_despliegue.docx --toc
        pandoc .\manual_despliegue.md -o .\manual_despliegue.odt --toc
        ```

---

## Puntos de Control y Errores Frecuentes

- **Subir documentos binarios compilados al repositorio Git:** Los `.pdf` o `.docx` generados automáticamente cambian de bytes en cada compilación y engordan innecesariamente el repositorio; mantén en Git la fuente `.md` y añádelos al `.gitignore` (o publícalos como *Release Artifacts*).
- **Formato manual en LibreOffice:** Al abrir `manual_despliegue.odt` generado con `pandoc`, comprobarás que usa automáticamente los **Estilos oficiales (`Heading 1`, `Heading 2`)** y crea un índice clicable, evitando aplicar negritas manuales.

## Recursos para Profundizar

- Concepto asociado: [Documentación con Ofimática, Markdown y Trabajo Colaborativo](../conceptos/ra7-documentacion-ofimatica-markdown-trabajo-colaborativo.md) y [Búsqueda de Documentación Técnica](../conceptos/ra7-busqueda-documentacion-tecnica-utilidades-sistema.md).
- Vídeo recomendado sobre Markdown y documentación técnica: [Markdown y documentación técnica profesional (YouTube)](https://www.youtube.com/watch?v=eaKFOC8lfjU).
- Vídeo recomendado sobre LibreOffice y productividad: [LibreOffice y herramientas colaborativas (YouTube)](https://www.youtube.com/watch?v=GArVeJj8MHo).
