---
ra: RA7
ce:
  - RA7.a
  - RA7.b
  - RA7.c
  - RA7.d
  - RA7.e
  - RA7.f
  - RA7.g
tipo: practica
publicar: true
fuentes:
  - raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md
  - raw/procesados/ra7-ofimatica-colaboracion-documentacion-markdown.md
  - raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md
ultima_revision: "2026-11-15"
---

# p07 · Auditoría de Licencias, Documentación *Docs-as-Code*, Correo, SFTP y Utilidades (`RA7.a`–`RA7.g`)

<!-- fuente: raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md -->

## Situación Profesional de Partida

El estudio **PixelForge DAM** (20 desarrolladores y personal administrativo) quiere estandarizar su entorno documental y de intercambio de entregables evitando costes innecesarios de licencias propietarias, eliminando el uso de FTP en claro y automatizando su documentación técnica. Te asignan diseñar el dossier y demostrar todo el flujo técnico sobre **VirtualBox en MAX (16 GB RAM)**.

## Topología VirtualBox y Presupuesto de RAM

| Máquina Virtual | Sistema Operativo | RAM asignada | Red VirtualBox | Función |
| :--- | :--- | :---: | :--- | :--- |
| **`DAM-Doc-Ubuntu`** | Ubuntu Desktop / Server 24.04 | **2 GB** | `intnet_oficina` (`192.168.90.10/24`) + NAT (`apt`) | Documentación `pandoc`/Git, SSH/SFTP/`rsync`, `ClamAV`, `7z` |
| **`DAM-Oficina-Win10`** | Windows 10 Education / Pro | **4 GB** | `intnet_oficina` (`192.168.90.20/24`) | Inventario `winget`, envío `scp`/`Get-FileHash`, consultas DNS correo |
| **Consumo total activo** | **2 VMs sobre MAX (16 GB)** | **6 GB** | Margen libre **10 GB** | Respeta el tope de aula (≤ 10–12 GB) |

---

## Tareas Evaluables (`RA7.a` – `RA7.g`)

### Tarea 1 · Clasificación de Licencias y Auditoría de Dependencias (`RA7.a`)

1. En **`DAM-Doc-Ubuntu`**, inspecciona las licencias oficiales en `/usr/share/doc/*/copyright` de 3 herramientas (ej. `git`, `bash`, `openjdk` o `python3`) y audita con `pip-licenses` en un entorno virtual `python3 -m venv` qué licencias usan librerías como `mkdocs` o `requests`.
2. Elabora una tabla clasificando al menos 6 programas (cubriendo **GPLv3**, **AGPLv3**, **MIT/Apache 2.0**, **Propietario SaaS**, **Freeware** y **Shareware**) indicando si permiten integrarse dentro de un producto comercial de código cerrado sin abrir las fuentes.

### Tarea 2 · Evaluación de Necesidades Productivas (`RA7.b`)

Redacta un **Cuadro Comparativo de Implantación para PixelForge DAM (20 puestos)**:
- Compara **LibreOffice Still + Nextcloud/Collabora** frente a **Microsoft 365** o **Google Workspace**, evaluando **TCO a 3 años**, dependencia del proveedor (*vendor lock-in*), estándares abiertos (**ODF**, **PDF/A**) y requisitos legales **RGPD/ENS**.

### Tarea 3 · Pipeline Documental Markdown + Git + Pandoc (`RA7.c`, `RA7.f`)

1. Consulta con `man rsync` y `7z --help` (fuentes primarias `RA7.f`) los parámetros exactos de sincronización diferencial y cifrado de cabeceras antes de redactar el manual.
2. Crea en **`DAM-Doc-Ubuntu`** un repositorio Git `~/manual_pixelforge` con `README.md` estructurado (encabezados `#`/`##`, tabla comparativa de formatos, bloque de código Bash).
3. Compila con **`pandoc`** una versión `.odt` con índice automático (`--toc`) y expórtala a **PDF/A o PDF estándar** mediante LibreOffice *headless* (`soffice --headless --convert-to pdf`). Excluye los binarios generados mediante `.gitignore` y realiza dos commits con historial limpio.

