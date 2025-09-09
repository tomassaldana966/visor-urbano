import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from '../Button/Button';
import { Upload, FileText, X, Clock, Award } from 'lucide-react';
import {
  issueLicenseScanned,
  generateLicense,
} from '../../utils/api/api.client';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '../Dialog/Dialog';
import { useSignatures } from '../../hooks/useSignatures';

interface IssueLicenseModalProps {
  isOpen: boolean;
  onClose: () => void;
  folio: string;
  authToken?: string;
  municipalityId?: number;
  onLicenseIssued?: () => void;
}

export function IssueLicenseModal({
  isOpen,
  onClose,
  folio,
  authToken,
  municipalityId,
  onLicenseIssued,
}: IssueLicenseModalProps) {
  const { t } = useTranslation('procedureApprovals');

  // Load signatures dynamically
  const { signatures, isLoading: signaturesLoading } =
    useSignatures(municipalityId);

  const [selectedOption, setSelectedOption] = useState<
    'generate' | 'upload' | null
  >('generate'); // Auto-select "Generar por Visor Urbano"
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [formData, setFormData] = useState<{
    opening_time: string;
    closing_time: string;
    authorized_area: string;
    license_cost: string;
    observations: string;
    signature_ids: number[]; // Array for multiple signature selection
  }>({
    opening_time: '',
    closing_time: '',
    authorized_area: '',
    license_cost: '',
    observations: '',
    signature_ids: [], // Array for multiple signature selection
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);
  const [showErrorDialog, setShowErrorDialog] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  if (!isOpen) return null;

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
    }
  };

  const handleSubmitScanned = async () => {
    if (!uploadedFile || !authToken) return;

    setIsSubmitting(true);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('file', uploadedFile);
      formDataToSend.append('opening_time', formData.opening_time);
      formDataToSend.append('closing_time', formData.closing_time);
      formDataToSend.append('authorized_area', formData.authorized_area);
      formDataToSend.append('license_cost', formData.license_cost);
      formDataToSend.append('observations', formData.observations);

      // Add signatures as JSON string if any are selected
      if (formData.signature_ids.length > 0) {
        formDataToSend.append(
          'signatures',
          JSON.stringify({
            signature_ids: formData.signature_ids,
          })
        );
      }

      // Encode folio to base64
      const encodedFolio = btoa(folio);

      await issueLicenseScanned(encodedFolio, formDataToSend, authToken);

      onLicenseIssued?.();
      onClose();
      // Show success message
      setShowSuccessDialog(true);
    } catch (error) {
      console.error('Error issuing license:', error);
      setErrorMessage(
        error instanceof Error ? error.message : t('license.issueError')
      );
      setShowErrorDialog(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGenerateBySystem = async () => {
    if (!authToken) return;

    setIsSubmitting(true);

    try {
      const encodedFolio = btoa(folio);

      // Prepare license data to send to backend
      const licenseData = {
        opening_time: formData.opening_time,
        closing_time: formData.closing_time,
        authorized_area: formData.authorized_area,
        license_cost: formData.license_cost,
        observations: formData.observations,
        signature_ids:
          formData.signature_ids.length > 0
            ? formData.signature_ids
            : undefined,
      };

      await generateLicense(encodedFolio, authToken, licenseData);

      onLicenseIssued?.();
      onClose();
      setShowSuccessDialog(true);
    } catch (error) {
      console.error('Error generating license:', error);
      setErrorMessage(
        error instanceof Error
          ? error.message
          : t('license.systemGenerationError')
      );
      setShowErrorDialog(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="bg-green-500 text-white p-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold">{t('license.modal.title')}</h2>
          <button onClick={onClose} className="text-white hover:text-gray-200">
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="p-6">
          <p className="text-gray-600 mb-4">{t('license.modal.subtitle')}</p>
          <p className="text-gray-600 mb-6">{t('license.modal.description')}</p>

          {/* Option Selection */}
          <div className="flex border-b mb-6">
            <button
              onClick={() => setSelectedOption('generate')}
              className={`px-4 py-2 text-sm font-medium border-b-2 ${
                selectedOption === 'generate'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {t('license.modal.generateBySystem')}
            </button>
            <button
              onClick={() => setSelectedOption('upload')}
              className={`px-4 py-2 text-sm font-medium border-b-2 ${
                selectedOption === 'upload'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {t('license.modal.uploadScanned')}
            </button>
          </div>

          {/* Generate by System Option */}
          {selectedOption === 'generate' && (
            <div className="space-y-6">
              <div className="text-center py-4">
                <Award className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-600">
                  {t('license.modal.generateDescription')}
                </p>
              </div>

              {/* Business Details Form */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.openingTime')}
                  </label>
                  <input
                    type="time"
                    value={formData.opening_time}
                    onChange={e =>
                      setFormData({ ...formData, opening_time: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.closingTime')}
                  </label>
                  <input
                    type="time"
                    value={formData.closing_time}
                    onChange={e =>
                      setFormData({ ...formData, closing_time: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('license.modal.authorizedArea')}
                  <span className="text-gray-500 ml-1">
                    {t('license.modal.areaUnit')}
                  </span>
                </label>
                <input
                  type="text"
                  value={formData.authorized_area}
                  onChange={e =>
                    setFormData({
                      ...formData,
                      authorized_area: e.target.value,
                    })
                  }
                  placeholder={t('license.modal.areaPlaceholder')}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.licenseCost')}
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-2 text-gray-500">
                      MXN
                    </span>
                    <input
                      type="text"
                      value={formData.license_cost}
                      onChange={e =>
                        setFormData({
                          ...formData,
                          license_cost: e.target.value,
                        })
                      }
                      className="w-full pl-12 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="0.00"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.signatures')}
                    {formData.signature_ids.length > 0 && (
                      <span className="ml-2 text-sm text-green-600">
                        ({formData.signature_ids.length} seleccionada
                        {formData.signature_ids.length !== 1 ? 's' : ''})
                      </span>
                    )}
                  </label>
                  <div className="border border-gray-300 rounded-md p-3 max-h-48 overflow-y-auto">
                    {signaturesLoading ? (
                      <p className="text-sm text-gray-500">
                        {t('common:loading')}
                      </p>
                    ) : signatures.length === 0 ? (
                      <p className="text-sm text-gray-500">
                        {t('license.modal.noSignaturesAvailable')}
                      </p>
                    ) : (
                      <div className="space-y-2">
                        {signatures.map(signature => (
                          <label
                            key={signature.id}
                            className="flex items-center space-x-2 cursor-pointer"
                          >
                            <input
                              type="checkbox"
                              checked={formData.signature_ids.includes(
                                signature.id
                              )}
                              onChange={e => {
                                const isChecked = e.target.checked;
                                const signatureId = signature.id;
                                setFormData({
                                  ...formData,
                                  signature_ids: isChecked
                                    ? [...formData.signature_ids, signatureId]
                                    : formData.signature_ids.filter(
                                        id => id !== signatureId
                                      ),
                                });
                              }}
                              className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                            />
                            <span className="text-sm">
                              {signature.signer_name} -{' '}
                              {signature.position_title}
                            </span>
                          </label>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('license.modal.observations')}
                </label>
                <textarea
                  value={formData.observations}
                  onChange={e =>
                    setFormData({ ...formData, observations: e.target.value })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder={t('license.modal.observationsPlaceholder')}
                />
              </div>

              <div className="flex justify-end space-x-2">
                <Button variant="secondary" onClick={onClose}>
                  {t('license.modal.cancel')}
                </Button>
                <Button
                  variant="primary"
                  onClick={handleGenerateBySystem}
                  disabled={
                    !formData.opening_time ||
                    !formData.closing_time ||
                    !formData.authorized_area ||
                    isSubmitting
                  }
                >
                  {isSubmitting ? (
                    <>
                      <Clock className="h-4 w-4 mr-2 animate-spin" />
                      {t('license.modal.generating')}
                    </>
                  ) : (
                    t('license.modal.generateLicense')
                  )}
                </Button>
              </div>
            </div>
          )}

          {/* Upload Scanned Option */}
          {selectedOption === 'upload' && (
            <div className="space-y-6">
              {/* File Upload Section */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('license.modal.fileUploadLabel')}
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                  <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <div className="text-sm text-gray-600 mb-4">
                    {uploadedFile
                      ? uploadedFile.name
                      : t('license.modal.noFileChosen')}
                  </div>
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="license-upload"
                  />
                  <label
                    htmlFor="license-upload"
                    className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 cursor-pointer"
                  >
                    {t('license.modal.chooseFile')}
                  </label>
                </div>
              </div>

              {/* Business Details Form - Same as generate option */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.openingTime')}
                  </label>
                  <input
                    type="time"
                    value={formData.opening_time}
                    onChange={e =>
                      setFormData({ ...formData, opening_time: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.closingTime')}
                  </label>
                  <input
                    type="time"
                    value={formData.closing_time}
                    onChange={e =>
                      setFormData({ ...formData, closing_time: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('license.modal.authorizedArea')}
                  <span className="text-gray-500 ml-1">
                    {t('license.modal.areaUnit')}
                  </span>
                </label>
                <input
                  type="text"
                  value={formData.authorized_area}
                  onChange={e =>
                    setFormData({
                      ...formData,
                      authorized_area: e.target.value,
                    })
                  }
                  placeholder={t('license.modal.areaPlaceholder')}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.licenseCost')}
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-2 text-gray-500">
                      MXN
                    </span>
                    <input
                      type="text"
                      value={formData.license_cost}
                      onChange={e =>
                        setFormData({
                          ...formData,
                          license_cost: e.target.value,
                        })
                      }
                      className="w-full pl-12 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="0.00"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('license.modal.signatures')}
                    {formData.signature_ids.length > 0 && (
                      <span className="ml-2 text-sm text-green-600">
                        ({formData.signature_ids.length} seleccionada
                        {formData.signature_ids.length !== 1 ? 's' : ''})
                      </span>
                    )}
                  </label>
                  <div className="border border-gray-300 rounded-md p-3 max-h-48 overflow-y-auto">
                    {signaturesLoading ? (
                      <p className="text-sm text-gray-500">
                        {t('common:loading')}
                      </p>
                    ) : signatures.length === 0 ? (
                      <p className="text-sm text-gray-500">
                        {t('license.modal.noSignaturesAvailable')}
                      </p>
                    ) : (
                      <div className="space-y-2">
                        {signatures.map(signature => (
                          <label
                            key={signature.id}
                            className="flex items-center space-x-2 cursor-pointer"
                          >
                            <input
                              type="checkbox"
                              checked={formData.signature_ids.includes(
                                signature.id
                              )}
                              onChange={e => {
                                const isChecked = e.target.checked;
                                const signatureId = signature.id;
                                setFormData({
                                  ...formData,
                                  signature_ids: isChecked
                                    ? [...formData.signature_ids, signatureId]
                                    : formData.signature_ids.filter(
                                        id => id !== signatureId
                                      ),
                                });
                              }}
                              className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                            />
                            <span className="text-sm">
                              {signature.signer_name} -{' '}
                              {signature.position_title}
                            </span>
                          </label>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('license.modal.observations')}
                </label>
                <textarea
                  value={formData.observations}
                  onChange={e =>
                    setFormData({ ...formData, observations: e.target.value })
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder={t('license.modal.observationsPlaceholder')}
                />
              </div>

              <div className="flex justify-end space-x-2">
                <Button variant="secondary" onClick={onClose}>
                  {t('license.modal.cancel')}
                </Button>
                <Button
                  variant="primary"
                  onClick={handleSubmitScanned}
                  disabled={
                    !uploadedFile ||
                    !formData.opening_time ||
                    !formData.closing_time ||
                    !formData.authorized_area ||
                    isSubmitting
                  }
                >
                  {isSubmitting ? (
                    <>
                      <Clock className="h-4 w-4 mr-2 animate-spin" />
                      {t('license.modal.uploading')}
                    </>
                  ) : (
                    t('license.modal.issueLicense')
                  )}
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Success Dialog */}
      <Dialog open={showSuccessDialog} onOpenChange={setShowSuccessDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('license.modal.successTitle')}</DialogTitle>
            <DialogDescription>
              {t('license.modal.successDescription')}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button onClick={() => setShowSuccessDialog(false)}>
              {t('license.modal.accept')}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Error Dialog */}
      <Dialog open={showErrorDialog} onOpenChange={setShowErrorDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('license.modal.errorTitle')}</DialogTitle>
            <DialogDescription>{errorMessage}</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button onClick={() => setShowErrorDialog(false)}>
              {t('license.modal.accept')}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
