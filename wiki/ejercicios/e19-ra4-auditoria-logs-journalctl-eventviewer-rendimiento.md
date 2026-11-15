---
ra: RA4
ce:
  - RA4.f
  - RA4.g
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md
ultima_revision: "2026-11-15"
---

# e19 · Auditoría de Logs (`journalctl` / Visor de Eventos) y Monitorización de Rendimiento

<!-- fuente: raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md -->

## Escenario y Topología VirtualBox

Un servidor de prácticas muestra ralentizaciones puntuales y varios intentos fallidos de acceso administrativo. Tu misión como administrador junior es correlacionar el consumo de recursos (CPU, memoria, entrada/salida) con los registros del sistema (**`systemd-journald`** en Ubuntu y **Event Viewer / `Get-WinEvent`** en Windows) y aplicar tareas de limpieza y mantenimiento preventivo.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e19-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | `journalctl`, `/var/log/auth.log`, `free`, `vmstat`, `iostat`, limpieza de cachés `apt` |
| **`e19-Win10`** | Windows 10 Education / Pro | **4 GB** | `Get-WinEvent`, `Get-Counter`, `perfmon` y análisis de arranque/servicios |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Preserva más del 50 % de RAM libre en el equipo **MAX (16 GB)** |

## Objetivos

1. Consultar registros filtrados por **unidad (`-u`)**, **prioridad (`-p err`)** y **rango temporal (`--since`)** con `journalctl`, además de localizar eventos de seguridad en Windows (`4624` / `4625` o eventos de error de sistema).
2. Capturar métricas en tiempo real de CPU, paginación y disco (`free -h`, `vmstat`, `htop` / `Get-Counter`).
3. Instalar utilidades de diagnóstico (`htop`, `sysstat`, `ncdu`) y optimizar espacio de sistema eliminando paquetes obsoletos y rotando journals antiguos.

---

## Enunciado Detallado

1. **Investigación de logs de sistema y seguridad (`RA4.f`):**
   - Provoca un intento controlado fallido de `sudo` o `su` con una contraseña incorrecta y localiza exactamente la línea de registro que lo audita en Linux (`journalctl` o `/var/log/auth.log`).
   - En Linux, lista los errores graves (`-p err`) producidos desde el arranque actual (`-b`) y extrae los últimos 20 mensajes del servicio `ssh` (o `systemd-logind`).
   - En Windows, consulta con PowerShell (`Get-WinEvent`) los 10 errores o advertencias más recientes del registro **System** y filtra si existen eventos de inicio de sesión fallidos (**Event ID 4625**) o exitosos (**4624**) en **Security**.

2. **Monitorización de CPU, memoria y disco (`RA4.f`, `RA4.g`):**
   - Instala `htop`, `sysstat` y `ncdu` en Ubuntu.
   - Analiza el uso real de memoria (diferenciando *used* de *buff/cache* y *available* con `free -h`), registra 5 muestras cada 2 segundos de `vmstat 2 5` e identifica qué directorio dentro de `/var` ocupa más espacio con `ncdu` o `du -sh`.
   - En Windows, mide con `Get-Counter` el porcentaje instantáneo de procesador y los MB de memoria disponible.

