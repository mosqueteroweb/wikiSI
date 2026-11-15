---
title: "e10 · Recuperación ante Desastres: Snapshots, Timeshift, DISM/SFC y Acta Técnica"
ra: ["RA2"]
ce: ["RA2.f", "RA2.g", "RA2.i"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e10 · Recuperación ante Desastres: Snapshots, Timeshift, DISM/SFC y Acta Técnica

<!-- fuente: raw/procesados/ra2-arranque-aplicaciones-recuperacion-doc.md -->

> **Criterios de Evaluación:** `RA2.f`, `RA2.g`, `RA2.i` · **Concepto previo:** [Gestión de Aplicaciones, Actualización y Recuperación](../conceptos/ra2-gestion-aplicaciones-actualizacion-recuperacion.md)

## Objetivo

Aplicar tres mecanismos complementarios de recuperación del sistema operativo (**Snapshots de VirtualBox**, **Timeshift** en Linux Mint/Ubuntu y **`DISM` + `sfc /scannow`** en Windows 10) tras simular incidentes de configuración, redactando al final el **acta técnica de intervención (`RA2.i`)**.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e10-Mint`** | Invitado 1 | Linux Mint / Ubuntu | **2048 MB (2 GB)** | 2 | 25 GB VDI · NAT |
| **`e10-Win10`** | Invitado 2 | Windows 10 | **4096 MB (4 GB)** | 2 | 40 GB VDI · NAT |

> **Consumo total de VMs activas:** **6 GB** simultáneos sobre 16 GB disponibles (cumple el límite de 10–12 GB).

---

## Enunciado

1. **Snapshot de hipervisor (`RA2.g`, `RA2.f`):** Desde terminal del anfitrión **MAX**, crea mediante `VBoxManage` una instantánea (*snapshot*) en caliente o en frío llamada `Estado-Base-Limpio` sobre `e10-Mint` antes de realizar cambios destructivos.
2. **Recuperación interna con Timeshift (`RA2.f`):** Dentro de `e10-Mint`:
   - Instala `timeshift` y crea un punto de restauración `RSYNC` con `--create`.
   - Crea un archivo personal en `~/Documentos/apuntes_dam.txt`.
   - Simula un fallo administrativo grave modificando erróneamente `/etc/fstab` (añadiendo una línea inválida) o borrando `/etc/hosts`.
   - Restaura la instantánea de Timeshift y comprueba que **el fichero de `/etc` queda reparado mientras `~/Documentos/apuntes_dam.txt` se mantiene intacto**.
3. **Reparación de imagen en Windows 10 (`RA2.f`):** En `e10-Win10`, ejecuta en orden la verificación de salud del almacén de componentes con **`DISM`** y la reparación de archivos protegidos con **`sfc /scannow`**, interpretando su resultado.
4. **Documentación de la intervención (`RA2.i`):** Redacta la ficha técnica final con fecha, VMs implicadas, hashes/snapshots creados, comandos aplicados y resultado verificado.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Crear Snapshot base desde MAX con `VBoxManage` (`RA2.g`)

    ```bash
    # Crear instantánea de referencia con descripción técnica
    VBoxManage snapshot "e10-Mint" take "Estado-Base-Limpio" \
      --description "Sistema Linux Mint recién actualizado antes de pruebas con Timeshift"

    # Listar el árbol de instantáneas
    VBoxManage snapshot "e10-Mint" list
    ```

    ---

    ### Paso 2: Rescate selectivo del sistema con Timeshift en `e10-Mint` (`RA2.f`)

    ```bash
    # 1. Instalar Timeshift y verificar dispositivo raíz
    sudo apt update && sudo apt install -y timeshift
    lsblk -f

    # 2. Configurar Timeshift en modo RSYNC (o usar la GUI inicial para seleccionar /dev/sdaX)
    # Crear primera instantánea desde CLI:
    sudo timeshift --create --comments "Pre-cambio configuracion etc" --tags D

    # 3. Crear documento personal en /home que NO debe perderse al restaurar
    mkdir -p ~/Documentos
    echo "Apuntes importantes de DAM - No borrar" > ~/Documentos/apuntes_dam.txt

    # 4. Simular borrado accidental de archivo crítico /etc/hosts (o cambio erróneo)
    sudo mv /etc/hosts /etc/hosts.roto
    ls -l /etc/hosts     # Confirmar que /etc/hosts ha desaparecido

    # 5. Restaurar instantánea de Timeshift (selecciona el índice listado por --list)
    sudo timeshift --list
    sudo timeshift --restore
    # (El asistente te confirmará el dispositivo raíz; omite reinstalar GRUB si ya funciona)
    ```

    Tras reiniciar y volver a iniciar sesión en `e10-Mint`:
    ```bash
    ls -l /etc/hosts                  # Restaurado correctamente desde la instantánea
    cat ~/Documentos/apuntes_dam.txt  # ¡Intacto! Timeshift excluye /home por defecto
    ```

    *(Si alguna prueba hubiera dejado el sistema imposible de arrancar ni siquiera en modo recuperación, siempre queda la red de seguridad de Nivel 1 en el host MAX: `VBoxManage snapshot "e10-Mint" restore "Estado-Base-Limpio"`.)*

    ---

    ### Paso 3: Verificación e integridad de imagen en `e10-Win10` (`RA2.f`)

    Abre **PowerShell como Administrador** dentro de `e10-Win10` y ejecuta en este orden:

    ```powershell
    # 1. Comprobación rápida de marca de corrupción
    DISM /Online /Cleanup-Image /CheckHealth

    # 2. Escaneo profundo del almacén WinSxS (tarda varios minutos)
    DISM /Online /Cleanup-Image /ScanHealth

    # 3. Si detectó daños, reparar imagen descargando componentes limpios de Windows Update
    DISM /Online /Cleanup-Image /RestoreHealth

    # 4. Por último, comprobar y reparar archivos protegidos del sistema en C:\Windows
    sfc /scannow
    ```

    **Interpretación de salidas esperadas:**
    - `No component store corruption detected.` (DISM sano).
    - `La operación de restauración se completó correctamente.` (DISM reparó el almacén).
    - `Protección de recursos de Windows no encontró ninguna infracción de integridad.` (SFC limpio).

    ---

    ### Paso 4: Plantilla cumplimentada de Acta Técnica (`RA2.i`)

    ```markdown
    # Acta de Mantenimiento y Recuperación — Laboratorio RA2
    - **Técnico:** AlumDAM-XX · **Fecha:** 2026-11-15
    - **Anfitrión:** Aula-MAX (16 GB RAM, VirtualBox)
    - **Presupuesto RAM usado:** e10-Mint (2 GB) + e10-Win10 (4 GB) = 6 GB activos.

    ## Intervenciones realizadas
    1. **Snapshot previo en hipervisor (`e10-Mint`):** Creado `Estado-Base-Limpio` mediante `VBoxManage snapshot`.
    2. **Simulación y rescate en Linux (`e10-Mint`):**
       - Incidente: Eliminación/renombrado de `/etc/hosts`.
       - Solución: Restauración RSYNC mediante `timeshift --restore`.
       - Verificación: `/etc/hosts` restaurado y `~/Documentos/apuntes_dam.txt` conservado sin pérdida de datos.
    3. **Integridad de sistema Windows (`e10-Win10`):**
       - Ejecución secuencial de `DISM /RestoreHealth` seguido de `sfc /scannow`.
       - Estado final: Sin infracciones de integridad.
    ```
