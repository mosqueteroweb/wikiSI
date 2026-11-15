---
ra: RA5
ce:
  - RA5.c
  - RA5.f
  - RA5.g
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md
ultima_revision: "2026-11-15"
---

# e24 · Auditoría de Puertos (`ss`/`Get-NetTCPConnection`) y Diagnóstico *Bottom-Up* de Fallos de Red

<!-- fuente: raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md -->

## Escenario y Topología VirtualBox

Un compañero de proyecto despliega un servidor HTTP sencillo en Python sobre **`e24-Ubuntu`**, pero al probar desde **`e24-Win10`** la página no carga. Aplicaremos sistemáticamente la metodología ascendente (*bottom-up*) y la inspección de sockets para encontrar la causa raíz exacta.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e24-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | Servidor de pruebas (`ss -tulnp`, `tcpdump`, `python3 -m http.server`) |
| **`e24-Win10`** | Windows 10 Education / Pro | **4 GB** | Cliente diagnóstico (`Test-NetConnection`, `Resolve-DnsName`, `Get-NetTCPConnection`) |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Respeta el margen de aula en **MAX 16 GB** |

## Objetivos

1. Distinguir entre un servicio escuchando en **`127.0.0.1` (solo local)** frente a **`0.0.0.0` (todas las interfaces)** mediante `ss -tulnp`.
2. Diagnosticar paso a paso conectividad IP, resolución DNS y disponibilidad de puerto TCP desde Linux y Windows.
3. Realizar una captura breve de paquetes con `tcpdump` para observar solicitudes reales en tránsito.

---

## Enunciado Detallado

1. **Simulación del fallo clásico de enlace (`127.0.0.1` vs `0.0.0.0`):**
   - En **`e24-Ubuntu`** (con Red Interna o Solo-anfitrión, IP ejemplo `192.168.50.10`), arranca un servidor web de pruebas ligado **únicamente a localhost**: `python3 -m http.server 8080 --bind 127.0.0.1 &`.
   - Comprueba con `ss -tulnp` qué dirección aparece en la columna `Local Address:Port` e intenta conectar desde **`e24-Win10`** con `Test-NetConnection -ComputerName 192.168.50.10 -Port 8080`.
   - Detén el proceso, relánzalo escuchando en todas las interfaces (`0.0.0.0`) y verifica de nuevo desde Windows.

2. **Batería de diagnóstico de red y puertos (`RA5.f`, `RA5.g`):**
   - Lista todos los puertos TCP/UDP abiertos en escucha junto a su proceso propietario en **ambos sistemas operativos**.
   - Diagnostica un fallo simulado de DNS (consultando con `dig @1.1.1.1` frente a la configuración local) y captura 6 paquetes TCP del puerto `8080` mediante `tcpdump` mientras realizas una petición HTTP desde el otro equipo.
   - Si trabajas desde un portátil real en casa o aula Wi-Fi, documenta también cómo comprobar la banda/canal inalámbrico actual (`nmcli dev wifi list` / `netsh wlan show interfaces`).

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Diagnóstico del enlace `127.0.0.1` vs `0.0.0.0` (`RA5.f`, `RA5.g`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Paso 1: Arrancar servidor web ligado erróneamente solo a loopback (127.0.0.1)
        python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &
        PID_HTTP=$!

        # Inspeccionar socket en escucha: observar Local Address = 127.0.0.1:8080
        sudo ss -tulnp | grep 8080

        # En este estado, cualquier conexión desde otra máquina será rechazada (Connection refused)
        # Paso 2: Parar proceso y arrancar escuchando en todas las interfaces (0.0.0.0)
        kill -15 "$PID_HTTP"
        python3 -m http.server 8080 --bind 0.0.0.0 >/dev/null 2>&1 &
        PID_HTTP=$!

        # Verificar cambio a 0.0.0.0:8080 o *:8080
        sudo ss -tulnp | grep 8080

        # Comprobar localmente antes de pasar al cliente Windows
        nc -zv 192.168.50.10 8080
        ```

    === "Windows 10 / 11"

        ```powershell
        # Probar puerto 8080 cuando el servidor escucha en 127.0.0.1 -> TcpTestSucceeded : False
        # Tras corregir a 0.0.0.0 -> TcpTestSucceeded : True
        Test-NetConnection -ComputerName 192.168.50.10 -Port 8080

        # Descargar cabeceras HTTP para verificar respuesta de capa de aplicación
        Invoke-WebRequest -Uri "http://192.168.50.10:8080" -UseBasicParsing | Select-Object StatusCode

        # Listar todos los puertos TCP en escucha en Windows y su proceso dueño
        Get-NetTCPConnection -State Listen |
          Select-Object LocalAddress, LocalPort, OwningProcess,
          @{N='Proceso';E={(Get-Process -Id $_.OwningProcess).ProcessName}} |
          Sort-Object LocalPort
        ```

    ### 2. Diagnóstico DNS, captura de tráfico e información Wi-Fi (`RA5.c`, `RA5.g`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Verificación DNS directa frente a servidor público (aísla si el fallo es DNS local)
        dig @1.1.1.1 wikipedia.org +short

        # Capturar en tiempo real el handshake y cabeceras HTTP en puerto 8080
        # (ejecutar y mientras tanto lanzar petición desde Windows o curl)
        sudo tcpdump -i enp0s8 port 8080 -n -c 6

        # Limpiar el proceso de prueba cuando terminemos
        pkill -15 -f "http.server 8080"

        # Consulta de redes y canal Wi-Fi en equipo portátil o host MAX
        nmcli device wifi list
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar resolución DNS explícita y estado de enlace Wi-Fi en portátiles
        Resolve-DnsName wikipedia.org -Server 1.1.1.1
        netsh wlan show interfaces
        ```

---

## Puntos de Control y Errores Frecuentes

- **`127.0.0.1` no es alcanzable desde la red:** Es el error n.º 1 cuando un estudiante levanta una base de datos (`PostgreSQL`/`MySQL`) o API backend (`Flask`/`Spring Boot`) y no logra conectar desde otra VM ni desde el navegador de MAX. Comprueba siempre `ss -tulnp` antes de culpar al cable o a VirtualBox.
- **`TcpTestSucceeded : False` incluso escuchando en `0.0.0.0`:** Si el proceso escucha en `0.0.0.0:8080` pero `Test-NetConnection` falla tras agotar tiempo (*timeout*), revisa que el cortafuegos (`ufw` o Firewall de Windows) no esté descartando paquetes en silencio.

## Recursos para Profundizar

- Concepto asociado: [Gestión de Puertos y Diagnóstico Sistemático de Red](../conceptos/ra5-gestion-puertos-herramientas-diagnostico-red.md).
- Vídeo recomendado sobre TCP/IP y puertos: [Fundamentos TCP/IP y puertos de comunicaciones (YouTube)](https://www.youtube.com/watch?v=-c_o8nOavo4).
