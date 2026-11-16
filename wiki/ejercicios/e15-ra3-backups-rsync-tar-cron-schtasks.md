---
title: "e15 · Copias de Seguridad con rsync, tar y Robocopy más Automatización (cron y schtasks)"
ra: ["RA3"]
ce: ["RA3.f", "RA3.g", "RA3.h"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra3-copias-seguridad-automatizacion-tareas.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e15 · Copias de Seguridad con `rsync`, `tar` y `Robocopy` más Automatización (`cron` y `schtasks`)

<!-- fuente: raw/procesados/ra3-copias-seguridad-automatizacion-tareas.md -->

> **Criterios de Evaluación:** `RA3.f`, `RA3.g`, `RA3.h` · **Concepto previo:** [Copias de Seguridad, Clonación y Tareas Programadas](../conceptos/ra3-copias-seguridad-clonacion-tareas-programadas.md)

## Objetivo

Implementar una política de copias de seguridad incrementales/espejo y empaquetados comprimidos con verificación de restauración tanto en **GNU/Linux** (`tar`, `rsync`, `cron`) como en **Windows 10** (`robocopy /MIR`, `schtasks`), automatizando su ejecución periódica sin intervención manual.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e15-Ubuntu`** | Invitado 1 | Ubuntu 24.04 | **2048 MB (2 GB)** | 2 | 25 GB VDI · NAT |
| **`e15-Win10`** | Invitado 2 | Windows 10 | **4096 MB (4 GB)** | 2 | 40 GB VDI · NAT |

> **Consumo total de VMs activas:** **6 GB** simultáneos sobre 16 GB disponibles (cumple el tope de 10–12 GB).

---

## Enunciado

### Parte A — Respaldos y Cron en `e15-Ubuntu`
1. Crea un directorio de trabajo `~/app_dam/` con 3 archivos (`codigo.java`, `config.env`, `readme.md`).
2. Crea una **copia empaquetada y comprimida** con fecha en `~/backups/` usando `tar`, borra accidentalmente `config.env` en origen y **restáuralo únicamente** desde el `.tar.gz`.
3. Crea un espejo sincronizado hacia `/tmp/espejo_nas/` usando `rsync` (ejecuta primero una simulación en seco con `--dry-run`) y programa en **`crontab -e`** que esta sincronización se ejecute automáticamente **cada día a las 23:15**.
4. Verifica también un ejemplo con ejecución cada **2 minutos** temporalmente (`*/2 * * * *`) registrando la salida en un log `/tmp/backup_rsync.log`.

### Parte B — Robocopy y Programador de Tareas en `e15-Win10`
1. Crea `C:\DatosDAM` con varios archivos y realiza un espejo inicial a `C:\Backups\DatosDAM` usando **`robocopy /MIR`** con archivo de registro `/LOG`.
2. Crea una tarea programada diaria a las **23:15** llamada `BackupDiarioDAM` mediante **`schtasks`** (o PowerShell `Register-ScheduledTask`), lánzala bajo demanda para comprobar su ejecución y verifica el contenido de `log_robocopy.txt`.

---

??? success "Ver resolución paso a paso"

    ### Resolución Parte A: `tar`, `rsync` y `cron` en `e15-Ubuntu`

    ```bash
    # 1. Crear directorio origen de prueba y carpeta de respaldos
    mkdir -p ~/app_dam ~/backups /tmp/espejo_nas
    echo "public class Main {}" > ~/app_dam/codigo.java
    echo "DB_PORT=5432" > ~/app_dam/config.env
    echo "# Proyecto DAM" > ~/app_dam/readme.md

    # 2. Empaquetado comprimido con fecha + prueba de restauración selectiva
    tar -czvf ~/backups/app_dam_$(date +%F).tar.gz -C ~ app_dam
    rm ~/app_dam/config.env

    # Restaurar SOLO el fichero borrado sin sobreescribir el resto
    tar -xzvf ~/backups/app_dam_$(date +%F).tar.gz -C ~ app_dam/config.env
    cat ~/app_dam/config.env

    # 3. Sincronización con rsync (primero simulación --dry-run / -n)
    rsync -avhn --delete ~/app_dam/ /tmp/espejo_nas/
    # Ejecución real:
    rsync -avh --delete ~/app_dam/ /tmp/espejo_nas/

    # 4. Automatización en crontab (usa rutas absolutas y sin ~ en scripts complejos)
    # Ejecuta 'crontab -e' y añade las líneas siguientes:
    ```
    ```text
    # Copia diaria real a las 23:15
    15 23 * * * /usr/bin/rsync -avh --delete /home/alumdam/app_dam/ /tmp/espejo_nas/ >> /tmp/backup_rsync.log 2>&1

    # Prueba cada 2 minutos para validar en clase (comentar después de verificar):
    */2 * * * * /usr/bin/date >> /tmp/latido_cron.log
    ```
    ```bash
    # Verificar las tareas activas y esperar 2 minutos para revisar el log de prueba
    crontab -l
    cat /tmp/latido_cron.log
    ```

    ---

    ### Resolución Parte B: `robocopy` y `schtasks` en `e15-Win10`

    Abre **PowerShell como Administrador**:

    ```powershell
    # 1. Preparar directorios origen y destino
    New-Item -ItemType Directory -Force -Path "C:\DatosDAM", "C:\Backups\DatosDAM" | Out-Null
    "Proyecto Java 1DAM" | Out-File "C:\DatosDAM\proyecto.txt"
    "Clave local prueba" | Out-File "C:\DatosDAM\notas.md"

    # 2. Simulación de Robocopy (/L = List only) y copia espejo real (/MIR)
    robocopy "C:\DatosDAM" "C:\Backups\DatosDAM" /MIR /L
    robocopy "C:\DatosDAM" "C:\Backups\DatosDAM" /MIR /R:2 /W:5 /LOG:"C:\Backups\log_robocopy.txt"

    # 3. Crear tarea diaria con schtasks a las 23:15
    schtasks /create /tn "BackupDiarioDAM" `
      /tr "robocopy C:\DatosDAM C:\Backups\DatosDAM /MIR /LOG:C:\Backups\log_robocopy.txt" `
      /sc DAILY /st 23:15 /f

    # 4. Ejecutar inmediatamente bajo demanda para verificar que funciona sin errores
    schtasks /run /tn "BackupDiarioDAM"
    schtasks /query /tn "BackupDiarioDAM" /v /fo LIST | Select-String "Estado|Último resultado"
    Get-Content "C:\Backups\log_robocopy.txt" -Tail 15
    ```

    ### Parte C (Ampliación): Sincronización (`rclone`), Política 3-2-1 y Clonación Multicast

    1. **Sincronización en Linux y Windows:** configura dos tareas verificadas de sincronización de carpetas: una **local $\rightarrow$ local** y otra **local $\rightarrow$ nube**, utilizando **`rclone`** en Linux (`rclone sync /origen remoto:carpeta -P`) y **`FreeFileSync`** o **`Syncthing`** en Windows. Modifica un fichero en origen, vuelve a sincronizar y demuestra la propagación.
    2. **Clonación con Clonezilla:** arranca con la ISO de [Clonezilla Live](https://clonezilla.org/), guarda una imagen completa de una VM pequeña en un segundo disco virtual y restáurala en una VM destino limpia (y practica en red interna la restauración simultánea en 2 máquinas mediante modo **Multicast**).
    3. **Documento de Política 3-2-1:** redacta la política para tu estación DAM respondiendo a **qué datos** (*Sistema / Trabajos DAM / Otros*), **cómo** (*Completa + Incremental/Diferencial*), **cuándo**, **dónde** (*3-2-1*), **cifrado/etiquetado** y **prueba real de restauración**.
