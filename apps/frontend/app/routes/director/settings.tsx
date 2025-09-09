import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useLoaderData, type LoaderFunctionArgs } from 'react-router';
import {
  Save,
  Building,
  CheckCircle,
  AlertTriangle,
  Loader2,
  Upload,
  Palette,
  Users,
  Plus,
  Trash2,
  Edit,
} from 'lucide-react';
import {
  getMunicipality,
  updateMunicipality,
  createMunicipalitySignature,
  updateMunicipalitySignature,
  deleteMunicipalitySignature,
  uploadMunicipalityImage,
  uploadSignatureImage,
} from '@root/app/utils/api/municipalities';
import type {
  MunicipalitySettingsUpdate,
  Municipality,
} from '@root/app/schemas/municipalities';
import type { MunicipalitySignature } from '@root/app/schemas/municipality-signatures';
import {
  requireAuth,
  requireAccessToken,
} from '@root/app/utils/auth/auth.server';
import SignatureModal from '@root/app/components/SignatureModal';
import { useSignatures } from '@root/app/hooks/useSignatures';

export const handle = {
  title: 'director:navigation.settings',
  breadcrumb: 'director:navigation.settings',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  const accessToken = await requireAccessToken(request);

  return {
    user,
    accessToken,
  };
}

export default function DirectorSettings() {
  const { t } = useTranslation('director');
  const { user, accessToken } = useLoaderData<typeof loader>();

  // Load signatures dynamically
  const {
    signatures,
    isLoading: signaturesLoading,
    refetch: refetchSignatures,
  } = useSignatures(user?.municipality_id);

  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [municipality, setMunicipality] = useState<Municipality | null>(null);

  // Signature modal state
  const [isSignatureModalOpen, setIsSignatureModalOpen] = useState(false);
  const [editingSignature, setEditingSignature] =
    useState<MunicipalitySignature | null>(null);
  const [isSignatureLoading, setIsSignatureLoading] = useState(false);

  // Logo upload state
  const [isLogoUploading, setIsLogoUploading] = useState(false);

  // Municipality settings state
  const [settings, setSettings] = useState<MunicipalitySettingsUpdate>({
    name: '',
    director: '',
    address: '',
    phone: '',
    email: '',
    website: '',
    responsible_area: '',
    solving_days: undefined,
    initial_folio: undefined,
    low_impact_license_cost: '',
    license_additional_text: '',
    allow_online_procedures: false,
    allow_window_reviewer_licenses: false,
    theme_color: '',
  });

  // Load municipality settings
  const fetchMunicipalitySettings = async () => {
    if (!user?.municipality_id) {
      setErrorMessage(t('settings.errors.municipalityInfoNotFound'));
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      const municipality = await getMunicipality(
        user.municipality_id,
        accessToken
      );

      // Fix image URL if it exists
      if (municipality.image && !municipality.image.startsWith('http')) {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        municipality.image = `${apiUrl}/${municipality.image}`;
      }

      // Note: Signature URLs are now processed in the useSignatures hook

      setMunicipality(municipality);

      setSettings({
        name: municipality.name || '',
        director: municipality.director || '',
        address: municipality.address || '',
        phone: municipality.phone || '',
        email: municipality.email || '',
        website: municipality.website || '',
        responsible_area: municipality.responsible_area || '',
        solving_days: municipality.solving_days || undefined,
        initial_folio: municipality.initial_folio || undefined,
        low_impact_license_cost: municipality.low_impact_license_cost || '',
        license_additional_text: municipality.license_additional_text || '',
        allow_online_procedures: municipality.allow_online_procedures || false,
        allow_window_reviewer_licenses:
          municipality.allow_window_reviewer_licenses || false,
        theme_color: municipality.theme_color || '',
      });
    } catch (error) {
      console.error('Error fetching municipality settings:', error);
      setErrorMessage(t('settings.errors.loadSettings'));
      setShowError(true);
    } finally {
      setIsLoading(false);
    }
  };

  // Save municipality settings
  const saveMunicipalitySettings = async () => {
    if (!user?.municipality_id) {
      setErrorMessage(t('settings.errors.municipalityInfoNotFound'));
      setShowError(true);
      return;
    }

    try {
      setIsSaving(true);
      setShowError(false);
      setShowSuccess(false);

      await updateMunicipality(user.municipality_id, settings, accessToken);

      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error('Error saving municipality settings:', error);
      setErrorMessage(
        error instanceof Error
          ? error.message
          : t('settings.errors.saveSettings')
      );
      setShowError(true);
      setTimeout(() => setShowError(false), 5000);
    } finally {
      setIsSaving(false);
    }
  };

  // Signature management functions
  const handleAddSignature = () => {
    // Check if we already have 4 signatures
    if (signatures && signatures.length >= 4) {
      setErrorMessage(t('settings.signatures.maxSignaturesError'));
      setShowError(true);
      setTimeout(() => setShowError(false), 5000);
      return;
    }

    setEditingSignature(null);
    setIsSignatureModalOpen(true);
  };

  const handleEditSignature = (signature: MunicipalitySignature) => {
    setEditingSignature(signature);
    setIsSignatureModalOpen(true);
  };

  const handleDeleteSignature = async (signatureId: number) => {
    if (!user?.municipality_id) {
      setErrorMessage(t('settings.errors.municipalityIdNotFound'));
      setShowError(true);
      return;
    }

    if (!confirm(t('settings.signatures.confirmDelete'))) {
      return;
    }

    try {
      await deleteMunicipalitySignature(
        user.municipality_id,
        signatureId,
        accessToken
      );

      // Refresh signatures data
      await refetchSignatures();

      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error('Error deleting signature:', error);
      let errorMessage = t('settings.signatures.deleteError');

      if (error instanceof Error) {
        if (error.message.includes('Signature not found')) {
          errorMessage = t('settings.signatures.notFoundOrDeleted');
        } else if (error.message.includes('Municipality not found')) {
          errorMessage = t('settings.errors.municipalityNotFound');
        } else if (error.message.includes('User not authorized')) {
          errorMessage = t('settings.signatures.notAuthorizedDelete');
        } else if (error.message.toLowerCase().includes('network')) {
          errorMessage = t('settings.errors.networkError');
        } else {
          errorMessage = t('settings.errors.generic', { error: error.message });
        }
      }

      setErrorMessage(errorMessage);
      setShowError(true);
      setTimeout(() => setShowError(false), 5000);
    }
  };

  const handleSaveSignature = async (
    signatureData: {
      signer_name: string;
      position_title: string;
      order_index: number;
    },
    imageFile?: File
  ) => {
    if (!user?.municipality_id) {
      setErrorMessage(t('settings.errors.municipalityIdNotFound'));
      setShowError(true);
      return;
    }

    try {
      setIsSignatureLoading(true);

      // When creating a new signature, automatically assign the next available order
      if (!editingSignature && signatures) {
        const existingOrders = signatures.map(s => s.order_index);
        for (let i = 1; i <= 4; i++) {
          if (!existingOrders.includes(i)) {
            signatureData.order_index = i;
            break;
          }
        }
      }

      let signature;
      if (editingSignature) {
        // Update existing signature
        signature = await updateMunicipalitySignature(
          user.municipality_id,
          editingSignature.id,
          signatureData,
          accessToken
        );
      } else {
        // Create new signature
        signature = await createMunicipalitySignature(
          user.municipality_id,
          signatureData,
          accessToken
        );
      }

      // Upload image if provided
      if (imageFile && signature?.id) {
        await uploadSignatureImage(
          user.municipality_id,
          signature.id,
          imageFile,
          accessToken
        );
      }

      // Refresh signatures data
      await refetchSignatures();

      setIsSignatureModalOpen(false);
      setEditingSignature(null);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error('Error saving signature:', error);
      let errorMessage = t('settings.signatures.saveError');

      if (error instanceof Error) {
        if (error.message.includes('Failed to upload signature image')) {
          errorMessage = t('settings.signatures.uploadImageError');
        } else if (error.message.includes('Municipality not found')) {
          errorMessage = t('settings.errors.municipalityNotFound');
        } else if (error.message.includes('User not authorized')) {
          errorMessage = t('settings.signatures.notAuthorized');
        } else if (error.message.includes('Signature not found')) {
          errorMessage = t('settings.signatures.notFound');
        } else if (error.message.toLowerCase().includes('network')) {
          errorMessage = t('settings.errors.networkError');
        } else {
          errorMessage = t('settings.errors.generic', { error: error.message });
        }
      }

      setErrorMessage(errorMessage);
      setShowError(true);
      setTimeout(() => setShowError(false), 5000);
    } finally {
      setIsSignatureLoading(false);
    }
  };

  // Logo upload handler
  const handleLogoUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file || !user?.municipality_id) {
      if (!file) {
        setErrorMessage(t('settings.logo.noFileSelected'));
        setShowError(true);
        setTimeout(() => setShowError(false), 5000);
      }
      if (!user?.municipality_id) {
        setErrorMessage(t('settings.errors.municipalityIdNotFound'));
        setShowError(true);
        setTimeout(() => setShowError(false), 5000);
      }
      return;
    }

    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
      setErrorMessage(
        t('settings.logo.invalidFileType', { fileType: file.type })
      );
      setShowError(true);
      setTimeout(() => setShowError(false), 5000);
      return;
    }

    // Validate file size (5MB max)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
      setErrorMessage(t('settings.logo.fileTooLarge', { size: fileSizeMB }));
      setShowError(true);
      setTimeout(() => setShowError(false), 5000);
      return;
    }

    try {
      setIsLogoUploading(true);
      setShowError(false);

      const result = await uploadMunicipalityImage(
        user.municipality_id,
        file,
        accessToken
      );

      // Refresh municipality data to get the new image
      await fetchMunicipalitySettings();

      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error('Error uploading logo:', error);

      // More detailed error handling
      let errorMsg = t('settings.logo.uploadError');
      if (error instanceof Error) {
        if (error.message.includes('Failed to upload image')) {
          errorMsg = t('settings.logo.serverError', { error: error.message });
        } else if (
          error.message.includes('NetworkError') ||
          error.message.includes('fetch')
        ) {
          errorMsg = t('settings.errors.networkError');
        } else {
          errorMsg = t('settings.errors.generic', { error: error.message });
        }
      }

      setErrorMessage(errorMsg);
      setShowError(true);
      setTimeout(() => setShowError(false), 8000);
    } finally {
      setIsLogoUploading(false);
      // Clear the file input to allow re-uploading the same file
      event.target.value = '';
    }
  };

  // Load settings on component mount
  useEffect(() => {
    fetchMunicipalitySettings();
  }, []);

  const handleInputChange = (
    field: keyof MunicipalitySettingsUpdate,
    value: string | number | boolean | undefined
  ) => {
    setSettings(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSave = () => {
    saveMunicipalitySettings();
  };

  if (isLoading || isLogoUploading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex items-center space-x-2">
          <Loader2 className="h-6 w-6 animate-spin" />
          <span>
            {isLogoUploading
              ? t('settings.logo.uploading')
              : t('settings.general.loading')}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-2 mb-6">
        <Building className="h-6 w-6 text-blue-600" />
        <h1 className="text-2xl font-bold text-gray-800">
          {t('settings.title')}
        </h1>
      </div>

      {/* Success Alert */}
      {showSuccess && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center space-x-2">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <p className="text-green-800">{t('settings.messages.saveSuccess')}</p>
        </div>
      )}

      {/* Error Alert */}
      {showError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-2">
          <AlertTriangle className="h-5 w-5 text-red-600" />
          <p className="text-red-800">{errorMessage}</p>
        </div>
      )}

      {/* Settings Card */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-800">
            {t('settings.general.title')}
          </h2>
          <p className="text-gray-600 mt-1">
            {t('settings.general.description')}
          </p>
        </div>

        <div className="space-y-8">
          {/* Basic Information Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              {t('settings.basicInfo.title')}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Municipality Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.basicInfo.municipalityName')} *
                </label>
                <input
                  type="text"
                  value={settings.name}
                  onChange={e => handleInputChange('name', e.target.value)}
                  placeholder={t(
                    'settings.basicInfo.municipalityNamePlaceholder'
                  )}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Director */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.basicInfo.director')} *
                </label>
                <input
                  type="text"
                  value={settings.director}
                  onChange={e => handleInputChange('director', e.target.value)}
                  placeholder={t('settings.basicInfo.directorPlaceholder')}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Phone */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.basicInfo.phone')} *
                </label>
                <input
                  type="tel"
                  value={settings.phone}
                  onChange={e => handleInputChange('phone', e.target.value)}
                  placeholder={t('settings.basicInfo.phonePlaceholder')}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.basicInfo.email')}
                </label>
                <input
                  type="email"
                  value={settings.email}
                  onChange={e => handleInputChange('email', e.target.value)}
                  placeholder={t('settings.basicInfo.emailPlaceholder')}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Website */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.basicInfo.website')}
                </label>
                <input
                  type="url"
                  value={settings.website}
                  onChange={e => handleInputChange('website', e.target.value)}
                  placeholder={t('settings.basicInfo.websitePlaceholder')}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Responsible Area */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.basicInfo.responsibleArea')} *
                </label>
                <input
                  type="text"
                  value={settings.responsible_area}
                  onChange={e =>
                    handleInputChange('responsible_area', e.target.value)
                  }
                  placeholder={t(
                    'settings.basicInfo.responsibleAreaPlaceholder'
                  )}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>

            {/* Address - Full Width */}
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('settings.basicInfo.address')} *
              </label>
              <textarea
                value={settings.address}
                onChange={e => handleInputChange('address', e.target.value)}
                placeholder={t('settings.basicInfo.addressPlaceholder')}
                rows={3}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
          </div>

          {/* License Configuration Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              {t('settings.licenses.title')}
            </h3>

            {/* Authorization Checkboxes */}
            <div className="space-y-4 mb-6">
              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="allow_online_procedures"
                  checked={settings.allow_online_procedures}
                  onChange={e =>
                    handleInputChange(
                      'allow_online_procedures',
                      e.target.checked
                    )
                  }
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="allow_online_procedures"
                  className="text-sm font-medium text-gray-700"
                >
                  {t('settings.licenses.allowOnlineProcedures')}
                </label>
              </div>

              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="allow_window_reviewer_licenses"
                  checked={settings.allow_window_reviewer_licenses}
                  onChange={e =>
                    handleInputChange(
                      'allow_window_reviewer_licenses',
                      e.target.checked
                    )
                  }
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="allow_window_reviewer_licenses"
                  className="text-sm font-medium text-gray-700"
                >
                  {t('settings.licenses.allowWindowReviewerLicenses')}
                </label>
              </div>
            </div>

            {/* License Configuration Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Low Impact License Cost */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.licenses.lowImpactLicenseCost')} *
                </label>
                <input
                  type="text"
                  value={settings.low_impact_license_cost}
                  onChange={e =>
                    handleInputChange('low_impact_license_cost', e.target.value)
                  }
                  placeholder="199"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Solving Days */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.licenses.solvingDays')}
                </label>
                <input
                  type="number"
                  value={settings.solving_days || ''}
                  onChange={e =>
                    handleInputChange(
                      'solving_days',
                      e.target.value ? parseInt(e.target.value) : undefined
                    )
                  }
                  placeholder="14"
                  min="1"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Initial Folio */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.licenses.initialFolio')}
                </label>
                <input
                  type="number"
                  value={settings.initial_folio || ''}
                  onChange={e =>
                    handleInputChange(
                      'initial_folio',
                      e.target.value ? parseInt(e.target.value) : undefined
                    )
                  }
                  placeholder="835"
                  min="1"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Additional License Text */}
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('settings.licenses.additionalText')}
              </label>
              <textarea
                value={settings.license_additional_text}
                onChange={e =>
                  handleInputChange('license_additional_text', e.target.value)
                }
                placeholder={t('settings.licenses.additionalTextPlaceholder')}
                rows={4}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Visual Configuration Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              {t('settings.visual.title')}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Municipality Logo */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.visual.municipalLogo')}
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                  {municipality?.image ? (
                    <div className="flex items-center space-x-4">
                      <img
                        src={municipality.image}
                        alt="Logo municipal"
                        className="h-16 w-16 object-contain rounded-lg border border-gray-200 bg-white"
                      />
                      <div className="flex-1">
                        <p className="text-sm text-gray-600 mb-1">
                          {t('settings.visual.currentLogo')}
                        </p>
                        <p className="text-xs text-gray-500 mb-2">
                          {t('settings.visual.logoDescription')}
                        </p>
                        <input
                          type="file"
                          accept="image/png,image/jpeg,image/jpg"
                          onChange={handleLogoUpload}
                          className="hidden"
                          id="logo-upload-change"
                          disabled={isLogoUploading}
                        />
                        <label
                          htmlFor="logo-upload-change"
                          className={`inline-flex items-center px-3 py-1 text-sm rounded-md border cursor-pointer transition-colors ${
                            isLogoUploading
                              ? 'text-gray-400 bg-gray-100 border-gray-200 cursor-not-allowed'
                              : 'text-blue-600 bg-blue-50 border-blue-200 hover:bg-blue-100 hover:text-blue-700'
                          }`}
                        >
                          {isLogoUploading ? (
                            <>
                              <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                              {t('settings.logo.uploading')}
                            </>
                          ) : (
                            t('settings.visual.changeLogo')
                          )}
                        </label>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center">
                      <Upload className="mx-auto h-12 w-12 text-gray-400 mb-3" />
                      <p className="text-sm text-gray-600 mb-2">
                        {t('settings.visual.uploadLogoDescription')}
                      </p>
                      <input
                        type="file"
                        accept="image/png,image/jpeg,image/jpg"
                        onChange={handleLogoUpload}
                        className="hidden"
                        id="logo-upload-new"
                        disabled={isLogoUploading}
                      />
                      <label
                        htmlFor="logo-upload-new"
                        className={`inline-flex items-center px-4 py-2 text-sm rounded-md border cursor-pointer transition-colors ${
                          isLogoUploading
                            ? 'text-gray-400 bg-gray-100 border-gray-200 cursor-not-allowed'
                            : 'text-blue-600 bg-blue-50 border-blue-200 hover:bg-blue-100 hover:text-blue-700'
                        }`}
                      >
                        {isLogoUploading ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            {t('settings.logo.uploading')}
                          </>
                        ) : (
                          <>
                            <Upload className="h-4 w-4 mr-2" />
                            {t('settings.visual.uploadMunicipalLogo')}
                          </>
                        )}
                      </label>
                      <p className="text-xs text-gray-500 mt-2">
                        {t('settings.visual.supportedFormats')}
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Theme Color */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('settings.visual.themeColor')}
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={settings.theme_color || '#3B82F6'}
                    onChange={e =>
                      handleInputChange('theme_color', e.target.value)
                    }
                    className="h-10 w-20 border border-gray-300 rounded-lg cursor-pointer"
                  />
                  <input
                    type="text"
                    value={settings.theme_color || ''}
                    onChange={e =>
                      handleInputChange('theme_color', e.target.value)
                    }
                    placeholder="#3B82F6"
                    pattern="^#[0-9A-Fa-f]{6}$"
                    className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {t('settings.visual.themeColorDescription')}
                </p>
              </div>
            </div>
          </div>

          {/* Signatures Section */}
          <div>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-800">
                {t('settings.signatures.title')}
              </h3>
              <p className="text-sm text-gray-600">
                {t('settings.signatures.description')}
              </p>
              {signaturesLoading ? (
                <p className="text-xs text-gray-500 mt-1">
                  {t('common:loading')}...
                </p>
              ) : (
                <p className="text-xs text-gray-500 mt-1">
                  {t('settings.signatures.count', {
                    current: signatures.length,
                    max: 4,
                  })}
                </p>
              )}
            </div>

            {signaturesLoading ? (
              <div className="space-y-4">
                {[1, 2, 3].map(i => (
                  <div
                    key={i}
                    className="bg-gray-50 rounded-lg p-4 animate-pulse"
                  >
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : signatures && signatures.length > 0 ? (
              <div className="space-y-4">
                {signatures
                  .sort((a, b) => a.order_index - b.order_index)
                  .map((signature, index) => (
                    <div
                      key={signature.id}
                      className="bg-gray-50 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div>
                            <p className="text-sm font-medium text-gray-700">
                              {t('settings.signatures.name')}
                            </p>
                            <p className="text-sm text-gray-900">
                              {signature.signer_name}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700">
                              {t('settings.signatures.position')}
                            </p>
                            <p className="text-sm text-gray-900">
                              {signature.position_title}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700">
                              {t('settings.signatures.order')}
                            </p>
                            <p className="text-sm text-gray-900">
                              {signature.order_index}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <button
                            type="button"
                            onClick={() => handleEditSignature(signature)}
                            className="text-blue-600 hover:text-blue-700"
                            title="Editar firma"
                          >
                            <Edit className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDeleteSignature(signature.id)}
                            className="text-red-600 hover:text-red-700"
                            title="Eliminar firma"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </div>

                      {signature.signature_image && (
                        <div className="mt-3">
                          <p className="text-sm font-medium text-gray-700 mb-2">
                            Imagen de Firma
                          </p>
                          <img
                            src={signature.signature_image}
                            alt={`Firma de ${signature.signer_name}`}
                            className="h-16 w-auto border border-gray-200 rounded"
                          />
                        </div>
                      )}
                    </div>
                  ))}
              </div>
            ) : (
              <div className="text-center py-8 bg-gray-50 rounded-lg">
                <Users className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600">
                  No hay firmas configuradas
                </p>
                <p className="text-xs text-gray-500">
                  Agregue hasta 4 firmas para que aparezcan en las licencias
                  comerciales
                </p>
              </div>
            )}

            {/* Add Signature Button */}
            <div className="mt-4">
              <button
                type="button"
                onClick={handleAddSignature}
                disabled={signaturesLoading || signatures.length >= 4}
                className="flex items-center space-x-2 w-full justify-center px-4 py-2 border border-dashed border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:text-gray-900 hover:border-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Plus className="h-4 w-4" />
                <span>
                  {signatures.length >= 4
                    ? t('settings.signatures.maxReached')
                    : t('settings.signatures.addNew')}
                </span>
              </button>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end pt-4">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-lg transition-colors min-w-[120px] justify-center"
            >
              {isSaving ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Guardando...</span>
                </>
              ) : (
                <>
                  <Save className="h-4 w-4" />
                  <span>Guardar</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Signature Modal */}
      <SignatureModal
        isOpen={isSignatureModalOpen}
        onClose={() => {
          setIsSignatureModalOpen(false);
          setEditingSignature(null);
        }}
        signature={editingSignature}
        onSave={handleSaveSignature}
        isLoading={isSignatureLoading}
      />
    </div>
  );
}
