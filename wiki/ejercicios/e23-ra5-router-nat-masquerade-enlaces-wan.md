---
ra: RA5
ce:
  - RA5.d
  - RA5.e
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md
ultima_revision: "2026-11-15"
---

# e23 · VM Router Linux (`ip_forward`, NAT `MASQUERADE`) y Enrutamiento hacia Redes Externas

<!-- fuente: raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md -->

## Escenario y Topología VirtualBox

En una red interna aislada (`intnet_lab`), los equipos cliente no pueden acceder a Internet salvo que un **router de borde** encamine sus paquetes entre la LAN privada y la red externa aplicando traducción de direcciones (**NAT/PAT**). Para respetar holgadamente el límite del aula (**MAX 16 GB**), montaremos una topología completa de **3 VMs activas** consumiendo únicamente **4 GB totales**:

| Máquina Virtual | Sistema Operativo | RAM asignada | Interfaces VirtualBox | Función |
| :--- | :--- | :---: | :--- | :--- |
| **`e23-Router-Ubuntu`** | Ubuntu Server 24.04 (sin GUI) | **1 GB** | `enp0s3` (NAT) + `enp0s8` (`intnet_lab`) | Router IP + `ip_forward` + `MASQUERADE` |
| **`e23-LAN-Ubuntu`** | Ubuntu Desktop / Server 24.04 | **2 GB** | `enp0s3` (`intnet_lab`) | Cliente LAN principal (`10.10.20.10/24`) |
| **`e23-LAN-Puppy`** | Puppy Linux | **1 GB** | `eth0` (`intnet_lab`) | Segundo cliente LAN ultraligero (`10.10.20.11/24`) |
| **Total activo** | **3 VMs simultáneas** | **4 GB** | Topología multirred completa | Muy por debajo del tope de **10–12 GB** |

## Objetivos

1. Activar el reenvío de paquetes entre tarjetas (**IP Forwarding**) en el kernel Linux de **`e23-Router-Ubuntu`**.
2. Configurar traducción **PAT / Masquerade** saliente por la interfaz WAN simulada (`enp0s3`).
3. Enrutar los clientes de `intnet_lab` a través del gateway **`10.10.20.1`** comprobando navegación WAN real sin conectar los clientes directamente al modo NAT de VirtualBox.

---

## Enunciado Detallado

