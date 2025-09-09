import type { ApiData } from './api.types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export class UnauthorizedError extends Error {
  constructor(message: string = 'Unauthorized') {
    super(message);
    this.name = 'UnauthorizedError';
  }
}

export async function requestAPI({
  endpoint,
  data,
  method = 'GET',
  authToken,
  skipAuth = false,
  isFormData = false,
}: ApiData & {
  method?: 'POST' | 'GET' | 'PATCH' | 'PUT' | 'DELETE';
  authToken?: string;
  skipAuth?: boolean;
  isFormData?: boolean;
}) {
  const url = new URL(`${API_URL}/${endpoint}`);

  if (method === 'GET' && data) {
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        url.searchParams.append(key, String(value));
      }
    });
  }

  const headers: Record<string, string> = {
    Accept: 'application/json',
  };

  // Only set Content-Type for JSON, let browser set it for FormData
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }

  // Add authorization header if token is provided and auth is not skipped
  if (authToken && !skipAuth) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  let body: string | FormData | undefined;
  if (method === 'POST' || method === 'PATCH' || method === 'PUT') {
    if (isFormData && data instanceof FormData) {
      body = data;
    } else if (!isFormData) {
      body = JSON.stringify(data);
    }
  }

  const response = await fetch(url, {
    method,
    headers,
    body,
  });

  // Check if the response is ok
  if (!response.ok) {
    // Check for unauthorized status
    if (response.status === 401) {
      throw new UnauthorizedError('Unauthorized - Token expired or invalid');
    }

    // Try to parse error as JSON if possible
    let errorData;
    const contentType = response.headers.get('content-type');

    if (contentType?.includes('application/json')) {
      try {
        errorData = await response.json();
      } catch {
        errorData = {
          message: `HTTP ${response.status}: ${response.statusText}`,
        };
      }
    } else {
      // Handle non-JSON errors (like 500 Internal Server Error)
      const errorText = await response.text();
      errorData = {
        message: errorText ?? `HTTP ${response.status}: ${response.statusText}`,
        status: response.status,
      };
    }

    // For validation errors (422), include more detail
    let errorMessage = errorData.message ?? errorData.detail ?? 'Network error';
    if (
      response.status === 422 &&
      errorData.detail &&
      Array.isArray(errorData.detail)
    ) {
      const validationErrors = errorData.detail
        .map((err: unknown) => {
          const error = err as { loc?: (string | number)[]; msg?: string };
          const field = error.loc ? error.loc.join('.') : 'unknown field';
          return `${field}: ${error.msg}`;
        })
        .join(', ');
      errorMessage = `Validation error: ${validationErrors}`;
    }

    // For 500 errors, provide a user-friendly message
    if (response.status === 500) {
      errorMessage =
        'Internal server error. Please try again later or contact support if the problem persists.';
    }

    throw new Error(errorMessage);
  }

  // Handle successful responses
  // For 204 No Content or empty responses, don't try to parse JSON
  if (
    response.status === 204 ||
    response.headers.get('content-length') === '0'
  ) {
    return;
  }

  // Check if response has JSON content
  const contentType = response.headers.get('content-type');
  if (contentType?.includes('application/json')) {
    try {
      return await response.json();
    } catch {
      // If JSON parsing fails on a successful response, return empty object
      return {};
    }
  }

  // For non-JSON successful responses, return the text
  return await response.text();
}
