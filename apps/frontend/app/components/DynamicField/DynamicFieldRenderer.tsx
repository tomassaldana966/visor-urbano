import { useTranslation } from 'react-i18next';
import { Input } from '@/components/Input/Input';
import { Select, Option } from '@/components/Select/Select';
import { Checkbox } from '@/components/Checkbox/Checkbox';
import { Button } from '@/components/Button/Button';
import {
  type DynamicField,
  getFieldValidation,
  parseFieldOptions,
  isFieldVisible,
} from '@/schemas/dynamicFields';
import { Upload, X, ExternalLink, FileText } from 'lucide-react';
import { useState } from 'react';
import { getFileViewUrl, parseFileValue } from '@/utils/fileDownload';
import { uploadProcedureFile } from '@/utils/api/api.client';

interface DynamicFieldRendererProps {
  field: DynamicField;
  value: unknown;
  onChange: (value: unknown) => void;
  formValues: Record<string, unknown>;
  disabled?: boolean;
  procedureId?: number; // Add procedure ID for file downloads
  authToken?: string; // Add auth token for file uploads
  folio?: string; // Add folio for file uploads
}

export function DynamicFieldRenderer({
  field,
  value,
  onChange,
  formValues,
  disabled = false,
  procedureId,
  authToken,
  folio,
}: DynamicFieldRendererProps) {
  const { t } = useTranslation('procedures');
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [isUploading, setIsUploading] = useState(false);

  // Check if field should be visible based on conditions
  if (!isFieldVisible(field, formValues)) {
    return null;
  }

  const validation = getFieldValidation(field);
  const isRequired = field.required || validation.required;

  const handleFileUpload = async (file: File) => {
    if (!file) return;

    // Validate file size (15MB max)
    const maxSize = 15 * 1024 * 1024;
    if (file.size > maxSize) {
      alert(t('edit.validation.fileTooLarge'));
      return;
    }

    // Check if we have the required params for file upload
    if (!authToken || !folio || !field.name) {
      alert(t('edit.messages.error'));
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 100);

      // Upload file to backend
      const uploadResult = await uploadProcedureFile(
        authToken,
        folio,
        field.name,
        file
      );

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (uploadResult.success) {
        // Store the file metadata using local file info and server file path
        onChange({
          filename: file.name,
          original_name: file.name,
          file_path: uploadResult.file_path,
          size: file.size,
          content_type: file.type,
        });
      } else {
        throw new Error(uploadResult.error || 'Upload failed');
      }

      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 500);
    } catch (error) {
      setIsUploading(false);
      setUploadProgress(0);
      console.error('File upload error:', error);
      alert(t('edit.messages.error'));
    }
  };

  const renderField = () => {
    switch (field.field_type) {
      case 'input':
      case 'textarea':
        return (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {field.description}
              {isRequired && <span className="text-red-500 ml-1">*</span>}
            </label>
            {field.field_type === 'textarea' ? (
              <textarea
                value={typeof value === 'string' ? value : ''}
                onChange={e => onChange(e.target.value)}
                disabled={disabled}
                required={isRequired}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:cursor-not-allowed"
                rows={4}
                placeholder={field.description ?? undefined}
                minLength={validation.minLength}
                maxLength={validation.maxLength}
              />
            ) : (
              <Input
                type="text"
                value={typeof value === 'string' ? value : ''}
                onChange={e => onChange(e.target.value)}
                disabled={disabled}
                required={isRequired}
                placeholder={field.description ?? undefined}
                pattern={validation.pattern?.source}
                minLength={validation.minLength}
                maxLength={validation.maxLength}
              />
            )}
            {field.description_rec && (
              <p className="text-xs text-gray-500">{field.description_rec}</p>
            )}
          </div>
        );

      case 'select': {
        const selectOptions = parseFieldOptions(field);
        return (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {field.description}
              {isRequired && <span className="text-red-500 ml-1">*</span>}
            </label>
            <Select
              value={typeof value === 'string' ? value : ''}
              onValueChange={onChange}
              disabled={disabled}
              required={isRequired}
              placeholder={t('edit.form.chooseFile')}
            >
              {selectOptions.map(option => (
                <Option key={option.value} value={option.value}>
                  {option.label}
                </Option>
              ))}
            </Select>
            {field.description_rec && (
              <p className="text-xs text-gray-500">{field.description_rec}</p>
            )}
          </div>
        );
      }

      case 'radio': {
        const radioOptions = parseFieldOptions(field);
        return (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {field.description}
              {isRequired && <span className="text-red-500 ml-1">*</span>}
            </label>
            <div className="space-y-2">
              {radioOptions.map(option => (
                <label
                  key={option.value}
                  className="flex items-center space-x-2"
                >
                  <input
                    type="radio"
                    name={field.name}
                    value={option.value}
                    checked={value === option.value}
                    onChange={e => onChange(e.target.value)}
                    disabled={disabled}
                    required={isRequired}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                  />
                  <span className="text-sm text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
            {field.description_rec && (
              <p className="text-xs text-gray-500">{field.description_rec}</p>
            )}
          </div>
        );
      }

      case 'file':
      case 'multifile':
        return (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {field.description}
              {isRequired && <span className="text-red-500 ml-1">*</span>}
            </label>

            {/* Current file display */}
            {value &&
            (typeof value === 'object' || typeof value === 'string') ? (
              <div className="p-3 bg-gray-50 border border-gray-200 rounded-md">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {(() => {
                      // Parse the file value
                      const fileInfo = parseFileValue(value);

                      if (!fileInfo) {
                        return (
                          <>
                            <Upload className="h-4 w-4 text-gray-500" />
                            <span className="text-sm text-gray-700">
                              Unknown file
                            </span>
                          </>
                        );
                      }

                      const { filename, originalName, contentType } = fileInfo;
                      const displayName = originalName || filename;
                      const isPdf =
                        contentType?.includes('pdf') ||
                        displayName.toLowerCase().includes('.pdf');
                      const FileIcon = isPdf ? FileText : Upload;

                      // Generate download URL if we have procedure ID and field name
                      const downloadUrl =
                        procedureId && field.name
                          ? getFileViewUrl(procedureId, field.name)
                          : null;

                      return (
                        <>
                          <FileIcon className="h-4 w-4 text-gray-500" />
                          {downloadUrl ? (
                            <a
                              href={downloadUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-blue-600 hover:text-blue-800 hover:underline cursor-pointer flex items-center gap-1"
                              onClick={e => {
                                e.stopPropagation();
                              }}
                            >
                              {displayName}
                              <ExternalLink className="h-3 w-3" />
                            </a>
                          ) : (
                            <span className="text-sm text-gray-700">
                              {displayName}
                            </span>
                          )}
                        </>
                      );
                    })()}
                  </div>
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    onClick={() => onChange(null)}
                    disabled={disabled}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ) : null}

            {/* Upload progress */}
            {isUploading && (
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            )}

            {/* File input */}
            <div className="flex items-center space-x-2">
              <input
                type="file"
                id={`file-${field.id}`}
                onChange={e => {
                  const file = e.target.files?.[0];
                  if (file) {
                    handleFileUpload(file);
                  }
                }}
                disabled={disabled || isUploading}
                required={isRequired && !value}
                className="hidden"
                accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
              />
              <label
                htmlFor={`file-${field.id}`}
                className="cursor-pointer inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-50 disabled:cursor-not-allowed"
              >
                <Upload className="h-4 w-4 mr-2" />
                {value ? t('edit.form.chooseFile') : t('edit.form.uploadFile')}
              </label>
              <span className="text-xs text-gray-500">
                {t('edit.form.maxFileSize')}
              </span>
            </div>

            {field.description_rec && (
              <p className="text-xs text-gray-500">{field.description_rec}</p>
            )}
          </div>
        );

      default:
        return (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {field.description}
              {isRequired && <span className="text-red-500 ml-1">*</span>}
            </label>
            <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-sm text-yellow-800">
                Unsupported field type: {field.field_type}
              </p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="relative">
      {renderField()}
      {field.rationale && (
        <div className="mt-1">
          <button
            type="button"
            className="text-xs text-blue-600 hover:text-blue-800"
            onClick={() => {
              // Could show a modal with legal basis information
              alert(field.rationale);
            }}
          >
            Ver fundamento legal
          </button>
        </div>
      )}
    </div>
  );
}
