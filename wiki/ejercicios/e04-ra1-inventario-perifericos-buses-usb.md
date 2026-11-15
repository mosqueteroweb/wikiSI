---
title: "e04 · Inventario de Buses PCIe/USB y Periféricos en VirtualBox"
ra: ["RA1"]
ce: ["RA1.a", "RA1.d"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra1-memorias-arranque-perifericos.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e04 · Inventario de Buses PCIe/USB y Periféricos en VirtualBox

> **Criterios de Evaluación:** `RA1.a` y `RA1.d` · **Concepto previo:** [Periféricos, Interfaces de Entrada/Salida y Buses](../conceptos/ra1-perifericos-interfaces-buses.md)

## Objetivo

Identificar los buses internos (PCIe, SATA, NVMe) y externos (USB) del equipo anfitrión **MAX**, comprobar qué módulo del kernel (*driver*) gestiona cada dispositivo y configurar en **VirtualBox** tanto el paso directo (*passthrough*) de un pendrive USB como una carpeta compartida hacia una VM **Linux Mint**.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(14 GB libres)* | Físicas | Red del aula |
| **`e04-Mint`** | Invitado | Linux Mint | **2048 MB (2 GB)** | 2 | 20 GB VDI · NAT |

> **Consumo total de VMs activas:** **2 GB** de 16 GB disponibles.

---

## Enunciado

1. En **MAX**, traza el árbol de dispositivos **PCI/PCIe** identificando la tarjeta gráfica, el controlador NVMe/SATA, el controlador USB xHCI y la tarjeta de red, junto al nombre del driver del kernel activo para cada uno.
2. Conecta un pendrive USB físico al equipo MAX y localiza en `lsusb -tv` y `dmesg` su velocidad negociada (`480M` USB 2.0 o `5000M` USB 3.x) y su nodo de bloque (`/dev/sdX`).
3. En **VirtualBox** (VM `e04-Mint`):
   - Configura una **carpeta compartida** (`~/Compartida_DAM` en MAX $\rightarrow$ montada en `e04-Mint`).
   - Añade un **filtro USB** para capturar el pendrive desde la VM (o conéctalo desde el menú *Dispositivos $\rightarrow$ USB* de VirtualBox).
4. Verifica dentro de `e04-Mint` que el pendrive aparece con `lsblk` y `lsusb`.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Inventario de buses PCIe y drivers en MAX

    ```bash
    # 1. Vista en árbol de puentes PCIe y dispositivos conectados
    lspci -tv

    # 2. Listar dispositivos con su identificador [Vendor:Device] y driver en uso
    lspci -nnk | grep -A 3 -E "VGA|NVMe|SATA|USB|Ethernet|Network"

    # 3. Ver el tipo de transporte físico de los discos instalados (nvme, sata, usb)
    lsblk -o NAME,SIZE,TYPE,TRAN,MODEL
    ```

    Verás líneas como `Kernel driver in use: nvme`, `xhci_hcd` (para el controlador USB 3.x) o `r8169` / `e1000e` (para Ethernet).

    ### Paso 2: Inspección del pendrive USB en MAX

    Conecta el pendrive y ejecuta:

    ```bash
    # Árbol de puertos raíz USB y velocidad negociada (480M = USB 2.0, 5000M = USB 3.0)
    lsusb -tv

    # Eventos del núcleo al detectar e identificar el almacenamiento masivo USB
    sudo dmesg | grep -i -E "usb|sd[a-z]" | tail -n 15
    ```

    ### Paso 3: Passthrough USB y Carpeta Compartida en VirtualBox

    1. **Permisos en MAX:** Tu usuario debe pertenecer al grupo `vboxusers` para capturar dispositivos USB físicos (si no lo está, el administrador ejecuta `sudo usermod -aG vboxusers $USER` y reinicia sesión).
    2. **Filtro USB en `e04-Mint`:**
       - Con la VM apagada, abre *Configuración → USB*.
       - Selecciona **Controlador USB 3.0 (xHCI)** (si el Extension Pack está instalado; si no, USB 1.1/2.0 según disponibilidad).
       - Pulsa el icono **Añadir filtro desde dispositivo (+)** y elige tu pendrive.
    3. **Carpeta compartida:**
       - En *Configuración → Carpetas compartidas*, añade `~/Compartida_DAM`, marca **Automontar** y define punto de montaje `/media/sf_Compartida_DAM`.
       - Dentro de `e04-Mint` (con *Guest Additions* instaladas), añade tu usuario invitado al grupo `vboxsf`:
         ```bash
         sudo usermod -aG vboxsf $USER
         ```
    4. **Comprobación final dentro de `e04-Mint`:**
       ```bash
       lsusb
       lsblk -o NAME,SIZE,TRAN,MOUNTPOINT
       ```
       El pendrive habrá desaparecido temporalmente del host MAX para quedar montado de forma exclusiva dentro de `e04-Mint`. Al apagar o liberar el dispositivo en *Dispositivos → USB*, vuelve automáticamente a MAX.
