import {
  Users,
  BarChart3,
  Settings,
  Layers,
  Shield,
  FileText,
  Building,
  Building2,
  Map,
  BookOpen,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface QuickAction {
  id: string;
  label: string;
  description: string;
  icon: React.ReactNode;
  onClick: () => void;
  badge?: number;
  color?: 'primary' | 'success' | 'warning' | 'danger';
  disabled?: boolean;
}

interface QuickActionsPanelProps {
  onNavigateToUsers: () => void;
  onNavigateToAnalytics: () => void;
  onNavigateToSettings: () => void;
  onNavigateToMunicipalLayers: () => void;
  onNavigateToImpactMap: () => void;
  onNavigateToRoles: () => void;
  onNavigateToRequirements: () => void;
  onNavigateToBusinessTypes: () => void;
  onNavigateToDependencies: () => void;
  onNavigateToBlog: () => void;
  onExportReports: () => void;
  onViewNotifications: () => void;
}

export function QuickActionsPanel({
  onNavigateToUsers,
  onNavigateToAnalytics,
  onNavigateToSettings,
  onNavigateToMunicipalLayers,
  onNavigateToImpactMap,
  onNavigateToRoles,
  onNavigateToRequirements,
  onNavigateToBusinessTypes,
  onNavigateToDependencies,
  onNavigateToBlog,
  onExportReports,
  onViewNotifications,
}: QuickActionsPanelProps) {
  const { t: tDirector } = useTranslation('director');

  const quickActions: QuickAction[] = [
    {
      id: 'analytics',
      label: tDirector('quickActions.actions.analytics.label'),
      description: tDirector('quickActions.actions.analytics.description'),
      icon: <BarChart3 className="w-5 h-5" />,
      onClick: onNavigateToAnalytics,
      color: 'primary',
    },
    {
      id: 'dependencies',
      label: tDirector('quickActions.actions.dependencies.label'),
      description: tDirector('quickActions.actions.dependencies.description'),
      icon: <Building2 className="w-5 h-5" />,
      onClick: onNavigateToDependencies,
      color: 'primary',
    },
    {
      id: 'municipalLayers',
      label: tDirector('quickActions.actions.municipalLayers.label'),
      description: tDirector(
        'quickActions.actions.municipalLayers.description'
      ),
      icon: <Layers className="w-5 h-5" />,
      onClick: onNavigateToMunicipalLayers,
      color: 'primary',
    },
    {
      id: 'impactMap',
      label: tDirector('quickActions.actions.impactMap.label'),
      description: tDirector('quickActions.actions.impactMap.description'),
      icon: <Map className="w-5 h-5" />,
      onClick: onNavigateToImpactMap,
      color: 'primary',
    },
    {
      id: 'users',
      label: tDirector('quickActions.actions.users.label'),
      description: tDirector('quickActions.actions.users.description'),
      icon: <Users className="w-5 h-5" />,
      onClick: onNavigateToUsers,
      color: 'primary',
    },
    {
      id: 'roles',
      label: tDirector('quickActions.actions.roles.label'),
      description: tDirector('quickActions.actions.roles.description'),
      icon: <Shield className="w-5 h-5" />,
      onClick: onNavigateToRoles,
      color: 'primary',
    },
    {
      id: 'requirements',
      label: tDirector('quickActions.actions.requirements.label'),
      description: tDirector('quickActions.actions.requirements.description'),
      icon: <FileText className="w-5 h-5" />,
      onClick: onNavigateToRequirements,
      color: 'primary',
    },
    {
      id: 'businessTypes',
      label: tDirector('quickActions.actions.businessTypes.label'),
      description: tDirector('quickActions.actions.businessTypes.description'),
      icon: <Building className="w-5 h-5" />,
      onClick: onNavigateToBusinessTypes,
      color: 'primary',
    },
    {
      id: 'blog',
      label: tDirector('quickActions.actions.blog.label'),
      description: tDirector('quickActions.actions.blog.description'),
      icon: <BookOpen className="w-5 h-5" />,
      onClick: onNavigateToBlog,
      color: 'primary',
    },
    {
      id: 'settings',
      label: tDirector('quickActions.actions.settings.label'),
      description: tDirector('quickActions.actions.settings.description'),
      icon: <Settings className="w-5 h-5" />,
      onClick: onNavigateToSettings,
      color: 'primary',
    },
  ];

  const getActionColors = (color: QuickAction['color']) => {
    switch (color) {
      case 'success':
        return 'border-green-200 hover:border-green-300 hover:bg-green-50';
      case 'warning':
        return 'border-yellow-200 hover:border-yellow-300 hover:bg-yellow-50';
      case 'danger':
        return 'border-red-200 hover:border-red-300 hover:bg-red-50';
      default:
        return 'border-blue-200 hover:border-blue-300 hover:bg-blue-50';
    }
  };

  const getIconColors = (color: QuickAction['color']) => {
    switch (color) {
      case 'success':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'danger':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-blue-600 bg-blue-100';
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">
          {tDirector('quickActions.title')}
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          {tDirector('quickActions.subtitle')}
        </p>
      </div>

      <div className="p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map(action => (
            <button
              key={action.id}
              onClick={action.onClick}
              disabled={action.disabled}
              className={`
                relative p-4 border-2 rounded-lg text-left transition-all duration-200
                ${getActionColors(action.color)}
                ${
                  action.disabled
                    ? 'opacity-50 cursor-not-allowed'
                    : 'cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                }
              `}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div
                    className={`inline-flex p-2 rounded-lg ${getIconColors(action.color)} mb-3`}
                  >
                    {action.icon}
                  </div>
                  <h4 className="text-sm font-medium text-gray-900 mb-1">
                    {action.label}
                  </h4>
                  <p className="text-xs text-gray-600">{action.description}</p>
                </div>
                {action.badge !== undefined && action.badge > 0 && (
                  <span className="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-600 rounded-full">
                    {action.badge > 99 ? '99+' : action.badge}
                  </span>
                )}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
