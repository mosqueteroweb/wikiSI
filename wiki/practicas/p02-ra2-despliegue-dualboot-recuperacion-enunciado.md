---
title: "Práctica p02 · Despliegue Dual-Boot, Gestión de Paquetes, Arranque y Recuperación"
ra: ["RA2"]
ce: ["RA2.a", "RA2.b", "RA2.c", "RA2.d", "RA2.e", "RA2.f", "RA2.g", "RA2.h", "RA2.i"]
tipo: "practica-enunciado"
publicar: true
fuentes:
  - "raw/procesados/ra2-arquitectura-so-licencias.md"
  - "raw/procesados/ra2-virtualizacion-planificacion-instalacion.md"
  - "raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md"
ultima_revision: "2026-11-15"
---

# Práctica 02 · Despliegue Dual-Boot, Gestión de Paquetes, Arranque y Recuperación

<!-- fuente: raw/procesados/ra2-arquitectura-so-licencias.md -->
<!-- fuente: raw/procesados/ra2-virtualizacion-planificacion-instalacion.md -->
<!-- fuente: raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md -->

> **Criterios de Evaluación cubiertos:** `RA2.a`, `RA2.b`, `RA2.c`, `RA2.d`, `RA2.e`, `RA2.f`, `RA2.g`, `RA2.h`, `RA2.i` (100% de **RA2**)

---

## Escenario Profesional

Un estudio de desarrollo de software necesita implantar estaciones de trabajo mixtas **Windows 10/11 + Ubuntu 24.04 LTS** en arranque dual (**UEFI + GPT**) para compilar y probar aplicaciones multiplataforma, junto con un protocolo estandarizado de despliegue de software, copias/instantáneas de seguridad y un medio ligero de rescate (**Puppy Linux**).

Como técnico de **1º DAM**, realizarás la planificación, instalación virtualizada en **Oracle VirtualBox sobre MAX**, personalización de arranque, gestión de paquetes, simulacro de rescate y documentación técnica final (**Acta RA2**), apoyándote en los conceptos teóricos y los ejercicios `e06`–`e10`.

---

## Presupuesto de Recursos VirtualBox (Obligatorio · Aula 16 GB)

| Equipo / VM | Rol en la práctica | Sistema Operativo | RAM asignada | vCPUs | Disco / Firmware | Red VirtualBox |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **Host Aula** | Estación anfitriona | **MAX (Linux)** | *(11 GB libres)* | Físicas | Disco físico aula | Red física aula |
| **`DAM-Estacion-Dual`** | Estación Dual-Boot | **Windows 10 + Ubuntu 24.04** | **4096 MB (4 GB)** | 2 | **60 GB VDI · UEFI activado** | NAT + `intnet` (`lan-ra2`) |
| **`DAM-Rescate-Puppy`** | Nodo ligero de rescate | **Puppy Linux (Live/RAM)** | **1024 MB (1 GB)** | 1 | Live ISO / 8 GB VDI | `intnet` (`lan-ra2`) |

> **Consumo total de VMs simultáneas:** **5 GB de 16 GB** disponibles en el host MAX (cumple ampliamente el margen máximo de 10–12 GB).

---

## Apoyo Previo Recomendado

