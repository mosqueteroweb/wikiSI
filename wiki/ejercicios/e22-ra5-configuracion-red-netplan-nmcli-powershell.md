---
ra: RA5
ce:
  - RA5.a
  - RA5.b
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md
ultima_revision: "2026-11-15"
---

# e22 · Configuración de Red en Clientes: Netplan (`YAML`), `nmcli` y PowerShell sobre Red Interna VirtualBox

<!-- fuente: raw/procesados/ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md -->

## Escenario y Topología VirtualBox

En el laboratorio **MAX (16 GB RAM)** aislamos dos máquinas virtuales dentro de la **Red Interna VirtualBox `aula_dam`** (sin salida externa ni DHCP externo) para practicar configuración IP estática cableada multiplataforma y verificación de enlace Capa 2/3.

| Máquina Virtual | Sistema Operativo | RAM asignada | Adaptador VirtualBox | IP asignada (`192.168.50.0/24`) |
| :--- | :--- | :---: | :--- | :--- |
| **`e22-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | NIC 1: NAT · NIC 2: Red Interna `aula_dam` | **`192.168.50.10/24`** |
| **`e22-Win10`** | Windows 10 Education / Pro | **4 GB** | NIC 1: Red Interna `aula_dam` | **`192.168.50.20/24`** |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Comunicación directa entre VMs | Gateway común `.1` · DNS `1.1.1.1` |

## Objetivos

1. Configurar una interfaz Ethernet secundaria con IP estática mediante **Netplan YAML** (`sudo netplan try`) en Ubuntu y comprender su correspondencia con **`nmcli`**.
2. Configurar la interfaz homóloga en Windows 10 mediante **PowerShell (`New-NetIPAddress`)** y consultar la tabla ARP generada tras intercambiar tráfico ICMP.

---

## Enunciado Detallado

1. En VirtualBox (con ambas VMs apagadas), configura la segunda tarjeta de **`e22-Ubuntu`** y la tarjeta principal de **`e22-Win10`** en modo **Red Interna**, nombre exacto **`aula_dam`**.
2. Arranca **`e22-Ubuntu`**, localiza el nombre real de la nueva interfaz cableada con `ip -br link` (normalmente `enp0s8`) y crea un fichero `/etc/netplan/60-aula-dam.yaml` (permisos `0600`) con IP **`192.168.50.10/24`** y DNS `1.1.1.1`. Aplícalo validando previamente con `sudo netplan try`.
3. En **`e22-Win10`**, asigna **`192.168.50.20/24`** mediante PowerShell como Administrador.
4. Verifica conectividad bidireccional (`ping`), observa la ausencia de direcciones `169.254.x.x` (APIPA) y comprueba la entrada MAC correspondiente en la tabla de vecinos ARP (`ip neigh` / `arp -a`).

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Configuración en `e22-Ubuntu` con Netplan (2 GB RAM)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Identificar el nombre de la interfaz conectada a Red Interna (estado DOWN o sin IP)
        ip -br link

        # Crear archivo Netplan específico para la interfaz secundaria (ejemplo: enp0s8)
        sudo tee /etc/netplan/60-aula-dam.yaml > /dev/null <<'EOF'
        network:
          version: 2
          ethernets:
            enp0s8:
              dhcp4: false
              addresses:
                - 192.168.50.10/24
              nameservers:
                addresses:
                  - 1.1.1.1
        EOF

        # Restringir permisos a root (obligatorio para evitar avisos de Netplan)
        sudo chmod 600 /etc/netplan/60-aula-dam.yaml

        # Probar sintaxis con reversión automática de seguridad y luego aplicar
        sudo netplan try
        sudo netplan apply

        # Verificar IP asignada y velocidad física virtualizada
        ip -br addr show dev enp0s8
        ethtool enp0s8 2>/dev/null | grep -E "Speed|Duplex|Link detected"
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador en e22-Win10
        # 1. Ver el nombre exacto del adaptador conectado a 'aula_dam'
        Get-NetAdapter | Select-Object Name, InterfaceIndex, Status, MacAddress

        # 2. Comprobar que antes de configurar solía tener APIPA 169.254.x.x al no haber DHCP
        Get-NetIPAddress -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress

        # 3. Aplicar IP estática 192.168.50.20/24 en la interfaz (ej. "Ethernet")
        Remove-NetIPAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4 -Confirm:$false -ErrorAction SilentlyContinue
        New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.50.20 -PrefixLength 24
        Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("1.1.1.1")
        ```

    ### 2. Verificación cruzada ICMP y tabla ARP

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Hacer ping al compañero Windows (si Windows bloquea ICMP entrante, revisar nota abajo)
        ping -c 4 192.168.50.20

        # Confirmar que se resolvió la dirección MAC en la tabla ARP
        ip neigh show dev enp0s8
        ```

    === "Windows 10 / 11"

        ```powershell
        # Permitir ICMPv4 entrante si Firewall de Windows bloquea pings desde Linux en red Pública
        New-NetFirewallRule -DisplayName "Permitir Ping ICMPv4 Laboratorio" -Protocol ICMPv4 -IcmpType 8 -Enabled True -Action Allow

        # Probar ping hacia e22-Ubuntu y consultar caché ARP
        ping 192.168.50.10
        arp -a
        ```

---

## Puntos de Control y Errores Frecuentes

- **Ping funciona de Windows → Ubuntu, pero falla de Ubuntu → Windows:** Windows clasifica redes internas sin gateway como **Red Pública**, bloqueando por defecto el *Echo Request* ICMPv4 entrante hasta habilitar la regla de cortafuegos o cambiar el perfil a Red Privada (`Set-NetConnectionProfile -NetworkCategory Private`).
- **Errores de indentación en YAML:** Netplan exige espacios reales (nunca tabuladores `\t`). Si aparece `Error in network definition`, revisa la alineación de 2 espacios por nivel.
- **No poner dos puertas de enlace por defecto en Linux:** Como la NIC 1 en modo NAT ya aporta una ruta por defecto (`0.0.0.0/0` vía `10.0.2.2`), en la NIC 2 de laboratorio interno **no** definimos `gateway`/ruta `default` para no romper la salida a Internet para paquetes `apt`.

## Recursos para Profundizar

- Concepto asociado: [Configuración de Red en Clientes: Netplan, NetworkManager y PowerShell](../conceptos/ra5-configuracion-red-clientes-netplan-powershell.md).
- Vídeo recomendado sobre Netplan y DHCP: [Configuración de red con Netplan, DHCP y Gateway (YouTube)](https://www.youtube.com/watch?v=xSf9CenBR4U).
