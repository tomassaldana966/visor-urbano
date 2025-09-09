import type { LoaderFunctionArgs } from 'react-router';
import { useLoaderData, useNavigate } from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireUser } from '../../utils/auth/utils';
import { checkDirectorPermissions } from '@root/app/utils/auth/director';
import { MetricsCard } from '../../components/Director/MetricsCard';
import { ActivityFeed } from '../../components/Director/ActivityFeed';
import { QuickActionsPanel } from '../../components/Director/QuickActionsPanel';
import { formatDate } from '../../utils/dates/dates';
import {
  TrendingUp,
  Clock,
  CheckCircle,
  Users,
  FileText,
  Building,
} from 'lucide-react';
import { getDirectorDashboard } from '../../utils/api/director';
import { getAccessToken } from '../../utils/auth/auth.server';

export const handle = {
  title: 'director:navigation.dashboard',
  breadcrumb: 'director:navigation.dashboard',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const auth = await requireUser(request);
  const accessToken = await getAccessToken(request);

  // Convert to the expected AuthUser type for director permissions check
  const userForPermissions = {
    id: auth.user?.id || 0,
    email: auth.user?.email || '',
    name: auth.user?.name || '',
    role_name: auth.user?.role_name,
    role_id: auth.user?.role_id,
  };

  if (!checkDirectorPermissions(userForPermissions)) {
    throw new Response('Unauthorized access', { status: 403 });
  }

  // Get complete dashboard data from API if access token is available
  let dashboardData = null;
  if (accessToken) {
    try {
      dashboardData = await getDirectorDashboard(accessToken);
    } catch (error) {
      console.error('Error fetching director dashboard:', error);
      // Continue with fallback values if API fails
    }
  }

  // Use real data from API or fallback to default values
  const finalDashboardData = dashboardData || {
    total_procedures_this_month: 0,
    pending_procedures: 0,
    licenses_issued_today: 0, // Changed from procedures_completed_today
    licenses_trend: 0, // New field for trend
    average_processing_time: 8.5,
    procedures_by_type: {
      construction: 0,
      commercial: 0,
      others: 0,
    },
    recent_activities: [],
    pending_reviews: 0,
    alerts: 0,
  };

  return { auth, dashboardData: finalDashboardData };
}

