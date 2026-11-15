---
ra: RA7
ce:
  - RA7.e
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md
ultima_revision: "2026-11-15"
---

# e34 · Transferencia Segura en Red (`SFTP`, `SCP`, `rsync`) y Verificación Criptográfica (`SHA-256`)

<!-- fuente: raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md -->

## Escenario y Topología VirtualBox

Un equipo de desarrollo necesita distribuir una nueva versión compilada de su aplicación junto con activos multimedia entre una estación Windows 10 (**`e34-Win10`**) y un servidor Linux Ubuntu (**`e34-Ubuntu`**), garantizando cifrado durante el tránsito, eficiencia diferencial en futuras actualizaciones y validación de integridad sin errores mediante **SHA-256**.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e34-Ubuntu`** | Ubuntu Server 24.04 | **2 GB** | Servidor SSH/SFTP (`openssh-server`) y receptor `rsync` |
| **`e34-Win10`** | Windows 10 Education / Pro | **4 GB** | Cliente emisor `scp` / `sftp` / `Get-FileHash` (y opcional WinSCP/FileZilla) |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Cumple margen seguro en **MAX (16 GB)** |

## Objetivos

1. Enviar lotes de archivos mediante **`sftp`** y **`scp`** verificando que no circulan credenciales ni datos sin cifrar.
2. Sincronizar incrementalmente un árbol de directorios mediante **`rsync -avz -e ssh`** comprobando la velocidad diferencial en el segundo envío.
3. Generar y validar firmas **`SHA-256`** tanto en Linux (`sha256sum -c`) como en Windows (`Get-FileHash`) detectando alteraciones intencionadas.

---

## Enunciado Detallado

1. **Empaquetado, firma y transferencia SFTP (`RA7.e`):**
   - En **`e34-Win10`** (o en una carpeta cliente), crea un directorio `release_v2` con 3 archivos de prueba, comprímelo en `.zip` y calcula su hash **SHA-256** (`Get-FileHash`).
   - Transfiere el `.zip` a `/tmp/entregas/` dentro de **`e34-Ubuntu`** (`192.168.50.10`) utilizando una sesión interactiva **`sftp`** (`mkdir`, `put`, `ls`).
   - En **`e34-Ubuntu`**, comprueba con `sha256sum` que la firma coincide bit a bit con la calculada en Windows.

2. **Sincronización incremental `rsync` sobre SSH (`RA7.e`):**
   - Desde una sesión Linux (o WSL/MAX hacia `e34-Ubuntu`), sincroniza una carpeta `web_estatica` de al menos 20 archivos con `rsync -avz --progress -e ssh`, añade 1 archivo nuevo, vuelve a lanzar `rsync` y verifica que solo transmite el archivo modificado.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Empaquetado, cálculo de hash SHA-256 y envío con SFTP (`RA7.e`)

    === "Windows 10 / 11"

        ```powershell
        # En e34-Win10: crear carpeta de ejemplo y comprimirla
        New-Item -Path "C:\Temp\release_v2" -ItemType Directory -Force | Out-Null
        "Version 2.0 compilada" | Out-File "C:\Temp\release_v2\README.txt" -Encoding UTF8
        "Configuracion produccion" | Out-File "C:\Temp\release_v2\app.properties" -Encoding UTF8

        Compress-Archive -Path "C:\Temp\release_v2\*" -DestinationPath "C:\Temp\release_v2.zip" -Force

        # Calcular suma criptográfica SHA-256 antes de transferir
        (Get-FileHash "C:\Temp\release_v2.zip" -Algorithm SHA256).Hash

        # Enviar usando cliente SCP nativo o sesión SFTP interactiva (si existe en servidor):
        scp "C:\Temp\release_v2.zip" usuario@192.168.50.10:/tmp/
        ```

    === "MAX / Ubuntu (Linux)"

        ```bash
        # En e34-Ubuntu: asegurar que openssh-server está activo y comprobar directorio de destino
        sudo systemctl status ssh --no-pager

        # Calcular y verificar huella SHA-256 en el receptor
        sha256sum /tmp/release_v2.zip
        # Comparar exactamente la cadena hexadecimal de 64 caracteres con la salida de Windows PowerShell

        # Ejemplo de sesión interactiva SFTP desde un cliente Linux/MAX:
        # sftp usuario@192.168.50.10
        # sftp> mkdir /tmp/entregas
        # sftp> put release_v2.zip /tmp/entregas/
        # sftp> ls -lh /tmp/entregas/
        # sftp> bye
        ```

    ### 2. Sincronización diferencial segura con `rsync` sobre SSH (`RA7.e`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Simular carpeta de origen con 20 ficheros desde el host MAX o cliente Linux
        mkdir -p ~/web_estatica && touch ~/web_estatica/pagina_{01..20}.html

        # Primera sincronización: crea la carpeta remota y transfiere los 20 archivos cifrados por SSH
        rsync -avz --progress -e ssh ~/web_estatica/ usuario@192.168.50.10:/tmp/web_destino/

        # Modificar únicamente un archivo nuevo y re-ejecutar exactamente el mismo comando
        echo "Actualización incremental" > ~/web_estatica/novedades.html
        rsync -avz --stats -e ssh ~/web_estatica/ usuario@192.168.50.10:/tmp/web_destino/
        # Observa en --stats que 'Number of regular files transferred: 1' (ahorro masivo de ancho de banda)
        ```

    === "Windows 10 / 11"

        ```powershell
        # En Windows GUI para usuarios administrativos, instalar WinSCP o FileZilla mediante winget:
        # winget install --id TimKosse.FileZilla.Client -e
        # Nota crítica: en Gestor de Sitios elegir SIEMPRE protocolo "SFTP - SSH File Transfer Protocol" (puerto 22).
        Write-Host "Para transferencias incrementales masivas desde Windows se recomienda usar WSL o WinSCP Synchronize (SFTP)."
        ```

---

## Puntos de Control y Errores Frecuentes

- **Barra final `/` en `rsync`:** Escribir `rsync -avz origen/ destino/` copia el **contenido** de `origen`, mientras que `rsync -avz origen destino/` crea una carpeta `destino/origen/`. Presta siempre atención a esa `/` final antes de añadir `--delete`.
- **Diferencia de mayúsculas en hashes:** PowerShell imprime los hashes SHA-256 en **MAYÚSCULAS** y `sha256sum` de Linux en **minúsculas**, pero representan exactamente el mismo valor hexadecimal.

## Recursos para Profundizar

- Concepto asociado: [Servicios de Transferencia de Ficheros (`SFTP`, `SCP`, `rsync`)](../conceptos/ra7-servicios-transferencia-ficheros-sftp-scp-sincronizacion.md).
- Vídeo recomendado sobre SFTP: [Transferencias seguras con SFTP y SSH (YouTube)](https://www.youtube.com/watch?v=S-2TIRnsioM).
- Vídeo recomendado sobre `rsync`: [Sincronización diferencial con rsync (YouTube)](https://www.youtube.com/watch?v=MPqCAhVKlBs).
