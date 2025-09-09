import { Button } from '@/components/Button/Button';
import { Input } from '@/components/Input/Input';
import { Logo } from 'config/constants';
import { Lock, Mail } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import {
  data,
  Form,
  Link,
  redirect,
  useActionData,
  useLoaderData,
  useNavigation,
  type ActionFunctionArgs,
  type LoaderFunctionArgs,
} from 'react-router';
import { z } from 'zod';
import { zx } from 'zodix';
import { getObjectFromZodIssues, ZodInputs } from '../utils/zod/zod';
import { login } from '../utils/api/api.server';
import { commitSession, getSession } from '../utils/sessions.server';
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from '../components/Dialog/Dialog';
import { BloombergLogo } from '../components/Logos/Bloomberg';

export function meta() {
  return [{ title: 'Visor Urbano | Login' }];
}

export async function loader({ request }: LoaderFunctionArgs) {
  const session = await getSession(request.headers.get('Cookie'));

  if (session.has('access_token')) {
    return redirect('/notifications');
  }

  const registerSuccess = session.get('success') === 'register.success';
  const loginError = session.get('error') === 'login.error';

  return data(
    {
      registerSuccess,
      loginError,
    },
    {
      headers: {
        'Set-Cookie': await commitSession(session),
      },
    }
  );
}

export async function action({ request }: ActionFunctionArgs) {
  const session = await getSession(request.headers.get('Cookie'));

  const result = await zx.parseFormSafe(
    request,
    z.object({
      email: ZodInputs.email,
      password: z.string().min(1, {
        message: 'input.required',
      }),
    })
  );

  const errors = getObjectFromZodIssues(result.error?.issues);

  if (!errors) {
    const user = await login(result.data);

    if (!user) {
      session.flash('error', 'login.error');

      return redirect('/login', {
        headers: {
          'Set-Cookie': await commitSession(session),
        },
      });
    }

    session.set('access_token', user.access_token);
    session.set('user', user.user);

    // Role-based redirection
    const roleName = user.user.role_name?.toLowerCase();
    let redirectPath = '/notifications'; // Default redirect

    if (
      roleName === 'director' ||
      roleName === 'director_admin' ||
      roleName === 'director_municipal'
    ) {
      redirectPath = '/director/dashboard';
    }

    return redirect(redirectPath, {
      headers: {
        'Set-Cookie': await commitSession(session),
      },
    });
  }

  return data(
    {
      errors,
    },
    {
      headers: {
        'Set-Cookie': await commitSession(session),
      },
    }
  );
}

export default function () {
  const { t: tLogin } = useTranslation('login');

  const loaderData = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();

  const navigation = useNavigation();

  const isSubmitting = navigation.state === 'submitting';

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

      {loaderData.registerSuccess ? (
        <Dialog defaultOpen>
          <DialogContent>
            <DialogTitle className="text-primary">
              {tLogin('register.success.title')}
            </DialogTitle>

            <DialogDescription className="flex flex-col gap-4">
              {tLogin('register.success.description')}
            </DialogDescription>

            <DialogClose asChild>
              <Button type="button">{tLogin('register.success.close')}</Button>
            </DialogClose>
          </DialogContent>
        </Dialog>
      ) : null}

      {loaderData.loginError ? (
        <Dialog defaultOpen>
          <DialogContent>
            <DialogTitle className="text-destructive">
              {tLogin('errors.invalidCredentials.title')}
            </DialogTitle>

            <DialogDescription className="flex flex-col gap-4">
              {tLogin('errors.invalidCredentials.description')}
            </DialogDescription>

            <DialogClose asChild>
              <Button type="button">
                {tLogin('errors.invalidCredentials.close')}
              </Button>
            </DialogClose>
          </DialogContent>
        </Dialog>
      ) : null}

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
          {tLogin('title')}
        </h1>

        <Input
          disabled={isSubmitting}
          type="email"
          name="email"
          label={tLogin('email.label')}
          post={<Mail className="text-gray-400" size={16} />}
          error={actionData?.errors?.email}
        />

        <Input
          disabled={isSubmitting}
          type="password"
          name="password"
          label={tLogin('password.label')}
          post={<Lock className="text-gray-400" size={16} />}
          error={actionData?.errors?.password}
        />

        <div className="flex flex-col items-center gap-8">
          <div className="max-w-8/12 w-full flex flex-col self-center gap-4">
            <Link
              viewTransition
              to="/change-password"
              className="text-center text-sm text-primary"
            >
              {tLogin('forgotPassword')}
            </Link>

            <Button type="submit">{tLogin('submit')}</Button>
          </div>

          <div className="max-w-8/12 w-full flex flex-col self-center gap-4">
            <span className="text-gray-400 text-center">
              {tLogin('register.title')}
            </span>

            <Button type="button" asChild variant="tertiary">
              <Link viewTransition to="/register">
                {tLogin('register.link')}
              </Link>
            </Button>
          </div>
        </div>
      </Form>
    </main>
  );
}
