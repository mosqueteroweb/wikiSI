---
title: "e09 · Gestión Profesional de Aplicaciones: apt, dpkg, Snap y winget"
ra: ["RA2"]
ce: ["RA2.h"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e09 · Gestión Profesional de Aplicaciones: `apt`, `dpkg`, Snap y `winget`

<!-- fuente: raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md -->

> **Criterio de Evaluación:** `RA2.h` · **Concepto previo:** [Gestión de Aplicaciones, Actualización y Recuperación](../conceptos/ra2-gestion-aplicaciones-actualizacion-recuperacion.md)

## Objetivo

Dominar el ciclo completo de vida del software (búsqueda, inspección, instalación desde repositorio y paquete local, actualización y desinstalación limpia con limpieza de dependencias) tanto en **GNU/Linux (Ubuntu/MAX)** usando `apt`/`dpkg`/`snap`, como en **Windows 10/11** usando **`winget`**, además de saber exportar un manifiesto reproducible de software.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e09-Ubuntu`** | Invitado 1 | Ubuntu Desktop 24.04 | **2048 MB (2 GB)** | 2 | 25 GB VDI · NAT |
| **`e09-Win10`** | Invitado 2 | Windows 10 | **4096 MB (4 GB)** | 2 | 40 GB VDI · NAT |

> **Consumo total de VMs activas:** **6 GB** simultáneos sobre 16 GB disponibles (cumple el margen de 10–12 GB en aula).

---

## Enunciado

### Parte A — GNU/Linux (`e09-Ubuntu` o terminal de práctica)
1. Actualiza la caché de repositorios e inspecciona sin instalar todavía los paquetes `nginx` y `htop` (`apt show`).
2. Instala **`htop`** y **`ncdu`** en una sola orden desde repositorio oficial.
3. Simula la descarga manual de un paquete `.deb` (p. ej. obteniendo el `.deb` de `neofetch` o `fastfetch` con `apt download` o `wget`), **instálalo con `dpkg -i`** y analiza si requiere resolver dependencias con `apt install -f`.
4. Comprueba la diferencia práctica eliminando un paquete de servidor con **`apt remove`** vs **`apt purge`**: instala `nginx`, verifica que existe `/etc/nginx/nginx.conf`, desinstálalo primero con `remove` (comprobando si `/etc/nginx/` sobrevive) y luego ejecuta `purge` + `autoremove`.
5. Exporta el inventario de paquetes instalados a `inventario_ubuntu.txt`.

### Parte B — Windows 10 (`e09-Win10`)
1. Abre **PowerShell** y busca con **`winget`** el identificador exacto de **7-Zip** y **Notepad++**.
2. Instala ambos programas de forma desatendida aceptando los acuerdos de licencia por parámetro.
3. Consulta qué aplicaciones instaladas en la VM tienen actualizaciones pendientes (`winget upgrade`).
4. Desinstala **Notepad++** limpiamente usando su `--id` exacto y exporta un fichero JSON con la lista de aplicaciones restantes (`winget export`).

---

??? success "Ver resolución paso a paso"

    ### Resolución Parte A: GNU/Linux (`e09-Ubuntu`)

    ```bash
    # 1. Actualizar índices e inspeccionar paquetes antes de instalar
    sudo apt update
    apt show htop
    apt show nginx | grep -E "Package|Version|Installed-Size|Depends"

    # 2. Instalar htop y ncdu desde repositorios oficiales
    sudo apt install -y htop ncdu
    which htop ncdu

    # 3. Descarga manual de un .deb e instalación directa con dpkg (nivel bajo)
    mkdir -p /tmp/paquetes && cd /tmp/paquetes
    apt download tree
    ls -l tree_*.deb

    # Instalar manualmente el .deb con dpkg
    sudo dpkg -i tree_*.deb
    # Si faltara alguna librería dependiente en un paquete complejo, se repara con:
    sudo apt install -f -y

    # 4. Diferencia práctica entre remove y purge
    sudo apt install -y nginx
    ls -ld /etc/nginx            # Existe la carpeta de configuración

    sudo apt remove -y nginx
    ls -ld /etc/nginx            # ¡Sigue existiendo! remove conserva /etc/nginx

    sudo apt purge -y nginx
    ls -ld /etc/nginx            # Desaparece por completo (No such file or directory)
    sudo apt autoremove -y       # Elimina librerías auxiliares de nginx que ya nadie usa

    # 5. Exportar inventario reproducible de paquetes
    dpkg --get-selections > ~/inventario_ubuntu.txt
    head -n 10 ~/inventario_ubuntu.txt
    ```

    *(Nota: Si en tu entorno también usas `snap`, puedes comprobar qué aplicaciones aisladas hay activas con `snap list` y actualizarlas con `sudo snap refresh`.)*

    ---

    ### Resolución Parte B: Windows 10 (`e09-Win10`)

    Abre **PowerShell** en `e09-Win10`:

    ```powershell
    # 1. Buscar identificadores exactos en los repositorios de winget
    winget search "7zip"
    winget search "Notepad++"

    # 2. Instalación desatendida usando el ID exacto (-e evita ambigüedades)
    winget install --id 7zip.7zip -e --accept-source-agreements --accept-package-agreements
    winget install --id Notepad++.Notepad++ -e --accept-source-agreements --accept-package-agreements

    # 3. Auditar versiones instaladas y actualizaciones disponibles
    winget list --id 7zip.7zip
    winget upgrade

    # (Opcional: actualizar todo el software compatible)
    # winget upgrade --all --accept-source-agreements --accept-package-agreements

    # 4. Desinstalar Notepad++ limpiamente y exportar catálogo JSON reproducible
    winget uninstall --id Notepad++.Notepad++ -e
    winget export -o "$env:USERPROFILE\Desktop\apps_win10.json"

    # Ver contenido inicial del manifiesto exportado
    Get-Content "$env:USERPROFILE\Desktop\apps_win10.json" -TotalCount 20
    ```

    Con `apps_win10.json` y `inventario_ubuntu.txt` podrías clonar el mismo parque de software en cualquier otro equipo de clase mediante `winget import -i apps_win10.json`.
