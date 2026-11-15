---
title: "Conceptos Teóricos"
tipo: "indice"
publicar: true
ultima_revision: "2026-11-15"
---

# Conceptos Teóricos

Páginas de referencia teórica del módulo **Sistemas Informáticos (0483)**. Cada tema sigue unos criterios estrictos de calidad y trazabilidad:

1. **Trazabilidad curricular:** Enlazado a su Resultado de Aprendizaje (`RA`) y Criterios de Evaluación (`CE`) concretos.
2. **Enfoque dual:** Comparativa técnica entre sistemas libres (Linux/MAX/Ubuntu/Mint/Puppy) y propietarios (Windows 10/11) cuando corresponde.
3. **Soporte visual obligatorio:** Diagramas editables en Mermaid/SVG e ilustraciones conceptuales almacenadas localmente en `wiki/assets/`.
4. **Credibilidad y ampliación:** Fuentes verificadas de Nivel 1 y Nivel 2, más una sección final de **Recursos para profundizar** (documentación oficial y vídeos explicativos).

---

## RA1 · Evaluación de Sistemas Informáticos (Completado ✅)

1. [Arquitectura de Von Neumann, Placa Base y CPU](ra1-arquitectura-placa-base-cpu.md) (`RA1.a`)
2. [Jerarquía de Memorias y Tipos de Memoria](ra1-jerarquia-tipos-memoria.md) (`RA1.b`)
3. [Puesta en Marcha del Equipo: POST, BIOS Legacy y UEFI](ra1-puesta-en-marcha-bios-uefi.md) (`RA1.c`)
4. [Periféricos, Interfaces de Entrada/Salida y Buses](ra1-perifericos-interfaces-buses.md) (`RA1.a`, `RA1.d`)
5. [Redes, Componentes, Cableado y Mapas Físico y Lógico](ra1-redes-componentes-topologias-mapas.md) (`RA1.e`, `RA1.f`, `RA1.g`)
6. [Normas de Seguridad y Prevención de Riesgos Laborales (PRL)](ra1-seguridad-prevencion-riesgos-prl.md) (`RA1.h`)

---

## RA2 · Instalación y Virtualización de Sistemas Operativos (Completado ✅)

1. [Arquitectura, Elementos Funcionales y Clasificación de Sistemas Operativos](ra2-arquitectura-funciones-sistema-operativo.md) (`RA2.a`, `RA2.b`)
2. [Comparativa de Sistemas Operativos, Requisitos y Licencias](ra2-comparativa-so-licencias.md) (`RA2.c`)
3. [Tecnologías de Virtualización y Laboratorio VirtualBox en MAX](ra2-virtualizacion-virtualbox-max.md) (`RA2.d`, `RA2.g`)
4. [Planificación, Particionado GPT/UEFI e Instalación Dual-Boot](ra2-planificacion-instalacion-dual-boot.md) (`RA2.d`, `RA2.e`, `RA2.i`)
5. [Gestores de Arranque: GRUB2, Windows BCD y Reparación](ra2-gestores-arranque-grub-bcd.md) (`RA2.e`, `RA2.f`)
6. [Gestión de Aplicaciones, Actualización y Recuperación del Sistema](ra2-gestion-aplicaciones-actualizacion-recuperacion.md) (`RA2.f`, `RA2.h`, `RA2.i`)

---

## RA3 · Gestión de la Información, Almacenamiento y Backups (Completado ✅)

1. [Sistemas de Archivos: Anatomía y Comparativa Técnica](ra3-sistemas-archivos-anatomia-comparativa.md) (`RA3.a`)
2. [Estructura y Función de los Directorios: FHS Linux vs. Windows](ra3-estructura-directorios-fhs-windows.md) (`RA3.b`, `RA3.c`)
3. [Búsqueda, Localización de Información e Inventario de Software](ra3-busqueda-localizacion-informacion.md) (`RA3.d`, `RA3.h`)
4. [Administración de Discos, Particiones, LVM y Matrices RAID](ra3-particiones-lvm-raid-administracion-discos.md) (`RA3.e`, `RA3.h`)
5. [Diagnóstico, Chequeo, TRIM vs. Desfragmentación y Cifrado de Discos](ra3-chequeo-desfragmentacion-cifrado-discos.md) (`RA3.e`, `RA3.h`)
6. [Copias de Seguridad, Clonación y Automatización de Tareas](ra3-copias-seguridad-clonacion-tareas-programadas.md) (`RA3.f`, `RA3.g`, `RA3.h`)

## RA4 · Administración de Usuarios, Permisos, Procesos, Monitorización y Desarrollo (Completado ✅)

1. [Administración de Usuarios y Grupos Locales](ra4-administracion-usuarios-grupos-locales.md) (`RA4.a`, `RA4.e`)
2. [Directivas de Cuenta, Contraseñas y Delegación `sudo`](ra4-directivas-cuenta-politicas-contrasenas-sudo.md) (`RA4.b`, `RA4.e`)
3. [Permisos Locales, Bits Especiales (`SUID`/`SGID`/`Sticky`) y ACLs (`setfacl`/`icacls`)](ra4-permisos-locales-bits-especiales-acls.md) (`RA4.d`, `RA4.e`)
4. [Gestión de Procesos, Señales y Servicios (`systemd` y Windows)](ra4-gestion-procesos-servicios-systemd-windows.md) (`RA4.c`, `RA4.e`)
5. [Comandos de Administración, Variables de Entorno y Scripting](ra4-comandos-administracion-variables-scripting.md) (`RA4.e`, `RA4.h`)
6. [Monitorización, Registros (`journalctl`/Eventos) y Dimensionamiento para Desarrollo DAM](ra4-monitorizacion-logs-optimizacion-entorno-dam.md) (`RA4.f`, `RA4.g`, `RA4.h`)

## RA5 · Interconexión de Sistemas en Red y Protocolos Seguros (Completado ✅)

1. [Arquitectura TCP/IP, Direccionamiento IPv4/IPv6 y Subredes (CIDR/VLSM)](ra5-arquitectura-tcpip-direccionamiento-ipv4-ipv6.md) (`RA5.a`)
2. [Configuración de Red en Clientes: Netplan, NetworkManager, PowerShell y VirtualBox](ra5-configuracion-red-clientes-netplan-powershell.md) (`RA5.a`, `RA5.b`)
3. [Redes LAN Cableadas (`802.3`) e Inalámbricas (`802.11` / Wi-Fi Segura)](ra5-redes-lan-cableadas-inalambricas-wifi-seguridad.md) (`RA5.b`, `RA5.c`)
4. [Dispositivos de Interconexión, VLANs (`802.1Q`), NAT y Acceso WAN](ra5-interconexion-enrutamiento-nat-acceso-wan.md) (`RA5.d`, `RA5.e`)
5. [Gestión de Puertos y Diagnóstico Sistemático de Red (*Bottom-Up*)](ra5-gestion-puertos-herramientas-diagnostico-red.md) (`RA5.f`, `RA5.g`)
6. [Protocolos Seguros de Comunicaciones: TLS, SSH, SFTP y VPN](ra5-protocolos-seguros-comunicaciones-tls-ssh-vpn.md) (`RA5.h`, `RA5.f`)

## Próximos Bloques Planificados

- **[RA6 · Operación de sistemas en red, servicios y dominios](../ra/RA6.md)**
- **[RA7 · Documentación técnica y utilidades de propósito general](../ra/RA7.md)**
