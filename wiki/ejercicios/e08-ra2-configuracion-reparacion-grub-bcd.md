---
title: "e08 · Configuración y Reparación de Arranque Dual-Boot (GRUB2 y BCD)"
ra: ["RA2"]
ce: ["RA2.e", "RA2.f"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e08 · Configuración y Reparación de Arranque Dual-Boot (GRUB2 y BCD)

<!-- fuente: raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md -->

> **Criterios de Evaluación:** `RA2.e`, `RA2.f` · **Concepto previo:** [Gestores de Arranque: GRUB2, Windows BCD y Reparación](../conceptos/ra2-gestores-arranque-grub-bcd.md)

## Objetivo

Personalizar el comportamiento del gestor de arranque **GRUB2**, analizar la tabla NVRAM de UEFI (`efibootmgr`) y el almacén **BCD** de Windows, simular la pérdida del menú GRUB (avería clásica tras una actualización mayor de Windows) y restaurarlo por completo desde un **Live-CD** usando `chroot`.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(12 GB libres)* | Físicas | Red del aula |
| **`e08-DualBoot-Rescue`** | Invitado único (clon de `e07`) | Windows 10 + Ubuntu 24.04 | **4096 MB (4 GB)** | 2 | 60 GB VDI · UEFI · NAT |

> **Consumo total de VMs activas:** **4 GB** de 16 GB disponibles.
>
> **Regla de seguridad previa:** Antes de empezar, crea un **Snapshot** en VirtualBox llamado `Pre-Averia-GRUB`.

---

## Enunciado

1. **Personalización de GRUB2 (`RA2.e`):** Inicia en Ubuntu, edita `/etc/default/grub` para que:
   - El menú sea visible durante **8 segundos** (`GRUB_TIMEOUT=8`).
   - Recuerde automáticamente el último sistema operativo arrancado (`GRUB_DEFAULT=saved` y `GRUB_SAVEDEFAULT=true`).
   - Aplique cambios con `update-grub`.
2. **Auditoría NVRAM y BCD (`RA2.e`, `RA2.f`):** Anota el orden de arranque actual con `efibootmgr -v` desde Ubuntu, y luego reinicia en Windows para inspeccionar su almacén mediante `bcdedit /enum`.
3. **Simulación de avería real (`RA2.f`):** Desde Ubuntu (o cambiando prioridad desde EFI), fuerza a que **Windows Boot Manager** quede primero en `BootOrder` (o elimina temporalmente el directorio `/boot/efi/EFI/ubuntu` tras verificar el snapshot) de modo que al reiniciar el PC entre directo a Windows sin mostrar GRUB.
4. **Rescate desde Live-ISO con `chroot` (`RA2.f`):** Arranca `e08-DualBoot-Rescue` desde la ISO Live de Ubuntu (*Probar Ubuntu*), monta la partición raíz `/` y la partición **ESP** (`/boot/efi`), enlaza los pseudo-sistemas de archivos (`/dev`, `/proc`, `/sys`, `/sys/firmware/efi/efivars`), accede con `chroot` y reinstala **GRUB2** verificando que al reiniciar vuelve el menú dual.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Configuración persistente de GRUB2 en Ubuntu (`RA2.e`)

    ```bash
    # Editar la configuración base de GRUB
    sudo nano /etc/default/grub
    ```

    Asegura que contenga estas directivas:
    ```ini
    GRUB_DEFAULT=saved
    GRUB_SAVEDEFAULT=true
    GRUB_TIMEOUT_STYLE=menu
    GRUB_TIMEOUT=8
    GRUB_DISABLE_OS_PROBER=false
    ```

    Regenera `/boot/grub/grub.cfg` y comprueba las entradas UEFI:
    ```bash
    sudo update-grub
    efibootmgr -v
    ```
    **Ejemplo de salida `efibootmgr -v`:**
    ```text
    BootCurrent: 0002
    BootOrder: 0002,0001,0000
    Boot0001* Windows Boot Manager  HD(1,GPT,...)/File(\EFI\Microsoft\Boot\bootmgfw.efi)
    Boot0002* ubuntu                HD(1,GPT,...)/File(\EFI\ubuntu\shimx64.efi)
    ```

    ### Paso 2: Inspección de BCD en Windows (`RA2.e`)

    Reinicia eligiendo **Windows Boot Manager** en GRUB y abre PowerShell como Administrador:
    ```powershell
    bcdedit /enum firmware
    bcdedit /enum {bootmgr}
    ```
    Comprobarás que `{bootmgr}` apunta a `\EFI\Microsoft\Boot\bootmgfw.efi` cuando Windows gestiona su propio arranque.

    ### Paso 3: Simulación controlada de pérdida de GRUB (`RA2.f`)

    Dentro de Windows (PowerShell Admin), simulamos el cambio de prioridad que a veces provoca una *Feature Update* de Windows poniendo Windows Boot Manager por delante en el firmware, o desde Ubuntu ejecutamos:
    ```bash
    # Ejemplo desde Linux: anteponer Boot0001 (Windows) a Boot0002 (ubuntu)
    sudo efibootmgr -o 0001,0002
    sudo reboot
    ```
    *(Al reiniciar, el equipo entrará directamente en Windows sin mostrar el menú de Ubuntu.)*

    ### Paso 4: Reparación completa desde Ubuntu Live ISO (`RA2.f`)

    1. Apaga la VM, inserta la ISO de Ubuntu Desktop en el DVD de VirtualBox y arranca pulsando **`F12`** para elegir el arranque desde DVD, seleccionando **Probar Ubuntu** (*Try Ubuntu*).
    2. Abre una terminal en el entorno Live y localiza tus particiones:

    ```bash
    lsblk -f
    # Supongamos: /dev/sda1 -> vfat (ESP) y /dev/sda5 -> ext4 (raíz /)
    ```

    3. Monta el sistema instalado, su partición EFI y los directorios virtuales del kernel:

    ```bash
    # Montar raíz y partición EFI
    sudo mount /dev/sda5 /mnt
    sudo mount /dev/sda1 /mnt/boot/efi

    # Enlazar dispositivos y variables EFI del kernel activo del Live-USB
    for d in /dev /dev/pts /proc /sys /sys/firmware/efi/efivars; do
        sudo mount --bind "$d" "/mnt$d"
    done

    # Entrar en el sistema instalado con chroot
    sudo chroot /mnt
    ```

    4. Dentro del entorno `chroot` (el prompt ya pertenece a tu Ubuntu instalado), reinstala GRUB en la ESP y regenera el menú:

    ```bash
    grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu --recheck
    update-grub
    efibootmgr -v   # Verifica que 'ubuntu' vuelve a encabezar BootOrder
    exit
    ```

    5. Desmonta limpiamente y reinicia extrayendo la ISO:

    ```bash
    sudo umount -R /mnt
    sudo reboot
    ```

    Al arrancar nuevamente desde disco duro, volverá a aparecer el menú **GRUB2** con sus 8 segundos de espera y recordando la última entrada elegida.
