---
title: "RA4 · Comandos de Administración, Redirecciones y Variables de Entorno"
ra: ["RA4"]
ce: ["RA4.e", "RA4.h"]
tipo: "concepto"
publicar: true
fuentes:
  - "raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md"
ultima_revision: "2026-11-15"
---

# Comandos de Administración, Redirecciones y Variables de Entorno

<!-- fuente: raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md -->

> **Criterios de evaluación cubiertos:** `RA4.e` (uso de comandos en tareas básicas de configuración y administración) y `RA4.h` (configuración del entorno para desarrollo de aplicaciones).

Dominar la línea de comandos (**Bash** en GNU/Linux y **PowerShell** en Windows) multiplica la velocidad de administración y permite automatizar configuraciones repetitivas mediante tuberías, redirecciones y variables de entorno.

---

## 1. Flujos Estándar, Redirecciones y Tuberías (`|`) (`RA4.e`)

<!-- fuente: raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md -->

Todo proceso en Linux (y consola Windows) dispone de tres descriptores estándar:
- **`stdin` (0):** Entrada estándar (normalmente teclado).
- **`stdout` (1):** Salida estándar (pantalla).
- **`stderr` (2):** Salida de errores (pantalla).

### Composición mediante operadores
- **`>`** y **`>>`**: Redirigen `stdout` a un archivo (sobrescribiendo o añadiendo al final respectivamente).
- **`2>`** y **`2>&1`**: Redirigen errores (`stderr`) o unen errores al flujo estándar.
- **`|` (*Pipe / Tubería*):** Conecta el `stdout` de un comando directamente como `stdin` del siguiente. En **Bash** viajan flujos de texto; en **PowerShell**, viajan **objetos tipados** completos con propiedades y métodos.

=== "MAX / Ubuntu (Bash)"
    ```bash
    # Filtrar errores de permiso al buscar en /etc y contar líneas encontradas
    find /etc -name "*.conf" 2>/dev/null | wc -l

    # Ordenar usuarios reales del sistema por UID y guardar resultado con fecha
    awk -F: '$3 >= 1000 {print $1, $3}' /etc/passwd | sort -k2 -n > ~/usuarios_locales.txt

    # Encadenar con && (ejecuta solo si el anterior tuvo éxito) o || (si falló)
    mkdir -p /tmp/compilacion && cd /tmp/compilacion && pwd

    # Ver simultáneamente salida en pantalla y guardarla en archivo (tee)
    ip -brief address | tee ~/red_actual.log
    ```

=== "Windows 10 / 11 (PowerShell)"
    ```powershell
    # Pipeline orientado a objetos: filtrar, ordenar y exportar a CSV limpio
    Get-Service |
      Where-Object { $_.Status -eq 'Running' } |
      Sort-Object DisplayName |
      Select-Object Name, DisplayName -First 10 |
      Export-Csv -Path "$env:USERPROFILE\Desktop\servicios_activos.csv" -NoTypeInformation

    # Ver salida en consola y enviarla a archivo al mismo tiempo (Tee-Object)
    Get-NetIPAddress -AddressFamily IPv4 | Tee-Object -FilePath "$env:TEMP\ips.txt"
    ```

---

## 2. Variables de Entorno (`PATH`, `JAVA_HOME`, Perfil de Usuario) (`RA4.e`, `RA4.h`)

<!-- fuente: raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md -->

Las **variables de entorno** permiten a las aplicaciones y herramientas CLI localizar compiladores, SDKs, idioma o rutas de ejecución sin escribir rutas fijas:

| Variable clave | Función en el sistema / entorno de desarrollo DAM |
| :--- | :--- |
| **`PATH`** | Lista de directorios separados por `:` (Linux) o `;` (Windows) donde la shell busca comandos al escribir su nombre |
| **`HOME`** / **`USERPROFILE`** | Ruta del directorio personal del usuario conectado |
| **`JAVA_HOME`** / **`ANDROID_HOME`** | Ruta raíz donde reside el JDK o Android SDK para compilaciones Maven/Gradle |
| **`LANG`** / **`LC_ALL`** | Configuración regional y codificación de caracteres (ej. `es_ES.UTF-8`) |

=== "MAX / Ubuntu (Linux)"
    ```bash
    # Inspeccionar variables actuales
    env | grep -E "PATH|HOME|LANG|USER"
    echo "$PATH"

    # Definir variable temporal en la sesión actual
    export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
    export PATH="$JAVA_HOME/bin:$PATH"

    # Hacerla persistente para el usuario en ~/.bashrc (o global para todos en /etc/profile.d/dam_env.sh)
    echo 'export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"' >> ~/.bashrc
    echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

=== "Windows 10 / 11"
    ```powershell
    # Consultar variables de entorno actuales
    Get-ChildItem Env: | Where-Object Name -in "PATH","USERNAME","OS"
    $env:PATH -split ';'

    # Variable temporal (solo sesión abierta):
    $env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21"

    # Variable persistente a nivel de Usuario ("User") o Sistema ("Machine", requiere Admin):
    [Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Eclipse Adoptium\jdk-21", "User")
    ```

---

## 3. Equivalencia Rápida de Comandos Administrativos (`RA4.e`)

| Operación administrativa | GNU/Linux (MAX / Ubuntu) | Windows (PowerShell / CMD) |
| :--- | :--- | :--- |
| **Nombre equipo y versión SO** | `hostnamectl` / `uname -a` | `hostname` / `Get-ComputerInfo` |
| **Espacio libre en disco** | `df -h` / `du -sh *` | `Get-Volume` / `Get-PSDrive` |
| **Apagar / Reiniciar inmediato** | `sudo poweroff` / `sudo reboot` | `Stop-Computer` / `Restart-Computer` (`shutdown /r /t 0`) |
| **Consultar manual o ayuda** | `man <cmd>` / `<cmd> --help` | `Get-Help <cmdlet> -Examples` / `<cmd> /?` |

---

## Recursos para profundizar

- **Documentación oficial:** [GNU Bash Reference Manual (Redirections)](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) y [Microsoft Learn: About Environment Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables).
- **Vídeo recomendado:** [Dominando la consola Linux: tuberías, redirecciones y administración base](https://www.youtube.com/watch?v=dx-ixZOnkpQ).
- **Siguiente tema:** [Monitorización, Registros de Eventos, Optimización y Necesidades para Desarrollo DAM](ra4-monitorizacion-logs-optimizacion-entorno-dam.md).
