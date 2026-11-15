---
title: "Práctica p03 · Almacenamiento Elástico (LVM/RAID), Cifrado y Copias Automatizadas"
ra: ["RA3"]
ce: ["RA3.a", "RA3.b", "RA3.c", "RA3.d", "RA3.e", "RA3.f", "RA3.g", "RA3.h"]
tipo: "practica-enunciado"
publicar: true
fuentes:
  - "raw/procesados/ra3-sistemas-archivos-directorios-busqueda.md"
  - "raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md"
  - "raw/procesados/ra3-copias-seguridad-automatizacion-tareas.md"
ultima_revision: "2026-11-15"
---

# Práctica 03 · Almacenamiento Elástico (LVM/RAID), Cifrado y Copias Automatizadas

<!-- fuente: raw/procesados/ra3-sistemas-archivos-directorios-busqueda.md -->
<!-- fuente: raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md -->
<!-- fuente: raw/procesados/ra3-copias-seguridad-automatizacion-tareas.md -->

> **Criterios de Evaluación cubiertos:** `RA3.a`, `RA3.b`, `RA3.c`, `RA3.d`, `RA3.e`, `RA3.f`, `RA3.g`, `RA3.h` (100 % de **RA3**)

---

## Escenario Profesional

Un estudio de desarrollo de aplicaciones multiplataforma necesita diseñar la infraestructura de almacenamiento de sus nuevos servidores internos y estaciones de trabajo: particiones dedicadas para proyectos, capacidad ampliable sin cortes de servicio (**LVM**), protección frente a avería física de discos (**RAID 1**), contenedores cifrados para credenciales y código propietario (**LUKS2** / **BitLocker**), y un plan automatizado de copias de seguridad siguiendo la regla **3-2-1**.

Como técnico de **1º DAM**, desplegarás este laboratorio mixto en **Oracle VirtualBox sobre MAX** respetando el límite de memoria del aula y entregando la documentación de verificación.

---

## Presupuesto de Recursos VirtualBox (Obligatorio · Aula 16 GB)

| Equipo / VM | Rol en la práctica | Sistema Operativo | RAM asignada | vCPUs | Discos VDI / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Host Aula** | Anfitrión físico | **MAX (Linux)** | *(10 GB libres)* | Físicas | Disco físico aula |
| **`DAM-Storage-Ubuntu`** | Servidor almacenamiento Linux | **Ubuntu 24.04** | **2048 MB (2 GB)** | 2 | 25 GB SO + **3 discos VDI de 5 GB** (`sdb`, `sdc`, `sdd`) · NAT |
| **`DAM-Client-Win10`** | Estación cliente Windows | **Windows 10** | **4096 MB (4 GB)** | 2 | 40 GB SO + **1 disco VDI de 5 GB** (`E:`) · NAT |

> **Consumo total de VMs simultáneas:** **6 GB de 16 GB** disponibles en el host MAX (cumple el límite máximo de 10–12 GB).

---

## Apoyo Previo Recomendado

