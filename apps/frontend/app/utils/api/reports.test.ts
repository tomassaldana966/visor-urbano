import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  getAnnualBarChart,
  getLicensingStatusSummary,
  getReviewStatusPie,
  getCompleteAnalytics,
} from './reports';

// Mock requestAPI
vi.mock('./base', () => ({
  requestAPI: vi.fn(),
  UnauthorizedError: class extends Error {
    constructor(message = 'Unauthorized') {
      super(message);
      this.name = 'UnauthorizedError';
    }
  },
}));

import { requestAPI } from './base';

const mockRequestAPI = vi.mocked(requestAPI);

describe('Reports API Integration', () => {
  const mockAuthToken = 'test-auth-token';

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getAnnualBarChart', () => {
    it('should fetch annual bar chart data successfully', async () => {
      const mockResponse = [
        { name: 'Enero', value: 25, extra: 1 },
        { name: 'Febrero', value: 30, extra: 2 },
        { name: 'Marzo', value: 35, extra: 3 },
      ];

      mockRequestAPI.mockResolvedValueOnce(mockResponse);

      const result = await getAnnualBarChart(mockAuthToken);

      expect(mockRequestAPI).toHaveBeenCalledWith({
        endpoint: 'v1/reports/charts/annual-bar',
        method: 'GET',
        authToken: mockAuthToken,
      });

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response format', async () => {
      const invalidResponse = { invalid: 'data' };
      mockRequestAPI.mockResolvedValueOnce(invalidResponse);

      await expect(getAnnualBarChart(mockAuthToken)).rejects.toThrow(
        'Invalid response format for annual bar chart'
      );
    });
  });

  describe('getLicensingStatusSummary', () => {
    it('should fetch licensing status summary successfully', async () => {
      const mockResponse = {
        consultation: 45,
        initiated: 32,
        under_review: 18,
        issued: 127,
      };

      mockRequestAPI.mockResolvedValueOnce(mockResponse);

      const result = await getLicensingStatusSummary(mockAuthToken);

      expect(mockRequestAPI).toHaveBeenCalledWith({
        endpoint: 'v1/reports/charts/advanced-pie',
        method: 'GET',
        authToken: mockAuthToken,
      });

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response format', async () => {
      const invalidResponse = { invalid: 'data' };
      mockRequestAPI.mockResolvedValueOnce(invalidResponse);

      await expect(getLicensingStatusSummary(mockAuthToken)).rejects.toThrow(
        'Invalid response format for licensing status summary'
      );
    });
  });

  describe('getReviewStatusPie', () => {
    it('should fetch review status data successfully', async () => {
      const mockResponse = {
        approved: 85,
        under_review: 42,
        corrected: 15,
        discarded: 8,
      };

      mockRequestAPI.mockResolvedValueOnce(mockResponse);

      const result = await getReviewStatusPie(mockAuthToken);

      expect(mockRequestAPI).toHaveBeenCalledWith({
        endpoint: 'v1/reports/charts/review-pie',
        method: 'GET',
        authToken: mockAuthToken,
      });

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response format', async () => {
      const invalidResponse = { invalid: 'data' };
      mockRequestAPI.mockResolvedValueOnce(invalidResponse);

      await expect(getReviewStatusPie(mockAuthToken)).rejects.toThrow(
        'Invalid response format for review status pie'
      );
    });
  });

  describe('getCompleteAnalytics', () => {
    it('should fetch and return complete analytics successfully', async () => {
      const mockData = {
        kpis: {
          tiempo_promedio: 8.5,
          eficiencia: 92.5,
          total_procesados: 150,
          satisfaccion: 85.2,
        },
        tendencias: [
          { name: 'Enero', value: 25, extra: 1 },
          { name: 'Febrero', value: 30, extra: 2 },
          { name: 'Marzo', value: 35, extra: 3 },
        ],
        distribucion_estados: [
          {
            estado: 'APROBADO',
            cantidad: 120,
            porcentaje: 80.0,
            color: '#10B981',
          },
          {
            estado: 'PENDIENTE',
            cantidad: 25,
            porcentaje: 16.7,
            color: '#F59E0B',
          },
          {
            estado: 'RECHAZADO',
            cantidad: 5,
            porcentaje: 3.3,
            color: '#EF4444',
          },
        ],
        dependencias: [
          {
            id: 'BOMBEROS',
            nombre: 'Bomberos',
            tramites_procesados: 45,
            tiempo_promedio: 7.2,
            eficiencia: 88.5,
            estado: 'ACTIVO',
          },
          {
            id: 'SIFRA',
            nombre: 'SIFRA',
            tramites_procesados: 30,
            tiempo_promedio: 9.1,
            eficiencia: 82.0,
            estado: 'ACTIVO',
          },
        ],
        licensing_status: {
          consultation: 45,
          initiated: 32,
          under_review: 18,
          issued: 127,
        },
        review_status: {
          approved: 85,
          under_review: 42,
          corrected: 15,
          discarded: 8,
        },
      };

      mockRequestAPI.mockResolvedValueOnce(mockData);

      const result = await getCompleteAnalytics(mockAuthToken);

      expect(mockRequestAPI).toHaveBeenCalledWith({
        endpoint: 'v1/reports/charts/complete-analytics',
        method: 'GET',
        authToken: mockAuthToken,
      });

      expect(result).toEqual(mockData);
    });

    it('should throw error when API call fails', async () => {
      mockRequestAPI.mockRejectedValueOnce(new Error('API Error'));

      await expect(getCompleteAnalytics(mockAuthToken)).rejects.toThrow(
        'Failed to fetch complete analytics data'
      );
    });

    it('should throw error for invalid response format', async () => {
      const invalidData = { invalid: 'data' };
      mockRequestAPI.mockResolvedValueOnce(invalidData);

      await expect(getCompleteAnalytics(mockAuthToken)).rejects.toThrow(
        'Failed to fetch complete analytics data'
      );
    });
  });

  describe('Authentication and Authorization', () => {
    it('should include auth token in all requests', async () => {
      const mockResponse = {
        consultation: 0,
        initiated: 0,
        under_review: 0,
        issued: 0,
      };
      mockRequestAPI.mockResolvedValueOnce(mockResponse);

      await getLicensingStatusSummary(mockAuthToken);

      expect(mockRequestAPI).toHaveBeenCalledWith(
        expect.objectContaining({
          authToken: mockAuthToken,
        })
      );
    });

    it('should handle unauthorized errors', async () => {
      const { UnauthorizedError } = await import('./base');
      mockRequestAPI.mockRejectedValueOnce(new UnauthorizedError());

      await expect(getAnnualBarChart(mockAuthToken)).rejects.toThrow(
        'Unauthorized'
      );
    });
  });

  describe('Data Validation', () => {
    it('should validate ChartPoint schema', async () => {
      const validData = [
        { name: 'Enero', value: 25, extra: 1 },
        { name: 'Febrero', value: 30 }, // extra is optional
      ];

      mockRequestAPI.mockResolvedValueOnce(validData);
      const result = await getAnnualBarChart(mockAuthToken);

      expect(result).toEqual(validData);
    });

    it('should reject invalid ChartPoint data', async () => {
      const invalidData = [
        { name: 'Enero', value: 'invalid' }, // value should be number
      ];

      mockRequestAPI.mockResolvedValueOnce(invalidData);

      await expect(getAnnualBarChart(mockAuthToken)).rejects.toThrow(
        'Invalid response format for annual bar chart'
      );
    });

    it('should validate LicensingStatusSummary schema', async () => {
      const validData = {
        consultation: 45,
        initiated: 32,
        under_review: 18,
        issued: 127,
      };

      mockRequestAPI.mockResolvedValueOnce(validData);
      const result = await getLicensingStatusSummary(mockAuthToken);

      expect(result).toEqual(validData);
    });

    it('should reject incomplete LicensingStatusSummary data', async () => {
      const incompleteData = {
        consultation: 45,
        initiated: 32,
        // missing under_review and issued
      };

      mockRequestAPI.mockResolvedValueOnce(incompleteData);

      await expect(getLicensingStatusSummary(mockAuthToken)).rejects.toThrow(
        'Invalid response format for licensing status summary'
      );
    });
  });
});
