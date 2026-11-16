---
title: "Práctica p08 · Catálogo de Tareas Entregables del Curso"
ra: ["RA1", "RA2", "RA3", "RA4", "RA5", "RA6", "RA7"]
ce: ["RA1.a", "RA1.b", "RA1.d", "RA1.h", "RA2.c", "RA2.e", "RA2.g", "RA3.d", "RA3.e", "RA3.h", "RA4.e", "RA5.e", "RA6.a", "RA6.d", "RA7.b", "RA7.c", "RA7.f", "RA7.g"]
tipo: "practica-enunciado"
publicar: true
ultima_revision: "2026-11-16"
---

# Práctica 08 · Catálogo de Tareas Entregables del Aula Virtual

Esta página reúne los enunciados normalizados y las listas de comprobación (*checklists*) de las **12 tareas prácticas entregables** a lo largo del módulo **Sistemas Informáticos (`0483 · 1.º DAM`)**. Salvo indicación contraria en el Aula Virtual, todas se entregan de forma individual en **PDF con portada, índice, título y autor visible**.

---

## Bloque 1 · Hardware y Montaje (`RA1`)

### Tarea 1 · Comprar ordenador (2 presupuestos por componentes)

Consiste en diseñar **dos presupuestos cerrados** de ordenadores montados por piezas: uno de **Alto Rendimiento / Gaming (`2.200 €`)** y otro de **Ofimática bajo-medio (`800 €`)**.

1. **Catálogo comparativo previo:** selecciona **3 componentes diferentes**, con **características distintas** y de **marcas diferentes**, por cada una de las **10 categorías** obligatorias:
   `Chasis` · `Fuente de alimentación` · `Placa base` · `Microprocesador` · `RAM` · `Discos duros` · `Tarjeta gráfica` · `Monitor` · `Teclado` · `Ratón`.
