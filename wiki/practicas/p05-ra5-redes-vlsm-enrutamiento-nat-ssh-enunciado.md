---
ra: RA5
ce:
  - RA5.a
  - RA5.b
  - RA5.c
  - RA5.d
  - RA5.e
  - RA5.f
  - RA5.g
  - RA5.h
tipo: practica
publicar: true
fuentes:
  - raw/procesados/ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md
  - raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md
  - raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md
ultima_revision: "2026-11-15"
---

# p05 · Diseño de Subredes VLSM, Router NAT, Diagnóstico de Puertos y Comunicaciones Seguras (`RA5.a`–`RA5.h`)

<!-- fuente: raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md -->

## Situación Profesional de Partida

La empresa **NovaCode DAM** estrena una pequeña sede técnica aislada de Internet y necesita que implementes su infraestructura de red completa sobre **VirtualBox** en un PC del aula (**MAX 16 GB RAM**): un **Router Linux de borde** hará de pasarela NAT hacia la WAN para dos estaciones internas (una Ubuntu de servidores/backend y otra Windows 10 cliente de desarrollo), asegurando acceso administrativo cifrado y diagnóstico completo de red.

## Topología VirtualBox y Presupuesto de RAM

| Máquina Virtual | Sistema Operativo | RAM asignada | Interfaces VirtualBox | Dirección / Función |
| :--- | :--- | :---: | :--- | :--- |
| **`DAM-Router-Gate`** | Ubuntu Server 24.04 | **1 GB** | `enp0s3` (NAT WAN) · `enp0s8` (`intnet_nova`) | Router IP + `ip_forward` + NAT `MASQUERADE` (`192.168.80.1/26`) |
| **`DAM-Net-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | `enp0s3` (`intnet_nova`) | Servidor aplicaciones + SSH (`192.168.80.10/26`) |
| **`DAM-Net-Win10`** | Windows 10 Education / Pro | **4 GB** | `Ethernet` (`intnet_nova`) | Estación cliente PowerShell/OpenSSH (`192.168.80.20/26`) |
| **Consumo total activo** | **3 VMs simultáneas sobre MAX (16 GB)** | **7 GB** | Margen libre **9 GB** | Dentro del tope estricto de aula ($\le 10\text{–}12\text{ GB}$) |

---

## Tareas Evaluables (`RA5.a` – `RA5.h`)

### Tarea 1 · Planificación VLSM y Compresión IPv6 (`RA5.a`)

Antes de tocar las VMs, documenta en tu memoria técnica:

1. Reparte mediante **VLSM** el bloque **`192.168.80.0/24`** sin solapamientos de mayor a menor demanda:
   - **Subred 1 — Red Cableada DAM:** **50 hosts** útiles (esta será tu red de laboratorio `intnet_nova`).
   - **Subred 2 — Red Wi-Fi Corporativa:** **25 hosts** útiles.
   - **Subred 3 — Red Servidores DMZ:** **12 hosts** útiles.
   - **Subred 4 — Enlace Router Troncal:** **2 hosts** útiles.
   Indica para cada subred: Dirección de Red, prefijo CIDR, máscara decimal, rango de hosts útiles y dirección de Broadcast.
2. Comprime al máximo siguiendo RFC 5952 la dirección IPv6 `2001:0db8:0040:0000:0000:0000:000a:001f`.

### Tarea 2 · Configuración Estática de la Red Interna (`RA5.a`, `RA5.b`)

1. Conecta las tres VMs a la **Red Interna `intnet_nova`** (únicamente `DAM-Router-Gate` mantendrá una segunda interfaz en modo **NAT** para salida WAN).
2. Configura mediante **Netplan** (`0600`) en **`DAM-Router-Gate`** (`192.168.80.1/26`) y en **`DAM-Net-Ubuntu`** (`192.168.80.10/26`, gateway `.1`, DNS `1.1.1.1`). Validando con `netplan try` / `netplan apply`.
3. Configura por PowerShell en **`DAM-Net-Win10`** (`192.168.80.20/26`, gateway `.1`, DNS `1.1.1.1`).

### Tarea 3 · Planificación de Red Cableada, Wi-Fi Segura y Conmutación (`RA5.b`, `RA5.c`, `RA5.d`)

Redacta una breve ficha técnica de implantación física para la sede real de **NovaCode DAM** respondiendo con precisión:
- Categoría mínima de cableado UTP/STP recomendada para enlaces Gigabit / 10 Gbps y distancia máxima.
- Justificación de qué dispositivos separan dominios de colisión (Switch L2) frente a dominios de broadcast (VLANs `802.1Q` + Router L3).
- Qué canales no solapados elegirías en 2,4 GHz frente a 5 GHz y qué protocolo de cifrado inalámbrico (WPA3-SAE / 802.1X frente a WEP/TKIP obsoletos) aplicarías.

### Tarea 4 · Router Linux, `ip_forward` y Salida WAN por NAT (`RA5.d`, `RA5.e`)

En **`DAM-Router-Gate`** (1 GB RAM):
1. Habilita el reenvío de paquetes (`net.ipv4.ip_forward=1`) de forma persistente.
2. Configura `iptables` (NAT `MASQUERADE` saliendo por `enp0s3` y reglas `FORWARD` entre `enp0s8` y `enp0s3`).
3. Demuestra desde **`DAM-Net-Ubuntu`** y **`DAM-Net-Win10`** que ambos clientes salen a Internet pasando obligatoriamente por **`192.168.80.1`** (muestra la salida de `tracepath -n 1.1.1.1` y `tracert -d 1.1.1.1`).

### Tarea 5 · Gestión de Puertos y Diagnóstico *Bottom-Up* (`RA5.f`, `RA5.g`)

1. En **`DAM-Net-Ubuntu`**, instala y arranca `nginx` o `python3 -m http.server 8080 --bind 0.0.0.0`, y verifica con `sudo ss -tulnp` todos los puertos en escucha junto al PID propietario.
2. Ejecuta desde **`DAM-Net-Win10`** la comprobación completa hasta el puerto abierto (`Test-NetConnection -ComputerName 192.168.80.10 -Port ...`) y resuelve un dominio externo mediante `Resolve-DnsName`.
3. Realiza una captura de 5 paquetes con `sudo tcpdump -i enp0s3 port 8080 -n -c 5` mientras generas tráfico desde Windows.

### Tarea 6 · Administración y Transferencia con Protocolos Seguros (`RA5.h`)

1. Instala `openssh-server` en **`DAM-Net-Ubuntu`**, deshabilita el login directo de `root` (`PermitRootLogin no`) y verifica el servicio con `sshd -t`.
2. Desde **`DAM-Net-Win10`** (o desde Ubuntu cliente), genera un par de claves **Ed25519** (`ssh-keygen -t ed25519`), autoriza la clave pública en `~/.ssh/authorized_keys` (`0600`) en **`DAM-Net-Ubuntu`**, conecta por SSH usando autenticación por clave y transfiere un archivo de prueba mediante **`scp` o `sftp`**.
3. Inspecciona con `openssl s_client -connect github.com:443` el protocolo TLS negociado y explica por qué reemplaza a HTTP/Telnet/FTP.

---

## Entregables y Criterios de Evaluación

Entrega un único informe técnico (`Apellido_Nombre_p05_RA5.pdf` o `.md`) con:
- Tabla VLSM completa de la Tarea 1 + respuesta física/Wi-Fi de la Tarea 3.
- Salidas de terminal y capturas verificadas de Netplan, PowerShell, `ip route`, `iptables -t nat -L -n`, `tracepath`/`tracert`, `ss -tulnp`, `tcpdump`, acceso SSH por clave Ed25519 y transferencia `sftp`/`scp`.

| Bloque evaluado | Criterios cubiertos | Peso |
| :--- | :---: | :---: |
| Diseño VLSM/IPv6 y configuración Netplan / PowerShell | `RA5.a`, `RA5.b` | **25 %** |
| Planificación física cableada/Wi-Fi y dispositivos L2/L3 | `RA5.b`, `RA5.c`, `RA5.d` | **20 %** |
| Router NAT Linux (`ip_forward` + `MASQUERADE`) y salida WAN | `RA5.d`, `RA5.e` | **20 %** |
| Gestión de puertos y diagnóstico *bottom-up* | `RA5.f`, `RA5.g` | **20 %** |
| Protocolos seguros (SSH Ed25519, SFTP, TLS) | `RA5.h` | **15 %** |

## Recursos de Apoyo

- [Conceptos del bloque RA5](../ra/RA5.md#conceptos-teoricos)
- [Ejercicios resueltos e21–e25](../ra/RA5.md#ejercicios-practicos-resueltos)
- Vídeos recomendados: [TCP/IP y puertos](https://www.youtube.com/watch?v=-c_o8nOavo4) · [Subnetting y VLSM](https://www.youtube.com/watch?v=BvyLZX9tSvA) · [DHCP/NAT/Netplan](https://www.youtube.com/watch?v=xSf9CenBR4U) · [SSH/SFTP y seguridad](https://www.youtube.com/watch?v=S-2TIRnsioM)
