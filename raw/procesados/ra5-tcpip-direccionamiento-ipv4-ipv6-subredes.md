---
tema: "Arquitectura TCP/IP, Direccionamiento IPv4/IPv6, CIDR, VLSM y Configuración en Clientes"
ra: RA5
ce:
  - RA5.a
  - RA5.b
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA5 (1/3) · TCP/IP, Direccionamiento IPv4/IPv6 y Subredes

## 1. Arquitectura de Capas TCP/IP frente al Modelo OSI

- **Capas del modelo TCP/IP (4/5 capas):**
  1. **Acceso a Red (Física + Enlace OSI):** Ethernet (`802.3`), Wi-Fi (`802.11`), tramas MAC de 48 bits, protocolo ARP (resolución IP → MAC) e ICMPv6 NDP en IPv6.
  2. **Internet (Red OSI):** IPv4 (`32 bits`), IPv6 (`128 bits`), ICMP/ICMPv6 (diagnóstico `ping`/`traceroute`), encaminamiento entre subredes mediante *gateway* (puerta de enlace).
  3. **Transporte:** TCP (orientado a conexión, *three-way handshake* `SYN` → `SYN-ACK` → `ACK`, control de flujo, retransmisión y puertos) y UDP (no orientado a conexión, baja latencia: DNS, DHCP, streaming, QUIC/HTTP3).
  4. **Aplicación:** HTTP/HTTPS, SSH, DNS, DHCP, SMB, SMTP/IMAP.

## 2. Direccionamiento IPv4, Máscaras CIDR y Subnetting / VLSM

- **Estructura IPv4:** 32 bits divididos en 4 octetos (`0–255`), compuestos por **Porción de Red + Porción de Host** delimitada por la máscara (`/prefijo` CIDR).
- **Cálculo rápido en subnetting:**
  - Direcciones útiles por subred = 2ʰ − 2 (donde h = 32 − prefijo; se restan dirección de **red** con bits de host a 0 y **broadcast** con bits de host a 1). En enlaces punto a punto (`/31`, RFC 3021) se aprovechan ambas direcciones.
  - Salto de bloque (*block size*): 256 − octeto crítico de la máscara.
- **Rangos privados RFC 1918 (no enrutables en Internet público):**
  - `10.0.0.0/8` (`10.0.0.0` – `10.255.255.255`)
  - `172.16.0.0/12` (`172.16.0.0` – `172.31.255.255`)
  - `192.168.0.0/16` (`192.168.0.0` – `192.168.255.255`)
  - Especiales: `127.0.0.0/8` (loopback), `169.254.0.0/16` (APIPA/link-local cuando falla DHCP).
- **VLSM (*Variable Length Subnet Mask*):** siempre ordenar los departamentos de **mayor a menor demanda de hosts** para asignar máscaras ajustadas sin solapamiento (ej. 60 hosts → `/26` [62 útiles], 25 hosts → `/27` [30 útiles], 10 hosts → `/28` [14 útiles], enlace WAN → `/30` [2 útiles]).

## 3. Introducción Operativa a IPv6

- 128 bits en 8 hextetos hexadecimales (`2001:0db8:85a3::8a2e:0370:7334`). Reglas de compresión: omitir ceros a la izquierda por hexteto y colapsar **una sola vez** bloques consecutivos de `0000` con `::`.
- Tipos clave:
  - **Global Unicast (`2000::/3`):** direcciones públicas enrutables.
  - **Unique Local (`fc00::/7`, habitualmente `fd00::/8`):** equivalente a RFC 1918 privado.
  - **Link-Local (`fe80::/10`):** obligatoria en cada interfaz para NDP, SLAAC y gateway por defecto.
  - **Loopback (`::1/128`)** y sin broadcast (sustituido por multicast `ff02::1`, etc.).

## 4. Configuración en Clientes Linux (Netplan / `nmcli`) y Windows (`netsh` / PowerShell)

- **Ubuntu Desktop / Server (`Netplan`):** YAML en `/etc/netplan/*.yaml` (permisos `0600`), aplicando con `sudo netplan try` y `sudo netplan apply`. En Desktop suele usar `renderer: NetworkManager` y en Server `renderer: networkd`.
- **`nmcli` / `iproute2`:** consulta rápida `ip -br a`, `ip route`, `resolvectl status`. En MAX/Desktop `nmcli con mod ...` y `nmcli con up ...`.
- **Windows 10/11 PowerShell:** `Get-NetIPConfiguration`, `New-NetIPAddress`, `Set-DnsClientServerAddress`, o tradicional `netsh interface ipv4 set address ...`.
- **VirtualBox adaptadores en aula DAM:** *NAT* (salida a Internet aislada en `10.0.2.0/24`), *Red NAT* (red compartida con DHCP y salida), *Red Interna* (aislada entre VMs sin salida directa), *Solo-anfitrión* (comunicación MAX ↔ VMs) y *Adaptador Puente* (*Bridged*, cuidado en redes escolares restringidas con port-security o DHCP corporativo).
