---
sidebar_position: 3
---

# Integración API

Este documento describe cómo integrar con la API de Visor Urbano.

## Autenticación

- Todos los endpoints requieren autenticación mediante API key.
- Las API keys se pueden generar en el panel de administración.

## Endpoints

- `/v1/permits`
- `/v1/licenses`

## Ejemplo de petición

```bash
curl -H "Authorization: Bearer <API_KEY>" https://visor-urbano.org/v1/permits
```

## Formato de respuesta

Todas las respuestas están en formato JSON.
