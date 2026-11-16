---
title: "e13 · Volúmenes Lógicos LVM y Matrices RAID 1 por Software (mdadm)"
ra: ["RA3"]
ce: ["RA3.e", "RA3.h"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e13 · Volúmenes Lógicos `LVM` y Matrices `RAID 1` por Software (`mdadm`)

<!-- fuente: raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md -->

> **Criterios de Evaluación:** `RA3.e`, `RA3.h` · **Concepto previo:** [Administración de Discos, Particiones, LVM y RAID](../conceptos/ra3-particiones-lvm-raid-administracion-discos.md)

## Objetivo

Construir una infraestructura de almacenamiento flexible en GNU/Linux combinando discos virtuales VDI en **Volúmenes Lógicos (`LVM`)** con ampliación dinámica en caliente sin pérdida de datos, y crear una matriz tolerante a fallos **RAID 1 (Espejo)** con `mdadm` simulando la caída y sustitución de un disco.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Discos VDI / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(14 GB libres)* | Físicas | Red del aula |
| **`e13-Ubuntu-Storage`** | Servidor almacenamiento | Ubuntu 24.04 | **2048 MB (2 GB)** | 2 | 25 GB SO + **4 discos VDI de 4 GB** (`/dev/sd[b-e]`) |

> **Consumo total de VMs activas:** **2 GB** sobre 16 GB disponibles (cumple holgadamente el límite de 10–12 GB).

---

## Enunciado

### Parte A — Almacenamiento Elástico con LVM (`/dev/sdb` y `/dev/sdc`)
1. Inicializa `/dev/sdb` y `/dev/sdc` (4 GB cada uno) como **Volúmenes Físicos (`PV`)**.
2. Únelos en un único **Grupo de Volúmenes (`VG`)** llamado `vg_dam` (~8 GB totales).
3. Crea dentro un **Volumen Lógico (`LV`)** llamado `lv_proyectos` de **3 GB**, formatéalo en `ext4`, móntalo en `/mnt/proyectos` y crea un fichero testigo `/mnt/proyectos/importante.txt`.
4. **Ampliación en caliente:** Sin desmontar `/mnt/proyectos`, amplía `lv_proyectos` en **+2 GB adicionales** (total 5 GB) redimensionando automáticamente el sistema de archivos `ext4`, y comprueba que `importante.txt` sigue intacto y `df -h` refleja los ~5 GB.

### Parte B — Matriz RAID 1 con `mdadm` (`/dev/sdd` y `/dev/sde`)
1. Crea un arreglo **RAID 1 (`/dev/md0`)** usando `/dev/sdd` y `/dev/sde` (4 GB cada uno), formatéalo en `ext4`, móntalo en `/mnt/espejo` y guarda un fichero de prueba.
2. Verifica su estado en `/proc/mdstat` y con `mdadm --detail /dev/md0` (debe mostrar `[2/2] [UU]`).
3. **Simulación de avería:** Marca `/dev/sdd` como fallido (`--fail`) y retíralo (`--remove`), comprobando que `/mnt/espejo` y tu fichero siguen totalmente accesibles en modo degradado `[UU -> U_]`.

---

??? success "Ver resolución paso a paso"

    ### Resolución Parte A: Creación y Extensión en Caliente LVM

    ```bash
    # 0. Instalar herramientas LVM y mdadm si no estuvieran presentes
    sudo apt update && sudo apt install -y lvm2 mdadm

    # Comprobar los 4 discos nuevos conectados en VirtualBox
    lsblk

    # 1. Crear Volúmenes Físicos (PV)
    sudo pvcreate /dev/sdb /dev/sdc
    sudo pvs

    # 2. Crear Grupo de Volúmenes (VG) llamado vg_dam
    sudo vgcreate vg_dam /dev/sdb /dev/sdc
    sudo vgs

    # 3. Crear Volumen Lógico (LV) de 3 GB, formatear y montar
    sudo lvcreate -L 3G -n lv_proyectos vg_dam
    sudo mkfs.ext4 -L ProyectosLVM /dev/vg_dam/lv_proyectos
    sudo mkdir -p /mnt/proyectos
    sudo mount /dev/vg_dam/lv_proyectos /mnt/proyectos

    echo "Archivo critico en LVM" | sudo tee /mnt/proyectos/importante.txt
    df -h /mnt/proyectos   # Mostrará ~2.9 GB

    # 4. Extender el LV +2 GB EN CALIENTE (-r ejecuta resize2fs automáticamente)
    sudo lvextend -L +2G -r /dev/vg_dam/lv_proyectos

    # Verificar el nuevo tamaño (~4.9 GB) y la integridad del fichero testigo
    df -h /mnt/proyectos
    cat /mnt/proyectos/importante.txt
    sudo lvs
    ```

    ---

    ### Resolución Parte B: RAID 1 Tolerante a Fallos con `mdadm`

    ```bash
    # 1. Crear RAID 1 sobre /dev/sdd y /dev/sde
    sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdd /dev/sde
    # (Confirmar 'y' si pregunta por metadatos superblock)

    # Esperar unos segundos a que sincronice y formatear / montar
    cat /proc/mdstat
    sudo mkfs.ext4 -L EspejoRAID1 /dev/md0
    sudo mkdir -p /mnt/espejo
    sudo mount /dev/md0 /mnt/espejo

    echo "Alta disponibilidad RAID 1" | sudo tee /mnt/espejo/datos_criticos.txt

    # 2. Inspeccionar estado sano [UU]
    sudo mdadm --detail /dev/md0 | grep -E "State|Active Devices|Failed Devices|/dev/sd"

    # 3. Simular fallo físico de /dev/sdd y comprobar supervivencia de los datos
    sudo mdadm --manage /dev/md0 --fail /dev/sdd
    sudo mdadm --manage /dev/md0 --remove /dev/sdd

    cat /proc/mdstat                 # Mostrará estado degradado [2/1] [_U]
    cat /mnt/espejo/datos_criticos.txt   # ¡Los datos siguen 100% disponibles!

    # (Para reintegrar un disco de reemplazo en el RAID: sudo mdadm --manage /dev/md0 --add /dev/sdd)
    ```

    ### Parte C (Ampliación): Batería completa RAID 0, RAID 1 y RAID 5 en Windows y Linux

    Si quieres ampliar el laboratorio con los tres niveles de referencia (`0`, `1` y `5`) en ambos sistemas operativos:

    1. **Linux (`mdadm` con 3 discos virtuales de prueba):**
       - `RAID 0`: `sudo mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/sdd /dev/sde`
       - `RAID 1`: `sudo mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/sdd /dev/sde`
       - `RAID 5`: `sudo mdadm --create /dev/md5 --level=5 --raid-devices=3 /dev/sdd /dev/sde /dev/sdf`
    2. **Windows 10/11 (*Espacios de almacenamiento*):** añade 3 discos sin formato en VirtualBox y crea sucesivamente un **Espacio simple** (`Simple` → RAID 0), un **Espacio de reflejo doble** (`Mirror` → RAID 1) y un **Espacio de paridad** (`Parity` → RAID 5), documentando el espacio útil resultante y desconectando un disco para observar la degradación y reconstrucción ([guía Espacios de almacenamiento en Windows](https://support.microsoft.com/es-es/windows/espacios-de-almacenamiento-en-windows-b6c8b540-b8d8-fb8a-e7ab-4a75ba11f9f2#WindowsVersion=Windows_10)).
