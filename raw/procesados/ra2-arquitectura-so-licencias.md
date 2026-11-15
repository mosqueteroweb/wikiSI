---
id: "raw-ra2-arquitectura-so-licencias"
ra: ["RA2"]
ce: ["RA2.a", "RA2.b", "RA2.c"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "Linux Kernel Documentation & man-pages: uname(1), syscalls(2), lsmod(8), strace(1)"
  - "Microsoft Learn: Windows NT Architecture, Kernel-Mode and User-Mode, SoftwareLicensingProduct"
  - "GNU Project (gnu.org): Categorías de software libre y no libre, GPLv3, LGPL"
  - "Open Source Initiative (opensource.org): Licencias MIT, Apache 2.0, BSD"
  - "Documentación oficial de MAX (EducaMadrid), Canonical Ubuntu, Linux Mint, Puppy Linux y Microsoft Windows 10/11"
---

# Fuente Procesada: Arquitectura del Sistema Operativo, Funciones y Licencias

## 1. Elementos Funcionales de un Sistema Informático (`RA2.a`)

Un sistema informático completo se estructura en cuatro capas funcionales interdependientes:
1. **Hardware:** CPU, memoria RAM, almacenamiento, buses y periféricos.
2. **Sistema Operativo (SO):** Capa software privilegiada que abstrae el hardware, arbitra recursos y ofrece una interfaz uniforme (`API`/`POSIX`/Win32) al resto de programas.
3. **Aplicaciones:** Software de propósito general o específico (IDEs, compiladores, bases de datos, ofimática) ejecutado sobre el SO.
4. **Usuarios / Operadores:** Personas o servicios externos que interactúan con el sistema mediante interfaz gráfica (GUI) o línea de comandos (CLI).

## 2. Evolución, Clasificación y Arquitectura del SO (`RA2.b`)

- **Evolución histórica:** Sistemas por lotes (*batch*), multiprogramación, sistemas de tiempo compartido (*time-sharing* con planificación por turnos), sistemas de escritorio/red, tiempo real (**RTOS**, plazos deterministas) y entornos virtualizados/nube.
- **Clasificación:**
  - *Por usuarios:* Monousuario vs. Multiusuario (aislamiento de sesiones y permisos).
  - *Por tareas:* Monotarea vs. Multitarea (apropiativa/*preemptive* mediante interrupciones de reloj vs. cooperativa).
  - *Por propósito:* Escritorio, Servidor, Móvil, Embebido / Tiempo Real.
- **Funciones esenciales del SO:**
  1. Gestión de procesos e hilos (planificador de CPU, cambio de contexto, estados: Nuevo, Listo, Ejecutando, Bloqueado, Terminado).
  2. Gestión de memoria principal y virtual (paginación, tablas de páginas, aislamiento de direcciones).
  3. Gestión del almacenamiento y sistemas de archivos (`ext4`, `NTFS`, `Btrfs`, `VFAT`).
  4. Gestión de Entrada/Salida y controladores (*drivers*).
  5. Red, seguridad, cuentas y auditoría.
- **Anillos de protección de CPU (x86-64):**
  - **Ring 0 (Modo Kernel):** Privilegio total sobre registros de control, tablas de páginas e instrucciones hardware.
  - **Ring 3 (Espacio de Usuario):** Ejecución restringida de aplicaciones; para leer discos, abrir sockets o crear procesos debe invocar una **llamada al sistema (*syscall*)** controlada.
- **Arquitecturas de núcleo (*Kernel*):**
  - **Monolítico Modular (Linux):** Todos los subsistemas principales (planificador, memoria, VFS, red, drivers) se ejecutan en Ring 0 en un mismo espacio de direcciones, logrando máxima velocidad con carga dinámica de módulos (`.ko` mediante `lsmod`/`modprobe`).
  - **Microkernel (MINIX, QNX, seL4):** Ring 0 queda reducido al mínimo (IPC, hilos básicos, interrupciones); drivers y sistemas de archivos corren como servidores en Ring 3, aumentando el aislamiento y tolerancia a fallos a costa de mayor sobrecarga IPC.
  - **Kernel Híbrido (Windows NT / macOS XNU):** Combina estructura modular inspirada en microkernel (HAL, Executive, subsistemas) manteniendo los servicios críticos y drivers dentro de espacio kernel para conservar alto rendimiento.

## 3. Licencias de Software y Comparativa de SO (`RA2.c`)

- **Software Libre (4 libertades FSF):** Usar con cualquier propósito (0), estudiar y modificar el código fuente (1), redistribuir copias (2) y distribuir versiones modificadas (3).
  - **Copyleft fuerte (`GPLv3`):** Toda obra derivada distribuida hereda obligatoriamente la licencia GPL y debe entregar su código fuente (usada en el kernel Linux y herramientas GNU).
  - **Copyleft débil (`LGPL`):** Permite enlazar librerías con software propietario manteniendo libre la librería modificada.
- **Código Abierto Permisivo (`MIT`, `BSD`, `Apache 2.0`):** Permiten usar, modificar e integrar el código en productos comerciales cerrados conservando el aviso de autoría original (Apache 2.0 añade cláusula explícita de patentes).
- **Modelos no libres / propietarios:**
  - *Freeware:* Gratuito en uso, código cerrado y prohibida su modificación.
  - *Shareware / Trial:* Evaluación limitada por tiempo o funciones.
  - *Propietario comercial (**EULA**):*
    - **OEM:** Ligada a la placa base del equipo donde se instala por primera vez (no transferible).
    - **Retail (FPP):** Transferible de un equipo a otro desactivando la instalación previa.
    - **Licenciamiento por Volumen (KMS / MAK):** Activación centralizada para centros educativos y empresas.

### Requisitos de aula (VirtualBox sobre Host MAX 16 GB)

| Sistema Operativo | Tipo / Licencia | CPU mínima | RAM recomendada en aula | Disco virtual recomendado | Firmware / Notas |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **MAX (Host)** | Linux (Debian/Ubuntu) · Libre GPL | x86-64 (VT-x/AMD-V) | *(4–6 GB libres reservados)* | SSD local | Host oficial del aula |
| **Ubuntu Desktop** | Linux · Libre (GPL/MIT/etc.) | x86-64 2 GHz dual core | **2048–4096 MB (2–4 GB)** | 25 GB VDI | BIOS o UEFI |
| **Ubuntu Server** | Linux · Libre | x86-64 1 GHz | **1024–2048 MB (1–2 GB)** | 15–20 GB VDI | Sin GUI, consumo mínimo |
| **Linux Mint** | Linux · Libre | x86-64 dual core | **2048 MB (2 GB)** | 20–25 GB VDI | Muy ligero con Xfce/MATE |
| **Puppy Linux** | Linux · Libre | x86 / x86-64 | **512–1024 MB (0,5–1 GB)** | 4–8 GB VDI | Ideal para labs multi-VM |
| **Windows 10** | Propietario (EULA) | x86-64 1 GHz+ | **4096 MB (4 GB)** | 40–50 GB VDI | BIOS o UEFI |
| **Windows 11** | Propietario (EULA) | x86-64 2+ núcleos | **4096 MB (4 GB)** | 50–64 GB VDI | **Exige UEFI + Secure Boot + TPM 2.0** |