- [Conceptos de RA3](../ra/RA3.md#conceptos-teoricos)
- [e11 · Exploración FHS, Inodos y Búsqueda](../ejercicios/e11-ra3-exploracion-fhs-inodos-enlaces-busqueda.md)
- [e12 · Particionado GPT y `/etc/fstab`](../ejercicios/e12-ra3-particionado-montaje-fstab-diskpart.md)
- [e13 · Volúmenes Lógicos LVM y RAID 1](../ejercicios/e13-ra3-volumenes-logicos-lvm-raid-mdadm.md)
- [e14 · Chequeo SMART, `fsck`/`chkdsk` y Cifrado LUKS](../ejercicios/e14-ra3-chequeo-smart-cifrado-luks-bitlocker.md)
- [e15 · Copias `rsync`/`tar`/`robocopy` y `cron`/`schtasks`](../ejercicios/e15-ra3-backups-rsync-tar-cron-schtasks.md)

---

## Tareas a Realizar

### Tarea 1 · Sistemas de Archivos, Estructura de Directorios y Enlaces (`RA3.a`, `RA3.b`, `RA3.c`)
1. En **`DAM-Storage-Ubuntu`**, ejecuta `df -Th` y `stat /etc/fstab` explicando qué almacena el inodo del archivo frente a su nombre y qué ventajas aporta el *journaling* de `ext4` frente a `FAT32`.
2. Explica la función exacta de los directorios FHS `/etc`, `/var`, `/home`, `/boot`, `/mnt` y `/tmp`, comparando la estructura de árbol único de Linux frente a `C:\Windows`, `C:\ProgramData` y `C:\Users\...\AppData` en **`DAM-Client-Win10`**.
3. Crea en `~/lab_enlaces/` un archivo `manual.txt`, un **enlace duro** y un **enlace simbólico**, elimina `manual.txt` y documenta el resultado de leer ambos enlaces explicando por qué ocurre.

### Tarea 2 · Búsqueda de Información e Inventario de Software (`RA3.d`, `RA3.h`)
1. En **`DAM-Storage-Ubuntu`**, usa **`find`** para localizar ficheros mayores de `5 MiB` en `/usr` y usa **`grep -rn`** para localizar dónde aparece `UUID=` dentro de `/etc/fstab`.
2. En **`DAM-Client-Win10`**, usa **PowerShell** (`Get-ChildItem` y `Select-String`) para localizar todos los archivos `.log` en `C:\Windows\Logs` mayores de `100 KB`.
3. Genera e incluye los primeros 15 registros del software instalado en ambos nodos (`dpkg -l` y `winget list`).

### Tarea 3 · Almacenamiento Elástico con LVM y Cifrado LUKS2 (`RA3.e`, `RA3.h`)
Sobre los discos adicionales añadidos a **`DAM-Storage-Ubuntu`** (`5 GB` cada uno):
1. Con **`sdb` y `sdc`**, crea dos **PVs**, un **VG** llamado `vg_estudio` (~10 GB) y dos volúmenes lógicos:
   - `lv_proyectos` (**4 GB**, formateado en `ext4`, montado de forma **persistente en `/etc/fstab` por UUID** sobre `/srv/proyectos`).
   - `lv_backups` (**3 GB**, formateado en `ext4`, montado por UUID en `/mnt/backups_locales`).
2. Crea un fichero testigo en `/srv/proyectos/entregable.txt`, amplía `lv_proyectos` **en caliente** `+2 GB` (`lvextend -r`) hasta 6 GB y verifica que `df -h` refleja el incremento sin pérdida de datos.
3. Sobre **`sdd`**, inicializa tabla GPT con `parted`, crea `sdd1` (`5 GB`) y cífrala con **`cryptsetup luksFormat`**, ábrela como `cofre_estudio`, formatea en `ext4`, guarda `secretos.txt`, cierra el contenedor (`cryptsetup close`) y verifica con `blkid` que queda marcado como `crypto_LUKS`.

### Tarea 4 · Diagnóstico, Chequeo y Optimización de Unidades (`RA3.e`, `RA3.h`)
1. Desde el **Host MAX**, ejecuta `sudo smartctl -H` sobre el disco físico del equipo (si está instalado) e interpreta el resultado.
2. En **`DAM-Storage-Ubuntu`**, desmonta `/mnt/backups_locales`, pásale `sudo fsck -f` y vuelve a montarlo con `sudo mount -a`.
3. En **`DAM-Client-Win10`**, inicializa como GPT el disco extra de 5 GB asignándole letra `E:` en NTFS (`Get-Disk`/`Initialize-Disk`/`New-Partition`/`Format-Volume`), ejecuta `chkdsk E: /f` y `Get-PhysicalDisk`, y redacta en 3 líneas por qué **no** se debe desfragmentar un SSD sino ejecutar TRIM (`fstrim` / `Optimize-Volume -ReTrim`).

### Tarea 5 · Copias de Seguridad, Recuperación y Tareas Programadas (`RA3.f`, `RA3.g`)
1. En **`DAM-Storage-Ubuntu`**:
   - Simula un proyecto con varios archivos dentro de `/srv/proyectos/app1/`.
   - Programa una tarea **`cron`** (`crontab -e`) que cada día a las **22:00** ejecute `rsync -av --delete /srv/proyectos/ /mnt/backups_locales/` registrando un log en `/var/log/backup_estudio.log` (realiza una prueba manual o cada 2 minutos para demostrar que el log se genera).
   - Realiza un empaquetado de seguridad `tar -czvf` en `/tmp/`, borra un archivo de `/srv/proyectos/app1/` y demuestra su **restauración selectiva**.
2. En **`DAM-Client-Win10`**:
   - Configura una tarea diaria a las **22:00** con **`schtasks`** (o `Register-ScheduledTask`) llamada `BackupEstudioWin` que ejecute `robocopy C:\DatosEstudio E:\CopiaEstudio /MIR /LOG:E:\robocopy.log`, lánzala con `/run` y adjunta el contenido del log generado.
3. Describe brevemente cómo ampliarías esta práctica al modelo **3-2-1** real en una empresa (incluyendo copia externa *off-site*).

---

## Entregables en el Aula Virtual

Sube un único PDF **`Informe_RA3_ApellidoNombre.pdf`** que contenga ordenadamente:

1. Portada, tabla de VMs usadas (`2 GB + 4 GB = 6 GB`) y justificación del cumplimiento del presupuesto de RAM.
2. Evidencias (comandos ejecutados + salidas verificables de terminal) de las **Tareas 1 a 5**.
3. Comparativa del árbol `lsblk -f` final en Ubuntu y `Get-Volume` en Windows 10.
4. Captura o extracto del `/etc/fstab`, `crontab -l` y `schtasks /query`.

---

## Ponderación por Criterios de Evaluación

| Criterio | Peso en la práctica | Evidencia principal |
| :--- | :---: | :--- |
| **RA3.a** | 10 % | Anatomía e inodos `ext4`, `NTFS`, `exFAT` y `FAT32` (Tarea 1) |
| **RA3.b** | 10 % | Estructura de directorios FHS Linux vs jerarquía Windows + enlaces (Tarea 1) |
| **RA3.c** | 5 % | Identificación funcional de carpetas de sistema y rutas (Tarea 1) |
| **RA3.d** | 15 % | Búsquedas efectivas con `find`, `grep`, `Get-ChildItem` y `Select-String` (Tarea 2) |
| **RA3.e** | 20 % | Particionado GPT, `fstab` UUID, ampliación LVM en caliente, cifrado LUKS2 y `chkdsk` (Tareas 3 y 4) |
| **RA3.f** | 15 % | Copias con `rsync`, `tar`, `robocopy`, prueba de restauración y estrategia 3-2-1 (Tarea 5) |
| **RA3.g** | 15 % | Planificación automática verificada con `cron` y `schtasks` (Tarea 5) |
| **RA3.h** | 10 % | Inventarios de software y evaluación de SMART, TRIM vs defrag y utilidades (Tareas 2, 4 y 5) |
| **Total** | **100 %** | **Informe RA3 completo en Aula Virtual** |
