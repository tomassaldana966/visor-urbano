import { createCookieSessionStorage } from 'react-router';

type SessionData = {
  access_token: string;
  user: {
    name: string;
  };
};

type SessionFlashData = {
  error: string;
  success: string;
};

const { getSession, commitSession, destroySession } =
  createCookieSessionStorage<SessionData, SessionFlashData>({
    cookie: {
      name: '__session',
      httpOnly: process.env.NODE_ENV === 'production', // Enable httpOnly in production for security
      maxAge: 60 * 60 * 24 * 7,
      path: '/',
      sameSite: 'lax',
      secrets: [process.env.COOKIES_SECRET ?? 'please set a secret'],
      secure: process.env.NODE_ENV === 'production', // Only secure in production
    },
  });

export { getSession, commitSession, destroySession };
