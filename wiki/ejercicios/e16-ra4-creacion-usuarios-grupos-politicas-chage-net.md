---
ra: RA4
ce:
  - RA4.a
  - RA4.b
  - RA4.e
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra4-usuarios-grupos-directivas-seguridad.md
ultima_revision: "2026-11-15"
---

# e16 · Creación de Usuarios, Grupos y Directivas de Seguridad (`chage` y `net accounts`)

<!-- fuente: raw/procesados/ra4-usuarios-grupos-directivas-seguridad.md -->

## Escenario y Topología VirtualBox

En el aula **1.º DAM** (PC anfitrión **MAX** con **16 GB de RAM**), necesitamos desplegar una estructura mínima multiusuario y de control de contraseñas para el equipo de desarrollo **Proyecto Aurora**:

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e16-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | Gestión POSIX (`/etc/passwd`, `/etc/shadow`, `chage`, `sudo`) |
| **`e16-Win10`** | Windows 10 Education / Pro | **4 GB** | Gestión local SAM (`net user`, `net accounts`, `secpol.msc`) |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Respeta ampliamente el límite del aula (≤ 10–12 GB) |

## Objetivos

1. Crear el grupo secundario `aurora_dev` y dos cuentas locales (`dev_elena` y `dev_carlos`) con directorio personal propio.
2. Configurar la caducidad y bloqueo preventivo de contraseñas (`chage` en Linux y `net accounts` / PowerShell en Windows).
3. Delegar privilegios administrativos auditados a `dev_elena` (`sudo` limitado o pertenencia a grupo autorizado) e impedir el inicio de sesión interactivo a una cuenta de servicio `svc_backup`.
4. Verificar los ficheros de identidad locales sin exponer hashes.

---

## Enunciado Detallado

Realiza sobre ambas máquinas virtuales los pasos siguientes y captura o verifica la salida de los comandos solicitados:

1. **Grupos y cuentas locales (`RA4.a`, `RA4.e`):**
   - Crea el grupo `aurora_dev`.
   - Crea el usuario `dev_elena` (nombre completo `Elena Navarro`, shell `/bin/bash` en Linux) y añádela a `aurora_dev`.
   - Crea el usuario `dev_carlos` en `aurora_dev`, asignándole una contraseña temporal segura y obligándole a cambiarla en su **primer inicio de sesión**.
   - Crea la cuenta técnica `svc_backup` sin directorio personal ni acceso a shell interactiva (`/usr/sbin/nologin` en Linux; deshabilitada para inicio de sesión en consola o marcada adecuadamente en Windows).

2. **Directivas de cuenta y contraseñas (`RA4.b`, `RA4.e`):**
   - En Linux, aplica a `dev_carlos` una caducidad máxima de contraseña de **60 días**, mínimo **2 días** entre cambios, aviso previo de **7 días** e inactividad de **10 días** tras expirar (`chage`). Muestra la política resultante.
   - En Windows, ajusta la política local de cuentas para exigir longitud mínima de **10 caracteres**, vigencia máxima de **60 días**, historial de **5 contraseñas** y bloqueo de cuenta tras **5 intentos fallidos** durante **15 minutos** (`net accounts`).

