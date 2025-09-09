import { useState } from 'react';
import { Upload, Save, Loader2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Dialog } from './Dialog/Dialog';
import type { MunicipalitySignature } from '@root/app/schemas/municipality-signatures';

interface SignatureModalProps {
  isOpen: boolean;
  onClose: () => void;
  signature: MunicipalitySignature | null;
  onSave: (
    signatureData: {
      signer_name: string;
      position_title: string;
      order_index: number;
    },
    imageFile?: File
  ) => Promise<void>;
  isLoading?: boolean;
}

export default function SignatureModal({
  isOpen,
  onClose,
  signature,
  onSave,
  isLoading = false,
}: SignatureModalProps) {
  const { t } = useTranslation('director');
  const [formData, setFormData] = useState({
    signer_name: signature?.signer_name || '',
    position_title: signature?.position_title || '',
    order_index: signature?.order_index || 1,
  });
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(
    signature?.signature_image || null
  );

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onload = e => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async () => {
    try {
      await onSave(formData, imageFile || undefined);
      onClose();
    } catch (error) {
      console.error('Error saving signature:', error);
    }
  };

  const isValid =
    formData.signer_name.trim() &&
    formData.position_title.trim() &&
    formData.order_index > 0;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <div className="space-y-6">
        <h2 className="text-xl font-semibold mb-4">
          {signature
            ? t('settings.signatures.modal.editTitle')
            : t('settings.signatures.modal.addTitle')}
        </h2>
        {/* Form Fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Signer Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('settings.signatures.modal.signerName')} *
            </label>
            <input
              type="text"
              value={formData.signer_name}
              onChange={e => handleInputChange('signer_name', e.target.value)}
              placeholder={t('settings.signatures.modal.signerNamePlaceholder')}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          {/* Position Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('settings.signatures.modal.position')} *
            </label>
            <input
              type="text"
              value={formData.position_title}
              onChange={e =>
                handleInputChange('position_title', e.target.value)
              }
              placeholder={t('settings.signatures.modal.positionPlaceholder')}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          {/* Order Index */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('settings.signatures.modal.orderIndex')} *
            </label>
            <input
              type="number"
              value={formData.order_index}
              onChange={e =>
                handleInputChange('order_index', parseInt(e.target.value) || 1)
              }
              placeholder="1"
              min="1"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              {t('settings.signatures.modal.orderIndexDescription')}
            </p>
          </div>
        </div>

        {/* Image Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('settings.signatures.modal.signatureImage')}
          </label>

          {imagePreview ? (
            <div className="space-y-3">
              <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <img
                  src={imagePreview}
                  alt={t('settings.signatures.modal.signaturePreview')}
                  className="h-20 w-auto mx-auto"
                />
              </div>
              <div className="flex justify-center">
                <label className="cursor-pointer text-sm text-blue-600 hover:text-blue-700">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                  {t('settings.signatures.modal.changeImage')}
                </label>
              </div>
            </div>
          ) : (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
              <div className="text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <div className="mt-2">
                  <label className="cursor-pointer text-sm text-blue-600 hover:text-blue-700">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageChange}
                      className="hidden"
                    />
                    {t('settings.signatures.modal.uploadImage')}
                  </label>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {t('settings.signatures.modal.imageFormat')}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {t('settings.signatures.modal.cancel')}
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={!isValid || isLoading}
            className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>{t('settings.signatures.modal.saving')}</span>
              </>
            ) : (
              <>
                <Save className="h-4 w-4" />
                <span>
                  {signature
                    ? t('settings.signatures.modal.update')
                    : t('settings.signatures.modal.save')}
                </span>
              </>
            )}
          </button>
        </div>
      </div>
    </Dialog>
  );
}
