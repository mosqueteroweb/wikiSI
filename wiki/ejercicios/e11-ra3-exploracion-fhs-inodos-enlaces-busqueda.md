---
title: "e11 · Exploración FHS, Inodos, Enlaces y Búsqueda Avanzada"
ra: ["RA3"]
ce: ["RA3.a", "RA3.b", "RA3.c", "RA3.d"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra3-sistemas-archivos-directorios-busqueda.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e11 · Exploración FHS, Inodos, Enlaces y Búsqueda Avanzada

<!-- fuente: raw/procesados/ra3-sistemas-archivos-directorios-busqueda.md -->

> **Criterios de Evaluación:** `RA3.a`, `RA3.b`, `RA3.c`, `RA3.d` · **Conceptos previos:** [Sistemas de Archivos](../conceptos/ra3-sistemas-archivos-anatomia-comparativa.md) · [Estructura de Directorios](../conceptos/ra3-estructura-directorios-fhs-windows.md) · [Búsqueda e Inventario](../conceptos/ra3-busqueda-localizacion-informacion.md)

## Objetivo

Inspeccionar el sistema de archivos raíz (`ext4` y sus inodos) y la jerarquía estándar **FHS** en Ubuntu/MAX frente a la estructura de carpetas en Windows 10, diferenciar en práctica enlaces duros (*hard links*) de simbólicos (*symlinks*), y localizar ficheros y textos mediante consola (`find`, `grep`, `Get-ChildItem`, `Select-String`).

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e11-Ubuntu`** | Invitado 1 | Ubuntu Desktop 24.04 | **2048 MB (2 GB)** | 2 | 25 GB VDI · NAT |
| **`e11-Win10`** | Invitado 2 | Windows 10 | **4096 MB (4 GB)** | 2 | 40 GB VDI · NAT |

> **Consumo total de VMs activas:** **6 GB** simultáneos sobre 16 GB disponibles (cumple el límite de 10–12 GB).

---

## Enunciado

### Parte A — Ubuntu (`e11-Ubuntu`)
1. Comprueba el sistema de archivos de `/` con `df -Th` y lista las carpetas de primer nivel en `/` (`ls -l /`) explicando la función de `/etc`, `/var`, `/home`, `/boot` y `/tmp`.
2. En `~/lab_ra3/`, crea `fuente.txt` con una frase dentro, crea un enlace duro (`duro.txt`) y un enlace simbólico (`simbolico.txt`), comprueba sus números de inodo (`ls -li`), borra `fuente.txt` y describe qué ocurre al hacer `cat` sobre `duro.txt` y sobre `simbolico.txt`.
3. Mediante `find` y `grep`, busca dentro de `/etc` todos los archivos `.conf` modificados en los últimos 30 días o que contengan la palabra `localhost` (suprimiendo errores de permiso).

### Parte B — Windows 10 (`e11-Win10`)
1. Usando **PowerShell**, muestra el tamaño en GB y el sistema de archivos de la unidad `C:` (`Get-Volume`).
2. Busca en `C:\Windows\System32\drivers\etc\` cualquier archivo que contenga la cadena `localhost` usando `Select-String` y localiza el binario `notepad.exe` con `where.exe`.
3. Inventaría en ambos sistemas los paquetes/aplicaciones relacionadas con compresión o administración instalados (`dpkg -l` / `winget list`).

---

??? success "Ver resolución paso a paso"

    ### Resolución Parte A: GNU/Linux (`e11-Ubuntu`)

    ```bash
    # 1. Sistema de archivos montado en raíz y primer nivel FHS
    df -Th /
    ls -l /
    # /etc: configuración global; /var: logs y datos variables; /home: perfiles usuario;
    # /boot: kernel/GRUB/ESP; /tmp: archivos temporales compartidos con Sticky Bit.

    # 2. Experimentación con inodos y enlaces duros vs simbólicos
    mkdir -p ~/lab_ra3 && cd ~/lab_ra3
    echo "Datos importantes de Sistemas Informaticos" > fuente.txt
    ln fuente.txt duro.txt
    ln -s fuente.txt simbolico.txt

    ls -li
    # Observa: 'fuente.txt' y 'duro.txt' tienen EXACTO el mismo número de inodo (link count = 2);
    # 'simbolico.txt' tiene otro inodo propio que apunta por nombre a 'fuente.txt'.

    rm fuente.txt
    cat duro.txt       # ¡FUNCIONA! El inodo sigue vivo con contador = 1
    cat simbolico.txt  # Error: No such file or directory (enlace simbólico roto)

    # 3. Búsqueda de archivos y contenido en /etc
    find /etc -type f -name "*.conf" -mtime -30 2>/dev/null | head -n 10
    grep -rn "localhost" /etc/hosts /etc/*.conf 2>/dev/null

    # Inventario de paquetes relacionados con archivadores
    dpkg -l | grep -E "tar|gzip|zip|rsync"
    ```

    ---

    ### Resolución Parte B: Windows 10 (`e11-Win10`)

    Abre **PowerShell**:

    ```powershell
    # 1. Consultar sistema de archivos y capacidad en C:
    Get-Volume | Format-Table DriveLetter, FileSystem, FileSystemLabel, @{N="FreeGB";E={[math]::Round($_.SizeRemaining/1GB,2)}}

    # 2. Localizar texto en archivos de red de sistema y ruta del ejecutable
    Select-String -Path "C:\Windows\System32\drivers\etc\*" -Pattern "localhost" -ErrorAction SilentlyContinue
    where.exe notepad

    # 3. Búsqueda recursiva por tamaño en el perfil de usuario
    Get-ChildItem -Path $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue |
      Sort-Object Length -Descending |
      Select-Object Name, Length -First 5

    # Inventario rápido de software instalado
    winget list | Select-Object -First 15
    ```
