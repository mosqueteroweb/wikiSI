---
tema: "Puertos de Comunicaciones, Verificación y Diagnóstico de Red y Protocolos Seguros"
ra: RA5
ce:
  - RA5.f
  - RA5.g
  - RA5.h
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA5 (3/3) · Puertos, Diagnóstico y Protocolos Seguros

## 1. Gestión de Puertos de Comunicaciones (TCP y UDP)

- Rango total: `0–65535` (16 bits en cabecera TCP/UDP):
  - **Puertos bien conocidos (`0–1023`):** `20/21` FTP, `22` SSH/SFTP, `23` Telnet (inseguro), `25` SMTP, `53` DNS, `67/68` DHCP, `80` HTTP, `123` NTP, `143` IMAP, `443` HTTPS, `445` SMB.
  - **Puertos registrados (`1024–49151`):** `3306` MySQL/MariaDB, `3389` RDP, `5432` PostgreSQL, `8080` HTTP alternativo/Spring Boot.
  - **Dinámicos o efímeros (`49152–65535`):** asignados temporalmente al lado cliente (en Linux rango configurable `/proc/sys/net/ipv4/ip_local_port_range`, típico `32768–60999`).
- **Inspección de sockets y procesos en escucha:**
  - Linux: `ss -tulnp` (sustituto moderno de `netstat`: `-t` TCP, `-u` UDP, `-l` listening, `-n` numérico sin resolver DNS, `-p` PID/proceso).
  - Windows: `Get-NetTCPConnection -State Listen`, `netstat -ano` (`-o` muestra el PID para correlacionar con `Get-Process`).

## 2. Verificación y Diagnóstico Sistemático de la Red (`RA5.g`)

Metodología ascendente (*bottom-up*) para aislar fallos en el laboratorio VirtualBox y entorno real:
1. **Capa física y enlace:** `ip link` / `ethtool` / `nmcli dev status` · Windows `Get-NetAdapter`. Verificar *UP/LOWER_UP*.
2. **Capa IP local y vecinos ARP:** `ip -br addr`, `ip neigh` · Windows `Get-NetIPAddress`, `arp -a`.
3. **Puerta de enlace y rutas:** `ip route`, `ping -c 4 <gateway>` · Windows `route print` / `Get-NetRoute`, `Test-NetConnection`.
4. **Conectividad IP externa y trazado:** `ping -c 4 1.1.1.1` (descarta fallo DNS), `traceroute` / `mtr` · Windows `tracert`, `pathping`.
5. **Resolución DNS:** `dig`, `nslookup`, `resolvectl query` · Windows `Resolve-DnsName`.
6. **Puertos y capa de aplicación:** `ss -tulnp`, `nc -zv <host> <puerto>`, `curl -I https://...` · Windows `Test-NetConnection -ComputerName <host> -Port <puerto>`.
7. **Captura y análisis de paquetes:** `tcpdump -i eth0 port 80 -n` o **Wireshark** (análisis visual de handshake TCP, peticiones DNS en claro frente a tráfico TLS cifrado).

## 3. Protocolos Seguros de Comunicaciones (`RA5.h`)

- **Principios de seguridad en red:** Confidencialidad (cifrado), Integridad (HMAC/AEAD) y Autenticidad (certificados X.509 o claves públicas).
- **Reemplazos seguros obligatorios frente a protocolos en claro:**
  - `HTTP (80)` → **`HTTPS (443)`** sobre **TLS 1.3 / 1.2** (certificados X.509 firmados por CA, cifrado asimétrico inicial + clave simétrica AES-GCM/ChaCha20).
  - `Telnet (23)` / `rlogin` → **`SSH (22)`** (autenticación por contraseña o preferiblemente **par de claves Ed25519/RSA**, reenvío seguro de puertos *tunneling* y verificación de *fingerprint* en `~/.ssh/known_hosts`).
  - `FTP (21)` → **`SFTP (22 sobre SSH)`** o **`FTPS (990/explicit TLS)`**.
  - **DNS cifrado:** **DoT (DNS over TLS, puerto 853)** y **DoH (DNS over HTTPS, puerto 443)**.
  - **VPNs modernas:** **WireGuard** (UDP 51820, criptografía moderna ligera integrada en el kernel Linux) y **OpenVPN / IPsec** para interconectar sedes o teletrabajar cifrando todo el túnel de capa IP.
