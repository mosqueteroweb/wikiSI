---
ra: RA6
ce:
  - RA6.a
  - RA6.b
  - RA6.c
  - RA6.d
  - RA6.e
  - RA6.f
  - RA6.g
tipo: solucion
publicar: false
fuentes:
  - raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md
  - raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md
  - raw/procesados/ra6-dominios-active-directory-ldap-integracion.md
ultima_revision: "2026-11-15"
---

# Solución Docente · p06 · Servidores Compartidos, Acceso Remoto, Cortafuegos y Dominio Samba AD

> **Documento interno docente (`publicar: false`).** No publicar ni enlazar desde páginas públicas.

---

## Tarea 1 · Samba (`SMB3`) y Permisos Efectivos

```bash
# En DAM-Corp-Srv (192.168.75.10)
sudo apt-get update && sudo apt-get install -y samba acl smbclient
sudo groupadd vega_devs
sudo useradd -m -s /usr/sbin/nologin -G vega_devs mario.dev
sudo useradd -m -s /usr/sbin/nologin sara.ro
sudo smbpasswd -a mario.dev
sudo smbpasswd -a sara.ro

sudo mkdir -p /srv/vega_datos
sudo chown root:vega_devs /srv/vega_datos
sudo chmod 2770 /srv/vega_datos
sudo setfacl -m u:sara.ro:rx /srv/vega_datos
sudo setfacl -d -m u:sara.ro:rx /srv/vega_datos

sudo tee -a /etc/samba/smb.conf > /dev/null <<'EOF'

[VegaRepo]
   path = /srv/vega_datos
   browseable = yes
   read only = yes
   valid users = @vega_devs, sara.ro
   write list = @vega_devs
   create mask = 0660
   directory mask = 0770
   force group = vega_devs
EOF
testparm -s && sudo systemctl restart smbd
```

En `DAM-Corp-Win10`:
```cmd
net use * /delete /y
net use Z: \\192.168.75.10\VegaRepo /user:mario.dev
echo ok > Z:\archivo_mario.txt
net use Z: /delete /y
net use Z: \\192.168.75.10\VegaRepo /user:sara.ro
dir Z:\
echo fail > Z:\intruso.txt   REM Acceso denegado por intersección Share/ACL
```

---

## Tarea 2 · CUPS PDF + Proxy Inverso Nginx (`80 → 8085`)

```bash
sudo apt-get install -y cups printer-driver-cups-pdf nginx
sudo systemctl enable --now cups
lpstat -p -d
echo "Prueba VegaSoft" | lp -d PDF

python3 -m http.server 8085 --bind 127.0.0.1 >/dev/null 2>&1 &
sudo tee /etc/nginx/sites-available/vega_proxy > /dev/null <<'EOF'
server {
    listen 80 default_server;
    location / { proxy_pass http://127.0.0.1:8085; }
}
EOF
sudo ln -sf /etc/nginx/sites-available/vega_proxy /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

---

## Tarea 3 · RDP con NLA y Túnel SSH Local (`9085 → 8085`)

En Windows 10 Admin PowerShell:
```powershell
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1
Enable-NetFirewallRule -DisplayGroup "Escritorio remoto" -ErrorAction SilentlyContinue

# Abrir túnel local cifrado hacia backend 8085 ligado a 127.0.0.1 en Ubuntu:
ssh -N -L 9085:127.0.0.1:8085 usuario@192.168.75.10
```

---

## Tarea 4 y 5 · UFW, Defender Firewall, `fail2ban` y `lynis`

```bash
# DAM-Corp-Srv
sudo apt-get install -y ufw fail2ban lynis
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw limit 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow from 192.168.75.0/24 to any port 445 proto tcp
sudo ufw --force enable
sudo ufw status numbered

sudo tee /etc/fail2ban/jail.local > /dev/null <<'EOF'
[sshd]
enabled = true
port = ssh
backend = systemd
maxretry = 3
bantime = 15m
EOF
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
sudo lynis audit system --quick | tail -n 20
```

En Windows PowerShell:
```powershell
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private
New-NetFirewallRule -DisplayName "RDP Solo LAN Corp" -Direction Inbound -Protocol TCP -LocalPort 3389 -RemoteAddress 192.168.75.0/24 -Profile Private -Action Allow
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled
```

---

## Tarea 6 · Dominio Samba AD DC `vega.local`

*(Tras snapshot VirtualBox si se reutilizó la misma VM, y con `ufw` permitiendo DNS 53, Kerberos 88, LDAP 389, SMB 445, RPC 135 desde `192.168.75.0/24`):*

```bash
sudo hostnamectl set-hostname dc1.vega.local
echo "192.168.75.10 dc1.vega.local dc1" | sudo tee -a /etc/hosts
sudo systemctl disable --now smbd nmbd winbind systemd-resolved
sudo rm -f /etc/resolv.conf /etc/samba/smb.conf
printf "nameserver 127.0.0.1\nsearch vega.local\n" | sudo tee /etc/resolv.conf

sudo apt-get install -y samba krb5-user winbind
sudo samba-tool domain provision --use-rfc2307 --realm=VEGA.LOCAL --domain=VEGA --server-role=dc --dns-backend=SAMBA_INTERNAL --adminpass='VegaAdmin#2026!'
sudo cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
sudo systemctl unmask samba-ad-dc
sudo systemctl enable --now samba-ad-dc

sudo samba-tool ou create "OU=Ingenieria"
sudo samba-tool group add g_ingenieros
sudo samba-tool user create elena.corp 'ElenaDam#2026!' --userou="OU=Ingenieria"
sudo samba-tool group addmembers g_ingenieros elena.corp
```

En `DAM-Corp-Win10`:
```powershell
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("192.168.75.10")
Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.vega.local
Add-Computer -DomainName "vega.local" -Restart
```
