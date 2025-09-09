// Client-side types for procedures
export type ProcedureStatus =
  | 'draft'
  | 'pending_review'
  | 'in_review'
  | 'approved'
  | 'rejected'
  | 'prevention'
  | 'license_issued';

// Utility function to transform status from API number to frontend string
export function transformProcedureStatus(
  status: number | null | undefined
): ProcedureStatus {
  switch (status) {
    case 0:
      return 'draft'; // Backend uses 0 for new/draft procedures
    case 1:
      return 'pending_review'; // Backend uses 1 for complete procedures ready for review
    case 2:
      return 'approved'; // Backend uses 2 for approved procedures
    case 3:
      return 'prevention'; // Backend uses 3 for "Requires Attention" (prevention)
    case 4:
      return 'in_review'; // Backend uses 4 for in_review (if used)
    case 7:
      return 'license_issued'; // Backend uses 7 for license issued
    default:
      console.warn('Unknown status code:', status, 'defaulting to draft');
      return 'draft'; // fallback to draft for unknown values (safer default)
  }
}

// Utility function to transform API procedure data to frontend format
export function transformProcedureData(apiData: any): ProcedureData {
  return {
    ...apiData,
    status: transformProcedureStatus(apiData.status),
  };
}

export interface BusinessCommercialProcedureData {
  id: number;
  folio: string | null;
  current_step?: number | null;
  procedure_type?: string | null;
  license_status?: string | null;
  status: ProcedureStatus;
  procedure_start_date?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  official_applicant_name?: string | null;

  // Address information
  street?: string | null;
  exterior_number?: string | null;
  interior_number?: string | null;
  neighborhood?: string | null;
  full_address?: string | null;

  // Municipality information
  municipality_id?: number | null;
  municipality_name?: string | null;

  // Business sector information (SCIAN)
  industry_classification_code?: string | null;
  business_line?: string | null;
  business_line_code?: string | null;

  // Business details
  business_name?: string | null;
  detailed_description?: string | null;
}

export interface ConstructionProcedureData {
  id: number;
  folio: string | null;
  current_step?: number | null;
  procedure_type?: string | null;
  license_status?: string | null;
  status: ProcedureStatus;
  procedure_start_date?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  official_applicant_name?: string | null;

  // Address information
  street?: string | null;
  exterior_number?: string | null;
  interior_number?: string | null;
  neighborhood?: string | null;
  reference?: string | null;
  full_address?: string | null;

  // Municipality information
  municipality_id?: number | null;
  municipality_name?: string | null;
}

// Legacy procedure data type for backward compatibility
export interface ProcedureData {
  id: number;
  folio: string | null;
  current_step?: number | null;
  procedure_type?: string | null;
  license_status?: string | null;
  status: ProcedureStatus;
  procedure_start_date?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  official_applicant_name?: string | null;
  street?: string | null;
  exterior_number?: string | null;
  interior_number?: string | null;
  neighborhood?: string | null;
  municipality?: string | null;
  postal_code?: string | null;
  scian_code?: string | null;
  scian_description?: string | null;
  business_name?: string | null;
  license_pdf?: string | null;
}
