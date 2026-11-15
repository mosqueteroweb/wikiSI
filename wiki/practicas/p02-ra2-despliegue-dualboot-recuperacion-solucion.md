---
title: "Solución Práctica p02 · Despliegue Dual-Boot, Gestión de Paquetes, Arranque y Recuperación"
ra: ["RA2"]
ce: ["RA2.a", "RA2.b", "RA2.c", "RA2.d", "RA2.e", "RA2.f", "RA2.g", "RA2.h", "RA2.i"]
tipo: "practica-solucion"
publicar: false
fuentes:
  - "raw/procesados/ra2-arquitectura-so-licencias.md"
  - "raw/procesados/ra2-virtualizacion-planificacion-instalacion.md"
  - "raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md"
ultima_revision: "2026-11-15"
---

# Guía de Resolución · Práctica 02 (RA2)

> **Estado:** Privada para docente (`publicar: false`). Cambiar a `publicar: true` tras finalizar la entrega en clase si se desea publicar la solución oficial.

---

## Solución Tarea 1 · Arquitectura, Licencias y Planificación (`RA2.a`, `RA2.b`, `RA2.c`, `RA2.d`)

### 1. Elementos funcionales y comparación de arquitecturas (`RA2.a`, `RA2.b`)
- **Interacción funcional:** El hipervisor VirtualBox sobre MAX asigna CPU virtual (`VT-x`/`AMD-V`), RAM (4 GB) y periféricos virtuales (`AHCI`, `82540EM`). El **kernel** del sistema operativo invitado gestiona esa memoria mediante MMU virtualizada y traduce llamadas del espacio de usuario (`ring 3`) a controladores en modo núcleo (`ring 0`). El **sistema de archivos** (`NTFS`/`ext4`) organiza el bloque VDI y la **interfaz** (shell `bash`/`PowerShell` o GUI) entrega el resultado al usuario.
- **Arquitectura:** **Windows 10/11** utiliza un **kernel híbrido** (`ntoskrnl.exe` + subsistema gráfico/ejecutivo integrado con capas bien definidas), mientras **Ubuntu/MAX** utiliza el **kernel Linux monolítico modular**, donde los controladores se cargan dinámicamente en tiempo de ejecución mediante módulos `.ko` (`lsmod`, `modprobe`).

### 2. Matriz comparativa y justificación Puppy Linux (`RA2.c`)
- **Windows 10/11:** Privativa (`EULA` comercial Microsoft). Windows 11 exige TPM 2.0 + UEFI + Secure Boot + 4 GB RAM mínimos.
- **Ubuntu 24.04 LTS:** Software Libre (Linux `GPLv2` + ecosistema MIT/Apache/GPL). Soporte de 5 años, ideal para estación de trabajo/servidor.
- **Linux Mint (Cinnamon/Xfce):** Libre (`GPLv2+`), derivada de Ubuntu/Debian sin Snap por defecto; ágil en equipos de gama media.
- **Puppy Linux:** Libre (`GPLv2+`), diseñada para ejecutarse íntegramente en RAM (SFS comprimido + carga en tmpfs) con escritorio JWM ultraligero (< 300–500 MB en reposo). Por ello opera con absoluta soltura en **`DAM-Rescate-Puppy` (1024 MB RAM)**.

### 3. Verificación SHA-256 y Plan GPT (`RA2.d`)
```bash
cd ~/ISOs/
sha256sum -c --ignore-missing SHA256SUMS
```
Plan GPT sobre 60 GiB: `sda1` ESP (100–300 MiB FAT32), `sda2` MSR (16 MiB), `sda3` Windows `C:` (~29 GiB NTFS), `sda4` WinRE (~550 MiB NTFS), `sda5` Raíz Linux `/` (16 GiB ext4 + `/swapfile`), `sda6` `/home` (~14 GiB ext4).

---

## Solución Tarea 2 · Provisionamiento VirtualBox y Dual-Boot (`RA2.d`, `RA2.e`, `RA2.g`)

```bash
# Creación reproducible desde host MAX
VBoxManage createvm --name "DAM-Estacion-Dual" --ostype "Ubuntu_64" --register
VBoxManage modifyvm "DAM-Estacion-Dual" \
  --memory 4096 --cpus 2 --vram 128 --graphicscontroller vboxsvga \
  --firmware efi --ioapic on --hwvirtex on --nestedpaging on \
  --nic1 nat --nic2 intnet --intnet2 "lan-ra2"

VBoxManage createmedium disk \
  --filename "$HOME/VirtualBox VMs/DAM-Estacion-Dual/DAM-Estacion-Dual.vdi" \
  --size 61440 --format VDI --variant Standard
VBoxManage storagectl "DAM-Estacion-Dual" --name "SATA" --add sata --controller IntelAhci
VBoxManage storageattach "DAM-Estacion-Dual" --storagectl "SATA" --port 0 --device 0 \
  --type hdd --medium "$HOME/VirtualBox VMs/DAM-Estacion-Dual/DAM-Estacion-Dual.vdi"
```

1. **Windows 10 primero:** En instalación personalizada, crear nueva partición de **`30720 MB`** (~30 GiB), finalizar OOBE como `alumdam` y ejecutar en PowerShell Administrador:
   ```powershell
   powercfg /hibernate off
   ```
2. **Snapshot intermedio en MAX:**
   ```bash
   VBoxManage snapshot "DAM-Estacion-Dual" take "Base-Win10-OK"
   ```
