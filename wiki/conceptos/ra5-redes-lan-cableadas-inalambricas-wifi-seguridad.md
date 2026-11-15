---
ra: RA5
ce:
  - RA5.b
  - RA5.c
tipo: concepto
publicar: true
fuentes:
  - raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md
ultima_revision: "2026-11-15"
---

# Redes de Área Local Cableadas (`802.3`) e Inalámbricas (`802.11` / Wi-Fi)

<!-- fuente: raw/procesados/ra5-lan-cableada-inalambrica-enrutamiento-wan.md -->

## 1. Redes LAN Cableadas (`IEEE 802.3`) y Cableado Estructurado

Las redes cableadas proporcionan latencia predecible, inmunidad electromagnética superior y ancho de banda simétrico dedicado:

| Medio / Categoría | Velocidad típica | Alcance estándar | Aplicación habitual en aula / empresa |
| :--- | :---: | :---: | :--- |
| **UTP Cat 5e** | 1 Gbps (1000BASE-T) | 100 m | Puestos heredados; no recomendado en instalaciones nuevas |
| **UTP/STP Cat 6** | 1 Gbps / 10 Gbps | 100 m (1G) / 55 m (10G) | Estándar mínimo en aulas técnicas y oficinas modernas |
| **Cat 6A** | 10 Gbps (10GBASE-T) | 100 m | Enlaces horizontales críticos, puntos de acceso Wi-Fi 6/7 |
| **Fibra Multimodo (OM3/OM4)** | 10 / 40 / 100 Gbps | 300–550 m | Troncales verticales entre racks de un mismo edificio |
| **Fibra Monomodo (OS2)** | 10 / 100+ Gbps | Varios km | Enlace entre edificios y acometida FTTH hacia operador |

- **Norma de crimpado RJ-45 (`T568B`):** ambos extremos del latiguillo directo siguen el mismo orden (`Naranja-Blanco, Naranja, Verde-Blanco, Azul, Azul-Blanco, Verde, Marrón-Blanco, Marrón`); hoy todos los switches Gigabit soportan **Auto-MDI-X**, eliminando la necesidad de cables cruzados manuales.
- **Full-Duplex:** permite transmitir y recibir simultáneamente sin colisiones (CSMA/CD queda prácticamente obsoleto en enlaces conmutados modernos).

---

## 2. Redes LAN Inalámbricas (`IEEE 802.11` / Wi-Fi)

A diferencia del cable, el medio inalámbrico es **compartido (*half-duplex* en un mismo canal)** y utiliza **CSMA/CA** (*Carrier Sense Multiple Access with Collision Avoidance*) para evitar interferencias entre dispositivos.

| Generación | Estándar | Bandas | Anchos de canal | Características clave |
| :--- | :--- | :---: | :---: | :--- |
| **Wi-Fi 5** | `802.11ac` | 5 GHz | 20–160 MHz | MU-MIMO en bajada |
| **Wi-Fi 6 / 6E** | `802.11ax` | 2,4 / 5 / **6 GHz** | 20–160 MHz | **OFDMA**, TWT (ahorro energético) y alta densidad de aula |
| **Wi-Fi 7** | `802.11be` | 2,4 / 5 / 6 GHz | Hasta 320 MHz | Multi-Link Operation (MLO), latencia ultrabaja |

### Planificación de Canales y Seguridad Wi-Fi

- **Banda 2,4 GHz:** penetra mejor paredes, pero solo ofrece **3 canales que no se solapan entre sí en 20 MHz: `1`, `6` y `11`**.
- **Banda 5 GHz y 6 GHz:** canales no solapados mucho más numerosos, menor interferencia y tasas muy superiores en espacios abiertos o aulas.
- **Cifrado y autenticación:**
  - **Estándar actual recomendado:** **WPA3-Personal (SAE)** (protegido frente a ataques de diccionario offline) o **WPA3-Enterprise (`802.1X` + servidor RADIUS)** en campus/empresas.
  - **Compatible aceptable:** **WPA2-PSK (AES/CCMP)**.
  - **Prohibidos por vulnerabilidad grave:** **WEP**, **WPA-TKIP** y **WPS por PIN**.

---

## 3. Gestión de Redes Cableadas e Inalámbricas por Consola

=== "MAX / Ubuntu (Linux)"

    ```bash
    # Inspeccionar velocidad negociada y enlace físico en tarjeta cableada (Cableada)
    ethtool enp0s3 2>/dev/null | grep -E "Speed|Duplex|Link detected"
    nmcli device status

    # Escanear puntos de acceso Wi-Fi, ver canal, señal y seguridad
    nmcli device wifi list

    # Conectarse a un SSID protegido desde terminal
    nmcli device wifi connect "AulaDAM-5G" password "ClaveSegura"
    ```

=== "Windows 10 / 11"

    ```powershell
    # Comprobar velocidad negociada del adaptador Ethernet o Wi-Fi
    Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MacAddress

    # Inspeccionar señal, canal y protocolo Wi-Fi conectado
    netsh wlan show interfaces

    # Listar perfiles Wi-Fi guardados y exportar/revisar estado
    netsh wlan show profiles
    ```

---

## Recursos para profundizar

- Concepto siguiente: [Dispositivos de Interconexión, VLANs, Enrutamiento y Acceso WAN](ra5-interconexion-enrutamiento-nat-acceso-wan.md).
- Estándar Wi-Fi Alliance: [Wi-Fi CERTIFIED WPA3](https://www.wi-fi.org/discover-wi-fi/security).
- Vídeo recomendado sobre configuración de redes y protocolos: [Configuración TCP/IP, LAN y protocolos en consola (YouTube)](https://www.youtube.com/watch?v=-c_o8nOavo4).
