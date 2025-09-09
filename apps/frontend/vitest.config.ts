import path from 'path';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig, loadEnv } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [tailwindcss(), tsconfigPaths()],
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./app/test/setup.ts'],
      env: {
        API_URL: env.API_URL || 'http://localhost:8000',
        COOKIES_SECRET: env.COOKIES_SECRET || 'test-secret',
        GEOSERVER_URL: env.GEOSERVER_URL || 'https://datahub.mpiochih.gob.mx/',
        FICHA_LAYERS:
          env.FICHA_LAYERS ||
          'visorurbano:predio_urbano,chih_zonificacion_secundaria_2023,visorurbano:predio_urbano',
        FICHA_STYLES:
          env.FICHA_STYLES || 'chih_manzanas_catastro,,chih_predio_detalle',
        MAP_ESTADO_LAYER:
          env.MAP_ESTADO_LAYER || 'visorurbano:chih_lim_estatal_utmz13n',
        MAP_ESTADO_CQL_FILTER: env.MAP_ESTADO_CQL_FILTER || '',
        MAP_MUNICIPIO_LAYER:
          env.MAP_MUNICIPIO_LAYER || 'visorurbano:chih_limite_municipal',
        MAP_CENTER_LAT: env.MAP_CENTER_LAT || '20.175628',
        MAP_CENTER_LON: env.MAP_CENTER_LON || '-104.211594',
      },
      coverage: {
        reporter: ['text', 'json', 'html', 'lcov'],
        exclude: [
          'node_modules/',
          'tests/',
          '.storybook/',
          'storybook-static/',
          'coverage/',
          'build/',
          '**/*.d.ts',
          '**/*.config.*',
          '**/vite.*.ts',
          '**/*.stories.*',
        ],
      },
    },
    resolve: {
      extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
      alias: {
        '@root': path.resolve(__dirname),
        '@': path.resolve(__dirname, './app'),
        '@components': path.resolve(__dirname, './app/components'),
        '@hooks': path.resolve(__dirname, './app/hooks'),
        '@layouts': path.resolve(__dirname, './app/layouts'),
        '@pages': path.resolve(__dirname, './app/pages'),
        '@routes': path.resolve(__dirname, './app/routes'),
        '@services': path.resolve(__dirname, './app/services'),
        '@styles': path.resolve(__dirname, './app/styles'),
        '@utils': path.resolve(__dirname, './app/utils'),
      },
    },
  };
});
