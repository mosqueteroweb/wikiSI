---
title: "Práctica p01 · Auditoría Integral de Hardware, Arranque, Red y PRL"
ra: ["RA1"]
ce: ["RA1.a", "RA1.b", "RA1.c", "RA1.d", "RA1.e", "RA1.f", "RA1.g", "RA1.h"]
tipo: "practica-enunciado"
publicar: true
fuentes:
  - "raw/procesados/ra1-hardware-cpu-placas.md"
  - "raw/procesados/ra1-memorias-arranque-perifericos.md"
  - "raw/procesados/ra1-redes-fisica-topologias-prl.md"
ultima_revision: "2026-11-15"
---

# Práctica 01 · Auditoría Integral de Sistema, Arranque, Red y PRL

> **Criterios de Evaluación cubiertos:** `RA1.a`, `RA1.b`, `RA1.c`, `RA1.d`, `RA1.e`, `RA1.f`, `RA1.g`, `RA1.h` (100% de **RA1**)

---

## Escenario Profesional

El departamento de Sistemas de una empresa de desarrollo de software acaba de incorporar nuevos puestos de trabajo con **MAX (Linux)** y necesita validar tanto el hardware físico de cada estación como la preparación de su laboratorio de virtualización mixto en **Oracle VirtualBox** (Windows + Linux) antes de iniciar el desarrollo de aplicaciones.

Como técnico de **1º DAM**, debes elaborar el **Informe Técnico de Auditoría RA1** completo de tu puesto en el aula y de un laboratorio de dos máquinas virtuales en red aislada, apoyándote en los conceptos teóricos y los ejercicios `e01`–`e05`.

---

## Presupuesto de Recursos VirtualBox (Obligatorio · Aula 16 GB)

| Equipo / VM | Rol en la auditoría | Sistema Operativo | RAM asignada | vCPUs | Disco / Firmware | Red VirtualBox |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **Host Aula** | Estación física base | **MAX (Linux)** | *(10 GB libres)* | Físicas | Disco físico aula | Red física aula |
| **`DAM-Win10-Audit`** | Estación cliente Windows | **Windows 10** | **4096 MB (4 GB)** | 2 | 40 GB VDI · EFI off/on | **Red interna** (`lan-ra1`) |
| **`DAM-Ubuntu-Node`** | Nodo Linux auditor | **Ubuntu Desktop** | **2048 MB (2 GB)** | 2 | 25 GB VDI · **EFI activado** | **Red interna** (`lan-ra1`) |

> **Consumo total de VMs simultáneas:** **6 GB de 16 GB** disponibles en el host MAX (dentro del límite máximo de 10–12 GB).

---

## Apoyo Previo Recomendado

