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

## RA4 · Administración Multiusuario, Permisos, Servicios y Monitorización (`RA4.a`–`RA4.h`)

1. [e16 · Creación de Usuarios, Grupos y Directivas (`chage` y `net accounts`)](e16-ra4-creacion-usuarios-grupos-politicas-chage-net.md) (`RA4.a`, `RA4.b`, `RA4.e` · 6 GB RAM)
2. [e17 · Permisos Locales (`chmod`, SGID, Sticky) y ACLs (`setfacl` e `icacls`)](e17-ra4-permisos-chmod-sgid-sticky-setfacl-icacls.md) (`RA4.d`, `RA4.e` · 6 GB RAM)
3. [e18 · Control de Procesos, Señales (`kill`/`nice`) y Servicios (`systemd`/PowerShell)](e18-ra4-control-procesos-senales-servicios-systemd.md) (`RA4.c`, `RA4.e` · 6 GB RAM)
4. [e19 · Auditoría de Logs (`journalctl`/Eventos) y Monitorización de Rendimiento](e19-ra4-auditoria-logs-journalctl-eventviewer-rendimiento.md) (`RA4.f`, `RA4.g` · 6 GB RAM)
5. [e20 · Preparación de Estación de Desarrollo DAM: Variables, `PATH` y Scripting](e20-ra4-preparacion-estacion-desarrollo-dam-variables.md) (`RA4.e`, `RA4.g`, `RA4.h` · 6 GB RAM)

## RA5 · Redes TCP/IP, Subredes VLSM, NAT, Diagnóstico y Protocolos Seguros (`RA5.a`–`RA5.h`)

1. [e21 · Cálculo de Subredes IPv4, Planificación VLSM y Compresión IPv6](e21-ra5-calculo-subredes-cidr-vlsm-ipv6.md) (`RA5.a` · 2 GB RAM)
2. [e22 · Configuración de Red con Netplan, `nmcli` y PowerShell en Red Interna](e22-ra5-configuracion-red-netplan-nmcli-powershell.md) (`RA5.a`, `RA5.b` · 6 GB RAM)
3. [e23 · VM Router Linux (`ip_forward`, NAT `MASQUERADE`) y Enrutamiento WAN](e23-ra5-router-nat-masquerade-enlaces-wan.md) (`RA5.d`, `RA5.e` · 4 GB RAM)
4. [e24 · Auditoría de Puertos (`ss`/`Get-NetTCPConnection`) y Diagnóstico *Bottom-Up*](e24-ra5-auditoria-puertos-diagnostico-red-ss-wireshark.md) (`RA5.c`, `RA5.f`, `RA5.g` · 6 GB RAM)
5. [e25 · Comunicaciones Seguras: SSH por Claves Ed25519, SFTP y Verificación TLS](e25-ra5-comunicaciones-seguras-ssh-claves-sftp-tls.md) (`RA5.f`, `RA5.h` · 6 GB RAM)

## RA6 · Recursos Compartidos, Servidores, Acceso Remoto, Cortafuegos y Dominios (`RA6.a`–`RA6.g`)

1. [e26 · Compartición de Recursos con Samba (`SMB3`) y Permisos Efectivos](e26-ra6-comparticion-samba-smb-permisos-efectivos.md) (`RA6.a`, `RA6.b`, `RA6.c` · 6 GB RAM)
2. [e27 · Despliegue NFSv4 (`root_squash`), Impresión CUPS y Proxy Nginx](e27-ra6-servidor-nfs-impresion-cups-tomcat.md) (`RA6.c` · 4 GB RAM)
3. [e28 · Conexión Remota Segura: RDP (NLA), Remmina y Túnel Local SSH](e28-ra6-escritorio-remoto-rdp-remmina-ssh-tunnel.md) (`RA6.d` · 6 GB RAM)
4. [e29 · Cortafuegos (`ufw`/Defender), `fail2ban` y Auditoría de Seguridad](e29-ra6-cortafuegos-ufw-windows-defender-fail2ban.md) (`RA6.e`, `RA6.f` · 6 GB RAM)
5. [e30 · Dominio Samba AD DC, Unidades Organizativas (`OU`) y Unión Windows 10](e30-ra6-dominio-samba-ad-dc-unidades-organizativas.md) (`RA6.b`, `RA6.g` · 6 GB RAM)

## Otros Bloques

*Los ejercicios de RA7 se publicarán secuencialmente tras completar el bloque.*
