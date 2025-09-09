import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import { requireAuth, getAccessToken } from '../utils/auth/auth.server';
import {
  checkDirectorPermissions,
  checkAdminPermissions,
} from '../utils/auth/director';
import {
  getBusinessLicenses,
  updateBusinessLicensePayment,
  uploadPaymentReceipt,
  updateBusinessLicenseStatus,
  uploadStatusFile,
} from '../utils/api/api.server';

// Server-side loader function
export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  const authToken = await getAccessToken(request);

  // Check if user has proper permissions (Director, Admin, or Supervisor)
  if (!checkDirectorPermissions(user) && !checkAdminPermissions(user)) {
    throw new Response(
      'Acceso no autorizado - Se requieren permisos de director o administrador',
      {
        status: 403,
      }
    );
  }

  // Extract pagination parameters from URL
  const url = new URL(request.url);
  const page = parseInt(url.searchParams.get('page') || '1');
  const perPage = 20; // Fixed to 20 items per page

  try {
    // Get business licenses from API with pagination
    const licensesResponse = await getBusinessLicenses({
      municipality_id: user.municipality_id || 1,
      page,
      per_page: perPage,
      authToken: authToken || '', // Use the authToken from session
    });

    return {
      user,
      licenses: licensesResponse.items,
      pagination: {
        page: licensesResponse.page,
        per_page: licensesResponse.per_page,
        total: licensesResponse.total,
        total_pages: licensesResponse.total_pages,
      },
      municipalityName: user.municipality_data?.name || 'Municipio',
      authToken: authToken || '',
    };
  } catch (error) {
    // Fallback to empty array if API fails
    return {
      user,
      licenses: [],
      pagination: {
        page: 1,
        per_page: perPage,
        total: 0,
        total_pages: 1,
      },
      municipalityName: user.municipality_data?.name || 'Municipio',
      error: 'licenses:errors.loadingError',
      authToken: authToken || '',
    };
  }
}

export async function action({ request }: ActionFunctionArgs) {
  const user = await requireAuth(request);
  const authToken = await getAccessToken(request);

  // Check permissions
  if (!checkDirectorPermissions(user) && !checkAdminPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  const formData = await request.formData();
  const intent = formData.get('_intent') as string;
  const licenseFolio = formData.get('licenseFolio') as string;

  try {
    switch (intent) {
      case 'updatePayment': {
        const paymentStatus = parseInt(formData.get('paymentStatus') as string);
        const paymentReceiptFile =
          (formData.get('paymentReceiptFile') as string) || undefined;

        await updateBusinessLicensePayment({
          license_folio: licenseFolio,
          payment_status: paymentStatus,
          payment_receipt_file: paymentReceiptFile,
          authToken: authToken || '',
        });

        return {
          success: true,
          action: 'updatePayment',
          paymentStatus: paymentStatus,
          message: 'Payment updated successfully',
        };
      }

      case 'uploadReceipt': {
        const receiptFile = formData.get('receiptFile') as File;

        if (!receiptFile) {
          return { success: false, error: 'No file provided' };
        }

        // Upload receipt (this now also marks as paid automatically)
        const result = await uploadPaymentReceipt(
          authToken || '',
          licenseFolio,
          receiptFile
        );

        return {
          success: true,
          action: 'uploadReceipt',
          paymentStatus: 1,
          message: 'Receipt uploaded and payment updated successfully',
          filePath: result,
        };
      }

      case 'updateStatus': {
        const licenseStatus = formData.get('licenseStatus') as string;
        const reason = (formData.get('reason') as string) || undefined;
        let reasonFile: string | undefined;

        // Check if there's a status file to upload
        const statusFile = formData.get('statusFile') as File;
        if (statusFile && statusFile.size > 0) {
          reasonFile = await uploadStatusFile(
            authToken || '',
            licenseFolio,
            statusFile
          );
        }

        await updateBusinessLicenseStatus({
          license_folio: licenseFolio,
          license_status: licenseStatus,
          reason: reason,
          reason_file: reasonFile,
          authToken: authToken || '',
        });

        return {
          success: true,
          action: 'updateStatus',
          licenseStatus: licenseStatus,
          message: 'License status updated successfully',
        };
      }

      default:
        return { success: false, error: 'Invalid intent' };
    }
  } catch (error) {
    console.error('Error handling action:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}
