---
id: "raw-ra3-copias-seguridad-automatizacion-tareas"
ra: ["RA3"]
ce: ["RA3.f", "RA3.g", "RA3.h"]
nivel_credibilidad: "Nivel 1 y Nivel 2"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "man-pages Linux: tar(1), rsync(1), cron(8), crontab(5), systemd.timer(5), at(1), dd(1)"
  - "Clonezilla Official Documentation (clonezilla.org)"
  - "Microsoft Learn: Robocopy, Wbadmin, Task Scheduler (schtasks / Register-ScheduledTask)"
---

# Fuente Procesada: Copias de Seguridad, Clonación y Automatización de Tareas

## 1. Estrategias y Tipos de Copias de Seguridad (`RA3.f`)

Dos métricas definen cualquier plan de respaldo empresarial:
- **RPO (*Recovery Point Objective*):** Pérdida máxima admisible de datos medida en tiempo (ej. copias cada 24 h = RPO de 24 h).
- **RTO (*Recovery Time Objective*):** Tiempo máximo tolerable hasta restaurar la operatividad del servicio.

### Comparativa de tipos de respaldo
1. **Completa (*Full*):** Copia todos los archivos seleccionados cada vez. Máximo consumo de espacio/tiempo al realizarla; **restauración más rápida** (solo requiere el último archivo completo).
2. **Incremental:** Solo copia los cambios desde la **última copia realizada (sea completa o incremental)**. Mínimo tamaño y rapidez diaria; **restauración lenta** (necesita la última completa + **todas** las incrementales encadenadas hasta la fecha).
3. **Diferencial:** Copia todo lo modificado desde la **última copia completa**. Ocupación intermedia creciente cada día; **restauración intermedia** (solo necesita la última completa + la última diferencial).

### Regla de Oro 3-2-1
- **3** copias de tus datos críticos (1 original + 2 respaldos).
- En **2** soportes o medios distintos (ej. SSD interno + NAS/disco USB externo).
- Al menos **1** copia **fuera del emplazamiento físico** (*off-site* / nube cifrada / ubicación remota) resistente a incendios, robos o ransomware (*air-gapped* o inmutable).

## 2. Herramientas de Respaldo y Clonación (`RA3.f`, `RA3.h`)

- **Linux CLI:**
  - `tar -czvf backup.tar.gz /ruta` (empaquetado + compresión gzip; con `-g snapshot.snar` hace copias incrementales).
  - `rsync -avh --delete /origen/ /destino/` (sincronización diferencial por bloques/metadatos, local o sobre SSH con `-e ssh`; `--dry-run` permite simular sin escribir).
  - `dd` / `partclone`: clonación sector a sector (solo particiones usadas en `partclone`).
  - **Clonezilla Live:** Estándar libre para clonar e restaurar imágenes completas de discos o particiones NTFS/ext4/GPT por red o USB.
  - **Deja Dup** / **BorgBackup** / **Restic**: Herramientas con deduplicación y cifrado de cliente.
- **Windows:**
  - `robocopy C:\Datos D:\Backup /MIR /Z /R:3 /W:5 /LOG:backup.log` (*Robust File Copy*, estándar superior a `xcopy`).
  - `wbadmin` / Copias de seguridad e imagen del sistema, **Historial de archivos**, o soluciones de imagen en caliente en servidor/aula.

## 3. Planificación y Automatización de Tareas (`RA3.g`)

- **GNU/Linux — `cron` y `systemd timers`:**
  - Archivo de usuario con `crontab -e` o global en `/etc/cron.d/`.
  - Formato clásico de **5 campos temporales**:
    `m  h  dom  mon  dow  comando`
    - Minuto (`0–59`), Hora (`0–23`), Día del mes (`1–31`), Mes (`1–12`), Día de semana (`0–7`, `0` y `7` = domingo).
    - Ejemplos clave: `0 2 * * *` (todos los días a las 02:00), `*/15 * * * 1-5` (cada 15 min de lunes a viernes), `@reboot` (al arrancar).
  - **`at`** (`at 23:00`): Programación puntual (*one-shot*) de una tarea futura.
  - **`systemd timers` (`.timer` + `.service`):** Reemplazo moderno en Ubuntu/MAX (`systemctl list-timers --all`), ofrece logs integrados en `journalctl` y opción `Persistent=true` si el PC estaba apagado a la hora programada.
- **Windows — Programador de tareas (*Task Scheduler*):**
  - Interfaz gráfica **`taskschd.msc`** (Desencadenadores: por horario, al iniciar sesión, al arrancar o por evento del Visor de Eventos).
  - Consola clásica **`schtasks`** (`schtasks /create /tn "BackupDAM" /tr "C:\scripts\backup.bat" /sc daily /st 22:00`).
  - PowerShell moderno: `New-ScheduledTaskAction`, `New-ScheduledTaskTrigger`, `Register-ScheduledTask`.
