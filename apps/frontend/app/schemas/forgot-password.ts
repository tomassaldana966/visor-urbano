import { z } from 'zod';

export const forgotPasswordRequestSchema = z.object({
  email: z.string().email({ message: 'input.email.invalid' }),
});

export const forgotPasswordResponseSchema = z.object({
  detail: z.string(),
  success: z.boolean(),
});

export const forgotPasswordErrorSchema = z.object({
  detail: z.array(
    z.object({
      loc: z.array(z.union([z.string(), z.number()])),
      msg: z.string(),
      type: z.string(),
    })
  ),
});

export type ForgotPasswordRequest = z.infer<typeof forgotPasswordRequestSchema>;
export type ForgotPasswordResponse = z.infer<
  typeof forgotPasswordResponseSchema
>;
export type ForgotPasswordError = z.infer<typeof forgotPasswordErrorSchema>;
