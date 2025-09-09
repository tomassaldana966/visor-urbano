import { z } from 'zod';

export function getObjectFromZodIssues(issues?: z.ZodIssue[]) {
  let errors: Record<string, string> | null = null;

  if (!issues) {
    return errors;
  }

  for (const [_key, value] of issues.entries()) {
    if (!errors) {
      errors = {};
    }

    if (value.path.length > 0) {
      errors[value.path[0]] = value.message;
    }
  }

  return errors;
}

export const ZodInputs = {
  email: z.string().email({ message: 'input.email' }),
};
