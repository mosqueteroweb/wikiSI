---
title: "Arquitectura de Von Neumann, Placa Base y CPU"
ra: ["RA1"]
ce: ["RA1.a"]
tipo: "concepto"
publicar: true
fuentes:
  - "raw/procesados/ra1-hardware-cpu-placas.md"
ultima_revision: "2026-11-15"
---

# Arquitectura de Von Neumann, Placa Base y CPU

> **Criterio de Evaluación cubierto:** `RA1.a` — *Se han reconocido los componentes físicos de un sistema informático y sus mecanismos de interconexión.*

---

## 1. Arquitectura de Von Neumann y Harvard Modificada

<!-- fuente: raw/procesados/ra1-hardware-cpu-placas.md -->

El modelo propuesto por **John von Neumann (1945)** establece la base de los ordenadores de propósito general actuales: tanto las **instrucciones del programa** como los **datos** que manipula residen en una misma **memoria principal** direccionable, sin necesidad de recablear la máquina para cambiar de tarea.

![Arquitectura de Von Neumann y formatos de placa base](../assets/ra1-arquitectura-von-neumann.svg)

Sus cuatro bloques funcionales y sus mecanismos de interconexión son:

1. **Unidad Central de Proceso (CPU):** Interpreta y ejecuta las instrucciones.
2. **Memoria Principal (RAM):** Almacena temporalmente programas activos y datos.
3. **Subsistema de Entrada/Salida (E/S):** Conecta periféricos, almacenamiento secundario y redes.
4. **Buses del sistema:**
   - **Bus de Datos (bidireccional):** Transporta los bits de datos o instrucciones (64 bits por transferencia en CPUs modernas).
   - **Bus de Direcciones (unidireccional CPU → RAM/E/S):** Indica la posición exacta de memoria a leer o escribir. Su anchura $n$ determina el espacio teórico direccionable ($2^n$ posiciones).
   - **Bus de Control:** Transmite señales de sincronización y estado (`RD`, `WR`, reloj `CLK`, interrupciones `IRQ` y concesión de bus para `DMA`).

!!! warning "El cuello de botella de Von Neumann y la solución Harvard modificada"
    Como instrucciones y datos comparten un único bus principal hacia la RAM, la CPU pasa ciclos esperando transferencias. Para mitigarlo, los procesadores actuales aplican externamente el modelo **Von Neumann**, pero internamente usan una **arquitectura Harvard modificada** separando la caché de primer nivel en **L1i** (instrucciones) y **L1d** (datos), permitiendo leer código y operandos en paralelo.

---

## 2. La Placa Base (*Motherboard*) y sus Mecanismos de Interconexión

<!-- fuente: raw/procesados/ra1-hardware-cpu-placas.md -->

La placa base es el circuito impreso multicapa (PCB) que interconecta físicamente la CPU, la memoria, el almacenamiento y los buses de expansión.

### Formatos habituales

| Formato | Dimensiones | Ranuras PCIe típicas | Uso habitual |
| :--- | :---: | :---: | :--- |
| **ATX** | $305 \times 244\text{ mm}$ | Hasta 7 | Estaciones de trabajo, servidores torre, gaming |
| **Micro-ATX ($\mu$ATX)** | $244 \times 244\text{ mm}$ | Hasta 4 | Equipos de oficina y PCs de aula |
| **Mini-ITX** | $170 \times 170\text{ mm}$ | 1 (x16) | Mini-PCs, equipos compactos, laboratorios silenciosos |

### Componentes esenciales en la placa

- **Zócalo (*Socket*) de CPU:**
  - **LGA (*Land Grid Array*):** Pines en el zócalo de la placa y contactos planos en el procesador (Intel LGA 1700/1851, AMD AM5).
  - **PGA (*Pin Grid Array*):** Pines en la base de la CPU (AMD AM4).
  - **BGA (*Ball Grid Array*):** Procesador soldado directamente a la placa (portátiles y mini-PCs).
- **Chipset / PCH (*Platform Controller Hub*):** Circuito integrado que gestiona las comunicaciones secundarias (SATA, USB, audio, LAN, PCIe del chipset), conectado a la CPU mediante un enlace de alta velocidad (**DMI** o PCIe interno).
- **VRM (*Voltage Regulator Module*):** Conjunto de bobinas, condensadores y MOSFETs que transforman los $+12\text{ V}$ de la fuente en el voltaje preciso del procesador ($V_{\text{core}} \approx 0.8\text{–}1.4\text{ V}$).
- **Alimentación:** Conector principal **ATX de 24 pines** y conector auxiliar **EPS12V de 4 u 8 pines** dedicado a la CPU.

---

## 3. Estructura Interna del Procesador y Ciclo de Instrucción

<!-- fuente: raw/procesados/ra1-hardware-cpu-placas.md -->

### Bloques y registros internos de la CPU

