---
tema: "Redes Cableadas Ethernet, Wi-Fi, Dispositivos de Interconexión, VLANs, NAT y Acceso WAN"
ra: RA5
ce:
  - RA5.b
  - RA5.c
  - RA5.d
  - RA5.e
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA5 (2/3) · LAN Cableada/Inalámbrica, Dispositivos y Acceso WAN

## 1. Redes Cableadas (`IEEE 802.3`), Cableado Estructurado y Switches

- **Medios físicos Ethernet:** par trenzado UTP/STP Cat 5e (1 Gbps), Cat 6 (1 Gbps a 100 m / 10 Gbps hasta 55 m), Cat 6A (10 Gbps a 100 m) y fibra óptica monomodo (SMF, largas distancias) / multimodo (MMF, edificios/CPD).
- **Conmutación (Switch Capa 2):** tabla CAM/MAC (aprende direcciones MAC origen por puerto y reenvía tramas *unicast* solo al puerto destino). Reduce dominios de colisión a **uno por puerto** (Full-Duplex sin CSMA/CD).
- **VLANs (`IEEE 802.1Q`):** segmentación lógica de dominios de broadcast en un mismo switch físico mediante etiqueta de **4 bytes (VID 1–4094)** en puertos *trunk* y sin etiqueta en puertos *access*. En Linux los interfaces VLAN se crean como `enp0s3.10`.

## 2. Redes Inalámbricas (`IEEE 802.11` / Wi-Fi)

- **Estándares:** `802.11ac` (Wi-Fi 5, 5 GHz), `802.11ax` (Wi-Fi 6/6E, 2.4/5/6 GHz, OFDMA y MU-MIMO), `802.11be` (Wi-Fi 7).
- **Bandas y canales:**
  - **2,4 GHz:** mayor alcance y penetración en muros, menor velocidad; solo **3 canales no solapados** en ancho de 20 MHz (**1, 6 y 11**).
  - **5 GHz y 6 GHz:** mucho menos congestionadas, canales anchos (40/80/160 MHz), menor penetración física.
- **Seguridad Wi-Fi:** **WPA3-Personal (SAE)** o **WPA3-Enterprise (802.1X / RADIUS)** como estándar recomendado; **WPA2-AES (CCMP)** aún aceptable con frase robusta; obsoletos e inseguros **WEP**, **TKIP** y **WPS PIN** vulnerable.
- **Gestión en Linux/Windows:** `nmcli dev wifi list`, `nmcli dev wifi connect "<SSID>" password "<clave>"`, `iw dev`; en Windows `netsh wlan show profiles` y `netsh wlan show interfaces`.

## 3. Dispositivos de Interconexión y Acceso a Redes WAN

- **Hub (obsoleto, Capa 1)** vs **Switch L2 (Capa 2, tabla MAC, dominios colisión separados)** vs **Switch L3 / Router (Capa 3, tabla de rutas IP, separa dominios de broadcast)**.
- **Punto de Acceso (AP)** frente a **Router doméstico integrado** (que aglutina módem/ONT bridge, router IP, NAT, servidor DHCP y switch/AP).
- **Acceso a redes externas (WAN) y traducción de direcciones (NAT/PAT):**
  - **NAT estático** (1:1 IP privada ↔ IP pública), **NAT dinámico** y **PAT / Masquerade** (*Port Address Translation*: múltiples hosts privados comparten 1 IP pública distinguiéndose por puerto origen).
  - **Enrutamiento estático vs dinámico:** puerta de enlace por defecto (`0.0.0.0/0`) y rutas específicas (`ip route add <red/cidr> via <nexthop>`). En Linux convertido a router temporal o permanente: activar `net.ipv4.ip_forward=1` en `/etc/sysctl.d/` + regla `iptables -t nat -A POSTROUTING -o <wan_if> -j MASQUERADE` o `nftables`.
  - **Servicios de infraestructura en la salida:** **DHCP** (DORA: *Discover, Offer, Request, Acknowledge*; puertos UDP `67/68`) y **DNS** (resolución recursiva/autoritativa de nombres, registros `A`, `AAAA`, `CNAME`, `MX`, `PTR`, puerto `53` TCP/UDP y DoT/DoH).
