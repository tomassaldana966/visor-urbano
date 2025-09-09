import { z } from 'zod';
import { requestAPI } from './base';
import {
  businessTypesSchema,
  createBusinessTypeSchema,
  updateBusinessTypeStatusSchema,
  updateBusinessTypeCertificateSchema,
  businessTypeImpactUpdateSchema,
} from '../../schemas/business-types';

export async function getBusinessTypes(data: { municipality_id: number }) {
  return requestAPI({
    endpoint: 'v1/business_types/enabled',
    method: 'GET',
    data,
  }).then(response => {
    const result = businessTypesSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      return [];
    }
  });
}

export async function getAllBusinessTypes(authToken: string) {
  return requestAPI({
    endpoint: 'v1/business_types/all',
    method: 'GET',
    authToken,
  }).then(response => {
    const result = businessTypesSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      console.error('Failed to parse business types:', result.error);
      return [];
    }
  });
}

export async function createBusinessType(
  data: z.infer<typeof createBusinessTypeSchema>,
  authToken: string
) {
  return requestAPI({
    endpoint: 'v1/business_types/',
    method: 'POST',
    data,
    authToken,
  });
}

export async function updateBusinessTypeStatus(
  status: number,
  data: z.infer<typeof updateBusinessTypeStatusSchema>,
  authToken: string
) {
  const parsed = updateBusinessTypeStatusSchema.safeParse(data);

  if (!parsed.success) {
    throw new Error('Invalid request body for updateBusinessTypeStatus');
  }

  return requestAPI({
    endpoint: `v1/business_types/disable/status/${status}`,
    method: 'POST',
    data: parsed.data,
    authToken,
  });
}

export async function updateBusinessTypeCertificate(
  status: number,
  data: z.infer<typeof updateBusinessTypeCertificateSchema>,
  authToken: string
) {
  const parsed = updateBusinessTypeCertificateSchema.safeParse(data);

  if (!parsed.success) {
    throw new Error('Invalid request body for updateBusinessTypeCertificate');
  }

  return requestAPI({
    endpoint: `v1/business_types/disable/certificate/${status}`,
    method: 'POST',
    data: parsed.data,
    authToken,
  });
}

export async function updateBusinessTypeImpact(
  data: z.infer<typeof businessTypeImpactUpdateSchema>,
  authToken: string
) {
  const parsed = businessTypeImpactUpdateSchema.safeParse(data);

  if (!parsed.success) {
    throw new Error('Invalid request body for updateBusinessTypeImpact');
  }

  return requestAPI({
    endpoint: 'v1/business_types/impact',
    method: 'PATCH',
    data: parsed.data,
    authToken,
  });
}
