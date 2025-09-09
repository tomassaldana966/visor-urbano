import path from 'path';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tailwindcss(), tsconfigPaths()],
  server: {
    proxy: {
      '/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
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
  optimizeDeps: {
    esbuildOptions: {
      resolveExtensions: ['.js', '.jsx', '.ts', '.tsx', '.mjs'],
      format: 'esm',
    },
  },
  build: {
    commonjsOptions: {
      transformMixedEsModules: true,
    },
  },
});
