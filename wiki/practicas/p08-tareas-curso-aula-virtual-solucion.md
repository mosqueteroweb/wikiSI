---
title: "Solución Práctica p08 · Solucionarios y Guías de Corrección del Aula Virtual"
ra: ["RA1", "RA2", "RA3", "RA4", "RA5", "RA6", "RA7"]
ce: ["RA1.h", "RA3.h", "RA6.a", "RA6.b", "RA6.d", "RA7.b", "RA7.c", "RA7.g"]
tipo: "practica-solucion"
publicar: false
ultima_revision: "2026-11-16"
---

# Guía de Resolución · Tareas del Aula Virtual (`p08`)

> [!CAUTION]
> **Documento privado para el profesor (`publicar: false`).** Visible exclusivamente en el Portal Docente Local (puerto 81).

---

## 1. Solución Completa · Tarea de Riesgos Laborales (`PRL` / `FFE`)

### 1. Factores de riesgo en su actividad
- **Riesgos derivados del lugar y equipos de trabajo:** iluminación deficiente, ventilación o climatización inadecuada en aulas/centros de datos; equipos informáticos o servidores en mal estado con riesgo de cortocircuitos, sobrecalentamiento o caída física de cargas pesadas en racks.
- **Riesgos físicos, químicos o biológicos:**
  - *Físicos:* fatiga ocular, cefaleas y trastornos musculoesqueléticos por uso prolongado de pantallas; ruido continuo en salas de servidores.
  - *Químicos:* exposición puntual a plomo, mercurio o cadmio en reciclaje o manipulación de componentes electrónicos deteriorados.
  - *Biológicos:* proliferación de hongos y mohos en salas climatizadas con humedad descontrolada.
- **Riesgos ergonómicos:** sillas/monitores mal regulados (túnel carpiano, dolores cervicales/lumbares) y trabajo continuado frente a PVD sin descansos.
- **Riesgos psicosociales:** estrés por plazos ajustados, aislamiento en teletrabajo o CPDs nocturnos y síndrome de desgaste profesional (*burnout*).

### 2. Medidas de prevención de riesgos laborales
- **Ergonomía:** silla regulable con pies apoyados, borde superior del monitor a la altura de los ojos (45–70 cm), teclado y ratón alineados.
- **Pausas activas:** pausas breves cada 20–30 minutos para descanso visual y estiramientos.
- **Formación e higiene ambiental:** capacitación postural, control de temperatura/humedad/ventilación, iluminación sin reflejos y gestión saludable de cargas de trabajo.

### 3. Principales daños derivados
- **Accidentes de trabajo:** golpes, caídas de material, descargas eléctricas o cortes al manipular chasis.
- **Enfermedades profesionales:** trastornos musculoesqueléticos (espalda, cuello, muñeca) y fatiga visual (síndrome visual informático, sequedad ocular), además de estrés crónico / *burnout*.

### 4. Principales protocolos de trabajo seguro
- **Seguridad eléctrica:** tomas con puesta a tierra, regletas con protección contra sobrecargas y desconexión previa antes de abrir equipos.
- **Limpieza y mantenimiento:** rutinas periódicas para evitar obstrucción de disipadores y acumulación de polvo conductor.
- **Evacuación y prevención de estrés:** señalización de salidas de emergencia y canales flexibles de seguimiento laboral.

### 5. Principales fuentes de riesgo
1. Hardware o servidores deteriorados / cables expuestos.
2. Factores ambientales deficientes (iluminación, ruido, temperatura).
3. Organización deficiente de tareas y falta de pausas.

### 6. Equipamientos, instalaciones preventivas y EPIs
- **Instalaciones/mobiliario:** sillas ergonómicas, mesas regulables, climatización de CPD, **SAIs (UPS)** y supresores de picos, luminarias y pantallas antirreflejos.
- **EPIs:** **protección auditiva** en centros de datos ruidosos, **guantes/pulseras antiestáticos (`ESD`)** al manipular placas base/RAM y **gafas de protección** ante trabajos con fibra óptica/láser o herramientas mecánicas.

### 7. Señalización de seguridad
- **Advertencia** (triángulo amarillo: riesgo eléctrico / alta temperatura), **Obligación** (círculo azul: uso de EPIs/ESD), **Socorro/Salvamento** (verde: botiquín/ducha/primeros auxilios), **Prohibición** (círculo rojo tachado: acceso restringido), **Evacuación** (verde: rutas de salida) e **Información/Equipos contra incendios**.

### 8. Medidas de protección colectiva
- Sistemas generales de ventilación/extracción, resguardos y cerramientos de seguridad en maquinaria/racks, protocolos de limpieza y barreras o cabinas acústicas de atenuación de ruido.

### 9. Salud psicológica en el equipo
- Prevención activa del **estrés laboral**, **aislamiento** en remoto, **burnout** y **conflictos interpersonales** mediante comunicación clara, reparto equilibrado de cargas y apoyo organizacional.

