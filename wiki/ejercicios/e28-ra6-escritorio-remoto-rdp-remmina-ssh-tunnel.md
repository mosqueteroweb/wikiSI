---
ra: RA6
ce:
  - RA6.d
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md
ultima_revision: "2026-11-15"
---

# e28 · Conexión Remota Multiplataforma: RDP (`xrdp` / NLA), Remmina y Túnel Seguro SSH (`-L`)

<!-- fuente: raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md -->

## Escenario y Topología VirtualBox

El equipo técnico necesita administrar gráficamente una máquina Windows 10 desde Linux (**Remmina / FreeRDP**), así como acceder de forma segura a un servicio interno de desarrollo (o VNC en `127.0.0.1`) encapsulando el tráfico mediante un **túnel local SSH**.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e28-Ubuntu`** | Ubuntu Desktop / Server 24.04 | **2 GB** | Servidor SSH (`22`), servicio interno solo local (`8088`) y cliente `xfreerdp` |
| **`e28-Win10`** | Windows 10 Education / Pro | **4 GB** | Servidor Escritorio Remoto RDP (`3389` con NLA) y cliente túnel `ssh -L` |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Operativo dentro del presupuesto de **16 GB** de **MAX** |

## Objetivos

1. Habilitar **Escritorio Remoto (RDP)** con autenticación **NLA** obligatoria en Windows 10 y conectar desde Ubuntu/MAX usando `xfreerdp` o Remmina.
2. Levantar un servicio sensible ligado **solo a `127.0.0.1:8088`** en Ubuntu (inaccesible directamente por red) y consumirlo de forma cifrada desde Windows creando un **túnel SSH local (`ssh -L`)**.

---

## Enunciado Detallado

1. **Escritorio Remoto Windows con NLA desde Linux (`RA6.d`):**
   - En **`e28-Win10`** (`192.168.50.20`), habilita RDP mediante PowerShell asegurando que **NLA (`UserAuthentication = 1`)** y la regla de cortafuegos queden activas. Crea o usa una cuenta con contraseña válida (Windows bloquea RDP con contraseña vacía por defecto).
   - Desde **`e28-Ubuntu`** (`192.168.50.10`), establece sesión gráfica hacia **`192.168.50.20`** usando `xfreerdp` o **Remmina**.

2. **Blindaje de servicios internos con Túnel SSH `-L` (`RA6.d`):**
   - En **`e28-Ubuntu`**, ejecuta un servicio de pruebas restringido estrictamente a loopback: `python3 -m http.server 8088 --bind 127.0.0.1 &`.
   - Comprueba desde **`e28-Win10`** que el acceso directo a `http://192.168.50.10:8088` falla (protegido frente a exposición en LAN).
   - Abre desde PowerShell en **`e28-Win10`** un túnel SSH cifrado: `ssh -N -L 9000:127.0.0.1:8088 usuario@192.168.50.10`, y accede desde el navegador o PowerShell de Windows a `http://localhost:9000`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Habilitación segura de RDP (NLA) en Windows y conexión desde Ubuntu/MAX

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar cliente gráfico Remmina y herramienta de línea de comandos FreeRDP
        sudo apt-get update && sudo apt-get install -y remmina freerdp2-x11

        # Conectar vía RDP hacia e28-Win10 (sustituir usuario Windows)
        xfreerdp /v:192.168.50.20 /u:pedro /w:1280 /h:720 /cert:ignore +clipboard

        # (Opcional) Si quisiéramos instalar servidor RDP en Ubuntu Desktop para entrar DESDE Windows:
        # sudo apt-get install -y xrdp && sudo systemctl enable --now xrdp
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador en e28-Win10
        # 1. Habilitar conexiones RDP en el registro
        Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0

        # 2. Exigir Network Level Authentication (NLA = 1) obligatoria
        Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1

        # 3. Abrir regla del cortafuegos para Escritorio Remoto (adaptado a idioma ES/EN)
        Enable-NetFirewallRule -DisplayGroup "Escritorio remoto" -ErrorAction SilentlyContinue
        Enable-NetFirewallRule -DisplayGroup "Remote Desktop" -ErrorAction SilentlyContinue

        # Verificar que el puerto 3389 escucha
        Get-NetTCPConnection -LocalPort 3389 -State Listen
        ```

    ### 2. Túnel Local SSH (`-L`) para servicios restringidos a `127.0.0.1` (`RA6.d`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # En e28-Ubuntu: iniciar servidor interno accesible SOLO desde 127.0.0.1
        python3 -m http.server 8088 --bind 127.0.0.1 >/dev/null 2>&1 &
        sudo ss -tulnp | grep 8088
        # Mostrará 127.0.0.1:8088 -> inaccesible desde otros hosts sin SSH
        ```

    === "Windows 10 / 11"

        ```powershell
        # 1. Verificar que el puerto remoto 8088 NO está expuesto en la IP de LAN
        Test-NetConnection -ComputerName 192.168.50.10 -Port 8088
        # Resultado esperado: TcpTestSucceeded : False

        # 2. Abrir túnel local cifrado (mientras esta ventana siga abierta, localhost:9000 redirige por SSH)
        ssh -N -L 9000:127.0.0.1:8088 usuario@192.168.50.10

        # 3. En una SEGUNDA ventana PowerShell o navegador en Windows, probar localhost:9000:
        # Invoke-WebRequest -Uri "http://localhost:9000" -UseBasicParsing | Select-Object StatusCode
        ```

    ### Paso 4 (Ampliación): PuTTY desde Windows y Control Sin Sesión con RustDesk

    1. **SSH desde Windows con PuTTY / OpenSSH sin contraseña:** además de conectar por consola Linux, prueba la conexión desde **PuTTY** en Windows (o `ssh` nativo) configurando el par de **claves pública/privada** (`ssh-keygen` + `authorized_keys`) para iniciar sesión sin introducir la contraseña manualmente cada vez.
    2. **Administración remota y modo presentación con [RustDesk](https://rustdesk.com/):** instala RustDesk en tu equipo Windows y en otro Linux y compara ambas modalidades:
       - **Administración remota** (control completo de teclado/ratón y transferencia de archivos) entre Windows, Linux y un dispositivo móvil.
       - **Modo presentación / solo visualización** (ver qué permisos cambian cuando solo se permite observar la pantalla frente al control remoto tradicional de **VNC**).

---

## Puntos de Control y Errores Frecuentes

- **Pantalla negra con `xrdp` en Ubuntu:** En Ubuntu Desktop con GNOME, si el usuario ya mantiene una sesión gráfica abierta en la consola física de VirtualBox, `xrdp` mostrará pantalla negra al iniciar la segunda sesión simultánea. Cierra antes la sesión local del usuario o usa una cuenta distinta para RDP.
- **Confundir los puertos de `ssh -L`:** La sintaxis es `ssh -L PUERTO_TUYO_LOCAL:127.0.0.1:PUERTO_SERVICIO_EN_SERVIDOR`. Aunque ambos números suelan coincidir, en este ejercicio diferenciamos `9000` (en Windows) y `8088` (en Ubuntu) para comprobar visualmente cómo funciona la redirección.

## Recursos para Profundizar

- Concepto asociado: [Conexión y Administración Remota Segura (SSH, RDP y VNC)](../conceptos/ra6-conexion-administracion-remota-ssh-rdp-vnc.md).
- Vídeo recomendado sobre acceso remoto seguro: [SSH, RDP, cortafuegos y acceso remoto (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
