---
title: "e03 · Verificación del Arranque UEFI vs. BIOS y Análisis de Tiempos"
ra: ["RA1"]
ce: ["RA1.c"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra1-memorias-arranque-perifericos.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e03 · Verificación del Arranque UEFI vs. BIOS y Análisis de Tiempos

> **Criterio de Evaluación:** `RA1.c` · **Concepto previo:** [Puesta en Marcha del Equipo: POST, BIOS Legacy y UEFI](../conceptos/ra1-puesta-en-marcha-bios-uefi.md)

## Objetivo

Comprobar desde el sistema operativo si el arranque se realizó en modo **UEFI** o **BIOS Legacy**, inspeccionar la partición del sistema EFI (`ESP`) y las entradas de arranque en NVRAM, y medir cuánto tarda cada etapa de la puesta en marcha en **MAX** y en una VM **Ubuntu** en VirtualBox.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | Firmware VirtualBox | Disco / Red |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(14 GB libres)* | UEFI / BIOS del PC | Red del aula |
| **`e03-Ubuntu-EFI`** | Invitado | Ubuntu Desktop | **2048 MB (2 GB)** | **EFI habilitado** | 25 GB VDI · NAT |

> **Consumo total de VMs activas:** **2 GB** de 16 GB disponibles.

---

## Enunciado

1. En el host **MAX**, verifica mediante la existencia del directorio `/sys/firmware/efi` si el sistema arrancó con UEFI o BIOS Legacy.
2. Lista las particiones de almacenamiento para localizar la partición EFI (`FAT32` / `vfat` montada en `/boot/efi`) e inspecciona las entradas registradas en la NVRAM con `efibootmgr`.
3. Analiza el tiempo de arranque desglosado (`firmware`, `loader`, `kernel`, `userspace`) y detecta los 5 servicios que más tiempo consumen al iniciar el equipo.
4. En VirtualBox, crea o configura `e03-Ubuntu-EFI` activando la casilla **Habilitar EFI (solo SO especiales)** en *Sistema → Placa base* (sin marcar nada fuera de las especificaciones del SO) y comprueba la diferencia frente a una VM sin EFI.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Comprobar modo de firmware (UEFI vs. BIOS Legacy)

    ```bash
    # Si existe /sys/firmware/efi el sistema arrancó en modo UEFI
    if [ -d /sys/firmware/efi ]; then
      echo "Arranque en modo UEFI"
    else
      echo "Arranque en modo BIOS Legacy"
    fi
    ```

    ### Paso 2: Localizar la partición ESP y entradas NVRAM UEFI

    ```bash
    # Mostrar discos, particiones, tipo de sistema de archivos y punto de montaje
    lsblk -o NAME,SIZE,FSTYPE,PARTTYPENAME,MOUNTPOINT

    # Consultar el orden de arranque y rutas .efi en NVRAM (solo en modo UEFI)
    sudo efibootmgr -v
    ```

    **Qué debes observar en UEFI:**
    - Una partición pequeña (habitualmente 100–512 MB) con formato **`vfat` (FAT32)**, tipo `EFI System` y montada en **`/boot/efi`**.
    - En `efibootmgr -v`, verás la variable `BootOrder` y entradas como `\EFI\ubuntu\shimx64.efi` (en MAX/Ubuntu) o `\EFI\Microsoft\Boot\bootmgfw.efi` (en Windows).

    ### Paso 3: Medir tiempos de puesta en marcha con `systemd-analyze`

    ```bash
    # Tiempo total desglosado por fase (en UEFI incluye el tiempo del firmware y bootloader)
    systemd-analyze

    # Los 10 servicios que más tardan en inicializarse durante el arranque
    systemd-analyze blame | head -n 10
    ```

    > En sistemas arrancados en **BIOS Legacy**, `systemd-analyze` no puede medir con precisión la fase `firmware` ni `loader`, por lo que suele empezar directamente en `kernel + userspace`.

    ### Paso 4: Verificación en VirtualBox

    - Con **Habilitar EFI** desactivado en VirtualBox, la VM emula una **BIOS Legacy** clásica (pantalla de texto inicial y tabla de particiones MBR por defecto).
    - Con **Habilitar EFI** activado, la VM muestra el logotipo gráfico de **TianoCore EDK II UEFI** durante el POST, permite entrar al menú UEFI pulsando `Esc` o `F2`, y utiliza discos particionados en **GPT** con partición **ESP**.
