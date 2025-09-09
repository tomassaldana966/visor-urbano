import { z } from 'zod';
import { requestAPI } from './base';

// Department schemas
const DepartmentSchema = z.object({
  id: z.number(),
  name: z.string(),
  code: z.string(),
  description: z.string().optional(),
  municipality_id: z.number(),
  is_active: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
});

const DepartmentRoleSchema = z.object({
  id: z.number(),
  department_id: z.number(),
  role_id: z.number(),
  role_name: z.string(),
  created_at: z.string(),
});

const DepartmentUserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string(),
  role_name: z.string().optional(),
  is_active: z.boolean(),
  is_active_for_reviews: z.boolean().optional().default(true),
  can_receive_assignments: z.boolean().optional().default(true),
  can_review_requirements: z.boolean().optional().default(true),
  can_approve_department_review: z.boolean().optional().default(false),
  can_reject_department_review: z.boolean().optional().default(false),
  is_backup_reviewer: z.boolean().optional().default(false),
  last_activity_at: z.string().nullable().optional(),
  assigned_at: z.string().nullable().optional(),
  permissions: z
    .object({
      can_review_requirements: z.boolean(),
      can_approve_department_review: z.boolean(),
      can_reject_department_review: z.boolean(),
      is_department_lead: z.boolean(),
    })
    .optional(),
});

const DepartmentRequirementSchema = z.object({
  id: z.number(),
  field_id: z.number(),
  field_name: z.string(),
  field_label: z.string(),
  field_type: z.string(),
  procedure_type: z.string(),
  is_required_for_approval: z.boolean(),
  can_be_reviewed_in_parallel: z.boolean(),
  review_priority: z.number(),
  depends_on_department_id: z.number().nullable(),
  requires_all_users_approval: z.boolean(),
  auto_approve_if_no_issues: z.boolean(),
  created_at: z.string(),
});

