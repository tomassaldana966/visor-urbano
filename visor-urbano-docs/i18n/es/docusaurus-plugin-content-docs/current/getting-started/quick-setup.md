# ⚡ Configuración Rápida

Esta guía te ayudará a configurar Visor Urbano en tu ambiente de desarrollo en menos de 10 minutos.

## 🎯 Objetivo

Configurar rapidamente:

- Ambiente de desarrollo local
- Dependencias necesarias
- Configuraciones básicas
- Primeras pruebas del sistema

## 🔧 Prerrequisitos

### Software Requerido

- **Node.js** 18+ ([Descargar](https://nodejs.org/))
- **Python** 3.8+ ([Descargar](https://python.org/downloads/))
- **Git** ([Descargar](https://git-scm.com/downloads))
- **Docker** (opcional, pero recomendado) ([Descargar](https://docker.com/get-started))

### Herramientas de Desarrollo

- Editor de código (VS Code recomendado)
- Terminal/línea de comandos
- Navegador web moderno

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Delivery-Associates/visor-urbano.git
cd visor-urbano
```

### 2. Configurar Backend

```bash
cd apps/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Configurar Frontend

```bash
cd ../frontend
npm install
npm run dev
```

### 4. Configurar Documentación

```bash
cd ../../visor-urbano-docs
npm install
npm start
```

## 🌐 URLs de Desarrollo

Después de la instalación, tendrás acceso a:

| Servicio            | URL                                               | Descripción                      |
| ------------------- | ------------------------------------------------- | -------------------------------- |
| 🎨 **Frontend**     | [localhost:3000](http://localhost:3000)           | Interfaz principal de usuario    |
| 📡 **API Backend**  | [localhost:8000](http://localhost:8000)           | Servicios de backend             |
| 📚 **Swagger Docs** | [localhost:8000/docs](http://localhost:8000/docs) | Documentación interactiva de API |
| 🎭 **Storybook**    | [localhost:6006](http://localhost:6006)           | Catálogo de componentes UI       |
| 📖 **Docusaurus**   | [localhost:3001](http://localhost:3001)           | Esta documentación               |

## ✅ Verificación de Instalación

### Probar Frontend

1. Navega a [localhost:3000](http://localhost:3000)
2. Verifica que la interfaz carga correctamente
3. Prueba la navegación básica entre secciones

### Probar Backend

1. Accede a [localhost:8000/docs](http://localhost:8000/docs)
2. Ejecuta algunos endpoints de prueba
3. Verifica la conexión con la base de datos

### Probar Integración

1. Confirma que el frontend se conecta con el backend
2. Prueba un flujo completo de la aplicación
3. Verifica que las APIs responden correctamente

## 🔗 Próximos Pasos

### Para Desarrollo

- [Requisitos del Sistema](./system-requirements.md) - Especificaciones detalladas
- [Integración API](../development/api-integration.md) - Guía técnica para desarrolladores
- [Documentación API](../development/api-documentation.md) - Referencias de endpoints

### Para Producción

- [Despliegue en Producción](../deployment/production-deployment.md) - Guía de instalación en servidor

### Para Personalización

- [Adaptación por Ciudad](../city-adaptation/legal-framework-chile.md) - Guías de personalización local

## 🛠️ Solución de Problemas Comunes

### Error: Puerto en Uso

```bash
# Cambiar puerto del frontend
npm run dev -- --port 3001

# Cambiar puerto del backend
uvicorn app.main:app --reload --port 8001
```

### Error: Dependencias Faltantes

```bash
# Reinstalar dependencias de Node.js
rm -rf node_modules package-lock.json
npm install

# Reinstalar dependencias de Python
pip install --upgrade -r requirements.txt
```

### Error: Permisos de Archivos

```bash
# En sistemas Unix/Linux/macOS
sudo chown -R $USER:$USER .
chmod -R 755 .
```

### Error: Base de Datos

```bash
# Reiniciar servicios de Docker
docker-compose down
docker-compose up -d

# Verificar conexión
docker-compose logs db
```

## 🆘 Obtener Ayuda

Si encuentras problemas durante la instalación:

1. **Revisa los logs**: Cada servicio genera logs detallados
2. **Consulta la documentación**: [Requisitos del Sistema](./system-requirements.md)
3. **Busca en Issues**: [GitHub Issues](https://github.com/Delivery-Associates/visor-urbano/issues)
4. **Pregunta en Discusiones**: [GitHub Discussions](https://github.com/Delivery-Associates/visor-urbano/discussions)

## 🎉 ¡Listo para Desarrollar!

Una vez completada la configuración, estarás listo para:

- Explorar el código fuente
- Hacer modificaciones y mejoras
- Integrar con sistemas existentes
- Contribuir al proyecto

---

> 💡 **Tip**: Mantén todos los servicios ejecutándose mientras desarrollas para una mejor experiencia de desarrollo con hot-reload automático.
