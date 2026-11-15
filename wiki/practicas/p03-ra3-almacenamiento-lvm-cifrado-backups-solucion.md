---
title: "Solución Práctica p03 · Almacenamiento Elástico (LVM/RAID), Cifrado y Backups"
ra: ["RA3"]
ce: ["RA3.a", "RA3.b", "RA3.c", "RA3.d", "RA3.e", "RA3.f", "RA3.g", "RA3.h"]
tipo: "practica-solucion"
publicar: false
fuentes:
  - "raw/procesados/ra3-sistemas-archivos-directorios-busqueda.md"
  - "raw/procesados/ra3-particiones-volumenes-lvm-raid-cifrado.md"
  - "raw/procesados/ra3-copias-seguridad-automatizacion-tareas.md"
ultima_revision: "2026-11-15"
---

# Guía de Resolución · Práctica 03 (RA3)

> **Estado:** Privada para docente (`publicar: false`).

---

## Solución Tarea 1 · Sistemas de Archivos, Directorios y Enlaces (`RA3.a`, `RA3.b`, `RA3.c`)

```bash
df -Th /
stat /etc/fstab
mkdir -p ~/lab_enlaces && cd ~/lab_enlaces
echo "Manual tecnico" > manual.txt
ln manual.txt manual_duro.txt
ln -s manual.txt manual_simbolico.txt
ls -li
rm manual.txt
cat manual_duro.txt       # Sigue legible: comparte el mismo inodo y contador baja de 2 a 1
cat manual_simbolico.txt  # Falla: apunta al nombre 'manual.txt' eliminado (enlace roto)
```
- `ext4` posee *journaling* (`$JBD2`) para consistencia ante cortes de energía y permisos POSIX; `FAT32` carece de ambos y limita cada fichero a 4 GiB - 1 B.

---

## Solución Tarea 2 · Búsqueda e Inventario (`RA3.d`, `RA3.h`)

```bash
# Ubuntu
find /usr -type f -size +5M 2>/dev/null
grep -rn "UUID=" /etc/fstab
dpkg -l | head -n 15
```

```powershell
# Windows 10
Get-ChildItem -Path "C:\Windows\Logs" -Recurse -Filter "*.log" -ErrorAction SilentlyContinue |
  Where-Object { $_.Length -gt 100KB } |
  Select-Object FullName, Length
winget list | Select-Object -First 15
```

---

## Solución Tarea 3 · LVM, UUID en `fstab` y Cifrado LUKS2 (`RA3.e`, `RA3.h`)

```bash
sudo apt update && sudo apt install -y lvm2 cryptsetup smartmontools

# 1. LVM sobre sdb y sdc
sudo pvcreate /dev/sdb /dev/sdc
sudo vgcreate vg_estudio /dev/sdb /dev/sdc
sudo lvcreate -L 4G -n lv_proyectos vg_estudio
sudo lvcreate -L 3G -n lv_backups vg_estudio

sudo mkfs.ext4 -L ProyectosEstudio /dev/vg_estudio/lv_proyectos
sudo mkfs.ext4 -L BackupsLocales /dev/vg_estudio/lv_backups

sudo mkdir -p /srv/proyectos /mnt/backups_locales
UUID_PROY=$(sudo blkid -s UUID -o value /dev/vg_estudio/lv_proyectos)
UUID_BACK=$(sudo blkid -s UUID -o value /dev/vg_estudio/lv_backups)

echo "UUID=$UUID_PROY /srv/proyectos ext4 defaults,noatime 0 2" | sudo tee -a /etc/fstab
echo "UUID=$UUID_BACK /mnt/backups_locales ext4 defaults,noatime 0 2" | sudo tee -a /etc/fstab
sudo mount -a

# 2. Ampliación en caliente a 6 GB
echo "Entregable v1" | sudo tee /srv/proyectos/entregable.txt
sudo lvextend -L +2G -r /dev/vg_estudio/lv_proyectos
df -h /srv/proyectos

# 3. Cifrado LUKS2 sobre sdd1
sudo parted /dev/sdd --script mklabel gpt mkpart primary ext4 1MiB 100%
sudo cryptsetup luksFormat /dev/sdd1
sudo cryptsetup open /dev/sdd1 cofre_estudio
sudo mkfs.ext4 -L Cofre /dev/mapper/cofre_estudio
sudo mkdir -p /mnt/cofre && sudo mount /dev/mapper/cofre_estudio /mnt/cofre
echo "Secretos de API" | sudo tee /mnt/cofre/secretos.txt
sudo umount /mnt/cofre && sudo cryptsetup close cofre_estudio
sudo blkid /dev/sdd1
```

---

## Solución Tarea 4 · Diagnóstico, `fsck`, `chkdsk` y SSD TRIM (`RA3.e`, `RA3.h`)

```bash
# En Host MAX: sudo smartctl -H /dev/sda (o /dev/nvme0n1)
# En Ubuntu VM:
sudo umount /mnt/backups_locales
sudo fsck -f -y /dev/vg_estudio/lv_backups
sudo mount -a
```

```powershell
# En Windows 10 (Disk 1 es el disco VDI extra de 5 GB):
Initialize-Disk -Number 1 -PartitionStyle GPT
New-Partition -DiskNumber 1 -UseMaximumSize -DriveLetter E |
  Format-Volume -FileSystem NTFS -NewFileSystemLabel "EstudioWin" -Confirm:$false
chkdsk E: /f
Get-PhysicalDisk
```
- **Justificación SSD:** Las unidades flash NAND no tienen cabezal mecánico (acceso aleatorio uniforme); desfragmentarlas desgasta innecesariamente sus ciclos P/E. En su lugar debe ejecutarse **TRIM** (`fstrim` / `Optimize-Volume -ReTrim`) para liberar páginas inválidas.

---

## Solución Tarea 5 · Backups, Restauración y Tareas Programadas (`RA3.f`, `RA3.g`)

```bash
sudo mkdir -p /srv/proyectos/app1 && echo "main(){}" | sudo tee /srv/proyectos/app1/app.c
sudo rsync -avh --delete /srv/proyectos/ /mnt/backups_locales/
sudo tar -czvf /tmp/proyectos_manual.tar.gz -C /srv proyectos
sudo rm /srv/proyectos/app1/app.c
sudo tar -xzvf /tmp/proyectos_manual.tar.gz -C /srv proyectos/app1/app.c

# En crontab de root (sudo crontab -e):
# 0 22 * * * /usr/bin/rsync -avh --delete /srv/proyectos/ /mnt/backups_locales/ >> /var/log/backup_estudio.log 2>&1
```

```powershell
New-Item -ItemType Directory -Force -Path "C:\DatosEstudio" | Out-Null
"Codigo fuente" | Out-File "C:\DatosEstudio\app.txt"
schtasks /create /tn "BackupEstudioWin" /tr "robocopy C:\DatosEstudio E:\CopiaEstudio /MIR /LOG:E:\robocopy.log" /sc DAILY /st 22:00 /f
schtasks /run /tn "BackupEstudioWin"
Get-Content "E:\robocopy.log"
```
- **Estrategia 3-2-1 completa:** A las copias en `/srv/proyectos` (original) y `/mnt/backups_locales/` (copia local) se añadiría una tercera copia enviada por `rsync -e ssh` o nube cifrada (*Restic*/*Borg*) a un NAS remoto o soporte extraíble desconectado (*off-site*).
