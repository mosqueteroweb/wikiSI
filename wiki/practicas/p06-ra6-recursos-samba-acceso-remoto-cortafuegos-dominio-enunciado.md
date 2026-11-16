---
ra: RA6
ce:
  - RA6.a
  - RA6.b
  - RA6.c
  - RA6.d
  - RA6.e
  - RA6.f
  - RA6.g
tipo: practica
publicar: true
fuentes:
  - raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md
  - raw/procesados/ra6-acceso-remoto-cortafuegos-seguridad-red.md
  - raw/procesados/ra6-dominios-active-directory-ldap-integracion.md
ultima_revision: "2026-11-15"
---

# p06 · Servidores Compartidos, Acceso Remoto, Cortafuegos y Dominio Samba AD (`RA6.a`–`RA6.g`)

<!-- fuente: raw/procesados/ra6-recursos-compartidos-permisos-red-servidores.md -->

## Situación Profesional de Partida

La consultora **VegaSoft DAM** te encarga implantar su infraestructura interna sobre la red privada del laboratorio VirtualBox en un PC **MAX de 16 GB RAM**: un servidor Linux centralizará recursos compartidos multiplataforma (**Samba / SMB3**), cola de impresión (**CUPS**), servicio proxy web, administración remota segura (**SSH + túnel** / **RDP**), cortafuegos perimetral endurecido (**`ufw` + `fail2ban`**) y un **Controlador de Dominio Samba AD DC** al que se unirá el equipo cliente Windows 10.

> **Importante:** Por claridad pedagógica, si despliegas Samba en modo servidor de archivos clásico (`smbd`) vs Controlador de Dominio (`samba-ad-dc`), **haz una instantánea VirtualBox (*Snapshot*)** antes de ejecutar `samba-tool domain provision` (o ejecuta primero las Tareas 1–5 en `smbd` clásico y finalmente la Tarea 6 creando el Controlador de Dominio en la misma VM o tras revertir un snapshot).

## Topología VirtualBox y Presupuesto de RAM

| Máquina Virtual | Sistema Operativo | RAM asignada | Red VirtualBox | Función |
| :--- | :--- | :---: | :--- | :--- |
| **`DAM-Corp-Srv`** | Ubuntu Server 24.04 | **2 GB** | `intnet_corp` (`192.168.75.10/24`) [+ NAT temporal `apt`] | Samba/CUPS/Nginx/UFW/Fail2ban + Samba AD DC |
| **`DAM-Corp-Win10`** | Windows 10 Pro / Education | **4 GB** | `intnet_corp` (`192.168.75.20/24`, DNS `.10`) | Estación cliente mapeando recursos, RDP/SSH y unida al dominio |
| **Consumo total activo** | **2 VMs sobre MAX (16 GB)** | **6 GB** | Margen libre **10 GB** | Respeta el tope de aula (≤ 10–12 GB) |

---

## Tareas Evaluables (`RA6.a` – `RA6.g`)

### Tarea 1 · Compartición Samba y Permisos Efectivos (`RA6.a`, `RA6.b`, `RA6.c`)

1. En **`DAM-Corp-Srv`**, crea el grupo `vega_devs` y los usuarios `mario.dev` (en `vega_devs`) y `sara.ro` (fuera de `vega_devs`), habilitando ambos en Samba (`smbpasswd -a`).
2. Crea `/srv/vega_datos` propiedad `root:vega_devs` con permisos **`2770`** y lectura POSIX ACL para `sara.ro`.
3. Publica el recurso `[VegaRepo]` en `/etc/samba/smb.conf` permitiendo escritura solo a `@vega_devs` y lectura a `sara.ro`, valida con `testparm -s`, reinicia `smbd` y comprueba desde **`DAM-Corp-Win10`** mapeando `Z:` (`net use`) qué sucede al escribir como `mario.dev` frente a `sara.ro`.

### Tarea 2 · Servidor de Impresión CUPS y Proxy de Aplicaciones (`RA6.c`)

1. Instala `cups` y `printer-driver-cups-pdf` en **`DAM-Corp-Srv`**, verifica la cola virtual con `lpstat -p -d` y envía una impresión de prueba por consola (`lp -d PDF`).
2. Levanta un servidor web backend en `127.0.0.1:8085` y publícalo mediante **Nginx** como proxy inverso en el puerto `80`, demostrando que `80` responde desde Windows pero `8085` permanece oculto a la red.

