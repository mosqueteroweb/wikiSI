---
ra: RA4
ce:
  - RA4.e
  - RA4.g
  - RA4.h
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md
ultima_revision: "2026-11-15"
---

# e20 · Preparación de Estación de Desarrollo DAM: Variables de Entorno, `PATH`, Scripting y Dimensionamiento

<!-- fuente: raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md -->

## Escenario y Topología VirtualBox

Un alumno de **1.º DAM** comienza el segundo trimestre y necesita dejar su sistema listo para desarrollar en **Java (OpenJDK 21)**, **Python** y **Git**, automatizando un pequeño script de verificación de entorno y documentando las necesidades reales de hardware y software de su equipo de desarrollo frente al equipo de pruebas virtualizado.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e20-Ubuntu-Dev`** | Ubuntu Desktop / Server 24.04 | **2 GB** | Variables `JAVA_HOME`/`PATH`, entornos Python `venv`, script Bash de chequeo |
| **`e20-Win10-Dev`** | Windows 10 Education / Pro | **4 GB** | Variables de entorno de usuario/sistema, `winget`, script PowerShell de validación |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Respeta el presupuesto **MAX 16 GB** del aula |

## Objetivos

1. Configurar de forma **persistente** las variables de entorno `JAVA_HOME` y `PATH` tanto en sesión Bash como en Windows sin sobrescribir la ruta global del sistema.
2. Evaluar un script ejecutable (`check_dev.sh` / `Check-Dev.ps1`) con permisos de ejecución y código de retorno correcto.
3. Elaborar una matriz técnica de dimensionamiento (`RA4.h`) para una estación de trabajo **1.º DAM** (IDE + JDK + Docker/BD + navegador + VM).

---

## Enunciado Detallado

1. **Variables de entorno y herramientas de desarrollo (`RA4.e`, `RA4.h`):**
   - Instala **OpenJDK 21** (`openjdk-21-jdk` en Ubuntu) y **Git**, además de `python3-venv` en Linux.
   - Localiza la ruta exacta del ejecutable `javac` y define la variable `JAVA_HOME` de forma persistente (en `~/.bashrc` en Ubuntu y mediante `[Environment]::SetEnvironmentVariable` de ámbito `User` en Windows) añadiendo `$JAVA_HOME/bin` al `PATH` sin destruir el resto de rutas.
   - Crea un entorno virtual aislado de Python en `~/proyectos/venv_dam` (o `C:\Proyectos\venv_dam`) para evitar instalar librerías en el Python global del sistema.

2. **Automatización mediante script administrativo (`RA4.e`):**
   - Escribe un script llamado `check_dev.sh` (Linux) y `Check-Dev.ps1` (Windows) que compruebe: la versión de `java`, la versión de `git`, el espacio libre disponible en `/` o `C:\` y si `JAVA_HOME` está definida; en Linux debe tener permisos `750` y encabezarse con `#!/usr/bin/env bash`.