- [Conceptos de RA2](../ra/RA2.md#conceptos-teoricos)
- [e06 · Verificación de ISOs y Provisionamiento VM UEFI](../ejercicios/e06-ra2-verificacion-isos-creacion-vm-virtualbox.md)
- [e07 · Planificación e Instalación Dual-Boot](../ejercicios/e07-ra2-instalacion-dual-boot-windows-ubuntu.md)
- [e08 · Configuración y Reparación GRUB2/BCD](../ejercicios/e08-ra2-configuracion-reparacion-grub-bcd.md)
- [e09 · Gestión de Paquetes `apt`, `dpkg` y `winget`](../ejercicios/e09-ra2-gestion-paquetes-apt-dpkg-winget.md)
- [e10 · Recuperación con Snapshots, Timeshift y DISM](../ejercicios/e10-ra2-recuperacion-snapshots-timeshift-dism.md)

---

## Tareas a Realizar

### Tarea 1 · Arquitectura, Licencias y Planificación (`RA2.a`, `RA2.b`, `RA2.c`, `RA2.d`)
1. Describe brevemente cómo interactúan los elementos funcionales del puesto (**hardware virtualizado → kernel → sistema de archivos/drivers → shell/aplicaciones**) en tu VM `DAM-Estacion-Dual` y compara la arquitectura de kernel de **Windows** (híbrido) frente a **Linux** (monolítico modular).
2. Elabora una tabla comparativa de requisitos y licenciamiento (**Windows 10/11**, **Ubuntu 24.04 LTS**, **Linux Mint** y **Puppy Linux**) justificando por qué `DAM-Rescate-Puppy` funciona fluidamente con solo `1024 MB` de RAM.
3. Verifica en el **Host MAX** mediante `sha256sum` la integridad de las imágenes ISO que vayas a utilizar antes de crear las VMs.
4. Diseña por escrito el **plan de particionado GPT** sobre el disco de `60 GiB` antes de iniciar el instalador.

### Tarea 2 · Provisionamiento VirtualBox y Despliegue Dual-Boot (`RA2.d`, `RA2.e`, `RA2.g`)
1. Provisiona la VM **`DAM-Estacion-Dual`** (`4096 MB`, `2 vCPUs`, **`--firmware efi`**, `60 GB VDI` dinámico, Adaptador 1 **NAT**, Adaptador 2 **Red interna `lan-ra2`**) preferiblemente mediante `VBoxManage` (o documentando la equivalencia GUI).
2. Instala **Windows 10** en la primera mitad del disco (~30 GiB), dejando ~30 GiB **Sin asignar**, finaliza la configuración OOBE con usuario local `alumdam`, **desactiva el Inicio Rápido** (`powercfg /hibernate off`) y crea un snapshot en VirtualBox llamado **`Base-Win10-OK`**.
3. Instala **Ubuntu 24.04 Desktop** en el espacio libre usando particionado manual:
   - Reutiliza la partición **ESP (FAT32)** existente montándola en **`/boot/efi` SIN formatear**.
   - Crea **`/`** (`ext4`, `16 GiB`) y **`/home`** (`ext4`, espacio restante).
   - Habilita `GRUB_DISABLE_OS_PROBER=false` si fuera necesario y confirma que GRUB ofrece ambos sistemas.

### Tarea 3 · Personalización del Arranque y Rescate de GRUB (`RA2.e`, `RA2.f`)
1. Configura **`/etc/default/grub`** para mostrar el menú durante **7 segundos** y recordar la última opción elegida (`GRUB_DEFAULT=saved`, `GRUB_SAVEDEFAULT=true`). Aplica cambios con `sudo update-grub`.
2. Registra el estado sano antes de la avería ejecutando `efibootmgr -v` (en Ubuntu) y `bcdedit /enum` (en Windows).
3. Toma un **Snapshot de VirtualBox** llamado **`Pre-Averia-Boot`**. A continuación, simula la pérdida del selector GRUB anteponiendo la entrada UEFI de Windows con `efibootmgr -o` para que arranque Windows directamente sin pasar por GRUB.
4. Arranca `DAM-Estacion-Dual` desde la ISO Live de Ubuntu (*Probar Ubuntu*), monta `/` y `/boot/efi`, enlaza `/dev`, `/proc`, `/sys`, `/sys/firmware/efi/efivars`, accede mediante **`chroot`** y reinstala **GRUB2** (`grub-install` + `update-grub`) comprobando que el arranque dual vuelve a funcionar.

### Tarea 4 · Gestión de Software y Mantenimiento del Sistema (`RA2.f`, `RA2.h`)
1. **En Ubuntu (`DAM-Estacion-Dual`):**
   - Ejecuta `sudo apt update && sudo apt upgrade -y` e instala `htop` y `timeshift`.
   - Descarga un paquete `.deb` (p. ej. `apt download tree`) e instálalo manualmente con `sudo dpkg -i`.
   - Instala `nginx` (o `screen`), demuestra la diferencia real entre `sudo apt remove` y `sudo apt purge` comprobando `/etc/`, ejecuta `autoremove` y exporta la lista de paquetes instalados a `paquetes_ubuntu.txt`.
2. **En Windows 10 (`DAM-Estacion-Dual`):**
   - Instala **`7zip.7zip`** mediante **`winget`**, consulta actualizaciones con `winget upgrade` y exporta tu catálogo a `apps_win10.json`.
   - Comprueba la salud de la imagen del sistema ejecutando `DISM /Online /Cleanup-Image /CheckHealth` y `sfc /scannow`.

### Tarea 5 · Recuperación Interna y Nodo Ligero en Red Aislada (`RA2.f`, `RA2.g`)
1. En Ubuntu, crea una instantánea **`Timeshift`** (`RSYNC`), crea un documento de usuario `~/Documentos/entrega_dam.txt`, simula el borrado accidental de `/etc/hosts` (`sudo mv /etc/hosts /etc/hosts.bak`) y restaura el sistema con Timeshift demostrando que `/etc/hosts` vuelve a existir y `entrega_dam.txt` no se pierde.
2. Arranca simultáneamente **`DAM-Rescate-Puppy`** (`1024 MB RAM`, conectada a `lan-ra2`), configura temporalmente una IP en `lan-ra2` (`192.168.100.30/24`) y verifica la conectividad con el Ubuntu de `DAM-Estacion-Dual` (`192.168.100.10/24`), documentando el consumo total de RAM real en el host MAX (`free -h` en MAX).

### Tarea 6 · Documentación Técnica y Acta de Entrega (`RA2.i`)
Redacta el informe final **`Informe_RA2_ApellidoNombre.pdf`** siguiendo estándares profesionales de documentación de sistemas (ver sección *Entregables*).

---

## Entregables en el Aula Virtual

Sube un único PDF **`Informe_RA2_ApellidoNombre.pdf`** que incluya ordenadamente:

1. **Portada y Presupuesto VirtualBox:** Tabla de VMs usadas (`4 GB + 1 GB = 5 GB`) y comandos/capturas de verificación **SHA-256** de las ISOs.
2. **Arquitectura, Licencias y Planificación (`Tareas 1 y 2`):** Tabla comparativa de SO/licencias, tabla de particiones planificada frente a salida real de `lsblk -f` y `Get-Partition`.
3. **Arreglo de Arranque y Mantenimiento (`Tareas 3 y 4`):** Salidas de `efibootmgr -v`, `bcdedit`, comandos de rescate `chroot`, capturas/logs de `apt`/`dpkg`/`winget` y resultados de `DISM` + `sfc`.
4. **Rescate y Entorno Multinodo (`Tarea 5`):** Evidencias de recuperación de Timeshift conservando `/home`, prueba `ping` entre `DAM-Estacion-Dual` y `DAM-Rescate-Puppy` y captura de `free -h` en MAX demostrando el respeto al margen de RAM.
5. **Bitácora de Incidencias y Árbol de Snapshots (`Tarea 6`):** Registro cronológico de fallos simulados/resueltos y salida de `VBoxManage snapshot "DAM-Estacion-Dual" list`.

---

## Ponderación por Criterios de Evaluación

| Criterio | Peso en la práctica | Evidencia principal |
| :--- | :---: | :--- |
| **RA2.a** | 5 % | Descripción de elementos funcionales e interacción en la VM (Tarea 1) |
| **RA2.b** | 10 % | Comparativa funcional y arquitectura de kernel Windows vs Linux (Tarea 1) |
| **RA2.c** | 10 % | Matriz de requisitos, campos de aplicación y licencias (Tarea 1) |
| **RA2.d** | 15 % | Verificación SHA-256 + diseño previo del particionado GPT/UEFI (Tareas 1 y 2) |
| **RA2.e** | 15 % | Instalación Dual-Boot Windows + Ubuntu funcional y configuración GRUB2 (Tareas 2 y 3) |
| **RA2.f** | 15 % | Rescate GRUB vía `chroot` + recuperación Timeshift + `DISM`/`sfc` (Tareas 3, 4 y 5) |
| **RA2.g** | 10 % | Provisionamiento VirtualBox, red interna `lan-ra2`, snapshots y cálculo de RAM (Tareas 2 y 5) |
| **RA2.h** | 10 % | Gestión completa de paquetes con `apt`, `dpkg` (`remove` vs `purge`) y `winget` (Tarea 4) |
| **RA2.i** | 10 % | Calidad técnica, trazabilidad y rigor del Informe/Acta final (Tarea 6) |
| **Total** | **100 %** | **Informe RA2 completo en Aula Virtual** |
