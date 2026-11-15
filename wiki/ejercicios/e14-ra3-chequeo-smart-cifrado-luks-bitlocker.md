---
title: "e14 · Chequeo SMART, Reparación Lógica (fsck/chkdsk), TRIM y Cifrado LUKS/BitLocker"
ra: ["RA3"]
ce: ["RA3.e", "RA3.h"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e14 · Chequeo SMART, Reparación Lógica (`fsck`/`chkdsk`), TRIM y Cifrado `LUKS` / `BitLocker`

<!-- fuente: raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md -->

> **Criterios de Evaluación:** `RA3.e`, `RA3.h` · **Concepto previo:** [Diagnóstico, Chequeo, TRIM y Cifrado de Discos](../conceptos/ra3-chequeo-desfragmentacion-cifrado-discos.md)

## Objetivo

Evaluar el estado de salud físico de unidades reales mediante **SMART**, comprobar y reparar estructuras lógicas de almacenamiento con **`fsck`** y **`chkdsk`**, aplicar **TRIM** correctamente en unidades SSD y crear un volumen cifrado en reposo con **LUKS2** (`cryptsetup`) y consultar la protección **BitLocker** en Windows.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Discos / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e14-Ubuntu`** | Invitado 1 | Ubuntu 24.04 | **2048 MB (2 GB)** | 2 | 25 GB VDI + Disco 4 GB VDI (`/dev/sdb`) |
| **`e14-Win10`** | Invitado 2 | Windows 10 Pro | **4096 MB (4 GB)** | 2 | 40 GB VDI + Disco 4 GB VDI (`E:`) |

> **Consumo total de VMs activas:** **6 GB** simultáneos sobre 16 GB disponibles (cumple el límite de 10–12 GB).

---

## Enunciado

1. **Diagnóstico físico SMART en Host MAX (`RA3.h`):** Comprueba desde una terminal del equipo anfitrión **MAX** (las VMs VirtualBox emulan controladores sin atributos SMART físicos completos) el estado de salud del SSD/HDD físico del ordenador de clase usando `smartctl -H`.
2. **Chequeo lógico y TRIM en `e14-Ubuntu` (`RA3.e`, `RA3.h`):** Particiona y formatea `/dev/sdb1` en `ext4`, realiza una verificación segura **desmontada** con `fsck -f` y comprueba la programación automática del servicio `fstrim.timer`.
3. **Cifrado de volumen con LUKS2 en `e14-Ubuntu` (`RA3.e`):** Cifra `/dev/sdb1` con **`cryptsetup luksFormat`**, ábrelo bajo el nombre `boveda_dam`, crea un sistema `ext4` dentro de `/dev/mapper/boveda_dam`, guarda un archivo secreto `claves.txt`, desmonta, cierra el contenedor y demuestra qué ocurre al intentar montar `/dev/sdb1` directamente sin descifrarlo.
4. **Chequeo `chkdsk` y BitLocker en `e14-Win10` (`RA3.e`, `RA3.h`):** Abre PowerShell como Administrador, verifica la unidad de datos `E:` con `chkdsk E: /f`, consulta `Get-PhysicalDisk` y verifica el estado de soporte BitLocker (`manage-bde -status`).

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Comprobación SMART real en el anfitrión MAX

    ```bash
    # En terminal del equipo físico MAX (instalar smartmontools si es necesario)
    sudo apt update && sudo apt install -y smartmontools

    # Identificar el disco principal (ej. /dev/nvme0n1 o /dev/sda)
    lsblk -d -o NAME,SIZE,MODEL,TRAN

    # Consultar veredicto general SMART (debe decir PASSED)
    sudo smartctl -H /dev/sda
    ```

    ---

    ### Paso 2: Chequeo `fsck` seguro y `TRIM` en `e14-Ubuntu`

    ```bash
    # Formatear partición de prueba /dev/sdb1
    sudo parted /dev/sdb --script mklabel gpt mkpart primary ext4 1MiB 100%
    sudo mkfs.ext4 /dev/sdb1

    # NUNCA ejecutar fsck en RW estando montada; verificar primero con lsblk que está desmontada:
    sudo fsck -f -v /dev/sdb1

    # Verificar temporizador systemd de TRIM para SSDs
    systemctl status fstrim.timer
    sudo fstrim -av
    ```

    ---

    ### Paso 3: Cifrado de disco completo sobre `/dev/sdb1` con `LUKS2`

    ```bash
    sudo apt install -y cryptsetup

    # 1. Inicializar cabecera cifrada LUKS2 (pedirá confirmar YES en mayúsculas y una frase de paso)
    sudo cryptsetup luksFormat /dev/sdb1

    # 2. Abrir el contenedor descifrado como /dev/mapper/boveda_dam
    sudo cryptsetup open /dev/sdb1 boveda_dam

    # 3. Formatear y usar el volumen descifrado
    sudo mkfs.ext4 -L BovedaDAM /dev/mapper/boveda_dam
    sudo mkdir -p /mnt/boveda
    sudo mount /dev/mapper/boveda_dam /mnt/boveda
    echo "Contenido confidencial cifrado con AES-XTS" | sudo tee /mnt/boveda/claves.txt

    # 4. Cerrar de forma segura
    sudo umount /mnt/boveda
    sudo cryptsetup close boveda_dam

    # 5. Demostración de protección: intentar leer o montar el dispositivo en crudo falla
    sudo blkid /dev/sdb1       # TYPE="crypto_LUKS"
    sudo mount /dev/sdb1 /mnt/boveda   # Fallará: sistema de archivos desconocido ('crypto_LUKS')
    ```

    ---

    ### Paso 4: Reparación lógica y verificación BitLocker en `e14-Win10`

    Abre **PowerShell como Administrador**:

    ```powershell
    # Salud física reportada al SO y optimización de disco
    Get-PhysicalDisk | Format-Table FriendlyName, MediaType, HealthStatus

    # Comprobación y reparación lógica NTFS en disco adicional E:
    chkdsk E: /f

    # Consultar estado de cifrado BitLocker en todos los volúmenes
    manage-bde -status
    # Nota: En VMs sin TPM virtual activado, BitLocker puede habilitarse en unidades de datos (E:)
    # con protector de contraseña: Enable-BitLocker -MountPoint "E:" -EncryptionMethod XtsAes256 -PasswordProtector
    ```
