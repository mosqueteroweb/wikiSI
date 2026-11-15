---
title: "e01 · Auditoría de Hardware: CPU y Placa Base en MAX y VirtualBox"
ra: ["RA1"]
ce: ["RA1.a"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra1-hardware-cpu-placas.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e01 · Auditoría de Hardware: CPU y Placa Base

> **Criterio de Evaluación:** `RA1.a` · **Concepto previo:** [Arquitectura de Von Neumann, Placa Base y CPU](../conceptos/ra1-arquitectura-placa-base-cpu.md)

## Objetivo

Extraer el inventario técnico completo del procesador (arquitectura, núcleos físicos, hilos, cachés, flags de virtualización) y de la placa base sin abrir la carcasa del PC, comparando el hardware real del **host MAX** con el hardware emulado/paravirtualizado de una máquina virtual **Windows 10** en **Oracle VirtualBox**.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(12 GB libres)* | Físicas | Red del aula |
| **`e01-Win10`** | Invitado | Windows 10 | **4096 MB (4 GB)** | 2 | 40 GB VDI · NAT |

> **Consumo total de VMs activas:** **4 GB** de 16 GB disponibles (cumple el tope de 10–12 GB).

---

## Enunciado

1. Abre una terminal en el equipo anfitrión **MAX** y averigua:
   - Modelo exacto de procesador, arquitectura (`x86_64`), número de núcleos físicos, hilos por núcleo y si está activada la virtualización por hardware (`VT-x` o `AMD-V`).
   - Fabricante, modelo y versión de la placa base física.
2. En **VirtualBox** (sobre MAX), comprueba en *Configuración → Sistema → Procesador* y *Aceleración* que la VM `e01-Win10` tiene asignadas **2 vCPUs** y **PAE/NX + KVM/VT-x** habilitados.
3. Arranca `e01-Win10`, abre **PowerShell** y consulta desde consola (y con `msinfo32`) el procesador y la placa base detectados dentro de la VM.
4. Responde brevemente: ¿por qué coinciden el modelo de CPU entre MAX y la VM, pero difiere el fabricante de la placa base?

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Inspección en el anfitrión MAX (Linux)

    ```bash
    # 1. Consultar CPU, núcleos físicos, hilos y virtualización
    lscpu | grep -E "Architecture|Model name|Thread\(s\) per core|Core\(s\) per socket|CPU\(s\)|Virtualization"

    # 2. Consultar fabricante y modelo de la placa base real
    sudo dmidecode -t baseboard | grep -E "Manufacturer|Product Name|Version"
    ```

    **Ejemplo de salida esperada en un PC de aula:**
    ```text
    Architecture:            x86_64
    CPU(s):                  12
    Thread(s) per core:      2
    Core(s) per socket:      6
    Model name:              Intel(R) Core(TM) i5-12400
    Virtualization:          VT-x
    ```
    En `dmidecode`, observarás el fabricante real de la placa física (por ejemplo, `ASUS`, `Gigabyte`, `HP` o `Lenovo`).

    ### Paso 2: Verificación en la VM `e01-Win10` (PowerShell)

    Dentro de Windows 10, abre **PowerShell** y ejecuta:

    ```powershell
    # Datos del procesador detectado por Windows 10
    Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed, VirtualizationFirmwareEnabled

    # Datos de la placa base vista por la máquina virtual
    Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, Version

    # Alternativa gráfica completa:
    msinfo32
    ```

    **Salida esperada en la VM:**
    - `Win32_Processor`: mostrará el procesador físico del aula (`Core i5-12400`), pero limitado a **`NumberOfCores: 2`** y **`NumberOfLogicalProcessors: 2`** (las 2 vCPUs asignadas en VirtualBox).
    - `Win32_BaseBoard`: reportará `Manufacturer: Oracle Corporation` y `Product: VirtualBox` (o placa virtual emulada).

    ### Paso 3: Respuesta técnica

    - **CPU coincidente:** Los hipervisores de tipo 2 con virtualización asistida por hardware (`VT-x` / `AMD-V`) permiten que la VM ejecute instrucciones directamente sobre los núcleos físicos de la CPU real, exponiendo la arquitectura e identidad del procesador físico al invitado.
    - **Placa base diferente:** VirtualBox abstrae y virtualiza la placa base, los puentes y el chipset (`PIIX3` o `ICH9`) para ofrecer un hardware estándar y portable al sistema operativo invitado, aislando al invitado de las peculiaridades físicas de la placa del aula.
