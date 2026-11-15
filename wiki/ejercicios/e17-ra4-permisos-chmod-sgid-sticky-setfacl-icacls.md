---
ra: RA4
ce:
  - RA4.d
  - RA4.e
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra4-permisos-locales-acls-herencia.md
ultima_revision: "2026-11-15"
---

# e17 · Permisos Locales (`chmod`, SGID, Sticky Bit) y Listas de Control de Acceso (`setfacl` e `icacls`)

<!-- fuente: raw/procesados/ra4-permisos-locales-acls-herencia.md -->

## Escenario y Topología VirtualBox

Partiendo de los usuarios creados en [`e16`](e16-ra4-creacion-usuarios-grupos-politicas-chage-net.md) (`dev_elena` y `dev_carlos` en el grupo `aurora_dev`, más un usuario externo `auditor_externo`), debemos construir un repositorio compartido colaborativo que garantice aislamiento frente a terceros, propiedad de grupo automática y lectura restringida a un auditor puntual mediante **ACLs extendidas**.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e17-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | Permisos POSIX (`chmod`), bits especiales (`SGID`, `Sticky`), `setfacl`/`getfacl` |
| **`e17-Win10`** | Windows 10 Education / Pro | **4 GB** | ACLs NTFS con `icacls`, desactivación de herencia y denegación explícita |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Operativo dentro del presupuesto de **16 GB** del PC **MAX** |

## Objetivos

1. Configurar permisos octales estándar (`chmod`) y herencia de grupo automática mediante **SGID** junto con protección contra borrado cruzado mediante **Sticky Bit** en un directorio compartido.
2. Aplicar una excepción de solo lectura para un usuario externo sin alterar el grupo propietario mediante **POSIX ACLs** (`setfacl`, incluidas ACLs por defecto `d:`).
3. Replicar un escenario equivalente sobre **NTFS** mediante `icacls`, rompiendo la herencia automática sin perder los permisos actuales.

---

## Enunciado Detallado

1. **Directorio colaborativo seguro con SGID y Sticky Bit (`RA4.d`, `RA4.e`):**
   - En Linux, crea `/srv/aurora_compartido` con propietario `root:aurora_dev`.
   - Asigna permisos para que **propietario y grupo tengan `rwx`**, **otros no tengan ningún acceso (`---`)**, los nuevos ficheros hereden automáticamente el grupo `aurora_dev` (**SGID = 2**) y ningún integrante del grupo pueda borrar ficheros creados por otro compañero (**Sticky Bit = 1**).
   - Prueba creando un archivo desde `dev_elena` y otro desde `dev_carlos`, comprobando su grupo propietario y el rechazo al intentar eliminar el fichero ajeno.

2. **Excepción selectiva y herencia con POSIX ACL (`RA4.d`, `RA4.e`):**
   - Crea el usuario `auditor_externo` (fuera de `aurora_dev`).
   - Concede mediante `setfacl` permiso de lectura y ejecución (`r-x` sobre el directorio y `r--` heredable `d:` para futuros ficheros) a `auditor_externo` en `/srv/aurora_compartido`, sin añadirle al grupo `aurora_dev`.
   - Comprueba con `ls -ld` (presencia del símbolo `+` al final de la cadena de permisos) y con `getfacl /srv/aurora_compartido`.

