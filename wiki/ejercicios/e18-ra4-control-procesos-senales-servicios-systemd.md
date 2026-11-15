---
ra: RA4
ce:
  - RA4.c
  - RA4.e
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md
ultima_revision: "2026-11-15"
---

# e18 · Control de Procesos, Señales (`kill`/`nice`) y Servicios (`systemd` / PowerShell)

<!-- fuente: raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md -->

## Escenario y Topología VirtualBox

Durante las pruebas de un servidor web interno en 1.º DAM, un script de laboratorio entra en bucle infinito consumiendo CPU mientras un servicio de base de datos o servidor web requiere diagnóstico y ajuste en el arranque automático. Trabajarás sobre una pareja de VMs dentro del presupuesto de RAM del aula:

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e18-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | Procesos en primer/segundo plano, `nice`/`renice`, señales `SIGTERM`/`SIGKILL` y `systemd` |
| **`e18-Win10`** | Windows 10 Education / Pro | **4 GB** | Procesos y servicios con `Get-Process`, `Get-Service` y `sc.exe` / Administrador de tareas |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Dentro del rango seguro (**2–7 GB**) sobre anfitrión **MAX 16 GB** |

## Objetivos

1. Lanzar procesos en segundo plano (`&`), gestionarlos con `jobs`, `bg`, `fg` y alterar su prioridad de planificación (`nice` / `renice`).
2. Distinguir en la práctica el envío ordenado de **`SIGTERM` (`-15`)** frente a la terminación forzada **`SIGKILL` (`-9`)** mediante PID.
3. Instalar o gestionar un servicio estándar (`nginx` o `ssh` en Linux; servicio de impresión `Spooler` o servicio SSH en Windows) con `systemctl` y PowerShell (`Start-Service`, `Set-Service`).

---

## Enunciado Detallado

1. **Gestión de trabajos, prioridades y señales (`RA4.c`, `RA4.e`):**
   - En Linux, lanza dos procesos benignos en segundo plano: `sleep 600 &` y un bucle controlado de baja prioridad con `nice -n 15 yes > /dev/null &`.
   - Localiza sus **PID** con `ps aux` y `pgrep -a`. Comprueba el consumo de CPU del proceso `yes` con `top -n 1` o `ps -eo pid,ni,pcpu,comm --sort=-pcpu | head`.
   - Modifica la prioridad del proceso `sleep` a `nice = 10` con `renice`.
   - Envía una señal limpia `SIGTERM` (`kill -15`) a `sleep` y termina `yes` comprobando su desaparición.

