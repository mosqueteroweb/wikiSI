---
id: "raw-ra4-usuarios-grupos-directivas-seguridad"
ra: ["RA4"]
ce: ["RA4.a", "RA4.b", "RA4.e"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "man-pages Linux: passwd(5), shadow(5), group(5), useradd(8), usermod(8), chage(1), sudoers(5), pam(8)"
  - "Ubuntu Server Guide: User Management y Security Console"
  - "Microsoft Learn: Local Users and Groups (lusrmgr.msc), SAM, Security Identifiers (SID), Account Policies (secpol.msc)"
---

# Fuente Procesada: Usuarios, Grupos y Directivas de Seguridad de Cuentas y Contraseñas

## 1. Gestión de Cuentas Locales y Grupos (`RA4.a`, `RA4.e`)

- **En GNU/Linux (MAX / Ubuntu):**
  - **`/etc/passwd`**: Lista cuentas de usuario (`usuario:x:UID:GID:GECOS:home:shell`). Legible por todos (`644`), ya no guarda contraseñas reales sino un marcador `x`.
    - `UID 0`: Superusuario `root`.
    - `UID 1–999`: Cuentas del sistema/servicios (sin inicio interactivo `/usr/sbin/nologin`).
    - `UID >= 1000`: Usuarios humanos estándar (primer usuario creado en Ubuntu = `1000`).
  - **`/etc/shadow`**: Almacena los hashes criptográficos (`yescrypt` `$y$` o SHA-512 `$6$`) con *salt* aleatorio, fecha del último cambio, caducidad y bloqueo. Legible **solo por `root`/grupo `shadow`** (`640`).
  - **`/etc/group`** y **`/etc/gshadow`**: Grupos primarios y secundarios (`nombre:x:GID:miembros`). En Debian/Ubuntu el grupo administrativo privilegiado es **`sudo`**.
  - **`/etc/skel`**: Directorio plantilla cuyo contenido (`.bashrc`, `.profile`) se copia automáticamente al `home` de cada nuevo usuario al usar `useradd -m` o `adduser`.
  - Comandos clave: `adduser`, `useradd -m -s /bin/bash`, `usermod -aG sudo,docker usuario` (siempre usar `-aG`, nunca `-G` solo o sobreescribirá sus grupos anteriores), `groupadd`, `deluser --remove-home`, `id`, `groups`, `who`, `w`, `last`.
- **En Windows 10 / 11:**
  - La base de datos local **SAM (*Security Accounts Manager*)** en `%SystemRoot%\System32\config\SAM` gestiona cuentas y grupos locales asignando a cada entidad un **SID (*Security Identifier*)** único (`S-1-5-21-...`).
  - Herramientas: GUI **`lusrmgr.msc`** (en ediciones Pro/Edu/Enterprise), **PowerShell** módulo `Microsoft.PowerShell.LocalAccounts` (`New-LocalUser`, `New-LocalGroup`, `Add-LocalGroupMember`, `Get-LocalUser`, `Disable-LocalUser`), y comando clásico **`net user`** / **`net localgroup`**.

## 2. Directivas de Cuenta, Contraseñas y Elevación de Privilegios (`RA4.b`, `RA4.e`)

- **Seguridad de contraseñas y caducidad en Linux:**
  - **`/etc/login.defs`**: Define rangos UID/GID, días máximos/mínimos de validez (`PASS_MAX_DAYS`, `PASS_MIN_DAYS`, `PASS_WARN_AGE`).
  - **`chage`** (`chage -l usuario`, `chage -M 90 -m 7 -W 14 usuario`, `chage -d 0 usuario` para forzar cambio al próximo inicio).
  - **`passwd -l` / `passwd -u`** (o `usermod -L/-U`) para bloquear y desbloquear cuentas.
  - **PAM (*Pluggable Authentication Modules*):** Módulos en `/etc/pam.d/` como `pam_pwquality` / `pam_unix` (longitud mínima, complejidad) y **`pam_faillock`** (bloqueo temporal tras $N$ intentos fallidos de inicio de sesión o `ssh`).
  - **`sudo` y `visudo`:** Delegación granular de privilegios administrativos editando `/etc/sudoers` o drop-ins en `/etc/sudoers.d/` mediante `sudo visudo` (que valida la sintaxis antes de guardar para no bloquear el acceso administrativo).
- **Directivas de cuenta en Windows (`RA4.b`):**
  - Consola **`secpol.msc`** (*Directiva de seguridad local → Directivas de cuenta*):
    1. *Directiva de contraseñas:* Historial (recordar últimas contraseñas), vigencia máxima/mínima, longitud mínima y requisitos de complejidad.
    2. *Directiva de bloqueo de cuenta:* Umbral de bloqueo (ej. 5 intentos inválidos), duración del bloqueo y restablecimiento del contador.
  - CLI clásica: **`net accounts`** (`net accounts /minpwlen:10 /maxpwage:90 /lockoutthreshold:5 /lockoutduration:15`) y **`secedit`**.
  - **UAC (*User Account Control*):** Separa tokens administrativos de estándar solicitando consentimiento o credenciales al ejecutar operaciones elevadas.
