import { z } from 'zod';

// User creation schema for API requests
export const createUserSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  paternal_last_name: z.string().min(1, 'Paternal last name is required'),
  maternal_last_name: z.string().optional(),
  cellphone: z.string().min(1, 'Cellphone is required'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  municipality_id: z.number().min(1, 'Municipality is required'),
  role_id: z.number().min(1, 'Role is required'),
});

// User update schema for API requests
export const updateUserSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  paternal_last_name: z.string().min(1, 'Paternal last name is required'),
  maternal_last_name: z.string().optional(),
  cellphone: z.string().min(1, 'Cellphone is required'),
  email: z.string().email('Invalid email address'),
  password: z
    .string()
    .min(6, 'Password must be at least 6 characters')
    .optional(),
  municipality_id: z.number().min(1, 'Municipality is required'),
  role_id: z.number().min(1, 'Role is required'),
});

// User response schema from API
export const userSchema = z.object({
  id: z.number(),
  name: z.string(),
  paternal_last_name: z.string(),
  maternal_last_name: z.string().nullable(),
  cellphone: z.string(),
  email: z.string(),
  role_name: z.string().default('User'),
  municipality_data: z.record(z.unknown()).nullable(),
  municipality_geospatial: z.record(z.unknown()).nullable(),
});

// Array of users for list endpoints
export const usersListSchema = z.array(userSchema);

// User filters schema
export const userFiltersSchema = z.object({
  search: z.string().optional(),
  role: z.string().optional(),
});

export type CreateUserData = z.infer<typeof createUserSchema>;
export type UpdateUserData = z.infer<typeof updateUserSchema>;
export type User = z.infer<typeof userSchema>;
export type UserFilters = z.infer<typeof userFiltersSchema>;
