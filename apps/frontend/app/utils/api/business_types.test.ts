import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import {
  createBusinessType,
  getAllBusinessTypes,
  getBusinessTypes,
  updateBusinessTypeCertificate,
  updateBusinessTypeStatus,
  updateBusinessTypeImpact,
} from './business_types';

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Helper function to create mock response with proper headers
const createMockResponse = (
  data: any,
  options: {
    status?: number;
    headers?: Record<string, string>;
    text?: string;
  } = {}
) => ({
  ok: options.status ? options.status < 400 : true,
  status: options.status || 200,
  headers: {
    get: (key: string) => {
      // Default headers
      const defaultHeaders: Record<string, string> = {
        'content-type': 'application/json',
        'content-length': options.text
          ? options.text.length.toString()
          : JSON.stringify(data).length.toString(),
      };
      return options.headers?.[key] || defaultHeaders[key] || null;
    },
  },
  json: () => Promise.resolve(data),
  text: () => Promise.resolve(options.text || JSON.stringify(data)),
});

describe('business_types', () => {
  const mockApiUrl = process.env.API_URL ?? 'http://localhost';
  const mockAuthToken = 'test-auth-token';

  beforeEach(() => {
    mockFetch.mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getBusinessTypes', () => {
    const mockResponse = [
      {
        business_type_id: 1,
        municipality_id: 1,
        id: 1,
        is_disabled: false,
        has_certificate: true,
        impact_level: 2,
        name: 'Restaurant',
        description: 'Food service establishment',
        code: '722513',
        related_words: 'food, dining, restaurant',
      },
      {
        business_type_id: 2,
        municipality_id: 1,
        id: 2,
        is_disabled: false,
        has_certificate: false,
        impact_level: 1,
        name: 'Retail Store',
        description: 'General retail establishment',
        code: '468111',
        related_words: 'store, retail, shop',
      },
    ];

    it('should fetch business types successfully and return parsed data', async () => {
      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getBusinessTypes({ municipality_id: 1 });

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/enabled?municipality_id=1`),
        {
          method: 'GET',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: undefined,
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should return empty array when response validation fails', async () => {
      const invalidResponse = [
        {
          business_type_id: 'invalid',
          municipality_id: 1,
        },
      ];

      mockFetch.mockResolvedValueOnce(createMockResponse(invalidResponse));

      const result = await getBusinessTypes({ municipality_id: 1 });

      expect(result).toEqual([]);
    });

    it('should handle network errors', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      await expect(getBusinessTypes({ municipality_id: 1 })).rejects.toThrow(
        'Network error'
      );
    });

    it('should handle HTTP errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        headers: {
          get: () => 'application/json',
        },
        json: async () => ({ message: 'Not found' }),
      });

      await expect(getBusinessTypes({ municipality_id: 1 })).rejects.toThrow(
        'Not found'
      );
    });
  });

  describe('getAllBusinessTypes', () => {
    const mockResponse = [
      {
        business_type_id: 1,
        municipality_id: 1,
        id: 1,
        is_disabled: false,
        has_certificate: true,
        impact_level: 2,
        name: 'Restaurant',
        description: 'Food service establishment',
        code: '722513',
        related_words: 'food, dining, restaurant',
      },
    ];

    it('should fetch all business types successfully with auth token', async () => {
      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getAllBusinessTypes(mockAuthToken);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/all`),
        {
          method: 'GET',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          },
          body: undefined,
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should return empty array and log error when schema validation fails', async () => {
      const invalidResponse = [{ invalid: 'data' }];
      const consoleSpy = vi
        .spyOn(console, 'error')
        .mockImplementation(() => {});

      mockFetch.mockResolvedValueOnce(createMockResponse(invalidResponse));

      const result = await getAllBusinessTypes(mockAuthToken);

      expect(result).toEqual([]);
      expect(consoleSpy).toHaveBeenCalledWith(
        'Failed to parse business types:',
        expect.any(Object)
      );

      consoleSpy.mockRestore();
    });
  });

  describe('createBusinessType', () => {
    const mockData = {
      name: 'New Business Type',
      description: 'A new type of business',
      code: '123456',
      related_words: 'new, business, type',
      is_active: true,
    };

    it('should create business type successfully', async () => {
      const mockResponse = { success: true, id: 123 };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await createBusinessType(mockData, mockAuthToken);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/`),
        {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          },
          body: JSON.stringify(mockData),
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should handle creation errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        headers: {
          get: () => 'application/json',
        },
        json: async () => ({ detail: 'Validation error' }),
      });

      await expect(createBusinessType(mockData, mockAuthToken)).rejects.toThrow(
        'Validation error'
      );
    });
  });

  describe('updateBusinessTypeStatus', () => {
    const mockData = {
      business_type_id: 1,
      municipality_id: 1,
    };

    it('should update business type status successfully', async () => {
      const mockResponse = { success: true };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const mockData = { business_type_id: 1 };

      const result = await updateBusinessTypeStatus(1, mockData, mockAuthToken);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/disable/status/1`),
        {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          },
          body: JSON.stringify(mockData),
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should handle status false', async () => {
      const mockResponse = { success: true };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      await updateBusinessTypeStatus(0, mockData, mockAuthToken);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/disable/status/0`),
        expect.any(Object)
      );
    });

    it('should throw error for invalid data', async () => {
      const invalidData = {
        business_type_id: 'invalid',
        municipality_id: 1,
      };

      await expect(
        updateBusinessTypeStatus(1, invalidData as never, mockAuthToken)
      ).rejects.toThrow('Invalid request body for updateBusinessTypeStatus');
    });

    it('should handle server errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        headers: {
          get: () => 'text/plain',
        },
        text: async () => 'Internal server error',
      });

      await expect(
        updateBusinessTypeStatus(1, mockData, mockAuthToken)
      ).rejects.toThrow('Internal server error');
    });
  });

  describe('updateBusinessTypeCertificate', () => {
    const mockData = {
      business_type_id: 1,
      municipality_id: 1,
      status: true,
    };

    it('should update business type certificate successfully', async () => {
      const mockResponse = { success: true };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const mockData = { business_type_id: 1, status: true };

      const result = await updateBusinessTypeCertificate(
        1,
        mockData,
        mockAuthToken
      );

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/disable/certificate/1`),
        {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          },
          body: JSON.stringify(mockData),
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should handle certificate status false', async () => {
      const mockResponse = { success: true };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const mockDataFalse = { business_type_id: 1, status: false };

      await updateBusinessTypeCertificate(1, mockDataFalse, mockAuthToken);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/disable/certificate/1`),
        {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          },
          body: JSON.stringify(mockDataFalse),
        }
      );
    });

    it('should throw error for invalid data', async () => {
      const invalidData = { business_type_id: 'invalid', status: true };

      await expect(
        updateBusinessTypeCertificate(1, invalidData as never, mockAuthToken)
      ).rejects.toThrow(
        'Invalid request body for updateBusinessTypeCertificate'
      );
    });

    it('should handle unauthorized errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        headers: {
          get: () => 'application/json',
        },
        json: async () => ({ message: 'Unauthorized' }),
      });

      const mockData = { business_type_id: 1, status: true };

      await expect(
        updateBusinessTypeCertificate(1, mockData, mockAuthToken)
      ).rejects.toThrow('Unauthorized - Token expired or invalid');
    });
  });

  describe('updateBusinessTypeImpact', () => {
    const mockData = {
      business_type_id: 1,
      impact_level: 3,
    };

    it('should update business type impact successfully', async () => {
      const mockResponse = { success: true };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await updateBusinessTypeImpact(mockData, mockAuthToken);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/business_types/impact`),
        {
          method: 'PATCH',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          },
          body: JSON.stringify(mockData),
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid data', async () => {
      const invalidData = {
        business_type_id: 'invalid',
        impact_level: 'invalid',
      };

      await expect(
        updateBusinessTypeImpact(invalidData as never, mockAuthToken)
      ).rejects.toThrow('Invalid request body for updateBusinessTypeImpact');
    });

    it('should handle server errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        headers: {
          get: () => 'text/plain',
        },
        text: async () => 'Internal server error',
      });

      await expect(
        updateBusinessTypeImpact(mockData, mockAuthToken)
      ).rejects.toThrow('Internal server error');
    });
  });
});
