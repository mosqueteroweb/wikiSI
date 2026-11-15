---
title: "e02 · Análisis de la Jerarquía de Memorias y Presupuesto de RAM"
ra: ["RA1"]
ce: ["RA1.b"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra1-memorias-arranque-perifericos.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e02 · Análisis de la Jerarquía de Memorias y Presupuesto de RAM

> **Criterio de Evaluación:** `RA1.b` · **Concepto previo:** [Jerarquía de Memorias y Tipos de Memoria](../conceptos/ra1-jerarquia-tipos-memoria.md)

## Objetivo

Inspeccionar todos los niveles de la jerarquía de memoria volátil y virtual en **MAX** y en una máquina virtual **Ubuntu Desktop** en VirtualBox (cachés L1/L2/L3, módulos RAM físicos, velocidad DDR y memoria de intercambio *Swap*), y validar un escenario multi-VM respetando el límite de **10–12 GB** de los equipos de 16 GB del aula.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(14 GB libres)* | Físicas | Red del aula |
| **`e02-Ubuntu`** | Invitado | Ubuntu Desktop | **2048 MB (2 GB)** | 2 | 25 GB VDI · NAT |

> **Consumo total de VMs activas:** **2 GB** de 16 GB disponibles.

---

## Enunciado

1. En el anfitrión **MAX**, obtén mediante comandos:
   - El tamaño de las cachés **L1d, L1i, L2 y L3** de la CPU.
   - El número de módulos RAM instalados, su capacidad individual, tipo (`DDR4`/`DDR5`), formato (`DIMM`/`SO-DIMM`) y velocidad configurada en `MT/s`.
   - La RAM total, usada, disponible y el estado de la memoria **Swap**.
2. Arranca la VM `e02-Ubuntu` con **2 GB de RAM** y ejecuta `free -h` y `swapon --show` para comparar su memoria virtual con la del anfitrión.
3. **Caso de planificación:** Un compañero quiere arrancar simultáneamente en el aula (PC de 16 GB con MAX): una VM **Windows 11** (6 GB), una VM **Ubuntu Desktop** (4 GB), una VM **Ubuntu Server** (2 GB) y una VM **Linux Mint** (3 GB). Calcula el consumo total y propón una redistribución segura cumpliendo las normas de clase.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Cachés, módulos RAM y Swap en el anfitrión MAX

    ```bash
    # 1. Tamaños de caché SRAM en el procesador
    lscpu | grep -i cache

    # 2. Inventario de zócalos de memoria y módulos físicos instalados
    sudo dmidecode -t memory | grep -E "Locator:|Size:|Type:|Form Factor:|Configured Memory Speed:"

    # 3. Memoria RAM total, caché de disco (buff/cache) y Swap activa
    free -h
    swapon --show
    ```

    **Interpretación clave de `free -h`:**
    - Fíjate en la columna **`available`** (no solo en `free`): Linux aprovecha la RAM ociosa como caché de archivos (`buff/cache`) para acelerar lecturas, pero la libera al instante si una aplicación o VirtualBox la solicita.
    - Si en `dmidecode` aparecen dos módulos idénticos instalados en ranuras emparejadas (ej. `2 x 8 GB DDR4-3200`), el controlador trabaja en **Dual Channel** (~51,2 GB/s teóricos).

    ### Paso 2: Comparativa dentro de la VM `e02-Ubuntu`

    ```bash
    free -h
    swapon --show
    cat /proc/meminfo | head -n 5
    ```

    Verás `MemTotal` próximo a `1.9Gi` (los 2048 MB asignados en VirtualBox menos una pequeña reserva del firmware/kernel) y un archivo `/swapfile` o partición swap que amortigua picos puntuales de memoria dentro de la VM.

    ### Paso 3: Corrección del presupuesto multi-VM

    - **Propuesta del compañero:** $6 + 4 + 2 + 3 = \mathbf{15\text{ GB}}$ para las VMs, dejando solo **1 GB** para el anfitrión MAX y VirtualBox. Esto provocaría *swapping/thrashing* severo y congelamiento del equipo del aula.
    - **Redistribución válida ($\le 10\text{–}12\text{ GB}$ totales en VMs):**
      - Si solo necesita 3 máquinas a la vez: Windows 11 (**4 GB**) + Ubuntu Desktop (**2 GB**) + Ubuntu Server (**1,5 GB**) + **Puppy Linux** en lugar de Mint si requiere un cuarto nodo ligero (**1 GB**) = **8,5 GB totales**, reservando **7,5 GB libres** para MAX.
      - En cualquier caso, **nunca superar los 10–12 GB sumando todas las VMs encendidas al mismo tiempo**.
