import { useTranslation } from 'react-i18next';

/**
 * Maps technical procedure type names to user-friendly translated names
 */
export function useProcedureTypeTranslation() {
  const { t: tProcedures } = useTranslation('procedures');
  const { t: tApprovals } = useTranslation('procedureApprovals');

  /**
   * Get the translated name for a procedure type
   * @param procedureType - The technical procedure type name
   * @returns The translated user-friendly name
   */
  const getProcedureTypeName = (
    procedureType: string | null | undefined
  ): string => {
    if (!procedureType) {
      return tApprovals('procedureTypes.default', {
        defaultValue: 'Trámite General',
      });
    }

    // Check for exact match in procedureApprovals translations first
    const approvalTranslation = tApprovals(`procedureTypes.${procedureType}`, {
      defaultValue: null,
    });
    if (approvalTranslation && approvalTranslation !== procedureType) {
      return approvalTranslation;
    }

    // Fallback to procedures translations
    const procedureTypeMap: Record<string, string> = {
      business_license: tProcedures('edit.pdf.procedureTypes.businessLicense'),
      permits_building_license: tProcedures(
        'edit.pdf.procedureTypes.buildingLicense'
      ),
    };

    // Check for exact match
    if (procedureTypeMap[procedureType]) {
      return procedureTypeMap[procedureType];
    }

    // Check for partial matches (in case the type contains the key)
    for (const [key, value] of Object.entries(procedureTypeMap)) {
      if (procedureType.includes(key)) {
        return value;
      }
    }

    // Fallback: convert snake_case to Title Case
    return procedureType
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };

  /**
   * Get a map of all available procedure types with their translations
   */
  const getProcedureTypeMap = (): Record<string, string> => {
    return {
      business_license: tApprovals('procedureTypes.business_license', {
        defaultValue: tProcedures('edit.pdf.procedureTypes.businessLicense'),
      }),
      permits_building_license: tApprovals(
        'procedureTypes.permits_building_license',
        {
          defaultValue: tProcedures('edit.pdf.procedureTypes.buildingLicense'),
        }
      ),
    };
  };

  return {
    getProcedureTypeName,
    getProcedureTypeMap,
  };
}
