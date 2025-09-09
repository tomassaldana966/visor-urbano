import { useEffect } from 'react';
import { Loader, Map } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { cn } from '@/lib/utils';

interface LoadingModalProps {
  isOpen: boolean;
  message?: string;
  type?: 'default' | 'map';
  useTranslations?: boolean;
}

export function LoadingModal({
  isOpen,
  message,
  type = 'default',
  useTranslations = false,
}: LoadingModalProps) {
  const { t } = useTranslation('common');

  const getLoadingContent = () => {
    if (useTranslations && type === 'map') {
      return {
        title: t('loading.map.title'),
        message: t('loading.map.message'),
        subtitle: t('loading.map.subtitle'),
      };
    }

    if (useTranslations) {
      return {
        title: t('loading.default.title'),
        message: message || t('loading.default.message'),
        subtitle: t('loading.default.subtitle'),
      };
    }

    // Default fallback values when not using translations
    return {
      title: type === 'map' ? 'Loading Map' : 'Saving Changes',
      message: message || 'Saving information...',
      subtitle: 'Please wait while we process your information...',
    };
  };

  const loadingContent = getLoadingContent();
  const IconComponent = type === 'map' ? Map : Loader;
  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    // Cleanup on unmount
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center animate-in fade-in duration-200">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm" />

      {/* Modal Content */}
      <div className="relative bg-white rounded-lg shadow-xl p-8 mx-4 max-w-sm w-full animate-in slide-in-from-bottom-4 duration-300">
        <div className="flex flex-col items-center space-y-4">
          {/* Loading Spinner */}
          <div className="relative">
            <IconComponent
              size={48}
              className={cn(
                type === 'map' ? 'text-green-600' : 'text-blue-600',
                type === 'map' ? 'animate-pulse' : 'animate-spin'
              )}
            />
          </div>

          {/* Message */}
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {loadingContent.title}
            </h3>
            <p className="text-gray-600 text-sm">{loadingContent.message}</p>
            <p className="text-gray-500 text-xs mt-2">
              {loadingContent.subtitle}
            </p>
          </div>

          {/* Progress indicator */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={cn(
                'h-2 rounded-full animate-pulse',
                type === 'map' ? 'bg-green-600' : 'bg-blue-600'
              )}
              style={{ width: '100%' }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
}
