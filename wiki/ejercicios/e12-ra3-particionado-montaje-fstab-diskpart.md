---
title: "e12 · Particionado GPT, Formateo y Montaje Persistente (fstab vs. DiskPart)"
ra: ["RA3"]
ce: ["RA3.a", "RA3.e"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e12 · Particionado GPT, Formateo y Montaje Persistente (`fstab` vs. `DiskPart`)

<!-- fuente: raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md -->

> **Criterios de Evaluación:** `RA3.a`, `RA3.e` · **Concepto previo:** [Administración de Discos, Particiones, LVM y RAID](../conceptos/ra3-particiones-lvm-raid-administracion-discos.md)

## Objetivo

Añadir un disco duro virtual secundario **VDI** en VirtualBox a las VMs Linux y Windows, inicializarlo con tabla **GPT**, dividirlo en dos particiones con distintos sistemas de archivos (`ext4` + `exFAT` en Linux; `NTFS` + `exFAT` en Windows) y automatizar el montaje persistente en **`/etc/fstab` por UUID** verificando que sobrevive a un reinicio.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e12-Ubuntu`** | Invitado 1 | Ubuntu Desktop 24.04 | **2048 MB (2 GB)** | 2 | 25 GB VDI + **Disco extra 10 GB VDI** |
| **`e12-Win10`** | Invitado 2 | Windows 10 | **4096 MB (4 GB)** | 2 | 40 GB VDI + **Disco extra 10 GB VDI** |

> **Consumo total de VMs activas:** **6 GB** simultáneos sobre 16 GB disponibles (cumple el límite de 10–12 GB).

---

## Enunciado

1. Con ambas VMs apagadas, añade desde VirtualBox (*Configuración → Almacenamiento → Controlador SATA → Añadir disco duro*) un nuevo disco VDI dinámico de **10 GB** a `e12-Ubuntu` y otro a `e12-Win10`.
2. **En `e12-Ubuntu`:**
   - Inicializa el nuevo disco (`/dev/sdb`) como tabla **GPT** con `parted`.
   - Crea 2 particiones primarias de **5 GiB cada una**: la primera formateada en **`ext4`** (etiqueta `DatosLinux`) y la segunda en **`exfat`** (etiqueta `Intercambio`).
   - Monta `DatosLinux` de manera **persistente** en `/mnt/datos` añadiendo su **UUID** a `/etc/fstab`, prueba con `sudo mount -a` y comprueba tras reiniciar que sigue montado.
3. **En `e12-Win10`:**
   - Utilizando **PowerShell** (o `diskpart`), inicializa el disco secundario como **GPT**, crea una partición **`NTFS`** de 5 GB con letra `E:` (etiqueta `TrabajoWin`) y otra **`exFAT`** con el resto del espacio y letra `F:`.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Crear y conectar discos VDI extra desde MAX (opcional CLI con `VBoxManage`)

    ```bash
    # Ejemplo para e12-Ubuntu (VM apagada):
    VBoxManage createmedium disk --filename "$HOME/VirtualBox VMs/e12-Ubuntu/extra10G.vdi" --size 10240 --format VDI
    VBoxManage storageattach "e12-Ubuntu" --storagectl "SATA" --port 1 --device 0 \
      --type hdd --medium "$HOME/VirtualBox VMs/e12-Ubuntu/extra10G.vdi"
    ```

    ---

    ### Paso 2: Particionado GPT y `/etc/fstab` en `e12-Ubuntu`

    ```bash
    # 1. Confirmar el nombre de dispositivo asignado al nuevo disco de 10 GB
    lsblk

    # 2. Crear tabla GPT y dos particiones de ~5 GiB cada una con parted
    sudo parted /dev/sdb --script mklabel gpt \
      mkpart DatosLinux ext4 1MiB 5GiB \
      mkpart Intercambio 5GiB 100%

    # 3. Instalar soporte exFAT si faltara y formatear ambas particiones
    sudo apt update && sudo apt install -y exfatprogs
    sudo mkfs.ext4 -L DatosLinux /dev/sdb1
    sudo mkfs.exfat -n Intercambio /dev/sdb2

    # 4. Consultar el UUID de sdb1 y configurar montaje persistente en /etc/fstab
    sudo blkid /dev/sdb1 /dev/sdb2
    UUID_DATOS=$(sudo blkid -s UUID -o value /dev/sdb1)

    sudo mkdir -p /mnt/datos
    echo "UUID=$UUID_DATOS  /mnt/datos  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab

    # 5. Validar antes de reiniciar (CRÍTICO: si mount -a falla, el próximo arranque puede bloquearse)
    sudo mount -a
    df -Th /mnt/datos
    ```

    Reinicia `e12-Ubuntu` (`sudo reboot`) y verifica de nuevo `lsblk -f` para confirmar que `/dev/sdb1` monta automáticamente en `/mnt/datos`.

    ---

    ### Paso 3: Particionado GPT desde PowerShell en `e12-Win10`

    Abre **PowerShell como Administrador**:

    ```powershell
    # Ver el disco secundario sin inicializar (PartitionStyle = RAW)
    Get-Disk

    # Suponiendo que el disco extra de 10 GB es el Disk Number 1:
    Initialize-Disk -Number 1 -PartitionStyle GPT

    # Partición 1 de 5 GB NTFS con letra E:
    New-Partition -DiskNumber 1 -Size 5GB -DriveLetter E |
      Format-Volume -FileSystem NTFS -NewFileSystemLabel "TrabajoWin" -Confirm:$false

    # Partición 2 con el espacio restante en exFAT con letra F:
    New-Partition -DiskNumber 1 -UseMaximumSize -DriveLetter F |
      Format-Volume -FileSystem exFAT -NewFileSystemLabel "Intercambio" -Confirm:$false

    # Comprobar resultado final
    Get-Volume E, F
    ```
