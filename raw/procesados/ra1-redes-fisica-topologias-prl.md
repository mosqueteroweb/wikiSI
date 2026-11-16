---
id: "raw-ra1-redes-fisica-topologias-prl"
ra: ["RA1"]
ce: ["RA1.e", "RA1.f", "RA1.g", "RA1.h"]
nivel_credibilidad: "Nivel 1"
fecha_ingesta: "2026-11-15"
fuentes_primarias:
  - "IEEE 802.3 (Ethernet) & IEEE 802.11 (Wi-Fi)"
  - "ANSI/TIA-568: Estándares de Cableado Estructurado y Pines T568A/T568B"
  - "Oracle VirtualBox User Manual: Chapter 6 - Virtual Networking (NAT, NAT Network, Bridged, Internal, Host-Only)"
  - "INSST (Instituto Nacional de Seguridad y Salud en el Trabajo): Guía Técnica RD 488/1997 (PVD) y RD 614/2001 (Riesgo Eléctrico)"
  - "Real Decreto 110/2015 sobre Residuos de Aparatos Eléctricos y Electrónicos (RAEE)"
---

# Fuente Procesada: Redes Locales, Cableado, Mapas Físico/Lógico y PRL

## 1. Tipos de Redes y Sistemas de Comunicación

- **Por alcance geográfico:**
  - **PAN (*Personal Area Network*):** Alcance de pocos metros (Bluetooth, NFC, USB tethering).
  - **LAN (*Local Area Network*):** Aula, oficina o edificio; alta velocidad, baja latencia, propiedad privada (Ethernet / Wi-Fi).
  - **MAN (*Metropolitan Area Network*):** Campus o área metropolitana interconectando múltiples LANs mediante fibra.
  - **WAN (*Wide Area Network*):** Alcance nacional o global (Internet, enlaces MPLS/SD-WAN de operadores).
- **Por medio de transmisión:** Cableadas (cobre par trenzado / fibra óptica) vs Inalámbricas (Wi-Fi IEEE 802.11ax/be, radioenlaces).
- **Por direccionalidad del canal:** Símplex (un sentido), Semidúplex (*half-duplex*, alterno) y Dúplex completo (*full-duplex*, bidireccional simultáneo en switches modernos).

## 2. Componentes de una Red y Cableado Estructurado

- **Tarjeta de red (NIC):** Interfaz Ethernet o Wi-Fi identificada físicamente por una dirección **MAC** de 48 bits en hexadecimal (primeros 24 bits: OUI del fabricante; últimos 24 bits: identificador único).
- **Dispositivos de interconexión (Modelo OSI):**
  - **Repetidor / Concentrador (*Hub* - Capa 1 Física):** Reenvía la señal eléctrica por todos los puertos; comparte un único **dominio de colisión** (obsoleto en LANs modernas).
  - **Conmutador (*Switch* - Capa 2 Enlace):** Aprende direcciones MAC en su tabla CAM y conmuta tramas únicamente hacia el puerto destino. Cada puerto aísla su dominio de colisión, aunque todos pertenecen al mismo **dominio de difusión (*broadcast*)** salvo uso de VLANs.
  - **Punto de Acceso (*Access Point / AP* - Capa 2):** Puentea clientes inalámbricos Wi-Fi hacia la red Ethernet cableada.
  - **Enrutador (*Router* - Capa 3 Red):** Interconecta distintas redes IP, toma decisiones por dirección IP/tabla de rutas y separa dominios de difusión.
- **Medios guiados y conectores:**
  - **Par trenzado (conector RJ-45 8P8C):**
    - *Blindaje:* **UTP** (sin blindaje), **FTP** (lámina global), **SFTP** (malla global + lámina por par).
    - *Categorías:* **Cat5e** (1 Gbps hasta 100 m, 100 MHz), **Cat6** (1 Gbps a 100 m / 10 Gbps hasta 55 m, 250 MHz), **Cat6A** (10 Gbps a 100 m, 500 MHz).
    - *Normas de crimpado:* **TIA/EIA-568B** (pines 1–8: Blanco-Naranja, Naranja, Blanco-Verde, Azul, Blanco-Azul, Verde, Blanco-Marrón, Marrón) y **TIA/EIA-568A** (intercambia los pares naranja y verde). Cable **directo** (misma norma en ambos extremos, el más habitual hoy con *Auto-MDIX*) vs **cruzado** (568A en un extremo y 568B en el otro).
  - **Fibra óptica (conectores LC, SC):** Inmune a interferencias electromagnéticas (EMI) y gran distancia. **Multimodo (MMF: OM3/OM4)** para distancias medias en campus/CPD; **Monomodo (SMF: OS2)** para kilómetros.
