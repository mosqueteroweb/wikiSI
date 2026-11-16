---
ra: RA6
ce:
  - RA6.a
  - RA6.b
  - RA6.c
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md
ultima_revision: "2026-11-15"
---

# e26 · Compartición de Recursos con Samba (`SMB3`), Permisos Efectivos y Mapeo Multiplataforma

<!-- fuente: raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md -->

## Escenario y Topología VirtualBox

En la red interna VirtualBox del aula (**MAX 16 GB RAM**), compartiremos un directorio departamental en **`e26-Ubuntu-Samba`** comprobando cómo interactúan los permisos de red Samba frente a los permisos POSIX locales del sistema de archivos al acceder desde **`e26-Win10-Cli`**.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e26-Ubuntu-Samba`** | Ubuntu Server 24.04 | **2 GB** | Servidor Samba (`445/TCP`) compartiendo `/srv/smb_aurora` |
| **`e26-Win10-Cli`** | Windows 10 Education / Pro | **4 GB** | Cliente mapeando unidad de red (`net use Z:`) |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Cumple margen seguro en **MAX (16 GB)** |

## Objetivos

1. Desplegar **Samba (`smbd`)** con credenciales dedicadas (`smbpasswd -a`).
2. Configurar permisos de compartición (`valid users`, `write list`) combinados con permisos locales POSIX (`3770`).
3. Validar la configuración con `testparm -s` y montar el recurso desde cliente Windows y Linux (`mount -t cifs`).

---

## Enunciado Detallado

1. En **`e26-Ubuntu-Samba`** (`192.168.50.10`), crea el grupo `equipo_dam` y dos usuarios: `dev_ana` (pertenece a `equipo_dam`) y `invitado_ro` (fuera de `equipo_dam`). Habilita ambos para Samba mediante `sudo smbpasswd -a`.
2. Crea `/srv/smb_aurora` propiedad de `root:equipo_dam` con permisos **`2770`** (SGID + `rwx` propietario y grupo), y además concede lectura POSIX a `invitado_ro` mediante `setfacl -m u:invitado_ro:rx /srv/smb_aurora` (o deja que Samba filtre la escritura).
3. Añade en `/etc/samba/smb.conf` el recurso `[AuroraShare]` accesible solo para `dev_ana` e `invitado_ro`, permitiendo escritura **exclusivamente** a `@equipo_dam` (`write list = @equipo_dam`, `read only = yes` por defecto). Valida con `testparm -s` y reinicia `smbd`.
4. Desde **`e26-Win10-Cli`**, mapea `Z:` autenticado como `dev_ana` para probar crear un fichero, y después prueba desde `smbclient` (o desconectando y reconectando como `invitado_ro`) que la escritura queda denegada al aplicar el permiso más restrictivo.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Instalación de Samba, cuentas SMB y permisos base (`RA6.a`, `RA6.b`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar Samba y utilidades cliente/ACL
        sudo apt-get update && sudo apt-get install -y samba smbclient cifs-utils acl

        # Crear grupo, usuarios locales y asignarles contraseña SMB independiente
        sudo groupadd equipo_dam
        sudo useradd -m -s /usr/sbin/nologin -G equipo_dam dev_ana
        sudo useradd -m -s /usr/sbin/nologin invitado_ro
        sudo smbpasswd -a dev_ana
        sudo smbpasswd -a invitado_ro

        # Carpeta física con SGID (2770) y lectura ACL puntual para invitado_ro
        sudo mkdir -p /srv/smb_aurora
        sudo chown root:equipo_dam /srv/smb_aurora
        sudo chmod 2770 /srv/smb_aurora
        sudo setfacl -m u:invitado_ro:rx /srv/smb_aurora
        sudo setfacl -d -m u:invitado_ro:rx /srv/smb_aurora
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar conectividad previa al puerto SMB 445 en e26-Ubuntu-Samba
        Test-NetConnection -ComputerName 192.168.50.10 -Port 445
        ```

    ### 2. Configuración `/etc/samba/smb.conf` y validación (`RA6.c`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Añadir sección al final de /etc/samba/smb.conf
        sudo tee -a /etc/samba/smb.conf > /dev/null <<'EOF'

        [AuroraShare]
           comment = Carpeta Compartida Proyecto Aurora
           path = /srv/smb_aurora
           browseable = yes
           read only = yes
           valid users = @equipo_dam, invitado_ro
           write list = @equipo_dam
           create mask = 0660
           directory mask = 0770
           force group = equipo_dam
        EOF

        # Validar sintaxis antes de reiniciar el demonio
        testparm -s
        sudo systemctl restart smbd
        sudo systemctl enable smbd

        # Probar localmente con smbclient como ambos usuarios
        smbclient //192.168.50.10/AuroraShare -U dev_ana -c "ls"
        ```

    === "Windows 10 / 11"

        ```cmd
        REM Limpiar posibles credenciales SMB cacheadas previas
        net use * /delete /y

        REM Mapear unidad persistente Z: como dev_ana (pedirá clave SMB)
        net use Z: \\192.168.50.10\AuroraShare /user:dev_ana /persistent:yes
        echo Prueba desde Win10 > Z:\entrega_ana.txt
        dir Z:\

        REM Si montamos luego como invitado_ro (tras net use Z: /delete), podrá listar Z:
        REM pero recibirá "Acceso denegado" al intentar escribir en Z:\
        ```

    ### Paso 4 (Ampliación en Red Interna Windows NTFS): Anónimo, Propietario y Caso EFS Pedro/Luis

    En dos máquinas Windows (`Win-A` y `Win-B`) conectadas en **Red Interna** sobre partición **NTFS**, comprueba experimentalmente los siguientes supuestos del trabajo en grupo sin dominio:

    1. **Usuario inexistente en remoto y acceso anónimo:** intenta acceder desde `Win-B` con una cuenta que no existe en `Win-A`. Observa qué cambia al entrar en el **Centro de redes y recursos compartidos** $\rightarrow$ *Configuración de uso compartido avanzado* y **desactivar la protección por contraseña** (habilitando `Todos`).
    2. **Control selectivo en red:** configura la carpeta para que únicamente `pedro` pueda leer/escribir desde cualquier equipo Windows y el resto solo leer (`Permisos SMB` + `Permisos NTFS`).
    3. **El dilema del cifrado EFS entre Pedro y Luis:** con ambos usuarios autorizados para escribir en la carpeta compartida, haz que `pedro` cifre la carpeta con todo su contenido (*Propiedades* $\rightarrow$ *Avanzadas* $\rightarrow$ *Cifrar contenido*). Comprueba y razona por qué:
       - `luis` **no puede leer** los ficheros de `pedro`, aunque sí puede crear otros nuevos en la carpeta si tiene permiso de escritura.
       - Los archivos creados por `luis` quedan cifrados con la clave de `luis`, impidiendo que `pedro` los abra en local o por red sin compartir certificados EFS.
    4. **Cambio de propietario:** transfiere la propiedad NTFS de una carpeta de prueba a otro administrador y verifica si el antiguo propietario conserva acceso cuando se revisan los permisos explícitos (concluyendo por qué en redes medianas se adopta un **Dominio Active Directory / Samba AD**, trabajado en `e30`).

---

## Puntos de Control y Errores Frecuentes

- **Olvidar `smbpasswd -a`:** Que el usuario exista en `/etc/passwd` NO basta; Samba exige que la cuenta esté dada de alta en su propia base TDB con `sudo smbpasswd -a`.
- **Caché de sesiones SMB en Windows:** Windows no permite conectar simultáneamente al mismo servidor IP usando dos nombres de usuario distintos en la misma sesión de escritorio. Ejecuta `net use * /delete /y` antes de cambiar de usuario de prueba.

## Recursos para Profundizar

- Concepto asociado: [Recursos Compartidos en Red, Permisos Efectivos y Samba/SMB](../conceptos/ra6-recursos-compartidos-permisos-red-samba-smb.md).
- Vídeo recomendado sobre Samba SMB: [Compartición de recursos con Samba SMB (YouTube)](https://www.youtube.com/watch?v=ayaI9WNiFXA).