3. **Control NTFS y ruptura de herencia con `icacls` (`RA4.d`, `RA4.e`):**
   - En Windows (`C:\Aurora_Compartido`), rompe la herencia del directorio raíz copiando los permisos actuales (`icacls ... /inheritance:d`), elimina los permisos de `Usuarios` (`BUILTIN\Users`), y concede control total al grupo `aurora_dev` (con herencia `(OI)(CI)`) y solo lectura a `auditor_externo`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Permisos octales, SGID y Sticky Bit en Linux (`RA4.d`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Crear estructura base y grupo propietario
        sudo mkdir -p /srv/aurora_compartido
        sudo chown root:aurora_dev /srv/aurora_compartido

        # Modo octal 3770:
        # 3 = SGID (2) + Sticky Bit (1)
        # 7 = rwx propietario (root)
        # 7 = rwx grupo (aurora_dev)
        # 0 = --- otros usuarios
        sudo chmod 3770 /srv/aurora_compartido
        ls -ld /srv/aurora_compartido
        # Resultado esperado: drwxrws--T 2 root aurora_dev ...

        # Simular creación de ficheros por dos miembros distintos
        sudo -u dev_elena touch /srv/aurora_compartido/modulo_elena.py
        sudo -u dev_carlos touch /srv/aurora_compartido/modulo_carlos.py

        # Comprobar que ambos archivos heredaron el grupo aurora_dev gracias al SGID
        ls -l /srv/aurora_compartido

        # Verificar que dev_carlos NO puede borrar el fichero de dev_elena (Sticky Bit)
        sudo -u dev_carlos rm /srv/aurora_compartido/modulo_elena.py
        # Resultado esperado: rm: cannot remove '...': Operation not permitted
        ```

    === "Windows 10 / 11"

        ```powershell
        # Crear usuario auditor_externo y carpeta compartida NTFS
        $pass = ConvertTo-SecureString "TemporalDam#2026!" -AsPlainText -Force
        New-LocalUser -Name "auditor_externo" -Password $pass -ErrorAction SilentlyContinue
        New-Item -Path "C:\Aurora_Compartido" -ItemType Directory -Force
        ```

    ### 2. POSIX ACLs con herencia por defecto (`setfacl` / `getfacl`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar utilidad acl si el sistema mínimo no la trae
        sudo apt-get update && sudo apt-get install -y acl

        # Crear el usuario externo sin pertenencia a aurora_dev
        sudo useradd -m -s /bin/bash auditor_externo

        # Conceder acceso actual (-m) de lectura+tránsito (rx) y ACL por defecto (-d -m)
        # Nota: en ficheros nuevos dentro del directorio, la máscara de creación suele quitar 'x' si se usa 'rX'
        sudo setfacl -m u:auditor_externo:rx /srv/aurora_compartido
        sudo setfacl -d -m u:auditor_externo:rx /srv/aurora_compartido

        # Aplicar también sobre archivos ya creados previamente dentro de la carpeta
        sudo setfacl -R -m u:auditor_externo:rX /srv/aurora_compartido

        # Inspeccionar '+' en ls y detalle completo con getfacl
        ls -ld /srv/aurora_compartido
        getfacl /srv/aurora_compartido

        # Probar lectura como auditor_externo y rechazo de escritura
        sudo -u auditor_externo ls /srv/aurora_compartido
        sudo -u auditor_externo touch /srv/aurora_compartido/intruso.txt
        # Debe fallar con Permission denied
        ```

    === "Windows 10 / 11"

        ```cmd
        REM En NTFS equivalente: deshabilitar herencia copiando ACLs heredadas (/inheritance:d)
        icacls C:\Aurora_Compartido /inheritance:d

        REM Retirar acceso genérico de Usuarios locales
        icacls C:\Aurora_Compartido /remove:g "BUILTIN\Usuarios"

        REM En Windows en inglés usar BUILTIN\Users; ante duda de idioma usar SID *S-1-5-32-545
        icacls C:\Aurora_Compartido /remove:g "*S-1-5-32-545"

        REM Conceder Modificar (M) heredable a objetos (OI) y contenedores (CI) para aurora_dev
        icacls C:\Aurora_Compartido /grant "aurora_dev:(OI)(CI)M"

        REM Conceder solo Lectura y ejecución (RX) heredable para auditor_externo
        icacls C:\Aurora_Compartido /grant "auditor_externo:(OI)(CI)RX"

        REM Mostrar tabla final de ACLs NTFS
        icacls C:\Aurora_Compartido
        ```

---

## Puntos de Control y Errores Frecuentes

- **`rX` vs `rx` en `setfacl`:** Usar `X` mayúscula en recursivo (`setfacl -R -m u:usuario:rX`) otorga el bit de ejecución **solo** a directorios y a archivos que ya fueran ejecutables, evitando dar permisos ejecutables innecesarios a documentos o ficheros fuente `.py`/`.txt`.
- **La máscara (`mask`) en POSIX ACL:** Si modificas permisos tradicionales con `chmod` sobre un directorio con ACLs, modificas el parámetro `mask::` de la ACL y puedes limitar sin querer el permiso efectivo de los usuarios ACL aunque aparezcan con `rwx`. Verifica siempre `#effective:` en `getfacl`.
- **SID universales en `icacls`:** En instalaciones de Windows en español, `BUILTIN\Users` se llama `BUILTIN\Usuarios`. Usar el **SID universal `*S-1-5-32-545`** funciona independientemente del idioma del sistema operativo.

## Recursos para Profundizar

- Concepto asociado: [Permisos locales, bits especiales y listas de control de acceso (ACLs)](../conceptos/ra4-permisos-locales-bits-especiales-acls.md).
- Documentación de `icacls`: [Microsoft Learn · icacls](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/icacls).
- Vídeo recomendado sobre permisos POSIX y ACLs: [Permisos en Linux: chmod, chown y ACLs (YouTube)](https://www.youtube.com/watch?v=zAie7f3uhp8).
