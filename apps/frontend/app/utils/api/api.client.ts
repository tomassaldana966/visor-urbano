// Client-side API functions for use in React components
import type {
  BusinessCommercialProcedureData,
  ConstructionProcedureData,
} from '@root/app/types/procedures';

// Types for API responses
export interface BusinessCommercialProceduresResponse {
  procedures: BusinessCommercialProcedureData[];
  total: number;
  page: number;
  limit: number;
}

export interface ConstructionProceduresResponse {
  procedures: ConstructionProcedureData[];
  total: number;
  page: number;
  limit: number;
}

export interface BusinessLicense {
  id: number;
  owner: string;
  license_folio: string;
  commercial_activity: string;
  industry_classification_code: string;
  authorized_area: string;
  opening_time: string;
  closing_time: string;
  owner_last_name_p?: string;
  owner_last_name_m?: string;
  national_id?: string;
  owner_profile?: string;
  logo_image?: string;
  signature?: string;
  minimap_url?: string;
  scanned_pdf?: string;
  license_year?: number;
  license_category?: number;
  generated_by_user_id?: number;
  payment_status?: number;
  payment_user_id?: number;
  deactivation_status?: number;
  payment_date?: string;
  deactivation_date?: string;
  secondary_folio?: string;
  deactivation_reason?: string;
  deactivated_by_user_id?: number;
  signer_name_1?: string;
  department_1?: string;
  signature_1?: string;
  signer_name_2?: string;
  department_2?: string;
  signature_2?: string;
  signer_name_3?: string;
  department_3?: string;
  signature_3?: string;
  signer_name_4?: string;
  department_4?: string;
  signature_4?: string;
  license_number?: number;
  municipality_id?: number;
  license_type?: string;
  license_status?: string;
  reason?: string;
  reason_file?: string;
  status_change_date?: string;
  observations?: string;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
}

export interface BusinessLicensesResponse {
  items: BusinessLicense[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface PaginatedBusinessLicenseData {
  items: BusinessLicense[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

// Client-side API functions
export async function getBusinessLicensesListClient(params?: {
  page?: number;
  per_page?: number;
  search?: string;
  municipality_id?: number;
}): Promise<BusinessLicensesResponse> {
  const searchParams = new URLSearchParams();

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, String(value));
      }
    });
  }

  const url = searchParams.toString()
    ? `/v1/business_licenses/public?${searchParams}`
    : `/v1/business_licenses/public`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function getBusinessCommercialProceduresClient(
  authToken: string,
  params: {
    municipality_id?: number;
    user_id?: number;
    status?: number;
    limit?: number;
    offset?: number;
  } = {}
): Promise<BusinessCommercialProceduresResponse> {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      searchParams.append(key, String(value));
    }
  });

  const response = await fetch(
    `/v1/business_commercial_procedures/?${searchParams}`,
    {
      headers: {
        Authorization: `Bearer ${authToken}`,
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function getConstructionProceduresClient(
  authToken: string,
  params: {
    municipality_id?: number;
    user_id?: number;
    status?: number;
    limit?: number;
    offset?: number;
  } = {}
): Promise<ConstructionProceduresResponse> {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      searchParams.append(key, String(value));
    }
  });

  const response = await fetch(`/v1/construction_procedures/?${searchParams}`, {
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Upload a file for a procedure field (client-side)
 */
export async function uploadProcedureFile(
  authToken: string,
  folio: string,
  fieldName: string,
  file: File
): Promise<{
  success: boolean;
  file_path?: string;
  message?: string;
  error?: string;
}> {
  try {
    const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';

    const formData = new FormData();
    formData.append('files', file);
    formData.append('field_names', fieldName);

    const encodedFolio = btoa(folio);
    const response = await fetch(
      `${API_URL}/v1/procedures/upload_documents/${encodedFolio}`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
        body: formData,
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Upload failed: ${response.status} ${errorText}`);
    }

    const result = await response.json();
    return {
      success: true,
      file_path: result.uploaded_files?.[fieldName]?.file_path,
      message: result.message,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown upload error',
    };
  }
}

export async function exportBusinessLicenses({
  municipality_id,
  authToken,
}: {
  municipality_id: number;
  authToken: string;
}): Promise<Blob> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';

  const url = new URL(`${API_URL}/v1/business_licenses/export`);
  url.searchParams.append('municipality_id', municipality_id.toString());

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
      Accept:
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to export business licenses: ${response.status} ${errorText}`
    );
  }

  return response.blob();
}

export async function getBusinessLicenses({
  municipality_id,
  page = 1,
  per_page = 20,
  authToken,
}: {
  municipality_id: number;
  page?: number;
  per_page?: number;
  authToken: string;
}): Promise<PaginatedBusinessLicenseData> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  const url = new URL(`${API_URL}/v1/business_licenses/`);

  url.searchParams.append('municipality_id', municipality_id.toString());
  url.searchParams.append('page', page.toString());
  url.searchParams.append('per_page', per_page.toString());

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to get business licenses: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  return data;
}

export async function updateBusinessLicensePayment({
  license_folio,
  payment_status,
  payment_receipt_file,
  authToken,
}: {
  license_folio: string;
  payment_status: number;
  payment_receipt_file?: string;
  authToken: string;
}): Promise<{ message: string }> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(license_folio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/payment`
  );

  const response = await fetch(url.toString(), {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      payment_status,
      payment_receipt_file,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to update payment status: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function uploadPaymentReceipt(
  authToken: string,
  licenseFolio: string,
  receiptFile: File
): Promise<string> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  const formData = new FormData();
  formData.append('file', receiptFile);

  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/upload_receipt`
  );

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
      // Don't set Content-Type header for FormData
    },
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to upload receipt: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  return data.file_path;
}

