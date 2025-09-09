import { z } from 'zod';
import { requestAPI } from './base';
import {
  dynamicFieldsResponseSchema,
  apiDynamicFieldsResponseSchema,
  type DynamicFieldsResponse,
  type ValidationCapture,
} from '@root/app/schemas/dynamicFields';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ProcedureSchema = z.object({
  id: z.number(),
  folio: z.string().nullable().optional(),
  official_applicant_name: z.string().nullable().optional(),
  procedure_type: z.string().nullable().optional(),
  current_step: z.number().nullable().optional(),
  status: z.number().nullable().optional(),
  license_status: z.string().nullable().optional(),
  procedure_start_date: z.string().nullable().optional(),
  created_at: z.string().nullable().optional(),
  updated_at: z.string().nullable().optional(),
  street: z.string().nullable().optional(),
  exterior_number: z.string().nullable().optional(),
  interior_number: z.string().nullable().optional(),
  neighborhood: z.string().nullable().optional(),
  municipality: z.string().nullable().optional(),
  postal_code: z.string().nullable().optional(),
  business_name: z.string().nullable().optional(),
  business_sector: z.string().nullable().optional(),
  business_activity: z.string().nullable().optional(),
  operating_hours: z.string().nullable().optional(),
  employee_count: z.union([z.string(), z.number()]).nullable().optional(),
  scian_code: z.string().nullable().optional(),
  scian_description: z.string().nullable().optional(),
  scian_name: z.string().nullable().optional(),
  establishment_name: z.string().nullable().optional(),
  establishment_address: z.string().nullable().optional(),
  establishment_phone: z.string().nullable().optional(),
  establishment_area: z.string().nullable().optional(),
  municipality_id: z.number().nullable().optional(),
  municipality_name: z.string().nullable().optional(),
  project_municipality_id: z.number().nullable().optional(),
  business_line: z.string().nullable().optional(),
  user_id: z.number().nullable().optional(),
  entry_role: z.number().nullable().optional(),
  window_user_id: z.number().nullable().optional(),
  user_signature: z.string().nullable().optional(),
  documents_submission_date: z.string().nullable().optional(),
  window_seen_date: z.string().nullable().optional(),
  license_delivered_date: z.string().nullable().optional(),
  has_signature: z.number().nullable().optional(),
  no_signature_date: z.string().nullable().optional(),
  responsibility_letter: z.string().nullable().optional(),
  sent_to_reviewers: z.number().nullable().optional(),
  sent_to_reviewers_date: z.string().nullable().optional(),
  license_pdf: z.string().nullable().optional(),
  payment_order: z.string().nullable().optional(),
  step_one: z.number().nullable().optional(),
  step_two: z.number().nullable().optional(),
  step_three: z.number().nullable().optional(),
  step_four: z.number().nullable().optional(),
  director_approval: z.number().nullable().optional(),
  window_license_generated: z.number().nullable().optional(),
  reason: z.string().nullable().optional(),
  renewed_folio: z.string().nullable().optional(),
  requirements_query_id: z.number().nullable().optional(),
});

export type ProcedureData = z.infer<typeof ProcedureSchema>;

export type ProceduresResponse = {
  procedures: ProcedureData[];
};

export const BusinessCommercialProcedureSchema = z.object({
  id: z.number(),
  folio: z.string().nullable(),
  current_step: z.number().nullable().optional(),
  procedure_type: z.string().nullable().optional(),
  license_status: z.string().nullable().optional(),
  status: z
    .number()
    .nullable()
    .optional()
    .transform(val => {
      switch (val) {
        case 1:
          return 'pending_review';
        case 2:
          return 'in_review';
        case 3:
          return 'approved';
        case 4:
          return 'rejected';
        default:
          return 'pending_review';
      }
    }),
  procedure_start_date: z.string().nullable().optional(),
  created_at: z.string().nullable().optional(),
  updated_at: z.string().nullable().optional(),
  street: z.string().nullable().optional(),
  exterior_number: z.string().nullable().optional(),
  interior_number: z.string().nullable().optional(),
  neighborhood: z.string().nullable().optional(),
  full_address: z.string().nullable().optional(),
  municipality_id: z.number().nullable().optional(),
  municipality_name: z.string().nullable().optional(),
  industry_classification_code: z.string().nullable().optional(),
  business_line: z.string().nullable().optional(),
  business_line_code: z.string().nullable().optional(),
  business_name: z.string().nullable().optional(),
  detailed_description: z.string().nullable().optional(),
});