### Tarea 3 · Administración y Escritorio Remoto Seguro (`RA6.d`)

1. En **`DAM-Corp-Win10`**, activa Escritorio Remoto (**RDP `3389/TCP`**) exigiendo **NLA (`UserAuthentication=1`)** y comprueba su escucha.
2. En **`DAM-Corp-Win10`**, abre un **túnel SSH local (`ssh -N -L 9085:127.0.0.1:8085`)** contra **`DAM-Corp-Srv`** para alcanzar de forma cifrada el servicio backend `8085` directamente por `http://localhost:9085`.

### Tarea 4 · Cortafuegos de Host y Protección de Recursos (`RA6.e`, `RA6.f`)

1. Activa **`ufw`** en **`DAM-Corp-Srv`** con política `default deny incoming`, `limit ssh`, permiso `80/TCP` LAN y permiso **`445/TCP` restringido únicamente a `192.168.75.0/24`**.
2. En **`DAM-Corp-Win10`**, habilita todos los perfiles de **Windows Defender Firewall**, cambia la red `intnet_corp` al perfil **Privado** y crea una regla que permita TCP `3389` solo desde `192.168.75.0/24`.

### Tarea 5 · Defensa Activa (`fail2ban`) y Auditoría Básica (`RA6.e`, `RA6.f`)

1. Instala **`fail2ban`** y **`lynis`** en **`DAM-Corp-Srv`**. Configura `/etc/fail2ban/jail.local` con `backend = systemd` y `maxretry = 3` para `sshd`. Verifica `fail2ban-client status sshd` y ejecuta `sudo lynis audit system --quick`.
2. En Windows, comprueba que **Microsoft Defender** tiene protección en tiempo real habilitada (`Get-MpComputerStatus`).

### Tarea 6 · Dominio Samba AD DC, Unidades Organizativas y Unión de Cliente (`RA6.b`, `RA6.g`)

1. **Snapshot recomendado antes de este paso:** Provisiona un dominio **`vega.local`** (`CORP: VEGA`) en **`DAM-Corp-Srv`** (deshabilitando `systemd-resolved`, `smbd`, `nmbd` previos y arrancando `samba-ad-dc`).
2. Crea la Unidad Organizativa **`OU=Ingenieria`**, el grupo `g_ingenieros` y el usuario **`elena.corp`** dentro de esa OU con `samba-tool`.
3. Apunta el DNS de **`DAM-Corp-Win10`** exactamente a **`192.168.75.10`**, verifica los registros SRV (`Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.vega.local`), une Windows al dominio `vega.local` con `Add-Computer` e inicia sesión tras el reinicio como `VEGA\elena.corp`.

---

## Entregables y Criterios de Evaluación

Entrega un dosier (`Apellido_Nombre_p06_RA6.pdf` / `.md`) con evidencias de terminal y capturas de las 6 tareas, destacando la verificación negativa de permisos efectivos SMB, las reglas UFW/Defender, la salida de `fail2ban`/`lynis` y el inicio de sesión exitoso en el dominio `VEGA`.

| Bloque evaluado | Criterios cubiertos | Peso |
| :--- | :---: | :---: |
| Permisos efectivos de red (`SMB3`) y compartición Samba | `RA6.a`, `RA6.b`, `RA6.c` | **25 %** |
| Impresión CUPS, Nginx proxy inverso y acceso remoto (`RDP NLA` / Túnel SSH) | `RA6.c`, `RA6.d` | **20 %** |
| Cortafuegos (`ufw` / Defender), `fail2ban` y auditoría de seguridad | `RA6.e`, `RA6.f` | **25 %** |
| Dominio Samba AD DC, OUs, DNS SRV y unión del cliente Windows | `RA6.b`, `RA6.g` | **30 %** |

## Recursos de Apoyo

- [Conceptos del bloque RA6](../ra/RA6.md#conceptos-teoricos)
- [Ejercicios resueltos e26–e30](../ra/RA6.md#ejercicios-practicos-resueltos)
- Vídeos de repaso: [Samba SMB y Active Directory](https://www.youtube.com/watch?v=ayaI9WNiFXA) · [Acceso remoto y cortafuegos](https://www.youtube.com/watch?v=S-2TIRnsioM)
