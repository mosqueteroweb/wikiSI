---
id: "raw-ra2-virtualizacion-planificacion-instalacion"
ra: ["RA2"]
ce: ["RA2.d", "RA2.e", "RA2.g"]
nivel_credibilidad: "Nivel 1"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "Oracle VirtualBox User Manual: Chapter 1 (First Steps), Chapter 5 (Virtual Storage), Chapter 8 (VBoxManage)"
  - "IBM & Red Hat Documentation: Hypervisors Type 1 vs Type 2"
  - "Canonical Ubuntu Installation Guide & Desktop Partitioning Docs"
  - "Microsoft Learn: Windows 10/11 Installation, UEFI/GPT Partition Layout, Get-FileHash"
---

# Fuente Procesada: Virtualización, Planificación de Instalación y Dual Boot

## 1. Tecnologías de Virtualización (`RA2.g`)

- **Hipervisor Tipo 1 (Nativo / *Bare-Metal*):** Se instala directamente sobre el hardware sin SO previo (VMware ESXi, Proxmox VE / KVM, Microsoft Hyper-V). Uso estándar en centros de datos y nube.
- **Hipervisor Tipo 2 (Alojado / *Hosted*):** Se ejecuta como aplicación sobre un sistema operativo anfitrión (**Oracle VirtualBox sobre MAX**, VMware Workstation, Parallels). Uso estándar en aulas, laboratorios DAM y pruebas locales.
- **Contenedores vs. VMs:** Las VMs virtualizan hardware completo e incluyen su propio kernel completo (mayor aislamiento entre Linux y Windows); los contenedores (Docker/Podman) comparten el kernel del host aislando espacios de usuario (`namespaces` y `cgroups`).
- **Almacenamiento y formatos virtuales:**
  - `VDI` (VirtualBox nativo), `VMDK` (VMware/portable), `VHD`/`VHDX` (Microsoft Hyper-V), `QCOW2` (QEMU/KVM).
  - **Tamaño dinámico (*Dynamically allocated*):** El archivo crece conforme se escriben datos reales hasta el máximo configurado (ideal en el aula para ahorrar SSD en MAX).
  - **Tamaño fijo (*Fixed size*):** Reserva todo el disco desde el inicio (menor fragmentación, mayor consumo inmediato).
- **Operaciones clave de laboratorio en VirtualBox:**
  - **Instantáneas (*Snapshots*):** Capturan el estado del disco y opcionalmente la memoria en un instante dado mediante discos diferenciales, permitiendo revertir cambios tras una práctica o fallo de configuración.
  - **Clonación completa vs. enlazada (*Linked Clone*):** La clonación completa duplica todo el disco base (independiente); la clonación enlazada crea un disco diferencial ligado a una instantánea base ahorrando gigabytes de almacenamiento.
  - **Exportación/Importación (`OVA` / `OVF`):** Estándar abierto para empaquetar descriptor XML + discos comprimidos y distribuir máquinas virtuales preconfiguradas entre puestos del aula.
- **CLI `VBoxManage`:** Permite crear, modificar RAM/EFI/red, tomar instantáneas y clonar máquinas mediante scripts reproducibles (`VBoxManage createvm`, `modifyvm`, `createmedium`, `snapshot`, `clonevm`).

## 2. Planificación e Instalación de Sistemas Operativos (`RA2.d`, `RA2.e`)

- **Fase previa de planificación:**
  1. Verificar compatibilidad hardware y presupuesto de RAM (en aula MAX 16 GB: tope **10–12 GB totales** para VMs).
  2. Comprobar edición y licencia (OEM/Retail/Volumen vs GPL/MIT).
  3. Descargar ISO desde fuente oficial y **verificar integridad criptográfica SHA-256** (`sha256sum archivo.iso` en Linux / `Get-FileHash archivo.iso -Algorithm SHA256` en PowerShell).
  4. Realizar copia de seguridad de datos previos si se trabaja sobre equipo físico o disco compartido.
  5. Diseñar el esquema de particiones (`GPT` + `ESP` en FAT32 para UEFI; `NTFS` para Windows; `ext4` `/` + `/home` opcional + `swap` para Linux).
- **Arranque Dual (*Dual Boot*) Windows 10/11 + Ubuntu en UEFI/GPT:**
  1. Instalar Windows primero (o reducir su partición `C:` desde *Administración de discos* para dejar espacio **No asignado**).
  2. Desactivar el **Inicio rápido** (*Fast Startup*) en Windows (`powercfg /h off` o Panel de Control) para evitar hibernación del sistema de archivos NTFS que impediría montarlo en Linux.
  3. Instalar Ubuntu usando el espacio libre sin formatear la partición `ESP` existente; el instalador añade `\EFI\ubuntu\shimx64.efi` / `grubx64.efi` junto a `\EFI\Microsoft\Boot\bootmgfw.efi`.
  4. Al reiniciar, **GRUB 2** gestiona la selección del sistema operativo.
