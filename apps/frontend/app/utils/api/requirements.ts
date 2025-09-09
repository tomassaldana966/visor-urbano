import { z } from 'zod';
import { requestAPI } from './base';
import { requirementsSchema } from '@root/app/schemas/requirements';

function mapLegacyFieldsToEnglish(
  data: z.infer<typeof requirementsSchema>
): z.infer<typeof requirementsSchema> {
  const fieldMapping: Record<string, string> = {
    calle: 'street',
    colonia: 'neighborhood',
    municipio: 'municipality_name',
    id_municipio: 'municipality_id',
    codigo_scian: 'scian_code',
    nombre_scian: 'scian_name',
    superficie_propiedad: 'property_area',
    superficie: 'activity_area',
    nombre: 'applicant_name',
    caracter: 'applicant_character',
    tipo_persona: 'person_type',
    localidad: 'locality',
    actividad: 'activity_description',
    alcohol: 'alcohol_sales',
    url_minimapa: 'minimap_url',
    url_croquis: 'minimap_sketch_url',
    restricciones: 'restrictions',
    camposDinamicos: 'dynamic_fields',
    street: 'street',
    neighborhood: 'neighborhood',
    municipality_name: 'municipality_name',
    municipality_id: 'municipality_id',
    scian_code: 'scian_code',
    scian_name: 'scian_name',
    property_area: 'property_area',
    activity_area: 'activity_area',
    applicant_name: 'applicant_name',
    applicant_character: 'applicant_character',
    person_type: 'person_type',
    locality: 'locality',
    activity_description: 'activity_description',
    alcohol_sales: 'alcohol_sales',
    minimap_url: 'minimap_url',
    minimap_sketch_url: 'minimap_sketch_url',
    restrictions: 'restrictions',
    dynamic_fields: 'dynamic_fields',
    folio: 'folio',
    primary_folio: 'primary_folio',
  };

  const mappedData: Record<string, unknown> = {};
  const dataAsRecord = data as Record<string, unknown>;

  Object.keys(dataAsRecord).forEach(key => {
    const englishKey = fieldMapping[key] ?? key;
    let value = dataAsRecord[key];

    if (englishKey === 'municipality_id') {
      value = parseInt(String(value), 10) || 0;
    } else if (
      englishKey === 'property_area' ||
      englishKey === 'activity_area'
    ) {
      value = parseFloat(String(value)) || 0;
    } else if (englishKey === 'alcohol_sales') {
      if (typeof value === 'string' && value.includes('|')) {
        value = parseInt(value.split('|')[0], 10) || 0;
      } else {
        value = parseInt(String(value), 10) || 0;
      }
    }

    mappedData[englishKey] = value;
  });

  return mappedData as z.infer<typeof requirementsSchema>;
}

export async function postRequirementsQueries(
  data: z.infer<typeof requirementsSchema>
) {
  const mappedData = mapLegacyFieldsToEnglish(data);

  try {
    const response = await requestAPI({
      endpoint: 'v1/requirements-queries/requirements',
      method: 'POST',
      data: mappedData,
    });

    const result = z
      .object({
        data: z
          .object({
            folio: z.string().optional(),
            url: z.string().optional(),
            issue_license: z.number().optional(),
            license_type: z.string().optional(),
            requirements: z
              .union([z.array(z.unknown()), z.object({}).passthrough()])
              .optional(),
            total_requirements: z.number().optional(),
            municipality_name: z.string().optional(),
            address: z.string().optional(),
            interested_party: z.string().optional(),
          })
          .optional(),
        message: z.string(),
      })
      .safeParse(response);

    if (!result.success) {
      console.error(
        'Error in postRequirementsQueries response',
        JSON.stringify(result.error, null, 2)
      );
      return null;
    }

    return {
      data: result.data.data ?? {},
      message: result.data.message,
      url: result.data.data?.url,
      folio: result.data.data?.folio,
      issue_license: result.data.data?.issue_license ?? 0,
    };
  } catch (error) {
    console.error('Error in postRequirementsQueries:', error);
    return null;
  }
}
