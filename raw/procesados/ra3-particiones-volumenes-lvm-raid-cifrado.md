---
id: "raw-ra3-particiones-volumenes-lvm-raid-cifrado"
ra: ["RA3"]
ce: ["RA3.e", "RA3.h"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "man-pages Linux: lsblk(8), blkid(8), parted(8), fstab(5), lvm(8), mdadm(8), cryptsetup(8), fsck(8), smartctl(8), fstrim(8)"
  - "Red Hat / Ubuntu Documentation: Logical Volume Manager (LVM), Software RAID, LUKS Disk Encryption"
  - "Microsoft Learn: DiskPart, Storage Spaces, chkdsk, Optimize-Volume, BitLocker & manage-bde"
---

# Fuente Procesada: Particiones, Volúmenes Lógicos (LVM), RAID, Diagnóstico y Cifrado

## 1. Administración de Discos, Particiones y Montaje Persistente (`RA3.e`)

- **Identificación de dispositivos en Linux:** `lsblk -f`, `sudo blkid`, `sudo parted -l`, `sudo fdisk -l`.
- **Creación de tabla GPT y particiones:**
  - CLI interactiva/scripting: `parted /dev/sdb mklabel gpt`, `parted -a optimal /dev/sdb mkpart primary ext4 0% 100%`, `gdisk` o `cfdisk`.
  - GUI estándar en MAX/Ubuntu: **GParted** o **Discos** (`gnome-disks`).
  - Formateo: `mkfs.ext4 -L Datos`, `mkfs.vfat -F 32`, `mkfs.exfat`, `mkfs.ntfs -Q`.
- **Montaje temporal vs persistente:** `mount /dev/sdb1 /mnt/datos` es temporal; para persistir tras reiniciar se añade la entrada al fichero **`/etc/fstab`** utilizando el **UUID** del sistema de archivos (`UUID=... /mnt/datos ext4 defaults,noatime 0 2`) para evitar fallos si cambia la letra `/dev/sdX`, probando antes de reiniciar con `sudo mount -a`.
- **Windows:** GUI `diskmgmt.msc` (*Administración de discos*), CLI `diskpart` (`list disk`, `select disk`, `convert gpt`, `create partition primary`, `format fs=ntfs quick`, `assign letter=E`), y PowerShell módulo `Storage` (`Get-Disk`, `Initialize-Disk`, `New-Partition`, `Format-Volume`).

## 2. Volúmenes Lógicos (`LVM`) vs Discos Dinámicos y *Storage Spaces* (`RA3.e`, `RA3.h`)

- **LVM (Logical Volume Manager)** desacopla las particiones físicas de los puntos de montaje permitiendo redimensionar en caliente y agrupar discos:
  1. **PV (*Physical Volume*):** Disco o partición tipo LVM inicializada con `pvcreate /dev/sdb1`.
  2. **VG (*Volume Group*):** Pool agregado de capacidad creado con `vgcreate vg_datos /dev/sdb1 /dev/sdc1`.
  3. **LV (*Logical Volume*):** Unidad virtual equivalente a una partición lógica tradicional creada con `lvcreate -L 10G -n lv_proyectos vg_datos` (accesible en `/dev/vg_datos/lv_proyectos`).
  4. **Extensión en caliente:** `vgextend vg_datos /dev/sdd1` seguido de `lvextend -L +5G -r /dev/vg_datos/lv_proyectos` (el parámetro `-r` redimensiona automáticamente el sistema de archivos `ext4`/`xfs` sin desmontar).
- **Windows:** Conceptos equivalentes en volúmenes distribuidos/seccioandos (*Spanned*, *Striped*) mediante Discos Dinámicos (legado) o **Espacios de Almacenamiento (*Storage Spaces*)** modernos.

## 3. Matrices RAID por Software y Hardware (`RA3.e`, `RA3.h`)

| Nivel | Nombre | Discos mín. | Capacidad útil | Tolerancia fallos | Uso típico |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **RAID 0** | *Striping* (División) | 2 | $N \times C$ (100 %) | **0 discos** (alto riesgo) | Caché temporal, vídeo no crítico |
| **RAID 1** | *Mirroring* (Espejo) | 2 | $1 \times C$ (50 %) | 1 disco (de 2) | Arranque de servidores, datos críticos |
| **RAID 5** | Paridad distribuida | 3 | $(N-1) \times C$ | 1 disco | Archivos generales, equilibrio coste/seguridad |
| **RAID 6** | Doble paridad | 4 | $(N-2) \times C$ | 2 discos | Cabinas grandes HDD |
| **RAID 10** | Espejos en *Stripe* | 4 (pares) | $(N/2) \times C$ (50 %) | 1 por cada par | Bases de datos intensivas IOPS |

- **Implementación en Linux (`mdadm`):** `sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1`, monitorizado en `/proc/mdstat` y guardado en `/etc/mdadm/mdadm.conf`. *Nota pedagógica:* **RAID proporciona disponibilidad, NO sustituye a las copias de seguridad** (si borras un archivo accidentalmente o entra ransomware, se replica instantáneamente en todos los discos del RAID).

## 4. Chequeo, Desfragmentación / TRIM y Cifrado (`RA3.e`, `RA3.h`)

- **Chequeo de integridad:**
  - Linux: `sudo umount /dev/sdb1 && sudo fsck -f -y /dev/sdb1` (nunca ejecutar `fsck` en modo escritura sobre una partición montada).
  - Windows: `chkdsk E: /f` (reparar estructura lógica) o `/r` (localiza sectores defectuosos). En `C:` programa la revisión para el siguiente reinicio.
- **Salud SMART:** `sudo smartctl -H /dev/sda` y `smartctl -a` (`smartmontools`) para leer sectores reasignados, temperatura y horas de encendido.
- **Desfragmentación (HDD) vs TRIM (SSD):** Los HDD requieren ocasionalmente reducir fragmentación (`e4defrag` / `defrag` o *Optimizar unidades*); los **SSD NO deben desfragmentarse** para no agotar ciclos de escritura NAND, sino enviar comandos **TRIM** (`sudo fstrim -av` / `fstrim.timer` o `Optimize-Volume -DriveLetter C -ReTrim`).
- **Cifrado de volúmenes:**
  - **LUKS2 (`cryptsetup`) en Linux:** `sudo cryptsetup luksFormat /dev/sdb1`, `sudo cryptsetup open /dev/sdb1 datos_seguros` $\rightarrow$ `/dev/mapper/datos_seguros`.
  - **BitLocker (`manage-bde`) en Windows:** Cifra particiones enteras apoyándose en chip **TPM 2.0** (o clave de recuperación USB/AD).
