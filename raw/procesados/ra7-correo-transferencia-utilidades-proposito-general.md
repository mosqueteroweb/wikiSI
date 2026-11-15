---
tema: "Correo Corporativo Seguro, Transferencia de Ficheros y Utilidades de Propósito General"
ra: RA7
ce:
  - RA7.d
  - RA7.e
  - RA7.g
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA7 (3/3) · Correo, Transferencia de Ficheros y Utilidades

## 1. Sistemas de Correo Electrónico y Mensajería Corporativa (`RA7.d`)

- **Protocolos de envío y recepción:**
  - **Envío (MTA / MSA):** **SMTP** con cifrado obligatorio en puerto **`587/TCP` (Submission + STARTTLS)** o **`465/TCP` (SMTPS)** — el puerto clásico `25` se usa solo entre servidores MTA, nunca para clientes finales sin cifrar.
  - **Recepción (MUA):** **IMAP (`993/TCP` IMAPS)** recomendado (sincroniza carpetas y estados en servidor para multidispositivo) frente a **POP3 (`995/TCP` POP3S)** (pensado para descargar y borrar del servidor).
- **Seguridad antispam, antiphishing y cifrado:**
  - **SPF** (registro DNS `TXT` que lista qué servidores IP están autorizados a enviar correos en nombre del dominio).
  - **DKIM** (firma criptográfica del mensaje comprobable mediante clave pública en DNS).
  - **DMARC** (política de rechazo/cuarentena si fallan SPF y DKIM + informes de suplantación).
  - Clientes habituales: **Mozilla Thunderbird** (multiplataforma FOSS, soporte S/MIME y OpenPGP nativo integrado), clientes webmail (*Roundcube*, *Nextcloud Mail*), mensajería corporativa federada o cifrada (**Matrix/Element**, **Mattermost**, **Slack/Teams**).

## 2. Transferencia y Sincronización de Ficheros en Red (`RA7.e`)

- **Sustitución definitiva de FTP plano (`21`):** usar **SFTP (`22/TCP`)** / **SCP** sobre túnel SSH, o **FTPS (`990/TCP` TLS)** en integraciones heredadas.
- **Sincronización diferencial:** **`rsync -avz -e ssh`** transfiere únicamente bloques modificados con compresión y cifrado SSH; clientes gráficos multiplataforma como **FileZilla** (usando explícitamente protocolo `SFTP - SSH File Transfer Protocol`) o **WinSCP** en Windows.
- **Verificación de integridad tras transferencia:** comparar siempre sumas criptográficas **`sha256sum`** (Linux) o **`Get-FileHash -Algorithm SHA256`** (Windows) en origen y destino para archivos críticos (ISOs, binarios `jar`/instaladores, backups).

## 3. Utilidades de Propósito General (`RA7.g`)

- **Compresión y empaquetado:** `tar` + `gzip` / `xz` / `zstd` (`.tar.gz`, `.tar.zst`), `zip` / `unzip`, **7-Zip (`7z`)** (alta compresión AES-256) y `PeaZip`.
- **Seguridad antimalware y verificación:** **ClamAV (`clamscan` / `freshclam`)** en servidores Linux de intercambio, **Microsoft Defender** en Windows, verificación de firma digital.
- **Grabación y recuperación de medios / diagnóstico:** utilidades multiplataforma **Ventoy** / **BalenaEtcher** / **Rufus**, capturadores técnicos (**Flameshot**), lectores PDF libres (**Okular** / **Evince**), gestores de contraseñas cifrados (**KeePassXC** con base `.kdbx`), conversión documental (**Pandoc**, **ImageMagick**).
