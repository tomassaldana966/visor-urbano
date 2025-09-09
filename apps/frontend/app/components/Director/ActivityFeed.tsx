import { Clock, FileCheck, X, CheckCircle, AlertTriangle } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface ActivityItem {
  id: string;
  type: 'approval' | 'rejection' | 'review' | 'submission' | 'alert';
  title: string;
  description: string;
  timestamp: string;
  folio?: string;
  user?: string;
  priority?: 'high' | 'medium' | 'low';
}

interface ActivityFeedProps {
  activities: ActivityItem[];
  maxItems?: number;
  showViewAll?: boolean;
  onViewAll?: () => void;
}

export function ActivityFeed({
  activities,
  maxItems = 10,
  showViewAll = true,
  onViewAll,
}: ActivityFeedProps) {
  const { t: tDirector } = useTranslation('director');
  const displayedActivities = activities.slice(0, maxItems);

  const getActivityIcon = (type: ActivityItem['type']) => {
    switch (type) {
      case 'approval':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'rejection':
        return <X className="w-4 h-4 text-red-600" />;
      case 'review':
        return <FileCheck className="w-4 h-4 text-blue-600" />;
      case 'submission':
        return <Clock className="w-4 h-4 text-orange-600" />;
      case 'alert':
        return <AlertTriangle className="w-4 h-4 text-yellow-600" />;
      default:
        return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  const getActivityColor = (type: ActivityItem['type']) => {
    switch (type) {
      case 'approval':
        return 'border-l-green-500 bg-green-50';
      case 'rejection':
        return 'border-l-red-500 bg-red-50';
      case 'review':
        return 'border-l-blue-500 bg-blue-50';
      case 'submission':
        return 'border-l-orange-500 bg-orange-50';
      case 'alert':
        return 'border-l-yellow-500 bg-yellow-50';
      default:
        return 'border-l-gray-500 bg-gray-50';
    }
  };

  const getPriorityBadge = (priority?: ActivityItem['priority']) => {
    if (!priority) return null;

    const colors = {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800',
    };

    return (
      <span
        className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${colors[priority]}`}
      >
        {tDirector(`activity.priority.${priority}`)}
      </span>
    );
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">
            {tDirector('activity.title')}
          </h3>
        </div>
      </div>

      <div className="divide-y divide-gray-200">
        {displayedActivities.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            <Clock className="w-8 h-8 mx-auto mb-2 text-gray-300" />
            <p>{tDirector('activity.noActivity')}</p>
          </div>
        ) : (
          displayedActivities.map(activity => (
            <div
              key={activity.id}
              className={`px-6 py-4 border-l-4 ${getActivityColor(activity.type)} hover:bg-gray-50 transition-colors`}
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 mt-1">
                  {getActivityIcon(activity.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {activity.title}
                    </p>
                    <div className="flex items-center space-x-2">
                      {getPriorityBadge(activity.priority)}
                      <span className="text-xs text-gray-500 whitespace-nowrap">
                        {activity.timestamp}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {activity.description}
                  </p>
                  {(activity.folio || activity.user) && (
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      {activity.folio && (
                        <span>
                          {tDirector('activity.labels.folio')}: {activity.folio}
                        </span>
                      )}
                      {activity.user && (
                        <span>
                          {tDirector('activity.labels.user')}: {activity.user}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
