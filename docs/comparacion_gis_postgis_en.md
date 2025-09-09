# Comparison between QGIS, ArcGIS and GeoServer for use with PostGIS/PostgreSQL

This document presents a technical comparison between **QGIS**, **ArcGIS** and **GeoServer**, focused on their compatibility and integration with **PostGIS/PostgreSQL**, with special interest in municipal applications like **Visor Urbano**, which currently uses GeoServer.

## Comparison table

| **Aspect**                                 | **QGIS (Desktop + QGIS Server)**                                                                                       | **ArcGIS (ArcGIS Pro + ArcGIS Server)**                                                 | **GeoServer**                                                                    |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **PostGIS Integration**                    | Native compatibility. Direct editing and visualization from QGIS Desktop. QGIS Server publishes PostGIS layers easily. | Compatible via ArcSDE geodatabases. Full access requires additional configuration.      | Direct integration, designed for PostGIS. High performance and complete support. |
| **Web Services (WMS, WFS, GeoJSON, etc.)** | WMS 1.3.0, WFS 1.1.0, OGC API (GeoJSON), WMTS 1.0.                                                                     | WMS 1.3.0, WFS 2.0.0, WMTS, REST services (Esri), partial GeoJSON.                      | WMS 1.1.1/1.3.0, WFS 1.0/1.1/2.0 (GeoJSON), WMTS, WCS. WPS via plugins.          |
| **Implementation ease**                    | Simple installation. Requires Apache/FCGI configuration. No native web panel.                                          | Requires multiple components. High learning curve. Integrated GUI.                      | Integrated web interface. Medium curve. Simple and flexible configuration.       |
| **Scalability and performance**            | Good performance on medium loads. Less scalable under high concurrency.                                                | Highly scalable with adequate infrastructure. Requires investment in hardware/licenses. | Excellent performance with PostGIS. Horizontally scalable. Integrated caching.   |
| **Community and support**                  | Active community, extensive documentation. No licensing costs.                                                         | Official enterprise support (Esri). Closed community. Expensive licenses.               | Active technical community. Professional support available. No licenses.         |
| **Costs**                                  | Free (GPL). No cost per installation or use.                                                                           | Expensive licenses. Annual costs per server and user.                                   | Free (GPL). Costs only for infrastructure and optional support.                  |
| **Interoperability**                       | Compatible with multiple open source tools. Supports OGC standards.                                                    | Better integration with Esri products. Partially supports OGC.                          | High interoperability. Compatible with QGIS, Leaflet, OpenLayers.                |

## Analysis and recommendation

### QGIS + QGIS Server

Ideal for teams already using QGIS Desktop, as map publishing can be done directly from .qgs projects. However, **QGIS Server has performance limitations in high concurrency environments**, and lacks an integrated web console, which can hinder advanced administration in large municipal contexts. Nevertheless, its **learning curve is low** and **requires no economic investment**, making it attractive for small municipalities or pilots.

### ArcGIS

Powerful, robust and scalable, but with **high licensing costs** and complex infrastructure. While it offers PostgreSQL integration and advanced publishing capabilities, its use may be excessive for needs focused on web publishing of GIS data. It's only recommended if the Esri ecosystem is already available or exclusive platform functionalities are required.

### GeoServer

**The most balanced and robust option** for municipal environments like Visor Urbano. Native PostGIS integration, publishing through OGC standards, scalable performance, and no licensing costs. Enables easy consumption from web viewers like Leaflet/OpenLayers, and can scale horizontally to serve multiple municipalities.

The combination **QGIS (cartographic production) + PostGIS (storage) + GeoServer (web publishing)** is a proven architecture, successfully used in projects like Visor Urbano Guadalajara.

## Conclusion

**Recommendation:** For an Visor Urbano-type platform that already uses PostGIS, **GeoServer** is the most suitable alternative as a geospatial engine, due to its balance between performance, standards, scalability and costs. It can be complemented with QGIS as a layer editing tool and symbology definition, without needing to change the current technology stack. ArcGIS, although powerful, presents high costs and doesn't provide significant advantages in this specific case.
