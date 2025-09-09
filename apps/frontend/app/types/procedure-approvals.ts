// Types based on backend ProcedureRead schema
export interface ProcedureApproval {
  id: number;
  folio?: string | null;
  current_step?: number | null;
  user_signature?: string | null;
  user_id?: number | null;
  window_user_id?: number | null;
  entry_role?: number | null;
  documents_submission_date?: string | null;
  procedure_start_date?: string | null;
  window_seen_date?: string | null;
  license_delivered_date?: string | null;
  has_signature?: number | null;
  no_signature_date?: string | null;
  official_applicant_name?: string | null;
  responsibility_letter?: string | null;
  sent_to_reviewers?: number | null;
  sent_to_reviewers_date?: string | null;
  license_pdf?: string | null;
  payment_order?: string | null;
  status?: number | null;
  step_one?: number | null;
  step_two?: number | null;
  step_three?: number | null;
  step_four?: number | null;
  director_approval?: number | null;
  window_license_generated?: number | null;
  procedure_type?: string | null;
  license_status?: string | null;
  reason?: string | null;
  renewed_folio?: string | null;
  requirements_query_id?: number | null;
  business_type_id?: number | null;

  // Address fields
  street?: string | null;
  exterior_number?: string | null;
  interior_number?: string | null;
  neighborhood?: string | null;
  reference?: string | null;
  project_municipality_id?: number | null;
  municipality_id?: number | null;

  // Business establishment fields
  establishment_name?: string | null;
  establishment_address?: string | null;
  establishment_phone?: string | null;
  establishment_area?: string | null;

  // SCIAN fields for business classification
  scian_code?: string | null;
  scian_name?: string | null;

  // Additional fields
  created_at?: string | null;
  updated_at?: string | null;
  municipality_name?: string | null;
  business_line?: string | null;
}

import type { AuthUser } from '../utils/auth/auth.server';

export interface LoaderData {
  user: AuthUser;
  procedureApprovals: ProcedureApproval[];
  allProceduresForCounts: ProcedureApproval[];
  accessToken: string;
  pagination: {
    page: number;
    per_page: number;
    total: number;
  };
  filters: {
    tab_filter?: TabFilter;
    folio?: string;
  };
}

export type TabFilter =
  | 'business_licenses'
  | 'permits_building_license'
  | 'en_revisiones'
  | 'prevenciones'
  | 'desechados'
  | 'aprobados'
  | 'en_ventanilla';

export interface ActionItem {
  type: string;
  icon: React.ReactNode;
  label: string;
  variant: 'primary' | 'secondary';
  href?: string;
  action?: () => void;
  isCustom?: boolean;
  procedure?: ProcedureApproval;
}

export interface StatusDisplay {
  label: string;
  color: string;
  icon: React.ReactNode;
}
