#!/bin/bash

# Script to extract route and story information for documentation mapping
# This script analyzes the frontend codebase to generate accurate mappings

FRONTEND_DIR="apps/frontend"
OUTPUT_FILE="visor-urbano-docs/src/data/route-mappings.json"

echo "Extracting route and story information..."

# Create temporary files
ROUTES_TEMP=$(mktemp)
STORIES_TEMP=$(mktemp)

# Extract routes from routes.ts
echo "Extracting routes..."
node -e "
const fs = require('fs');
const path = require('path');

try {
  const routesFile = fs.readFileSync('$FRONTEND_DIR/app/routes.ts', 'utf8');
  
  // Simple regex extraction for route patterns
  const indexMatch = routesFile.match(/index\('([^']+)'\)/);
  const routeMatches = routesFile.match(/route\('([^']+)'[^,]*'([^']+)'\)/g) || [];
  const layoutMatches = routesFile.match(/layout\('([^']+)'[^[]*\[([^]]+)\]/g) || [];
  
  const routes = [];
  
  // Add index route
  if (indexMatch) {
    routes.push({
      path: '/',
      file: indexMatch[1],
      type: 'index'
    });
  }
  
  // Add regular routes
  routeMatches.forEach(match => {
    const parts = match.match(/route\('([^']+)'[^,]*'([^']+)'\)/);
    if (parts) {
      routes.push({
        path: '/' + parts[1],
        file: parts[2],
        type: 'route'
      });
    }
  });
  
  // Extract layout routes
  layoutMatches.forEach(layoutMatch => {
    const layoutParts = layoutMatch.match(/layout\('([^']+)'[^[]*\[([^]]+)\]/);
    if (layoutParts) {
      const layoutFile = layoutParts[1];
      const nestedRoutes = layoutParts[2];
      
      // Extract nested routes within layout
      const nestedMatches = nestedRoutes.match(/route\('([^']+)'[^,]*'([^']+)'\)/g) || [];
      nestedMatches.forEach(nestedMatch => {
        const nestedParts = nestedMatch.match(/route\('([^']+)'[^,]*'([^']+)'\)/);
        if (nestedParts) {
          routes.push({
            path: '/' + nestedParts[1],
            file: nestedParts[2],
            type: 'nested',
            layout: layoutFile
          });
        }
      });
    }
  });
  
  console.log(JSON.stringify(routes, null, 2));
} catch (error) {
  console.error('Error processing routes:', error.message);
  process.exit(1);
}
" > $ROUTES_TEMP

# Extract story information
echo "Extracting story information..."
find $FRONTEND_DIR -name "*.stories.{ts,tsx}" -type f | while read story_file; do
  echo "Processing: $story_file"
  
  # Extract title and exports from story file
  node -e "
const fs = require('fs');
const path = require('path');

