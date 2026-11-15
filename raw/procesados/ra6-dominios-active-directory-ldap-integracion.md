---
tema: "Administración de Dominios, Directorios Activos (AD DS / Samba AD DC), LDAP, Unidades Organizativas y GPO"
ra: RA6
ce:
  - RA6.b
  - RA6.g
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA6 (3/3) · Dominios, Active Directory y LDAP

## 1. Grupo de Trabajo (*Workgroup*) vs. Dominio Centralizado (`RA6.g`)

- **Grupo de trabajo (*Workgroup*):** cada equipo mantiene su propia base local de usuarios (`/etc/shadow` o SAM local), requiere duplicar cuentas y políticas en cada PC; solo viable hasta ~10 equipos.
- **Dominio (*Domain* / Active Directory / Samba AD DC):** base de datos jerárquica centralizada y replicable gestionada por uno o varios **Controladores de Dominio (DC)**:
  - **Autenticación única (SSO) con Kerberos (`88/TCP+UDP`):** emite *tickets* cifrados dependientes de hora sincronizada (**NTP**, `123/UDP` máximo 5 minutos de desfase).
  - **Directorio LDAP (`389/TCP`, LDAPS `636/TCP`):** almacena objetos organizados jerárquicamente (**Dominio → Unidades Organizativas `OU` → Usuarios, Grupos y Equipos**).
  - **DNS integrado obligatorio (`53/TCP+UDP`):** utiliza registros **SRV** (`_ldap._tcp`, `_kerberos._tcp`) para localizar los controladores de dominio. Sin DNS apuntando al DC no funciona la unión ni el inicio de sesión en dominio.
  - **Sysvol (`SMB 445/TCP`):** almacena scripts de inicio y **Directivas de Grupo (GPO)**.

## 2. Derechos de Usuario, Grupos de Seguridad y Directivas de Grupo (`RA6.b`, `RA6.g`)

- **Modelo AGDLP en dominios:** Cuentas (*Accounts*) → Grupos **Globales** (por departamento/rol) → Grupos **Locales de Dominio** (por recurso) → Permisos (**Permissions** sobre carpetas/impresoras).
- **Directivas de Grupo (GPO / Group Policy):**
  - Se vinculan al nivel **Sitio, Dominio o Unidad Organizativa (`OU`)** siguiendo orden de precedencia **LSDOU** (*Local → Site → Domain → OU*), separando **Configuración de equipo** y **Configuración de usuario**.
  - Permiten desplegar bloqueo de pantalla, complejidad de contraseñas única, mapeo automático de unidades de red, restricciones de USB o políticas de Firewall Windows de forma masiva.

## 3. Implantación Ligera en Aula VirtualBox (Samba AD DC + Windows 10)

- En entornos educativos Linux con **2 GB RAM** (`e30-Ubuntu-DC`), **Samba 4** permite provisionar un Controlador de Dominio compatible con Active Directory real (`samba-tool domain provision --use-rfc2307`), crear OUs (`samba-tool ou create`), usuarios (`samba-tool user create`) y unir un cliente **Windows 10 Pro/Education** (`4 GB RAM`) apuntando su DNS principal hacia la IP del servidor Ubuntu.
- Para clientes Linux que quieran unirse a un dominio AD se utiliza **`sssd` + `realmd` (`realm join <dominio>`)** manteniendo autenticación centralizada Kerberos/LDAP.
