import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      // Critical rules that should block builds
      'no-console': ['error', { allow: ['warn', 'error'] }],

      // Turn off rules that are too noisy for the existing codebase
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/no-empty-object-type': 'off',
      '@typescript-eslint/no-unused-expressions': 'off',
      'prefer-const': 'off',
    },
  },
  {
    files: ['**/*.stories.{ts,tsx}', '**/*.test.{ts,tsx}', '.storybook/**/*'],
    rules: {
      // Keep story and test files completely relaxed
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
    },
  },
  {
    ignores: [
      'build/**',
      'storybook-static/**',
      'dist/**',
      'node_modules/**',
      '*.config.*',
      'app/assets/**',
      '.react-router/**',
      'public/locales/**',
      'debug-edit-endpoints.js',
      'debug-edit.mjs',
    ],
  }
);
