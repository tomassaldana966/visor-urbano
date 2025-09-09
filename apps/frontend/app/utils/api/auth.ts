import { z } from 'zod';
import { requestAPI } from './base';
import {
  forgotPasswordResponseSchema,
  type ForgotPasswordRequest,
} from '../../schemas/forgot-password';
import {
  resetPasswordResponseSchema,
  type ResetPasswordRequest,
} from '../../schemas/reset-password';

export async function register(data?: {
  cellphone: string;
  email: string;
  maternal_last_name: string;
  municipality_id: string;
  name: string;
  password: string;
  paternal_last_name: string;
}) {
  if (!data) {
    return;
  }

  return requestAPI({
    endpoint: 'v1/users',
    method: 'POST',
    data: {
      ...data,
      municipality_id: parseInt(data.municipality_id, 10),
    },
    skipAuth: true,
  });
}

export async function login(data?: { email: string; password: string }) {
  if (!data) {
    return;
  }

  try {
    const response = await requestAPI({
      endpoint: 'v1/auth/login',
      method: 'POST',
      data: {
        email: data.email,
        password: data.password,
      },
      skipAuth: true,
    })
      .then(response => {
        return response;
      })
      .catch(error => {
        console.error('Login error:', error);

        throw error;
      });

    const schema = z.object({
      access_token: z.string(),
      user: z.object({
        id: z.number(),
        name: z.string(),
        email: z.string(),
        role_name: z.string().optional(),
        role_id: z.number().optional(),
        municipality_id: z.number().optional(),
      }),
    });

    const result = schema.safeParse(response);

    if (result.success) {
      return result.data;
    }

    return null;
  } catch (error) {
    if (error instanceof Error && error.name === 'UnauthorizedError') {
      return null;
    }
    throw error;
  }
}

export async function forgotPassword(data?: ForgotPasswordRequest) {
  if (!data) {
    return;
  }

  const response = await requestAPI({
    endpoint: 'v1/password/reset-password-request',
    method: 'POST',
    data: {
      email: data.email,
    },
    skipAuth: true,
  });

  const successResult = forgotPasswordResponseSchema.safeParse(response);

  if (successResult.success) {
    return { success: true, data: successResult.data };
  }

  return { success: false, error: 'Invalid response format' };
}

export async function resetPassword(data?: ResetPasswordRequest) {
  if (!data) {
    return;
  }

  const response = await requestAPI({
    endpoint: 'v1/password/change-password',
    method: 'POST',
    data: {
      email: data.email,
      password: data.password,
      token: data.token,
    },
    skipAuth: true,
  });

  const successResult = resetPasswordResponseSchema.safeParse(response);

  if (successResult.success) {
    return { success: true, data: successResult.data };
  }

  return { success: false, error: 'Invalid response format' };
}
