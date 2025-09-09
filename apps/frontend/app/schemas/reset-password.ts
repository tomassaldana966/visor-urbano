import { z } from 'zod';
import { passwordSchema } from './password';

export const resetPasswordRequestSchema = z.object({
  email: z.string().email({ message: 'input.emailInvalid' }),
  password: passwordSchema,
  token: z.string().min(1, { message: 'input.required' }),
});

export const resetPasswordResponseSchema = z.object({
  detail: z.string(),
  success: z.boolean(),
});

export const resetPasswordErrorSchema = z.object({
  detail: z.array(
    z.object({
      loc: z.array(z.union([z.string(), z.number()])),
      msg: z.string(),
      type: z.string(),
    })
  ),
});

export type ResetPasswordRequest = z.infer<typeof resetPasswordRequestSchema>;
export type ResetPasswordResponse = z.infer<typeof resetPasswordResponseSchema>;
export type ResetPasswordError = z.infer<typeof resetPasswordErrorSchema>;
