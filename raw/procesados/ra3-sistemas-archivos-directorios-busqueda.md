---
id: "raw-ra3-sistemas-archivos-directorios-busqueda"
ra: ["RA3"]
ce: ["RA3.a", "RA3.b", "RA3.c", "RA3.d", "RA3.h"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "Linux Kernel Documentation (Filesystems: ext4, XFS, Btrfs) y man-pages: filesystems(5), hier(7), find(1), locate(1)"
  - "Linux Foundation: Filesystem Hierarchy Standard (FHS 3.0)"
  - "Microsoft Learn: File Systems Overview (NTFS, ReFS, FAT32, exFAT) y PowerShell Get-ChildItem / Select-String"
  - "Documentación oficial de Ubuntu / MAX (EducaMadrid) y Windows 10/11"
---

# Fuente Procesada: Sistemas de Archivos, Estructura de Directorios y Búsqueda de Información

## 1. Anatomía y Comparativa de Sistemas de Archivos (`RA3.a`)

Un **sistema de archivos** (*filesystem*) organiza la secuencia lineal de sectores/bloques de un volumen físico o lógico para almacenar archivos, directorios y metadatos:

- **Estructuras internas en UNIX/Linux:**
  - **Superbloque (*Superblock*):** Almacena geometría del volumen (tamaño de bloque, total de inodos, bloques libres, UUID y tipo de sistema de archivos). Dispone de copias redundantes.
  - **Inodo (*Index Node*):** Registro único por archivo que guarda metadatos (**tipo, permisos, UID/GID, tamaño, marcas temporales `atime/mtime/ctime`, contador de enlaces y punteros/extents hacia los bloques de datos**), **pero NO almacena el nombre del archivo** (el nombre reside en la entrada del directorio que mapea `nombre → nº inodo`).
  - **Extents y Journaling:** `ext4` usa *extents* (rangos contiguos de bloques) reduciendo la fragmentación y un *journal* (diario transaccional) para recuperarse tras apagados bruscos sin escanear todo el disco.
  - **Copy-on-Write (CoW):** Utilizado por **Btrfs** y **ZFS**; en lugar de sobreescribir bloques en sitio, escribe la modificación en bloques libres nuevos y actualiza punteros atómicamente, habilitando *snapshots* instantáneos y comprobación de integridad mediante *checksums*.
- **Estructuras internas en Windows:**
  - **NTFS:** Basado en la **MFT (*Master File Table*)**, donde todo objeto (incluso la propia MFT y `$Bitmap`) es un registro de archivo con atributos, soporte de **ACLs**, cifrado **EFS**, compresión transparente, *journaling* (`$LogFile`) y enlaces simbólicos/duros (`mklink`).
  - **FAT32 / exFAT:** Sin *journaling* ni permisos POSIX/ACL; FAT32 limita el tamaño máximo por archivo a **4 GiB menos 1 byte**, mientras **exFAT** elimina ese límite (hasta 16 EiB teóricos) con máxima compatibilidad cruzada Windows/Linux/macOS para pendrives y tarjetas SD.

## 2. Estructura y Función de los Directorios del Sistema Operativo (`RA3.b`, `RA3.c`)

> Nota curricular oficial: En el diseño oficial de 1º DAM (`0483`), el contenido sobre estructura y función de directorios abarca los criterios `RA3.b` y `RA3.c`.

- **Linux — Estándar FHS 3.0 (*Filesystem Hierarchy Standard*):** Árbol único jerárquico que parte de la raíz `/`:
  - `/bin` y `/usr/bin`: Comandos esenciales de usuario (`ls`, `cp`, `bash`). En Ubuntu/Debian modernos `/bin` es un enlace simbólico a `/usr/bin`.
  - `/sbin` y `/usr/sbin`: Binarios administrativos de sistema (`fdisk`, `mkfs`, `ip`).
  - `/etc`: Archivos de configuración global editables (`fstab`, `netplan`, `hosts`, `passwd`).
  - `/home` y `/root`: Directorios personales de los usuarios estándar y de la cuenta `root`.
  - `/var`: Datos variables (logs en `/var/log`, colas de correo/impresión, caché de `apt` y bases de datos).
  - `/tmp`: Archivos temporales volátiles (limpiados en el arranque, con *Sticky Bit* `1777`).
  - `/usr`: Programas de usuario, librerías compartidas y documentación en solo lectura ordinaria.
  - `/opt`: Aplicaciones adicionales de terceros fuera del gestor estándar.
  - `/boot`: Kernel `vmlinuz`, imagen `initrd.img` y partición ESP montada en `/boot/efi`.
  - `/dev`, `/proc`, `/sys`: Pseudo-sistemas virtuales en memoria para archivos de dispositivo (`sda`, `nvme0n1`, `null`), procesos del kernel y topología de hardware.
  - `/mnt` y `/media`: Puntos de montaje temporales (manuales en `/mnt`, dispositivos extraíbles automáticos en `/media/$USER`).
- **Windows:** Estructura basada en **letras de unidad** (`C:`, `D:`), separador `\` e insensibilidad por defecto a mayúsculas:
  - `C:\Windows` y `System32`: Núcleo, librerías DLL y utilidades del sistema (`SysWOW64` para compatibilidad 32-bit en 64-bit).
  - `C:\Program Files` y `C:\Program Files (x86)`: Software instalado de 64 y 32 bits respectivamente.
  - `C:\ProgramData`: Configuración compartida entre todos los usuarios.
  - `C:\Users\<usuario>` (con `AppData\Local`, `AppData\Roaming` y `Documentos`/`Escritorio`).
- **Enlaces:** **Hard link** (comparte el mismo número de inodo en el mismo sistema de archivos; los datos no se borran hasta eliminar el último enlace) vs **Symbolic link / Soft link** (`ln -s` / `mklink`; fichero puntero por ruta que puede cruzar particiones y romperse si desaparece el destino).

## 3. Búsqueda, Localización e Identificación de Información y Software (`RA3.d`, `RA3.h`)

- **Búsqueda en Linux:**
  - `find <ruta> [criterios]` (en tiempo real por nombre `-name`/`-iname`, tipo `-type f|d`, tamaño `-size +100M`, fecha `-mtime -7`, permisos `-perm`, y acciones `-exec`).
  - `locate` / `plocate` (ultrarrápida sobre índice precompilado con `sudo updatedb`).
  - `grep -rn "patrón" <ruta>` (búsqueda de contenido dentro de archivos).
  - `which`, `whereis`, `type` (localizar ejecutables en `$PATH`, manuales y alias).
  - Identificación de software instalado (`RA3.h`): `dpkg -l`, `apt list --installed`, `snap list`, `flatpak list`.
- **Búsqueda en Windows:**
  - Indexador gráfico del Explorador de archivos (operadores `extensión:`, `tamaño:`, `fecha de modificación:`).
  - PowerShell: `Get-ChildItem -Path C:\ -Recurse -Filter "*.log" -ErrorAction SilentlyContinue`, `Select-String -Pattern "error"`, `where.exe`.
  - Identificación de software instalado (`RA3.h`): `winget list`, `Get-Package`, `Get-AppxPackage`.
