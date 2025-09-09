import React, { useState, useEffect, useRef } from 'react';
import {
  Form,
  useActionData,
  useNavigation,
  useRevalidator,
} from 'react-router';
import { Badge } from '../Badge/Badge';
import { Button } from '../Button/Button';
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '../Accordion/Accordion';
import { DynamicFieldRenderer } from '../DynamicField';
import { LoadingModal } from '../LoadingModal';
import { type DynamicField } from '../../schemas/dynamicFields';
import { FileText, CheckCircle, XCircle, Save, Loader } from 'lucide-react';

interface SectionFormProps {
  sectionId: string;
  fields: DynamicField[];
  sectionTitle: string;
  sectionIcon?: any;
  sectionDescription?: string;
  folio: string;
  isExpanded: boolean;
  onToggle: () => void;
  t: any;
  procedureId?: number; // Add procedure ID for file downloads
  authToken?: string; // Add auth token for file uploads
}

export function SectionForm({
  sectionId,
  fields,
  sectionTitle,
  sectionIcon,
  sectionDescription,
  folio,
  isExpanded,
  onToggle,
  t,
  procedureId,
  authToken,
}: SectionFormProps) {
  const [formData, setFormData] = useState<Record<string, unknown>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoadingModalOpen, setIsLoadingModalOpen] = useState(false);
  const navigation = useNavigation();
  const actionData = useActionData<any>();
  const revalidator = useRevalidator();
  const lastProcessedActionData = useRef<any>(null);

  // Initialize form data from field default values
  useEffect(() => {
    const initialData: Record<string, unknown> = {};
    fields.forEach(field => {
      const fieldKey = field.id.toString();
      if (field.value !== undefined && field.value !== null) {
        initialData[fieldKey] = field.value;
      }
    });

    setFormData(initialData);
  }, [fields, sectionId]);

  // Handle loading modal based on navigation state
  useEffect(() => {
    const isSubmitting = navigation.state === 'submitting';
    const isForThisSection = navigation.formData?.get('step') === sectionId;

    if (isSubmitting && isForThisSection) {
      setIsLoadingModalOpen(true);
    } else {
      // Close modal when not submitting or when action completes
      setIsLoadingModalOpen(false);
    }
  }, [navigation.state, navigation.formData, sectionId]);

  // Handle successful save and reload
  useEffect(() => {
    // Avoid processing the same actionData multiple times
    if (actionData && actionData !== lastProcessedActionData.current) {
      if (actionData?.success && actionData?.step === parseInt(sectionId)) {
        // Close the loading modal immediately on success
        setIsLoadingModalOpen(false);

        // Update form data with saved values if provided
        if (actionData.savedData) {
          // For steps 2+, the saved data contains field IDs as keys
          if (parseInt(sectionId) >= 2) {
            setFormData(actionData.savedData);
          } else {
            // For step 1, we might need mapping, but for now just try direct update
            setFormData(prev => ({ ...prev, ...actionData.savedData }));
          }
        }

        // Trigger revalidation after a delay
        if (actionData.reload) {
          setTimeout(() => {
            revalidator.revalidate();
          }, 100);
        }
      }

      // Close modal on error as well
      if (
        actionData?.success === false &&
        actionData?.step === parseInt(sectionId)
      ) {
        setIsLoadingModalOpen(false);
      }

      // Mark this actionData as processed
      lastProcessedActionData.current = actionData;
    }
  }, [actionData, sectionId, revalidator]);

  const handleFieldChange = (fieldId: string, value: unknown) => {
    setFormData(prev => ({ ...prev, [fieldId]: value }));
    // Clear error when user starts typing
    if (errors[fieldId]) {
      setErrors(prev => ({ ...prev, [fieldId]: '' }));
    }
  };

  const validateSection = (): boolean => {
    const newErrors: Record<string, string> = {};

    fields.forEach(field => {
      const fieldKey = field.id.toString();
      if (
        field.required &&
        (!formData[fieldKey] || formData[fieldKey] === '')
      ) {
        newErrors[fieldKey] = t('edit.validation.fieldRequired');
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isLoading = navigation.state === 'submitting' || isLoadingModalOpen;
  const hasSuccess =
    actionData?.success && actionData?.step === parseInt(sectionId);
  const hasError = actionData?.success === false;

  return (
    <AccordionItem value={sectionId}>
      <AccordionTrigger onClick={onToggle} className="text-left">
        <div className="flex items-center justify-between w-full pr-4">
          <div className="flex items-center space-x-3">
            {sectionIcon &&
              React.createElement(sectionIcon, {
                size: 20,
                className: 'text-blue-600',
              })}
            <div className="text-left">
              <span className="font-medium">{sectionTitle}</span>
              {sectionDescription && (
                <p className="text-sm text-gray-500 mt-1">
                  {sectionDescription}
                </p>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {hasSuccess && (
              <Badge variant="success">
                <CheckCircle size={12} className="mr-1" />
                {t('edit.status.saved')}
              </Badge>
            )}
            {hasError && (
              <Badge variant="destructive">
                <XCircle size={12} className="mr-1" />
                {t('edit.status.error')}
              </Badge>
            )}
            {fields.length > 0 && (
              <Badge variant="outline">
                {fields.length} {t('edit.form.fieldsCount')}
              </Badge>
            )}
          </div>
        </div>
      </AccordionTrigger>
      <AccordionContent>
        {fields.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <FileText size={48} className="mx-auto mb-4 opacity-50" />
            <p>{t('edit.form.noFieldsInSection')}</p>
          </div>
        ) : (
          <Form method="post" className="space-y-6">
            <input type="hidden" name="_action" value="save" />
            <input type="hidden" name="step" value={sectionId} />
            <input
              type="hidden"
              name="sectionData"
              value={JSON.stringify(formData)}
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {fields.map(field => {
                const fieldKey = field.id.toString();
                return (
                  <div key={field.id} className="space-y-2">
                    <DynamicFieldRenderer
                      field={field}
                      value={formData[fieldKey]}
                      onChange={value => handleFieldChange(fieldKey, value)}
                      formValues={formData}
                      procedureId={procedureId}
                      authToken={authToken}
                      folio={folio}
                    />
                    {errors[fieldKey] && (
                      <p className="text-sm text-red-600">{errors[fieldKey]}</p>
                    )}
                  </div>
                );
              })}
            </div>

            {hasError && actionData?.error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex items-center">
                  <XCircle className="h-5 w-5 text-red-400 mr-2" />
                  <p className="text-sm text-red-800">{actionData.error}</p>
                </div>
              </div>
            )}

            <div className="flex justify-end pt-4 border-t">
              <Button
                type="submit"
                disabled={isLoading}
                onClick={e => {
                  if (!validateSection()) {
                    e.preventDefault();
                  }
                }}
              >
                {isLoading ? (
                  <>
                    <Loader size={16} className="mr-2 animate-spin" />
                    {t('edit.messages.saving')}
                  </>
                ) : (
                  <>
                    <Save size={16} className="mr-2" />
                    {t('edit.actions.saveSection')}
                  </>
                )}
              </Button>
            </div>
          </Form>
        )}

        {/* Loading Modal */}
        <LoadingModal
          isOpen={isLoadingModalOpen}
          message={`Guardando ${sectionTitle.toLowerCase()}...`}
        />
      </AccordionContent>
    </AccordionItem>
  );
}
