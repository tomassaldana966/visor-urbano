import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';

const mockApiUrl = process.env.API_URL;

import {
  UnauthorizedError,
  register,
  login,
  getMapLayers,
  getTechnicalSheetURL,
  getNotifications,
  markNotificationAsRead,
  getProcedureFiles,
  getProcedures,
  createProcedure,
  getMunicipalities,
  searchByAddress,
  validateFolio,
  uploadProcedureFile,
  getRoles,
  getUsers,
  exportBusinessLicenses,
  uploadPaymentReceipt,
  getProcedureInfo,
  postRequirementsQueries,
} from './api.server';

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock btoa for base64 encoding
global.btoa = vi.fn((str: string) => Buffer.from(str).toString('base64'));

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

describe('api.server', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('UnauthorizedError', () => {
    it('should create an error with correct properties', () => {
      const error = new UnauthorizedError('Custom message');
      expect(error.name).toBe('UnauthorizedError');
      expect(error.message).toBe('Custom message');
    });

    it('should use default message when none provided', () => {
      const error = new UnauthorizedError();
      expect(error.message).toBe('Unauthorized');
    });
  });

  describe('register', () => {
    it('should register a user successfully', async () => {
      const userData = {
        cellphone: '1234567890',
        email: 'test@example.com',
        maternal_last_name: 'Martinez',
        municipality_id: '1',
        name: 'John',
        password: 'password123',
        paternal_last_name: 'Doe',
      };

      const mockResponse = { id: 1, email: 'test@example.com' };
      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await register(userData);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/users`),
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
          body: JSON.stringify({
            ...userData,
            municipality_id: 1,
          }),
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('should return undefined when no data provided', async () => {
      const result = await register();
      expect(result).toBeUndefined();
      expect(mockFetch).not.toHaveBeenCalled();
    });

    it('should handle fetch errors', async () => {
      const userData = {
        cellphone: '1234567890',
        email: 'test@example.com',
        maternal_last_name: 'Martinez',
        municipality_id: '1',
        name: 'John',
        password: 'password123',
        paternal_last_name: 'Doe',
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        headers: new Headers({ 'content-type': 'application/json' }),
        json: () => Promise.resolve({ message: 'Invalid data' }),
      });

      await expect(register(userData)).rejects.toThrow('Invalid data');
    });
  });

  describe('login', () => {
    it('should login successfully with valid credentials', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123',
      };

      const mockResponse = {
        access_token: 'mock-token',
        user: {
          id: 1,
          name: 'John Doe',
          email: 'test@example.com',
          role_name: 'admin',
          role_id: 1,
          municipality_id: 1,
        },
      };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await login(loginData);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/auth/login`),
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
          body: JSON.stringify(loginData),
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('should return null for invalid response format', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123',
      };

      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await login(loginData);
      expect(result).toBeNull();
    });

    it('should return undefined when no data provided', async () => {
      const result = await login();
      expect(result).toBeUndefined();
      expect(mockFetch).not.toHaveBeenCalled();
    });
  });

  describe('getMapLayers', () => {
    it('should fetch and sort map layers correctly', async () => {
      const municipality = 1;
      const mockResponse = [
        {
          active: true,
          attribution: 'Test Attribution',
          cql_filter: null,
          editable: false,
          format: 'image/png',
          id: 1,
          label: 'Layer 1',
          layers: 'test_layer',
          municipality_ids: [1],
          opacity: 1,
          order: 2,
          projection: 'EPSG:4326',
          server_type: 'geoserver',
          type_geom: 'polygon',
          type: 'WMS',
          url: 'https://example.com/geoserver',
          value: 'layer1',
          version: '1.1.0',
          visible: true,
        },
        {
          active: true,
          attribution: 'Test Attribution 2',
          cql_filter: null,
          editable: false,
          format: 'image/png',
          id: 2,
          label: 'Layer 2',
          layers: 'test_layer_2',
          municipality_ids: [1],
          opacity: 1,
          order: 1,
          projection: 'EPSG:4326',
          server_type: 'geoserver',
          type_geom: 'point',
          type: 'WMS',
          url: 'https://example.com/geoserver',
          value: 'layer2',
          version: '1.1.0',
          visible: true,
        },
      ];

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getMapLayers({ municipality });

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(URL),
        expect.objectContaining({
          method: 'GET',
        })
      );

      // Should sort by order (layer with order 1 should come first)
      expect(result).toHaveLength(2);
      expect(result![0].order).toBe(1);
      expect(result![1].order).toBe(2);
    });

    it('should handle invalid response format', async () => {
      const municipality = 1;
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getMapLayers({ municipality });
      expect(result).toBeUndefined();
    });
  });

  describe('getTechnicalSheetURL', () => {
    it('should return technical sheet URL on success', async () => {
      const data = {
        address: 'Test Address',
        square_meters: '100',
        coordinates: '10,20',
        image: 'base64image',
        municipality_id: 1,
        technical_sheet_download_id: 123,
      };

      const mockResponse = { uuid: 'test-uuid-123' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getTechnicalSheetURL(data);

      expect(mockFetch).toHaveBeenCalledWith(
        new URL(`${mockApiUrl}/v1/technical_sheets`),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(data),
        })
      );
      expect(result).toBe('/technical-sheet/test-uuid-123');
    });

    it('should return null for invalid response', async () => {
      const data = {
        address: 'Test Address',
        square_meters: '100',
        coordinates: '10,20',
        image: 'base64image',
        municipality_id: 1,
        technical_sheet_download_id: 123,
      };

      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getTechnicalSheetURL(data);
      expect(result).toBeNull();
    });
  });

  describe('getNotifications', () => {
    it('should fetch notifications successfully', async () => {
      const authToken = 'mock-token';
      const params = { page: 1, per_page: 10 };

      const mockResponse = {
        notifications: [
          {
            id: 1,
            user_id: 1,
            applicant_email: 'test@example.com',
            comment: 'Test comment',
            folio: 'FOL-123',
            creation_date: '2023-01-01T00:00:00Z',
            seen_date: null,
            dependency_file: null,
            notified: 1,
            notifying_department: 1,
            notification_type: 1,
            resolution_id: 1,
            created_at: '2023-01-01T00:00:00Z',
            updated_at: '2023-01-01T00:00:00Z',
          },
        ],
        total_count: 1,
        page: 1,
        per_page: 10,
        has_next: false,
        has_prev: false,
      };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getNotifications(authToken, params);

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(URL),
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            Authorization: `Bearer ${authToken}`,
          }),
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response format', async () => {
      const authToken = 'mock-token';
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      await expect(getNotifications(authToken)).rejects.toThrow(
        'Invalid response format for notifications'
      );
    });
  });

  describe('markNotificationAsRead', () => {
    it('should mark notification as read successfully', async () => {
      const authToken = 'mock-token';
      const notificationId = 1;

      const mockResponse = {
        message: 'Notification marked as read',
        status_code: 200,
      };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await markNotificationAsRead(authToken, notificationId);

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response', async () => {
      const authToken = 'mock-token';
      const notificationId = 1;
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      await expect(
        markNotificationAsRead(authToken, notificationId)
      ).rejects.toThrow('Invalid response format for mark as read');
    });
  });

  describe('getProcedureFiles', () => {
    it('should fetch procedure files successfully', async () => {
      const authToken = 'mock-token';
      const procedureId = 1;

      const mockResponse = [
        {
          id: 1,
          procedure_id: 1,
          file_path: '/path/to/file.pdf',
          file_type: 'application/pdf',
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
      ];

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getProcedureFiles(authToken, procedureId);

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response format', async () => {
      const authToken = 'mock-token';
      const procedureId = 1;
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      await expect(getProcedureFiles(authToken, procedureId)).rejects.toThrow(
        'Invalid response format for procedure files'
      );
    });
  });

  describe('getProcedures', () => {
    it('should fetch procedures successfully', async () => {
      const authToken = 'mock-token';
      const params = { folio: 'FOL-123', page: 1, per_page: 10 };

      const mockResponse = [
        {
          id: 1,
          folio: 'FOL-123',
          official_applicant_name: 'John Doe',
          procedure_type: 'business_license',
          current_step: 1,
          status: 1,
          license_status: 'pending',
          procedure_start_date: '2023-01-01T00:00:00Z',
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await getProcedures(authToken, params);

      expect(result).toEqual(mockResponse);
    });

    it('should handle fetch errors', async () => {
      const authToken = 'mock-token';

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        text: () => Promise.resolve('Internal Server Error'),
      });

      await expect(getProcedures(authToken)).rejects.toThrow(
        'Failed to fetch procedures: 500 Internal Server Error'
      );
    });
  });

  describe('getMunicipalities', () => {
    it('should fetch municipalities successfully', async () => {
      const mockResponse = [
        {
          id: 1,
          name: 'Test Municipality',
          image: 'test-image.jpg',
          director: 'John Director',
          director_signature: 'signature.jpg',
          process_sheet: 1,
          signatures: [],
          solving_days: 30,
          issue_license: 1,
          address: '123 City Hall Ave',
          phone: '+1234567890',
          responsible_area: 'Planning Department',
          window_license_generation: 1,
          license_restrictions: 'Standard restrictions',
          license_price: '100.00',
          initial_folio: 1000,
          has_zoning: true,
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
          deleted_at: null,
          email: 'admin@testmunicipality.gov',
          website: 'https://testmunicipality.gov',
          allow_online_procedures: true,
          allow_window_reviewer_licenses: true,
          low_impact_license_cost: '50.00',
          license_additional_text: 'Additional license information',
          theme_color: '#0066CC',
        },
      ];

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getMunicipalities();

      expect(result).toEqual(mockResponse);
    });

    it('should return empty array for invalid response', async () => {
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getMunicipalities();
      expect(result).toEqual([]);
    });
  });

  describe('searchByAddress', () => {
    it('should search address successfully', async () => {
      const data = {
        address: '123 Main St',
        municipality: 'Test Municipality',
      };

      const mockResponse = {
        address_components: [
          {
            long_name: '123',
            short_name: '123',
            types: ['street_number'],
          },
          {
            long_name: 'Main Street',
            short_name: 'Main St',
            types: ['route'],
          },
        ],
        formatted_address: '123 Main St, Test Municipality',
        geometry: {
          bounds: {
            northeast: { lat: 40.7129, lng: -74.0059 },
            southwest: { lat: 40.7127, lng: -74.0061 },
          },
          location: { lat: 40.7128, lng: -74.006 },
          location_type: 'ROOFTOP',
          viewport: {
            northeast: { lat: 40.7129, lng: -74.0059 },
            southwest: { lat: 40.7127, lng: -74.0061 },
          },
        },
        partial_match: false,
        place_id: 'ChIJd8BlQ2BZwokRAFQEcgEdHDA',
        types: ['street_address'],
      };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await searchByAddress(data);

      expect(result).toEqual(mockResponse);
    });

    it('should return null for invalid response', async () => {
      const data = {
        address: '123 Main St',
        municipality: 'Test Municipality',
      };

      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await searchByAddress(data);
      expect(result).toBeNull();
    });
  });

  describe('createProcedure', () => {
    it('should create procedure successfully', async () => {
      const authToken = 'mock-token';
      const procedureData = {
        folio: 'FOL-123',
        requirements_query_id: 1,
        status: 1,
        current_step: 1,
        businessType: 1,
      };

      const mockResponse = {
        id: 1,
        folio: 'FOL-123',
        status: 1,
        current_step: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await createProcedure(authToken, procedureData);

      expect(mockFetch).toHaveBeenCalledWith(
        `${mockApiUrl}/v1/procedures/entry`,
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            Authorization: `Bearer ${authToken}`,
            'Content-Type': 'application/json',
          }),
          body: expect.stringContaining('"folio":"FOL-123"'),
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('should handle duplicate procedure error', async () => {
      const authToken = 'mock-token';
      const procedureData = {
        folio: 'FOL-123',
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 409,
        text: () => Promise.resolve('Procedure already exists'),
      });

      await expect(createProcedure(authToken, procedureData)).rejects.toThrow(
        'DUPLICATE_PROCEDURE: Procedure already exists'
      );
    });
  });

  describe('uploadProcedureFile', () => {
    it('should upload file successfully', async () => {
      const authToken = 'mock-token';
      const folio = 'FOL-123';
      const fieldName = 'document';
      const file = new File(['test content'], 'test.pdf', {
        type: 'application/pdf',
      });

      const mockResponse = {
        filename: 'test.pdf',
        size: 1024,
        file_path: '/uploads/test.pdf',
        content_type: 'application/pdf',
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await uploadProcedureFile(
        authToken,
        folio,
        fieldName,
        file
      );

      expect(result).toEqual(mockResponse);
    });

    it('should handle upload errors', async () => {
      const authToken = 'mock-token';
      const folio = 'FOL-123';
      const fieldName = 'document';
      const file = new File(['test content'], 'test.pdf', {
        type: 'application/pdf',
      });

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        text: () => Promise.resolve('Bad Request'),
      });

      await expect(
        uploadProcedureFile(authToken, folio, fieldName, file)
      ).rejects.toThrow('Failed to upload file: 400 Bad Request');
    });
  });

  describe('getRoles', () => {
    it('should fetch roles successfully', async () => {
      const authToken = 'mock-token';
      const mockResponse = [
        {
          id: 1,
          name: 'Admin',
          description: 'Administrator role',
          municipality_id: 1,
          deleted_at: null,
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
      ];

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getRoles(authToken);

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response', async () => {
      const authToken = 'mock-token';
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      await expect(getRoles(authToken)).rejects.toThrow(
        'Invalid response format for roles'
      );
    });
  });

  describe('getUsers', () => {
    it('should fetch users successfully', async () => {
      const authToken = 'mock-token';
      const params = { search: 'john', role: 'admin' };

      const mockResponse = [
        {
          id: 1,
          name: 'John',
          paternal_last_name: 'Doe',
          maternal_last_name: 'Smith',
          cellphone: '+1234567890',
          email: 'john@example.com',
          role_name: 'admin',
          municipality_data: null,
          municipality_geospatial: null,
        },
      ];

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await getUsers(authToken, params);

      expect(result).toEqual(mockResponse);
    });

    it('should throw error for invalid response', async () => {
      const authToken = 'mock-token';
      const mockResponse = { invalid: 'response' };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      await expect(getUsers(authToken)).rejects.toThrow(
        'Invalid response format for users'
      );
    });
  });

  describe('validateFolio', () => {
    it('should validate folio successfully', async () => {
      const authToken = 'mock-token';
      const folio = 'FOL-123';

      const mockResponse = [
        { requirement: 'Document 1', status: 'pending' },
        { requirement: 'Document 2', status: 'completed' },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await validateFolio(authToken, folio);

      expect(global.btoa).toHaveBeenCalledWith(folio);
      expect(result).toEqual(mockResponse);
    });

    it('should return empty array for non-array response', async () => {
      const authToken = 'mock-token';
      const folio = 'FOL-123';

      const mockResponse = { message: 'Not found' };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await validateFolio(authToken, folio);
      expect(result).toEqual([]);
    });
  });

  describe('Unauthorized error handling', () => {
    it('should throw UnauthorizedError for 401 responses', async () => {
      const authToken = 'invalid-token';

      // Mock needs to be called twice since we have two expectations
      mockFetch
        .mockResolvedValueOnce({
          ok: false,
          status: 401,
          statusText: 'Unauthorized',
          headers: new Headers({ 'content-type': 'application/json' }),
          json: () => Promise.resolve({ message: 'Unauthorized access' }),
        })
        .mockResolvedValueOnce({
          ok: false,
          status: 401,
          statusText: 'Unauthorized',
          headers: new Headers({ 'content-type': 'application/json' }),
          json: () => Promise.resolve({ message: 'Unauthorized access' }),
        });

      await expect(getNotifications(authToken)).rejects.toThrow(
        UnauthorizedError
      );
      await expect(getNotifications(authToken)).rejects.toThrow(
        'Unauthorized - Token expired or invalid'
      );
    });
  });

  describe('Error handling for non-JSON responses', () => {
    it('should handle non-JSON error responses', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        headers: new Headers({ 'content-type': 'text/html' }),
        text: () => Promise.resolve('Internal Server Error Page'),
      });

      await expect(getMunicipalities()).rejects.toThrow(
        'Internal server error. Please try again later or contact support if the problem persists.'
      );
    });

    it('should handle responses with no content-type', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        headers: new Headers(),
        text: () => Promise.resolve(null),
      });

      await expect(getMunicipalities()).rejects.toThrow(
        'Internal server error. Please try again later or contact support if the problem persists.'
      );
    });
  });

  describe('FormData handling', () => {
    it('should handle FormData uploads correctly', async () => {
      const authToken = 'mock-token';
      const licenseFolio = 'LIC-123';
      const file = new File(['receipt content'], 'receipt.pdf', {
        type: 'application/pdf',
      });

      const mockResponse = { file_path: '/uploads/receipt.pdf' };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await uploadPaymentReceipt(authToken, licenseFolio, file);

      expect(global.btoa).toHaveBeenCalledWith(licenseFolio);
      expect(mockFetch).toHaveBeenCalledWith(
        `${mockApiUrl}/v1/business_licenses/TElDLTEyMw==/upload_receipt`,
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            Authorization: `Bearer ${authToken}`,
          }),
          body: expect.any(FormData),
        })
      );
      expect(result).toBe('/uploads/receipt.pdf');
    });
  });

  describe('Base64 encoding for folios', () => {
    it('should encode folios for API calls', async () => {
      const authToken = 'mock-token';
      const folio = 'FOL-123/456';

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({}),
      });

      await getProcedureInfo(authToken, folio);

      expect(global.btoa).toHaveBeenCalledWith(folio);
    });
  });

  describe('Query parameter handling', () => {
    it('should handle GET requests with query parameters', async () => {
      const municipality = 5;

      mockFetch.mockResolvedValueOnce(createMockResponse([]));

      await getMapLayers({ municipality });

      expect(mockFetch).toHaveBeenCalledWith(expect.any(URL), {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: undefined,
      });
    });
  });

  describe('Export functions', () => {
    it('should handle blob responses for exports', async () => {
      const authToken = 'mock-token';
      const municipality_id = 1;

      const mockBlob = new Blob(['mock excel data'], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });

      mockFetch.mockResolvedValueOnce({
        ok: true,
        blob: () => Promise.resolve(mockBlob),
      });

      const result = await exportBusinessLicenses({
        municipality_id,
        authToken,
      });

      expect(result).toBe(mockBlob);
      expect(mockFetch).toHaveBeenCalledWith(
        `${mockApiUrl}/v1/business_licenses/export?municipality_id=1`,
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            Authorization: `Bearer ${authToken}`,
            Accept:
              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          }),
        })
      );
    });
  });

  describe('postRequirementsQueries', () => {
    it('should handle commercial requirements', async () => {
      const data = {
        municipality_id: '1',
        license_type: 'commercial' as const,
        activity_area: '100',
        activity_description: 'Restaurant',
        alcohol_sales: '0',
        applicant_character: 'Owner',
        applicant_name: 'John Doe',
        street: 'Main Street',
        neighborhood: 'Downtown',
        municipality_name: 'Test City',
      };

      const mockResponse = {
        data: {
          folio: 'FOL-123',
          url: '/requirements/FOL-123',
          issue_license: 1,
        },
        message: 'Requirements processed successfully',
      };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await postRequirementsQueries(data);

      expect(mockFetch).toHaveBeenCalledWith(expect.any(URL), {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          municipality_id: 1,
          license_type: 'commercial',
          activity_area: 100,
          activity_description: 'Restaurant',
          alcohol_sales: 0,
          applicant_character: 'Owner',
          applicant_name: 'John Doe',
          street: 'Main Street',
          neighborhood: 'Downtown',
          municipality_name: 'Test City',
        }),
      });

      expect(result).toEqual({
        data: mockResponse.data,
        message: mockResponse.message,
        url: mockResponse.data.url,
        folio: mockResponse.data.folio,
        issue_license: mockResponse.data.issue_license,
      });
    });

    it('should handle construction requirements', async () => {
      const data = {
        municipality_id: '1',
        license_type: 'construction' as const,
        street: 'Main Street',
        neighborhood: 'Downtown',
        municipality_name: 'Test City',
        interested_party: 'Property Owner',
      };

      const mockResponse = {
        data: {
          folio: 'CON-123',
          url: '/requirements/CON-123',
          issue_license: 0,
        },
        message: 'Construction requirements processed',
      };

      mockFetch.mockResolvedValueOnce(createMockResponse(mockResponse));

      const result = await postRequirementsQueries(data);

      expect(result).toEqual({
        data: mockResponse.data,
        message: mockResponse.message,
        url: mockResponse.data.url,
        folio: mockResponse.data.folio,
        issue_license: mockResponse.data.issue_license,
      });
    });

    it('should handle errors gracefully', async () => {
      const data = {
        municipality_id: '1',
        license_type: 'commercial' as const,
        activity_area: '100',
        activity_description: 'Restaurant',
        alcohol_sales: '0',
        applicant_character: 'Owner',
        applicant_name: 'John Doe',
      };

      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await postRequirementsQueries(data);
      expect(result).toBeNull();
    });
  });
});
