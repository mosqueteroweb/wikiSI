---
ra: RA5
ce:
  - RA5.h
  - RA5.f
tipo: concepto
publicar: true
fuentes:
  - raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md
ultima_revision: "2026-11-15"
---

# Protocolos Seguros de Comunicaciones: TLS, SSH, SFTP y VPN

<!-- fuente: raw/procesados/ra5-puertos-diagnostico-protocolos-seguros.md -->

## 1. Por qué los Protocolos Clásicos son Inseguros

Protocolos diseñados en los orígenes de Internet (**Telnet**, **FTP**, **HTTP** sin TLS, **SMTP** en claro) transmiten usuarios, contraseñas y datos sin cifrado ni verificación de identidad. En una LAN compartida o red Wi-Fi pública, cualquier capturador (`Wireshark` / `tcpdump`) lee las credenciales al instante.

Todo protocolo seguro garantiza tres propiedades criptográficas:
1. **Confidencialidad:** nadie intermedio puede leer la carga útil (cifrado simétrico **AES-GCM** o **ChaCha20-Poly1305** tras negociación asimétrica).
2. **Integridad:** cualquier alteración del paquete en tránsito invalida el código de autenticación (**MAC / AEAD**).
3. **Autenticidad:** prueba criptográfica de que el servidor es quien dice ser mediante **certificados X.509 firmados por una CA** (HTTPS/TLS) o **clave pública/huella verificada** (SSH).

---

## 2. Mapa de Sustitución hacia Protocolos Seguros

| Protocolo inseguro (Obsoleto) | Alternativa segura actual | Puerto estándar | Tecnología de protección |
| :--- | :--- | :---: | :--- |
| **HTTP** | **HTTPS** | `443/TCP` | **TLS 1.3 / 1.2** + certificado X.509 |
| **Telnet / rlogin** | **SSH** (OpenSSH) | `22/TCP` | Cifrado punto a punto + par de claves **Ed25519 / RSA** |
| **FTP** | **SFTP** (sobre SSH) / **FTPS** | `22/TCP` o `990/TCP` | Canal cifrado completo (datos + credenciales) |
| **DNS UDP plano** | **DoT** / **DoH** | `853/TCP` / `443/TCP` | Consultas DNS cifradas frente a observadores del ISP |
| **Tráfico intersede en claro** | **VPN (WireGuard / OpenVPN / IPsec)** | `51820/UDP` (WG) | Túnel IP cifrado extremo a extremo |

---

## 3. Despliegue Seguro con SSH y Verificación TLS

La autenticación mediante **claves públicas Ed25519** supera ampliamente al uso de contraseñas repetidas en SSH: el cliente guarda su **clave privada (`~/.ssh/id_ed25519`, permisos `0600`)** sin salir jamás del equipo y copia la **clave pública (`id_ed25519.pub`)** al fichero `~/.ssh/authorized_keys` del servidor.

=== "MAX / Ubuntu (Linux)"

    ```bash
    # 1. Generar par de claves moderno Ed25519 en cliente MAX o Ubuntu
    ssh-keygen -t ed25519 -C "pedro@dam-aula"

    # 2. Copiar clave pública al servidor remoto sin pegado manual erróneo
    ssh-copy-id usuario@192.168.50.10

    # 3. Transferir ficheros de forma cifrada con SFTP / SCP
    scp -i ~/.ssh/id_ed25519 ./entrega.tar.gz usuario@192.168.50.10:/home/usuario/

    # 4. Auditar certificado TLS y versión negociada de un servicio HTTPS
    openssl s_client -connect github.com:443 -servername github.com </dev/null 2>/dev/null | grep -E "Protocol|Cipher|subject="
    ```

=== "Windows 10 / 11"

    Windows 10 y 11 integran el cliente **OpenSSH nativo** en PowerShell/CMD (y la opción de habilitar el servidor SSH en *Características opcionales*):

    ```powershell
    # 1. Generar par de claves Ed25519 en $HOME\.ssh\
    ssh-keygen -t ed25519 -C "dam-win10"

    # 2. Copiar clave pública al servidor Linux vía tubería SSH
    Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" |
      ssh usuario@192.168.50.10 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

    # 3. Iniciar sesión interactiva segura o sesión SFTP
    ssh usuario@192.168.50.10
    sftp usuario@192.168.50.10
    ```

> [!IMPORTANT]
> **Verificación de huella (*fingerprint*):** La primera vez que conectas por SSH a un servidor, el cliente guarda la clave pública del servidor en `~/.ssh/known_hosts`. Si en el futuro cambia inesperadamente y aparece el aviso `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`, puede indicar un ataque *Man-in-the-Middle* (o que la VM ha sido reinstalada).

---

## Recursos para profundizar

- Concepto anterior: [Gestión de Puertos y Diagnóstico Sistemático de Red](ra5-gestion-puertos-herramientas-diagnostico-red.md).
- Guía oficial OpenSSH / Mozilla SSL Config: [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/).
- Vídeo recomendado sobre comunicaciones seguras: [SSH, SFTP, cortafuegos y comunicaciones seguras (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