const DepartmentFullInfoSchema = z.object({
  id: z.number(),
  name: z.string(),
  code: z.string(),
  description: z.string().optional(),
  municipality_id: z.number(),
  is_active: z.boolean(),
  can_approve_procedures: z.boolean(),
  can_reject_procedures: z.boolean(),
  requires_all_requirements: z.boolean(),
  user_count: z.number(),
  active_user_count: z.number(),
  requirement_count: z.number(),
  pending_procedures: z.number(),
  completed_procedures: z.number(),
  roles: z.array(DepartmentRoleSchema),
  requirements: z.array(DepartmentRequirementSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

const DepartmentUsersResponseSchema = z.object({
  department_id: z.number(),
  department_name: z.string(),
  users: z.array(DepartmentUserSchema),
  total_users: z.number(),
  active_users: z.number(),
  active_for_reviews: z.number(),
});

const DepartmentRequirementsResponseSchema = z.object({
  department_id: z.number(),
  department_name: z.string(),
  procedure_type: z.string().nullable(),
  requirements: z.array(DepartmentRequirementSchema),
  total_requirements: z.number(),
});

const DepartmentQuickActionRequestSchema = z.object({
  department_id: z.number(),
  action: z.enum(['add_field', 'remove_field', 'add_role', 'remove_role']),
  field_id: z.number().optional(),
  role_id: z.number().optional(),
  procedure_type: z.string().optional(),
});

const DepartmentQuickActionResponseSchema = z.object({
  success: z.boolean(),
  message: z.string(),
  department_id: z.number(),
  action_performed: z.string(),
  affected_item_id: z.number().optional(),
});

export type Department = z.infer<typeof DepartmentSchema>;
export type DepartmentRole = z.infer<typeof DepartmentRoleSchema>;
export type DepartmentUser = z.infer<typeof DepartmentUserSchema>;
export type DepartmentRequirement = z.infer<typeof DepartmentRequirementSchema>;
export type DepartmentFullInfo = z.infer<typeof DepartmentFullInfoSchema>;
export type DepartmentUsersResponse = z.infer<
  typeof DepartmentUsersResponseSchema
>;
export type DepartmentRequirementsResponse = z.infer<
  typeof DepartmentRequirementsResponseSchema
>;
export type DepartmentQuickActionRequest = z.infer<
  typeof DepartmentQuickActionRequestSchema
>;
export type DepartmentQuickActionResponse = z.infer<
  typeof DepartmentQuickActionResponseSchema
>;

// API functions
export async function getDepartments(
  authToken: string,
  includeInactive: boolean = false
): Promise<DepartmentFullInfo[]> {
  const response = await requestAPI({
    endpoint: 'v1/director/departments',
    method: 'GET',
    data: { include_inactive: includeInactive },
    authToken,
  });

  return z.array(DepartmentFullInfoSchema).parse(response);
}

export async function getDepartmentUsers(
  authToken: string,
  departmentId: number
): Promise<DepartmentUsersResponse> {
  const response = await requestAPI({
    endpoint: `v1/director/departments/${departmentId}/users`,
    method: 'GET',
    authToken,
  });

  return DepartmentUsersResponseSchema.parse(response);
}

export async function getDepartmentRequirements(
  authToken: string,
  departmentId: number
): Promise<DepartmentRequirementsResponse> {
  const response = await requestAPI({
    endpoint: `v1/director/departments/${departmentId}/requirements`,
    method: 'GET',
    authToken,
  });

  return DepartmentRequirementsResponseSchema.parse(response);
}

export async function performQuickAction(
  authToken: string,
  actionRequest: DepartmentQuickActionRequest
): Promise<DepartmentQuickActionResponse> {
  const response = await requestAPI({
    endpoint: 'v1/director/departments/quick-action',
    method: 'POST',
    data: actionRequest,
    authToken,
  });

  return DepartmentQuickActionResponseSchema.parse(response);
}

// Utility functions for available roles
export const AVAILABLE_DEPARTMENT_ROLES = [
  {
    id: 'reviewer',
    name: 'Reviewer',
    description: 'Reviewer of procedures and documents',
  },
  {
    id: 'counter',
    name: 'Counter',
    description: 'Front desk and customer service staff',
  },
  {
    id: 'technician',
    name: 'Technician',
    description: 'Specialized technical staff',
  },
];

// Update department
export async function updateDepartment(
  authToken: string,
  departmentId: number,
  updateData: Partial<{
    name: string;
    description: string;
    is_active: boolean;
    can_approve_procedures: boolean;
    can_reject_procedures: boolean;
    requires_all_requirements: boolean;
  }>
): Promise<DepartmentFullInfo> {
  const response = await requestAPI({
    endpoint: `v1/director/departments/${departmentId}`,
    method: 'PUT',
    data: updateData,
    authToken,
  });

  return DepartmentFullInfoSchema.parse(response);
}

// Create new department
export async function createDepartment(
  authToken: string,
  departmentData: {
    name: string;
    code: string;
    description?: string;
    municipality_id: number;
    is_active?: boolean;
    can_approve_procedures?: boolean;
    can_reject_procedures?: boolean;
    requires_all_requirements?: boolean;
  }
): Promise<DepartmentFullInfo> {
  const response = await requestAPI({
    endpoint: `v1/director/departments`,
    method: 'POST',
    data: departmentData,
    authToken,
  });

  return DepartmentFullInfoSchema.parse(response);
}

// Toggle user activation for reviews
export async function toggleUserActivationForReviews(
  accessToken: string,
  departmentId: number,
  userId: number,
  isActive: boolean
): Promise<{
  success: boolean;
  message: string;
  user_id: number;
  is_active_for_reviews: boolean;
}> {
  const response = await fetch(
    `/v1/director/departments/${departmentId}/users/${userId}/toggle-activation?is_active=${isActive}`,
    {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    throw new Error('Failed to toggle user activation');
  }

  return await response.json();
}
