import { Button } from '@/components/Button/Button';
import { Input } from '@/components/Input/Input';
import { Logo } from 'config/constants';
import { Lock } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import {
  Form,
  Link,
  useActionData,
  useSearchParams,
  redirect,
  type ActionFunctionArgs,
  type LoaderFunctionArgs,
} from 'react-router';
import { z } from 'zod';
import { zx } from 'zodix';
import { getObjectFromZodIssues } from '@/utils/zod/zod';
import { BloombergLogo } from '../components/Logos/Bloomberg';
import { resetPassword } from '../utils/api/api.server';
import { passwordSchema } from '../schemas/password';

export function meta() {
  return [{ title: 'Visor Urbano | Reset Password' }];
}

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const token = url.searchParams.get('token');

  if (!token) {
    throw new Response('Token is required', { status: 400 });
  }

  return { token };
}

export async function action({ request }: ActionFunctionArgs) {
  const url = new URL(request.url);
  const token = url.searchParams.get('token');

  if (!token) {
    return {
      errors: { general: 'Token is required' },
    };
  }

  const result = await zx.parseFormSafe(
    request,
    z
      .object({
        email: z.string().email({ message: 'input.emailInvalid' }),
        password: passwordSchema,
        confirmPassword: z.string().min(1, { message: 'input.required' }),
      })
      .refine(data => data.password === data.confirmPassword, {
        message: 'input.passwordMismatch',
        path: ['confirmPassword'],
      })
  );

  const errors = getObjectFromZodIssues(result?.error?.issues);

  if (!errors && result.data) {
    try {
      const response = await resetPassword({
        email: result.data.email,
        password: result.data.password,
        token: token,
      });

      if (response?.success) {
        return redirect('/login?message=password-reset-success');
      } else {
        return {
          errors: { general: response?.error ?? 'Failed to reset password' },
        };
      }
    } catch (error) {
      console.error('Reset password error:', error);
      return {
        errors: { general: 'An error occurred while resetting your password' },
      };
    }
  }

  return {
    errors,
  };
}

export default function ResetPassword() {
  const { t } = useTranslation('common');
  const [searchParams] = useSearchParams();
  const actionData = useActionData<typeof action>();
  const token = searchParams.get('token');

  if (!token) {
    return (
      <main className="min-w-screen min-h-screen flex items-center justify-center bg-primary/80">
        <div className="flex flex-col gap-6 bg-white rounded-2xl shadow-2xl px-6 py-12 w-full max-w-lg mx-auto text-center">
          <h1 className="text-xl text-red-600">Invalid Reset Link</h1>
          <p className="text-gray-600">
            The password reset link is invalid or has expired.
          </p>
          <Button asChild variant="primary">
            <Link to="/login">Back to Login</Link>
          </Button>
        </div>
      </main>
    );
  }

  return (
    <main
      className="min-w-screen min-h-screen flex items-center justify-center bg-primary/80"
      style={{
        backgroundImage:
          'url(/background/login.png), url(/background/login-2.svg)',
        backgroundPosition: '80vw 100%, bottom',
        backgroundRepeat: 'no-repeat, repeat-x',
        viewTransitionName: 'container',
      }}
    >
      <header className="absolute top-0 inset-x-0 justify-between flex p-8 items-center">
        {Logo}
        <BloombergLogo className="h-12" />
      </header>

      <Form
        className="flex flex-col gap-6 bg-white rounded-2xl shadow-2xl px-6 py-12 w-full max-w-lg mx-auto"
        method="POST"
      >
        <Link to="/">
          <img
            style={{
              viewTransitionName: 'logo',
            }}
            src="/logos/visor-urbano.svg"
            alt="Visor Urbano"
            className="h-12"
          />
        </Link>

        <h1
          style={{
            viewTransitionName: 'title',
          }}
          className="text-center text-lg"
        >
          Reset Your Password
        </h1>

        {actionData?.errors?.general ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {actionData.errors.general}
          </div>
        ) : null}

        <div className="flex flex-col gap-4">
          <Input
            type="email"
            label="Email Address"
            name="email"
            error={actionData?.errors?.email}
            placeholder="Enter your email address"
            required
          />

          <Input
            type="password"
            label="New Password"
            name="password"
            error={actionData?.errors?.password}
            post={<Lock className="text-gray-400" size={16} />}
            placeholder="Enter your new password"
            required
          />

          <Input
            type="password"
            label="Confirm New Password"
            post={<Lock className="text-gray-400" size={16} />}
            name="confirmPassword"
            error={actionData?.errors?.confirmPassword}
            placeholder="Confirm your new password"
            required
          />
        </div>

        <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded">
          <p className="font-medium mb-1">Password requirements:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>At least 8 characters long</li>
            <li>Contains at least one uppercase letter</li>
            <li>Contains at least one lowercase letter</li>
            <li>Contains at least one number</li>
            <li>Contains at least one special character</li>
          </ul>
        </div>

        <div className="flex flex-col items-center gap-4">
          <div className="w-full flex flex-col gap-4">
            <Button type="submit">Reset Password</Button>
          </div>

          <div className="w-full flex flex-col gap-4">
            <span className="text-gray-400 text-center text-sm">
              Remember your password?
            </span>

            <Button type="button" asChild variant="tertiary">
              <Link viewTransition to="/login">
                Back to Login
              </Link>
            </Button>
          </div>
        </div>
      </Form>
    </main>
  );
}
