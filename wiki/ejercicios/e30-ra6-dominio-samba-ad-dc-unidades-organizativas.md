---
ra: RA6
ce:
  - RA6.b
  - RA6.g
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra6-dominios-active-directory-ldap-integracion.md
ultima_revision: "2026-11-15"
---

# e30 · Implantación de Dominio con Samba AD DC, Unidades Organizativas (`OU`) y Unión de Cliente Windows 10

<!-- fuente: raw/procesados/ra6-dominios-active-directory-ldap-integracion.md -->

## Escenario y Topología VirtualBox

Pasaremos de un entorno aislado en grupo de trabajo a un **Dominio Active Directory real** utilizando **Samba 4 AD DC** sobre una VM Ubuntu Server ligera (`2 GB RAM`) en **Red Interna `intnet_ad`**, uniendo al dominio un equipo cliente **Windows 10 Pro/Education** (`4 GB RAM`) para comprobar inicio de sesión centralizado, resolución DNS SRV y organización por Unidades Organizativas (`OU`).

| Máquina Virtual | Sistema Operativo | RAM asignada | Adaptador / IP (`intnet_ad`) | Rol |
| :--- | :--- | :---: | :--- | :--- |
| **`e30-Ubuntu-DC`** | Ubuntu Server 24.04 | **2 GB** | `192.168.70.10/24` (DNS propio Samba) | Controlador de Dominio **`corp.dam.local`** |
| **`e30-Win10-Domain`** | Windows 10 Pro / Education | **4 GB** | `192.168.70.20/24` (DNS: `192.168.70.10`) | Estación de trabajo unida al dominio |
| **Total activo** | **2 VMs simultáneas** | **6 GB** | Máximo recomendado en **MAX 16 GB** | Nota: requiere **Win10 Pro/Edu** (Home no une dominios) |

## Objetivos

1. Comprender los requisitos previos críticos de un dominio AD: **hostname FQDN fijo**, **IP estática**, **puerto `53` libre** para el DNS interno del controlador y **sincronización horaria**.
2. Provisionar un controlador Samba AD DC (`samba-tool domain provision`), crear una Unidad Organizativa **`OU=Desarrollo`** y un usuario corporativo **`laura.dev`**.
3. Configurar el DNS del cliente Windows apuntando al DC, comprobar los registros **SRV `_ldap._tcp` y `_kerberos._tcp`** y unir la estación al dominio.

---

## Enunciado Detallado

1. **Preparación de `e30-Ubuntu-DC` (2 GB RAM):**
   - Asigna hostname `dc1.corp.dam.local` (`hostnamectl set-hostname dc1.corp.dam.local`) y añade `192.168.70.10 dc1.corp.dam.local dc1` en `/etc/hosts`.
   - Configura Netplan en `intnet_ad` con IP `192.168.70.10/24` y DNS `127.0.0.1` (desactivando `systemd-resolved` para dejar libre el puerto `53` al DNS interno de Samba).

2. **Provisionado del dominio `corp.dam.local` y objetos LDAP (`RA6.g`):**
   - Instala `samba`, `krb5-user` y `winbind` (con paquete de utilidades Samba AD).
   - Elimina `/etc/samba/smb.conf` previo y ejecuta `samba-tool domain provision --use-rfc2307 --realm=CORP.DAM.LOCAL --domain=CORP --adminpass='AdminDam#2026!' --dns-backend=SAMBA_INTERNAL`.
   - Desenmascara y arranca el servicio `samba-ad-dc`.
   - Crea la Unidad Organizativa `OU=Desarrollo` y el usuario `laura.dev` dentro de esa OU.

