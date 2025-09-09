---
sidebar_position: 1
title: Visión General
description: Introducción al sistema de gestión municipal Visor Urbano
---

# Visor Urbano - Visión General

Visor Urbano es una plataforma moderna de gestión urbana y planificación municipal diseñada para ser implementada y adaptada por ciudades de todo el mundo.

## 🎯 ¿Qué es Visor Urbano?

**Visor Urbano** es un sistema integral que permite a los municipios:

- 📋 **Gestionar trámites** digitalmente (licencias, permisos, certificados)
- 🗺️ **Visualizar información geoespacial** con mapas interactivos
- 🏘️ **Administrar zonificación urbana** y regulaciones
- 👥 **Gestionar usuarios** con diferentes roles y permisos
- 📊 **Generar reportes** y análisis de datos
- 🔄 **Automatizar procesos** administrativos

## 🚀 Stack Tecnológico

### Frontend

- **React 19** + TypeScript
- **Vite** para desarrollo rápido
- **OpenLayers** para mapas interactivos
- **Tailwind CSS** para estilos
- **react-i18next** para internacionalización

### Backend

- **FastAPI** + Python 3.13
- **PostgreSQL** + PostGIS para datos geoespaciales
- **SQLAlchemy** + Alembic para ORM y migraciones
- **JWT** con authlib para autenticación segura

### Infraestructura

- **Docker** + Docker Compose
- **Turborepo** para monorepo
- **pnpm** para gestión de dependencias

## 🌍 Casos de Uso por País

### 🇨🇱 Chile - Piloto nueva version

- Permisos de edificación según OGUC
- Patentes comerciales
- Certificados de informaciones previas
- Integración con SII y Registro Civil

### 🇲🇽 México - Version clasica

- Licencias de funcionamiento
- Permisos de construcción
- Licencias de uso de suelo
- Integración con SIAT

## 📋 Beneficios Clave

### Para Ciudadanos

- ⏱️ **Trámites más rápidos**: Reducción del 50% en tiempos
- 🌐 **Acceso 24/7**: Disponible desde cualquier dispositivo
- 📱 **Interface intuitiva**: Fácil de usar
- 📍 **Seguimiento en tiempo real**: Ver el estado de sus trámites

### Para Funcionarios Municipales

- 📊 **Dashboard administrativo**: Vista completa de procesos
- 🤖 **Automatización**: Menos trabajo manual
- 📈 **Métricas y reportes**: Datos para tomar decisiones
- 💼 **Gestión eficiente**: Mejor organización del trabajo

### Para el Municipio

- 💰 **Reducción de costos**: Menos papel y recursos
- 🔍 **Transparencia**: Procesos visibles y auditables
- 📊 **Mejores datos**: Información para planificación urbana
- 🏆 **Modernización**: Imagen de gobierno digital

## 🏁 Próximos Pasos

1. **[Configuración Rápida](./quick-setup)**: Setup inicial con Docker
2. **[Requisitos del Sistema](./system-requirements)**: Especificaciones técnicas
3. **[Implementation Guide](../implementation/step-by-step-guide)**: Step-by-step setup instructions
4. **[Despliegue en Producción](../deployment/production-deployment)**: Implementación completa

¿Listo para transformar la gestión municipal de tu ciudad? ¡Comencemos! 🚀