export const ConstructionProcedureSchema = z.object({
  id: z.number(),
  folio: z.string().nullable(),
  current_step: z.number().nullable().optional(),
  procedure_type: z.string().nullable().optional(),
  license_status: z.string().nullable().optional(),
  status: z.number().transform(val => {
    switch (val) {
      case 1:
        return 'pending_review';
      case 2:
        return 'in_review';
      case 3:
        return 'approved';
      case 4:
        return 'rejected';
      default:
        return 'pending_review';
    }
  }),
  procedure_start_date: z.string().nullable().optional(),
  created_at: z.string().nullable().optional(),
  updated_at: z.string().nullable().optional(),
  official_applicant_name: z.string().nullable().optional(),
  street: z.string().nullable().optional(),
  exterior_number: z.string().nullable().optional(),
  interior_number: z.string().nullable().optional(),
  neighborhood: z.string().nullable().optional(),
  reference: z.string().nullable().optional(),
  full_address: z.string().nullable().optional(),
  municipality_id: z.number().nullable().optional(),
  municipality_name: z.string().nullable().optional(),
});

export const BusinessCommercialProceduresListSchema = z.object({
  procedures: z.array(BusinessCommercialProcedureSchema),
  total_count: z.number(),
  skip: z.number(),
  limit: z.number(),
});

export const ConstructionProceduresListSchema = z.object({
  procedures: z.array(ConstructionProcedureSchema),
  total_count: z.number(),
  skip: z.number(),
  limit: z.number(),
});

export type BusinessCommercialProcedureData = z.infer<
  typeof BusinessCommercialProcedureSchema
>;
export type ConstructionProcedureData = z.infer<
  typeof ConstructionProcedureSchema
>;
export type BusinessCommercialProceduresListData = z.infer<
  typeof BusinessCommercialProceduresListSchema
>;
export type ConstructionProceduresListData = z.infer<
  typeof ConstructionProceduresListSchema
>;

export async function getProcedures(
  authToken: string,
  params?: {
    folio?: string;
    page?: number;
    per_page?: number;
  }
): Promise<ProcedureData[]> {
  const url = new URL(`${API_URL}/v1/procedures/list`);

  if (params?.folio) {
    url.searchParams.append('folio', params.folio);
  }
  if (params?.page) {
    url.searchParams.append('page', params.page.toString());
  }
  if (params?.per_page) {
    url.searchParams.append('per_page', params.per_page.toString());
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(
      '[getProcedures] Failed to fetch procedures:',
      response.status,
      errorText
    );
    throw new Error(
      `Failed to fetch procedures: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();

  const schema = z.array(ProcedureSchema);
  const result = schema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    console.error('[getProcedures] Schema validation failed:', result.error);
    throw new Error(
      `Invalid response format for procedures: ${result.error.issues.map(i => `${i.path.join('.')}: ${i.message}`).join(', ')}`
    );
  }
}

export async function getProceduresEnhanced(
  authToken: string,
  params?: {
    folio?: string;
  }
): Promise<ProcedureData[]> {
  const url = new URL(`${API_URL}/v1/procedures/enhanced`);

  if (params?.folio) {
    url.searchParams.append('folio', params.folio);
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(
      '[getProceduresEnhanced] Failed to fetch procedures:',
      response.status,
      errorText
    );
    throw new Error(
      `Failed to fetch procedures: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();

  const schema = z.array(ProcedureSchema);
  const result = schema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    console.error(
      '[getProceduresEnhanced] Schema validation failed:',
      result.error
    );
    throw new Error(
      `Invalid response format for procedures: ${result.error.issues.map(i => `${i.path.join('.')}: ${i.message}`).join(', ')}`
    );
  }
}

export async function getProcedureApprovals(
  authToken: string,
  params?: {
    folio?: string;
    page?: number;
    per_page?: number;
    municipality_id?: number;
    tab_filter?:
      | 'business_licenses'
      | 'permits_building_license'
      | 'en_revisiones'
      | 'prevenciones'
      | 'desechados'
      | 'en_ventanilla';
    procedure_type?: string;
  }
): Promise<ProcedureData[]> {
  const response = await requestAPI({
    endpoint: 'v1/procedures/procedure-approvals',
    method: 'GET',
    data: params,
    authToken,
  });

  const schema = z.array(ProcedureSchema);
  const result = schema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for procedure approvals');
  }
}

