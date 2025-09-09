import { z } from 'zod';
import { requestAPI } from './base';
import {
  roleSchema,
  rolesListSchema,
  type Role,
  type CreateRoleData,
  type UpdateRoleData,
} from '@root/app/schemas/roles';

// Export types for use in other components
export type { Role, CreateRoleData, UpdateRoleData };

export async function getRoles(authToken: string): Promise<Role[]> {
  const response = await requestAPI({
    endpoint: 'v1/roles',
    method: 'GET',
    authToken,
  });

  const result = rolesListSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for roles');
  }
}

export async function getRoleById(
  authToken: string,
  id: number
): Promise<Role> {
  const response = await requestAPI({
    endpoint: `v1/roles/${id}`,
    method: 'GET',
    authToken,
  });

  const result = roleSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for role');
  }
}

export async function createRole(
  authToken: string,
  roleData: CreateRoleData
): Promise<Role> {
  const response = await requestAPI({
    endpoint: 'v1/roles',
    method: 'POST',
    data: roleData,
    authToken,
  });

  const result = roleSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for created role');
  }
}

export async function updateRole(
  authToken: string,
  id: number,
  roleData: UpdateRoleData
): Promise<Role> {
  const response = await requestAPI({
    endpoint: `v1/roles/${id}`,
    method: 'PUT',
    data: roleData,
    authToken,
  });

  const result = roleSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for updated role');
  }
}

export async function deleteRole(
  authToken: string,
  id: number
): Promise<{ detail?: { loc: string[]; msg: string; type: string }[] }> {
  const response = await requestAPI({
    endpoint: `v1/roles/${id}`,
    method: 'DELETE',
    authToken,
  });

  return response;
}