1. Configura **`e23-Router-Ubuntu`** con dos tarjetas: `enp0s3` en modo **NAT** (recibe IP automática hacia Internet) y `enp0s8` en **Red Interna `intnet_lab`** con IP fija **`10.10.20.1/24`**.
2. Habilita `net.ipv4.ip_forward = 1` de manera persistente en `/etc/sysctl.d/99-router.conf` y aplica la regla de traducción NAT saliente por `enp0s3`.
3. En **`e23-LAN-Ubuntu`** (sin tarjeta NAT directa, solo `intnet_lab`), configura la IP **`10.10.20.10/24`**, puerta de enlace **`10.10.20.1`** y DNS **`1.1.1.1`**.
4. Verifica con `traceroute -n 1.1.1.1` o `tracepath -n 1.1.1.1` desde el cliente que el primer salto es **`10.10.20.1`** y se alcanza salida WAN real, además de hacer ping interno entre **`e23-LAN-Ubuntu`** y **`e23-LAN-Puppy`** (`10.10.20.11/24`).

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Configuración de `e23-Router-Ubuntu` (1 GB RAM)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # 1. Configurar Netplan para enp0s3 (DHCP WAN) y enp0s8 (IP fija LAN como gateway)
        sudo tee /etc/netplan/01-router.yaml > /dev/null <<'EOF'
        network:
          version: 2
          ethernets:
            enp0s3:
              dhcp4: true
            enp0s8:
              dhcp4: false
              addresses:
                - 10.10.20.1/24
        EOF
        sudo chmod 600 /etc/netplan/01-router.yaml
        sudo netplan apply

        # 2. Activar IP Forwarding persistente entre interfaces
        echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-router.conf
        sudo sysctl -p /etc/sysctl.d/99-router.conf

        # 3. Configurar regla NAT (PAT Masquerade) sobre la interfaz WAN enp0s3
        sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
        sudo iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT
        sudo iptables -A FORWARD -i enp0s3 -o enp0s8 -m state --state RELATED,ESTABLISHED -j ACCEPT

        # Comprobar tabla NAT activa
        sudo iptables -t nat -L -n -v
        ```

    === "Windows 10 / 11"

        ```powershell
        # Referencia en Windows si actuase como cliente en la misma Red Interna:
        # New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 10.10.20.20 -PrefixLength 24 -DefaultGateway 10.10.20.1
        # Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("1.1.1.1")
        Write-Host "Este laboratorio utiliza Ubuntu Server 1 GB como router dedicado para minimizar RAM."
        ```

    ### 2. Configuración y trazado desde `e23-LAN-Ubuntu` y `e23-LAN-Puppy`

    === "MAX / Ubuntu (Linux)"

        ```bash
        # En e23-LAN-Ubuntu (NIC única conectada a intnet_lab)
        sudo tee /etc/netplan/01-cliente-lan.yaml > /dev/null <<'EOF'
        network:
          version: 2
          ethernets:
            enp0s3:
              dhcp4: false
              addresses:
                - 10.10.20.10/24
              routes:
                - to: default
                  via: 10.10.20.1
              nameservers:
                addresses: [1.1.1.1, 8.8.8.8]
        EOF
        sudo chmod 600 /etc/netplan/01-cliente-lan.yaml
        sudo netplan apply

        # Verificar puerta de enlace y salto real hacia WAN
        ip route
        ping -c 3 10.10.20.1
        ping -c 3 1.1.1.1
        tracepath -n 1.1.1.1
        # El primer salto mostrado debe ser obligatoriamente 10.10.20.1

        # En e23-LAN-Puppy (terminal rápida):
        # ifconfig eth0 10.10.20.11 netmask 255.255.255.0 up
        # route add default gw 10.10.20.1
        # ping -c 2 10.10.20.10
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comandos equivalentes de validación si el cliente fuese Windows:
        route print -4
        tracert -d 1.1.1.1
        ```

---

## Puntos de Control y Errores Frecuentes

- **Reglas `iptables` no persistentes tras reinicio:** Por defecto, los cambios en `iptables` desaparecen al reiniciar la VM salvo instalar `iptables-persistent` (`sudo apt install -y iptables-persistent && sudo netfilter-persistent save`) o declarar `nftables` en `/etc/nftables.conf`.
- **Olvidar `ip_forward=1`:** Aunque la regla NAT esté bien escrita, sin `net.ipv4.ip_forward=1` el kernel Linux descarta silenciosamente cualquier paquete destinado a una IP que no sea local.

### Parte 2 (Ampliación): Emulador TP-Link Archer C20 y Publicación de Servidor en Casa

1. Accede al [**Emulador Online TP-Link (Archer C20)**](https://www.tp-link.com/es/support/emulator/) y localiza las pantallas de **DHCP Address Reservation**, **Forwarding $\rightarrow$ Virtual Servers**, **DMZ**, **UPnP** y **Dynamic DNS**.
2. Configura hipotéticamente la publicación de un servidor web interno (`192.168.0.50:8080`) en el puerto externo `80` con reserva DHCP por dirección MAC.
3. Describe los pasos adicionales necesarios en un entorno real para publicar ese servidor desde casa: comprobación de ausencia de **CG-NAT** (comparar la IP WAN del router con la IP pública mostrada externamente), alta de un dominio **DDNS** (*DuckDNS* / *No-IP*) y uso de un proxy inverso si conviven varias aplicaciones web.

## Recursos para Profundizar

- Concepto asociado: [Dispositivos de Interconexión, VLANs, Enrutamiento y Acceso WAN](../conceptos/ra5-interconexion-enrutamiento-nat-acceso-wan.md).
- Vídeo recomendado sobre NAT, Gateway y enrutamiento: [DHCP, NAT, Gateway y Enrutamiento (YouTube)](https://www.youtube.com/watch?v=xSf9CenBR4U).
