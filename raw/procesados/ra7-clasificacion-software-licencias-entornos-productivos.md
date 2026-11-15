---
tema: "Clasificación del Software, Licencias, Propósito y Evaluación de Necesidades en Entornos Productivos"
ra: RA7
ce:
  - RA7.a
  - RA7.b
fecha_ingesta: "2026-11-15"
fuente_tipo: sintesis-tecnica-curada
---

# Fuente Curada · RA7 (1/3) · Licencias de Software y Entornos Productivos

## 1. Clasificación del Software por Propósito y Licencia (`RA7.a`)

- **Clasificación según propósito:**
  - **Software de base / sistema:** sistemas operativos, controladores, hipervisores, firmware.
  - **Software de programación / desarrollo:** compiladores, intérpretes, IDEs, SDKs, control de versiones (`git`).
  - **Software de aplicación / propósito general:** ofimática (LibreOffice, Microsoft 365), navegadores, correo, diseño, ERP/CRM corporativos.
- **Clasificación por licencia y modelo de distribución:**
  - **Software Libre y de Código Abierto (FOSS):** garantiza 4 libertades (usar, estudiar, modificar y redistribuir):
    - *Copyleft fuerte:* **GPLv3** / **AGPLv3** (si redistribuyes obras derivadas —o las sirves en red en AGPL— deben mantener exactamente la misma licencia abierta).
    - *Copyleft débil:* **LGPL** (permite enlazar librerías desde código propietario manteniendo abierta la librería).
    - *Permisivas:* **MIT**, **Apache 2.0** (incluye cláusula explícita de patentes), **BSD 2/3-Clause** (permiten integrar código en productos comerciales cerrados citando autoría).
  - **Software Propietario / Comercial:** licencia **EULA** (usuario final), pago perpetuo, por suscripción (**SaaS**, *Microsoft 365*) o **CAL / OEM / Volumen**, sin acceso al código fuente.
  - **Freeware** (gratuito pero código cerrado y sin redistribución modificada) vs **Shareware / Freemium / Trial** (funcionalidad o tiempo limitados).
- **Auditoría de licencias en proyectos de desarrollo:** comprobar dependencias (`package.json`, `pom.xml`, `pip-licenses` / `licensecheck`) para evitar incompatibilidades legales antes de distribuir software comercial en una empresa DAM.

## 2. Evaluación de Necesidades de Software en Entornos Productivos (`RA7.b`)

- Criterios de selección en empresas y aulas educativas:
  1. **TCO (*Total Cost of Ownership*):** coste de licencias + formación + soporte + migración + hardware exigido.
  2. **Interoperabilidad y estándares abiertos:** uso de formatos abiertos (**ODF `.odt`/`.ods`**, **PDF/A** para archivo legal a largo plazo, **CSV/JSON**, **Markdown**) frente a formatos cerrados que generan *vendor lock-in* (dependencia de un único proveedor).
  3. **Mantenimiento, ciclo de vida LTS y cumplimiento normativo:** soporte de parches (Ubuntu LTS, LibreOffice Still, Firefox ESR), RGPD/ENS (soberanía del dato en la nube).
  4. **Modelos de despliegue:** Instalación local (*on-premise*), aplicación portátil, suite Web / **SaaS** colaborativa (Nextcloud/Collabora vs Google Workspace / Microsoft 365).
