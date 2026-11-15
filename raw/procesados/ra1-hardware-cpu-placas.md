---
id: "raw-ra1-hardware-cpu-placas"
ra: ["RA1"]
ce: ["RA1.a"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "Linux man-pages: lscpu(1), lshw(1), dmidecode(8), proc(5) (/proc/cpuinfo)"
  - "Microsoft Learn: Win32_Processor, Win32_BaseBoard, msinfo32"
  - "Intel ATX Specification & Form Factors (ATX, Micro-ATX, Mini-ITX)"
  - "Oracle VirtualBox User Manual: Hardware Virtualization (VT-x / AMD-V)"
  - "Wikipedia / Arquitectura de Von Neumann (Nivel 2 referencia académica)"
---

# Fuente Procesada: Arquitectura Von Neumann, Placas Base y CPU

## 1. Modelo Funcional de Von Neumann y Harvard Modificada

- **Arquitectura de Von Neumann (1945):** Almacena tanto instrucciones como datos en una única memoria principal direccionable. Se compone de:
  1. **Unidad Central de Proceso (CPU):** Unidad de Control (UC) + Unidad Aritmético-Lógica (ALU) + Banco de Registros.
  2. **Memoria Principal (RAM):** Direccionamiento lineal de palabras para instrucciones y datos.
  3. **Subsistema de Entrada/Salida (E/S):** Controladores y puertos de comunicación con el exterior.
  4. **Buses del sistema:**
     - **Bus de Datos:** Bidireccional; transporta palabras de datos o instrucciones (ancho típico 64 bits en arquitecturas modernas).
     - **Bus de Direcciones:** Unidireccional desde CPU/DMA hacia memoria o E/S; determina el espacio máximo direccionable ($2^n$ direcciones).
     - **Bus de Control:** Señales de lectura (`RD`), escritura (`WR`), reloj (`CLK`), interrupciones (`IRQ`, `NMI`), arbitraje de bus (`HOLD`/`HLDA`).
- **Cuello de botella de Von Neumann:** La compartición de un único bus para instrucciones y datos limita el rendimiento efectivo de la CPU.
- **Arquitectura Harvard modificada en procesadores modernos:** Mantiene memoria principal unificada (modelo Von Neumann externo), pero divide la caché de primer nivel (`L1i` para instrucciones y `L1d` para datos) para permitir captación y carga simultáneas sin conflictos de bus.

## 2. Placa Base (*Motherboard / BaseBoard*)

- **Formatos estandarizados (Intel / VIA):**
  - **ATX (*Advanced Technology Extended*):** $305 \times 244\text{ mm}$. Hasta 7 ranuras de expansión PCIe, 4 ranuras DIMM habituales, máxima capacidad de refrigeración y fases VRM.
  - **Micro-ATX ($\mu$ATX):** $244 \times 244\text{ mm}$. Hasta 4 ranuras de expansión, 2–4 ranuras DIMM; muy común en equipos de oficina y aulas escolares.
  - **Mini-ITX:** $170 \times 170\text{ mm}$. 1 ranura PCIe x16, 2 ranuras DIMM/SO-DIMM; ideal para mini-PCs y estaciones compactas.
- **Elementos clave de interconexión:**
  - **Zócalo (*Socket*) de CPU:** LGA (*Land Grid Array*, pines en el zócalo, ej. Intel LGA 1700/1851 y AMD AM5), PGA (*Pin Grid Array*, pines en la CPU, ej. AMD AM4) y BGA (*Ball Grid Array*, soldado en placa en portátiles/mini-PCs).
  - **Chipset / PCH (*Platform Controller Hub*):** Gestiona los enlaces secundarios (USB, SATA, audio, LAN, ranuras PCIe de menor ancho de banda), conectado a la CPU por un enlace DMI (*Direct Media Interface*) o equivalente PCIe interno, mientras la CPU controla directamente la memoria RAM y las líneas PCIe principales (GPU + primer M.2 NVMe).
  - **VRM (*Voltage Regulator Module*):** Regula los $+12\text{ V}$ de la fuente hacia el voltaje preciso del núcleo ($V_{\text{core}} \approx 0.8\text{–}1.4\text{ V}$).
  - **Conectores de alimentación:** Conector principal ATX de 24 pines y conector auxiliar EPS12V de 4 u 8 pines para la CPU.

## 3. Estructura Interna del Procesador y Ciclo de Instrucción

- **Componentes internos:**
  - **Unidad de Control (UC):** Decodifica la instrucción, genera señales de temporización y coordina el flujo entre registros, ALU y buses.
  - **Unidad Aritmético-Lógica (ALU) y FPU:** Ejecutan operaciones aritméticas enteras, lógicas (`AND`, `OR`, `XOR`, desplazamientos) y en coma flotante (`FPU` / unidades vectoriales SIMD como AVX2/AVX-512 o NEON).
  - **Registros principales:**
    - `PC` / `RIP` (*Program Counter* / *Instruction Pointer*): Dirección de la siguiente instrucción.
    - `IR` (*Instruction Register*): Instrucción actual en decodificación.
    - `MAR` (*Memory Address Register*) y `MDR` (*Memory Data Register*): Interfaz con los buses de direcciones y datos.
    - `Acumulador` y registros de propósito general (`RAX`, `RBX`, etc. en x86-64).
    - `Flags` / `RFLAGS` (Registro de estado): Banderas de acarreo (`CF`), cero (`ZF`), signo (`SF`), desbordamiento (`OF`) y habilitación de interrupciones (`IF`).
- **Ciclo de instrucción (*Fetch-Decode-Execute*):**
  1. **Fetch (Captación):** Se copia `PC` en `MAR`, se lee memoria en `MDR`, se carga `IR` y se incrementa `PC`.
  2. **Decode (Decodificación):** La UC interpreta el código de operación (*opcode*) y prepara los operandos.
  3. **Execute (Ejecución):** La ALU/FPU opera o realiza transferencia a memoria/E/S y actualiza `Flags`.
- **Interrupciones y DMA:**
  - **Interrupciones hardware (`IRQ` / `NMI`):** Permiten a los dispositivos avisar a la CPU de eventos asíncronos sin espera activa (*polling*).
  - **Interrupciones software / excepciones:** Llamadas al sistema (`syscall`) o errores (división por cero, fallo de página).
  - **DMA (*Direct Memory Access*):** Permite a controladores (disco, red) transferir bloques directamente con la RAM liberando a la CPU de copiar byte a byte.
- **Paralelismo e ISA:**
  - **CISC (`x86-64`):** Instrucciones de longitud variable, alta densidad de código (PCs de escritorio, servidores, VirtualBox en aula MAX).
  - **RISC (`ARM64` / `RISC-V`):** Instrucciones de longitud fija, arquitectura carga-almacenamiento (*load-store*), alta eficiencia energética.
  - **Multinúcleo y SMT/Hyper-Threading:** Múltiples núcleos físicos en un encapsulado y duplicación de contexto lógico (hilos por núcleo) para aprovechar etapas ociosas del *pipeline*.

## 4. Comandos de Verificación en Nivel 1 (Aula)

- **Linux / MAX (`util-linux`, `dmidecode`, `lshw`):**
  - `lscpu`: Arquitectura, modelo, núcleos físicos, hilos por núcleo, virtualización (`VT-x` / `AMD-V`), cachés L1d/L1i/L2/L3.
  - `sudo dmidecode -t baseboard`: Fabricante, modelo y versión de la placa base.
  - `cat /proc/cpuinfo`: Flags de instrucciones y frecuencia por procesador lógico.
- **Windows 10/11 (PowerShell / CIM):**
  - `Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed, VirtualizationFirmwareEnabled`
  - `Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, Version`
  - `msinfo32`: Resumen gráfico de sistema, placa y procesador.
