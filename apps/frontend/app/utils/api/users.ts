import { z } from 'zod';
import { requestAPI } from './base';
import {
  userSchema,
  usersListSchema,
  type User,
  type CreateUserData,
  type UpdateUserData,
} from '@root/app/schemas/users';

export async function getUsers(
  authToken: string,
  params?: { search?: string; role?: string }
): Promise<User[]> {
  const response = await requestAPI({
    endpoint: 'v1/users/',
    method: 'GET',
    data: params,
    authToken,
  });

  const result = usersListSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for users');
  }
}

export async function getUserById(
  authToken: string,
  id: number
): Promise<User> {
  const response = await requestAPI({
    endpoint: `v1/users/${id}`,
    method: 'GET',
    authToken,
  });

  const result = userSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for user');
  }
}

export async function createUser(
  authToken: string,
  userData: CreateUserData
): Promise<User> {
  const response = await requestAPI({
    endpoint: 'v1/users/',
    method: 'POST',
    data: userData,
    authToken,
  });

  const result = userSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for created user');
  }
}

export async function updateUser(
  authToken: string,
  id: number,
  userData: UpdateUserData
): Promise<User> {
  const response = await requestAPI({
    endpoint: `v1/users/${id}`,
    method: 'PUT',
    data: userData,
    authToken,
  });

  const result = userSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for updated user');
  }
}

export async function deleteUser(
  authToken: string,
  id: number
): Promise<{ message: string }> {
  const response = await requestAPI({
    endpoint: `v1/users/${id}`,
    method: 'DELETE',
    authToken,
  });

  return response;
}
