---
sidebar_position: 1
title: Overview
description: Introduction to the Visor Urbano municipal management system
---

# Visor Urbano - Overview

Visor Urbano is a modern urban management and municipal planning platform designed to be implemented and adapted by cities around the world.

## 🎯 What is Visor Urbano?

**Visor Urbano** is a comprehensive system that allows municipalities to:

- 📋 **Manage procedures** digitally (licenses, permits, certificates)
- 🗺️ **Visualize geospatial information** with interactive maps
- 🏘️ **Manage urban zoning** and regulations
- 👥 **Manage users** with different roles and permissions
- 📊 **Generate reports** and data analytics
- 🔄 **Automate administrative processes**

## 🚀 Technology Stack

### Frontend

- **React 19** + TypeScript
- **Vite** for fast development
- **OpenLayers** for interactive maps
- **Tailwind CSS** for styling
- **react-i18next** for internationalization

### Backend

- **FastAPI** + Python 3.13
- **PostgreSQL** + PostGIS for geospatial data
- **SQLAlchemy** + Alembic for ORM and migrations
- **JWT** with authlib for secure authentication

### Infrastructure

- **Docker** + Docker Compose
- **Turborepo** for monorepo
- **pnpm** for dependency management

## 🌍 Use Cases by Country

### 🇨🇱 Chile - New Version Pilot

- Building permits according to OGUC
- Commercial patents
- Prior information certificates
- Integration with SII and Civil Registry

### 🇲🇽 Mexico - Classic Version

- Municipal permits
- Commercial licenses
- Urban development certificates

## 🛠️ Quick Start

1. **System Requirements**: Docker, Node.js 18+, Python 3.13
2. **Installation**: Clone repository and run setup
3. **Configuration**: Adapt for your municipality
4. **Deployment**: Production-ready Docker setup

## 📖 Documentation Structure

This documentation is organized into:

- **Getting Started**: Installation and setup
- **City Adaptation**: Country-specific implementations
- **Development**: API and component documentation
- **Deployment**: Production guides

## 🤝 Global Community

Visor Urbano is designed for international replication with:

- Multi-language support (Spanish, English, French, Portuguese)
- Adaptable legal frameworks
- Regional implementation guides
- Active development community

---

Ready to get started? Check our [quick setup guide](./quick-setup) or browse specific implementations for your region.
