import { type LoaderFunctionArgs } from 'react-router';

export async function loader({ params }: LoaderFunctionArgs) {
  const { uuid } = params;

  if (!uuid) {
    throw new Response('Not Found', { status: 404 });
  }

  try {
    const apiUrl = process.env.API_URL;

    const response = await fetch(`${apiUrl}/v1/technical_sheets/${uuid}`);

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
        'Content-Disposition': `inline; filename="technical-sheet-${uuid}.pdf"`,
        'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
      },
    });
  } catch (error) {
    if (error instanceof Response) {
      throw error;
    }

    throw new Response('Internal server error', { status: 500 });
  }
}
