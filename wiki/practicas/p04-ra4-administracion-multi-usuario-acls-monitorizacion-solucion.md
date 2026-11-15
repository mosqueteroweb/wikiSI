---
ra: RA4
ce:
  - RA4.a
  - RA4.b
  - RA4.c
  - RA4.d
  - RA4.e
  - RA4.f
  - RA4.g
  - RA4.h
tipo: solucion
publicar: false
fuentes:
  - raw/procesados/ra4-usuarios-grupos-directivas-seguridad.md
  - raw/procesados/ra4-permisos-locales-acls-herencia.md
  - raw/procesados/ra4-procesos-servicios-monitorizacion-desarrollo.md
ultima_revision: "2026-11-15"
---

# Solución Docente · p04 · Administración Multiusuario, ACLs, Servicios, Monitorización y Entorno DAM

> **Documento interno docente (`publicar: false`).** No publicar ni enlazar desde páginas públicas.

---

## Tarea 1 · Usuarios, Grupos y Delegación `sudo`

### En `DAM-Srv-Ubuntu` (2 GB RAM)

```bash
# Grupos
sudo groupadd kora_devs
sudo groupadd kora_qa

# Cuentas nominales
sudo useradd -m -c "Laura Dev" -s /bin/bash -G kora_devs laura.dev
sudo useradd -m -c "Marco QA" -s /bin/bash -G kora_qa marco.qa
sudo useradd -m -c "Sofia Lead" -s /bin/bash -G kora_devs,kora_qa sofia.lead

# Contraseñas iniciales temporales
echo "laura.dev:KoraDam#2026" | sudo chpasswd
echo "marco.qa:KoraDam#2026" | sudo chpasswd
echo "sofia.lead:KoraLead#2026" | sudo chpasswd

# Cuenta de servicio sin home y sin shell interactiva
sudo useradd -r -M -s /usr/sbin/nologin -c "CI Runner Kora" svc_ci

# Delegación sudo granular en /etc/sudoers.d/kora_lead
cat <<'EOF' | sudo tee /etc/sudoers.d/kora_lead
sofia.lead ALL=(root) /usr/bin/systemctl restart nginx, /usr/bin/journalctl, /usr/bin/apt update
EOF
sudo chmod 0440 /etc/sudoers.d/kora_lead
sudo visudo -c -f /etc/sudoers.d/kora_lead

# Verificaciones
id sofia.lead
sudo -l -U sofia.lead
getent passwd svc_ci
```

### En `DAM-Workstation-Win10` (4 GB RAM)

```powershell
New-LocalGroup -Name "kora_devs" -Description "Desarrolladores KoraApps"
New-LocalGroup -Name "kora_qa" -Description "Control de calidad KoraApps"

$pw = ConvertTo-SecureString "KoraDam#2026!" -AsPlainText -Force
New-LocalUser -Name "laura.dev" -FullName "Laura Dev" -Password $pw
New-LocalUser -Name "marco.qa" -FullName "Marco QA" -Password $pw
New-LocalUser -Name "sofia.lead" -FullName "Sofia Lead" -Password $pw

Add-LocalGroupMember -Group "kora_devs" -Member "laura.dev", "sofia.lead"
Add-LocalGroupMember -Group "kora_qa" -Member "marco.qa", "sofia.lead"
# Opcionalmente, en Windows sofia.lead puede añadirse a Administradores si ejerce soporte local
Add-LocalGroupMember -Group "Administradores" -Member "sofia.lead" -ErrorAction SilentlyContinue
```

---

## Tarea 2 · Directivas de Cuenta y Contraseñas

### Linux (`chage`)

```bash
sudo chage -M 90 -m 3 -W 10 laura.dev
sudo chage -M 90 -m 3 -W 10 -d 0 marco.qa
sudo chage -l marco.qa
```

### Windows (`net accounts`)

```cmd
net accounts /minpwlen:10 /maxpwage:90 /minpwage:3 /uniquepw:5
net accounts /lockoutthreshold:4 /lockoutduration:15 /lockoutwindow:15
net accounts
```

---

## Tarea 3 · SGID, Sticky Bit y ACLs

### Linux (`chmod 3770` + `setfacl`)

