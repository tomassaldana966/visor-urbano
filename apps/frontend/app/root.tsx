import React, { Suspense } from 'react';
import {
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from 'react-router';

import i18n from './i18n';

import './app.css';
import 'react-loading-skeleton/dist/skeleton.css';
import { I18nextProvider } from 'react-i18next';

export const links = () => [
  { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
  {
    rel: 'preconnect',
    href: 'https://fonts.gstatic.com',
    crossOrigin: 'anonymous',
  },
  {
    rel: 'stylesheet',
    href: 'https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap',
  },
  // Apple Touch Icons for Safari/iOS
  { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
  {
    rel: 'apple-touch-icon-precomposed',
    href: '/apple-touch-icon-precomposed.png',
  },
  // Standard favicon
  { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
];

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Visor Urbano" />
        <Meta />
        <Links />
      </head>
      <body>
        <Suspense fallback={<div />}>
          <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
        </Suspense>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function Root() {
  return <Outlet />;
}

export function ErrorBoundary({ error }: { error: unknown }) {
  let message = 'Oops!';
  let details = 'An unexpected error occurred.';
  let stack: string | undefined;
  let statusCode = 500;

  if (isRouteErrorResponse(error)) {
    statusCode = error.status;
    message = error.status === 404 ? '404' : 'Error';
    details =
      error.status === 404
        ? 'The requested page could not be found.'
        : error.statusText || details;
  } else if (import.meta.env.DEV && error && error instanceof Error) {
    details = error.message;
    stack = error.stack;
  }

  const is404 = statusCode === 404;

  return (
    <div className="min-h-screen bg-gradient-to-br from-vu-light-gray to-white flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
          {/* Header */}
          <div
            className={`px-8 py-12 text-center ${is404 ? 'bg-gradient-to-r from-vu-primary to-vu-green' : 'bg-gradient-to-r from-red-500 to-red-600'}`}
          >
            <div className="text-white">
              <h1 className="text-8xl font-bold mb-4">
                {is404 ? '404' : statusCode}
              </h1>
              <h2 className="text-2xl font-semibold">{message}</h2>
            </div>
          </div>

          {/* Content */}
          <div className="px-8 py-8">
            <div className="text-center mb-8">
              <p className="text-gray-600 text-lg mb-6">{details}</p>

              {is404 ? (
                <div className="space-y-4">
                  <p className="text-gray-500">
                    The page you're looking for might have been moved, deleted,
                    or doesn't exist.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <a
                      href="/"
                      className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-vu-primary text-white font-semibold rounded-lg hover:bg-vu-green transition-colors shadow-sm"
                    >
                      Go Home
                    </a>
                    <button
                      onClick={() => window.history.back()}
                      className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-colors"
                    >
                      Go Back
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <p className="text-gray-500">
                    Something went wrong on our end. Please try again later.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <button
                      onClick={() => window.location.reload()}
                      className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-vu-primary text-white font-semibold rounded-lg hover:bg-vu-green transition-colors shadow-sm"
                    >
                      Try Again
                    </button>
                    <a
                      href="/"
                      className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-colors"
                    >
                      Go Home
                    </a>
                  </div>
                </div>
              )}
            </div>

            {/* Development stack trace */}
            {stack && import.meta.env.DEV && (
              <details className="mt-8 p-4 bg-gray-50 rounded-lg border">
                <summary className="cursor-pointer font-medium text-gray-700 mb-2">
                  View technical details
                </summary>
                <pre className="text-xs text-gray-600 overflow-x-auto whitespace-pre-wrap break-words">
                  <code>{stack}</code>
                </pre>
              </details>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
