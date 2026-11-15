---
tema: "Administración y Conexión Remota Segura, Restricciones de Seguridad, Cortafuegos y Utilidades de Endurecimiento"
ra: RA6
ce:
  - RA6.d
  - RA6.e
  - RA6.f
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA6 (2/3) · Acceso Remoto, Cortafuegos y Utilidades de Seguridad

## 1. Conexión y Administración Remota (`RA6.d`)

- **SSH (`22/TCP`):** administración de consola en Linux y Windows Server/10/11 OpenSSH. Soporta además **túneles seguros (*Port Forwarding*)**:
  - Local forwarding (`ssh -L 5901:127.0.0.1:5901 user@srv`) para encapsular protocolos poco seguros (ej. VNC, bases de datos internas o paneles admin) dentro de un canal SSH cifrado sin exponer su puerto a la LAN.
- **RDP (*Remote Desktop Protocol*, `3389/TCP`):** estándar gráfico en Windows (Escritorio Remoto, NLA — *Network Level Authentication* obligatoria); en Linux se usa como cliente **Remmina** / `xfreerdp` y como servidor **`xrdp`** (usando usuario sin sesión X11 local abierta simultáneamente).
- **VNC (*RFB*, `5900+N/TCP`) vs SPICE / Guacamole:** útil para asistencia gráfica ligera multiplataforma, pero su tráfico nativo **no está cifrado por completo**, por lo que **siempre debe tunelizarse vía SSH o VPN** en redes no confiables.

## 2. Protección de Recursos y Políticas de Cortafuegos (`RA6.e`, `RA6.f`)

- **Principio de mínimo privilegio y superficie mínima de exposición:** cerrar todo puerto entrante innecesario (*Default Deny Incoming*), permitir salida controlada y aislar perfiles de red.
- **Linux — `ufw` (*Uncomplicated Firewall*, sobre `nftables`/`iptables`) y `nftables`:**
  - `sudo ufw default deny incoming` + `sudo ufw default allow outgoing`.
  - Reglas granulares por IP origen/subred: `sudo ufw allow from 192.168.50.0/24 to any port 445 proto tcp` o `sudo ufw limit ssh` (limita intentos repetidos por minuto).
  - Revisar reglas numeradas: `sudo ufw status numbered` / `sudo nft list ruleset`.
- **Windows Defender Firewall (`netsh advfirewall` / PowerShell):**
  - Tres perfiles diferenciados: **Dominio**, **Privado** y **Público** (más estricto).
  - PowerShell `New-NetFirewallRule -DisplayName "..." -Direction Inbound -Protocol TCP -LocalPort 3389 -RemoteAddress 192.168.50.0/24 -Action Allow -Profile Private`.

## 3. Utilidades de Seguridad Básica y Auditoría (`RA6.f`)

- **Protección contra fuerza bruta:** **`fail2ban`** en Linux monitoriza logs (`journald` / `/var/log/auth.log`) y banea temporalmente mediante reglas de cortafuegos las IP atacantes tras $N$ fallos SSH/web.
- **Auditoría de puertos expuestos y vulnerabilidades locales:** `nmap -sT -sV <ip>` (exclusivamente en redes/VMs propias de laboratorio), `ss -tulnp`, **`lynis audit system`** (auditoría de endurecimiento en Linux) y **Windows Defender (`Get-MpComputerStatus`, `Start-MpScan`)** / **AppLocker / BitLocker**.
- **Actualizaciones de seguridad automáticas:** `unattended-upgrades` en Ubuntu/Debian y Windows Update / WSUS en entornos corporativos.
