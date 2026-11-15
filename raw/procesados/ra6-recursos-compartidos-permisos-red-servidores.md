---
tema: "Recursos Compartidos en Red, Permisos Efectivos, Samba/SMB, NFS, Impresión CUPS y Servidores de Aplicaciones"
ra: RA6
ce:
  - RA6.a
  - RA6.b
  - RA6.c
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA6 (1/3) · Recursos Compartidos en Red y Servidores

## 1. Permisos de Acceso a Recursos Locales vs. Recursos de Red (`RA6.a`, `RA6.b`)

- **Diferencia clave en Windows y Samba:**
  - Al acceder **localmente**, solo intervienen los **permisos del sistema de archivos (NTFS en Windows / POSIX+ACLs en Linux)**.
  - Al acceder **en red (SMB / CIFS)**, el sistema aplica la **intersección más restrictiva** entre:
    1. **Permisos de recurso compartido (*Share Permissions*):** ej. `Control total`, `Cambiar` (*Change*), `Leer` (*Read*).
    2. **Permisos subyacentes del sistema de archivos (NTFS / POSIX + ACLs).**
  - Buena práctica estándar en Windows Server y Samba: conceder `Cambiar` (o `Control total`) a `Usuarios autentificados` en la capa de **recurso compartido** y gestionar el detalle granular de carpetas y grupos en los **permisos NTFS / POSIX** (o limitar explícitamente `valid users = @grupo` + `read list`/`write list` en Samba).

## 2. Protocolos y Servidores de Ficheros (`RA6.c`)

- **SMB / CIFS (`445/TCP`) con Samba (Linux) o Compartición Windows:**
  - Archivo de configuración principal: `/etc/samba/smb.conf` (validar siempre con `testparm -s`).
  - Los usuarios del sistema Linux deben añadirse además a la base de credenciales SMB mediante `sudo smbpasswd -a <usuario>`.
  - Parámetros clave en recurso compartido: `path`, `valid users`, `read only = no` / `writable = yes`, `create mask = 0660`, `directory mask = 0770`, `force group`.
  - Desde clientes: `smbclient -L //<ip> -U <user>`, `mount -t cifs //<ip>/<recurso> /mnt/... -o credentials=/etc/samba/creds` en Linux; `net use Z: \\<ip>\<recurso> /persistent:yes` o `New-SmbShare` en Windows PowerShell.
- **NFS (*Network File System*, `2049/TCP` en NFSv4):**
  - Estándar nativo Unix/Linux de alto rendimiento (`nfs-kernel-server`), configurado en `/etc/exports` (ej. `/srv/nfs_dam 192.168.50.0/24(rw,sync,no_subtree_check,root_squash)`).
  - La opción **`root_squash`** (por defecto y obligatoria en seguridad) mapea el `UID 0` remoto del cliente al usuario sin privilegios `nobody`, impidiendo que un cliente con acceso `root` local tome control del servidor exportado. Recargar con `sudo exportfs -ra`.

## 3. Servidores de Impresión y Aplicaciones (`RA6.c`)

- **Servidor de Impresión:** **CUPS (*Common Unix Printing System*, puerto `631/TCP`, protocolo IPP/IPPS)** en Linux con administración web en `https://localhost:631` y CLI `lpstat -p`, `lpadmin`, `cupsctl`; en Windows **Print Management** / Cola de impresión (`Spooler`, puerto LPD o IPP y compartición SMB `\\servidor\impresora`).
- **Servidores de Aplicaciones y Contenedores en Red:** servicios web/API y servidores de aplicaciones Java/Python (`Nginx` como proxy inverso `80/443`, `Apache Tomcat` / `Spring Boot` en `8080`, `PostgreSQL` en `5432`) gestionando puertos de escucha (`0.0.0.0`), pools de procesos/hilos y permisos mínimos para el usuario del demonio (`www-data`, `tomcat`).
