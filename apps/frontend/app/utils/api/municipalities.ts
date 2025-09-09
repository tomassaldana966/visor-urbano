import { z } from 'zod';
import { requestAPI } from './base';
import {
  municipalitySchema,
  municipalitySettingsUpdateSchema,
  type Municipality,
  type MunicipalitySettingsUpdate,
} from '@root/app/schemas/municipalities';
import { type Signature } from '@root/app/hooks/useSignatures';
import {
  geoCodeResultSchema,
  type GeoCodeResult,
} from '@root/app/schemas/geocode';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function getMunicipalities(
  data: {
    skip?: number;
    limit?: number;
    name?: string | null;
    has_zoning?: boolean | null;
    cvgeo?: string | null;
  } = { skip: 0, limit: 100 }
): Promise<Municipality[]> {
  const response = await requestAPI({
    endpoint: 'v1/municipalities/',
    method: 'GET',
    data,
  });

  const schema = z.array(municipalitySchema);
  const result = schema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid response format for municipalities');
    console.error(JSON.stringify(result.error, null, 2));
    return [];
  }
}

export async function searchByAddress(data: {
  address: string;
  municipality: string;
}): Promise<GeoCodeResult | null> {
  return requestAPI({
    endpoint: 'v1/geocode',
    method: 'GET',
    data,
  }).then(response => {
    const result = geoCodeResultSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      console.error('Invalid response format for geocode');
      console.error(JSON.stringify(result.error, null, 2));
      return null;
    }
  });
}

export async function getMunicipality(
  id: number,
  authToken?: string
): Promise<Municipality> {
  const response = await requestAPI({
    endpoint: `v1/municipalities/${id}`,
    method: 'GET',
    authToken,
  });

  const result = municipalitySchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid response format for municipality');
    console.error(JSON.stringify(result.error, null, 2));
    throw new Error('Invalid response format for municipality');
  }
}

export async function updateMunicipality(
  id: number,
  data: MunicipalitySettingsUpdate,
  authToken: string
): Promise<Municipality> {
  // Validate the input data
  const validationResult = municipalitySettingsUpdateSchema.safeParse(data);
  if (!validationResult.success) {
    throw new Error(
      'Invalid municipality data: ' + validationResult.error.message
    );
  }

  const response = await requestAPI({
    endpoint: `v1/municipalities/${id}`,
    method: 'PUT',
    data: validationResult.data,
    authToken,
  });

  const result = municipalitySchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    console.error('Invalid response format for updated municipality');
    console.error(JSON.stringify(result.error, null, 2));
    throw new Error('Invalid response format for updated municipality');
  }
}

export async function uploadMunicipalityImage(
  id: number,
  imageFile: File,
  authToken: string
): Promise<Municipality> {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch(`${API_URL}/v1/municipalities/${id}/image`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Failed to upload image: ${response.statusText}`);
  }

  const result = await response.json();
  const validationResult = municipalitySchema.safeParse(result);

  if (validationResult.success) {
    return validationResult.data;
  } else {
    console.error('Invalid response format for municipality image upload');
    console.error(JSON.stringify(validationResult.error, null, 2));
    throw new Error('Invalid response format for municipality image upload');
  }
}

export async function createMunicipalitySignature(
  municipalityId: number,
  signatureData: {
    signer_name: string;
    position_title: string;
    order_index: number;
  },
  authToken: string
): Promise<any> {
  const response = await requestAPI({
    endpoint: `v1/municipalities/${municipalityId}/signatures`,
    method: 'POST',
    data: signatureData,
    authToken,
  });

  return response;
}

export async function updateMunicipalitySignature(
  municipalityId: number,
  signatureId: number,
  signatureData: {
    signer_name?: string;
    position_title?: string;
    order_index?: number;
  },
  authToken: string
): Promise<any> {
  const response = await requestAPI({
    endpoint: `v1/municipalities/${municipalityId}/signatures/${signatureId}`,
    method: 'PUT',
    data: signatureData,
    authToken,
  });

  return response;
}

export async function deleteMunicipalitySignature(
  municipalityId: number,
  signatureId: number,
  authToken: string
): Promise<void> {
  await requestAPI({
    endpoint: `v1/municipalities/${municipalityId}/signatures/${signatureId}`,
    method: 'DELETE',
    authToken,
  });
}

export async function uploadSignatureImage(
  municipalityId: number,
  signatureId: number,
  imageFile: File,
  authToken: string
): Promise<any> {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch(
    `${API_URL}/v1/municipalities/${municipalityId}/signatures/${signatureId}/image`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to upload signature image: ${response.statusText}`);
  }

  return await response.json();
}

export async function getMunicipalitySignatures(
  municipalityId: number
): Promise<Signature[]> {
  const response = await requestAPI({
    endpoint: `v1/municipalities/${municipalityId}/signatures`,
    method: 'GET',
  });

  // Return the signatures array directly since the backend returns an array
  // Type assertion is safe here as the API contract is well-defined
  const signatures = Array.isArray(response) ? response : [];
  return signatures as Signature[];
}
