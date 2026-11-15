---
ra: RA7
ce:
  - RA7.f
  - RA7.g
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md
ultima_revision: "2026-11-15"
---

# e35 · Utilidades de Propósito General: Compresión Cifrada (`7z`/`tar`), Antimalware (`ClamAV`/Defender) y Rescate

<!-- fuente: raw/procesados/ra7-correo-transferencia-utilidades-proposito-general.md -->

## Escenario y Topología VirtualBox

Antes de archivar documentación confidencial o aceptar descargas externas en un servidor departamental, utilizaremos herramientas de propósito general multiplataforma para comprimir con cifrado **AES-256**, analizar carpetas en busca de amenazas con **ClamAV** / **Microsoft Defender** (verificado con el archivo inocuo estándar de prueba **`EICAR`**) y contrastar su sintaxis en la documentación oficial.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e35-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | `tar`, `7z` cifrado (`-mhe=on`), `ClamAV` y archivo de prueba `EICAR` |
| **`e35-Win10`** | Windows 10 Education / Pro | **4 GB** | `Compress-Archive`, `7-Zip` / Windows Defender (`Start-MpScan`) |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Operativo dentro del presupuesto de aula (**MAX 16 GB**) |

## Objetivos

1. Empaquetar respetando permisos con `tar` (`.tar.gz` / `.tar.zst`) frente a crear archivos **`7z` cifrados con AES-256 y cabeceras ocultas (`-mhe=on`)**.
2. Instalar y probar el motor antivirus FOSS **ClamAV** sobre un fichero de prueba inofensivo estándar de la industria (**EICAR test string**) y comprobar su detección en Windows Defender.
3. Consultar la ayuda oficial local antes de ejecutar parámetros avanzados (`RA7.f`).

---

## Enunciado Detallado

1. **Empaquetado y cifrado portátil (`RA7.g`, `RA7.f`):**
   - Consulta la página de manual `man 1 7z` (o `7z --help`) y comprueba qué diferencia existe entre `-p` y `-mhe=on`.
   - En **`e35-Ubuntu`**, crea una carpeta `~/confidencial` con dos archivos, empaquétala primero con `tar -czvf` (observando en `tar -tvf` que preserva usuario/permisos POSIX) y después protégela con `7z a -p -mhe=on secreto.7z ~/confidencial/` comprobando que al listar contenido con `7z l secreto.7z` pide contraseña incluso para ver los nombres de archivo.

2. **Detección antimalware estándar con test EICAR (`RA7.g`):**
   - Instala `clamav` en **`e35-Ubuntu`**, actualiza la base de firmas (`sudo freshclam` deteniendo antes `clamav-freshclam` si bloquea el fichero lock) y analiza la carpeta limpia `~/confidencial`.
   - Crea dentro de `/tmp/test_av/` la cadena oficial **EICAR** *(Nota: es una firma inocua de 68 bytes diseñada exclusivamente para verificar que los antivirus están operativos — **no** es software malicioso real)* y ejecuta `clamscan -r /tmp/test_av/` para observar la detección `Eicar-Signature FOUND` y su borrado controlado con `--remove`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Compresión preservando permisos (`tar`) y cifrado `7z` con cabeceras cifradas

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar 7-Zip CLI (p7zip-full) y zstd
        sudo apt-get update && sudo apt-get install -y p7zip-full zstd

        mkdir -p ~/confidencial
        echo "Contrato de confidencialidad DAM" > ~/confidencial/contrato.txt
        chmod 600 ~/confidencial/contrato.txt

        # 1. Empaquetar preservando permisos POSIX estrictos (600) con tar + gzip
        tar -czvf ~/confidencial.tar.gz ~/confidencial/
        tar -tvzf ~/confidencial.tar.gz

        # 2. Cifrar con AES-256 ocultando también los nombres de ficheros (-mhe=on)
        7z a -p"ClaveSuperSegura#2026" -mhe=on ~/secreto.7z ~/confidencial/

        # Verificar que ni siquiera el listado funciona sin la contraseña
        7z l -p"ClaveIncorrecta" ~/secreto.7z 2>&1 | head -n 10
        ```

    === "Windows 10 / 11"

        ```powershell
        # Empaquetado nativo ZIP en PowerShell o instalación de 7-Zip
        New-Item -Path "C:\Temp\Confidencial" -ItemType Directory -Force | Out-Null
        "Documento interno" | Out-File "C:\Temp\Confidencial\nota.txt"
        Compress-Archive -Path "C:\Temp\Confidencial\*" -DestinationPath "C:\Temp\nota.zip" -Force

        # Instalar 7-Zip FOSS en Windows si se requiere cifrado AES-256 (.7z):
        # winget install --id 7zip.7zip -e
        ```

    ### 2. Verificación antimalware con ClamAV / Defender y firma inocua EICAR (`RA7.g`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        sudo apt-get install -y clamav

        # Actualizar firmas (si el servicio en segundo plano bloquea el log, detenerlo un instante)
        sudo systemctl stop clamav-freshclam 2>/dev/null || true
        sudo freshclam
        sudo systemctl start clamav-freshclam 2>/dev/null || true

        # Crear archivo inofensivo estándar EICAR (68 bytes oficiales) en /tmp/test_av/
        mkdir -p /tmp/test_av
        printf '%s' 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > /tmp/test_av/eicar.txt

        # Analizar carpeta con ClamAV y verificar detección + limpieza posterior
        clamscan -r /tmp/test_av/
        # Resultado esperado: /tmp/test_av/eicar.txt: Eicar-Signature FOUND

        # Eliminar el archivo de prueba detectado de forma controlada
        clamscan -r --remove /tmp/test_av/
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar estado y lanzar análisis personalizado en Windows Defender
        Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureVersion
        Start-MpScan -ScanType CustomScan -ScanPath "C:\Temp\Confidencial"
        ```

---

## Puntos de Control y Errores Frecuentes

- **Olvidar `-mhe=on` en `7z`:** Sin `-mhe=on` (*Encrypt File Headers*), el contenido de los archivos queda cifrado pero cualquiera que ejecute `7z l secreto.7z` sigue viendo los nombres completos de tus documentos internos.
- **No uses `ZIP` tradicional para secretos críticos:** El algoritmo de cifrado clásico ZipCrypto es criptográficamente débil; usa siempre AES-256 (en `.7z` o `7z a -mem=AES256 archivo.zip`).
- **Memoria en ClamAV (`clamscan` vs `clamd`):** En máquinas con poca RAM (`2 GB`), cargar toda la base de firmas al vuelo en cada `clamscan` puede rozar `1,2 GB` de pico; evita lanzar dos escaneos simultáneos y apaga `clamav-daemon` residente si no lo necesitas constantemente.

## Recursos para Profundizar

- Concepto asociado: [Búsqueda de Documentación Técnica y Utilidades de Propósito General](../conceptos/ra7-busqueda-documentacion-tecnica-utilidades-sistema.md).
- Estándar internacional prueba antivirus EICAR: [EICAR Anti-Malware Testfile](https://www.eicar.org/download-anti-malware-testfile/).
- Vídeo recomendado sobre productividad y herramientas FOSS: [Utilidades libres, ofimática y herramientas de propósito general (YouTube)](https://www.youtube.com/watch?v=GArVeJj8MHo).
