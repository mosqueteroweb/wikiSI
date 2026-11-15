---
ra: RA5
ce:
  - RA5.f
  - RA5.h
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md
ultima_revision: "2026-11-15"
---

# e25 · Comunicaciones Seguras: Acceso SSH por Claves Ed25519, SFTP e Inspección TLS

<!-- fuente: raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md -->

## Escenario y Topología VirtualBox

En el laboratorio reemplazaremos la administración insegura sin cifrado por un túnel **OpenSSH** autenticado mediante criptografía de clave pública **Ed25519**, probaremos transferencia segura de ficheros (**SFTP**) y auditaremos certificados **TLS/HTTPS** reales desde línea de comandos.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e25-Ubuntu-Srv`** | Ubuntu Server 24.04 | **2 GB** | Servidor OpenSSH (`sshd` en TCP `22`) y receptor SFTP |
| **`e25-Win10-Cli`** | Windows 10 Education / Pro | **4 GB** | Cliente OpenSSH nativo generando par de claves y verificando TLS |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Cumple estrictamente el presupuesto **MAX 16 GB** |

## Objetivos

1. Desplegar el servidor **OpenSSH** en Ubuntu verificando su escucha en el puerto **`22/TCP`**.
2. Generar un par de claves **Ed25519** en cliente Windows/MAX y copiar la clave pública sin comprometer jamás la clave privada.
3. Deshabilitar el acceso `root` directo por SSH, probar transferencia cifrada **SFTP** y consultar protocolo y certificado X.509 de un servidor **HTTPS**.

---

## Enunciado Detallado

1. **Instalación y endurecimiento básico de OpenSSH (`RA5.f`, `RA5.h`):**
   - Instala `openssh-server` en **`e25-Ubuntu-Srv`** y verifica con `systemctl status ssh` y `ss -tulnp | grep :22` que está escuchando.
   - Edita `/etc/ssh/sshd_config` (o crea un archivo modular en `/etc/ssh/sshd_config.d/99-dam-seguro.conf`) fijando `PermitRootLogin no` y `PubkeyAuthentication yes`, valida sintaxis con `sudo sshd -t` y recarga `ssh`.

2. **Autenticación por clave pública Ed25519 y SFTP (`RA5.h`):**
   - Desde el cliente (`e25-Win10-Cli` o anfitrión MAX), genera un par de claves `ssh-keygen -t ed25519`, inspecciona el contenido de la **clave pública `.pub`** (nunca la privada) y autorízala en `~/.ssh/authorized_keys` del servidor Ubuntu con permisos `600`.
   - Conecta por `ssh` comprobando el aviso de huella (*fingerprint*) la primera vez, entra sin teclear la contraseña de cuenta del servidor (solo la *passphrase* si pusiste una) y sube un fichero de prueba mediante **`sftp`**.

3. **Auditoría rápida de certificado TLS (`RA5.h`):**
   - Desde terminal Linux, inspecciona con `openssl s_client` la versión de TLS negociada y el emisor del certificado para `github.com:443`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Instalación y endurecimiento del servidor OpenSSH (`e25-Ubuntu-Srv`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar OpenSSH Server
        sudo apt-get update && sudo apt-get install -y openssh-server
        sudo systemctl enable --now ssh

        # Comprobar puerto TCP 22 en escucha
        sudo ss -tulnp | grep ":22"

        # Crear configuración modular segura
        sudo tee /etc/ssh/sshd_config.d/99-dam-seguro.conf > /dev/null <<'EOF'
        PermitRootLogin no
        PubkeyAuthentication yes
        MaxAuthTries 4
        EOF

        # Validar sintaxis antes de recargar para no quedar fuera
        sudo sshd -t && sudo systemctl reload ssh
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar si OpenSSH Client está disponible en Windows 10/11
        Get-Command ssh, ssh-keygen, sftp
        ```

    ### 2. Generación de clave Ed25519, autorización y transferencia SFTP (`RA5.h`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Si conectamos desde MAX u otra VM Linux cliente:
        ssh-keygen -t ed25519 -C "alumno@dam-max"
        ls -la ~/.ssh/

        # Enviar clave pública al servidor Ubuntu (sustituir usuario e IP de laboratorio)
        ssh-copy-id usuario@192.168.50.10

        # Probar acceso SSH y transferencia cifrada SFTP
        echo "Archivo cifrado de prueba" > informe.txt
        sftp usuario@192.168.50.10 <<'EOF'
        put informe.txt /tmp/informe.txt
        ls -l /tmp/informe.txt
        bye
        EOF
        ```

    === "Windows 10 / 11"

        ```powershell
        # En PowerShell sobre e25-Win10-Cli:
        # 1. Generar par de claves Ed25519 (aceptar ruta por defecto C:\Users\<usuario>\.ssh\id_ed25519)
        ssh-keygen -t ed25519 -C "dam-win10"

        # 2. Subir clave pública y ajustar permisos estrictos en el servidor Linux remoto
        Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" |
          ssh usuario@192.168.50.10 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

        # 3. Iniciar sesión sin contraseña de usuario y abrir sesión SFTP cifrada
        ssh usuario@192.168.50.10 "hostname && whoami"
        New-Item -Path ".\prueba_sftp.txt" -ItemType File -Value "Envio cifrado SFTP" -Force
        scp .\prueba_sftp.txt usuario@192.168.50.10:/tmp/
        ```

    ### 3. Verificación de protocolo TLS y certificado HTTPS (`RA5.h`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Consultar versión TLS (ej. TLSv1.3), conjunto de cifrado y sujeto del certificado
        openssl s_client -connect github.com:443 -servername github.com </dev/null 2>/dev/null |
          grep -E "Protocol|Cipher|subject=|issuer="
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar conectividad HTTPS con PowerShell y validar certificado sin errores SSL
        Invoke-WebRequest -Uri "https://github.com" -Method Head -UseBasicParsing | Select-Object StatusCode
        ```

---

## Puntos de Control y Errores Frecuentes

- **Permisos laxos en `~/.ssh`:** Si en el servidor Linux el directorio `~/.ssh` tiene permisos distintos de `700` o `~/.ssh/authorized_keys` tiene permisos de escritura para grupo/otros (p. ej. `644` o `666`), OpenSSH **rechaza silenciosamente** la clave pública y vuelve a pedir contraseña. Fija siempre `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`.
- **Diferencia entre `id_ed25519` e `id_ed25519.pub`:** La clave privada (`id_ed25519`) **jamás** se copia ni se sube a GitHub ni al servidor remoto; solo se distribuye la pública (`.pub`).

## Recursos para Profundizar

- Concepto asociado: [Protocolos Seguros de Comunicaciones (TLS, SSH, SFTP y VPN)](../conceptos/ra5-protocolos-seguros-comunicaciones-tls-ssh-vpn.md).
- Vídeo recomendado sobre SSH, SFTP y comunicaciones seguras: [SSH, SFTP y comunicaciones seguras en red (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
