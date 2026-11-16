---
ra: RA7
ce:
  - RA7.b
tipo: concepto
publicar: true
fuentes:
  - raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md
ultima_revision: "2026-11-15"
---

# Evaluación de Necesidades de Software en Entornos Productivos

<!-- fuente: raw/procesados/ra7-clasificacion-software-licencias-entornos-productivos.md -->

## 1. Criterios Profesionales para Seleccionar Software Corporativo

Implantar una herramienta en una PYME, instituto o departamento de desarrollo no consiste en instalar "la más popular", sino en justificar una decisión técnica y económica mediante cuatro criterios objetivos:

1. **TCO (*Total Cost of Ownership*):** suma del coste anual de licencias (`SaaS` o perpetuas), renovación hardware requerida, tiempo de formación del personal, migración de documentos y soporte técnico oficial.
2. **Estándares abiertos e interoperabilidad (evitar *Vendor Lock-in*):** usar formatos documentales abiertos (**ODF** `.odt`/`.ods`, **PDF/A** ISO 19005 para archivo legal, **Markdown**, **CSV**, **JSON**) impide quedar cautivo de un proveedor único que pueda duplicar tarifas en el futuro.
3. **Ciclo de vida LTS y cumplimiento normativo (`RGPD` / `ENS`):** elegir ramas de soporte extendido (**Ubuntu LTS**, **LibreOffice Still**, **Firefox ESR**, **PostgreSQL** soportado) y garantizar dónde residen físicamente los datos personales de clientes y alumnado.
4. **Modelo de despliegue adecuado (*On-Premise* vs *SaaS*):** decidir si el software corre instalado en cada puesto (PC local), centralizado en servidor propio (*Nextcloud* en CPD privado) o contratado en nube externa (*Google Workspace* / *Microsoft 365*).

---

## 2. Comparativa Técnica: Escenario Aula DAM / Administración Pública vs. Consultora

| Necesidad del puesto | Opción Software Libre / Abierto | Opción Comercial / Nube | Criterio decisivo de elección |
| :--- | :--- | :--- | :--- |
| **Ofimática general** | **LibreOffice Still** (ODF nativo) | **Microsoft 365** (SaaS corporativo) | Presupuesto público, estándar ODF vs macros VBA complejas heredadas |
| **Nube colaborativa documental** | **Nextcloud + Collabora** (*on-premise*) | **Google Workspace / OneDrive** | Soberanía absoluta del dato (`ENS`/`RGPD`) frente a gestión sin mantenimiento propio |
| **Diseño UI / Vectorial** | **Inkscape / GIMP / Penpot** | **Figma / Adobe Creative Cloud** | Flujo colaborativo en tiempo real (Figma/Penpot web) vs exportación offline ligera |
| **IDE y Base de Datos DAM** | **VS Code / Eclipse / PostgreSQL** | **IntelliJ IDEA Ultimate / Oracle** | Uso gratuito educativo vs funciones Enterprise avanzadas |

---

## 3. Verificación de Recursos, Formatos y Dependencias antes del Despliegue

=== "MAX / Ubuntu (Linux)"

    ```bash
    # Comprobar si un documento corporativo cumple estándares abiertos ODF / PDF en repositorio
    file memoria_tecnica.odt documento_legal.pdf

    # Verificar versión instalada y rama estable del paquete clave en Ubuntu
    apt-cache policy libreoffice
    ```

=== "Windows 10 / 11"

    ```powershell
    # Evaluar consumo de disco y RAM antes de autorizar software en parque de equipos (ej. 16 GB MAX / Win10)
    Get-Process | Sort-Object WorkingSet64 -Descending |
      Select-Object -First 8 ProcessName, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}}
    ```

---

## Computación en la Nube (`SaaS`, `PaaS`, `IaaS`), VPS y Alojamiento Web

En entornos productivos modernos, la decisión técnica no solo abarca el software instalado en el PC local sino qué parte del servicio se ejecuta en la nube:

| Modelo Cloud | Quién gestiona el hardware/SO/runtime | Ejemplos habituales |
| :--- | :--- | :--- |
| **`IaaS`** (*Infraestructura como Servicio*) | Proveedor gestiona físico/virtualización; tú administras el SO y aplicaciones | Servidores **VPS** (*Clouding.io*), EC2 en **Amazon AWS**, **Google Cloud** Compute Engine, **Microsoft Azure** VMs, Oracle Cloud Free Tier |
| **`PaaS`** (*Plataforma como Servicio*) | Proveedor gestiona SO y runtime; tú despliegas tu código/BD | App Engine, Cloud Run, hosting PHP/Softaculous gestionado, GitHub Pages |
| **`SaaS`** (*Software como Servicio*) | Todo gestionado por el proveedor; el usuario accede vía web o app | Google Workspace, Microsoft 365, OneDrive, Dropbox, Nextcloud gestionado, Trello |

- **Almacenamiento en frío (*Cold Archive*):** servicios como **Amazon S3 Glacier** ofrecen costes mínimos por GB para copias históricas de respaldo a cambio de tiempos de recuperación mayores.
- **Servidor doméstico vs. VPS:** para publicar una web o servicio propio desde casa (p. ej. Raspberry Pi) se precisa un **DDNS** (*DuckDNS* / *No-IP*) y ausencia de *CG-NAT*; en un **VPS** (como *Clouding.io*) con pila **LAMP** (*Linux + Apache + MySQL + PHP*) dispones directamente de IPv4 pública fija y ancho de banda simétrico en centro de datos.

---

## Recursos para profundizar

- Concepto anterior: [Clasificación del Software y Licencias](ra7-clasificacion-software-licencias-modelos-distribucion.md).
- Guía de estándares abiertos en Administraciones Públicas: [Esquema Nacional de Interoperabilidad (ENI)](https://administracionelectronica.gob.es/).
- Vídeo recomendado sobre ofimática productiva y software libre: [Suites ofimáticas, productividad y estándares abiertos (YouTube)](https://www.youtube.com/watch?v=GArVeJj8MHo).
