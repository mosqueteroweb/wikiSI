---
ra: RA7
ce:
  - RA7.a
  - RA7.b
  - RA7.c
  - RA7.d
  - RA7.e
  - RA7.f
  - RA7.g
tipo: solucion
publicar: false
fuentes:
  - raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md
  - raw/procesados/ra7-ofimatica-colaboracion-documentacion-markdown.md
  - raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md
ultima_revision: "2026-11-15"
---

# Solución Docente · p07 · Auditoría de Licencias, Documentación, Correo, SFTP y Utilidades

> **Documento interno docente (`publicar: false`).** No publicar ni enlazar desde páginas públicas.

---

## Tarea 1 y 2 · Auditoría de Licencias y Selección Productiva

```bash
# En DAM-Doc-Ubuntu: inspección de copyright APT y pip-licenses en venv
grep -iE "License:" /usr/share/doc/git/copyright /usr/share/doc/bash/copyright | head -n 10
python3 -m venv /tmp/v_lic
/tmp/v_lic/bin/pip install --quiet requests pip-licenses
/tmp/v_lic/bin/pip-licenses
rm -rf /tmp/v_lic
```

**Tabla resumen de compatibilidad comercial cerrada:**
- **GPLv3 / AGPLv3:** Copyleft fuerte (obliga a liberar derivada; Nextcloud AGPLv3 también obliga si se sirve como SaaS).
- **MIT / Apache 2.0 / BSD:** Permisivas (permiten integración en producto propietario citando copyright original).
- **LibreOffice (MPL-2.0) / Nextcloud (AGPLv3):** Reducen TCO de licencias a 0 € en 20 puestos frente a suscripciones SaaS anuales (~20 × 12 € × 12 meses × 3 años ≈ 8.640 €), garantizan formatos ODF/PDF-A y alojamiento propio cumpliendo RGPD/ENS.

---

## Tarea 3 · Docs-as-Code (`Markdown + Git + Pandoc + LibreOffice`)

```bash
man rsync | grep -A 3 -- "--archive"
sudo apt-get update && sudo apt-get install -y git pandoc libreoffice-writer p7zip-full clamav dnsutils openssh-server
sudo systemctl enable --now ssh

mkdir -p ~/manual_pixelforge && cd ~/manual_pixelforge
git init && git config user.name "PixelForge Admin" && git config user.email "admin@pixelforge.local"

cat <<'EOF' > README.md
---
title: "Manual Estándar PixelForge DAM"
---

# Guía Corporativa de Documentación y Transferencia

| Herramienta | Formato / Puerto | Uso |
| :--- | :---: | :--- |
| LibreOffice / Pandoc | ODF / PDF-A | Documentación oficial |
| SFTP / rsync | 22/TCP | Intercambio cifrado |

```bash
rsync -avz --stats -e ssh ./origen/ usuario@192.168.90.10:/srv/respaldo/
```
EOF

printf "*.odt\n*.pdf\n*.html\n" > .gitignore
git add .gitignore README.md
git commit -m "docs: initial PixelForge standard manual"

pandoc README.md -o manual_pixelforge.odt --toc
soffice --headless --convert-to pdf manual_pixelforge.odt
```

---

## Tarea 4 · Auditoría DNS de Correo y Cifrado TLS

```bash
dig MX github.com +short
dig TXT github.com +short | grep -i spf
dig TXT _dmarc.github.com +short
openssl s_client -connect imap.gmail.com:993 -servername imap.gmail.com </dev/null 2>/dev/null | grep -E "Protocol|Cipher|Verify return code"
```

Configuración Thunderbird: **IMAPS `993/SSL/TLS`** entrada · **SMTP `587/STARTTLS` o `465/SSL/TLS`** salida · OpenPGP integrado para E2EE.

---

## Tarea 5 y 6 · SFTP, `SHA-256`, `rsync`, `7z -mhe=on` y ClamAV

En `DAM-Oficina-Win10`:
```powershell
New-Item -Path "C:\Temp\Entrega_PixelForge" -ItemType Directory -Force | Out-Null
"Artefacto oficial" | Out-File "C:\Temp\Entrega_PixelForge\acta.txt" -Encoding UTF8
Compress-Archive -Path "C:\Temp\Entrega_PixelForge\*" -DestinationPath "C:\Temp\Entrega_PixelForge.zip" -Force
(Get-FileHash "C:\Temp\Entrega_PixelForge.zip" -Algorithm SHA256).Hash
scp "C:\Temp\Entrega_PixelForge.zip" usuario@192.168.90.10:/tmp/
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled
```

En `DAM-Doc-Ubuntu`:
```bash
sha256sum /tmp/Entrega_PixelForge.zip
mkdir -p ~/espejo_backup
rsync -avz --stats /tmp/Entrega_PixelForge.zip ~/espejo_backup/
7z a -p"PixelClave#2026" -mhe=on ~/entrega_sellada.7z /tmp/Entrega_PixelForge.zip

sudo systemctl stop clamav-freshclam 2>/dev/null || true
sudo freshclam
mkdir -p /tmp/test_av
printf '%s' 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > /tmp/test_av/eicar.txt
clamscan -r /tmp/test_av/
clamscan -r --remove /tmp/test_av/
```
