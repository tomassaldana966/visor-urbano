import { getSession } from '../sessions.server';
import { handleUnauthorized } from './unauthorized.server';

export type AuthUser = {
  id: number;
  name: string;
  email: string;
  role_name?: string;
  role_id?: number;
  municipality_id?: number;
  municipality_data?: {
    id: number;
    name: string;
    director?: string;
    address?: string;
    phone?: string;
  };
  municipality_geospatial?: {
    entity_code: string;
    municipality_code: string;
    geocode: string;
    has_zoning: boolean;
  };
};

export type AuthData = {
  access_token: string;
  user: AuthUser;
};

/**
 * Require authentication and return the authenticated user
 * Redirects to login if not authenticated
 */
export async function requireAuth(request: Request): Promise<AuthUser> {
  const session = await getSession(request.headers.get('Cookie'));

  if (!session.has('access_token')) {
    await handleUnauthorized(request);
  }

  const user = session.get('user') as AuthUser;

  if (!user) {
    await handleUnauthorized(request);
  }

  return user;
}

/**
 * Get the current authenticated user without throwing on missing auth
 * Returns null if not authenticated
 */
export async function getAuthUser(request: Request): Promise<AuthUser | null> {
  const session = await getSession(request.headers.get('Cookie'));

  if (!session.has('access_token')) {
    return null;
  }

  return session.get('user') as AuthUser | null;
}

/**
 * Get the access token from the session
 */
export async function getAccessToken(request: Request): Promise<string | null> {
  const session = await getSession(request.headers.get('Cookie'));
  return session.get('access_token') ?? null;
}

/**
 * Require an access token for API requests
 * Redirects to login if not authenticated
 */
export async function requireAccessToken(request: Request): Promise<string> {
  const accessToken = await getAccessToken(request);

  if (!accessToken) {
    return await handleUnauthorized(request);
  }

  return accessToken;
}