export default function DirectorDashboard() {
  const { t: tDirector } = useTranslation('director');
  const { auth, dashboardData } = useLoaderData<typeof loader>();
  const navigate = useNavigate();

  // Transform real activity data from backend - no need for mock translations
  const translatedActivities = dashboardData.recent_activities.map(
    activity => ({
      id: activity.id,
      type: activity.type as
        | 'approval'
        | 'rejection'
        | 'review'
        | 'submission'
        | 'alert',
      title: activity.title,
      description: activity.description,
      timestamp: new Date(activity.timestamp).toLocaleTimeString() + ' ago',
      folio: activity.folio || undefined,
      user: activity.user_name || 'Usuario no especificado',
      priority: activity.priority as 'high' | 'medium' | 'low' | undefined,
    })
  );

  // Get real average processing time from backend
  const averageProcessingTime = `${dashboardData.average_processing_time} ${tDirector('time.days')}`;

  const handleNavigateToUsers = () => navigate('/director/users');
  const handleNavigateToAnalytics = () => navigate('/director/analytics');
  const handleNavigateToSettings = () => navigate('/director/settings');
  const handleNavigateToMunicipalLayers = () =>
    navigate('/director/municipal-layers');
  const handleNavigateToImpactMap = () => navigate('/director/impact-map');
  const handleNavigateToRoles = () => navigate('/director/roles');
  const handleNavigateToRequirements = () => navigate('/director/requirements');
  const handleNavigateToDependencies = () => navigate('/director/dependencies');
  const handleNavigateToBusinessTypes = () =>
    navigate('/director/business-types');
  const handleNavigateToBlog = () => navigate('/director/blog');

  const handleExportReports = () => {
    window.open('/director/reports/export', '_blank');
  };

  const handleViewNotifications = () => {
    navigate('/director/notifications');
  };

  const handleViewAllActivity = () => {
    navigate('/director/activity');
  };

  return (
    <div className="space-y-6 px-5 md:px-8 lg:px-10 py-6 md:py-8 lg:py-10">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {tDirector('title')}
          </h1>
          <p className="text-gray-600 mt-1">
            {tDirector('welcome', { name: auth.user?.name })}
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">{tDirector('lastUpdate')}</p>
          <p className="text-sm font-medium text-gray-900">
            {formatDate(new Date().toISOString())}
          </p>
        </div>
      </div>

      {/* Main metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard
          title={tDirector('metrics.totalProcedures')}
          value={dashboardData.total_procedures_this_month}
          icon={<FileText className="w-6 h-6" />}
          trend="up"
          trendValue={tDirector('metrics.trends.up', {
            value: '12%',
            period: tDirector('metrics.trends.previousMonth'),
          })}
          color="primary"
          onClick={() => navigate('/director/analytics')}
        />
        <MetricsCard
          title={tDirector('metrics.pendingApprovals')}
          value={dashboardData.pending_procedures}
          icon={<Clock className="w-6 h-6" />}
          color="warning"
          onClick={() => navigate('/procedure-approvals')}
        />
        <MetricsCard
          title={tDirector('metrics.licensesIssuedToday')}
          value={dashboardData.licenses_issued_today}
          icon={<CheckCircle className="w-6 h-6" />}
          trend={dashboardData.licenses_trend >= 0 ? 'up' : 'down'}
          trendValue={`${Math.abs(dashboardData.licenses_trend)} ${tDirector('metrics.trends.vsYesterday')}`}
          color="success"
        />
        <MetricsCard
          title={tDirector('metrics.averageProcessingTime')}
          value={averageProcessingTime}
          icon={<TrendingUp className="w-6 h-6" />}
          trend="down"
          trendValue={tDirector('metrics.trends.down', {
            value: '0.5 ' + tDirector('time.days'),
            period: tDirector('metrics.trends.previousMonth'),
          })}
          color="primary"
        />
      </div>

      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent activity - using specialized component */}
        <div className="lg:col-span-2">
          <ActivityFeed
            activities={translatedActivities}
            maxItems={5}
            showViewAll={true}
            onViewAll={handleViewAllActivity}
          />
        </div>

        {/* Side panel with statistics */}
        <div className="space-y-6">
          {/* Quick summary */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {tDirector('summary.title')}
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Building className="h-4 w-4 text-blue-600" />
                  <span className="text-sm text-gray-600">
                    {tDirector('summary.categories.construction')}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {dashboardData.procedures_by_type.construction}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Users className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-gray-600">
                    {tDirector('summary.categories.commercial')}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {dashboardData.procedures_by_type.commercial}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <FileText className="h-4 w-4 text-purple-600" />
                  <span className="text-sm text-gray-600">
                    {tDirector('summary.categories.others')}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {dashboardData.procedures_by_type.others}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick actions panel - using specialized component */}
      <QuickActionsPanel
        onNavigateToUsers={handleNavigateToUsers}
        onNavigateToAnalytics={handleNavigateToAnalytics}
        onNavigateToSettings={handleNavigateToSettings}
        onNavigateToMunicipalLayers={handleNavigateToMunicipalLayers}
        onNavigateToImpactMap={handleNavigateToImpactMap}
        onNavigateToRoles={handleNavigateToRoles}
        onNavigateToRequirements={handleNavigateToRequirements}
        onNavigateToDependencies={handleNavigateToDependencies}
        onNavigateToBusinessTypes={handleNavigateToBusinessTypes}
        onNavigateToBlog={handleNavigateToBlog}
        onExportReports={handleExportReports}
        onViewNotifications={handleViewNotifications}
      />
    </div>
  );
}
