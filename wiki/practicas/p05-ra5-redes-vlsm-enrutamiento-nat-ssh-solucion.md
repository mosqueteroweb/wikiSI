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
tipo: solucion
publicar: false
fuentes:
  - raw/procesados/ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md
  - raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md
  - raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md
ultima_revision: "2026-11-15"
---

# Solución Docente · p05 · Diseño VLSM, Router NAT, Diagnóstico y Protocolos Seguros

> **Documento interno docente (`publicar: false`).** No publicar ni enlazar desde páginas públicas.

---

## Tarea 1 · Tabla VLSM sobre `192.168.80.0/24` y Compresión IPv6

| Subred | Demanda | Prefijo / Máscara | Dirección de Red | Rango Útil | Broadcast |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Cableada DAM** | 50 | **`/26`** (`255.255.255.192`) | `192.168.80.0/26` | `.1` – `.62` (62) | `192.168.80.63` |
| **Wi-Fi Corp.** | 25 | **`/27`** (`255.255.255.224`) | `192.168.80.64/27` | `.65` – `.94` (30) | `192.168.80.95` |
| **DMZ Servidores** | 12 | **`/28`** (`255.255.255.240`) | `192.168.80.96/28` | `.97` – `.110` (14) | `192.168.80.111` |
| **Enlace Router** | 2 | **`/30`** (`255.255.255.252`) | `192.168.80.112/30` | `.113` – `.114` (2) | `192.168.80.115` |

- **IPv6 comprimida RFC 5952:** `2001:0db8:0040:0000:0000:0000:000a:001f` → **`2001:db8:40::a:1f`**.

---

## Tarea 2 · Netplan y PowerShell (`intnet_nova`)

### `DAM-Router-Gate` (1 GB)

```yaml
# /etc/netplan/01-router-nova.yaml (chmod 600)
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses: [192.168.80.1/26]
```

### `DAM-Net-Ubuntu` (2 GB)

```yaml
# /etc/netplan/01-lan-nova.yaml (chmod 600)
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: false
      addresses: [192.168.80.10/26]
      routes:
        - to: default
          via: 192.168.80.1
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
```

### `DAM-Net-Win10` (4 GB)

```powershell
Remove-NetIPAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4 -Confirm:$false -ErrorAction SilentlyContinue
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.80.20 -PrefixLength 26 -DefaultGateway 192.168.80.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("1.1.1.1","8.8.8.8")
```

---

## Tarea 3 · Pauta Esperada de Infraestructura LAN/Wi-Fi

- **Cableado:** Mínimo **Cat 6** (1 Gbps a 100 m / 10G a 55 m) o **Cat 6A** para enlaces horizontales hacia APs Wi-Fi 6/7 y racks.
- **Dispositivos:** Switch L2 conmuta por tabla MAC reduciendo dominios de colisión a 1 por puerto; VLANs `802.1Q` dividen dominios de broadcast y el Router L3 encamina entre VLANs + realiza PAT/NAT hacia el ISP.
- **Wi-Fi:** En 2,4 GHz solo canales **`1`, `6` y `11`** (sin solapamiento); priorizar **5 GHz / 6 GHz** (`802.11ax`). Seguridad obligatoria **WPA3-SAE** o **WPA3-Enterprise (`802.1X`)**; rechazar WEP/TKIP/WPS.

---

## Tarea 4 · Router NAT en `DAM-Router-Gate`

```bash
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-forward.conf
sudo sysctl -p /etc/sysctl.d/99-forward.conf
sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
sudo iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT
sudo iptables -A FORWARD -i enp0s3 -o enp0s8 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Verificación en clientes: `tracepath -n 1.1.1.1` (Ubuntu) y `tracert -d 1.1.1.1` (Windows) muestran `192.168.80.1` en el salto 1.

---

## Tarea 5 y 6 · Puertos, Captura, SSH Ed25519 y TLS

```bash
# En DAM-Net-Ubuntu: servicio escucha en 0.0.0.0:8080 y OpenSSH endurecido
python3 -m http.server 8080 --bind 0.0.0.0 >/dev/null 2>&1 &
sudo ss -tulnp | grep -E "8080|:22"
sudo tcpdump -i enp0s3 port 8080 -n -c 5

sudo apt-get update && sudo apt-get install -y openssh-server
echo "PermitRootLogin no" | sudo tee /etc/ssh/sshd_config.d/99-nova.conf
sudo sshd -t && sudo systemctl reload ssh

# Inspección TLS desde Ubuntu
openssl s_client -connect github.com:443 -servername github.com </dev/null 2>/dev/null | grep -E "Protocol|Cipher|issuer="
```

Desde `DAM-Net-Win10`:
```powershell
Test-NetConnection -ComputerName 192.168.80.10 -Port 8080
Resolve-DnsName github.com
ssh-keygen -t ed25519 -C "novacode-win10"
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" |
  ssh usuario@192.168.80.10 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
scp C:\Windows\win.ini usuario@192.168.80.10:/tmp/prueba.ini
```
