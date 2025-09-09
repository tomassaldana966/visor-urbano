import { useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import {
  generateProcedurePDF,
  type ProcedureData,
  type DynamicFieldData,
} from '../utils/pdf';
import { type DynamicField } from '../schemas/dynamicFields';

export function useProcedurePDF() {
  const { t } = useTranslation('procedures');

  const generatePDF = useCallback(
    async (
      procedure: ProcedureData,
      fieldsBySection: Record<string, DynamicField[]>
    ) => {
      try {
        // Convert the fields by section to the format expected by the PDF generator
        const dynamicFields: DynamicFieldData[][] = [];

        // Organize fields by section (1, 2, 3, 4)
        for (let i = 1; i <= 4; i++) {
          const sectionKey = i.toString();
          const sectionFields = fieldsBySection[sectionKey] || [];

          const formattedFields: DynamicFieldData[] = sectionFields.map(
            field => ({
              id: field.id,
              name: field.name,
              label: field.description || field.name, // Use description as label fallback
              value: field.value,
              field_type: field.field_type,
              step: field.step,
              options: field.options,
              options_description: field.options_description,
            })
          );

          dynamicFields.push(formattedFields);
        }

        await generateProcedurePDF(procedure, dynamicFields, t);

        return { success: true };
      } catch (error) {
        console.error('Error generating PDF:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },
    [t]
  );

  return { generatePDF };
}
