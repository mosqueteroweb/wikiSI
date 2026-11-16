---
title: "e07 · Planificación e Instalación Dual-Boot Windows + Ubuntu en UEFI/GPT"
ra: ["RA2"]
ce: ["RA2.d", "RA2.e", "RA2.g"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra2-virtualizacion-planificacion-instalacion.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e07 · Planificación e Instalación Dual-Boot Windows + Ubuntu en UEFI/GPT

<!-- fuente: raw/procesados/ra2-virtualizacion-planificacion-instalacion.md -->

> **Criterios de Evaluación:** `RA2.d`, `RA2.e`, `RA2.g` · **Concepto previo:** [Planificación, Particionado GPT/UEFI e Instalación Dual-Boot](../conceptos/ra2-planificacion-instalacion-dual-boot.md)

## Objetivo

Planificar el esquema de particiones sobre tabla **GPT** y firmware **UEFI**, instalar primero **Windows 10/11** reduciendo su partición sin pérdida de datos y desplegar después **Ubuntu 24.04 LTS** en el mismo disco virtual manteniendo una única partición **ESP (EFI)** compartida.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(12 GB libres)* | Físicas | Red del aula |
| **`e07-DualBoot-Lab`** | Invitado único | Windows 10 + Ubuntu 24.04 | **4096 MB (4 GB)** | 2 | **60 GB VDI** · UEFI · NAT |

> **Consumo total de VMs activas:** **4 GB** de 16 GB disponibles (cumple holgadamente el tope de 10–12 GB en aula).

---

## Enunciado

1. **Planificación del disco (`RA2.d`):** Diseña sobre un disco **VDI de 60 GiB** con tabla **GPT** el reparto de particiones para albergar Windows 10 (30 GiB) y Ubuntu Desktop (30 GiB con `/` y `/home` separados + *swap* en archivo).
2. **Instalación de Windows primero (`RA2.e`):** Crea la VM `e07-DualBoot-Lab` con **UEFI habilitado** (`--firmware efi`), arranca el instalador de Windows 10, crea manualmente un volumen de **~30 GiB** para Windows dejando los otros **30 GiB Sin asignar** (*Unallocated Space*) y finaliza la fase OOBE con cuenta local `alumdam`.
3. **Preparación segura antes de Linux (`RA2.d`):** Dentro de Windows, desactiva el **Inicio Rápido** (*Fast Startup*) para evitar que la partición NTFS quede bloqueada en modo hibernación.
4. **Instalación de Ubuntu en segundo lugar (`RA2.e`):** Arranca la VM con la ISO de Ubuntu Desktop, elige **Instalación manual (*Algo más*)** y crea `/` (`16 GiB`, `ext4`) y `/home` (`~14 GiB`, `ext4`), seleccionando la **ESP existente de Windows** como punto de montaje `/boot/efi` **SIN formatearla**.
5. **Verificación posinstalación (`RA2.e`, `RA2.g`):** Comprueba tras reiniciar que aparece el menú de GRUB ofreciendo Ubuntu y Windows Boot Manager, y documenta `lsblk -f` desde Ubuntu.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Plan de particionado GPT sobre 60 GiB (`RA2.d`)

    | Partición | Tamaño aprox. | Formato | Punto de montaje / Uso | ¿Se formatea al instalar Ubuntu? |
    | :--- | :---: | :---: | :--- | :---: |
    | `/dev/sda1` | 100–300 MiB | **FAT32** | **ESP** (`/boot/efi`) compartida | **NO** (conservar cargador de Windows) |
    | `/dev/sda2` | 16 MiB | *(raw)* | **MSR** (*Microsoft Reserved*) | NO |
    | `/dev/sda3` | ~29 GiB | **NTFS** | `C:` Sistema Windows 10 | NO |
    | `/dev/sda4` | ~550 MiB | **NTFS** | WinRE (Recuperación Windows) | NO |
    | `/dev/sda5` | 16 GiB | **ext4** | Raíz Linux **`/`** (con `/swapfile` de 2 GB) | **SÍ** |
    | `/dev/sda6` | ~14 GiB | **ext4** | Datos de usuario **`/home`** | **SÍ** |

    ### Paso 2: Instalación de Windows y desactivación de Fast Startup (`RA2.e`)

    1. En la pantalla *"¿Dónde quieres instalar Windows?"* del instalador de Windows 10, pulsa **Nuevo**, indica **`30720` MB** (30 GiB) y acepta. Windows creará automáticamente la **ESP**, **MSR**, la partición principal (`~29,4 GiB`) y **WinRE**, dejando casi **30 GiB de espacio sin asignar** al final del disco.
    2. Finaliza la instalación hasta entrar al escritorio de Windows.
    3. Abre **PowerShell como Administrador** y desactiva la hibernación / *Fast Startup*:

    ```powershell
    # Desactivar hibernación (deshabilita automáticamente Fast Startup y libera hiberfil.sys)
    powercfg /hibernate off

    # Comprobar estado de particiones GPT antes de pasar a Ubuntu
    Get-Partition | Format-Table DiskNumber, PartitionNumber, DriveLetter, Type, @{N="GB";E={[math]::Round($_.Size/1GB,2)}}
    ```

    ### Paso 3: Instalación manual de Ubuntu respetando la ESP (`RA2.e`)

    1. Apaga Windows completamente (*Inicio → Apagar*, no suspender).
    2. En VirtualBox (*Configuración → Almacenamiento*), inserta `ubuntu-24.04-desktop-amd64.iso` en la unidad óptica y asegúrate en *Sistema → Orden de arranque* de arrancar desde Óptica en UEFI (o pulsa `F12` al inicio de VirtualBox).
    3. En el instalador de Ubuntu, selecciona **Instalación manual** (opción *"Más opciones"*):
       - Localiza la partición `EFI System Partition` existente (~100 MB FAT32, `/dev/sda1`): pulsa *Cambiar*, asegúrate de usarla como **Partición del sistema EFI** (`/boot/efi`) y **verifica que la casilla Formatear está DESMARCADA**.
       - Sobre el espacio libre (*Free space* de ~30 GiB), crea:
         - Partición primaria **16384 MB**, sistema **Ext4 transaccional**, punto de montaje **`/`** (marcar *Formatear*).
         - Partición primaria con el espacio restante (~14000 MB), sistema **Ext4 transaccional**, punto de montaje **`/home`** (marcar *Formatear*).
       - En *"Dispositivo donde instalar el cargador de arranque"*, selecciona el disco raíz (`/dev/sda`) o su partición EFI.
    4. Completa el asistente (zona horaria `Madrid`, teclado `Español`, usuario `alumdam`) y reinicia retirando la ISO cuando el instalador lo solicite.

    ### Paso 4: Comprobación de GRUB y tabla final (`RA2.e`, `RA2.g`)

    Al reiniciar debe aparecer **GNU GRUB** con las entradas `Ubuntu` y `Windows Boot Manager (on /dev/sda1)`. Si Windows no aparece a la primera, en Ubuntu 24.04 activa `os-prober`:

    ```bash
    # Habilitar detección de otros SO si faltara Windows en el menú
    echo "GRUB_DISABLE_OS_PROBER=false" | sudo tee -a /etc/default/grub
    sudo update-grub

    # Documentar el esquema de particionado resultante
    lsblk -f
    ```

    **Salida verificable de `lsblk -f`:**
    ```text
    NAME   FSTYPE FSVER LABEL UUID                                 MOUNTPOINTS
    sda
    ├─sda1 vfat   FAT32       4A1B-9F20                            /boot/efi
    ├─sda2
    ├─sda3 ntfs               8C92A4...
    ├─sda4 ntfs               104E2B...
    ├─sda5 ext4   1.0         d73f9a...                            /
    └─sda6 ext4   1.0         a42c11...                            /home
    ```
    Con `/boot/efi` montado en `sda1`, `/` en `sda5` y `/home` en `sda6` y Windows intacto en `sda3`, el despliegue dual-boot queda verificado.

    ### Paso 5 (Ampliación): Despliegue Multi-SO (2 Windows + 2 Linux) y Cuenta Local en Windows 11

    Si quieres llevar la práctica al escenario avanzado de clase (**4 sistemas operativos en el mismo disco UEFI/GPT**):

    1. **Activa siempre EFI** en VirtualBox (`Sistema` → `Placa base` → `Habilitar EFI`) antes de crear las particiones.
    2. **Prepara las imágenes en USB multiarranque** con [Ventoy](https://ventoy.net/en/doc_start.html) si trabajas en equipo físico, o adjunta las ISOs secuencialmente en VirtualBox.
    3. **En Windows 11 en VM:** cuando pida cuenta Microsoft en el asistente OOBE, pulsa `Shift + F10`, ejecuta `start ms-cxh:localonly` y da de alta la cuenta local con tu nombre.
    4. **Instala siempre Windows antes que Linux** (y una distribución ligera como *Puppy Linux*, *Linux Mint* o *Ubuntu* al final) para que **GNU GRUB** detecte las dos entradas de Windows y ambas distribuciones Linux de forma limpia. Si se mueve o importa el `.ova` en los PCs del aula, verifica después `efibootmgr -v`.
