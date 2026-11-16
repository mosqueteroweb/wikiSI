---
id: "raw-ra1-memorias-arranque-perifericos"
ra: ["RA1"]
ce: ["RA1.b", "RA1.c", "RA1.d"]
nivel_credibilidad: "Nivel 1"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "JEDEC Standards: DDR4 (JESD79-4) y DDR5 (JESD79-5)"
  - "UEFI Forum: Unified Extensible Firmware Interface Specification 2.10"
  - "Arch Wiki & Linux Kernel Docs: Boot process, systemd-boot/GRUB2, efibootmgr, lspci, lsusb, udev"
  - "IBM Documentation & Red Hat Enterprise Linux Memory Management"
  - "Microsoft Learn: UEFI/GPT vs BIOS/MBR, bcdedit, Secure Boot, DevMgmt, pnputil"
  - "PCI-SIG (PCI Express) & USB-IF (USB 3.2 / USB4) & NVM Express (NVMe)"
  - "Oracle VirtualBox User Manual: EFI firmware, USB Passthrough, Shared Folders, Guest Additions"
---

# Fuente Procesada: Jerarquía de Memorias, Arranque (BIOS/UEFI) y Periféricos/Buses

## 1. Jerarquía de Memorias y Tipos

- **Principios de localidad:**
  - *Localidad temporal:* Un dato o instrucción accedido recientemente tiende a volver a usarse pronto.
  - *Localidad espacial:* Si se accede a una dirección de memoria, es probable acceder a direcciones contiguas.
- **Niveles volátiles (pierden el contenido sin alimentación eléctrica):**
  1. **Registros internos de la CPU:** Latencia < 1 ns (1 ciclo), capacidad de cientos de bytes a pocos KiB.
  2. **Memoria Caché SRAM (*Static RAM*):** Basada en biestables de 6 transistores; no requiere refresco.
     - `L1` (dividida en `L1i` instrucciones y `L1d` datos): ~32–64 KiB por núcleo, latencia ~1 ns.
     - `L2`: ~256 KiB – 2 MiB por núcleo, latencia ~3–10 ns.
     - `L3`: compartida entre núcleos (~8–96 MiB), latencia ~15–30 ns.
     - Conceptos: *cache hit* (acierto), *cache miss* (fallo) y coherencia de caché.
  3. **Memoria Principal DRAM (*Dynamic RAM*):** Basada en condensador + transistor; necesita ciclos periódicos de refresco.
     - Estándares actuales: DDR4 (2133–3200 MT/s nominales, 1.2 V) y DDR5 (4800–6400+ MT/s, 1.1 V, doble subcanal independiente por módulo).
     - Formatos físicos: **DIMM** (sobremesa, 288 pines DDR4/DDR5) y **SO-DIMM** (portátiles y mini-PCs, 260 pines DDR4 / 262 pines DDR5).
     - Canales: *Single Channel* (64 bits) vs *Dual Channel* (128 bits, duplica el ancho de banda teórico). Fórmula aproximada de ancho de banda: MT/s × 8 bytes × n.º canales.
     - **ECC (*Error-Correcting Code*):** Detecta y corrige errores de 1 bit en memoria (servidores y estaciones críticas).
- **Memorias no volátiles (conservan datos sin corriente):**
  - **ROM / PROM / EPROM / EEPROM:** Evolución histórica de solo lectura / grabable una vez / borrable por UV / borrable eléctricamente.
  - **Memoria Flash (NOR y NAND):**
    - *NOR Flash:* Acceso aleatorio rápido a nivel de byte/palabra, usada en chips SPI de placa base para almacenar el firmware **BIOS/UEFI**.
    - *NAND Flash:* Alta densidad por bloques (SLC, MLC, TLC, QLC), usada en unidades **SSD**, **NVMe**, tarjetas SD y memorias USB.
- **Memoria virtual y paginación:**
  - Extensión de la RAM mediante disco para aislar espacios de direcciones y aliviar presión de memoria.
  - **MAX / Ubuntu:** Partición `swap` o archivo `/swapfile` (`swapon --show`, `free -h`, `vmstat`).
  - **Windows 10/11:** Archivo oculto `C:\pagefile.sys`.
  - **Regla de aula:** Los PCs disponen de **16 GB de RAM física**; el total asignado a VMs activas en VirtualBox no debe exceder **10–12 GB** para evitar intercambio masivo (*thrashing*) en el host MAX.

## 2. Puesta en Marcha: Fuente, POST, BIOS Legacy y UEFI

