---
ra: RA7
ce:
  - RA7.a
  - RA7.b
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md
ultima_revision: "2026-11-15"
---

# e31 · Auditoría de Licencias de Software e Informe de Selección Productiva

<!-- fuente: raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md -->

## Escenario y Topología VirtualBox

Una pequeña consultora de desarrollo y administración (15 empleados) nos pide revisar las licencias reales instaladas en sus equipos Linux y elaborar un dictamen comparativo para elegir su suite ofimática, nube documental y base de datos reduciendo costes y evitando dependencia tecnológica (*vendor lock-in*).

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e31-Ubuntu`** | Ubuntu Desktop / Server 24.04 | **2 GB** | Inspección de ficheros `/usr/share/doc/*/copyright` y auditoría de dependencias Python |
| **`e31-Puppy`** | Puppy Linux | **1 GB** | Comparativa de software ultraligero FOSS para equipos antiguos |
| **Total activo** | **2 VMs simultáneas** | **3 GB** | Consumo mínimo sobre equipo **MAX (16 GB)** |

## Objetivos

1. Identificar y clasificar por familia legal (*Copyleft fuerte/débil*, *Permisiva*, *Propietario EULA*, *Freeware*) software habitual en un entorno de aula y empresa.
2. Inspeccionar en consola Linux la licencia exacta declarada en paquetes instalados (`/usr/share/doc/*/copyright` y entorno Python).
3. Redactar una matriz de decisión técnica (`TCO`, formatos abiertos `ODF`/`PDF-A`, soberanía RGPD/ENS).

---

## Enunciado Detallado

1. **Inspección real de licencias en `e31-Ubuntu` (`RA7.a`):**
   - Consulta los ficheros de licencia de al menos tres paquetes instalados (`bash`, `nginx` o `python3`, `git`) dentro de `/usr/share/doc/<paquete>/copyright`.
   - Crea un entorno virtual Python temporal y verifica con `pip-licenses` (o consultando metadatos `pip show`) bajo qué licencia se distribuyen librerías comunes como `requests` o `mkdocs`.
   - Clasifica qué implicación tiene usar código **`GPLv3`** frente a **`MIT`** o **`Apache 2.0`** si la empresa vende una aplicación propietaria de código cerrado al cliente final.

2. **Comparativa de software para entorno productivo (`RA7.b`):**
   - Propón una pila completa justificada para 15 puestos administrativos y técnicos cubriendo: **Ofimática**, **Nube colaborativa**, **Gestor de contraseñas** y **Compresión**, justificando formatos abiertos frente a cerrados y coste de licenciamiento a 3 años.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Inspección de licencias en consola (`RA7.a`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Inspeccionar licencias oficiales empaquetadas por Debian/Ubuntu
        grep -iE "License:" /usr/share/doc/bash/copyright | head -n 5
        grep -iE "License:" /usr/share/doc/git/copyright | head -n 5
        head -n 30 /usr/share/doc/python3/copyright

        # Auditar dependencias Python dentro de un venv aislado (respetando PEP 668)
        sudo apt-get update && sudo apt-get install -y python3-venv
        python3 -m venv /tmp/venv_audit
        /tmp/venv_audit/bin/pip install --quiet requests pip-licenses
        /tmp/venv_audit/bin/pip-licenses --format=markdown
        rm -rf /tmp/venv_audit
        ```

    === "Windows 10 / 11"

        ```powershell
        # Inventariar aplicaciones instaladas y verificar modelo de licencia del sistema operativo
        winget list | Select-Object -First 15
        Get-CimInstance SoftwareLicensingProduct -Filter "Name like 'Windows%' and LicenseStatus = 1" |
          Select-Object Name, Description
        ```

    ### 2. Implicaciones legales y matriz de selección (`RA7.a`, `RA7.b`)

    - **GPLv3 vs MIT/Apache 2.0:** Si enlazas o modificas librerías **`GPLv3`** dentro de un producto distribuido comercialmente, la licencia obliga por *copyleft fuerte* a liberar el código fuente derivado completo bajo GPLv3. Por el contrario, **`MIT`**, **`BSD`** y **`Apache 2.0`** permiten redistribuir la aplicación compilada en código cerrado respetando los avisos de copyright originales.

    | Categoría | Software Seleccionado | Licencia | Ventaja clave para PYME (TCO 3 años) |
    | :--- | :--- | :--- | :--- |
    | **Ofimática** | **LibreOffice Still** | MPL-2.0 (FOSS) | `0 €` en licencias; estándar abierto **ODF** y exportación nativa **PDF/A** |
    | **Nube documental** | **Nextcloud + Collabora** | AGPLv3 (FOSS) | Alojado en servidor propio cumpliendo **RGPD/ENS** sin cuotas por usuario SaaS |
    | **Credenciales** | **KeePassXC** | GPLv3 (FOSS) | Bóveda cifrada local `.kdbx` multiplataforma sin nube propietaria |
    | **Compresión** | **7-Zip / tar+zstd** | LGPL / FOSS | Alta compresión y cifrado AES-256 sin avisos comerciales (`Shareware`) |

---

## Puntos de Control y Errores Frecuentes

- **Confundir "gratuito" con "libre" (*Freeware* vs *FOSS*):** Herramientas gratuitas cerradas a menudo prohíben uso comercial en empresas en su contrato EULA o carecen de código fuente auditable.
- **Olvidar el `copyleft` en red (`AGPLv3`):** A diferencia de `GPL` clásica, `AGPLv3` obliga a ofrecer el código modificado incluso cuando el software únicamente se presta como servicio web (SaaS) sin entregar instaladores al usuario.

## Recursos para Profundizar

- Concepto asociado: [Clasificación del Software por Licencias](../conceptos/ra7-clasificacion-software-licencias-modelos-distribucion.md) y [Análisis de Necesidades en Entornos Productivos](../conceptos/ra7-analisis-necesidades-software-entornos-productivos.md).
- Vídeo recomendado sobre licencias de software: [Licencias de software libre, copyleft y propietario (YouTube)](https://www.youtube.com/watch?v=p4pSjP0FqQQ).
