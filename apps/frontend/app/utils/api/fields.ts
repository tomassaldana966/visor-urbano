import { z } from 'zod';
import { requestAPI } from './base';
import {
  dynamicFieldsSchema,
  dynamicFieldSchema,
} from '@root/app/schemas/requirements';

export async function getFields(authToken: string) {
  const response = await requestAPI({
    endpoint: 'v1/fields',
    method: 'GET',
    authToken,
  });

  const result = dynamicFieldsSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid response format for fields:', result.error);
    throw new Error('Invalid response format for fields');
  }
}

export async function createField(
  authToken: string,
  fieldData: Omit<z.infer<typeof dynamicFieldSchema>, 'id'>
) {
  const response = await requestAPI({
    endpoint: 'v1/fields/',
    method: 'POST',
    data: fieldData,
    authToken,
  });

  const result = dynamicFieldSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid response format for field creation:', result.error);
    throw new Error('Invalid response format for field creation');
  }
}

export async function updateField(
  authToken: string,
  fieldId: number,
  fieldData: Partial<z.infer<typeof dynamicFieldSchema>>
) {
  const response = await requestAPI({
    endpoint: `v1/fields/${fieldId}`,
    method: 'PUT',
    data: fieldData,
    authToken,
  });

  const result = dynamicFieldSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid response format for field update:', result.error);
    throw new Error('Invalid response format for field update');
  }
}

export async function getDynamicFields(
  municipality_id: number,
  type?: 'business_license' | 'permits_building_license' | 'all'
) {
  if (!municipality_id) {
    console.error('Municipality ID is required to fetch dynamic fields');
    return [];
  }

  return requestAPI({
    endpoint: `v1/fields/municipality/${municipality_id}`,
    method: 'GET',
  }).then(response => {
    let transformedResponse = response;
    if (Array.isArray(response)) {
      transformedResponse = response.map((field: Record<string, unknown>) => ({
        ...field,
        field_type: field.field_type === 'document' ? 'file' : field.field_type,
        required:
          typeof field.required === 'boolean'
            ? field.required
              ? 1
              : 0
            : field.required,
      }));
    }

    const result = dynamicFieldsSchema.safeParse(transformedResponse);

    if (!result.success) {
      console.error(
        'Error in dynamic fields response',
        JSON.stringify(result.error, null, 2)
      );

      if (Array.isArray(response)) {
        const retryResult = dynamicFieldsSchema.safeParse(transformedResponse);

        if (retryResult.success) {
          let filteredFields;
          if (!type || type === 'all') {
            filteredFields = retryResult.data;
          } else if (type === 'permits_building_license') {
            filteredFields = retryResult.data.filter(
              field => field.procedure_type === 'permits_building_license'
            );
          } else {
            filteredFields = retryResult.data.filter(
              field =>
                field.procedure_type === 'business_license' ||
                field.procedure_type === 'check_requirements'
            );
          }
          return filteredFields;
        }
      }

      return [];
    }

    let filteredFields;
    if (!type || type === 'all') {
      filteredFields = result.data;
    } else if (type === 'permits_building_license') {
      filteredFields = result.data.filter(
        field => field.procedure_type === 'permits_building_license'
      );
    } else {
      filteredFields = result.data.filter(
        field =>
          field.procedure_type === 'business_license' ||
          field.procedure_type === 'check_requirements'
      );
    }

    return filteredFields;
  });
}
