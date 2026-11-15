---
ra: RA5
ce:
  - RA5.a
tipo: ejercicio
publicar: true
fuentes:
  - raw/procesados/ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md
ultima_revision: "2026-11-15"
---

# e21 · Cálculo de Subredes IPv4, Planificación VLSM y Compresión IPv6

<!-- fuente: raw/procesados/ra5-tcpip-direccionamiento-ipv4-ipv6-subredes.md -->

## Escenario y Topología VirtualBox

Un centro educativo recibe el bloque privado **`172.16.40.0/23`** (`512` direcciones totales) para segmentar cuatro redes del departamento de Informática evitando desperdiciar direcciones IP y comprobando el plan mediante cálculo manual y utilidades de Linux.

| Máquina Virtual | Sistema Operativo | RAM asignada | Rol en el ejercicio |
| :--- | :--- | :---: | :--- |
| **`e21-Ubuntu`** | Ubuntu Server / Desktop 24.04 | **2 GB** | Validación matemática con `ipcalc` y módulo `ipaddress` de Python |
| **Total activo** | **1 VM ligera** | **2 GB** | Amplio margen sobre equipo **MAX (16 GB)** |

## Objetivos

1. Diseñar un direccionamiento **VLSM** sin solapamientos sobre **`172.16.40.0/23`** para 4 subredes de distintos tamaños.
2. Comprobar automáticamente los rangos calculados con `ipcalc` y Python (`ipaddress`).
3. Comprimir y expandir direcciones **IPv6** aplicando las reglas oficiales RFC 5952.

---

## Enunciado Detallado

1. **Planificación VLSM (`RA5.a`):** Partiendo del prefijo **`172.16.40.0/23`** (`172.16.40.0` – `172.16.41.255`), asigna subredes continuas sin huecos ni solapamientos para cubrir estas demandas:
   - **Red Aulas DAM:** **200 hosts** útiles.
   - **Red Servidores CPD:** **55 hosts** útiles.
   - **Red Invitados Wi-Fi:** **28 hosts** útiles.
   - **Enlace Router-ISP:** **2 hosts** útiles.
   Para cada subred indica: Dirección de red, CIDR, Máscara decimal, Primer host, Último host y Broadcast.

2. **Comprobación automática (`RA5.a`):** Usa `ipcalc` o un breve script con la librería estándar `ipaddress` de Python en **`e21-Ubuntu`** para verificar que ninguna subred se solapa.

3. **Compresión y clasificación IPv6 (`RA5.a`):**
   - Comprime al formato mínimo estándar RFC 5952 la dirección `2001:0db8:0000:0000:0a10:0000:0000:004f`.
   - Indica el tipo de cada prefijo: `fe80::1`, `fd12:3456:789a::10`, `2001:db8::1` y `::1`.

---

## Resolución Guiada

??? success "Ver resolución paso a paso"

    ### 1. Tabla VLSM ordenada de mayor a menor demanda

    Orden correcto por tamaño: **200 → 55 → 28 → 2** hosts.

    | Subred | Demanda | Potencia necesaria ($2^h - 2 \ge$) | Prefijo / Máscara | Red | Rango útil | Broadcast |
    | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
    | **Aulas DAM** | 200 | $2^8 - 2 = 254$ ($h=8$) | **`/24`** (`255.255.255.0`) | `172.16.40.0/24` | `.40.1` – `.40.254` | `172.16.40.255` |
    | **Servidores CPD** | 55 | $2^6 - 2 = 62$ ($h=6$) | **`/26`** (`255.255.255.192`) | `172.16.41.0/26` | `.41.1` – `.41.62` | `172.16.41.63` |
    | **Invitados Wi-Fi** | 28 | $2^5 - 2 = 30$ ($h=5$) | **`/27`** (`255.255.255.224`) | `172.16.41.64/27` | `.41.65` – `.41.94` | `172.16.41.95` |
    | **Enlace Router** | 2 | $2^2 - 2 = 2$ ($h=2$) | **`/30`** (`255.255.255.252`) | `172.16.41.96/30` | `.41.97` – `.41.98` | `172.16.41.99` |

    Queda libre sin asignar el resto del bloque desde `172.16.41.100` hasta `172.16.41.255`.

    ### 2. Verificación en terminal Linux (`e21-Ubuntu`)

    === "MAX / Ubuntu (Linux)"

        ```bash
        # Instalar ipcalc para comprobaciones visuales rápidas
        sudo apt-get update && sudo apt-get install -y ipcalc
        ipcalc 172.16.41.64/27

        # Validación programática de no solapamiento con Python 3
        python3 - <<'EOF'
        import ipaddress
        base = ipaddress.ip_network("172.16.40.0/23")
        redes = [
            ipaddress.ip_network("172.16.40.0/24"),
            ipaddress.ip_network("172.16.41.0/26"),
            ipaddress.ip_network("172.16.41.64/27"),
            ipaddress.ip_network("172.16.41.96/30"),
        ]
        for i, r in enumerate(redes):
            assert r.subnet_of(base), f"{r} fuera de bloque base"
            for j in range(i + 1, len(redes)):
                assert not r.overlaps(redes[j]), f"Solapamiento entre {r} y {redes[j]}"
            hosts = list(r.hosts())
            print(f"{str(r):18} -> utiles={len(hosts):3} | rango={hosts[0]}..{hosts[-1]} | bc={r.broadcast_address}")
        print("OK: Plan VLSM libre de solapamientos.")
        EOF
        ```

    === "Windows 10 / 11"

        ```powershell
        # Comprobación equivalente desde PowerShell (si Python está instalado) o cálculo CIDR
        python -c "import ipaddress; r=ipaddress.ip_network('172.16.41.64/27'); print(r.network_address, r.broadcast_address, r.num_addresses-2)"
        ```

    ### 3. Compresión y clasificación IPv6 (`RA5.a`)

    - Dirección dada: `2001:0db8:0000:0000:0a10:0000:0000:004f`
      1. Quitamos ceros a la izquierda por hexteto: `2001:db8:0:0:a10:0:0:4f`.
      2. Ambos grupos tienen la misma longitud (dos bloques de ceros); según **RFC 5952**, cuando hay empate se comprime el **bloque situado más a la izquierda**: **`2001:db8::a10:0:0:4f`**. (En todo caso, `::` nunca puede aparecer dos veces).
    - Clasificación:
      - `fe80::1`: **Link-Local** (solo válida en el enlace local L2).
      - `fd12:3456:789a::10`: **Unique Local Address (ULA)** (`fc00::/7`, direccionamiento interno privado).
      - `2001:db8::1`: **Global Unicast** (`2000::/3`, subrango reservado oficialmente para documentación RFC 3849).
      - `::1`: **Loopback IPv6**.

---

## Puntos de Control y Errores Frecuentes

- **No ordenar de mayor a menor:** Si asignas `/30` al principio y luego un `/24`, tendrás que alinear el `/24` dejando un agujero enorme de direcciones inutilizadas o producirás un solapamiento ilegal.
- **Doble `::` en IPv6:** Escribir `2001:db8::a10::4f` es sintácticamente inválido porque un parser no podría saber cuántos bloques de `0000` representó cada `::`.

## Recursos para Profundizar

- Concepto asociado: [Arquitectura TCP/IP y Direccionamiento IPv4/IPv6](../conceptos/ra5-arquitectura-tcpip-direccionamiento-ipv4-ipv6.md).
- Vídeo recomendado sobre Subnetting y VLSM: [Subnetting IPv4 y VLSM paso a paso (YouTube)](https://www.youtube.com/watch?v=BvyLZX9tSvA).