3. **Ubuntu 24.04 segundo:** En particionado manual, editar `EFI System Partition` (`/dev/sda1`) seleccionando punto de montaje `/boot/efi` **SIN formatear**, crear `/dev/sda5` (`16384 MB`, `ext4`, `/`) y `/dev/sda6` (`ext4`, `/home`). Tras primer inicio en Ubuntu:
   ```bash
   sudo sed -i 's/^#\?GRUB_DISABLE_OS_PROBER=.*/GRUB_DISABLE_OS_PROBER=false/' /etc/default/grub
   grep -q "GRUB_DISABLE_OS_PROBER" /etc/default/grub || echo "GRUB_DISABLE_OS_PROBER=false" | sudo tee -a /etc/default/grub
   sudo update-grub
   lsblk -f
   ```

---

## Solución Tarea 3 · Personalización y Rescate de GRUB (`RA2.e`, `RA2.f`)

### Configuración `/etc/default/grub` y registro previo
```bash
sudo tee -a /etc/default/grub <<'EOF'
GRUB_DEFAULT=saved
GRUB_SAVEDEFAULT=true
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=7
EOF
sudo update-grub
efibootmgr -v
```

### Snapshot + Simulación + Rescate vía Live ISO y `chroot`
```bash
# En MAX:
VBoxManage snapshot "DAM-Estacion-Dual" take "Pre-Averia-Boot"

# En Ubuntu (anotar BootNum de Windows, ej. 0001, y Ubuntu, ej. 0002):
sudo efibootmgr -o 0001,0002
sudo reboot
```

Tras comprobar que arranca directo Windows, reiniciar con la ISO de Ubuntu (`F12` → DVD → *Try Ubuntu*):
```bash
sudo mount /dev/sda5 /mnt
sudo mount /dev/sda1 /mnt/boot/efi
for d in /dev /dev/pts /proc /sys /sys/firmware/efi/efivars; do
    sudo mount --bind "$d" "/mnt$d"
done
sudo chroot /mnt /bin/bash -c "
  grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu --recheck &&
  update-grub &&
  efibootmgr -v
"
sudo umount -R /mnt
sudo reboot
```

---

## Solución Tarea 4 · Gestión de Paquetes y Salud del Sistema (`RA2.f`, `RA2.h`)

### En Ubuntu (`DAM-Estacion-Dual`)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y htop timeshift

cd /tmp && apt download tree && sudo dpkg -i tree_*.deb && sudo apt install -f -y

# Diferencia remove vs purge:
sudo apt install -y nginx
sudo apt remove -y nginx && ls -ld /etc/nginx   # Conserva /etc/nginx
sudo apt purge -y nginx && ls -ld /etc/nginx    # Elimina /etc/nginx
sudo apt autoremove -y

dpkg --get-selections > ~/paquetes_ubuntu.txt
```

### En Windows 10 (`DAM-Estacion-Dual`, PowerShell Admin)
```powershell
winget install --id 7zip.7zip -e --accept-source-agreements --accept-package-agreements
winget upgrade
winget export -o "$env:USERPROFILE\Desktop\apps_win10.json"

DISM /Online /Cleanup-Image /CheckHealth
sfc /scannow
```

---

## Solución Tarea 5 · Timeshift + Puppy Rescue en `lan-ra2` (`RA2.f`, `RA2.g`)

### 1. Rescate con Timeshift
```bash
sudo timeshift --create --comments "Base limpia RA2" --tags D
mkdir -p ~/Documentos && echo "Proyecto RA2 DAM" > ~/Documentos/entrega_dam.txt
sudo mv /etc/hosts /etc/hosts.bak
sudo timeshift --restore
# Tras reiniciar:
ls -l /etc/hosts && cat ~/Documentos/entrega_dam.txt
```

### 2. Red aislada `lan-ra2` con `DAM-Rescate-Puppy` (1 GB RAM)
- En **`DAM-Estacion-Dual` (Ubuntu)**, sobre la segunda NIC (`enp0s8`, conectada a `lan-ra2`):
  ```bash
  sudo ip addr add 192.168.100.10/24 dev enp0s8
  sudo ip link set enp0s8 up
  ```
- En **`DAM-Rescate-Puppy`**, sobre su NIC (`eth0` en `lan-ra2`):
  ```bash
  ip addr add 192.168.100.30/24 dev eth0
  ip link set eth0 up
  ping -c 4 192.168.100.10
  free -h
  ```
- En **Host MAX**, `free -h` confirmará ~10–11 GB disponibles/caché y las dos VMs consumiendo **5 GB asignados** ($\le 12\text{ GB}$).

---

## Criterios de Corrección para el Docente

1. **Integridad de datos en Dual-Boot (`RA2.d`, `RA2.e`):** Penalizar si el alumno formateó la ESP rompiendo el arranque de Windows o no desactivó *Fast Startup*.
2. **Rescate real vs trampa (`RA2.f`):** Verificar en `VBoxManage snapshot "DAM-Estacion-Dual" list` y en el comando `chroot` que se realizó `grub-install` sin restaurar simplemente el snapshot para saltarse la reparación.
3. **Presupuesto de RAM (`RA2.g`):** Comprobar que `DAM-Estacion-Dual` = `4096 MB` y `DAM-Rescate-Puppy` = `1024 MB` (`5 GB` total).
4. **Rigor documental (`RA2.i`):** El PDF debe permitir replicar el despliegue sin ambigüedades e incluir trazabilidad de todos los comandos y salidas pedidas.
