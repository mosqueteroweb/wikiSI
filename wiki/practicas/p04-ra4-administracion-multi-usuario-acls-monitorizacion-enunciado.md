---
ra: RA4
ce:
  - RA4.a
  - RA4.b
  - RA4.c
  - RA4.d
  - RA4.e
  - RA4.f
  - RA4.g
  - RA4.h
tipo: practica
publicar: true
fuentes:
  - raw/procesados/ra4-usuarios-grupos-directivas-seguridad.md
  - raw/procesados/ra4-permisos-locales-acls-herencia.md
  - raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md
ultima_revision: "2026-11-15"
---

# p04 · Administración Multiusuario, ACLs, Servicios, Monitorización y Entorno DAM (`RA4.a`–`RA4.h`)

<!-- fuente: raw/procesados/ra4-usuarios-grupos-directivas-seguridad.md -->

## Situación Profesional de Partida

El estudio de desarrollo **KoraApps DAM** necesita poner en producción su entorno interno de trabajo sobre dos equipos virtualizados dentro del laboratorio (**MAX 16 GB de RAM**): un servidor Linux de proyectos y compilación compartida y una estación de trabajo Windows para desarrollo de escritorio y pruebas cliente.

Debes configurar íntegramente las cuentas, políticas de contraseñas, permisos heredables, servicios críticos, auditoría de registros y entorno de desarrollo Java/Python cumpliendo todos los criterios **RA4.a – RA4.h**.

## Topología VirtualBox y Presupuesto de RAM