```bash
sudo apt-get update && sudo apt-get install -y acl
sudo mkdir -p /srv/kora_repo
sudo chown root:kora_devs /srv/kora_repo
sudo chmod 3770 /srv/kora_repo

# Permitir lectura y tránsito al grupo kora_qa (existentes y futuros ficheros/subcarpetas)
sudo setfacl -m g:kora_qa:rx /srv/kora_repo
sudo setfacl -d -m g:kora_qa:rX /srv/kora_repo

# Prueba funcional
sudo -u laura.dev touch /srv/kora_repo/release_v1.jar
ls -l /srv/kora_repo
# El grupo debe ser kora_devs por el SGID
sudo -u marco.qa ls -la /srv/kora_repo
sudo -u marco.qa rm /srv/kora_repo/release_v1.jar      # Debe fallar (Permission denied)
sudo -u marco.qa touch /srv/kora_repo/intruso.txt      # Debe fallar (Permission denied)
getfacl /srv/kora_repo
```

### Windows (`icacls`)

```cmd
mkdir C:\KoraRepo
icacls C:\KoraRepo /inheritance:d
icacls C:\KoraRepo /remove:g "*S-1-5-32-545"
icacls C:\KoraRepo /grant "kora_devs:(OI)(CI)M"
icacls C:\KoraRepo /grant "kora_qa:(OI)(CI)RX"
icacls C:\KoraRepo
```

---

## Tarea 4 · Procesos, Prioridades y Servicios

### Linux

```bash
sudo apt-get install -y nginx
sudo systemctl enable --now nginx
sudo systemctl reload nginx
systemctl status nginx --no-pager

nice -n 12 sleep 900 &
PID_S=$(pgrep -n sleep)
renice -n 18 -p "$PID_S"
ps -eo pid,ppid,ni,stat,comm | grep "$PID_S"
kill -15 "$PID_S"
```

### Windows (PowerShell Administrador)

```powershell
Get-Service Spooler | Select-Object Name, Status, StartType
Set-Service Spooler -StartupType Manual
Stop-Service Spooler -Force
Start-Service Spooler
Set-Service Spooler -StartupType Automatic
```

---

## Tarea 5 · Monitorización, Logs y Limpieza

### Linux

```bash
sudo apt-get install -y htop sysstat ncdu
free -h
vmstat 2 4
sudo journalctl -b -p err --no-pager | tail -n 20
sudo journalctl -u ssh -n 15 --no-pager || sudo journalctl --since "30 minutes ago" | grep -i sudo
sudo journalctl --vacuum-size=100M
sudo apt-get autoremove -y && sudo apt-get clean
```

### Windows

```powershell
Get-WinEvent -FilterHashtable @{ LogName = 'System'; Level = 1,2 } -MaxEvents 5 |
    Format-Table TimeCreated, Id, ProviderName
Get-Counter -Counter @("\Processor(_Total)\% Processor Time","\Memory\Available MBytes") -SampleInterval 2 -MaxSamples 3
```

---

## Tarea 6 · Entorno DAM, Script y Dimensionamiento

### Instalación SDKs y script `/usr/local/bin/kora_health.sh`

```bash
sudo apt-get install -y openjdk-21-jdk git python3-venv
echo 'export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"' >> ~/.bashrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

sudo tee /usr/local/bin/kora_health.sh > /dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "=== KoraApps Healthcheck ==="
echo "RAM available: $(free -h | awk '/^Mem:/ {print $7}')"
echo "Disco libre (/): $(df -h / | awk 'NR==2 {print $4}')"
echo "Servicio nginx: $(systemctl is-active nginx)"
EOF
sudo chmod 755 /usr/local/bin/kora_health.sh
/usr/local/bin/kora_health.sh
```

### Pauta de corrección del informe `RA4.h`

- **8 GB RAM:** Insuficiente para 1.º DAM cuando coexisten SO anfitrión (~2,5 GB), IDE Java + Gradle (3–4 GB), navegador (1,5–2 GB) y una VM VirtualBox de pruebas (2–4 GB): provocaría intercambio constante (*swapping/thrashing*), degradación grave de compilaciones y congelaciones del anfitrión.
- **16 GB RAM:** Mínimo operativo en aula manteniendo simultáneamente hasta 6–7 GB en VMs y el resto para MAX + IDE.
- **32 GB RAM + SSD NVMe:** Configuración profesional recomendada para contenedores, emulador Android/móvil e IDE sin cuellos de botella de IOPS ni memoria.
