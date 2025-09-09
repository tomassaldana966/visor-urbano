import { z } from 'zod';
import { requestAPI } from './base';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const BusinessLicenseHistorySchema = z.object({
  id: z.number(),
  license_folio: z.string().nullable(),
  issue_date: z.string().nullable(),
  business_line: z.string().nullable(),
  business_name: z.string().nullable(),
  owner_first_name: z.string().nullable(),
  owner_last_name_p: z.string().nullable(),
  owner_last_name_m: z.string().nullable(),
  street: z.string().nullable(),
  neighborhood: z.string().nullable(),
  license_type: z.string().nullable(),
  license_status: z.string().nullable(),
  payment_status: z.string().nullable(),
  opening_time: z.string().nullable(),
  closing_time: z.string().nullable(),
  municipality_id: z.number().nullable(),
  business_line_code: z.string().nullable(),
  detailed_description: z.string().nullable(),
  exterior_number: z.string().nullable(),
  interior_number: z.string().nullable(),
  coordinate_x: z.string().nullable(),
  coordinate_y: z.string().nullable(),
  user_tax_id: z.string().nullable(),
  national_id: z.string().nullable(),
  owner_phone: z.string().nullable(),
  owner_email: z.string().nullable(),
  created_at: z.string().nullable(),
  updated_at: z.string().nullable(),
});

export type BusinessLicenseHistoryData = z.infer<
  typeof BusinessLicenseHistorySchema
>;

export const BusinessLicenseSchema = z.object({
  id: z.number().optional(),
  license_folio: z.string(),
  commercial_activity: z.string(),
  industry_classification_code: z.string(),
  municipality_id: z.number(),
  municipality_name: z.string().nullable().optional(),
  license_status: z.string().nullable(),
  license_type: z.string().nullable(),
  payment_status: z.number().nullable(),
  scanned_pdf: z.string().nullable().optional(),
  // Owner information fields - required according to backend
  owner: z.string(),
  owner_last_name_p: z.string().nullable(),
  owner_last_name_m: z.string().nullable(),
  // Additional required fields according to backend
  authorized_area: z.string(),
  opening_time: z.string(),
  closing_time: z.string(),
  license_year: z.number(),
  // Optional additional fields
  created_at: z.string().nullable().optional(),
  updated_at: z.string().nullable().optional(),
  national_id: z.string().nullable().optional(),
  // Contact information (may not be available in BusinessLicense model)
  owner_phone: z.string().nullable().optional(),
  owner_email: z.string().nullable().optional(),
  license_category: z.number().nullable().optional(),
  // Additional data from procedure joins
  procedure_applicant_name: z.string().nullable().optional(),
  procedure_street: z.string().nullable().optional(),
  procedure_neighborhood: z.string().nullable().optional(),
  procedure_scian_name: z.string().nullable().optional(),
  procedure_establishment_name: z.string().nullable().optional(),
  procedure_establishment_address: z.string().nullable().optional(),
  procedure_establishment_phone: z.string().nullable().optional(),
  user_email: z.string().nullable().optional(), // Email del usuario que hizo el trámite

  // New establishment fields stored directly in BusinessLicense
  establishment_name: z.string().nullable().optional(),
  establishment_address: z.string().nullable().optional(),
  establishment_phone: z.string().nullable().optional(),
  establishment_email: z.string().nullable().optional(),
  procedure_id: z.number().nullable().optional(),
  requirements_query_id: z.number().nullable().optional(),
});

export type BusinessLicenseData = z.infer<typeof BusinessLicenseSchema>;

const PaginatedBusinessLicenseSchema = z.object({
  items: z.array(BusinessLicenseSchema),
  total: z.number(),
  page: z.number(),
  per_page: z.number(),
  total_pages: z.number(),
});

export type PaginatedBusinessLicenseData = z.infer<
  typeof PaginatedBusinessLicenseSchema
>;

export async function getBusinessLicenseHistories({
  municipality_id,
  status = 1,
  skip = 0,
  limit = 20,
  authToken,
}: {
  municipality_id: number;
  status?: number;
  skip?: number;
  limit?: number;
  authToken: string;
}): Promise<BusinessLicenseHistoryData[]> {
  return requestAPI({
    endpoint: 'v1/business_license_histories/',
    data: {
      municipality_id,
      status,
      skip,
      limit,
    },
    authToken,
  }).then(response => {
    const result = z.array(BusinessLicenseHistorySchema).safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      throw new Error('Invalid response format for business license histories');
    }
  });
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
  const response = await requestAPI({
    endpoint: 'v1/business_licenses/',
    data: {
      municipality_id,
      page,
      per_page,
    },
    authToken,
  });

  const result = PaginatedBusinessLicenseSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error(
      'Invalid response format for business licenses:',
      result.error
    );
    throw new Error('Invalid response format for business licenses');
  }
}

export async function exportBusinessLicenses({
  municipality_id,
  authToken,
}: {
  municipality_id: number;
  authToken: string;
}): Promise<Blob> {
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
  const encodedFolio = btoa(license_folio);
  const response = await requestAPI({
    endpoint: `v1/business_licenses/${encodedFolio}/payment`,
    method: 'PUT',
    data: {
      payment_status,
      payment_receipt_file,
    },
    authToken,
  });

  return response;
}

export async function uploadPaymentReceipt(
  authToken: string,
  licenseFolio: string,
  receiptFile: File
): Promise<string> {
  const formData = new FormData();
  formData.append('file', receiptFile);

  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/upload_receipt`
  );

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
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

export async function downloadPaymentReceipt(
  authToken: string,
  licenseFolio: string
): Promise<Blob> {
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/download_receipt`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('No receipt found for this license');
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to download receipt: ${response.status} ${errorText}`
    );
  }

  return response.blob();
}

export async function getBusinessLicensesList(data?: {
  page?: number;
  per_page?: number;
  search?: string;
  municipality_id?: number;
}) {
  return requestAPI({
    endpoint: 'v1/business_licenses/public',
    method: 'GET',
    data,
  });
}

export async function downloadLicensePdf(
  authToken: string,
  licenseFolio: string
): Promise<Blob> {
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
}): Promise<{ message: string; license: unknown }> {
  const encodedFolio = btoa(license_folio);
  const url = new URL(`${API_URL}/v1/business_licenses/${encodedFolio}/status`);

  const response = await fetch(url.toString(), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
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
  const formData = new FormData();
  formData.append('file', statusFile);

  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/upload_status_file`
  );

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
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
    changed_at: string | null;
    created_at: string | null;
  }>;
}> {
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(
    `${API_URL}/v1/business_licenses/${encodedFolio}/status_history`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch license status history: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function exportBusinessLicenseHistories({
  municipality_id,
  status = 1,
  authToken,
}: {
  municipality_id: number;
  status?: number;
  authToken: string;
}): Promise<Blob> {
  const url = new URL(`${API_URL}/v1/business_license_histories/export`);
  url.searchParams.append('municipality_id', municipality_id.toString());
  url.searchParams.append('status', status.toString());

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
      `Failed to export business license histories: ${response.status} ${errorText}`
    );
  }

  return response.blob();
}

export async function downloadBusinessLicensePDF({
  id,
  year,
  type,
  authToken,
}: {
  id: number;
  year: string;
  type: string;
  authToken: string;
}): Promise<Blob> {
  const url = new URL(
    `${API_URL}/v1/business_license_histories/pdf/${id}/${year}/${type}`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
      Accept: 'application/pdf',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to download business license PDF: ${response.status} ${errorText}`
    );
  }

  return response.blob();
}