3. **Delegación `sudo` y comprobación de bloqueo (`RA4.b`, `RA4.e`):**
   - Permite únicamente a `dev_elena` ejecutar `apt update` y `systemctl restart nginx` sin que afecte al resto de usuarios estándar ni conceder acceso total sin auditoría, usando `visudo -f /etc/sudoers.d/aurora` en Linux o comprobando la separación estándar/administrador en Windows.
   - Bloquea temporalmente la cuenta `dev_carlos` y verifica su estado antes de desbloquearla de nuevo.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Creación de grupos, usuarios y cuenta de servicio (`RA4.a`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # 1. Crear grupo secundario para el proyecto
        sudo groupadd aurora_dev

        # 2. Crear usuaria dev_elena con home (-m), comentario (-c), bash (-s) y grupo (-G)
        sudo useradd -m -c "Elena Navarro" -s /bin/bash -G aurora_dev dev_elena
        echo "dev_elena:TemporalDam#2026" | sudo chpasswd

        # 3. Crear usuario dev_carlos y forzar cambio de contraseña en el primer login
        sudo useradd -m -c "Carlos Ruiz" -s /bin/bash -G aurora_dev dev_carlos
        echo "dev_carlos:TemporalDam#2026" | sudo chpasswd
        sudo chage -d 0 dev_carlos

        # 4. Cuenta de servicio sin home (-M) y sin shell interactiva
        sudo useradd -r -M -s /usr/sbin/nologin -c "Servicio Backup Aurora" svc_backup

        # 5. Verificación en NSS / passwd y grupos (sin mostrar /etc/shadow)
        getent group aurora_dev
        getent passwd dev_elena dev_carlos svc_backup
        id dev_elena
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador
        New-LocalGroup -Name "aurora_dev" -Description "Desarrolladores Proyecto Aurora"

        $pass = ConvertTo-SecureString "TemporalDam#2026!" -AsPlainText -Force
        New-LocalUser -Name "dev_elena" -FullName "Elena Navarro" -Password $pass
        New-LocalUser -Name "dev_carlos" -FullName "Carlos Ruiz" -Password $pass

        # Añadir al grupo local aurora_dev
        Add-LocalGroupMember -Group "aurora_dev" -Member "dev_elena", "dev_carlos"

        # Forzar cambio de contraseña en el próximo inicio de sesión con net user
        net user dev_carlos /logonpasswordchg:yes

        # Crear cuenta técnica svc_backup deshabilitada para consola interactiva normal
        New-LocalUser -Name "svc_backup" -Description "Cuenta tecnica de servicio" -Password $pass -PasswordNeverExpires
        Disable-LocalUser -Name "svc_backup"

        # Verificar cuentas y membresía
        Get-LocalGroupMember -Group "aurora_dev"
        Get-LocalUser dev_elena, dev_carlos, svc_backup | Select-Object Name, Enabled, PasswordLastSet
        ```

    ### 2. Directivas de cuenta y contraseñas (`RA4.b`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Configurar caducidad para dev_carlos:
        # -m 2 (mínimo 2 días), -M 60 (máximo 60), -W 7 (aviso 7 días), -I 10 (inactivo 10 días tras expirar)
        sudo chage -m 2 -M 60 -W 7 -I 10 dev_carlos

        # Nota: mantener -d 0 solo si queremos forzar el cambio inmediato al próximo login;
        # la política anterior fija las ventanas de expiración.
        sudo chage -d 0 dev_carlos

        # Consultar estado resultante de la cuenta
        sudo chage -l dev_carlos
        ```

        La salida debe mostrar `Password must be changed` en el apartado *Last password change*, `Minimum number of days between password change: 2`, `Maximum: 60`, `Number of days of warning: 7` y `Inactive: 10`.

    === "Windows 10 / 11"

        ```cmd
        REM Ejecutar en Símbolo del sistema (cmd) como Administrador
        net accounts /minpwlen:10 /maxpwage:60 /minpwage:2 /uniquepw:5
        net accounts /lockoutthreshold:5 /lockoutduration:15 /lockoutwindow:15

        REM Verificar directivas locales vigentes
        net accounts
        ```

        En ediciones **Pro / Education**, estas mismas directivas quedan reflejadas gráficamente en `secpol.msc` bajo **Directivas de cuenta → Directiva de contraseñas** y **Directiva de bloqueo de cuenta**.

    ### 3. Delegación granular (`sudo`) y bloqueo/desbloqueo de cuentas (`RA4.b`, `RA4.e`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Validar sintaxis segura creando un fichero modular en /etc/sudoers.d/
        echo "dev_elena ALL=(root) /usr/bin/apt update, /usr/bin/systemctl restart nginx" | sudo tee /etc/sudoers.d/aurora
        sudo chmod 0440 /etc/sudoers.d/aurora
        sudo visudo -c -f /etc/sudoers.d/aurora

        # Probar privilegios efectivos asignados a dev_elena
        sudo -l -U dev_elena

        # Bloquear y verificar dev_carlos en /etc/shadow (antepone '!' al hash)
        sudo usermod -L dev_carlos
        sudo passwd -S dev_carlos

        # Desbloquear nuevamente
        sudo usermod -U dev_carlos
        sudo passwd -S dev_carlos
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar privilegios administrativos locales (solo Administradores los poseen)
        Get-LocalGroupMember -Group "Administradores" -ErrorAction SilentlyContinue

        # Bloquear (deshabilitar) y reactivar cuenta dev_carlos
        Disable-LocalUser -Name "dev_carlos"
        Get-LocalUser -Name "dev_carlos" | Select-Object Name, Enabled

        Enable-LocalUser -Name "dev_carlos"
        Get-LocalUser -Name "dev_carlos" | Select-Object Name, Enabled
        ```

---

## Puntos de Control y Errores Frecuentes

- **Error típico 1 (`usermod -G` sin `-a`):** Ejecutar `sudo usermod -G otro_grupo usuario` reemplaza todos sus grupos secundarios actuales. Para añadir un grupo sin perder `sudo` ni los anteriores, utiliza siempre `usermod -aG`.
- **Error típico 2 (permisos en `/etc/sudoers.d/`):** Un fichero con permisos `0644` en `/etc/sudoers.d/` hace que `sudo` lo ignore por seguridad o falle al parsear; debe tener exactamente `0440`.
- **Diferencia Linux vs Windows en bloqueo:** `usermod -L` bloquea la autenticación por contraseña en `/etc/shadow`, pero si el usuario tiene clave pública SSH en `~/.ssh/authorized_keys` aún podría entrar salvo que se bloquee también la shell o se use `usermod -e 1` (expiración total).

## Recursos para Profundizar

- Concepto asociado: [Administración de usuarios y grupos locales](../conceptos/ra4-administracion-usuarios-grupos-locales.md) y [Directivas de cuenta, contraseñas y sudo](../conceptos/ra4-directivas-cuenta-politicas-contrasenas-sudo.md).
- Manual oficial de Ubuntu (`chage`, `useradd`, `sudoers`): [Ubuntu Manpages](https://manpages.ubuntu.com/).
- Vídeo recomendado sobre usuarios, grupos y `sudo` en Linux: [Administración de usuarios y grupos en Linux (YouTube)](https://www.youtube.com/watch?v=6rrWRe_7Y-A).