3. **Evaluación de necesidades del sistema para desarrollo (`RA4.h`):**
   - Completa la tabla comparativa calculando la memoria RAM mínima vs recomendada cuando el desarrollador ejecuta simultáneamente IntelliJ IDEA, un contenedor PostgreSQL, navegador con documentación y una VM ligera de pruebas.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Instalación de SDKs y variables persistentes `JAVA_HOME` y `PATH`

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar OpenJDK 21, Git y soporte de entornos virtuales Python
        sudo apt-get update && sudo apt-get install -y openjdk-21-jdk git python3-venv

        # Localizar el directorio raíz del JDK resolviendo enlaces simbólicos
        dirname "$(dirname "$(readlink -f "$(which javac)")")"
        # En Ubuntu x86_64 suele ser: /usr/lib/jvm/java-21-openjdk-amd64

        # Añadir persistencia al final de ~/.bashrc (sin duplicar si se ejecuta una vez)
        cat <<'EOF' >> ~/.bashrc
        export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
        export PATH="$JAVA_HOME/bin:$PATH"
        EOF

        # Recargar la sesión actual y comprobar variables
        source ~/.bashrc
        echo "JAVA_HOME=$JAVA_HOME"
        java -version
        git --version

        # Crear entorno virtual Python aislado para no ensuciar el sistema
        mkdir -p ~/proyectos
        python3 -m venv ~/proyectos/venv_dam
        source ~/proyectos/venv_dam/bin/activate
        python3 --version
        deactivate
        ```

    === "Windows 10 / 11"

        ```powershell
        # Instalar Git y Temurin OpenJDK 21 con winget (o comprobar si ya están presentes)
        winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements
        winget install --id EclipseAdoptium.Temurin.21.JDK -e --accept-package-agreements --accept-source-agreements

        # Definir JAVA_HOME de ámbito Usuario de forma persistente (sin borrar PATH global)
        $jdkPath = (Get-ChildItem "C:\Program Files\Eclipse Adoptium\jdk-21*" | Select-Object -First 1).FullName
        if ($jdkPath) {
            [Environment]::SetEnvironmentVariable("JAVA_HOME", $jdkPath, "User")
            $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
            if ($userPath -notlike "*$jdkPath\bin*") {
                [Environment]::SetEnvironmentVariable("Path", "$jdkPath\bin;$userPath", "User")
            }
        }

        # Crear entorno virtual Python si python está instalado
        New-Item -Path "C:\Proyectos" -ItemType Directory -Force | Out-Null
        ```

    ### 2. Script de validación del entorno de desarrollo (`RA4.e`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        cat <<'EOF' > ~/proyectos/check_dev.sh
        #!/usr/bin/env bash
        set -euo pipefail

        echo "=== Verificacion Entorno DAM ==="
        if [ -z "${JAVA_HOME:-}" ]; then
            echo "[ERROR] JAVA_HOME no esta definida" >&2
            exit 1
        fi
        echo "JAVA_HOME: $JAVA_HOME"
        java -version 2>&1 | head -n 1
        git --version
        echo "Espacio libre en raiz (/): $(df -h / | awk 'NR==2 {print $4}')"
        EOF

        # Dar permiso de ejecución solo al propietario y lectura al grupo (750)
        chmod 750 ~/proyectos/check_dev.sh
        ~/proyectos/check_dev.sh
        ```

    === "Windows 10 / 11"

        ```powershell
        $scriptContent = @'
        Write-Host "=== Verificacion Entorno DAM ==="
        $jhome = [Environment]::GetEnvironmentVariable("JAVA_HOME", "User")
        if ([string]::IsNullOrEmpty($jhome)) {
            Write-Error "JAVA_HOME no esta definida"
            exit 1
        }
        Write-Host "JAVA_HOME: $jhome"
        git --version
        $c = Get-PSDrive C
        Write-Host ("Espacio libre C:\ : {0:N2} GB" -f ($c.Free / 1GB))
        '@

        Set-Content -Path "C:\Proyectos\Check-Dev.ps1" -Value $scriptContent -Encoding UTF8
        powershell -ExecutionPolicy Bypass -File "C:\Proyectos\Check-Dev.ps1"
        ```

    ### 3. Matriz de evaluación de requisitos para desarrollo DAM (`RA4.h`)

    | Carga simultánea habitual | Consumo RAM típico | Implicación en PC de **16 GB (MAX)** | Recomendación técnica (`RA4.h`) |
    | :--- | :---: | :--- | :--- |
    | **SO Anfitrión MAX + entorno gráfico** | ~2,5 GB | Base residente | Mantener servicios no usados detenidos |
    | **IDE Java / Kotlin (IntelliJ IDEA + Gradle)** | 2,5 – 4,0 GB | Pico al indexar proyectos | Ajustar `-Xmx` del IDE y excluir `target/`/`build/` del indexado |
    | **Contenedor BD (PostgreSQL / MySQL) o servidor local** | 0,5 – 1,5 GB | Ligero si está contenerizado | Arrancar contenedores solo bajo demanda |
    | **Navegador técnico + documentación** | 1,5 – 2,5 GB | Sube rápido con muchas pestañas | Evitar fugas cerrando pestañas pesadas |
    | **1 o 2 VMs de pruebas en VirtualBox** | 2,0 – 6,0 GB | Margen crítico del aula | No superar **6–7 GB** para conservar $\ge 4\text{ GB}$ libres al anfitrión + IDE |
    | **Total combinado recomendado** | **10 – 14 GB** | **16 GB mínimos en DAM**; **32 GB ideales** | Imprescindible **SSD NVMe ($\ge 512\text{ GB}$)** para compilaciones y VMs |

    ### 4. Reto de Tuberías (`cut`/`sed`/`awk`) y Búsqueda con `2>/dev/null`

    1. **Filtro de registros en un solo comando:** crea el fichero `viaje.txt` desde terminal (sin editor gráfico) con líneas mixtas de mayúsculas/minúsculas (`ALUMNO1: 7 no Viaja`, `ALUMNO2: 5 VIAJA`, `ALUMNO3: 8 NO VIAJA`, `ALUMNO4: 2 no viaja`). Usando una tubería única (`grep -i`, `sort`, `head`, `cut`/`awk`), obtén exclusivamente el nombre del alumno con **menor nota entre los que no viajan** (`ALUMNO4`).
    2. **Auditoría silenciosa de ejecutables:** lista con permisos los ficheros regulares ejecutables pertenecientes a usuarios cuyo nombre empiece por `prof*` en todo `/` ocultando los errores de acceso (`find / -type f -user "prof*" -perm /111 -ls 2>/dev/null`).

    ### 5. Taller Práctico Docker: Nginx, MySQL y App Web PHP + Monitorización

    Sobre tu Ubuntu (`e20-Ubuntu`) con Docker Engine instalado y tu usuario dentro del grupo `docker`:

    1. Lanza un contenedor **Nginx** mapeando el puerto `-p 8080:80` y comprueba con `curl http://localhost:8080` y `docker ps`.
    2. Despliega un contenedor **MySQL** con contraseña y conéctate mediante cliente (`mysql -h 127.0.0.1 -u root -p`).
    3. **Reto integrador (App + BD + Monitorización):** levanta con **Docker Compose** un formulario web PHP que guarde nombre y edad en MySQL (usando un **volumen persistente** y una **red Docker compartida**) y añade un contenedor de monitorización de recursos de los contenedores activos (`docker stats` / cAdvisor / Portainer).

---

## Puntos de Control y Errores Frecuentes

- **Sobrescribir `$PATH` por descuido:** Al añadir un binario al `PATH`, incluir siempre `:$PATH` al final en Linux o leer primero el `Path` existente en Windows; escribir `export PATH="/mi/ruta"` a secas hace desaparecer `ls`, `sudo` y todas las órdenes básicas en la sesión activa.
- **Instalar paquetes `pip` en global:** Las distribuciones recientes (Ubuntu 24.04) bloquean `pip install` global por la **PEP 668 (`externally-managed-environment`)** precisamente para proteger las herramientas internas del SO. Usar `python3 -m venv` es obligatorio.

## Recursos para Profundizar

- Concepto asociado: [Comandos de administración, variables y scripting](../conceptos/ra4-comandos-administracion-variables-scripting.md) y [Monitorización, logs y optimización del entorno DAM](../conceptos/ra4-monitorizacion-logs-optimizacion-entorno-dam.md).
- Referencia del lenguaje Bash y entorno: [GNU Bash Manual](https://www.gnu.org/software/bash/manual/).
- Vídeo recomendado sobre comandos y monitorización: [Administración en consola Linux y variables (YouTube)](https://www.youtube.com/watch?v=dx-ixZOnkpQ).
