---
sidebar_position: 2
---

# Requisitos del Sistema

Requisitos de hardware y software para desplegar Visor Urbano en diferentes entornos.

## Requisitos mínimos

### Entorno de desarrollo

- **CPU**: 2 núcleos, 2.0 GHz
- **RAM**: 8 GB
- **Almacenamiento**: 20 GB de espacio disponible
- **SO**: macOS, Linux o Windows 10/11

### Entorno de producción (municipio pequeño)

- **CPU**: 4 núcleos, 2.5 GHz
- **RAM**: 16 GB
- **Almacenamiento**: 100 GB SSD
- **Red**: 100 Mbps de ancho de banda

### Entorno de producción (municipio grande)

- **CPU**: 8 núcleos, 3.0 GHz
- **RAM**: 32 GB
- **Almacenamiento**: 500 GB SSD
- **Red**: 1 Gbps de ancho de banda

## Dependencias de software

### Software requerido

- **Node.js**: 18.x o 20.x LTS
- **Python**: 3.9, 3.10 o 3.11
- **PostgreSQL**: 14.x o 15.x
- **Redis**: 6.x o 7.x (para caché)

### Gestores de paquetes

- **pnpm**: 8.x (recomendado para monorepo)
- **npm**: 9.x (alternativa)
- **pip**: Última versión

### Software opcional

- **Docker**: 24.x con Docker Compose
- **Nginx**: 1.20+ (proxy inverso)
- **Git**: 2.30+ (control de versiones)

## Soporte de navegadores

### Navegadores soportados

- **Chrome**: 100+
- **Firefox**: 100+
- **Safari**: 15+
- **Edge**: 100+

### Soporte móvil

- **iOS Safari**: 15+
