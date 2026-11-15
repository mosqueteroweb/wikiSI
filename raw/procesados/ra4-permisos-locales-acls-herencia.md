---
id: "raw-ra4-permisos-locales-acls-herencia"
ra: ["RA4"]
ce: ["RA4.d", "RA4.e"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "man-pages Linux: chmod(1), chown(1), umask(2), acl(5), getfacl(1), setfacl(1)"
  - "Microsoft Learn: File and Folder Permissions (NTFS), icacls, PowerShell Get-Acl / Set-Acl"
---

# Fuente Procesada: Permisos Locales, Bits Especiales y Listas de Control de Acceso (ACL)

## 1. Modelo Clásico POSIX en GNU/Linux (`chmod`, `chown`, `umask`) (`RA4.d`)

Cada archivo o directorio pertenece a **un usuario propietario (`u`)** y **un grupo propietario (`g`)**, quedando el resto del sistema englobado como **otros (`o`)**:
- **Permisos básicos:** Lectura (`r = 4`), Escritura (`w = 2`), Ejecución (`x = 1`).
  - En **ficheros regulares**: `r` permite leer contenido, `w` modificar contenido, `x` ejecutar como programa/script.
  - En **directorios**: `r` permite listar nombres (`ls`), `w` crear/renombrar/borrar archivos dentro del directorio (combinado con `x`), y **`x` permite atravesar (`cd`) el directorio y acceder a los inodos**. Un directorio sin `x` queda inaccesible aunque tenga `r`.
- **Comandos de propiedad y permisos:**
  - `chown usuario:grupo archivo` (recursivo con `-R`).
  - `chmod 750 carpeta` (octal) o `chmod u=rwx,g=rx,o= carpeta` (simbólico).
- **Máscara `umask`:** Define los bits que se **restan** por defecto al crear archivos nuevos (base máxima `666` en ficheros, `777` en directorios). Con `umask 022`, directorios nacen en `755` y archivos en `644`; con `umask 027`, nacen en `750` y `640` (otros sin acceso).

## 2. Permisos Especiales POSIX (`SUID`, `SGID`, `Sticky Bit`) (`RA4.d`)

| Bit especial | Valor octal | Efecto sobre archivo ejecutable | Efecto sobre directorio |
| :---: | :---: | :--- | :--- |
| **SUID** (`u+s`) | `4000` | Se ejecuta con los privilegios del **propietario** del binario (ej. `/usr/bin/passwd` corre como `root`) | *(Sin efecto estándar)* |
| **SGID** (`g+s`) | `2000` | Se ejecuta con los privilegios del **grupo** del binario | Los nuevos archivos creados dentro heredan automáticamente el **grupo propietario del directorio** (fundamental para carpetas colaborativas) |
| **Sticky Bit** (`+t`) | `1000` | *(Ignorado en Linux moderno)* | Solo el **propietario del archivo**, el dueño del directorio o `root` pueden borrarlo/renombrarlo aunque la carpeta sea `rwx` para todos (ej. **`/tmp` con `1777`**) |

## 3. Listas de Control de Acceso POSIX (`ACL`: `getfacl` / `setfacl`) (`RA4.d`)

Cuando el esquema clásico `u:g:o` no basta (por ejemplo, dar permiso de escritura a dos usuarios de grupos distintos sin crear otro grupo):
- **`getfacl archivo`** inspecciona propietario, grupo, máscara efectiva y entradas adicionales.
- **`setfacl -m u:ana:rw archivo.txt`** otorga permiso específico a `ana`.
- **`setfacl -m d:g:profes:rwx /srv/compartido`** establece una **ACL por defecto (`d:`)** en un directorio para que los futuros ficheros/subcarpetas hereden permisos automáticamente.
- **`setfacl -b`** limpia todas las ACL extendidas. En `ls -l`, un archivo con ACL muestra un signo **`+`** al final de los permisos (ej. `-rw-r--r--+`).

## 4. Permisos Locales y ACLs en NTFS (Windows) (`RA4.d`, `RA4.e`)

- NTFS evalúa una lista ACL (**DACL**) con entradas (**ACEs**) mucho más granulares (Lectura, Lectura y ejecución, Mostrar contenido, Escritura, Modificar, Control total).
- **Reglas clave de cálculo efectivo en Windows:**
  1. Los permisos de distintas pertenencias a grupos se **acumulan** (unión).
  2. La **Denegación explícita (*Deny*) prevalece siempre** sobre cualquier permiso concedido (*Allow*).
  3. Las **ACLs explícitas** sobre un objeto prevalecen sobre las **heredadas** del directorio padre (salvo denegaciones/orden canónico).
- Herramientas: pestaña *Seguridad → Opciones avanzadas* en GUI, CLI **`icacls`** (`icacls C:\Proyecto /grant alumdam:(OI)(CI)M /inheritance:r`) y PowerShell (`Get-Acl` / `Set-Acl`).
