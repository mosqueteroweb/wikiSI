---
title: "e05 · Mapa Físico/Lógico de Red en VirtualBox y Checklist PRL"
ra: ["RA1"]
ce: ["RA1.e", "RA1.f", "RA1.g", "RA1.h"]
tipo: "ejercicio"
publicar: true
fuentes:
  - "raw/procesados/ra1-redes-fisica-topologias-prl.md"
ultima_revision: "2026-11-15"
---

# Ejercicio e05 · Mapa Físico/Lógico de Red en VirtualBox y Checklist PRL

> **Criterios de Evaluación:** `RA1.e`, `RA1.f`, `RA1.g` y `RA1.h` · **Conceptos previos:** [Redes, Componentes, Cableado y Mapas](../conceptos/ra1-redes-componentes-topologias-mapas.md) y [Seguridad y PRL](../conceptos/ra1-seguridad-prevencion-riesgos-prl.md)

## Objetivo

Montar un laboratorio ligero de dos nodos en **VirtualBox** sobre **MAX** usando **Puppy Linux** y **Ubuntu** en modo **Red Interna** (topología en estrella virtual), comprobar su enlace lógico, representar su **mapa físico y lógico** y auditar las condiciones **PRL / PVD** de tu propio puesto en el aula.

---

## Entorno y Presupuesto de RAM (Aula 16 GB)

| Equipo / VM | Rol | SO | RAM asignada | vCPUs | Adaptador de Red VirtualBox |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **PC Aula (Host)** | Anfitrión | MAX (Linux) | *(13 GB libres)* | Físicas | Puente / Red física aula |
| **`e05-Puppy`** | Nodo ligero A | **Puppy Linux** | **1024 MB (1 GB)** | 1 | **Red interna** (`red-e05`) |
| **`e05-Ubuntu`** | Nodo B | Ubuntu Desktop | **2048 MB (2 GB)** | 2 | **Red interna** (`red-e05`) |

> **Consumo total de VMs activas:** **3 GB** de 16 GB disponibles (excelente ejemplo de ahorro de memoria usando **Puppy Linux** en escenarios multi-VM).

---

## Enunciado

1. Inspecciona en el host **MAX** la interfaz física Ethernet o Wi-Fi real (`ip -br link`, `ip -br addr`, `ethtool`) para identificar su dirección **MAC** (OUI del fabricante) y si está conectada a 100 Mbps o 1000 Mbps Full-Duplex.
2. Configura las VMs `e05-Puppy` (1 GB RAM) y `e05-Ubuntu` (2 GB RAM) en VirtualBox conectando su **Adaptador 1** a la misma **Red interna** llamada `red-e05`.
3. Asigna manualmente en la subred lógica `192.168.50.0/24`:
   - `e05-Puppy`: `192.168.50.10/24`
   - `e05-Ubuntu`: `192.168.50.20/24`
   Verifica la conectividad entre ambas con `ping` y comprueba desde `e05-Ubuntu` que no tienen salida a Internet (aislamiento de Red Interna).
4. Dibuja dos esquemas diferenciados: el **Mapa Físico** del puesto hasta el armario Rack del aula y el **Mapa Lógico** de `red-e05`.
5. Completa la auditoría rápida **PRL (RD 488/1997 PVD y RD 614/2001)** de tu mesa en el aula detectando al menos 2 mejoras posibles.

---

??? success "Ver resolución paso a paso"

    ### Paso 1: Inspección de red en MAX (capa física y MAC)

    ```bash
    # Ver nombre de la interfaz cableada (ej. enp3s0), estado UP y dirección MAC
    ip -br link

    # Ver dirección IP en la red local del aula
    ip -br addr

    # Comprobar velocidad física negociada con el switch del aula
    sudo ethtool enp3s0 | grep -E "Speed:|Duplex:|Link detected:"
    ```

    La salida esperada mostrará `Speed: 1000Mb/s`, `Duplex: Full`, `Link detected: yes` (conectado por par trenzado Cat5e/Cat6 con norma T568B hasta la roseta y switch del rack).

    ### Paso 2: Configuración de Red Interna en `e05-Puppy` y `e05-Ubuntu`

    Al elegir **Red interna (`red-e05`)** no existe servidor DHCP automático por defecto, así que configuramos IP estática temporal para probar el enlace lógico:

    === "e05-Puppy (Terminal)"
        ```bash
        # Comprobar nombre de la interfaz (habitualmente eth0 o enp0s3)
        ip -br link

        # Asignar IP lógica y levantar interfaz
        ip addr add 192.168.50.10/24 dev eth0
        ip link set eth0 up

        # Probar conectividad con Ubuntu
        ping -c 4 192.168.50.20
        ```

    === "e05-Ubuntu (Terminal)"
        ```bash
        # Comprobar nombre de interfaz (enp0s3 en VirtualBox)
        ip -br link

        # Asignar IP lógica en la misma subred
        sudo ip addr add 192.168.50.20/24 dev enp0s3
        sudo ip link set enp0s3 up

        # Probar conectividad con Puppy Linux y tabla ARP (resolución IP → MAC)
        ping -c 4 192.168.50.10
        ip neigh show
        ```

    Si intentas `ping -c 2 8.8.8.8` desde cualquiera de las dos VMs, fallará (`Network is unreachable`): confirma que la **Red Interna** las aísla completamente de la red del instituto y de Internet.

    ### Paso 3: Diferenciación en Diagramas (Mapa Físico vs. Mapa Lógico)

    **Mapa Físico (cableado y ubicación en el aula):**
    ```mermaid
    flowchart LR
        PC["Puesto Alumno · PC MAX\nNIC Ethernet (RJ-45)"] -- "Latiguillo Cat6 T568B (2 m)" --> ROS["Roseta Mural P04"]
        ROS -- "Cableado horizontal Cat6 (18 m)" --> PP["Patch Panel Aula\nPuerto 04"]
        PP -- "Latiguillo (0,5 m)" --> SW["Switch Rack Aula\nPuerto Gi0/4 (1 Gbps Full)"]
    ```

    **Mapa Lógico (direccionamiento y flujo virtualizado):**
    ```mermaid
    flowchart TB
        SWV["Switch Virtual VirtualBox\nRed Interna: red-e05 (Aislada)"]
        PUP["e05-Puppy (1 GB RAM)\n192.168.50.10 /24"] <--> SWV
        UBU["e05-Ubuntu (2 GB RAM)\n192.168.50.20 /24"] <--> SWV
    ```

    ### Paso 4: Checklist PRL / PVD resuelto en el puesto del aula

    | Elemento evaluado | Criterio correcto (RD 488/1997 y RD 614/2001) | Estado / Mejora típica en aula |
    | :--- | :--- | :--- |
    | **Distancia y altura del monitor** | 50–70 cm; borde superior a la altura de los ojos | Subir soporte/monitor si queda demasiado bajo para evitar flexión cervical |
    | **Reflejos y ventanas** | Monitor perpendicular a la luz natural | Cerrar parcialmente persiana si produce reflejo directo en pantalla |
    | **Postura y pies** | Espalda apoyada, codos y rodillas ~90°, pies en suelo | Ajustar altura de silla para que antebrazos queden horizontales |
    | **Riesgo eléctrico y orden** | Cables recogidos sin tensión ni regletas encadenadas | Retirar regletas sueltas en suelo de paso y evitar cables pisados por ruedas |
    | **Pausas visuales** | Aplicar regla **20-20-20** durante prácticas largas | Descansar 20 s mirando a >6 m cada 20 min |