3. **Unión del cliente `e30-Win10-Domain` (4 GB RAM) (`RA6.b`, `RA6.g`):**
   - Fija en Windows IP `192.168.70.20/24` y **DNS primario obligatoriamente `192.168.70.10`**.
   - Verifica la resolución de registros SRV con `Resolve-DnsName` y une la máquina al dominio `corp.dam.local` con `Add-Computer`. Reinicia e inicia sesión en Windows como `CORP\laura.dev`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Preparación de red y DNS en `e30-Ubuntu-DC`

    === "MAX / Ubuntu (Linux)"

        ```bash
        # 1. Fijar FQDN y archivo /etc/hosts
        sudo hostnamectl set-hostname dc1.corp.dam.local
        echo "192.168.70.10 dc1.corp.dam.local dc1" | sudo tee -a /etc/hosts

        # 2. Instalar paquetes necesarios (temporalmente mientras tenga NAT para apt)
        sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y samba krb5-user winbind smbclient dnsutils

        # 3. Liberar el puerto 53 que ocupa systemd-resolved
        sudo systemctl disable --now systemd-resolved
        sudo rm -f /etc/resolv.conf
        printf "nameserver 127.0.0.1\nsearch corp.dam.local\n" | sudo tee /etc/resolv.conf

        # 4. Provisionar dominio limpio
        sudo systemctl stop smbd nmbd winbind 2>/dev/null || true
        sudo systemctl disable smbd nmbd winbind 2>/dev/null || true
        sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.orig 2>/dev/null || true

        sudo samba-tool domain provision \
          --use-rfc2307 \
          --realm=CORP.DAM.LOCAL \
          --domain=CORP \
          --server-role=dc \
          --dns-backend=SAMBA_INTERNAL \
          --adminpass='AdminDam#2026!'

        # Copiar configuración Kerberos generada por Samba y arrancar samba-ad-dc
        sudo cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
        sudo systemctl unmask samba-ad-dc
        sudo systemctl enable --now samba-ad-dc
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobar previamente que la edición es Pro o Education (Windows Home no puede unirse a dominios)
        (Get-WmiObject Win32_OperatingSystem).Caption
        ```

    ### 2. Creación de Unidad Organizativa (`OU`) y usuario corporativo (`RA6.g`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Verificar registros DNS SRV generados por el propio DC
        host -t SRV _ldap._tcp.corp.dam.local
        host -t SRV _kerberos._tcp.corp.dam.local

        # Crear OU=Desarrollo, grupo global y usuario dentro de la OU
        sudo samba-tool ou create "OU=Desarrollo"
        sudo samba-tool user create laura.dev 'LauraDam#2026!' \
          --userou="OU=Desarrollo" --given-name="Laura" --surname="Dev"
        sudo samba-tool group add dev_corp
        sudo samba-tool group addmembers dev_corp laura.dev

        # Comprobar listado de usuarios y OU en LDAP
        sudo samba-tool user list
        ```

    === "Windows 10 / 11"

        ```powershell
        # Ejecutar PowerShell como Administrador en e30-Win10-Domain:
        # 1. Configurar IP estática y APUNTAR DNS EXACTAMENTE al Controlador de Dominio (192.168.70.10)
        Remove-NetIPAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4 -Confirm:$false -ErrorAction SilentlyContinue
        New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.70.20 -PrefixLength 24
        Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("192.168.70.10")

        # 2. Comprobar que resuelve SRV de Active Directory
        Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.corp.dam.local

        # 3. Unir el cliente al dominio (introducir usuario CORP\Administrator y AdminDam#2026!)
        Add-Computer -DomainName "corp.dam.local" -Restart
        ```

---

## Puntos de Control y Errores Frecuentes

- **Error `No se pudo contactar con ningún controlador de dominio AD` en Windows:** En el 95 % de los casos ocurre porque Windows conserva `8.8.8.8` o `1.1.1.1` como DNS primario/secundario en lugar de tener **únicamente** la IP del DC (`192.168.70.10`) configurada.
- **Error de fecha/hora Kerberos:** Si la VM Windows tiene desfasado el reloj más de 5 minutos respecto al controlador Ubuntu, la autenticación Kerberos fallará aunque la contraseña sea correcta.
- **Edición Windows Home:** Windows 10/11 **Home** carece por licencia de soporte para unión a dominios Active Directory. Para la práctica debes usar la ISO de **Windows 10/11 Pro o Education**.

## Recursos para Profundizar

- Concepto asociado: [Implantación y Explotación de Dominios (Active Directory / Samba AD DC)](../conceptos/ra6-implantacion-explotacion-dominios-ad-samba-dc.md).
- Vídeo recomendado sobre Samba y Active Directory: [Samba SMB y Controlador de Dominio AD (YouTube)](https://www.youtube.com/watch?v=ayaI9WNiFXA).