- **Cableado estructurado:** Armario **Rack** (19 pulgadas, unidades `U`), **Patch Panel** (terminación de cableado horizontal rígido), **latiguillos** (*patch cords* flexibles hacia el switch), canalización y **rosetas** murales etiquetadas.

## 3. Topologías y Mapas Físicos vs. Lógicos

- **Topologías principales:** Estrella (estándar actual con switch central), Estrella extendida / Árbol, Bus (cable coaxial compartido, obsoleto), Anillo (token passing, presente en variantes redundantes de fibra), Malla total o parcial (alta redundancia en núcleo/WAN).
- **Mapa físico:** Representa la ubicación espacial real de puestos, tomas de pared, racks, switches, tipos y longitudes de cable, puertos ocupados y numeración física de latiguillos.
- **Mapa lógico:** Representa el flujo de datos y direccionamiento: direcciones IPv4/IPv6, máscaras de subred, puerta de enlace (*gateway*), DNS, VLANs y reglas entre nodos, con independencia de dónde esté físicamente cada cable.
- **Modos de red en Oracle VirtualBox (aula MAX):**
  - **NAT:** VM sale a Internet a través del host MAX; aislada de otras VMs.
  - **Red NAT (*NAT Network*):** Varias VMs comparten subred privada y salida a Internet vía NAT.
  - **Adaptador Puente (*Bridged*):** La VM obtiene IP directamente en la red física del aula como un PC más.
  - **Red Interna (*Internal Network*):** Aislamiento total entre VMs en un switch virtual privado (ideal para prácticas de aula sin interferir con la red del instituto).
  - **Solo Anfitrión (*Host-Only*):** Comunicación exclusiva entre el host MAX y las VMs.

## 4. Seguridad y Prevención de Riesgos Laborales (PRL)

- **Marco legal español:** Ley 31/1995 de Prevención de Riesgos Laborales, **RD 488/1997** (Pantallas de Visualización de Datos - PVD) y **RD 614/2001** (riesgo eléctrico).
- **Seguridad física y eléctrica en taller:**
  - **ESD (Descarga Electrostática):** Puede dañar circuitos integrados con voltajes imperceptibles para el humano (< 3.000 V no se sienten, pero ~100 V destruyen componentes CMOS). Uso de pulsera antiestática con resistencia de protección (1 MΩ) conectada a chasis/tierra, alfombrilla ESD y bolsas antiestáticas.
  - **Seguridad eléctrica:** Desenchufar el equipo de la toma AC antes de abrirlo, pulsar el botón de encendido unos segundos para descargar condensadores de la fuente, no abrir fuentes de alimentación sin formación de alta tensión, evitar regletas encadenadas y verificar toma de tierra.
  - **Protección de suministro (SAI/UPS):** Sistemas *Offline*, *Line-Interactive* y *Online* (doble conversión) contra cortes y sobretensiones.
- **Ergonomía PVD:**
  - Distancia ojos-pantalla de **50–70 cm**, borde superior de la pantalla a la altura de los ojos o ligeramente por debajo.
  - Monitor perpendicular a las ventanas para evitar deslumbramientos y reflejos; iluminación ambiente de 300–500 lux.
  - Espalda apoyada en respaldo lumbar, muslos horizontales y pies planos en el suelo (o reposapiés), ángulo de ~90° en codos y rodillas.
  - Pausas activas y **regla 20-20-20** (cada 20 minutos, mirar a 6 metros / 20 pies durante 20 segundos).
- **Gestión ambiental (RD 110/2015 RAEE):** Separación selectiva de residuos electrónicos, baterías de SAI y pilas CMOS en puntos limpios autorizados.
