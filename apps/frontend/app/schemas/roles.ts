import { z } from 'zod';

// Role schema for API responses
export const roleSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string(),
  municipality_id: z.number(),
  deleted_at: z.string().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

// Role creation schema for API requests
export const createRoleSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().min(1, 'Description is required'),
  // municipality_id is automatically set from current user on the backend
});

// Role update schema for API requests
export const updateRoleSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().min(1, 'Description is required'),
  // municipality_id should not be updated after creation
});

// Array of roles for list endpoints
export const rolesListSchema = z.array(roleSchema);

export type Role = z.infer<typeof roleSchema>;
export type CreateRoleData = z.infer<typeof createRoleSchema>;
export type UpdateRoleData = z.infer<typeof updateRoleSchema>;