- **Unidad de Control (UC):** Lee la instrucción de memoria, la decodifica y emite señales de control al resto del sistema siguiendo los pulsos del reloj.
- **ALU (*Arithmetic Logic Unit*) y FPU:** Ejecutan sumas/restas enteras, operaciones lógicas (`AND`, `OR`, `XOR`, desplazamientos) y cálculo en coma flotante / instrucciones vectoriales SIMD (`AVX2`, `NEON`).
- **Banco de registros (memoria ultrarrápida interna):**
  - **`PC` / `RIP` (*Program Counter* / *Instruction Pointer*):** Apunta a la dirección de memoria de la siguiente instrucción.
  - **`IR` (*Instruction Register*):** Almacena la instrucción actualmente en decodificación.
  - **`MAR` y `MDR`:** Conectan el procesador con los buses de direcciones y datos respectivamente.
  - **Registros de propósito general y `Flags`:** Almacenan operandos intermedios (`RAX`, `RBX`...) y banderas de resultado (cero `ZF`, acarreo `CF`, desbordamiento `OF`, interrupciones `IF`).

### Ciclo de instrucción (*Fetch–Decode–Execute*)

```mermaid
flowchart LR
    F["1. Fetch (Captación)\nPC → MAR → Leer RAM → IR\nPC = PC + longitud"] --> D["2. Decode (Decodificación)\nUC interpreta opcode\ny localiza operandos"]
    D --> E["3. Execute (Ejecución)\nALU/FPU opera o accede a E/S\nActualiza registros y Flags"]
    E --> I{"¿Interrupción\npendiente?"}
    I -- "No" --> F
    I -- "Sí" --> ISR["Guardar contexto PC/Flags\nEjecutar rutina ISR"] --> F
```

### Interrupciones y Acceso Directo a Memoria (DMA)

- **Interrupciones hardware (`IRQ` / `NMI`):** Permiten que un periférico (teclado, tarjeta de red, disco) avise a la CPU cuando tiene datos listos, evitando malgastar ciclos en espera activa (*polling*).
- **DMA (*Direct Memory Access*):** Controlador especializado que transfiere grandes bloques de datos directamente entre un dispositivo (NVMe, GPU, red) y la RAM sin que la CPU copie palabra a palabra.

### Conjuntos de instrucciones (ISA) y paralelismo

| Característica | Arquitectura CISC (`x86-64`) | Arquitectura RISC (`ARM64` / `RISC-V`) |
| :--- | :--- | :--- |
| **Longitud de instrucción** | Variable (1 a 15 bytes) | Fija (generalmente 32 bits) |
| **Acceso a memoria** | Algunas instrucciones operan directo sobre memoria | Modelo *load-store* (solo carga/almacén accede a RAM) |
| **Eficiencia y uso** | Alto rendimiento en PCs, servidores y aula MAX | Máxima eficiencia energética (móviles, portátiles ARM, IoT) |

- **Multinúcleo vs. SMT (*Hyper-Threading*):** Un procesador de 6 núcleos físicos puede exponer 12 hilos lógicos mediante *Simultaneous Multithreading*, duplicando los registros de contexto por núcleo para aprovechar unidades de ejecución ociosas.

---

## 4. Inspección Práctica en el Aula (MAX y VirtualBox)

<!-- fuente: raw/procesados/ra1-hardware-cpu-placas.md -->

En nuestro entorno de aula (**host MAX** + **VirtualBox**), podemos inspeccionar el hardware real y la virtualización asistida por hardware (`VT-x` / `AMD-V`) sin abrir el equipo:

=== "MAX / Ubuntu (Linux)"

    ```bash
    # Resumen completo de CPU, núcleos, cachés y soporte de virtualización
    lscpu

    # Fabricante, modelo y versión de la placa base (requiere privilegios)
    sudo dmidecode -t baseboard

    # Árbol hardware de procesador y placa
    sudo lshw -C cpu -C bus
    ```

    > **En VirtualBox sobre MAX:** Comprueba en `lscpu` que aparece `Virtualization: VT-x` (Intel) o `AMD-V` (AMD). Para las VMs del aula (equipos de 16 GB), asigna normalmente **2 vCPUs** sin superar los núcleos físicos reales del equipo anfitrión.

=== "Windows 10 / 11"

    ```powershell
    # Información de procesador y virtualización desde PowerShell
    Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed, VirtualizationFirmwareEnabled

    # Modelo de placa base y fabricante
    Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, Version

    # Herramienta gráfica integrada de información del sistema
    msinfo32
    ```

    > **En una VM Windows de VirtualBox:** Verás el modelo del procesador físico heredado del host MAX, mientras que `Win32_BaseBoard` reportará placa base virtual `Oracle Corporation VirtualBox`.

---

## Recursos para profundizar

- **Documentación oficial y referencia técnica:**
  - [Página de manual oficial de `lscpu(1)` (man7.org)](https://man7.org/linux/man-pages/man1/lscpu.1.html)
  - [Microsoft Learn: Clase CIM `Win32_Processor`](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-processor)
  - [Arquitectura de Von Neumann (Wikipedia en español)](https://es.wikipedia.org/wiki/Arquitectura_de_Von_Neumann)
- **Vídeos explicativos recomendados (YouTube):**
  - [Arquitectura de Von Neumann y funcionamiento del computador](https://www.youtube.com/watch?v=oEhTtQI9RN8)
  - [Cuello de botella de Von Neumann y arquitectura Harvard](https://www.youtube.com/watch?v=oH7vNuKyCPA)
- **Práctica relacionada en `wikiSI`:** [Ejercicio e01 · Auditoría de hardware, CPU y placa base](../ejercicios/e01-ra1-auditoria-hardware-cpu-placas.md)
