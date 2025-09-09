# Comparativa entre QGIS, ArcGIS y GeoServer para uso con PostGIS/PostgreSQL

Este documento presenta una comparativa técnica entre **QGIS**, **ArcGIS** y **GeoServer**, enfocada en su compatibilidad e integración con **PostGIS/PostgreSQL**, con especial interés en aplicaciones municipales tipo **Visor Urbano**, que actualmente utiliza GeoServer.

## Tabla comparativa

| **Aspecto**                                 | **QGIS (Desktop + QGIS Server)**                                                                                         | **ArcGIS (ArcGIS Pro + ArcGIS Server)**                                                     | **GeoServer**                                                                    |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Integración con PostGIS**                 | Compatibilidad nativa. Edición y visualización directa desde QGIS Desktop. QGIS Server publica capas PostGIS fácilmente. | Compatible vía geodatabases ArcSDE. Acceso completo requiere configuración adicional.       | Integración directa, diseñada para PostGIS. Alto rendimiento y soporte completo. |
| **Servicios Web (WMS, WFS, GeoJSON, etc.)** | WMS 1.3.0, WFS 1.1.0, OGC API (GeoJSON), WMTS 1.0.                                                                       | WMS 1.3.0, WFS 2.0.0, WMTS, servicios REST (Esri), GeoJSON parcial.                         | WMS 1.1.1/1.3.0, WFS 1.0/1.1/2.0 (GeoJSON), WMTS, WCS. WPS vía plugins.          |
| **Facilidad de implementación**             | Instalación sencilla. Requiere configuración con Apache/FCGI. Sin panel web nativo.                                      | Requiere múltiples componentes. Alta curva de aprendizaje. GUI integrada.                   | Interfaz web integrada. Curva media. Configuración sencilla y flexible.          |
| **Escalabilidad y rendimiento**             | Buen rendimiento en cargas medianas. Menos escalable bajo alta concurrencia.                                             | Altamente escalable con infraestructura adecuada. Requiere inversión en hardware/licencias. | Excelente rendimiento con PostGIS. Escalable horizontalmente. Caché integrado.   |
| **Comunidad y soporte**                     | Comunidad activa, gran cantidad de documentación. Sin costos de licencia.                                                | Soporte empresarial oficial (Esri). Comunidad cerrada. Licencias costosas.                  | Comunidad técnica activa. Soporte profesional disponible. Sin licencias.         |
| **Costos**                                  | Gratuito (GPL). Sin costo por instalación ni uso.                                                                        | Licencias costosas. Costos anuales por servidor y usuario.                                  | Gratuito (GPL). Costos solo por infraestructura y soporte opcional.              |
| **Interoperabilidad**                       | Compatible con múltiples herramientas libres. Soporta estándares OGC.                                                    | Mejor integración con productos Esri. Soporta OGC parcialmente.                             | Alta interoperabilidad. Compatible con QGIS, Leaflet, OpenLayers.                |

## Análisis y recomendación

### QGIS + QGIS Server

Ideal para equipos que ya utilizan QGIS Desktop, ya que la publicación de mapas puede hacerse directamente desde proyectos .qgs. Sin embargo, **QGIS Server tiene limitaciones de rendimiento en entornos con alta concurrencia**, y no cuenta con una consola web integrada, lo que puede dificultar la administración avanzada en contextos municipales grandes. Aun así, su **curva de aprendizaje es baja** y **no requiere inversión económica**, lo que lo hace atractivo para municipios pequeños o pilotos.

### ArcGIS

Potente, robusto y escalable, pero con **altos costos de licencias** y una infraestructura compleja. Si bien ofrece integración con PostgreSQL y capacidades avanzadas de publicación, su uso puede ser excesivo para necesidades centradas en publicación web de datos SIG. Es recomendable solo si ya se dispone del ecosistema Esri o se requieren funcionalidades exclusivas de su plataforma.

### GeoServer

**La opción más equilibrada y robusta** para entornos municipales como Visor Urbano. Integración nativa con PostGIS, publicación mediante estándares OGC, rendimiento escalable, y sin costos de licencia. Permite fácil consumo desde visores web como Leaflet/OpenLayers, y puede escalar horizontalmente para atender múltiples municipios.

La combinación **QGIS (producción cartográfica) + PostGIS (almacenamiento) + GeoServer (publicación web)** es una arquitectura comprobada, usada exitosamente en proyectos como Visor Urbano Guadalajara.

## Conclusión

**Recomendación:** Para una plataforma tipo Visor Urbano que ya utiliza PostGIS, **GeoServer** es la alternativa más adecuada como motor geoespacial, por su equilibrio entre rendimiento, estándares, escalabilidad y costos. Puede complementarse con QGIS como herramienta de edición de capas y definición de simbología, sin necesidad de cambiar el stack tecnológico actual. ArcGIS, aunque potente, presenta un costo elevado y no aporta ventajas significativas en este caso específico.
