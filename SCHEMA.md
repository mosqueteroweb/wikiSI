# SCHEMA.md — Normativa Permanente del Agente para `wikiSI`

Este documento define las reglas invariables que el agente LLM debe cumplir en cada operación de lectura, ingesta (`ingest`), compilación (`compile`), mantenimiento (`lint`), publicación y evaluación sobre el repositorio `wikiSI`.

---

## 1. Identidad del Proyecto y Autoría

- **Módulo profesional:** Sistemas Informáticos (Código **0483**).
- **Ciclo formativo:** 1º CFGS Desarrollo de Aplicaciones Multiplataforma (DAM).
- **Referencia curricular oficial:** [dam_si_relaciones.html](https://mosqueteroweb.github.io/ismie01/DAM/dam_si_relaciones.html) (Resultados de Aprendizaje RA1–RA7 y Contenidos Básicos Asociados).
- **Metodología:** Patrón **LLM Wiki** (Andrej Karpathy), adaptado con separación estricta entre fuentes inmutables (`raw/`), conocimiento compilado público (`wiki/`) y banco privado de evaluación (`privado_evaluacion/`).
- **Autor y marca:** Pedro Mosqueteroweb (`@mosqueteroweb` · `mosqueteroweb@gmail.com`).
- **Web pública (GitHub Pages):** `https://mosqueteroweb.github.io/wikiSI/`

---

## 2. Entorno Técnico Obligatorio del Aula

Toda guía paso a paso, ejercicio práctico, práctica integradora, comando de consola o diagrama de red debe estar obligatoriamente adaptado al equipamiento real del aula:

- **Sistema operativo anfitrión (Host):** **MAX (MAdrid_linuX)** de la Comunidad de Madrid (base Ubuntu/Debian LTS).
- **Hipervisor de virtualización:** **Oracle VirtualBox** ejecutándose sobre MAX.
- **Presupuesto estricto de RAM (equipos de 16 GB físicos):**
  - Ninguna práctica ni escenario con máquinas virtuales simultáneas puede superar un consumo total de **10–12 GB de RAM asignados al conjunto de las VMs activas**.
  - Se deben reservar siempre **4–6 GB libres** para el sistema anfitrión MAX y el entorno gráfico/navegador del alumno.
  - Todo enunciado de ejercicio o práctica con VirtualBox debe incluir explícitamente una **tabla de asignación de recursos**:

| VM | SO Invitado | RAM asignada | vCPUs | Disco virtual | Adaptador de red VirtualBox |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Ejemplo-VM1 | Ubuntu Server 24.04 | 2048 MB (2 GB) | 2 | 20 GB (VDI dinámico) | Red interna / NAT |

- **Sistemas operativos invitados (Guests) homologados:**
  - **Propietarios:** Windows 10, Windows 11.
  - **Libres:** Ubuntu (Desktop y Server), Linux Mint, Puppy Linux (recomendado para laboratorios multi-VM con presupuesto ajustado de RAM o pruebas ligeras).
- **Prohibiciones de entorno:** No diseñar prácticas que exijan VMware Workstation/Pro exclusivo, Hyper-V, KVM/Proxmox bare-metal o configuraciones que excedan los 12 GB simultáneos en VirtualBox. Cuando exista diferencia entre Linux y Windows, utilizar pestañas comparativas de MkDocs (`=== "Ubuntu / MAX"` / `=== "Windows 10/11"`).

---

## 3. Arquitectura de Tres Capas y Seguridad

```text
wikiSI/
├── PLAN_WIKISI.md            # Plan arquitectónico general
├── SCHEMA.md                 # Este documento normativo
├── mkdocs.yml                # Configuración de compilación MkDocs Material
├── requirements.txt          # Dependencias Python fijadas
├── scripts/
│   └── filter_unpublished.py # Hook de exclusión de páginas con publicar: false
├── raw/                      # CAPA 1: INMUTABLE (fuentes originales)
│   ├── propios/              # Apuntes, PDFs y enlaces del profesor
│   ├── inbox/                # Fuentes recolectadas pendientes de ingesta
│   ├── procesados/           # Fuentes ya compiladas en la wiki
│   └── descartados.txt       # Lista negra de URLs/dominios rechazados
├── wiki/                     # CAPA 2: WEB PÚBLICA (compilada por MkDocs)
│   ├── index.md              # Portada e índice maestro por RA y CE
│   ├── log.md                # Registro cronológico (ingest, lint, revisiones)
│   ├── assets/               # Imágenes locales (diagramas, generadas, abiertas)
│   ├── ra/                   # 7 páginas Hub (RA1.md .. RA7.md)
│   ├── conceptos/            # Conceptos teóricos + imágenes + recursos
│   ├── ejercicios/           # Ejercicios sencillos resueltos paso a paso
│   └── practicas/            # Prácticas integradoras (enunciado + solución)
└── privado_evaluacion/       # CAPA 3: PRIVADA (.gitignore — NUNCA en Git público)
    ├── examenes/             # Pruebas escritas, prácticas evaluables, Moodle/GIFT
    ├── soluciones/           # Solucionarios de examen
    └── rubricas/             # Rúbricas trazadas por RAx.CEy
```

### Regla crítica anti-filtraciones
1. `privado_evaluacion/` debe figurar siempre en `.gitignore`. Antes de cualquier `git commit` o `git push`, el agente verificará que ningún archivo de `privado_evaluacion/` esté en el área de preparación (*staging*).
2. Ninguna página de `wiki/` puede enlazar ni incrustar contenido procedente de `privado_evaluacion/`.

---

## 4. Matriz Curricular Oficial (Módulo 0483 — Sistemas Informáticos)

Fuente oficial: `https://mosqueteroweb.github.io/ismie01/DAM/dam_si_relaciones.html`.

### RA 1 — Evalúa sistemas informáticos, identificando sus componentes y características.
- **Criterios de Evaluación:**
  - `RA1.a`: Se han reconocido los componentes físicos de un sistema informático y sus mecanismos de interconexión.
  - `RA1.b`: Se han clasificado los tipos de memorias, señalando sus características e identifcando sus prestaciones y la función que desarrollan en el conjunto del sistema.
  - `RA1.c`: Se ha verificado el proceso de puesta en marcha de un equipo.
  - `RA1.d`: Se han clasificado, instalado y configurado diferentes tipos de dispositivos periféricos.
  - `RA1.e`: Se han identificado los tipos de redes y sistemas de comunicación.
  - `RA1.f`: Se han identificado los componentes de una red informática.
  - `RA1.g`: Se han interpretado mapas físicos y lógicos de una red informática.
  - `RA1.h`: Se han reconocido las normas de seguridad y prevención de riesgos laborales en el uso de los sistemas informáticos.
- **Contenidos Básicos Asociados (*Explotación de sistemas microinformáticos*):**
  - Placas base. Formatos.
  - Estructura y componentes: procesador (Set de Instrucciones, Registros, Contador, Unidad Aritmético-Lógica, Interrupciones); memoria interna, tipos y características (RAM, xPROM y otras); interfaces de entrada/salida; discos Periféricos. Adaptadores para la conexión de dispositivos. Componentes de un sistema informático.
  - Periféricos. Adaptadores para la conexión de dispositivos.
  - Normas de seguridad y prevención de riesgos laborales.
  - Características de las redes. Ventajas e inconvenientes.
  - Tipos de redes.
  - Componentes de una red informática.
  - Topologías de red.
  - Tipos de cableado. Conectores.
  - Mapa físico y lógico de una red local.

### RA 2 — Instala sistemas operativos planificando el proceso e interpretando documentación técnica.
- **Criterios de Evaluación:**
  - `RA2.a`: Se han identificado los elementos funcionales de un sistema informático.
  - `RA2.b`: Se han analizado las características, funciones y arquitectura de un sistema operativo.
  - `RA2.c`: Se han comparado sistemas operativos en base a sus requisitos, características, campos de aplicación y licencias de uso.
  - `RA2.d`: Se ha planificado el proceso de la instalación de sistemas operativos.
  - `RA2.e`: Se han instalado y actualizado sistemas operativos libres y propietarios.
  - `RA2.f`: Se han aplicado técnicas de actualización y recuperación del sistema.
  - `RA2.g`: Se han utilizado tecnologías de virtualización para instalar y probar sistemas operativos.
  - `RA2.h`: Se han instalado, desinstalado y actualizado aplicaciones.
  - `RA2.i`: Se han documentado los procesos realizados.
- **Contenidos Básicos Asociados (*Instalación de sistemas operativos*):**
  - Evolución histórica y clasificación.
  - Funciones de un sistema operativo.
  - Tipos de sistemas operativos.
  - Tipos de aplicaciones.
  - Licencias y tipos de licencias.
  - Procedimiento de instalación.
  - Gestores de arranque. Configuración y reparación.
  - Tecnologías de virtualización. Tipos.
  - Consideraciones previas a la instalación de sistemas operativos libres y propietarios.
  - Instalación de sistemas operativos libres y propietarios. Requisitos, versiones y licencias.
  - Instalación/desinstalación de aplicaciones. Requisitos, versiones y licencias.
  - Actualización y recuperación de sistemas operativos y aplicaciones.
  - Documentación de la instalación y de las incidencias detectadas.

### RA 3 — Gestiona la información del sistema identificando las estructuras de almacenamiento y aplicando medidas para asegurar la integridad de los datos.
- **Criterios de Evaluación:**
  - `RA3.a`: Se han comparado sistemas de archivos.
  - `RA3.b`: Se ha identificado la estructura y función de los directorios del sistema
  - `RA3.c`: operativo. *(Nota de trazabilidad curricular: en la tabla HTML oficial el criterio `b)` aparece partido entre `b)` y `c) operativo.`, manteniendo los 8 literales `RA3.a`–`RA3.h` de la fuente original).*
  - `RA3.d`: Se han utilizado herramientas en entorno gráfico y comandos para localizar información en el sistema de archivos.
  - `RA3.e`: Se han creado diferentes tipos de particiones y unidades lógicas.
  - `RA3.f`: Se han realizado y restaurado copias de seguridad.
  - `RA3.g`: Se han planificado y automatizado tareas.
  - `RA3.h`: Se han instalado y evaluado utilidades relacionadas con la gestión de información.
- **Contenidos Básicos Asociados (*Gestión de la información*):**
  - Gestión de sistemas de archivos mediante comandos y entornos gráficos.
  - Estructura de directorios de sistemas operativos libres y propietarios.
  - Búsqueda de información del sistema mediante comandos y herramientas gráficas.
  - Identificación del software instalado mediante comandos y herramientas gráficas.
  - Realización y restauración de copias de seguridad.
  - Herramientas de administración de discos. Particiones y volúmenes. Desfragmentación y chequeo. Cifrado.
  - Tareas automáticas. Planificación.

### RA 4 — Gestiona sistemas operativos utilizando comandos y herramientas gráficas y evaluando las necesidades del sistema.
- **Criterios de Evaluación:**
  - `RA4.a`: Se han configurado cuentas de usuario locales y grupos.
  - `RA4.b`: Se ha asegurado el acceso al sistema mediante el uso de directivas de cuenta y directivas de contraseñas.
  - `RA4.c`: Se han identificado, arrancado y detenido servicios y procesos.
  - `RA4.d`: Se ha protegido el acceso a la información mediante el uso de permisos locales y listas de control de acceso.
  - `RA4.e`: Se han utilizado comandos para realizar las tareas básicas de configuración y administración del sistema.
  - `RA4.f`: Se ha monitorizado el sistema.
  - `RA4.g`: Se han instalado y evaluado utilidades para el mantenimiento y optimización del sistema.
  - `RA4.h`: Se han evaluado las necesidades del sistema informático en relación con el desarrollo de aplicaciones.
- **Contenidos Básicos Asociados (*Configuración de sistemas operativos*):**
  - Configuración de usuarios y grupos.
  - Seguridad de cuentas de usuario.
  - Seguridad de contraseñas.
  - Acceso a recursos. Permisos locales. Listas de control de acceso.
  - Servicios y procesos.
  - Comandos de sistemas operativos libres y propietarios.
  - Herramientas de monitorización del sistema. Registros y logs.

### RA 5 — Interconecta sistemas en red configurando dispositivos y protocolos.
- **Criterios de Evaluación:**
  - `RA5.a`: Se ha configurado el protocolo TCP/IP.
  - `RA5.b`: Se han configurado redes de área local cableadas.
  - `RA5.c`: Se han configurado redes de área local inalámbricas.
  - `RA5.d`: Se han utilizado dispositivos de interconexión de redes.
  - `RA5.e`: Se ha configurado el acceso a redes de área extensa.
  - `RA5.f`: Se han gestionado puertos de comunicaciones.
  - `RA5.g`: Se ha verificado el funcionamiento de la red mediante el uso de comandos y herramientas básicas.
  - `RA5.h`: Se han aplicado protocolos seguros de comunicaciones.
- **Contenidos Básicos Asociados (*Conexión de sistemas en red*):**
  - Configuración del protocolo TCP/IP en un cliente de red. Direcciones IP. Máscaras de subred. Puertas de enlace. Servidores de nombres de dominio. IPv4. IPv6. Configuración estática. Configuración dinámica automática.
  - Ficheros de configuración de red.
  - Gestión de puertos.
  - Resolución de problemas de conectividad en sistemas operativos en red. Herramientas de diagnóstico.
  - Herramientas gráficas y comandos utilizados en sistemas operativos libres y propietarios.
  - Monitorización de redes.
  - Protocolos TCP/IP.
  - Configuración de los adaptadores de red en sistemas operativos libres y propietarios.
  - Interconexión de redes: adaptadores de red y dispositivos de interconexión. Enrutamiento.
  - Redes cableadas. Tipos y características. Adaptadores de red. Conmutadores, enrutadores, entre otros. Seguridad.
  - Redes inalámbricas. Tipos y características. Adaptadores. Dispositivos de interconexión. Seguridad.
  - Seguridad de comunicaciones.
  - Tecnologías de acceso a redes de área extensa.

### RA 6 — Opera sistemas en red gestionando sus recursos e identificando las restricciones de seguridad existentes.
- **Criterios de Evaluación:**
  - `RA6.a`: Se ha configurado el acceso a recursos locales y recursos de red.
  - `RA6.b`: Se han identificado y configurado los derechos de usuario y directivas de seguridad.
  - `RA6.c`: Se han explotado servidores de ficheros, servidores de impresión y servidores de aplicaciones.
  - `RA6.d`: Se ha accedido a los servidores utilizando técnicas de conexión remota.
  - `RA6.e`: Se ha evaluado la necesidad de proteger los recursos y el sistema.
  - `RA6.f`: Se han instalado y evaluado utilidades de seguridad básica.
  - `RA6.g`: Se han configurado y explotado dominios.
- **Contenidos Básicos Asociados (*Gestión de recursos en una red*):**
  - Permisos y derechos. Permisos de red. Permisos locales. Herencia. Listas de control de acceso.
  - Configuración de recursos compartidos. Permisos de acceso y directivas de seguridad.
  - Requisitos de seguridad del sistema y de los datos.
  - Servidores de ficheros.
  - Servidores de impresión.
  - Servidores de aplicaciones.
  - Técnicas de conexión remota.
  - Cortafuegos.
  - Implantación y explotación de dominios.

### RA 7 — Elabora documentación valorando y utilizando aplicaciones informáticas de propósito general.
- **Criterios de Evaluación:**
  - `RA7.a`: Se ha clasificado software en función de su licencia y propósito.
  - `RA7.b`: Se han analizado las necesidades específicas de software asociadas al uso de sistemas informáticos en diferentes entornos productivos.
  - `RA7.c`: Se han realizado tareas de documentación mediante el uso de herramientas ofimáticas y de trabajo colaborativo.
  - `RA7.d`: Se han utilizado sistemas de correo y mensajería electrónica.
  - `RA7.e`: Se han utilizado los servicios de transferencia de ficheros.
  - `RA7.f`: Se han utilizado métodos de búsqueda de documentación técnica mediante el uso de servicios de Internet.
  - `RA7.g`: Se han utilizado herramientas de propósito general.
- **Contenidos Básicos Asociados (*Explotación de aplicaciones informáticas de propósito general*):**
  - Software: tipos, requisitos, licencias.
  - Herramientas ofimáticas y de trabajo colaborativo.
  - Utilidades de propósito general: antimalware, correo, transferencia de ficheros, recuperación de datos, mantenimiento del sistema, entre otros.

---

## 5. Convenciones de Archivos y Frontmatter YAML

Todas las páginas de `wiki/` (salvo `index.md` y `log.md`, donde es opcional) deben incluir un bloque de frontmatter YAML al inicio:

```yaml
---
title: "Título descriptivo"
ra: ["RA1"]
ce: ["RA1.a", "RA1.b"]
tipo: "concepto" # concepto | ejercicio | practica-enunciado | practica-solucion | hub-ra | indice
publicar: true   # false para soluciones de prácticas aún no liberadas en clase
fuentes:
  - "raw/procesados/nombre-fuente.md"
ultima_revision: "2026-11-15"
---
```

### Reglas de publicación (`publicar`)
- `publicar: true` (valor por defecto si se omite): la página se compila y publica en GitHub Pages.
- `publicar: false`: el hook `scripts/filter_unpublished.py` excluye la página del build de MkDocs para que no sea accesible en la web pública hasta que el profesor autorice cambiarlo a `true`.

---

## 6. Progresión Pedagógica y Niveles de Contenido

El desarrollo de la wiki es **secuencial por Resultados de Aprendizaje**: se completa, enlaza y valida `RA1` antes de avanzar a `RA2`, y así sucesivamente hasta `RA7`.

Cada bloque de RA se articula en **4 niveles**:

1. **Conceptos (`wiki/conceptos/`):**
   - Nomenclatura sugerida: `raX-tema-corto.md` (p. ej., `ra1-placas-base-memorias.md`).
   - Explicación técnica rigurosa con comparativa entre sistemas libres y propietarios cuando corresponda.
   - **Imágenes explicativas obligatorias:**
     - Diagramas técnicos editables en **Mermaid** (` ```mermaid `) o **SVG**.
     - Ilustraciones conceptuales generadas con **Gemini (`image-generator`)** guardadas en `wiki/assets/`.
     - Imágenes externas con licencia abierta compatible (Wikimedia Commons, documentación oficial CC/MIT, etc.), descargadas siempre en local en `wiki/assets/` con atribución explícita para evitar enlaces rotos.
   - **Sección final obligatoria `## Recursos para profundizar`:**
     - Enlaces verificados a artículos o documentación técnica de referencia.
     - Enlaces relevantes a vídeos explicativos en YouTube.

2. **Ejercicios prácticos sencillos resueltos (`wiki/ejercicios/`):**
   - Nomenclatura sugerida: `eXX-raX-titulo-corto.md`.
   - Píldoras cortas enfocadas en una destreza atómica (un comando, un tipo de particionado, una configuración de red o permiso concreto).
   - Incluyen enunciado breve, requisitos en MAX/VirtualBox (si aplican) y **resolución paso a paso** visible o desplegable (`??? note "Ver resolución paso a paso"`).

3. **Prácticas integradoras de clase (`wiki/practicas/`):**
   - Diseñadas para que el alumno integre los conocimientos de los ejercicios sencillos previos.
   - Divididas **siempre** en dos documentos enlazados:
     - **Enunciado (`pXX-nombre-enunciado.md`):** `publicar: true` desde el inicio. Incluye tabla de VMs y RAM (máximo 10–12 GB totales), tareas numeradas, criterios de evaluación (`RAx.CEy`) y evidencias a entregar en el Aula Virtual.
     - **Guía de resolución (`pXX-nombre-solucion.md`):** `publicar: false` por defecto hasta que el profesor ordene su publicación tras finalizar la práctica en clase.

4. **Evaluación privada (`privado_evaluacion/`):**
   - Exámenes teóricos/prácticos (`examenes/`), solucionarios (`soluciones/`) y rúbricas (`rubricas/`) trazadas a `RAx.CEy`, alineados con lo impartido en `wiki/` y excluidos de Git público.

---

## 7. Protocolo de Credibilidad de Fuentes y Trazabilidad Inversa

### Clasificación en 3 niveles (antes de ingestar en `raw/`)
- **Nivel 1 (Autoridad máxima):** Documentación oficial de fabricantes y proyectos (Microsoft Learn, Debian/Ubuntu/Arch Wiki, Red Hat Docs, Kernel.org, Oracle VirtualBox User Manual, RFCs/IETF, guías oficiales de MAX/EducaMadrid).
- **Nivel 2 (Reputación técnica contrastada):** Universidades, instituciones educativas públicas, libros técnicos reconocidos y portales de ingeniería contrastados sin granjas de contenido SEO.
- **Nivel 3 (Descarte automático):** Blogs anónimos generados por IA, portales con errores técnicos detectados, páginas sin fecha ni autoría o contenido contradictorio sin respaldo. Todo dominio descartado se anota en `raw/descartados.txt`.

### Trazabilidad inversa y borrado limpio
- Toda página de `wiki/` enumera sus fuentes en el frontmatter (`fuentes: [...]`) y anota afirmaciones o bloques clave mediante comentarios HTML invisibles en el renderizado final:
  `<!-- fuente: raw/procesados/nombre-archivo.md -->`
- Cada compilación o lote de trabajo debe quedar registrado en `wiki/log.md` y consolidado con un **commit atómico en Git**.
- Si el profesor solicita *"quita esta fuente"* o *"corrige este dato"*:
  1. Localizar todas las ocurrencias en `wiki/` mediante búsqueda de comentarios y frontmatter.
  2. Reescribir y validar el contenido afectado manteniendo la coherencia con las fuentes restantes de Nivel 1/2.
  3. Añadir la URL o dominio retirado a `raw/descartados.txt` para impedir futuras descargas.

---

## 8. Flujo de Mantenimiento (`ingest`, `lint`, `publish`)

1. **Ingesta (`ingest`):** Leer nuevas fuentes en `raw/propios/` o `raw/inbox/`, validar nivel de credibilidad (descartando Nivel 3 en `raw/descartados.txt`), sintetizar en `wiki/` actualizando los hubs `wiki/ra/RAx.md` y `wiki/index.md`, mover la fuente a `raw/procesados/` y registrar en `wiki/log.md`.
2. **Auditoría (`lint`):** Comprobar periódicamente enlaces internos rotos, imágenes locales existentes en `wiki/assets/`, cumplimiento del presupuesto de RAM (<= 12 GB en VMs), coherencia curricular (`RAx.CEy`) y presencia de `## Recursos para profundizar` en conceptos.
3. **Publicación (`publish`):** Verificar localmente con `.venv/bin/mkdocs build` que las páginas con `publicar: false` quedan excluidas y realizar push a `main` para activar el despliegue automático en GitHub Pages.