---

## 2. Solucionario Razonado · Práctica de Carpetas Compartidas y Cifrado EFS (`Pedro y Luis`)

1. **Usuario que no existe en el servidor Windows compartido (`Grupo de Trabajo`):**
   - Por defecto falla la autenticación porque está activo el *Uso compartido con protección por contraseña*. Si el recurso añade `Todos` (*Everyone*) y se desactiva la protección por contraseña (y en su caso se habilita usuario anónimo/Invitado), podrá acceder si las directivas locales (`secpol.msc` → *Acceso a este equipo desde la red*) lo permiten, aunque se pierde trazabilidad y seguridad.
2. **`Pedro` lee y escribe, resto solo lee:**
   - En **Permisos de recurso compartido (SMB)** conviene conceder *Control total* o *Cambiar* a `Pedro` y *Lectura* al resto (o *Cambiar* a `Usuarios autentificados` filtrando finamente en **Permisos NTFS**: `Modificar` para `Pedro` y `Lectura y ejecución` para `Usuarios`). Recuerda que en red prevalece el permiso **más restrictivo** al cruzar SMB ∩ NTFS.
3. **Caso crítico de Cifrado EFS (`Pedro` cifra la carpeta con permisos de escritura para ambos):**
   - *¿Puede leer `Luis` los archivos de `Pedro`?* **No.** EFS cifra la clave simétrica de archivo (*FEK*) usando la clave pública del certificado EFS de `Pedro`. Aunque `Luis` tenga Control total NTFS sobre el fichero, Windows devuelve *Acceso denegado* al descifrar porque no posee la clave privada de `Pedro` (salvo que Pedro agregue explícitamente el certificado de Luis al archivo).
   - *¿Puede `Luis` crear archivos nuevos en esa carpeta y quedan cifrados?* **Sí.** `Luis` conserva su permiso NTFS de escritura en el directorio; al crear un archivo nuevo dentro de una carpeta marcada con el atributo EFS, Windows cifra ese nuevo fichero **con el certificado propio de `Luis`**, de modo que **`Pedro` tampoco podrá leer los archivos creados por `Luis`**.
   - *¿Y al acceder por red a la carpeta compartida?* Cada usuario solo podrá abrir **los suyos** (y siempre que el equipo servidor donde reside el perfil/certificado EFS o Active Directory resuelva correctamente el descifrado del certificado del usuario conectado).
4. **Cambio de propietario NTFS:** si el administrador transfiere la propiedad a otra cuenta y el antiguo propietario no figura con una ACE explícita de escritura/control total (o pertenecía solo por `CREATOR OWNER`), **pierde el acceso de modificación** en cuanto se recalculan o editan los permisos locales.
5. **Conclusión arquitectónica:** tener que replicar usuarios, contraseñas y certificados en cada máquina aislada es ingobernable → justificación directa del salto a **Active Directory / Samba AD DC**.

---

## 3. Criterios Rápidos de Verificación Docente (Resto de Tareas)

| Tarea | Puntos críticos que verificar al corregir |
| :--- | :--- |
| **Comprar ordenador** | Ver informe detallado de los 21 alumnos en [`correcciones/tarea-comprar-ordenador.md`](../privado_evaluacion/correcciones/tarea-comprar-ordenador.md). |
| **Múltiples SOs (4 SOs)** | Soporte **EFI** activo en VirtualBox, particiones diferenciadas sin machacar el bootloader, cuenta local creada en Windows 11 (`start ms-cxh:localonly`) y menú GRUB funcional con las 4 entradas. |
| **6 apps en Linux** | Evidencia por consola/captura de cada origen distinto (no valen 6 apps instaladas todas con `apt`): `dpkg -l`, `flatpak list`, archivo `.AppImage` ejecutable (`ls -l`), repositorio PPA listado en `/etc/apt/sources.list*`. |
| **RAID 0/1/5** | Capacidad útil correcta (`RAID 0 = N·C`, `RAID 1 = C`, `RAID 5 = (N-1)·C`), evidencia de fallo simulado en `mdadm` (`/proc/mdstat` degradado `[_U]`) y en *Espacios de almacenamiento* de Windows. |
| **Sincronización & Backups** | En Linux obligatorio **`rclone`** (uno `local->local`, otro `local->nube`); en política de backups no confundir copia con RAID/snapshot y aportar captura de **restauración real**. |
| **Clonezilla** | Imagen creada + prueba real de despliegue **Multicast** hacia al menos 2 VMs clientes en red interna. |
| **Aplicaciones comunes + Docker/VPS** | Captura donde siempre se distinga el nombre del alumno, configuración **GPG real en Thunderbird**, página `web1.html` con CSS externo en VPS LAMP (`HTTP 200`), y en Docker uso real de volumen + red entre el formulario PHP y la base de datos. |
