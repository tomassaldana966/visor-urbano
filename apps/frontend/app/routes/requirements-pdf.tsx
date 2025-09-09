import { type LoaderFunctionArgs } from 'react-router';

export async function loader({ params }: LoaderFunctionArgs) {
  const { folio } = params;

  if (!folio) {
    throw new Response('Not Found', { status: 404 });
  }

  try {
    const apiUrl = process.env.API_URL;

    const response = await fetch(
      `${apiUrl}/v1/requirements-queries/${folio}/requirements/pdf`
    );

    if (!response.ok) {
      if (response.status === 404) {
        throw new Response('Not Found', { status: 404 });
      }
      throw new Response('Error fetching technical sheet', {
        status: response.status,
      });
    }

    const pdfBuffer = await response.arrayBuffer();

    return new Response(pdfBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `inline; filename="requirements-${folio}.pdf"`,
        'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
      },
    });
  } catch (error) {
    console.error('Error proxying technical sheet:', error);

    if (error instanceof Response) {
      throw error;
    }

    throw new Response('Internal server error', { status: 500 });
  }
}
