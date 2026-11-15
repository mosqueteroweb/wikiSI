---
ra: RA6
ce:
  - RA6.e
  - RA6.f
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md
ultima_revision: "2026-11-15"
---

# e29 · Cortafuegos (`ufw` / Windows Defender Firewall), `fail2ban` y Auditoría de Puertos

<!-- fuente: raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md -->

## Escenario y Topología VirtualBox

Un servidor de producción recién instalado expone varios servicios sin restricciones de origen. Aplicaremos política predeterminada de cierre total entrante (**Default Deny**), abriremos únicamente los servicios necesarios por subred de confianza, activaremos **`fail2ban`** contra ataques SSH y auditaremos el resultado desde otra máquina.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e29-Ubuntu-FW`** | Ubuntu Server 24.04 | **2 GB** | Servidor endurecido con `ufw`, `fail2ban` y `lynis` |
| **`e29-Win10-FW`** | Windows 10 Education / Pro | **4 GB** | Reglas Defender Firewall, verificación `nmap`/`Test-NetConnection` y Defender |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Respetando ampliamente los **16 GB** del PC **MAX** |

## Objetivos

1. Configurar **`ufw`** con política `default deny incoming`, límite de tasa (`limit ssh`) y apertura restringida por subred para puertos específicos.
2. Desplegar **`fail2ban`** y ejecutar una auditoría rápida del sistema con **`lynis`**.
3. Configurar perfiles y reglas entrantes acotadas por IP origen en **Windows Defender Firewall** y verificar protección de **Microsoft Defender**.

---

## Enunciado Detallado

1. **Cortafuegos `ufw` en Ubuntu (`RA6.e`, `RA6.f`):**
   - Instala `openssh-server`, `nginx` y `ufw`.
   - Establece política predeterminada `deny incoming` y `allow outgoing`.
   - Antes de activar el cortafuegos, añade `ufw limit 22/tcp`, `ufw allow 'Nginx HTTP'` (`80/TCP`) y abre un puerto interno `5432/TCP` **exclusivamente** desde la subred `192.168.50.0/24`.
   - Habilita `ufw`, consulta `sudo ufw status numbered` y comprueba desde Windows con `Test-NetConnection` qué puertos responden y cuáles bloquea el muro.

2. **`fail2ban` y auditoría de endurecimiento (`RA6.f`):**
   - Instala `fail2ban` y `lynis`, crea `/etc/fail2ban/jail.local` protegiendo `sshd` (`maxretry = 3`, `bantime = 15m`), arranca el servicio y revisa el estado de la cárcel con `fail2ban-client status sshd`.
   - Lanza `sudo lynis audit system --quick` y anota dos recomendaciones de mejora propuestas para el servidor.

3. **Defender Firewall y antimalware en Windows (`RA6.e`, `RA6.f`):**
   - Activa el perfil **Privado**, crea una regla entrante permitiendo TCP `8080` únicamente desde `192.168.50.10`, y comprueba el estado del antivirus Microsoft Defender (`Get-MpComputerStatus`).

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Configuración `ufw`, `fail2ban` y `lynis` en `e29-Ubuntu-FW`

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar servicios de demostración y utilidades de seguridad
        sudo apt-get update && sudo apt-get install -y openssh-server nginx ufw fail2ban lynis

        # 1. Políticas predeterminadas del cortafuegos
        sudo ufw default deny incoming
        sudo ufw default allow outgoing

        # 2. Permitir SSH (con limitación anti fuerza bruta) ANTES de activar UFW
        sudo ufw limit 22/tcp comment 'SSH limitado'
        sudo ufw allow 80/tcp comment 'Web Nginx publica LAN'
        sudo ufw allow from 192.168.50.0/24 to any port 5432 proto tcp comment 'PostgreSQL solo subred aula'

        # 3. Activar y consultar estado numerado
        sudo ufw --force enable
        sudo ufw status numbered

        # 4. Configurar jail.local de fail2ban con backend systemd (Ubuntu 24.04)
        sudo tee /etc/fail2ban/jail.local > /dev/null <<'EOF'
        [sshd]
        enabled = true
        port = ssh
        backend = systemd
        maxretry = 3
        findtime = 10m
        bantime = 15m
        EOF
        sudo systemctl enable --now fail2ban
        sudo fail2ban-client status sshd

        # 5. Ejecutar auditoría de endurecimiento básica
        sudo lynis audit system --quick | tail -n 30
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador en e29-Win10-FW
        # 1. Asegurar los 3 perfiles de Defender Firewall habilitados
        Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
        Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction

        # 2. Crear regla acotada por IP remota origen (solo acepta desde 192.168.50.10)
        New-NetFirewallRule -DisplayName "Puerto 8080 Solo Ubuntu-FW" `
          -Direction Inbound -Protocol TCP -LocalPort 8080 `
          -RemoteAddress 192.168.50.10 -Profile Private -Action Allow

        # 3. Verificar conectividad hacia puertos filtrados vs abiertos en Ubuntu
        Test-NetConnection -ComputerName 192.168.50.10 -Port 80    # True
        Test-NetConnection -ComputerName 192.168.50.10 -Port 3306  # False (bloqueado por deny incoming)

        # 4. Auditar protección antimalware nativa en Windows
        Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntispywareEnabled
        ```

---

## Puntos de Control y Errores Frecuentes

- **`fail2ban` falla al arrancar en Ubuntu 24.04:** En versiones modernas de Ubuntu Server que ya no instalan `rsyslog` ni `/var/log/auth.log` por defecto, debes especificar `backend = systemd` en `/etc/fail2ban/jail.local` para que lea directamente desde `journald`.
- **Diferencia entre `ALLOW` y `LIMIT` en UFW:** `ufw limit ssh` añade una regla que bloquea nuevas conexiones de una IP si supera 6 intentos dentro de 30 segundos, añadiendo una primera barrera directamente en el kernel antes incluso de `fail2ban`.

## Recursos para Profundizar

- Concepto asociado: [Cortafuegos de Host (`ufw` y Defender)](../conceptos/ra6-seguridad-recursos-cortafuegos-ufw-defender.md) y [Utilidades Básicas de Seguridad](../conceptos/ra6-utilidades-seguridad-auditoria-endurecimiento.md).
- Vídeo recomendado sobre UFW y endurecimiento SSH: [Seguridad en red, cortafuegos UFW y SSH (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