2. **Gestión del ciclo de vida de servicios (`RA4.c`, `RA4.e`):**
   - En Ubuntu, instala `nginx` (o usa `ssh` si ya está disponible), detén el servicio, comprueba su estado (`status`), arráncalo de nuevo, habilítalo para el arranque automático (`enable`) y finalmente recarga su configuración sin cortar conexiones activas (`reload`). Muestra también qué unidad de arranque lo controla (`systemctl cat nginx`).
   - En Windows, consulta el estado del servicio `Spooler` (*Cola de impresión*) desde PowerShell, cambia su tipo de inicio a `Manual`, detenlo, arráncalo de nuevo y devuélvelo a `Automatic`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Trabajos en segundo plano, prioridades (`nice`/`renice`) y señales (`RA4.c`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Lanzar proceso sleep en segundo plano y proceso intensivo con baja prioridad (niceness +15)
        sleep 600 &
        nice -n 15 yes > /dev/null &

        # Listar trabajos de la shell actual y sus PIDs reales
        jobs -l
        pgrep -a "sleep|yes"

        # Consultar prioridad (NI) y porcentaje de CPU
        ps -eo pid,ppid,ni,stat,pcpu,comm --sort=-pcpu | head -n 10

        # Ajustar prioridad del proceso sleep (sustituir PID_SLEEP por el obtenido)
        PID_SLEEP=$(pgrep -n sleep)
        renice -n 10 -p "$PID_SLEEP"
        ps -o pid,ni,comm -p "$PID_SLEEP"

        # Enviar SIGTERM (-15) de terminación ordenada
        kill -15 "$PID_SLEEP"

        # Terminar también el proceso yes (si quedase atascado en código real usaríamos -9 SIGKILL)
        pkill -15 yes

        # Confirmar que no quedan procesos activos
        pgrep -a "sleep|yes" || echo "Procesos cerrados correctamente"
        ```

    === "Windows 10 / 11"

        ```powershell
        # Lanzar un proceso de prueba en segundo plano (Notepad o PowerShell durmiente)
        $proc = Start-Process -FilePath "notepad.exe" -PassThru
        Write-Host "PID asignado:" $proc.Id

        # Inspeccionar prioridad base y uso de CPU
        Get-Process -Id $proc.Id | Select-Object Id, ProcessName, PriorityClass, CPU

        # Reducir prioridad equivalente a 'nice'
        (Get-Process -Id $proc.Id).PriorityClass = "BelowNormal"
        Get-Process -Id $proc.Id | Select-Object Id, ProcessName, PriorityClass

        # Cierre ordenado equivalente a SIGTERM (CloseMainWindow) vs cierre forzado (Stop-Process)
        $proc.CloseMainWindow() | Out-Null
        Start-Sleep -Seconds 2
        if (-not $proc.HasExited) {
            Stop-Process -Id $proc.Id -Force
        }
        ```

    ### 2. Ciclo de vida de servicios (`systemd` y PowerShell) (`RA4.c`, `RA4.e`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar servicio ligero de demostración (si no estuviese presente)
        sudo apt-get update && sudo apt-get install -y nginx

        # Inspeccionar estado actual y si arranca con el sistema
        systemctl status nginx --no-pager
        systemctl is-enabled nginx

        # Detener, comprobar parada y volver a iniciar
        sudo systemctl stop nginx
        systemctl is-active nginx || echo "Servicio detenido"

        sudo systemctl start nginx
        sudo systemctl enable nginx

        # Recargar configuración sin interrumpir el PID principal (si la unidad lo soporta)
        sudo systemctl reload nginx

        # Inspeccionar el archivo .service real que usa systemd
        systemctl cat nginx --no-pager
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador
        Get-Service -Name "Spooler" | Select-Object Name, Status, StartType

        # Cambiar inicio a Manual y detener el servicio
        Set-Service -Name "Spooler" -StartupType Manual
        Stop-Service -Name "Spooler" -Force
        Get-Service -Name "Spooler" | Select-Object Name, Status, StartType

        # Volver a arrancarlo y restaurar arranque Automático
        Start-Service -Name "Spooler"
        Set-Service -Name "Spooler" -StartupType Automatic
        Get-Service -Name "Spooler" | Select-Object Name, Status, StartType
        ```

---

## Puntos de Control y Errores Frecuentes

- **`reload` vs `restart`:** `systemctl restart` destruye el proceso maestro y arranca otro con nuevo PID (corta conexiones abiertas brevemente), mientras `systemctl reload` envía `SIGHUP` al demonio para releer su configuración sin caer.
- **Abuso de `kill -9` (`SIGKILL`):** Enviar `-9` impide que bases de datos o aplicaciones graben sus cachés a disco o eliminen ficheros `.lock`/`.pid`. En administración profesional siempre se intenta primero `kill -15` (`SIGTERM`).
- **Servicios dependientes en Windows:** Al detener servicios con dependencias (por ejemplo `wuauserv` o servicios de red), PowerShell puede requerir `-Force` o parar primero sus servicios hijos mediante `Get-Service -DependentServices`.

## Recursos para Profundizar

- Concepto asociado: [Gestión de procesos y servicios (systemd y Windows)](../conceptos/ra4-gestion-procesos-servicios-systemd-windows.md).
- Manual oficial `systemctl`: [Freedesktop systemd docs](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html).
- Vídeo recomendado sobre procesos y servicios: [Gestión de procesos, servicios systemd y consola en Linux (YouTube)](https://www.youtube.com/watch?v=dx-ixZOnkpQ).
