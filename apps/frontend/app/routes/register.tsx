import { Button } from '@/components/Button/Button';
import { Input } from '@/components/Input/Input';
import { PrivacyModal } from '@/components/PrivacyModal/PrivacyModal';
import { Logo } from 'config/constants';
import {
  CircleUserRound,
  Fingerprint,
  Lock,
  Mail,
  Smartphone,
} from 'lucide-react';
import type { PropsWithChildren } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import {
  Form,
  Link,
  redirect,
  useActionData,
  type ActionFunctionArgs,
} from 'react-router';
import { z } from 'zod';
import { zx } from 'zodix';
import { getObjectFromZodIssues, ZodInputs } from '@/utils/zod/zod';
import { register } from '@/utils/api/api.server';
import { commitSession, getSession } from '../utils/sessions.server';
import { BloombergLogo } from '../components/Logos/Bloomberg';
import { Checkbox } from '../components/Checkbox/Checkbox';
import { passwordSchema } from '../schemas/password';

export function meta() {
  return [{ title: 'Visor Urbano | Register' }];
}

function Privacy({ children }: PropsWithChildren) {
  return (
    <PrivacyModal>
      <button type="button" className="text-primary">
        {children}
      </button>
    </PrivacyModal>
  );
}

export async function action({ request }: ActionFunctionArgs) {
  const session = await getSession(request.headers.get('Cookie'));

  const result = await zx.parseFormSafe(
    request,
    z
      .object({
        name: z.string().min(1, { message: 'input.required' }),
        paternal_last_name: z.string().min(1, { message: 'input.required' }),
        maternal_last_name: z.string().min(1, { message: 'input.required' }),
        cellphone: z.string().min(1, { message: 'input.required' }),
        email: ZodInputs.email,
        municipality_id: z.string().min(1, { message: 'input.required' }),
        password: passwordSchema,
        confirmPassword: z.string().min(1, { message: 'input.required' }),
        privacy: z
          .string({ message: 'input.required' })
          .refine(val => val === 'on', {
            message: 'input.required',
          }),
      })
      .refine(data => data.password === data.confirmPassword, {
        message: 'input.passwordMismatch',
        path: ['confirmPassword'],
      })
  );

  const errors = getObjectFromZodIssues(result?.error?.issues);

  if (!errors) {
    const { id } = await register(result.data);

    if (id) {
      session.flash('success', 'register.success');

      return redirect('/login', {
        headers: {
          'Set-Cookie': await commitSession(session),
        },
      });
    }
  }

  return {
    errors,
  };
}

export default function () {
  const { t: tRegister } = useTranslation('register');

  const actionData = useActionData<typeof action>();

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
          {tRegister('title')}
        </h1>

        <div className="grid md:grid-cols-2 gap-4">
          <Input
            label={tRegister('inputs.name.label')}
            post={<CircleUserRound className="text-gray-400" size={16} />}
            name="name"
            error={actionData?.errors?.name}
          />

          <Input
            label={tRegister('inputs.firstLastName.label')}
            post={<CircleUserRound className="text-gray-400" size={16} />}
            name="paternal_last_name"
            error={actionData?.errors?.paternal_last_name}
          />

          <Input
            label={tRegister('inputs.secondLastName.label')}
            post={<CircleUserRound className="text-gray-400" size={16} />}
            name="maternal_last_name"
            error={actionData?.errors?.maternal_last_name}
          />

          <Input
            label={tRegister('inputs.cellphone.label')}
            post={<Smartphone className="text-gray-400" size={16} />}
            name="cellphone"
            error={actionData?.errors?.cellphone}
          />

          <Input
            label={tRegister('inputs.curp.label')}
            post={<Fingerprint className="text-gray-400" size={16} />}
            name="municipality_id"
            error={actionData?.errors?.municipality_id}
          />

          <Input
            type="email"
            label={tRegister('inputs.email.label')}
            post={<Mail className="text-gray-400" size={16} />}
            name="email"
            error={actionData?.errors?.email}
          />

          <div className="col-span-2 grid-cols-subgrid grid">
            <Input
              type="password"
              label={tRegister('inputs.password.label')}
              name="password"
              error={actionData?.errors?.password}
              post={<Lock className="text-gray-400" size={16} />}
            />

            <Input
              type="password"
              label={tRegister('inputs.verifyPassword.label')}
              post={<Lock className="text-gray-400" size={16} />}
              name="confirmPassword"
              error={actionData?.errors?.confirmPassword}
            />
          </div>

          <div className="col-span-2 flex text-center justify-center text-sm text-gray-400">
            <Checkbox
              name="privacy"
              label={
                <Trans
                  i18nKey="register:inputs.privacy.label"
                  components={{
                    privacy: <Privacy />,
                  }}
                />
              }
              error={actionData?.errors?.privacy}
            />
          </div>
        </div>

        <div className="flex flex-col items-center gap-8">
          <div className="max-w-8/12 w-full flex flex-col self-center gap-4">
            <Button type="submit">{tRegister('submit')}</Button>
          </div>

          <div className="max-w-8/12 w-full flex flex-col self-center gap-4">
            <span className="text-gray-400 text-center">
              {tRegister('login.title')}
            </span>

            <Button type="button" asChild variant="tertiary">
              <Link viewTransition to="/login">
                {tRegister('login.link')}
              </Link>
            </Button>
          </div>
        </div>
      </Form>
    </main>
  );
}