2. **Componentes adicionales necesarios:** presupuesta también cualquier pieza indispensable (disipador si el procesador viene sin él, pasta térmica si procede, sistema operativo).
3. **Dos presupuestos finales cerrados:** indica el listado final con precios, suma exacta, enlaces directos de compra a producto real, fotografías/capturas de catálogo y justificación de cada elección.
4. **Análisis de cuellos de botella:** calcula y adjunta el resultado de [`pc-builds.com`](https://pc-builds.com/es/bottleneck-calculator/).

!!! check "Lista rápida antes de entregar «Comprar ordenador»"
    - [ ] ¿Los totales entran dentro del margen permitido (máx. `+5 %` y mínimo `75 %` del presupuesto)?
    - [ ] ¿Son físicamente compatibles CPU + Placa (socket) + RAM (`DDR4`/`DDR5`) + Caja (`ATX`/`mATX`)?
    - [ ] ¿Los equipos funcionan completos nada más montarlos (con **disipador** si la CPU no lo trae de serie y **Sistema Operativo**)?
    - [ ] ¿El PDF tiene portada, índice, título y autor? *(Si supera los 10 MB, sube un PDF ligero con enlace directo al PDF en tu nube).*

### Tarea 2 · Montaje de PC y Montaje de Servidor en taller

- Elabora **1 PDF** con fotografías secuenciadas y explicación técnica de cada paso realizado durante las sesiones de montaje de PC de escritorio y montaje de servidor en taller (precauciones ESD, placa base, CPU/pasta térmica/disipador, módulos RAM en doble canal, cableado ATX/SATA/frontal y verificación POST).

---

## Bloque 2 · Sistemas Operativos y Paquetería (`RA2`)

### Tarea 3 · Instalar múltiples Sistemas Operativos en VirtualBox (2 Windows + 2 Linux)

Sobre una máquina virtual en VirtualBox con un único disco duro virtual y **soporte EFI activado antes de instalar**:

- **Objetivo final:** instalar **2 sistemas Windows junto a 2 distribuciones Linux distintas**.
- **Progresión recomendada:** (1) 1 Windows + 1 Linux → (2) 2 Windows → (3) 2 Linux → (4) 2 Windows + 2 Linux en el menú de arranque (GRUB2).
- **Notas técnicas para Windows 11 en VM:** activa EFI; si requiere saltar comprobaciones TPM o crear cuenta local sin Microsoft Account durante el asistente OOBE, pulsa `Shift + F10` y utiliza `start ms-cxh:localonly` (con tu nombre y apellidos en la cuenta local) siguiendo [la guía de apoyo de VirtualBox](https://www.ubackup.com/es/windows-11/instalar-windows-11-iso-en-virtualbox-3023-tc.html).
- **Entrega:** guía paso a paso en PDF (y llevar la VM operativa al aula teniendo cuidado al exportar/importar `.ova`).

### Tarea 4 · Instalar 6 aplicaciones en Linux por métodos distintos

Sobre una VM Linux Mint o Ubuntu, instala y verifica **6 aplicaciones** utilizando obligatoriamente un método diferente para cada una:

1. Desde la **tienda gráfica** (ej. `GParted`).
2. Descargando paquete **`.deb`** desde web (ej. `Visual Studio Code`).
3. Mediante comando **`apt install`** en terminal (ej. `GIMP`).
4. En formato **Flatpak** (ej. `Telegram Desktop`).
5. En ejecutable portable **AppImage** (ej. `Audacity`).
6. Añadiendo un repositorio **PPA** por consola (ej. `my-weather-indicator` o equivalente vigente).

### Tarea 5 · USB Multiarranque y Alternativas de Software

- **USB Multiarranque:** crea una memoria USB multiarranque (con **Ventoy** o **YUMI**) cargada con varias ISOs de sistemas operativos y rescate (Windows, Linux, Hiren's BootCD PE) y documenta su menú de arranque real.
- **Alternativas en Windows (práctica comparativa):** busca, instala y captura el funcionamiento de **3 alternativas** para: explorador de archivos por defecto, analizador de ocupación de disco (*WinDirStat*), recuperación de archivos borrados y comparación de ficheros.

---

## Bloque 3 · Almacenamiento, Copias de Seguridad y PRL (`RA3` y `RA1.h`)

### Tarea 6 · Crear RAIDs (`0`, `1` y `5`) en Windows y Linux

Implementa y verifica tolerancia a fallos en **ambos sistemas**:
- **Windows:** mediante **Espacios de almacenamiento** (*espacio simple* → RAID 0, *espacio de reflejo* → RAID 1, *espacio de paridad* → RAID 5).
- **Linux (`mdadm`):** creación de `/dev/md0`, `/dev/md1` y `/dev/md5`, simulación de fallo de disco y verificación de lectura de datos.

### Tarea 7 · Política y Supuesto Práctico de Copias de Seguridad

Redacta un documento justificado cubriendo todos estos puntos + capturas de realización y restauración real con software de backup:
- **¿Qué datos?** Políticas diferenciadas por tipo (*Sistema*, *Documentos/trabajos del curso*, *Otros*).
- **¿Cómo?** Estrategia (*Completa*, *Diferencial*, *Incremental*).
- **¿Cuándo?** Periodicidad y política de sustitución/rotación.
- **¿Dónde?** Regla **3-2-1** y soportes elegidos.
- **¿Por qué y seguridad?** Cifrado, etiquetado, listado de acceso, software elegido y **pruebas verificadas de respaldo y recuperación**.

### Tarea 8 · Sincronización (`rclone` + herramienta en Windows)

Realiza una sincronización en **Windows** y otra en **Linux** (obligatoriamente con **`rclone`** en Linux): una **local → nube** y la otra **local → local**, eligiendo qué SO realiza cada caso, comprobando en PDF con capturas la propagación de cambios.

### Tarea 9 · Clonación de Equipos con Clonezilla

1. Crea una imagen completa de un equipo en VirtualBox con **Clonezilla**.
2. Restaura esa imagen sobre otro equipo (*unicast*).
3. Realiza la restauración simultánea en red sobre **2 equipos en paralelo por Multicast**.

### Tarea 10 · Investigación de Riesgos Laborales (`PRL` · Necesaria para `FFE`)

Elabora un informe sobre los riesgos laborales en sistemas informáticos (equipos personales, pymes y centros de datos) respondiendo de forma ordenada a los **9 puntos**:

1. Factores de riesgo (lugar/equipos, físicos, químicos, biológicos, ergonómicos y psicosociales).
2. Medidas de prevención de riesgos laborales.
3. Principales daños derivados (accidentes de trabajo y enfermedades profesionales).
4. Principales protocolos de trabajo seguro (eléctrico, limpieza, evacuación, gestión del estrés).
5. Principales fuentes de riesgo laboral.
6. Equipamientos, instalaciones preventivas y **Equipos de Protección Individual (EPIs)**.
7. Medidas de **señalización de seguridad** (advertencia, obligación, socorro, prohibición, evacuación, información).
8. Medidas de protección colectiva.
9. Riesgos laborales vinculados a la salud psicológica del equipo.

---

## Bloque 4 · Redes, Contenedores y Aplicaciones (`RA4`–`RA7`)

### Tarea 11 · Redes, Acceso Remoto, Contenedores y Nube

- **Carpetas compartidas en red interna Windows NTFS (`e26`):** pruebas de acceso anónimo, permisos diferenciados (`pedro` R/W vs resto RO), cambio de propietario y experimento de **cifrado EFS entre Pedro y Luis**.
- **Terminales y conexión remota (`e28`):** servidor **SSH** en Linux con claves sin contraseña, cliente **PuTTY**, **RDP** (*Windows App* + *Remmina*), **VNC** y **RustDesk** (administración remota y modo presentación desde PC y móvil).
- **Despliegue de aplicaciones y web:**
  - *Contenedores Docker:* formulario web PHP que almacena nombre y edad en base de datos + segundo contenedor de monitorización de recursos.
  - *Hosting / VPS (`Clouding.io`):* subir `web1.html` con CSS externo e imágenes servida desde un servidor web LAMP y entregar enlace en PDF.
  - *(Opcional)* Acceso desde Internet a un servidor alojado en casa (DDNS + redirección de puertos + verificación de CG-NAT).
- **Manual de comandos Linux en GitHub:** entregar un PDF con enlace clicable directo al `README.md` índice de vuestro repositorio.

### Tarea 12 · Manual de Aplicaciones Informáticas Comunes (`RA7`)

Elabora un manual de uso con **ejemplos reales y capturas de pantalla** (donde se vea siempre tu nombre y apellidos, aunque sea en un bloc de notas abierto en segundo plano) cubriendo las siguientes familias:

- **Ofimática:** creación/edición en local y en nube con Documentos y Hojas de cálculo (`Microsoft Office` Word/Excel, `Google Workspace`, `LibreOffice` — 4 ejemplos).
- **Diseño y Multimedia:** `Canva`, `Audacity`.
- **Comunicación y Colaboración:** `Microsoft Teams`, `Discord`, **Wiki + GitHub** (*TiddlyWiki* u *Obsidian* con repositorio GitHub).
- **Desarrollo y Bases de Datos:** `Visual Studio Code`, `Eclipse`, `MySQL`, `Oracle`.
- **Seguridad, Navegación y Correo:** Cortafuegos, cifrado/firma **GPG en Mozilla Thunderbird** (configurando cuenta de EducaMadrid), navegadores **Brave** y **Zen Browser**, mensajería (`Telegram`) y **WeTransfer**.
- **Nube, Búsqueda, Productividad e IA:** `Dropbox`, `pCloud`/`Mega`, buscadores (`Bing`, `DuckDuckGo`), **2 herramientas de IA generativa de texto y 2 de imagen**, notas (`Notion`/`Obsidian`/`Keep`), calendario en nube alternativo y tablero **Kanban** (`Trello`).
