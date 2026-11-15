---
ra: RA6
ce:
  - RA6.c
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md
ultima_revision: "2026-11-15"
---

# e27 · Despliegue de Servidor NFSv4 (`root_squash`), Cola de Impresión CUPS y Proxy de Aplicaciones

<!-- fuente: raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md -->

## Escenario y Topología VirtualBox

En un entorno cien por cien Linux (**4 GB totales** sobre anfitrión **MAX de 16 GB**), montaremos tres servicios clásicos del apartado de servidores de red: exportación de directorios por **NFSv4**, cola de impresión **CUPS** (generando salida virtual PDF) y publicación de una pequeña aplicación backend protegida por **Nginx como proxy inverso**.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e27-Ubuntu-Srv`** | Ubuntu Server 24.04 | **2 GB** | Servidor NFSv4 (`2049`), CUPS (`631`) y Nginx proxy inverso (`80` → `8080`) |
| **`e27-Ubuntu-Cli`** | Ubuntu Desktop / Server 24.04 | **2 GB** | Cliente montando el recurso NFS y consumiendo la aplicación HTTP |
| **Total activo** | **2 VMs simultáneas** | **4 GB** | Margen libre **12 GB** en anfitrión **MAX** |

## Objetivos

1. Exportar una carpeta mediante **NFSv4** verificando la protección **`root_squash`** al escribir desde el cliente como `root`.
2. Configurar una impresora virtual PDF en **CUPS** y revisar el estado de colas con `lpstat`.
3. Publicar un servicio backend en `127.0.0.1:8080` oculto a la red externa a través de **Nginx** en puerto `80`.

---

## Enunciado Detallado

1. **Servidor y Cliente NFSv4 (`RA6.c`):**
   - En **`e27-Ubuntu-Srv`** (`192.168.50.10`), instala `nfs-kernel-server`, crea `/srv/nfs_datos` con permisos `777` temporales (o propiedad compartida `nobody:nogroup`) y expórtalo en `/etc/exports` solo a tu red interna (`192.168.50.0/24(rw,sync,no_subtree_check,root_squash)`).
   - Recarga con `sudo exportfs -ra`. Desde **`e27-Ubuntu-Cli`** (`192.168.50.11`), instala `nfs-common`, monta en `/mnt/nfs_remoto`, crea un fichero usando `sudo touch /mnt/nfs_remoto/test_root.txt` y comprueba en el servidor quién figura como propietario del fichero (`ls -l`) gracias a **`root_squash`**.

2. **Impresión CUPS y Proxy Inverso de Aplicaciones (`RA6.c`):**
   - En **`e27-Ubuntu-Srv`**, instala `cups` y `printer-driver-cups-pdf`, revisa las impresoras con `lpstat -p -d` e imprime un archivo de prueba por CLI (`lp`).
   - Configura **Nginx** escuchando en el puerto `80` como `proxy_pass http://127.0.0.1:8080;` hacia una app Python en puerto `8080` ligada exclusivamente a localhost, comprobando desde **`e27-Ubuntu-Cli`** que accede por puerto `80` mientras `8080` queda inaccesible directamente.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Servidor y cliente NFSv4 con verificación `root_squash`

    === "MAX / Ubuntu (Linux)"

        ```bash
        # --- En e27-Ubuntu-Srv (192.168.50.10) ---
        sudo apt-get update && sudo apt-get install -y nfs-kernel-server
        sudo mkdir -p /srv/nfs_datos
        sudo chown nobody:nogroup /srv/nfs_datos
        sudo chmod 0775 /srv/nfs_datos

        echo "/srv/nfs_datos 192.168.50.0/24(rw,sync,no_subtree_check,root_squash)" |
          sudo tee -a /etc/exports
        sudo exportfs -ra
        sudo exportfs -v

        # --- En e27-Ubuntu-Cli (192.168.50.11) ---
        sudo apt-get update && sudo apt-get install -y nfs-common
        sudo mkdir -p /mnt/nfs_remoto
        sudo mount -t nfs4 192.168.50.10:/srv/nfs_datos /mnt/nfs_remoto
        sudo touch /mnt/nfs_remoto/test_root.txt

        # Volver al servidor y comprobar que el dueño NO es root, sino nobody (o 65534)
        ls -ln /srv/nfs_datos/test_root.txt
        ```

    === "Windows 10 / 11"

        ```powershell
        # Nota informativa: Windows utiliza principalmente SMB (puerto 445) y Spooler/IPP.
        # El cliente NFS en Windows está disponible solo como característica opcional (Ediciones Pro/Enterprise).
        Get-WindowsOptionalFeature -Online -FeatureName *NFS* -ErrorAction SilentlyContinue
        ```

    ### 2. Impresión CUPS (`printer-driver-cups-pdf`) y Proxy Inverso Nginx (`80 → 8080`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # --- En e27-Ubuntu-Srv ---
        # A) Servidor de impresión CUPS con cola virtual PDF
        sudo apt-get install -y cups printer-driver-cups-pdf
        sudo systemctl enable --now cups
        lpstat -p -d
        echo "Prueba cola CUPS DAM" | lp -d PDF
        ls -la ~/PDF/ /var/spool/cups-pdf/ANONYMOUS/ 2>/dev/null

        # B) Backend protegido en 127.0.0.1:8080 + Proxy inverso Nginx en 80
        sudo apt-get install -y nginx
        python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &

        sudo tee /etc/nginx/sites-available/app_dam > /dev/null <<'EOF'
        server {
            listen 80 default_server;
            location / {
                proxy_pass http://127.0.0.1:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }
        EOF
        sudo ln -sf /etc/nginx/sites-available/app_dam /etc/nginx/sites-enabled/default
        sudo nginx -t && sudo systemctl reload nginx

        # Comprobar desde e27-Ubuntu-Cli:
        # curl -I http://192.168.50.10       -> 200 OK (vía Nginx)
        # nc -zv 192.168.50.10 8080          -> Connection refused (aislado en localhost)
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar impresión IPP/Spooler y acceso HTTP al proxy Nginx desde Windows si estuviera presente
        Get-Printer | Select-Object Name, PortName, Shared
        Invoke-WebRequest -Uri "http://192.168.50.10" -UseBasicParsing | Select-Object StatusCode
        ```

---

## Puntos de Control y Errores Frecuentes

- **`no_root_squash` es un riesgo grave:** Permite que cualquier cliente que monte la carpeta como `root` pueda crear ejecutables SUID o alterar permisos arbitrarios del volumen compartido. Mantén siempre **`root_squash`**.
- **Nginx `502 Bad Gateway`:** Indica que Nginx funciona bien en el puerto `80`, pero el proceso backend en `127.0.0.1:8080` está caído o escuchando en otro puerto.

## Recursos para Profundizar

- Concepto asociado: [Servidores de Ficheros (SMB/NFS), Impresión (CUPS) y Aplicaciones](../conceptos/ra6-servidores-ficheros-impresion-aplicaciones.md).
- Vídeo recomendado sobre servidores de red en Linux: [Samba y servicios de red compartidos (YouTube)](https://www.youtube.com/watch?v=ayaI9WNiFXA).