try {
  const content = fs.readFileSync('$story_file', 'utf8');
  
  // Extract title
  const titleMatch = content.match(/title:\s*['\"](.*?)['\"]/);
  const title = titleMatch ? titleMatch[1] : '';
  
  // Extract story exports (Default, Primary, Secondary, etc.)
  const exportMatches = content.match(/export const (\w+):/g) || [];
  const stories = exportMatches.map(match => {
    const name = match.match(/export const (\w+):/)[1];
    return name;
  }).filter(name => name !== 'default');
  
  if (title && stories.length > 0) {
    const storyInfo = {
      file: '$story_file'.replace('$FRONTEND_DIR/', ''),
      title: title,
      stories: stories,
      component: path.basename(path.dirname('$story_file'))
    };
    
    console.log(JSON.stringify(storyInfo));
  }
} catch (error) {
  console.error('Error processing $story_file:', error.message);
}
  "
done > $STORIES_TEMP

# Combine the information
echo "Combining route and story information..."
node -e "
const fs = require('fs');

try {
  const routesData = JSON.parse(fs.readFileSync('$ROUTES_TEMP', 'utf8'));
  const storiesData = fs.readFileSync('$STORIES_TEMP', 'utf8')
    .split('\n')
    .filter(line => line.trim())
    .map(line => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
  
  // Create mapping with better story links
  const mappings = routesData.map(route => {
    const routePath = route.path;
    const fileName = route.file;
    
    // Try to find relevant stories based on route name and file
    const routeName = routePath.replace('/', '').split('/')[0] || 'home';
    const relevantStories = storiesData.filter(story => {
      const componentName = story.component.toLowerCase();
      const titleParts = story.title.toLowerCase().split('/');
      const lastTitlePart = titleParts[titleParts.length - 1];
      
      return componentName.includes(routeName) || 
             lastTitlePart.includes(routeName) ||
             routeName.includes(componentName) ||
             (routeName === 'home' && (componentName.includes('hero') || componentName.includes('dashboard')));
    });
    
    // Generate storybook links with proper format
    const storybookLinks = relevantStories.map(story => {
      return story.stories.map(storyName => {
        // Convert title format: 'Components/Button' -> 'components-button'
        const titleSlug = story.title.toLowerCase().replace(/\//g, '-');
        // Convert story name: 'Default' -> 'default'
        const storySlug = storyName.toLowerCase();
        
        return {
          name: \`\${story.component} - \${storyName}\`,
          path: \`?path=/docs/\${titleSlug}--\${storySlug}\`,
          category: story.title.split('/')[0] || 'Components'
        };
      });
    }).flat();
    
    return {
      route: routePath,
      file: fileName,
      description: generateDescription(routePath, fileName),
      status: determineStatus(routePath),
      storybook: storybookLinks,
      endpoints: generateEndpoints(routePath)
    };
  });
  
  function generateDescription(routePath, fileName) {
    const descriptions = {
      '/': 'Main page with dashboard and statistics',
      '/about': 'Information page about the project',
      '/login': 'User login page',
      '/logout': 'User logout',
      '/register': 'New user registration',
      '/forgot': 'Password recovery',
      '/map': 'Interactive map with layers and geospatial search',
      '/licenses': 'License management and consultation',
      '/news': 'News and articles center',
      '/procedures': 'Procedure and process management',
      '/notifications': 'User notification center',
      '/director/dashboard': 'Director administrative panel',
      '/director/users': 'System user management',
      '/director/settings': 'System settings'
    };
    
    // Check for exact match first
    if (descriptions[routePath]) {
      return descriptions[routePath];
    }
    
    // Check for pattern matches
    if (routePath.includes('/news/')) return 'Specific news article';
    if (routePath.includes('/procedures/')) return 'Specific procedure management';
    if (routePath.includes('/director/')) return 'Administrative panel - ' + routePath.split('/').pop();
    if (routePath.includes('/technical-sheet/')) return 'Project technical sheet';
    
    return 'System page - ' + routePath.split('/').filter(Boolean).join(' > ');
  }
  
  function determineStatus(routePath) {
    const completeRoutes = ['/', '/login', '/map', '/procedures', '/director/dashboard'];
    const partialRoutes = ['/register', '/forgot', '/news'];
    
    if (completeRoutes.some(route => routePath.startsWith(route))) return 'complete';
    if (partialRoutes.some(route => routePath.startsWith(route))) return 'partial';
    return 'minimal';
  }
  
  function generateEndpoints(routePath) {
    const endpointMap = {
      '/': [
        { method: 'GET', path: '/v1/dashboard/stats', description: 'Estadísticas del dashboard', router: 'dashboard' }
      ],
      '/login': [
        { method: 'POST', path: '/v1/auth/login', description: 'Iniciar sesión', router: 'auth' },
        { method: 'POST', path: '/v1/auth/refresh', description: 'Renovar token', router: 'auth' }
      ],
      '/logout': [
        { method: 'POST', path: '/v1/auth/logout', description: 'Cerrar sesión', router: 'auth' }
      ],
      '/register': [
        { method: 'POST', path: '/v1/auth/register', description: 'Registrar usuario', router: 'auth' }
      ],
      '/forgot': [
        { method: 'POST', path: '/v1/auth/forgot-password', description: 'Solicitar recuperación', router: 'password' }
      ],
      '/map': [
        { method: 'GET', path: '/v1/map/layers', description: 'Capas del mapa', router: 'map' },
        { method: 'GET', path: '/v1/map/search', description: 'Búsqueda geoespacial', router: 'map' }
      ],
      '/licenses': [
        { method: 'GET', path: '/v1/licenses', description: 'Listar licencias', router: 'licenses' }
      ],
      '/procedures': [
        { method: 'GET', path: '/v1/procedures', description: 'Listar procedimientos', router: 'procedures' },
        { method: 'POST', path: '/v1/procedures', description: 'Crear procedimiento', router: 'procedures' }
      ],
      '/news': [
        { method: 'GET', path: '/v1/news', description: 'Listar noticias', router: 'news' }
      ]
    };
    
    // Return exact match or try to find pattern
    if (endpointMap[routePath]) return endpointMap[routePath];
    
    // Pattern matching for dynamic routes
    if (routePath.includes('/procedures/')) {
      return [
        { method: 'GET', path: '/v1/procedures/:id', description: 'Obtener procedimiento', router: 'procedures' },
        { method: 'PUT', path: '/v1/procedures/:id', description: 'Actualizar procedimiento', router: 'procedures' }
      ];
    }
    
    if (routePath.includes('/news/')) {
      return [
        { method: 'GET', path: '/v1/news/:id', description: 'Obtener noticia', router: 'news' }
      ];
    }
    
    if (routePath.includes('/director/')) {
      return [
        { method: 'GET', path: '/v1/admin' + routePath.replace('/director', ''), description: 'Datos administrativos', router: 'admin' }
      ];
    }
    
    return [];
  }
  
  console.log(JSON.stringify(mappings, null, 2));
} catch (error) {
  console.error('Error combining data:', error.message);
  process.exit(1);
}
" > temp_mappings.json

# Create output directory if it doesn't exist
mkdir -p "$(dirname $OUTPUT_FILE)"

# Move final file
mv temp_mappings.json $OUTPUT_FILE

# Cleanup
rm -f $ROUTES_TEMP $STORIES_TEMP

echo "Route mappings generated successfully: $OUTPUT_FILE"
echo "Total routes mapped: $(cat $OUTPUT_FILE | jq '. | length')"
