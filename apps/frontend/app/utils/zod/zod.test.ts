import { describe, expect, it } from 'vitest';
import { z } from 'zod';
import { getObjectFromZodIssues } from './zod';

describe('utils/zod', () => {
  describe('getObjectFromIssues', () => {
    const schema = z.object({
      name: z.string({ message: 'Required' }),
      age: z.number().min(18, { message: 'min 18' }),
    });

    it('should return an object with the errors', () => {
      expect(
        getObjectFromZodIssues(schema.safeParse({ age: 17 }).error?.issues)
      ).toStrictEqual({
        name: 'Required',
        age: 'min 18',
      });
    });

    it('should return null if there are no errors', () => {
      expect(
        getObjectFromZodIssues(
          schema.safeParse({ name: 'John', age: 18 }).error?.issues
        )
      ).toStrictEqual(null);
    });

    it('should return null if issues is undefined', () => {
      expect(getObjectFromZodIssues()).toStrictEqual(null);
    });
  });
});
