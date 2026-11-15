---
id: "raw-ra2-arranque-aplicaciones-recuperacion-doc"
ra: ["RA2"]
ce: ["RA2.e", "RA2.f", "RA2.h", "RA2.i"]
nivel_credibilidad: "Nivel 1"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "GNU GRUB Manual 2.x & Ubuntu Community Help Wiki: Grub2 / Boot-Repair"
  - "Microsoft Learn: bcdedit, bcdboot, WinRE, SFC, DISM, Winget CLI"
  - "Debian Administrator's Handbook & Ubuntu Docs: dpkg, apt, snap"
  - "Timeshift / Linux Mint Backup & System Restore Documentation"
---

# Fuente Procesada: Gestores de Arranque, Aplicaciones, Recuperación y Documentación

## 1. Gestores de Arranque: GRUB 2 y BCD (`RA2.e`, `RA2.f`)

- **GRUB 2 (GNU GRand Unified Bootloader):**
  - Archivo de configuración principal editado por el administrador: `/etc/default/grub` (`GRUB_DEFAULT`, `GRUB_TIMEOUT`, `GRUB_DISABLE_OS_PROBER=false`, `GRUB_CMDLINE_LINUX_DEFAULT`).
  - Tras modificar `/etc/default/grub`, es obligatorio regenerar `/boot/grub/grub.cfg` con `sudo update-grub`.
  - **Reparación desde Live ISO (UEFI):**
    1. Montar partición raíz (`/mnt`) y partición EFI (`/mnt/boot/efi`).
    2. Montar sistemas virtuales enlazados (`--bind /dev`, `/proc`, `/sys`, `/sys/firmware/efi/efivars`).
    3. Hacer `chroot /mnt`, ejecutar `grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu` y `update-grub`.
- **Windows Boot Manager (`BCD` — *Boot Configuration Data*):**
  - Almacén binario editado con `bcdedit` desde PowerShell/CMD con privilegios de administrador (`bcdedit /enum`, `bcdedit /timeout 10`).
  - **Reparación desde Entorno de Recuperación WinRE:**
    - `bootrec /scanos` / `bootrec /rebuildbcd` (Legacy/general).
    - En **UEFI/GPT**, reconstrucción fiable mediante `bcdboot C:\Windows /s S: /f UEFI` (siendo `S:` la letra asignada temporalmente con `diskpart` a la partición EFI FAT32).

## 2. Gestión de Aplicaciones y Paquetes (`RA2.h`)

- **Ecosistema Debian / Ubuntu / MAX / Linux Mint:**
  - **Bajo nivel (`dpkg`):** Instala o inspecciona ficheros `.deb` locales (`sudo dpkg -i paquete.deb`, `dpkg -l`, `sudo dpkg --configure -a`), pero no descarga dependencias externas.
  - **Alto nivel (`apt`):** Consulta índices en `/etc/apt/sources.list` y `/etc/apt/sources.list.d/`, resuelve árbol de dependencias y descarga desde repositorios firmados:
    - `sudo apt update` (actualiza catálogo de paquetes).
    - `sudo apt upgrade` / `sudo apt full-upgrade` (instala actualizaciones).
    - `sudo apt install <pkg>` / `sudo apt remove <pkg>` / `sudo apt purge <pkg>` (borra también ficheros de configuración) / `sudo apt autoremove` (limpia dependencias huérfanas).
    - `sudo apt --fix-broken install` (repara dependencias rotas tras un `dpkg -i` manual).
  - **Formatos universales aislados:** **Snap** (`snap install`), **Flatpak** (`flatpak install`, muy integrado en Linux Mint) y **AppImage** (ejecutable portátil único sin instalación en sistema).
- **Ecosistema Windows 10 / 11:**
  - Instaladores tradicionales `.exe` (propios) y `.msi` (Windows Installer: `msiexec /i paquete.msi /qn`).
  - **Winget (*Windows Package Manager*):** Gestor oficial CLI de Microsoft integrado en Windows 10/11:
    - `winget search <app>`, `winget install --id <ID> -e`, `winget upgrade --all`, `winget uninstall <ID>`, `winget export -o apps.json` / `winget import -i apps.json`.

## 3. Actualización, Recuperación y Documentación (`RA2.f`, `RA2.i`)

- **Estrategia escalonada de recuperación:**
  1. **VirtualBox Snapshots:** Reversión instantánea de VM en laboratorio.
  2. **Puntos de control de SO:** **Timeshift** en Linux (instantáneas `RSYNC` o `BTRFS` del sistema excluyendo datos de usuario por defecto) y **Puntos de Restauración** en Windows.
  3. **Reparación de integridad del sistema sin pérdida de datos:**
     - Linux: `sudo dpkg --configure -a` + `sudo apt --fix-broken install`.
     - Windows: `DISM /Online /Cleanup-Image /RestoreHealth` (repara almacén de componentes) seguido de `sfc /scannow` (comprueba y sustituye ficheros protegidos del sistema dañados).
  4. **Rescate externo:** Live USB Ubuntu/Puppy Linux o medio de instalación WinRE.
- **Documentación de instalación e incidencias (`RA2.i`):**
  - Todo despliegue debe generar un acta técnica registrando: datos del equipo/VM, edición y hash SHA-256 de la ISO, esquema de particiones, software instalado, cuentas/servicios base y una **bitácora de incidencias** (síntoma, causa raíz, solución aplicada y verificación).