1. **Encendido y *Power Good*:** La fuente ATX suministra +12 V, +5 V, +3,3 V y +5 VSB (*standby*). Cuando las tensiones son estables, envía la señal *Power Good* para liberar el *reset* de la CPU.
2. **POST (*Power-On Self-Test*):** El firmware (alojado en chip Flash SPI) verifica CPU, controlador de memoria, RAM, GPU y bus PCIe/teclado. Los fallos críticos se reportan mediante códigos de pitidos (*beep codes*) o LEDs de diagnóstico (`CPU`, `DRAM`, `VGA`, `BOOT`).
3. **Configuración CMOS/NVRAM:** La pila de litio **CR2032 (3V)** mantiene el reloj RTC y la configuración básica en CMOS en placas antiguas, o la configuración en NVRAM.
4. **Comparativa BIOS Legacy vs UEFI:**
   - **BIOS Legacy:** Modo real de 16 bits, direccionamiento limitado a 1 MiB inicial, interfaz textual, particionado **MBR** (máx. 4 particiones primarias, discos ≤ 2 TiB), sin verificación criptográfica de arranque.
   - **UEFI:** Ejecución en 32/64 bits, soporte de ratón/red, tabla de particiones **GPT** (hasta 128 particiones estándar en Windows y discos > 2 TiB), requiere partición del sistema EFI (**ESP** en FAT32, punto de montaje `/boot/efi` en Linux), soporta **Secure Boot** (verificación de firmas digitales del cargador) y se integra con **TPM 2.0** (requisito oficial de Windows 11).
5. **Cadena de arranque del Sistema Operativo:**
   - **MAX / Ubuntu (UEFI):** `Firmware UEFI` → `/EFI/ubuntu/shimx64.efi` (firmado para Secure Boot) → `grubx64.efi` (**GRUB2**) → carga `vmlinuz` (kernel) + `initramfs` → `systemd` (PID 1).
   - **Windows 10/11 (UEFI):** `Firmware UEFI` → `\EFI\Microsoft\Boot\bootmgfw.efi` (*Windows Boot Manager*) lee el almacén **BCD** → `winload.efi` → `ntoskrnl.exe` → `smss.exe` / `wininit.exe`.

## 3. Periféricos, Buses e Interfaces de E/S

- **Clasificación:** Entrada (teclado, ratón, escáner, micrófono), Salida (monitor, impresora, altavoces), Entrada/Salida (almacenamiento masivo, pantallas táctiles, adaptadores de red).
- **Buses internos y almacenamiento:**
  - **PCI Express (PCIe):** Conexión serie punto a punto por carriles (*lanes*) full-duplex: `x1`, `x4`, `x8`, `x16`.
    - PCIe 3.0: ~1 GB/s por carril (~16 GB/s en x16).
    - PCIe 4.0: ~2 GB/s por carril (~32 GB/s en x16; típico M.2 x4 hasta ~7–8 GB/s).
    - PCIe 5.0: ~4 GB/s por carril (~64 GB/s en x16).
  - **SATA III:** 6 Gbps (~600 MB/s reales tras codificación 8b/10b), protocolo **AHCI** (cola de 32 comandos). Usado en HDDs 3.5"/2.5" y SSDs SATA 2.5".
  - **M.2 NVMe:** Conector compacto M.2 (clave `M`) transportando protocolo **NVMe** directamente sobre carriles PCIe (hasta 64.000 colas con 64.000 comandos por cola).
- **Interfaces externas y vídeo:**
  - **USB:** Arquitectura maestro-esclavo (*Host Controller*: xHCI). Versiones: USB 2.0 (480 Mbps), USB 3.2 Gen 1 (5 Gbps), USB 3.2 Gen 2 (10 Gbps), USB 3.2 Gen 2x2 (20 Gbps), USB4 / Thunderbolt 4 (40 Gbps, tunelización PCIe + DisplayPort, conector **USB-C** reversible con USB Power Delivery).
  - **Vídeo:** DisplayPort (1.4 / 2.1, soporta *daisy-chaining* MST) y HDMI (2.0 / 2.1, audio+vídeo).
- **Controladores y VirtualBox:**
  - En Linux, el kernel incluye la mayoría de módulos de drivers y `udev` crea nodos en `/dev/`; impresoras gestionadas con **CUPS**. Herramientas: `lspci -nnk`, `lsusb -tv`, `lsblk`, `dmesg`.
  - En Windows: `devmgmt.msc` (Administrador de dispositivos) y `pnputil`.
  - En VirtualBox: filtros de dispositivo USB en configuración de la VM y **Guest Additions** para gráficos, portapapeles y carpetas compartidas.
