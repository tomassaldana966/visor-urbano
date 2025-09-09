/**
 * Gets the workflow status from the backend using the debug endpoint
 */
export async function getWorkflowStatusFromBackend(
  authToken: string,
  folio: string
) {
  try {
    const encodedFolio = btoa(folio);
    const baseUrl =
      typeof window !== 'undefined'
        ? window.location.origin
        : 'http://localhost:8000';
    const response = await fetch(
      `${baseUrl}/v1/procedure-workflow/${encodedFolio}`,
      {
        headers: {
          Authorization: `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.ok) {
      return await response.json();
    } else {
      console.warn(
        `Workflow status API returned ${response.status}:`,
        await response.text()
      );
    }
  } catch (error) {
    console.warn('Could not fetch workflow status from backend:', error);
  }

  return null;
}
