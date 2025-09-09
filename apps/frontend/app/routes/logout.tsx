import { redirect, type LoaderFunctionArgs } from 'react-router';
import { commitSession, getSession } from '../utils/sessions.server';

export function meta() {
  return [{ title: 'Visor Urbano | Login' }];
}

export async function loader({ request }: LoaderFunctionArgs) {
  const session = await getSession(request.headers.get('Cookie'));

  session.unset('access_token');

  return redirect('/', {
    headers: {
      'Set-Cookie': await commitSession(session),
    },
  });
}
