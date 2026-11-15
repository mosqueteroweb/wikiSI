---
title: "e06 · Verificación de ISOs, Licencias y Provisionamiento VM UEFI en VirtualBox"
ra: ["RA2"]
ce: ["RA2.a", "RA2.c", "RA2.d", "RA2.g"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra2-arquitectura-so-licencias.md"
  - "raw/procesados/ra2-virtualizacion-planificacion-instalacion.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e06 · Verificación de ISOs, Licencias y Provisionamiento VM UEFI en VirtualBox

<!-- fuente: raw/procesados/ra2-arquitectura-so-licencias.md -->
<!-- fuente: raw/procesados/ra2-virtualizacion-planificacion-instalacion.md -->

> **Criterios de Evaluación:** `RA2.a`, `RA2.c`, `RA2.d`, `RA2.g` · **Conceptos previos:** [Comparativa de Sistemas Operativos y Licencias](../conceptos/ra2-comparativa-so-licencias.md) · [Virtualización con VirtualBox en MAX](../conceptos/ra2-virtualizacion-virtualbox-max.md)

## Objetivo

Evaluar los requisitos de hardware y licenciamiento de distintos sistemas operativos, comprobar la integridad criptográfica (`SHA-256`) de las imágenes ISO antes de instalarlas y provisionar de forma reproducible una máquina virtual con firmware **UEFI**, **TPM 2.0 virtual** y disco **VDI dinámico** en **VirtualBox** sobre el anfitrión **MAX**.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Disco / Red |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(10 GB libres)* | Físicas | Red del aula |
| **`e06-Win11-Prep`** | Invitado 1 | Windows 11 (evaluación) | **4096 MB (4 GB)** | 2 | 50 GB VDI · NAT + Red Interna |
| **`e06-Mint-Lite`** | Invitado 2 | Linux Mint Xfce / Ubuntu | **2048 MB (2 GB)** | 2 | 25 GB VDI · NAT + Red Interna |

> **Consumo total de VMs activas:** **6 GB** simultáneos (si se arrancan a la vez) sobre 16 GB disponibles (deja 10 GB libres para MAX, muy por debajo del tope de 10–12 GB).

---

## Enunciado

1. **Comparativa previa (`RA2.c`, `RA2.d`):** Completa una ficha técnica justificando qué licencia (`EULA` privativa vs `GPLv2`/`MIT`) aplica a **Windows 11 Pro**, **Ubuntu 24.04 LTS**, **Linux Mint** y **Puppy Linux**, e indica cuál elegirías para rescatar un equipo de aula con 2 GB de RAM frente a una estación de desarrollo de 16 GB.
2. **Integridad de medios (`RA2.d`):** En una terminal de **MAX**, verifica mediante `sha256sum` la imagen ISO de Ubuntu/Mint descargada en `~/ISOs/` comparándola con el fichero `SHA256SUMS` oficial.
3. **Provisionamiento automático con `VBoxManage` (`RA2.g`):** Sin usar el asistente gráfico de creación paso a paso, crea desde terminal en MAX la VM **`e06-Win11-Prep`** configurada con:
   - Tipo `Windows11_64`, **4096 MB** de RAM, **2 vCPUs**, firmware **`efi`**, chip **`tpm-type 2.0`**, controlador SATA con disco dinámico de **50 GB**, unidad óptica DVD con la ISO y segundo adaptador en `intnet` (`RedAulaSI`).
4. **Identificación de elementos funcionales (`RA2.a`, `RA2.g`):** Arranca **`e06-Mint-Lite`** en modo Live o instalado y ejecuta un comando que demuestre el estado de comunicación entre el núcleo Linux, los dispositivos virtuales de VirtualBox (tarjeta de red `e1000` o `virtio`, disco SATA) y la asignación de memoria.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Matriz comparativa de licencias y idoneidad (`RA2.c`, `RA2.d`)

    | Sistema Operativo | Licencia predominante | Requisitos mínimos prácticos | Uso recomendado en nuestro escenario |
    | :--- | :--- | :--- | :--- |
    | **Windows 11 Pro** | Privativa (`EULA` comercial Microsoft) | 4 GB RAM, 64 GB disco, **UEFI + Secure Boot + TPM 2.0** | Estación cliente corporativa o pruebas .NET/Win32 (en VM con 4 GB) |
    | **Ubuntu 24.04 LTS** | Libre multipaquete (**Linux GPLv2** + MIT/Apache + firmwares) | 2–4 GB RAM, 25 GB disco | Estación de desarrollo principal y servidores (`Server`) con soporte 5 años |
    | **Linux Mint Xfce** | Libre (base Ubuntu/Debian GPLv2+) | 1–2 GB RAM, 20 GB disco | Escritorio ligero ágil en VMs de 2 GB o PCs modestos |
    | **Puppy Linux** | Libre (GPLv2+ / scripts propios) | **300 MB–512 MB RAM** (carga íntegra en RAM) | **Rescate del equipo antiguo de 2 GB de RAM** y live-CD de diagnóstico ultrarrápido |

    ### Paso 2: Verificación SHA-256 en el host MAX (`RA2.d`)

    ```bash
    cd ~/ISOs/

    # Opción A: calcular hash individual y cotejar visualmente con la web oficial
    sha256sum linuxmint-22-xfce-64bit.iso

    # Opción B (recomendada): verificación automatizada contra el manifiesto oficial SHA256SUMS
    sha256sum -c --ignore-missing sha256sum.txt
    ```

    **Resultado válido:**
    ```text
    linuxmint-22-xfce-64bit.iso: La suma coincide
    ```
    Si devolviera `FALLO`, la descarga estaría corrupta o manipulada y **debe descartarse antes de continuar**.

    ### Paso 3: Creación por línea de comandos con `VBoxManage` (`RA2.g`)

    ```bash
    # 1. Crear y registrar la VM compatible con Windows 11
    VBoxManage createvm --name "e06-Win11-Prep" --ostype "Windows11_64" --register

    # 2. Asignar RAM (4096 MB), CPU, firmware UEFI, TPM 2.0, controlador gráfico y audio
    VBoxManage modifyvm "e06-Win11-Prep" \
      --memory 4096 --cpus 2 --vram 128 \
      --graphicscontroller vboxsvga \
      --firmware efi --tpm-type 2.0 \
      --ioapic on --pae on --hwvirtex on --nestedpaging on

    # 3. Configurar red: Adaptador 1 NAT (Internet) + Adaptador 2 Red Interna (aislada)
    VBoxManage modifyvm "e06-Win11-Prep" \
      --nic1 nat --nictype1 82540EM \
      --nic2 intnet --intnet2 "RedAulaSI" --nictype2 82540EM

    # 4. Crear disco duro virtual VDI dinámico de 50 GB (51200 MB) y controlador SATA + DVD
    VBoxManage createmedium disk \
      --filename "$HOME/VirtualBox VMs/e06-Win11-Prep/e06-Win11-Prep.vdi" \
      --size 51200 --format VDI --variant Standard

    VBoxManage storagectl "e06-Win11-Prep" --name "SATA" --add sata --controller IntelAhci
    VBoxManage storageattach "e06-Win11-Prep" --storagectl "SATA" --port 0 --device 0 \
      --type hdd --medium "$HOME/VirtualBox VMs/e06-Win11-Prep/e06-Win11-Prep.vdi"

    # Adjuntar unidad óptica en el puerto 1 (sustituir ruta por tu ISO verificada)
    VBoxManage storageattach "e06-Win11-Prep" --storagectl "SATA" --port 1 --device 0 \
      --type dvddrive --medium emptydrive

    # 5. Comprobar el resumen final de la configuración generada
    VBoxManage showvminfo "e06-Win11-Prep" | grep -E "Memory size|Number of CPUs|Firmware|TPM|NIC 1|NIC 2|SATA"
    ```

    ### Paso 4: Verificación funcional del hardware virtual desde `e06-Mint-Lite` (`RA2.a`, `RA2.g`)

    Dentro de la máquina virtual Linux arrancada, ejecutamos:

    ```bash
    # Verificar kernel, módulos de virtualización, dispositivos PCI simulados y memoria libre
    uname -a
    lspci | grep -E "VGA|Ethernet|SATA"
    free -h
    lsblk
    ```

    Esto evidencia la interacción de los elementos funcionales (`RA2.a`): el kernel Linux interactúa mediante sus drivers (`e1000`, `ahci`, `vmwgfx`) con el hardware virtualizado que expone el hipervisor Tipo 2 VirtualBox sobre la capa física del equipo MAX.
