import { z } from 'zod';

/**
 * Shared password validation schema
 * Requirements:
 * - At least 8 characters long
 * - Contains at least one uppercase letter
 * - Contains at least one lowercase letter
 * - Contains at least one number
 * - Contains at least one special character
 */
export const passwordSchema = z
  .string()
  .min(8, { message: 'input.passwordInvalid' })
  .regex(/[A-Z]/, { message: 'input.passwordInvalid' })
  .regex(/[a-z]/, { message: 'input.passwordInvalid' })
  .regex(/\d/, { message: 'input.passwordInvalid' })
  .regex(/[!@#$%^&*()_\-+={[}\]|:;"'<,>.?]/, {
    message: 'input.passwordInvalid',
  });

/**
 * Schema for forms that require password confirmation
 * Includes both password and confirmPassword fields with matching validation
 */
export const passwordWithConfirmationSchema = z
  .object({
    password: passwordSchema,
    confirmPassword: z.string().min(1, { message: 'input.required' }),
  })
  .refine(data => data.password === data.confirmPassword, {
    message: 'input.passwordMismatch',
    path: ['confirmPassword'],
  });

export type PasswordWithConfirmation = z.infer<
  typeof passwordWithConfirmationSchema
>;
