---
id: "raw-ra4-procesos-servicios-monitorizacion-desarrollo"
ra: ["RA4"]
ce: ["RA4.c", "RA4.e", "RA4.f", "RA4.g", "RA4.h"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "man-pages Linux: ps(1), kill(1), nice(1), systemctl(1), journalctl(1), top(1), logrotate(8)"
  - "systemd Documentation (freedesktop.org): systemd.service, systemd.unit"
  - "Microsoft Learn: Service Control Manager, Get-Process, Get-Service, Event Viewer (Get-WinEvent), Resource Monitor"
---

# Fuente Procesada: Procesos, Servicios, Monitorización, Logs y Entorno de Desarrollo DAM

## 1. Gestión de Procesos y Servicios (`RA4.c`, `RA4.e`)

- **Proceso vs. Hilo vs. Servicio/Demonio:**
  - Un **proceso** es una instancia de programa en ejecución con espacio de memoria aislado, **PID** (*Process ID*) y proceso padre (**PPID**). En Linux el primer proceso en espacio de usuario (`PID 1`) es **`systemd`**.
  - Estados principales en Linux (`ps`/`top`): **`R`** (Running/Runnable), **`S`** (Interruptible Sleep), **`D`** (Uninterruptible I/O Sleep), **`T`** (Stopped), **`Z`** (Zombie — terminó pero su padre aún no leyó su código de salida).
- **Control y prioridades en Linux:**
  - Ejecución en segundo plano y trabajo en terminal: `comando &`, `jobs`, `fg`, `bg`, `Ctrl+Z`, `nohup`.
  - Listado: `ps aux`, `ps -ef`, `pstree`, `pgrep`.
  - Prioridad de planificación (**Niceness** de `-20` máxima prioridad a `+19` mínima; por defecto `0`): `nice -n 10 script.sh`, `renice -n 5 -p <PID>`.
  - Envío de señales: **`kill -15 <PID>` (`SIGTERM`)** solicita cierre ordenado guardando datos; **`kill -9 <PID>` (`SIGKILL`)** fuerza terminación inmediata desde el kernel (no atrapable por el proceso); `kill -1` (`SIGHUP`) suele recargar configuración sin parar el servicio; `pkill` por nombre.
- **Gestión de servicios con `systemd` (Linux):**
  - `systemctl status|start|stop|restart|reload nginx`
  - `systemctl enable|disable nginx` (arranque automático en inicio del sistema).
  - Los ficheros de unidad residen en `/lib/systemd/system/` y `/etc/systemd/system/`.
- **Procesos y servicios en Windows:**
  - GUI: Administrador de tareas (`Ctrl+Shift+Esc`), **`services.msc`**.
  - Consola/PowerShell: `Get-Process` / `tasklist`, `Stop-Process -Id <PID> -Force` / `taskkill /PID ... /F`, `Get-Service`, `Start-Service`, `Stop-Service`, `Set-Service -StartupType Automatic`.

## 2. Monitorización del Sistema, Registros (Logs) y Optimización (`RA4.f`, `RA4.g`)

- **Monitorización de recursos (CPU, RAM, E/S Disco, Red):**
  - Linux: `top`, **`htop`**, **`btop`**, `free -h`, `vmstat 1 5`, `iostat -xz`, `uptime` (*load average* a 1, 5 y 15 minutos frente al número de núcleos).
  - Windows: Administrador de tareas (*Rendimiento*), **Monitor de recursos (`resmon`)** y **Monitor de rendimiento (`perfmon`)**, PowerShell `Get-Counter`.
- **Registros (*Logs*) y auditoría:**
  - Linux moderno usa **`journald`** (diario binario indexado consultable con **`journalctl`**: `journalctl -u ssh -p err -n 30`, `journalctl --since "1 hour ago"`, `journalctl -xe`) más archivos tradicionales en **`/var/log/`** (`syslog`, `auth.log`, `kern.log`, `dmesg`). La rotación automática para que no llenen `/` la gestiona **`logrotate`**.
  - Windows usa el **Visor de Eventos (`eventvwr.msc`)** dividido en *Aplicación*, *Seguridad*, *Instalación* y *Sistema*, automatizable en PowerShell con `Get-WinEvent -LogName System -MaxEvents 20`.

## 3. Necesidades del Sistema para el Desarrollo de Aplicaciones (`RA4.h`)

Al preparar una estación de desarrollo de aplicaciones (**1º/2º DAM**), el técnico debe dimensionar y configurar el SO según las cargas reales de trabajo:
- **CPU / RAM / Almacenamiento:** IDEs modernos (*IntelliJ IDEA*, *Android Studio*, *VS Code*), compiladores (*Gradle*, *Maven*, *GCC*), emuladores Android y contenedores (*Docker*) demandan almacenamiento **SSD/NVMe**, al menos **16 GB de RAM** física en anfitrión (y control de memoria al usar VirtualBox/emuladores) y 4+ núcleos con `VT-x`/`AMD-V`.
- **Configuración de variables de entorno y SDKs:** Gestión limpia de **`PATH`**, **`JAVA_HOME`**, **`ANDROID_HOME`** en `/etc/profile.d/` o `~/.bashrc` (Linux) y Variables del sistema/usuario (`[Environment]::SetEnvironmentVariable`) en Windows, evitando versiones conflictivas (uso de `update-alternatives --config java` o SDKMAN!).
- **Aislamiento y reproducibilidad:** Uso de entornos virtuales Python (`venv`), Node (`nvm`), Docker y máquinas virtuales snapshotables para no contaminar el sistema base del equipo.
