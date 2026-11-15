---
ra: RA6
ce:
  - RA6.b
  - RA6.e
  - RA6.f
tipo: concepto
publicar: true
fuentes:
  - raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md
ultima_revision: "2026-11-15"
---

# Utilidades de Seguridad Básica, Defensa Activa (`fail2ban`) y Auditoría de Endurecimiento

<!-- fuente: raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md -->

## 1. Utilidades Esenciales para Defensa y Auditoría (`RA6.f`)

Un cortafuegos estático filtra puertos, pero necesita complementarse con utilidades específicas para prevenir intrusiones repetitivas, detectar software malicioso, auditar vulnerabilidades de configuración y parchar el sistema automáticamente:

| Área de Seguridad | Herramienta en MAX / Ubuntu | Herramienta en Windows 10/11 | Objetivo |
| :--- | :--- | :--- | :--- |
| **Defensa contra fuerza bruta** | **`fail2ban`** | Directiva de bloqueo (`net accounts`) | Bloquear IPs o cuentas tras fallos reiterados de acceso |
| **Antimalware / Protección** | `ClamAV` (análisis de archivos/servidores) | **Microsoft Defender Antivirus** | Detección en tiempo real y análisis bajo demanda |
| **Auditoría del sistema** | **`lynis`**, `sudo ss -tulnp` | `Microsoft Security Compliance Toolkit` / `Get-NetTCPConnection` | Detectar permisos laxos, servicios inseguros o contraseñas débiles |
| **Actualizaciones automáticas** | **`unattended-upgrades`** | **Windows Update / WSUS** | Aplicar parches críticos de seguridad sin demora |
| **Escaneo de puertos propios** | `nmap` / `nc` (solo red autorizada) | `Test-NetConnection` | Comprobar desde otro host qué puertos están expuestos realmente |

---

## 2. Prevención Activa de Fuerza Bruta con `fail2ban`

Cuando un servidor tiene el puerto SSH (`22`) accesible, bots automatizados prueban miles de contraseñas cada hora. **`fail2ban`** lee continuamente los registros del servicio (`systemd-journald` o `/var/log/auth.log`) y crea una regla dinámica en el cortafuegos bloqueando durante un tiempo configurable (`bantime`) cualquier IP que supere `maxretry` fallos.

> [!CAUTION]
> **Uso ético de herramientas de escaneo (`nmap`):** Escanea **únicamente** las direcciones IP de tus propias máquinas virtuales en Red Interna VirtualBox o sistemas donde cuentes con autorización escrita explícita. Escanear equipos ajenos o redes de terceros viola la normativa del centro y la legislación vigente.

---

## 3. Despliegue de Utilidades de Seguridad

=== "MAX / Ubuntu (Linux)"

    ```bash
    # 1. Instalar fail2ban, auditoría lynis y parches automáticos
    sudo apt-get update && sudo apt-get install -y fail2ban unattended-upgrades lynis nmap

    # 2. Configurar copia local /etc/fail2ban/jail.local (nunca modificar jail.conf directamente)
    sudo tee /etc/fail2ban/jail.local > /dev/null <<'EOF'
    [sshd]
    enabled = true
    port = ssh
    backend = systemd
    maxretry = 4
    findtime = 10m
    bantime = 1h
    EOF

    sudo systemctl enable --now fail2ban
    sudo fail2ban-client status sshd

    # 3. Ejecutar auditoría de endurecimiento del servidor (genera índice y sugerencias)
    sudo lynis audit system --quick
    ```

=== "Windows 10 / 11"

    ```powershell
    # 1. Verificar estado de protección en tiempo real de Microsoft Defender
    Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated

    # 2. Lanzar análisis rápido bajo demanda y comprobar amenazas detectadas
    Start-MpScan -ScanType QuickScan
    Get-MpThreatDetection

    # 3. Revisar estado de BitLocker y últimos parches instalados
    Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 HotFixID, Description, InstalledOn
    ```

---

## Recursos para profundizar

- Concepto anterior: [Seguridad de Recursos y Cortafuegos](ra6-seguridad-recursos-cortafuegos-ufw-defender.md).
- Concepto siguiente: [Implantación y Explotación de Dominios (Active Directory / Samba AD DC)](ra6-implantacion-explotacion-dominios-ad-samba-dc.md).
- Documentación oficial `fail2ban`: [Fail2ban Documentation](https://fail2ban.readthedocs.io/).
- Vídeo recomendado sobre endurecimiento y servicios seguros: [Seguridad en SSH, cortafuegos y servidores Linux (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
