import type {
  requirementsSchema,
  dynamicFieldSchema,
} from '@root/app/schemas/requirements';
import type {
  MapLayerCreate,
  MapLayerUpdate,
} from '@root/app/schemas/map-layers';
import type {
  createBusinessTypeSchema,
  updateBusinessTypeStatusSchema,
  updateBusinessTypeCertificateSchema,
  businessTypeImpactUpdateSchema,
} from '@root/app/schemas/business-types';
import type {
  ZoningImpactLevelQuerySchema,
  CreateZoningImpactLevelSchema,
  UpdateZoningImpactLevelSchema,
} from '@root/app/schemas/zoning-impact-levels';
import type { z } from 'zod';
import type { register, login, getTechnicalSheetURL } from './api.server';

export type ApiData =
  | {
      endpoint: 'v1/users';
      data: Omit<Parameters<typeof register>[0], 'municipality_id'> & {
        municipality_id: number;
      };
    }
  | {
      endpoint: 'v1/auth/login';
      data: Parameters<typeof login>[0];
    }
  | {
      endpoint: 'v1/password/reset-password-request';
      data: { email: string };
    }
  | {
      endpoint: 'v1/password/change-password';
      data: { email: string; password: string; token: string };
    }
  | {
      endpoint: 'v1/map_layers';
      data: {
        municipality?: number;
      };
    }
  | {
      endpoint: 'v1/map_layers/';
      data: MapLayerCreate;
    }
  | {
      endpoint: `v1/map_layers/${number}`;
      data: MapLayerUpdate;
    }
  | {
      endpoint: 'v1/technical_sheets';
      data: Parameters<typeof getTechnicalSheetURL>[0];
    }
  | {
      endpoint: 'v1/notifications/';
      data?: {
        page?: number;
        per_page?: number;
      };
    }
  | {
      endpoint: `v1/notifications/${number}/read`;
      data?: {};
    }
  | {
      endpoint: `v1/notifications/procedure/${number}/files`;
      data?: {};
    }
  | {
      endpoint: 'v1/business_license_histories/';
      data: {
        municipality_id: number;
        status?: number;
        skip?: number;
        limit?: number;
      };
    }
  | {
      endpoint: 'v1/business_license/';
      data: {
        municipality_id: number;
        skip?: number;
        limit?: number;
      };
    }
  | {
      endpoint: 'v1/business_licenses/';
      data: {
        municipality_id: number;
        page?: number;
        per_page?: number;
      };
    }
  | {
      endpoint: `v1/business_licenses/${string}/payment`;
      data: {
        payment_status: number;
        payment_receipt_file?: string;
      };
    }
  | {
      endpoint: `v1/business_licenses/${string}/upload_receipt`;
      data: FormData;
    }
  | {
      endpoint: `v1/business_licenses/${string}/download_receipt`;
      data?: {};
    }
  | {
      endpoint: 'v1/business_types/enabled';
      data: {
        municipality_id: number;
      };
    }
  | {
      endpoint: 'v1/business_types/all';
      data?: never;
    }
  | {
      endpoint: 'v1/business_types/';
      data: z.infer<typeof createBusinessTypeSchema>;
    }
  | {
      endpoint: 'v1/requirements-queries/requirements';
      data: z.infer<typeof requirementsSchema>;
    }
  | {
      endpoint: `v1/fields/municipality/${number}`;
      data?: never;
    }
  | {
      endpoint: 'v1/fields';
      data?: never;
    }
  | {
      endpoint: 'v1/fields/';
      data: Omit<z.infer<typeof dynamicFieldSchema>, 'id'>;
    }
  | {
      endpoint: `v1/fields/${number}`;
      data: Partial<z.infer<typeof dynamicFieldSchema>>;
    }
  | {
      endpoint: 'v1/procedure_registrations/geometry';
      data: {
        folio: string;
        coordinates: string;
      };
    }
  | {
      endpoint: 'v1/news/';
      data?: {
        page?: number;
        per_page?: number;
      };
    }
  | {
      endpoint: `v1/news/${number}/${number}/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/news/${number}`;
      data?: never;
    }
  | {
      endpoint: 'v1/blog/';
      data?: never;
    }
  | {
      endpoint: `v1/blog/user/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/blog/${number}`;
      data?: never;
    }
  | {
      endpoint: 'v1/blog/';
      data: {
        title: string;
        image: string;
        link: string;
        summary: string;
        news_date: string;
        slug?: string;
        blog_type?: number;
        body?: string;
        municipality_id?: number;
        password: string;
      };
    }
  | {
      endpoint: `v1/blog/${number}`;
      data: {
        title?: string;
        image?: string;
        link?: string;
        summary?: string;
        news_date?: string;
        slug?: string;
        blog_type?: number;
        body?: string;
        municipality_id?: number;
        password: string;
      };
    }
  | {
      endpoint: `v1/blog/${number}/${string}`;
      data?: never;
    }
  | {
      endpoint: 'v1/business_licenses/public';
      data?: {
        page?: number;
        per_page?: number;
        search?: string;
        municipality_id?: number;
      };
    }
  | {
      endpoint: 'v1/procedures/director-review';
      data?: {
        folio?: string;
      };
    }
  | {
      endpoint: 'v1/procedures/procedure-approvals';
      data?: {
        folio?: string;
        page?: number;
        per_page?: number;
        tab_filter?:
          | 'business_licenses'
          | 'permits_building_license'
          | 'en_revisiones'
          | 'prevenciones'
          | 'desechados'
          | 'en_ventanilla';
        procedure_type?: string;
      };
    }
  | {
      endpoint: `v1/procedures/issue-license/${string}`;
      data?: FormData;
    }
  | {
      endpoint: 'v1/procedures/licenses-issued';
      data?: {
        page?: number;
        per_page?: number;
      };
    }
  | {
      endpoint: 'v1/director/facets';
      data?: {
        municipality_id?: number;
      };
    }
  | {
      endpoint: 'v1/municipalities/';
      data?: {
        skip?: number;
        limit?: number;
        name?: string | null;
        has_zoning?: boolean | null;
        cvgeo?: string | null;
      };
    }
  | {
      endpoint: `v1/municipalities/${number}`;
      data?: never;
    }
  | {
      endpoint: `v1/municipalities/${number}`;
      data: {
        name?: string;
        director?: string;
        address?: string;
        phone?: string;
        email?: string;
        website?: string;
        responsible_area?: string;
        solving_days?: number;
        initial_folio?: number;
        low_impact_license_cost?: string;
        license_additional_text?: string;
        allow_online_procedures?: boolean;
        allow_window_reviewer_licenses?: boolean;
      };
    }
  | {
      endpoint: 'v1/geocode';
      data: {
        address: string;
        municipality: string;
      };
    }
  | {
      endpoint: `v1/fields/by_folio/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/fields/by_renewal/${string}`;
      data?: never;
    }
  | {
      endpoint: 'v1/procedure_registrations/validate_capture/';
      data: {
        folio: string;
        step: number;
        fields: Record<string, unknown>;
      };
    }
  | {
      endpoint: 'v1/procedure_registrations/validate_capture/revalidation/';
      data: {
        folio: string;
        step: number;
        fields: Record<string, unknown>;
      };
    }
  | {
      endpoint: `v1/procedure_registrations/finalize_without_signature/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/procedure_registrations/send_application/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/procedure_registrations/by_folio/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/procedures/by_folio/${string}`;
      data: Record<string, any>;
    }
  | {
      endpoint: `v1/procedures/update_answers/${string}`;
      data: Record<string, any>;
    }
  | {
      endpoint: `v1/procedures/${number}`;
      data: Record<string, any>;
    }
  | {
      endpoint: 'v1/roles';
      data?: never;
    }
  | {
      endpoint: 'v1/roles';
      data: {
        name: string;
        description: string;
      };
    }
  | {
      endpoint: `v1/roles/${number}`;
      data?: never;
    }
  | {
      endpoint: `v1/roles/${number}`;
      data: {
        name: string;
        description: string;
      };
    }
  | {
      endpoint: 'v1/users/';
      data?: {
        search?: string;
        role?: string;
      };
    }
  | {
      endpoint: 'v1/users/';
      data: {
        name: string;
        paternal_last_name: string;
        maternal_last_name?: string;
        cellphone: string;
        email: string;
        password: string;
        municipality_id: number;
      };
    }
  | {
      endpoint: `v1/users/${number}`;
      data?: never;
    }
  | {
      endpoint: `v1/users/${number}`;
      data: {
        name: string;
        paternal_last_name: string;
        maternal_last_name?: string;
        cellphone: string;
        email: string;
        password?: string;
        municipality_id: number;
        role_id: number;
      };
    }
  | {
      endpoint: `v1/director/departments/${number}/users`;
      data?: never;
    }
  | {
      endpoint: `v1/director/departments/${number}/requirements`;
      data?: never;
    }
  | {
      endpoint: 'v1/director/departments/quick-action';
      data: {
        department_id: number;
        action: 'add_field' | 'remove_field' | 'add_role' | 'remove_role';
        field_id?: number;
        role_id?: number;
        procedure_type?: string;
      };
    }
  | {
      endpoint: `v1/director/departments/${number}`;
      data: {
        name?: string;
        description?: string;
        is_active?: boolean;
        can_approve_procedures?: boolean;
        can_reject_procedures?: boolean;
        requires_all_requirements?: boolean;
      };
    }
  | {
      endpoint: 'v1/director/departments';
      data: {
        name: string;
        code: string;
        description?: string;
        municipality_id: number;
        is_active?: boolean;
        can_approve_procedures?: boolean;
        can_reject_procedures?: boolean;
        requires_all_requirements?: boolean;
      };
    }
  | {
      endpoint: 'v1/director/departments';
      data?: {
        include_inactive?: boolean;
      };
    }
  | {
      endpoint: `v1/business_types/disable/status/${number}`;
      data: z.infer<typeof updateBusinessTypeStatusSchema>;
    }
  | {
      endpoint: `v1/business_types/disable/certificate/${number}`;
      data: z.infer<typeof updateBusinessTypeCertificateSchema>;
    }
  | {
      endpoint: 'v1/business_types/impact';
      data: z.infer<typeof businessTypeImpactUpdateSchema>;
    }
  | {
      endpoint: 'v1/zoning_impact_levels/';
      data: z.infer<typeof ZoningImpactLevelQuerySchema>;
    }
  | {
      endpoint: `v1/zoning_impact_levels/${number}`;
      data?: never;
    }
  | {
      endpoint: 'v1/zoning_impact_levels/';
      data: z.infer<typeof CreateZoningImpactLevelSchema>;
    }
  | {
      endpoint: `v1/zoning_impact_levels/${number}`;
      data: z.infer<typeof UpdateZoningImpactLevelSchema>;
    }
  | {
      endpoint: 'v1/reports/charts/annual-bar';
      data?: never;
    }
  | {
      endpoint: 'v1/reports/charts/advanced-pie';
      data?: never;
    }
  | {
      endpoint: `v1/reports/charts/annual-bar/${number}`;
      data?: never;
    }
  | {
      endpoint: 'v1/reports/charts/advanced-pie-admin';
      data?: {
        municipality_id?: number;
      };
    }
  | {
      endpoint: 'v1/reports/charts/bar-list';
      data: {
        month: number;
        start_date: string;
        end_date: string;
        municipality_id?: number;
      };
    }
  | {
      endpoint: 'v1/reports/charts/review-pie';
      data?: never;
    }
  | {
      endpoint: 'v1/reports/charts/pie-by-municipality';
      data: {
        start_date: string;
        end_date: string;
      };
    }
  | {
      endpoint: `v1/reports/charts/monthly-bar/${number}`;
      data: {
        start_date: string;
        end_date: string;
      };
    }
  | {
      endpoint: 'v1/reports/charts/full-report';
      data?: never;
    }
  | {
      endpoint: 'v1/reports/charts/technical-sheets-summary';
      data?: never;
    }
  | {
      endpoint: 'v1/reports/charts/complete-analytics';
      data?: never;
    }
  | {
      endpoint: `v1/reports/charts/complete-analytics/${number}`;
      data?: never;
    }
  | {
      endpoint: 'v1/director/dashboard';
      data?: {
        municipality_id?: number;
      };
    }
  | {
      endpoint: `v1/municipalities/${number}/signatures`;
      data: {
        signer_name: string;
        position_title: string;
        order_index: number;
      };
    }
  | {
      endpoint: `v1/municipalities/${number}/signatures`;
      data?: {}; // For GET requests
    }
  | {
      endpoint: `v1/municipalities/${number}/signatures/${number}`;
      data?: {
        signer_name?: string;
        position_title?: string;
        order_index?: number;
      };
    }
  | {
      endpoint: 'v1/zoning_impact_levels/';
      data: {
        municipality_id: number;
      };
    }
  | {
      endpoint: `v1/zoning_impact_levels/${number}`;
      data?: {};
    }
  | {
      endpoint: 'v1/zoning_impact_levels/';
      data: {
        impact_level: number;
        municipality_id: number;
        geom?: {
          type: 'Polygon';
          coordinates: number[][][];
        };
      };
    }
  | {
      endpoint: `v1/zoning_impact_levels/${number}`;
      data: {
        impact_level?: number;
        municipality_id?: number;
        geom?: {
          type: 'Polygon';
          coordinates: number[][][];
        };
      };
    }
  | {
      endpoint: `v1/procedures/license/status/${string}`;
      data?: never;
    }
  | {
      endpoint: `v1/procedures/license/download/${string}`;
      data?: never;
    };