- [Conceptos de RA1](../ra/RA1.md#conceptos-teoricos)
- [e01 · Auditoría de CPU y Placa Base](../ejercicios/e01-ra1-auditoria-hardware-cpu-placas.md)
- [e02 · Análisis de Jerarquía de Memorias](../ejercicios/e02-ra1-analisis-jerarquia-memorias.md)
- [e03 · Verificación del Arranque UEFI/BIOS](../ejercicios/e03-ra1-verificacion-arranque-uefi-bios.md)
- [e04 · Inventario de Buses PCIe/USB](../ejercicios/e04-ra1-inventario-perifericos-buses-usb.md)
- [e05 · Mapa Físico/Lógico y Checklist PRL](../ejercicios/e05-ra1-interpretacion-mapa-red-prl.md)

---

## Tareas a Realizar

### Tarea 1 · Hardware Central y Arquitectura (`RA1.a`)
1. Extrae del **Host MAX** (`lscpu`, `dmidecode -t baseboard`) el modelo de procesador, arquitectura, número de núcleos/hilos, soporte `VT-x`/`AMD-V`, fabricante/modelo de placa base y formato estimado.
2. Compara esos datos con los reportados dentro de **`DAM-Win10-Audit`** (`Get-CimInstance Win32_Processor`, `Win32_BaseBoard` y `msinfo32`). Explica en 3 líneas qué abstrae VirtualBox y qué hereda directamente de la CPU física.

### Tarea 2 · Jerarquía de Memorias y Planificación de RAM (`RA1.b`)
1. Documenta las **cachés L1d, L1i, L2 y L3**, la configuración de **RAM física** del equipo del aula (`dmidecode -t memory` / `free -h`: capacidad por módulo, tipo DDR, velocidad MT/s, Dual/Single Channel) y el tamaño del área **Swap** (en MAX) y **`pagefile.sys`** (en `DAM-Win10-Audit`).
2. Justifica numéricamente por qué este laboratorio (`6 GB` en VMs) es seguro en un equipo de 16 GB frente a asignar `14 GB` a máquinas virtuales.

### Tarea 3 · Verificación del Arranque y Firmware (`RA1.c`)
1. Comprueba el modo de arranque real del **Host MAX** (`[ -d /sys/firmware/efi ]`, `lsblk`, `efibootmgr -v`) y mide el tiempo total y los 5 servicios que más tardan en arrancar (`systemd-analyze blame`).
2. Configura **`DAM-Ubuntu-Node`** con **EFI habilitado** en VirtualBox y verifica desde dentro la existencia de la partición `ESP` (`/boot/efi` en `vfat`) y el cargador `\EFI\ubuntu\shimx64.efi`.

### Tarea 4 · Periféricos, Buses e Interconexión (`RA1.a`, `RA1.d`)
1. Identifica en **MAX** mediante `lspci -nnk`, `lsusb -tv` y `lsblk -o NAME,SIZE,TYPE,TRAN,MODEL` qué interfaz (`NVMe/PCIe`, `SATA`, `USB`) utiliza el disco principal del equipo y qué controlador del kernel gobierna la tarjeta de red y el controlador USB.
2. Configura una **carpeta compartida** entre MAX y `DAM-Ubuntu-Node` (con *Guest Additions*) y realiza una captura o registro verificando el acceso a un archivo de prueba desde ambas máquinas, o bien realiza *passthrough* de un pendrive USB comprobando su detección en `lsusb`.

### Tarea 5 · Topología, Cableado y Mapas Físico/Lógico (`RA1.e`, `RA1.f`, `RA1.g`)
1. Conecta **`DAM-Win10-Audit`** y **`DAM-Ubuntu-Node`** a la misma **Red interna** `lan-ra1` en VirtualBox y configura manualmente las IPs estáticas:
   - `DAM-Win10-Audit`: `192.168.100.10` / máscara `255.255.255.0`
   - `DAM-Ubuntu-Node`: `192.168.100.20` / máscara `255.255.255.0`
2. Verifica la conectividad bidireccional con `ping` y comprueba la resolución IP → MAC (`ip neigh show` / `arp -a`).
3. Elabora e incluye en tu informe:
   - Un **Mapa Físico** desde tu puesto MAX hasta el *Switch* del aula (indicando tipo de cable Cat5e/Cat6, conector RJ-45 norma **T568B**, roseta, *Patch Panel* y velocidad negociada con `ethtool`).
   - Un **Mapa Lógico** de `lan-ra1` (subred, máscaras, direcciones IP, direcciones MAC reales de tus adaptadores virtuales y modo de red VirtualBox).

### Tarea 6 · Auditoría de Seguridad y PRL (`RA1.h`)
1. Redacta un **protocolo breve de 5 pasos obligatorios** (seguridad eléctrica + protección **ESD**) que deberías aplicar antes de ampliar físicamente un módulo de memoria RAM en uno de los equipos del aula.
2. Evalúa tu puesto de trabajo en clase frente a 5 requisitos del **RD 488/1997 (PVD)** (distancia, altura del monitor, reflejos de ventanas, postura 90° y regla 20-20-20) indicando qué punto cumple y qué ajuste propones.

---

## Entregables en el Aula Virtual

Sube un único documento **`Informe_RA1_ApellidoNombre.pdf`** (o Markdown exportado a PDF) que contenga:

1. Portada con tus datos, fecha y tabla resumen del presupuesto de RAM usado.
2. Evidencias (salidas de terminal copiadas en bloques de código y/o capturas legibles) de las **Tareas 1 a 5**.
3. Los dos diagramas solicitados (**Mapa Físico** del aula y **Mapa Lógico** de `lan-ra1`).
4. El protocolo **ESD/Eléctrico** y la tabla **PVD** de la **Tarea 6**.

---

## Ponderación por Criterios de Evaluación

| Criterio | Peso en la práctica | Evidencia principal |
| :--- | :---: | :--- |
| **RA1.a** | 15 % | Inventario CPU/placa base + buses PCIe (Tareas 1 y 4) |
| **RA1.b** | 15 % | Cachés, módulos RAM, Swap/`pagefile.sys` y presupuesto de 16 GB (Tarea 2) |
| **RA1.c** | 15 % | Verificación UEFI/ESP, `efibootmgr` y `systemd-analyze` (Tarea 3) |
| **RA1.d** | 10 % | Controladores `lspci -nnk`/`lsusb` y periférico/carpeta compartida en VirtualBox (Tarea 4) |
| **RA1.e** | 10 % | Clasificación de la LAN física y red virtual aislada (Tarea 5) |
| **RA1.f** | 10 % | Identificación de NIC, MAC, cableado T568B y switch/patch panel (Tarea 5) |
| **RA1.g** | 15 % | Mapa Físico + Mapa Lógico + pruebas `ping`/`arp` en `lan-ra1` (Tarea 5) |
| **RA1.h** | 10 % | Protocolo de seguridad eléctrica/ESD y auditoría PVD (Tarea 6) |
| **Total** | **100 %** | Informe completo en Aula Virtual |