export async function getProcedureHistory(
  authToken: string,
  params?: {
    folio?: string;
  }
): Promise<ProcedureData[]> {
  const url = new URL(`${API_URL}/v1/procedures/history`);

  if (params?.folio) {
    url.searchParams.append('folio', params.folio);
  }

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
      `Failed to fetch procedure history: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const schema = z.array(ProcedureSchema);
  const result = schema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for procedure history');
  }
}

export async function continueProcedure(
  authToken: string,
  folio: string
): Promise<ProcedureData> {
  const encodedFolio = btoa(folio);
  const url = new URL(`${API_URL}/v1/procedures/continue/${encodedFolio}`);

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to continue procedure: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const result = ProcedureSchema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for continue procedure');
  }
}

export async function getProcedureByFolio(
  authToken: string,
  folio: string
): Promise<ProcedureData> {
  const url = new URL(`${API_URL}/v1/procedures/list`);
  url.searchParams.append('folio', folio);

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
      `Failed to fetch procedure details: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const schema = z.array(ProcedureSchema);
  const result = schema.safeParse(data);

  if (result.success && result.data.length > 0) {
    return result.data[0];
  } else if (result.success && result.data.length === 0) {
    throw new Error(`Procedure with folio '${folio}' not found`);
  } else {
    console.error('Schema validation failed for procedure data:', result.error);
    throw new Error('Invalid response format for procedure data');
  }
}

export async function copyProcedure(
  authToken: string,
  folio: string,
  userId: number
): Promise<ProcedureData> {
  const encodedFolio = btoa(folio);
  const url = new URL(
    `${API_URL}/v1/procedures/copy/${encodedFolio}/${userId}`
  );

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to copy procedure: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const result = ProcedureSchema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for copy procedure');
  }
}