| Máquina Virtual | Sistema Operativo | RAM asignada | Función |
| :--- | :--- | :---: | :--- |
| **`DAM-Srv-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | Servidor de repositorio local, servicios `systemd`, ACLs y logs |
| **`DAM-Workstation-Win10`** | Windows 10 Education / Pro | **4 GB** | Estación cliente de desarrollo, directivas locales, ACLs NTFS y PowerShell |
| **Consumo total activo** | **Anfitrión MAX (16 GB)** | **6 GB** | Margen libre **10 GB** (dentro del límite seguro del aula ≤ 10–12 GB) |

---

## Tareas Evaluables (`RA4.a` – `RA4.h`)

### Tarea 1 · Gestión de usuarios, grupos y privilegios delegados (`RA4.a`, `RA4.b`, `RA4.e`)

Configura en **ambas VMs** (`DAM-Srv-Ubuntu` y `DAM-Workstation-Win10`):

1. Dos grupos locales de proyecto: `kora_devs` y `kora_qa`.
2. Tres cuentas de usuario nominales con directorio personal:
   - `laura.dev` (pertenece a `kora_devs`).
   - `marco.qa` (pertenece a `kora_qa`).
   - `sofia.lead` (pertenece tanto a `kora_devs` como a `kora_qa`, con privilegios administrativos delegados).
3. En Linux, delega mediante `/etc/sudoers.d/kora_lead` (validado con `visudo -c`) permisos exclusivamente para que `sofia.lead` ejecute `systemctl restart nginx`, `journalctl` y `apt update` (sin darle `ALL` sin control y obligando a introducir su propia contraseña).
4. En `DAM-Srv-Ubuntu`, crea además la cuenta de servicio `svc_ci` sin directorio personal ni shell interactiva (`/usr/sbin/nologin`).

### Tarea 2 · Directivas de cuenta y contraseñas (`RA4.b`, `RA4.e`)

1. En `DAM-Srv-Ubuntu`, aplica mediante `chage` sobre `laura.dev` y `marco.qa`:
   - Caducidad máxima de contraseña: **90 días** (`-M 90`).
   - Mínimo entre cambios: **3 días** (`-m 3`).
   - Aviso de expiración: **10 días** antes (`-W 10`).
   - Fuerza que `marco.qa` cambie su contraseña en el primer inicio de sesión (`-d 0`).
2. En `DAM-Workstation-Win10`, configura la política local de cuentas (`net accounts`) con:
   - Longitud mínima de contraseña: **10 caracteres**.
   - Vigencia máxima: **90 días**; vigencia mínima: **3 días**; historial de **5 contraseñas**.
   - Umbral de bloqueo tras **4 intentos fallidos** durante **15 minutos** (ventana de observación **15 minutos**).

### Tarea 3 · Estructura colaborativa, SGID, Sticky Bit y ACLs (`RA4.d`, `RA4.e`)

1. En `DAM-Srv-Ubuntu`, crea `/srv/kora_repo` propiedad de `root:kora_devs` con:
   - Permisos octales **`3770`** (SGID + Sticky Bit + `rwx` propietario y grupo, `0` para otros).
   - Mediante **`setfacl`**, añade acceso de solo lectura/tránsito (`r-x` en carpeta actual y `rX` en archivos actuales y regla por defecto `d:` para futuros elementos) al grupo `kora_qa` sin incluir a `kora_qa` como grupo propietario ni añadir usuarios individuales a `kora_devs`.
2. En `DAM-Workstation-Win10`, crea `C:\KoraRepo`, rompe la herencia copiando permisos base (`/inheritance:d`), elimina a `Usuarios` (`*S-1-5-32-545`), concede control de modificación (`M`) heredable `(OI)(CI)` a `kora_devs` y solo lectura/ejecución (`RX`) heredable a `kora_qa`.

### Tarea 4 · Procesos, prioridades y servicios del sistema (`RA4.c`, `RA4.e`)

1. Instala `nginx` en `DAM-Srv-Ubuntu` (si no está instalado), comprueba su unidad `systemd`, habilítalo en el arranque (`enable`), realiza una modificación simulada o recarga sin corte (`reload`) y verifica su nuevo estado.
2. En Linux, lanza una tarea controlada `sleep 900 &` con prioridad reducida (`nice -n 12`), cámbiale la prioridad en ejecución a `18` con `renice`, muestra la línea con `ps -eo pid,ppid,ni,stat,comm` y finalízala limpiamente con `SIGTERM` (`-15`).
3. En `DAM-Workstation-Win10`, utiliza PowerShell para comprobar el estado del servicio `Spooler` (o `W32Time`), cambiar temporalmente su arranque a `Manual`, detenerlo, arrancarlo y restaurar `Automatic`.

### Tarea 5 · Monitorización, auditoría de logs y optimización (`RA4.f`, `RA4.g`)

1. Instala `htop`, `sysstat` y `ncdu` en `DAM-Srv-Ubuntu`.
2. Registra el consumo de memoria (`free -h`), captura 4 muestras de `vmstat 2 4` y audita con `journalctl` los errores del arranque actual (`-b -p err`) así como los eventos de autenticación recientes.
3. Reduce el almacenamiento de los diarios de `systemd` a un máximo de **100 MB** (`--vacuum-size=100M`) y purga la caché de paquetes `apt` sin usar.
4. En `DAM-Workstation-Win10`, extrae con `Get-WinEvent` los 5 últimos errores del registro `System` y mide CPU y RAM disponible durante 6 segundos con `Get-Counter`.

### Tarea 6 · Entorno de desarrollo DAM y dimensionamiento (`RA4.e`, `RA4.g`, `RA4.h`)

1. En `DAM-Srv-Ubuntu`, instala `openjdk-21-jdk`, `git` y `python3-venv`; define `JAVA_HOME` persistente en `~/.bashrc` y crea el script `/usr/local/bin/kora_health.sh` (permisos `755`) que muestre memoria libre (`available`), espacio libre en `/` y estado activo de `nginx`.
2. Redacta un **Informe Técnico de Dimensionamiento (`RA4.h`)** justificando si una estación con 8 GB de RAM sería suficiente para el desarrollador frente a la configuración de 16 GB del aula o 32 GB profesionales.

---

## Entregables y Criterios de Corrección

El alumno entregará un único dossier técnico en **PDF o Markdown** (`Apellido_Nombre_p04_RA4.pdf` / `.md`) que incluya:

1. **Evidencias de comandos y capturas** de las 6 tareas mostrando salida real de `id`, `chage -l`, `net accounts`, `getfacl`, `icacls`, `systemctl status nginx`, `journalctl`, `Get-WinEvent` y ejecución de `kora_health.sh`.
2. **Prueba funcional de aislamiento ACL y Sticky Bit** (demostrando que `marco.qa` lee ficheros en `/srv/kora_repo` pero recibe *Permission denied* al intentar escribir o borrar).
3. **Tabla comparativa de dimensionamiento DAM (`RA4.h`)** justificando cuello de botella de CPU, RAM e IOPS en disco.

| Bloque evaluado | Criterios cubiertos | Peso |
| :--- | :---: | :---: |
| Cuentas, grupos, `sudo` y directivas de contraseña | `RA4.a`, `RA4.b`, `RA4.e` | **25 %** |
| Permisos POSIX, SGID, Sticky Bit y ACLs (`setfacl`/`icacls`) | `RA4.d`, `RA4.e` | **25 %** |
| Procesos, prioridades y ciclo de vida de servicios | `RA4.c`, `RA4.e` | **15 %** |
| Auditoría de logs, rendimiento y optimización preventiva | `RA4.f`, `RA4.g` | **20 %** |
| Preparación entorno DAM, script y dimensionamiento | `RA4.e`, `RA4.g`, `RA4.h` | **15 %** |

## Recursos de Apoyo

- [Conceptos del bloque RA4](../ra/RA4.md#conceptos-teoricos)
- [Ejercicios resueltos e16–e20](../ra/RA4.md#ejercicios-practicos-resueltos)
- Vídeos de repaso del bloque: [Usuarios y sudo](https://www.youtube.com/watch?v=6rrWRe_7Y-A) · [Permisos y ACLs](https://www.youtube.com/watch?v=zAie7f3uhp8) · [Procesos y systemd](https://www.youtube.com/watch?v=dx-ixZOnkpQ)