export async function downloadLicensePdf(
  authToken: string,
  licenseFolio: string
): Promise<Blob> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/download_license`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('No license PDF found for this license');
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to download license: ${response.status} ${errorText}`
    );
  }

  return response.blob();
}

// License status update functions
export async function updateBusinessLicenseStatus({
  license_folio,
  license_status,
  reason,
  reason_file,
  authToken,
}: {
  license_folio: string;
  license_status: string;
  reason?: string;
  reason_file?: string;
  authToken: string;
}): Promise<{ message: string; license: any }> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(license_folio);
  const url = new URL(`${API_URL}/v1/business_licenses/${encodedFolio}/status`);

  const response = await fetch(url.toString(), {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      license_status,
      reason,
      reason_file,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to update license status: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function uploadStatusFile(
  authToken: string,
  licenseFolio: string,
  statusFile: File
): Promise<string> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  const formData = new FormData();
  formData.append('file', statusFile);

  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/upload_status_file`
  );

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
      // Don't set Content-Type header for FormData
    },
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to upload status file: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  return data.file_path;
}

// Get license status history
export async function getLicenseStatusHistory(
  authToken: string,
  licenseFolio: string
): Promise<{
  license_folio: string;
  current_status: string;
  status_history: Array<{
    id: number;
    previous_status: string | null;
    new_status: string;
    reason: string | null;
    reason_file: string | null;
    changed_by_user_id: number | null;
    changed_by_user: {
      id: number;
      name: string;
      role_name: string;
    } | null;
    changed_at: string | null;
    created_at: string | null;
  }>;
}> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/status_history`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to get status history: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

/**
 * Issue a license by uploading a scanned PDF (client-side)
 */
export async function issueLicenseScanned(
  encodedFolio: string,
  formData: FormData,
  authToken: string
): Promise<any> {
  if (!authToken) {
    throw new Error('No auth token found');
  }

  const response = await fetch(`/v1/procedures/issue-license/${encodedFolio}`, {
    method: 'POST',
    body: formData,
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to issue license');
  }

  return response.json();
}

/**
 * Generate a license automatically by the system (client-side)
 */
export async function generateLicense(
  encodedFolio: string,
  authToken: string,
  licenseData?: {
    opening_time?: string;
    closing_time?: string;
    authorized_area?: string;
    license_cost?: string;
    observations?: string;
    signature_ids?: number[];
  }
): Promise<any> {
  if (!authToken) {
    throw new Error('No auth token found');
  }

  const response = await fetch(
    `/v1/procedures/generate-license/${encodedFolio}`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authToken}`,
        'Content-Type': 'application/json',
      },
      body: licenseData ? JSON.stringify(licenseData) : undefined,
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to generate license');
  }

  return response.json();
}

/**
 * Get all issued licenses (client-side)
 */
export async function getIssuedLicenses(params?: {
  page?: number;
  per_page?: number;
}): Promise<any[]> {
  const authToken = localStorage.getItem('authToken');

  if (!authToken) {
    throw new Error('No auth token found');
  }

  const url = new URL('/v1/procedures/licenses-issued', window.location.origin);

  if (params?.page) {
    url.searchParams.append('page', params.page.toString());
  }
  if (params?.per_page) {
    url.searchParams.append('per_page', params.per_page.toString());
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch issued licenses');
  }

  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

/**
 * Download a license PDF (client-side)
 */
export async function downloadLicense(licenseId: string): Promise<void> {
  const authToken = localStorage.getItem('authToken');

  if (!authToken) {
    throw new Error('No auth token found');
  }

  const response = await fetch(`/v1/procedures/license/${licenseId}/download`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to download license');
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `license-${licenseId}.pdf`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

/**
 * Download a procedure license PDF directly from URL
 */
export async function downloadProcedureLicense(
  licenseUrl: string,
  filename?: string
): Promise<void> {
  try {
    // Handle relative URLs by adding the API base URL
    const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
    const fullUrl = licenseUrl.startsWith('http')
      ? licenseUrl
      : `${API_URL}${licenseUrl.startsWith('/') ? '' : '/'}${licenseUrl}`;

    const response = await fetch(fullUrl);

    if (!response.ok) {
      throw new Error('Failed to download license');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `license-${Date.now()}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    // Fallback: try to open in new window with full URL
    const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
    const fullUrl = licenseUrl.startsWith('http')
      ? licenseUrl
      : `${API_URL}${licenseUrl.startsWith('/') ? '' : '/'}${licenseUrl}`;
    window.open(fullUrl, '_blank');
  }
}

/**
 * Approve a procedure
 */
export async function approveProcedure(
  folio: string,
  authToken: string
): Promise<any> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(folio);
  const url = new URL(`${API_URL}/v1/procedures/approve/${encodedFolio}`);

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to approve procedure');
  }

  return response.json();
}

/**
 * Reject a procedure
 */
export async function rejectProcedure(
  folio: string,
  authToken: string
): Promise<any> {
  const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
  // Base64-encode the folio to handle special characters like "/"
  const encodedFolio = btoa(folio);
  const url = new URL(`${API_URL}/v1/procedures/reject/${encodedFolio}`);

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    console.error('Reject procedure error:', errorData);
    throw new Error(errorData.detail || 'Failed to reject procedure');
  }

  const result = await response.json();
  return result;
}
