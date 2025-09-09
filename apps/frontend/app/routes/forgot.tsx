import { Button } from '@/components/Button/Button';
import { Input } from '@/components/Input/Input';
import { Logo } from 'config/constants';
import { Mail } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import {
  Form,
  Link,
  useActionData,
  useNavigation,
  type ActionFunctionArgs,
} from 'react-router';
import { zx } from 'zodix';
import { BloombergLogo } from '../components/Logos/Bloomberg';
import { forgotPassword } from '../utils/api/auth';
import {
  forgotPasswordRequestSchema,
  forgotPasswordErrorSchema,
} from '../schemas/forgot-password';
import { getObjectFromZodIssues } from '../utils/zod/zod';

export function meta() {
  return [{ title: 'Visor Urbano | Forgot Password' }];
}

export async function action({ request }: ActionFunctionArgs) {
  const result = await zx.parseFormSafe(request, forgotPasswordRequestSchema);

  const errors = getObjectFromZodIssues(result.error?.issues);

  if (errors) {
    return { errors, success: false };
  }

  try {
    const response = await forgotPassword(result.data);

    if (!response) {
      return {
        errors: { general: 'error.general' },
        success: false,
      };
    }

    if (!response.success) {
      return {
        errors: {
          general:
            typeof response.error === 'string'
              ? response.error
              : 'error.general',
        },
        success: false,
      };
    }

    return {
      success: true,
      message: 'success.message',
    };
  } catch (error) {
    console.error('Forgot password error:', error);

    if (error instanceof Error) {
      try {
        const errorData = JSON.parse(error.message);
        const errorResult = forgotPasswordErrorSchema.safeParse(errorData);
        if (errorResult.success) {
          const apiErrors: Record<string, string> = {};
          errorResult.data.detail.forEach(validationError => {
            if (validationError.loc.length > 0) {
              const field = validationError.loc[validationError.loc.length - 1];
              apiErrors[field] = validationError.msg;
            }
          });
          return { errors: apiErrors, success: false };
        }
      } catch (error) {
        console.error('Error parsing forgot password response:', error);
      }

      return {
        errors: { general: error.message },
        success: false,
      };
    }

    return {
      errors: { general: 'error.general' },
      success: false,
    };
  }
}

export default function () {
  const { t: tForgot } = useTranslation('forgot');
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
          {tForgot('title')}
        </h1>

        {actionData?.success ? (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 text-sm text-center">
              {tForgot('success.message')}
            </p>
          </div>
        ) : null}

        {actionData?.errors?.general ? (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-sm text-center">
              {tForgot(actionData.errors.general)}
            </p>
          </div>
        ) : null}

        <Input
          type="email"
          name="email"
          label={tForgot('email.label')}
          post={<Mail className="text-gray-400" size={16} />}
          error={
            actionData?.errors?.email
              ? tForgot(actionData.errors.email)
              : undefined
          }
        />

        <div className="flex flex-col items-center gap-8">
          <div className="max-w-8/12 w-full flex flex-col self-center gap-4">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? tForgot('submitting') : tForgot('submit')}
            </Button>
          </div>
        </div>
      </Form>
    </main>
  );
}