export async function getDependencyResolutionsByFolio(
  authToken: string,
  folio: string
): Promise<unknown[]> {
  const url = new URL(`${API_URL}/v1/dependency_resolutions/by_folio/${folio}`);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      return [];
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch dependency resolutions: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

export async function getProcedureInfo(
  authToken: string,
  folio: string
): Promise<unknown> {
  const encodedFolio = btoa(folio);
  const url = new URL(
    `${API_URL}/v1/requirements_queries/${encodedFolio}/info`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch procedure info: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function getProcedureTypeInfo(
  authToken: string,
  folio: string
): Promise<unknown> {
  const encodedFolio = btoa(folio);
  const url = new URL(
    `${API_URL}/v1/requirements_queries/${encodedFolio}/type`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch procedure type info: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function getOwnerData(
  authToken: string,
  folio: string
): Promise<unknown> {
  const url = new URL(`${API_URL}/v1/procedures/owner-data/${folio}`);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch owner data: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function getProvisionalOpeningByFolio(
  authToken: string,
  folio: string
): Promise<unknown> {
  const encodedFolio = btoa(folio);
  const url = new URL(
    `${API_URL}/v1/provisional_openings/by_folio/${encodedFolio}`
  );

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch provisional opening: ${response.status} ${errorText}`
    );
  }

  return await response.json();
}

export async function validateFolio(
  authToken: string,
  folio: string
): Promise<unknown[]> {
  const encodedFolio = btoa(folio);
  const url = new URL(
    `${API_URL}/v1/requirements/validate/folio/${encodedFolio}`
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
      `Failed to validate folio: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

export async function createProcedure(
  authToken: string,
  procedureData: {
    folio: string;
    requirements_query_id?: number;
    status?: number;
    current_step?: number;
    businessType?: number;
  }
): Promise<ProcedureData> {
  const url = new URL(`${API_URL}/v1/procedures/entry`);

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify({
      folio: procedureData.folio,
      requirements_query_id: procedureData.requirements_query_id ?? null,
      status: procedureData.status ?? 0, // Fixed: New procedures should start with status 0, not 1
      current_step: procedureData.current_step ?? 1,
      step_one: 0,
      step_two: 0,
      step_three: 0,
      step_four: 0,
      director_approval: 0,
      window_license_generated: 0,
      business_type_id: procedureData.businessType ?? null,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    if (response.status === 409) {
      throw new Error(`DUPLICATE_PROCEDURE: ${errorText}`);
    }
    throw new Error(
      `Failed to create procedure: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const result = ProcedureSchema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for create procedure');
  }
}

export async function getDynamicFieldsByFolio(
  authToken: string,
  folio: string
): Promise<DynamicFieldsResponse> {
  try {
    const encodedFolio = btoa(folio);
    const data = await requestAPI({
      endpoint: `v1/fields/by_folio/${encodedFolio}`,
      authToken,
    });

    const apiResult = apiDynamicFieldsResponseSchema.safeParse(data);

    if (apiResult.success) {
      return apiResult.data;
    } else {
      const tupleResult = dynamicFieldsResponseSchema.safeParse(data);
      if (tupleResult.success) {
        return tupleResult.data;
      }

      console.error(
        'Schema validation failed for dynamic fields:',
        apiResult.error
      );
      console.error('Raw API response:', JSON.stringify(data, null, 2));
      throw new Error(`Invalid fields data format for folio '${folio}'`);
    }
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(
        `Failed to fetch dynamic fields for folio '${folio}': ${error.message}`
      );
    }
    throw error;
  }
}

export async function getDynamicFieldsByRenewal(
  authToken: string,
  folio: string
): Promise<DynamicFieldsResponse> {
  try {
    const encodedFolio = btoa(folio);
    const data = await requestAPI({
      endpoint: `v1/fields/by_renewal/${encodedFolio}`,
      authToken,
    });

    const apiResult = apiDynamicFieldsResponseSchema.safeParse(data);

    if (apiResult.success) {
      return apiResult.data;
    } else {
      const tupleResult = dynamicFieldsResponseSchema.safeParse(data);
      if (tupleResult.success) {
        return tupleResult.data;
      }

      console.error(
        'Schema validation failed for renewal dynamic fields:',
        apiResult.error
      );
      console.error('Raw API response:', JSON.stringify(data, null, 2));
      throw new Error(
        `Invalid fields data format for renewal folio '${folio}'`
      );
    }
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(
        `Failed to fetch dynamic fields for renewal folio '${folio}': ${error.message}`
      );
    }
    throw error;
  }
}

export async function validateProcedureCapture(
  authToken: string,
  validationData: ValidationCapture
): Promise<{ success: boolean; message?: string }> {
  const data = await requestAPI({
    endpoint: 'v1/procedure_registrations/validate_capture/',
    method: 'POST',
    data: validationData,
    authToken,
  });

  return data;
}

export async function validateRenewalCapture(
  authToken: string,
  validationData: ValidationCapture
): Promise<{ success: boolean; message?: string }> {
  const data = await requestAPI({
    endpoint: 'v1/procedure_registrations/validate_capture/revalidation/',
    method: 'POST',
    data: validationData,
    authToken,
  });

  return data;
}

export async function finalizeProcedureWithoutSignature(
  authToken: string,
  folio: string
): Promise<{ success: boolean; message?: string }> {
  const data = await requestAPI({
    endpoint: `v1/procedure_registrations/finalize_without_signature/${folio}`,
    method: 'POST',
    authToken,
  });

  return data;
}

export async function sendProcedureApplication(
  authToken: string,
  folio: string
): Promise<{ success: boolean; message?: string }> {
  const data = await requestAPI({
    endpoint: `v1/procedure_registrations/send_application/${folio}`,
    method: 'POST',
    authToken,
  });

  return data;
}

export async function getProcedureRegistrationByFolio(
  authToken: string,
  folio: string
): Promise<unknown> {
  const encodedFolio = btoa(folio);
  return requestAPI({
    endpoint: `v1/procedure_registrations/by_folio/${encodedFolio}`,
    method: 'GET',
    authToken,
  });
}

export async function updateProcedureByFolio(
  authToken: string,
  folio: string,
  updateData: Record<string, unknown>
): Promise<ProcedureData> {
  try {
    const encodedFolio = btoa(folio);

    const response = await requestAPI({
      endpoint: `v1/procedures/by_folio/${encodedFolio}`,
      method: 'PATCH',
      data: updateData,
      authToken,
    });

    const result = ProcedureSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      console.error('Invalid procedure update response:', result.error);
      console.error('Raw response:', response);
      throw new Error('Invalid response format from server');
    }
  } catch (error) {
    console.error('Error updating procedure by folio:', error);
    if (error instanceof Error) {
      throw new Error(`Failed to update procedure: ${error.message}`);
    }
    throw new Error('Failed to update procedure: Unknown error');
  }
}

export async function updateProcedureById(
  authToken: string,
  procedureId: number,
  updateData: Record<string, unknown>
): Promise<ProcedureData> {
  const response = await requestAPI({
    endpoint: `v1/procedures/${procedureId}`,
    method: 'PATCH',
    data: updateData,
    authToken,
  });

  const result = ProcedureSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid procedure update response:', result.error);
    throw new Error('Invalid response format from server');
  }
}

export async function updateProcedureAnswers(
  authToken: string,
  folio: string,
  answersData: Record<string, unknown>
): Promise<{ success: boolean; message?: string }> {
  const encodedFolio = btoa(folio);
  const data = await requestAPI({
    endpoint: `v1/procedures/update_answers/${encodedFolio}`,
    method: 'POST',
    data: answersData,
    authToken,
  });

  return data;
}

export async function uploadProcedureFile(
  authToken: string,
  folio: string,
  fieldName: string,
  file: File
): Promise<{
  filename: string;
  size: number;
  file_path: string;
  content_type: string;
}> {
  const encodedFolio = btoa(folio);
  const formData = new FormData();
  formData.append('files', file);
  formData.append('field_names', fieldName);

  const url = new URL(
    `${API_URL}/v1/procedures/upload_documents/${encodedFolio}`
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
    throw new Error(`Failed to upload file: ${response.status} ${errorText}`);
  }

  const data = await response.json();

  if (data && typeof data === 'object' && 'file_path' in data) {
    return data;
  } else {
    throw new Error('Invalid response format for file upload');
  }
}

export async function getBusinessCommercialProcedures(
  authToken: string,
  params: {
    municipality_id: number;
    user_id?: number;
    status?: number;
    skip?: number;
    limit?: number;
  }
): Promise<BusinessCommercialProceduresListData> {
  const url = new URL(`${API_URL}/v1/business_commercial_procedures/`);

  url.searchParams.append('municipality_id', params.municipality_id.toString());
  if (params.user_id) {
    url.searchParams.append('user_id', params.user_id.toString());
  }
  if (params.status !== undefined) {
    url.searchParams.append('status', params.status.toString());
  }
  if (params.skip) {
    url.searchParams.append('skip', params.skip.toString());
  }
  if (params.limit) {
    url.searchParams.append('limit', params.limit.toString());
  }

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
      `Failed to fetch business commercial procedures: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const result = BusinessCommercialProceduresListSchema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    throw new Error(
      'Invalid response format for business commercial procedures'
    );
  }
}

export async function getConstructionProcedures(
  authToken: string,
  params: {
    municipality_id: number;
    user_id?: number;
    status?: number;
    skip?: number;
    limit?: number;
  }
): Promise<ConstructionProceduresListData> {
  const url = new URL(`${API_URL}/v1/construction_procedures/`);

  url.searchParams.append('municipality_id', params.municipality_id.toString());
  if (params.user_id) {
    url.searchParams.append('user_id', params.user_id.toString());
  }
  if (params.status !== undefined) {
    url.searchParams.append('status', params.status.toString());
  }
  if (params.skip) {
    url.searchParams.append('skip', params.skip.toString());
  }
  if (params.limit) {
    url.searchParams.append('limit', params.limit.toString());
  }

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
      `Failed to fetch construction procedures: ${response.status} ${errorText}`
    );
  }

  const data = await response.json();
  const result = ConstructionProceduresListSchema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for construction procedures');
  }
}

export async function saveProcedureGeometry(data: {
  folio: string;
  coordinates: string;
}) {
  return requestAPI({
    endpoint: 'v1/procedure_registrations/geometry',
    method: 'POST',
    data,
  });
}

export async function issueLicenseScanned(
  authToken: string,
  encodedFolio: string,
  formData: FormData
): Promise<{ success: boolean; message?: string }> {
  const url = new URL(`${API_URL}/v1/procedures/issue-license/${encodedFolio}`);

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to issue license: ${response.status} ${errorText}`);
  }

  return await response.json();
}

export async function getIssuedLicenses(
  authToken: string,
  params?: {
    page?: number;
    per_page?: number;
  }
): Promise<unknown> {
  const response = await requestAPI({
    endpoint: 'v1/procedures/licenses-issued',
    method: 'GET',
    data: params,
    authToken,
  });

  return response;
}

export async function downloadLicense(
  authToken: string,
  licenseFolio: string
): Promise<Blob> {
  const encodedFolio = btoa(licenseFolio);
  const url = new URL(`${API_URL}/v1/licenses/${encodedFolio}/download`);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to download license: ${response.status} ${errorText}`
    );
  }

  return response.blob();
}

export async function submitProcedureForReview(
  authToken: string,
  folio: string
): Promise<{
  success: boolean;
  message: string;
  procedure: {
    id: number;
    folio: string;
    status: number;
    sent_to_reviewers: number;
    sent_to_reviewers_date: string | null;
    updated_at: string | null;
  };
}> {
  const encodedFolio = btoa(folio);
  const url = new URL(
    `${API_URL}/v1/submit_procedures/by_folio/${encodedFolio}/submit_for_review`
  );

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));

    if (response.status === 400) {
      // Handle validation errors with missing fields
      if (
        errorData.detail &&
        typeof errorData.detail === 'object' &&
        errorData.detail.missing_fields
      ) {
        throw new Error(
          JSON.stringify({
            type: 'validation',
            message: errorData.detail.message,
            missing_fields: errorData.detail.missing_fields,
          })
        );
      } else if (typeof errorData.detail === 'string') {
        throw new Error(
          JSON.stringify({
            type: 'validation',
            message: errorData.detail,
          })
        );
      }
    }

    if (response.status === 403) {
      throw new Error(
        JSON.stringify({
          type: 'unauthorized',
          message:
            errorData.detail || 'Not authorized to submit this procedure',
        })
      );
    }

    if (response.status === 404) {
      throw new Error(
        JSON.stringify({
          type: 'not_found',
          message: errorData.detail || 'Procedure not found',
        })
      );
    }

    throw new Error(
      JSON.stringify({
        type: 'server_error',
        message: errorData.detail || `Server error: ${response.status}`,
      })
    );
  }

  const data = await response.json();
  return data;
}

// License-related functions
export const LicenseStatusSchema = z.object({
  folio: z.string(),
  procedure_status: z.number(),
  license_exists: z.boolean(),
  license_paid: z.boolean(),
  license_file_exists: z.boolean(),
  can_download: z.boolean(),
});

export type LicenseStatus = z.infer<typeof LicenseStatusSchema>;

export async function getLicenseStatus(
  authToken: string,
  encodedFolio: string
): Promise<LicenseStatus> {
  const response = await requestAPI({
    endpoint: `v1/procedures/license/status/${encodedFolio}`,
    method: 'GET',
    authToken,
  });

  const result = LicenseStatusSchema.safeParse(response);
  if (!result.success) {
    console.error('License status validation error:', result.error.errors);
    throw new Error(
      `Invalid license status format: ${result.error.errors.map(e => `${e.path.join('.')}: ${e.message}`).join(', ')}`
    );
  }

  return result.data;
}

export function getLicenseDownloadUrl(
  authToken: string,
  encodedFolio: string
): string {
  return `${API_URL}/v1/procedures/license/download/${encodedFolio}`;
}