### Tarea 4 · Auditoría Técnica de Correo Seguro (`RA7.d`)

1. Desde consola Linux (`dig`) o Windows (`Resolve-DnsName`), verifica los registros **MX**, **SPF (`v=spf1`)** y **DMARC (`_dmarc`)** de un dominio técnico de referencia (p. ej. `github.com` o `debian.org`).
2. Comprueba con `openssl s_client -connect imap.gmail.com:993` el soporte **TLS 1.3/1.2** y especifica en tu memoria los puertos exactos y opciones de seguridad que configurarías en **Mozilla Thunderbird** (IMAP seguro, SMTP Submission y cifrado extremo a extremo OpenPGP).

### Tarea 5 · Transferencia Segura (`SFTP`, `rsync`) e Integridad (`SHA-256`) (`RA7.e`)

1. En **`DAM-Oficina-Win10`**, crea una carpeta con los documentos de entrega `Entrega_PixelForge`, comprímela, calcula su huella **`Get-FileHash -Algorithm SHA256`** y transfiérela a **`DAM-Doc-Ubuntu`** mediante **`scp` o `sftp`** (`22/TCP`).
2. En **`DAM-Doc-Ubuntu`**, verifica con `sha256sum` la integridad exacta bit a bit respecto a Windows, y sincroniza de forma diferencial hacia otra carpeta espejo de backup con `rsync -avz --stats`.

### Tarea 6 · Empaquetado Cifrado (`7z`) y Revisión Antimalware (`ClamAV`/Defender) (`RA7.g`)

1. Comprime la entrega final en **`DAM-Doc-Ubuntu`** con `7z a -p -mhe=on entrega_sellada.7z ...` demostrando que sin la contraseña no es posible listar ni siquiera los nombres internos de archivo.
2. Instala **ClamAV**, actualiza firmas (`freshclam`) y analiza tanto la carpeta recibida como la firma inofensiva de prueba **`EICAR`**, verificando también `Get-MpComputerStatus` en Windows 10.

---

## Entregables y Criterios de Evaluación

Entrega un único dosier técnico (`Apellido_Nombre_p07_RA7.pdf` o `.md`) acompañado del `.odt` y `.pdf` generados automáticamente con `pandoc`, junto a las capturas verificadas de todas las tareas.

| Bloque evaluado | Criterios cubiertos | Peso |
| :--- | :---: | :---: |
| Clasificación jurídica de licencias y auditoría técnica | `RA7.a` | **15 %** |
| Análisis comparativo de software en entorno productivo | `RA7.b` | **15 %** |
| Pipeline Markdown + Git + Pandoc + LibreOffice y fuentes primarias | `RA7.c`, `RA7.f` | **25 %** |
| Auditoría de correo seguro (SMTP/IMAP + SPF/DKIM/DMARC + TLS) | `RA7.d` | **15 %** |
| Transferencia cifrada `SFTP`/`rsync` y verificación `SHA-256` | `RA7.e` | **15 %** |
| Empaquetado AES-256 (`7z -mhe`) y verificación antimalware | `RA7.g` | **15 %** |

## Recursos de Apoyo

- [Conceptos del bloque RA7](../ra/RA7.md#conceptos-teoricos)
- [Ejercicios resueltos e31–e35](../ra/RA7.md#ejercicios-practicos-resueltos)
- Vídeos de repaso: [Licencias de software](https://www.youtube.com/watch?v=p4pSjP0FqQQ) · [Markdown técnico](https://www.youtube.com/watch?v=eaKFOC8lfjU) · [LibreOffice y productividad](https://www.youtube.com/watch?v=GArVeJj8MHo) · [SFTP y correo seguro](https://www.youtube.com/watch?v=S-2TIRnsioM)
