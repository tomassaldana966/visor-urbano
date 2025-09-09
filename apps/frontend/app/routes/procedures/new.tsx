import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Form,
  useActionData,
  useNavigation,
  useLoaderData,
  redirect,
  type ActionFunctionArgs,
  type LoaderFunctionArgs,
  useSearchParams,
} from 'react-router';
import { Button } from '@/components/Button/Button';
import { Input } from '@/components/Input/Input';
import { Checkbox } from '@/components/Checkbox/Checkbox';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/Accordion/Accordion';
import { PrivacyModal } from '@/components/PrivacyModal/PrivacyModal';
import {
  validateFolio,
  createProcedure,
  getBusinessTypes,
} from '@/utils/api/api.server';
import { requireAuth, getAccessToken } from '@/utils/auth/auth.server';
import { FileText } from 'lucide-react';
import { z } from 'zod';
import { zx } from 'zodix';
import type { businessTypeSchema } from '@root/app/schemas/business-types';

// Type definition for folio validation result
interface FolioValidationResult {
  id: number;
  folio: string;
  [key: string]: unknown;
}

export const handle = {
  title: 'procedures:new.title',
  breadcrumb: 'procedures:new.breadcrumb',
};

export async function loader({ request }: LoaderFunctionArgs) {
  // Require authentication and provide user data
  const user = await requireAuth(request);
  const accessToken = await getAccessToken(request);

  // Get business types for the user's municipality if available
  let businessTypes: z.infer<typeof businessTypeSchema>[] = [];

  if (user.municipality_id && accessToken) {
    try {
      businessTypes = await getBusinessTypes({
        municipality_id: user.municipality_id,
      });
    } catch (error) {
      console.warn(error);
    }
  }

  return { user, businessTypes };
}

export async function action({ request }: ActionFunctionArgs) {
  await requireAuth(request);

  const authToken = await getAccessToken(request);

  if (!authToken) {
    throw new Response('Unauthorized', { status: 401 });
  }

  const result = await zx.parseFormSafe(
    request,
    z.object({
      folio: z.string().min(1, { message: 'folioRequired' }),
      businessType: z.string().optional(),
      privacyAccepted: z.coerce
        .boolean()
        .refine(val => val === true, { message: 'privacyRequired' }),
    })
  );

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors,
    };
  }

  const { folio, businessType, privacyAccepted } = result.data;

  try {
    // Validate folio exists (equivalent to legacy existeFolio)
    const folioValidationResult = await validateFolio(authToken, folio);

    if (!folioValidationResult || folioValidationResult.length === 0) {
      return {
        success: false,
        errors: { folio: ['folioNotFound'] },
      };
    }

    // Get the first validation result and ensure it has the expected structure
    const validationData = folioValidationResult[0] as FolioValidationResult;

    // Create procedure (equivalent to legacy actualizarUsuario)
    const procedureData = await createProcedure(authToken, {
      folio: folio,
      requirements_query_id: validationData.id,
      status: 1,
      current_step: 1,
      businessType: businessType ? parseInt(businessType) : undefined, // Pass selected business type
    });

    // Success - redirect to the new procedure detail
    const encodedFolio = btoa(folio);
    return redirect(`/procedures/${encodedFolio}/detail`);
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : String(error);

    // Handle specific API errors
    if (errorMessage.includes('DUPLICATE_PROCEDURE')) {
      // If procedure already exists, redirect to the existing procedure
      const encodedFolio = btoa(folio);
      return redirect(`/procedures/${encodedFolio}/detail`);
    } else if (
      errorMessage.includes('folio does not exist or is no longer valid')
    ) {
      return {
        success: false,
        errors: { folio: ['folioInvalid'] },
      };
    } else if (errorMessage.includes('municipality is not available')) {
      return {
        success: false,
        errors: { folio: ['municipalityNotAvailable'] },
      };
    } else {
      return {
        success: false,
        errors: { general: ['error'] },
      };
    }
  }
}

export default function NewProcedure() {
  const { t } = useTranslation('procedures');
  const navigation = useNavigation();
  const actionData = useActionData<typeof action>();
  const { businessTypes } = useLoaderData<typeof loader>();

  const [privacyAccepted, setPrivacyAccepted] = useState(false);
  const [selectedBusinessType, setSelectedBusinessType] = useState<string>('');

  const [searchParams] = useSearchParams();

  // Check if form is submitting
  const isSubmitting = navigation.state === 'submitting';

  // Get form errors
  const errors = actionData?.errors || {};

  // Convert business types to select options
  const businessTypeOptions = businessTypes.map(
    (bt: z.infer<typeof businessTypeSchema>) => ({
      value: bt.business_type_id.toString(),
      label: `${bt.name} (${bt.code ?? 'N/A'})`,
      description: bt.description,
    })
  );

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <Accordion
        type="single"
        defaultValue="folio-form"
        className="bg-white rounded-lg shadow-sm"
      >
        <AccordionItem value="folio-form" disabled>
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <div className="flex items-center gap-3">
              <FileText size={20} className="text-primary" />
              <span className="text-lg font-medium">{t('new.form.title')}</span>
            </div>
          </AccordionTrigger>

          <AccordionContent className="px-6 pb-6">
            <div className="space-y-6">
              <p className="text-gray-600 mb-6">{t('new.form.description')}</p>

              <Form method="post" className="space-y-6">
                {/* General Error */}
                {'general' in errors && errors.general && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-600 text-sm">
                      {t(`new.messages.${errors.general[0]}`)}
                    </p>
                  </div>
                )}

                {/* Folio Input */}
                <div className="flex justify-center">
                  <div className="w-full max-w-md">
                    <Input
                      type="text"
                      name="folio"
                      defaultValue={searchParams.get('folio') ?? ''}
                      label={t('new.form.folioLabel')}
                      placeholder={t('new.form.folioPlaceholder')}
                      disabled={isSubmitting}
                      error={
                        'folio' in errors && errors.folio
                          ? t(`new.messages.${errors.folio[0]}`)
                          : undefined
                      }
                      post={<FileText className="text-gray-400" size={16} />}
                    />
                    <p className="text-xs text-gray-500 mt-1 text-center">
                      {t('new.form.folioHelp')}
                    </p>
                  </div>
                </div>

                {/* Privacy Checkbox */}
                <div className="flex justify-center">
                  <div className="flex items-center gap-2">
                    <Checkbox
                      name="privacyAccepted"
                      value="true"
                      checked={privacyAccepted}
                      onCheckedChange={checked =>
                        setPrivacyAccepted(checked === true)
                      }
                      disabled={isSubmitting}
                      label={
                        <span className="text-sm text-gray-700">
                          {t('new.form.privacyLabel')}
                          <PrivacyModal>
                            <button
                              type="button"
                              className="text-primary hover:underline ml-1"
                            >
                              {t('new.form.privacyLink')}
                            </button>
                          </PrivacyModal>
                        </span>
                      }
                    />
                  </div>
                </div>
                {'privacyAccepted' in errors && errors.privacyAccepted && (
                  <p className="text-red-600 text-xs text-center">
                    {t(`new.validation.${errors.privacyAccepted[0]}`)}
                  </p>
                )}

                {/* Submit Button */}
                <div className="flex justify-center pt-4">
                  <Button
                    type="submit"
                    disabled={isSubmitting}
                    className="min-w-[200px]"
                  >
                    {isSubmitting
                      ? t('new.messages.submitting')
                      : t('new.form.submitButton')}
                  </Button>
                </div>
              </Form>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}
