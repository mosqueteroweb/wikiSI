---
title: "Ejercicios Prácticos Resueltos"
tipo: "indice"
publicar: true
ultima_revision: "2026-11-15"
---

# Ejercicios Prácticos Resueltos

Píldoras prácticas breves enfocadas en **una destreza técnica concreta** (un comando de consola, un análisis de memoria o arranque, configuración de buses/USB o interpretación de red), diseñadas para ejecutarse en el laboratorio del aula (**MAX + Oracle VirtualBox**).

Cada ejercicio incluye:

- Objetivo y criterios de evaluación (`RAx.CEy`) trabajados.
- Especificación de máquinas virtuales y presupuesto de RAM ($\le 10\text{–}12\text{ GB}$ totales en equipos de 16 GB).
- Enunciado breve y **resolución paso a paso** desplegable.

---

## RA1 · Hardware, Memorias, Arranque, Periféricos, Redes y PRL (Completado ✅)

1. [e01 · Auditoría de Hardware: CPU y Placa Base en MAX y VirtualBox](e01-ra1-auditoria-hardware-cpu-placas.md) (`RA1.a` · 4 GB RAM)
2. [e02 · Análisis de la Jerarquía de Memorias y Presupuesto de RAM](e02-ra1-analisis-jerarquia-memorias.md) (`RA1.b` · 2 GB RAM)
3. [e03 · Verificación del Arranque UEFI vs. BIOS y Análisis de Tiempos](e03-ra1-verificacion-arranque-uefi-bios.md) (`RA1.c` · 2 GB RAM)
4. [e04 · Inventario de Buses PCIe/USB y Periféricos en VirtualBox](e04-ra1-inventario-perifericos-buses-usb.md) (`RA1.a`, `RA1.d` · 2 GB RAM)
5. [e05 · Mapa Físico/Lógico de Red en VirtualBox y Checklist PRL](e05-ra1-interpretacion-mapa-red-prl.md) (`RA1.e`–`RA1.h` · 3 GB RAM con Puppy + Ubuntu)

---

## RA2 · Instalación, Dual-Boot, Virtualización, Paquetes y Recuperación (Completado ✅)

1. [e06 · Verificación de ISOs, Licencias y Provisionamiento VM UEFI en VirtualBox](e06-ra2-verificacion-isos-creacion-vm-virtualbox.md) (`RA2.a`, `RA2.c`, `RA2.d`, `RA2.g` · 6 GB RAM con Win11 + Mint)
2. [e07 · Planificación e Instalación Dual-Boot Windows + Ubuntu en UEFI/GPT](e07-ra2-instalacion-dual-boot-windows-ubuntu.md) (`RA2.d`, `RA2.e`, `RA2.g` · 4 GB RAM)
3. [e08 · Configuración y Reparación de Arranque Dual-Boot (GRUB2 y BCD)](e08-ra2-configuracion-reparacion-grub-bcd.md) (`RA2.e`, `RA2.f` · 4 GB RAM)
4. [e09 · Gestión Profesional de Aplicaciones: `apt`, `dpkg`, Snap y `winget`](e09-ra2-gestion-paquetes-apt-dpkg-winget.md) (`RA2.h` · 6 GB RAM con Ubuntu + Win10)
5. [e10 · Recuperación ante Desastres: Snapshots, Timeshift, DISM/SFC y Acta Técnica](e10-ra2-recuperacion-snapshots-timeshift-dism.md) (`RA2.f`, `RA2.g`, `RA2.i` · 6 GB RAM con Mint + Win10)

---

## RA3 · Sistemas de Archivos, Directorios, Búsquedas, LVM/RAID, Cifrado y Backups (Completado ✅)

1. [e11 · Exploración FHS, Inodos, Enlaces y Búsqueda Avanzada](e11-ra3-exploracion-fhs-inodos-enlaces-busqueda.md) (`RA3.a`–`RA3.d` · 6 GB RAM con Ubuntu + Win10)
2. [e12 · Particionado GPT, Formateo y Montaje Persistente (`fstab` vs. `DiskPart`)](e12-ra3-particionado-montaje-fstab-diskpart.md) (`RA3.a`, `RA3.e` · 6 GB RAM)
3. [e13 · Volúmenes Lógicos `LVM` y Matrices `RAID 1` por Software (`mdadm`)](e13-ra3-volumenes-logicos-lvm-raid-mdadm.md) (`RA3.e`, `RA3.h` · 2 GB RAM)
4. [e14 · Chequeo SMART, Reparación Lógica (`fsck`/`chkdsk`), TRIM y Cifrado `LUKS` / `BitLocker`](e14-ra3-chequeo-smart-cifrado-luks-bitlocker.md) (`RA3.e`, `RA3.h` · 6 GB RAM)
5. [e15 · Copias de Seguridad con `rsync`, `tar` y `Robocopy` más Automatización (`cron` y `schtasks`)](e15-ra3-backups-rsync-tar-cron-schtasks.md) (`RA3.f`, `RA3.g`, `RA3.h` · 6 GB RAM)

## Otros Bloques

*Los ejercicios de RA4–RA7 se publicarán secuencialmente tras completar cada bloque.*
