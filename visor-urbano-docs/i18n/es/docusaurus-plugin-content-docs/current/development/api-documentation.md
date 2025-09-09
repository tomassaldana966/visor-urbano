---
sidebar_position: 4
---

# Documentación API

Este documento proporciona una visión general de los endpoints disponibles y su uso en Visor Urbano.

## Endpoints

- `/v1/permits` - Gestionar permisos
- `/v1/licenses` - Gestionar licencias

## Autenticación

Todos los endpoints requieren una API key.

## Ejemplo

```bash
curl -H "Authorization: Bearer <API_KEY>" https://visor-urbano.org/v1/licenses
```
