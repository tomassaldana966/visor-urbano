import { describe, expect, it, vi } from 'vitest';
import { formatDate } from './dates';

// Mock i18n to avoid hanging issues
vi.mock('@/i18n', () => ({
  default: {
    language: 'es',
  },
}));

describe('utils/dates', () => {
  describe('formatDate', () => {
    it('should format a date (basic test)', () => {
      const date = '2021-01-01T00:00:00.000Z';
      const result = formatDate(date);

      // Basic check that function returns a string
      expect(typeof result).toBe('string');
      expect(result.length).toBeGreaterThan(0);
    });

    it('should handle different date formats', () => {
      const testCases = [
        '2021-01-01T00:00:00.000Z',
        '2022-12-25T15:30:00.000Z',
        '2023-06-15T09:45:30.000Z',
      ];

      testCases.forEach(date => {
        const result = formatDate(date);
        expect(typeof result).toBe('string');
        expect(result.length).toBeGreaterThan(0);
      });
    });
  });
});
