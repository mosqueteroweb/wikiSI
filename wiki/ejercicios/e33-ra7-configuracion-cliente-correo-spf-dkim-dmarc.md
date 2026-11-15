---
ra: RA7
ce:
  - RA7.d
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md
ultima_revision: "2026-11-15"
---

# e33 · Auditoría de Correo Electrónico Seguro (`SMTP`/`IMAP`, `SPF`, `DKIM`, `DMARC`) y Cliente Thunderbird

<!-- fuente: raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md -->

## Escenario y Topología VirtualBox

Un departamento técnico necesita validar que la configuración de correo electrónico corporativo utiliza exclusivamente protocolos cifrados en cliente (**Thunderbird**) y diagnosticar en línea de comandos si distintos dominios públicos tienen bien configuradas sus defensas DNS contra *phishing* y suplantación (**MX, SPF, DKIM y DMARC**).

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e33-Ubuntu`** | Ubuntu Desktop / Server 24.04 | **2 GB** | Consultas DNS (`dig`/`host`), verificación de puertos TLS SMTP/IMAP con `openssl` |
| **Total activo** | **1 VM ligera** | **2 GB** | Mínimo consumo sobre **MAX (16 GB)** |

## Objetivos

1. Consultar registros DNS de correo (**`MX`**, **`SPF`**, **`DMARC`**) mediante `dig` y PowerShell (`Resolve-DnsName`).
2. Comprobar la negociación criptográfica TLS de servidores **SMTP Submission (`587/STARTTLS`)**, **SMTPS (`465`)** e **IMAPS (`993`)** con `openssl s_client`.
3. Documentar los parámetros exactos de configuración segura en **Mozilla Thunderbird** (incluyendo soporte S/MIME / OpenPGP).

---

## Enunciado Detallado

1. **Auditoría DNS antisuplantación (`RA7.d`):**
   - Consulta los registros **`MX`**, **`TXT` SPF** y **`TXT` `_dmarc`** de al menos dos dominios reales consolidados (por ejemplo `debian.org` y `github.com`).
   - Interpreta el significado del sufijo `-all` frente a `~all` en SPF y qué diferencia existe en DMARC entre `p=none`, `p=quarantine` y `p=reject`.

2. **Comprobación de cifrado TLS en transporte (`RA7.d`):**
   - Comprueba con `openssl s_client` el certificado TLS ofrecido en puerto `993` (IMAPS) o `465` (SMTPS) frente a un servidor público estándar (ej. `imap.gmail.com:993`) sin necesidad de autenticarte en ninguna cuenta.
   - Elabora la ficha de configuración obligatoria que entregarías a un empleado para dar de alta su correo corporativo en **Mozilla Thunderbird** (indicando protocolo entrante, saliente, puertos y método de cifrado).

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Auditoría de registros `MX`, `SPF` y `DMARC`

    === "MAX / Ubuntu (Linux)"

        ```bash
        sudo apt-get update && sudo apt-get install -y dnsutils openssl

        # 1. Consultar servidores MX responsables de recibir correo
        dig MX debian.org +short
        dig MX github.com +short

        # 2. Consultar registros TXT SPF
        dig TXT debian.org +short | grep -i spf
        dig TXT github.com +short | grep -i spf

        # 3. Consultar políticas DMARC públicas en subdominio _dmarc
        dig TXT _dmarc.debian.org +short
        dig TXT _dmarc.github.com +short
        ```

    === "Windows 10 / 11"

        ```powershell
        # Consultas DNS equivalentes nativas en Windows PowerShell
        Resolve-DnsName -Name github.com -Type MX | Select-Object NameExchange, Preference
        Resolve-DnsName -Name github.com -Type TXT | Where-Object Strings -like "*spf1*"
        Resolve-DnsName -Name _dmarc.github.com -Type TXT
        ```

    ### 2. Verificación TLS en `IMAPS (993)` y ficha de parámetros Thunderbird

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Inspeccionar el handshake TLS real de un servidor IMAPS (sin iniciar sesión)
        openssl s_client -connect imap.gmail.com:993 -servername imap.gmail.com </dev/null 2>/dev/null |
          grep -E "Protocol|Cipher|subject=|issuer=|Verify return code"

        # Nota para STARTTLS en puerto 587 (SMTP Submission):
        # openssl s_client -starttls smtp -connect smtp.gmail.com:587 </dev/null
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar alcance TCP hacia puerto seguro IMAPS (993) y Submission (587)
        Test-NetConnection -ComputerName imap.gmail.com -Port 993
        Test-NetConnection -ComputerName smtp.gmail.com -Port 587
        ```

    ### 3. Interpretación y ficha de configuración recomendada

    - **SPF:** `-all` indica rechazo estricto (*Fail*) a cualquier servidor no listado; `~all` marca como sospechoso (*SoftFail*).
    - **DMARC:** `p=none` solo monitoriza enviando informes; `p=quarantine` envía a carpeta de Spam; `p=reject` bloquea directamente el correo falsificado.
    - **Ficha estándar cliente Thunderbird:**
      - **Entrante:** **IMAP** · Puerto **`993/TCP`** · Seguridad **`SSL/TLS`** · Contraseña normal o OAuth2.
      - **Saliente:** **SMTP** · Puerto **`587/TCP` (`STARTTLS`)** o **`465/TCP` (`SSL/TLS`)**.
      - **Opcional privacidad extrema:** Habilitar par de claves **OpenPGP** desde *Configuración de la cuenta → Cifrado de extremo a extremo*.

---

## Puntos de Control y Errores Frecuentes

- **IMAP vs POP3 en puestos múltiples:** Configurar **POP3** suele borrar los mensajes del servidor tras descargarlos, provocando que el usuario pierda correos al abrir su bandeja en otro ordenador o móvil. Usa **IMAP (`993`)** salvo necesidad explícita de archivo offline.
- **Usar puerto `25` para clientes de escritorio:** La mayoría de ISP domésticos y centros educativos bloquean el tráfico saliente cliente al puerto `25` para frenar bots de spam; los clientes configurados correctamente deben usar siempre **`587` (STARTTLS)** o **`465` (SMTPS)**.

## Recursos para Profundizar

- Concepto asociado: [Sistemas de Correo y Mensajería Corporativa Segura](../conceptos/ra7-sistemas-correo-mensajeria-corporativa-segura.md).
- Vídeo recomendado sobre comunicaciones seguras: [Comunicaciones seguras en red y correo (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