3. **Mantenimiento y optimización (`RA4.g`):**
   - Verifica el tamaño actual de los registros de `journald` y límpialos dejando como máximo **100 MB** (`--vacuum-size=100M`), además de limpiar la caché de paquetes `apt` (`apt autoremove` y `apt clean`).

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Auditoría de logs con `journalctl` y `Get-WinEvent` (`RA4.f`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Simular fallo de autenticación controlado para verificar trazabilidad
        su -c "true" root <<< "clave_incorrecta" 2>/dev/null || true

        # Consultar registros de autenticación en los últimos 5 minutos
        sudo journalctl --since "5 minutes ago" | grep -E "authentication failure|FAILED SU|sudo"

        # Listar errores críticos o de prioridad err en el arranque actual (-b)
        sudo journalctl -b -p err --no-pager | tail -n 25

        # Filtrar por unidad concreta (ej. systemd-logind o ssh)
        sudo journalctl -u systemd-logind -n 20 --no-pager
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador
        # 10 últimos eventos de Error (Level 2) o Crítico (Level 1) en el log System
        Get-WinEvent -FilterHashtable @{ LogName = 'System'; Level = 1,2 } -MaxEvents 10 |
            Format-Table TimeCreated, Id, ProviderName, Message -Wrap

        # Consultar últimos 5 inicios de sesión exitosos (4624) o fallidos (4625) en Security
        Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4624,4625 } -MaxEvents 5 -ErrorAction SilentlyContinue |
            Select-Object TimeCreated, Id, @{N='MensajeCorto';E={($_.Message -split "`n")[0]}}
        ```

    ### 2. Instalación de utilidades y métricas de rendimiento (`RA4.f`, `RA4.g`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar herramientas profesionales de diagnóstico y análisis de espacio
        sudo apt-get update && sudo apt-get install -y htop sysstat ncdu

        # Revisar RAM real disponible (la columna 'available' incluye caché recuperable)
        free -h

        # Tomar 5 muestras separadas por 2 segundos de CPU, colas de procesos y swap (si/so)
        vmstat 2 5

        # Analizar qué subdirectorios de /var consumen más disco (modo no interactivo con du)
        sudo du -h --max-depth=1 /var | sort -hr | head -n 10
        # También puedes lanzar de forma interactiva: sudo ncdu /var
        ```

    === "Windows 10 / 11"

        ```powershell
        # Tomar 3 muestras cada 2 segundos de CPU total y RAM disponible (MB)
        Get-Counter -Counter @(
            "\Processor(_Total)\% Processor Time",
            "\Memory\Available MBytes"
        ) -SampleInterval 2 -MaxSamples 3

        # Top 5 procesos por consumo de memoria física (WorkingSet en MB)
        Get-Process | Sort-Object WorkingSet64 -Descending |
            Select-Object -First 5 Name, Id, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64 / 1MB, 1)}}
        ```

    ### 3. Mantenimiento y optimización de almacenamiento (`RA4.g`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Inspeccionar uso en disco actual de los diarios de systemd
        journalctl --disk-usage

        # Reducir logs históricos conservando un límite máximo de 100 MB
        sudo journalctl --vacuum-size=100M

        # Limpiar dependencias huérfanas y caché de paquetes .deb descargados
        sudo apt-get autoremove -y
        sudo apt-get clean
        df -h /
        ```

    === "Windows 10 / 11"

        ```powershell
        # Limpiar archivos temporales del usuario de forma segura y verificar espacio libre en C:
        Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
        Get-PSDrive -Name C | Select-Object Name,
            @{N='Usado_GB';E={[math]::Round($_.Used / 1GB, 2)}},
            @{N='Libre_GB';E={[math]::Round($_.Free / 1GB, 2)}}
        ```

---

## Puntos de Control y Errores Frecuentes

- **Falsa alarma con `free -h`:** Ver muy poca RAM en `free` no significa falta de memoria en Linux; el kernel aprovecha la RAM ociosa en **buff/cache** para acelerar lecturas de disco. El valor crítico que indica saturación real es **`available`**, junto con actividad continua de `si`/`so` (swap in / swap out) en `vmstat`.
- **Nunca usar `rm` sobre `/var/log/journal/` manualmente:** Borrar ficheros binarios `.journal` a mano puede corromper el índice de registros activos; utiliza siempre `journalctl --vacuum-size=...` o `--vacuum-time=...`.

## Recursos para Profundizar

- Concepto asociado: [Monitorización, logs y optimización del entorno DAM](../conceptos/ra4-monitorizacion-logs-optimizacion-entorno-dam.md).
- Documentación de `journalctl`: [ArchWiki · Systemd/Journal](https://wiki.archlinux.org/title/Systemd/Journal).
- Vídeo recomendado sobre monitorización y logs: [Monitorización, systemd y diagnóstico en consola Linux (YouTube)](https://www.youtube.com/watch?v=dx-ixZOnkpQ).
