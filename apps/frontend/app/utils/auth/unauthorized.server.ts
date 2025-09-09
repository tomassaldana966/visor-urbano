import { redirect } from 'react-router';
import { destroySession, getSession } from '../sessions.server';
import { UnauthorizedError } from '../api/api.server';

/**
 * Handle unauthorized errors by clearing the session and redirecting to login
 */
export async function handleUnauthorized(request: Request): Promise<never> {
  const session = await getSession(request.headers.get('Cookie'));

  // Clear the session data
  const destroyedSession = await destroySession(session);

  throw redirect('/login', {
    headers: {
      'Set-Cookie': destroyedSession,
    },
  });
}

/**
 * Wrapper to catch unauthorized errors and handle them appropriately
 */
export async function withUnauthorizedHandler<T>(
  request: Request,
  fn: () => Promise<T>
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (error instanceof UnauthorizedError) {
      await handleUnauthorized(request);
    }
    throw error;
  }
}
