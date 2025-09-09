import { getSession } from '../sessions.server';
import { handleUnauthorized } from './unauthorized.server';
import type { AuthUser } from './auth.server';

export async function requireUser(request: Request) {
  const session = await getSession(request.headers.get('Cookie'));

  if (!session.has('access_token')) {
    await handleUnauthorized(request);
  }

  return {
    access_token: session.get('access_token'),
    user: session.get('user') as AuthUser,
  };
}
