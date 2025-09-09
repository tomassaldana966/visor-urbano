import type { LoaderFunctionArgs } from 'react-router';
import { useState } from 'react';
import { useLoaderData } from 'react-router';
import { useTranslation } from 'react-i18next';
import {
  Clock,
  TrendingUp,
  BarChart3,
  Star,
  Calendar,
  Download,
  Filter,
  RefreshCw,
} from 'lucide-react';
import { requireAuth, getAccessToken } from '../../utils/auth/auth.server';
import { checkDirectorPermissions } from '../../utils/auth/director';
import { PieChart } from '../../components/Director/Charts/PieChart';
import { BarChart } from '../../components/Director/Charts/BarChart';
import {
  getCompleteAnalytics,
  type CompleteAnalytics,
  type ChartPoint,
  type LicensingStatusSummary,
  type ReviewStatusSummary,
} from '../../utils/api/reports';
import { useAnalyticsPDF } from '../../hooks/useAnalyticsPDF';

interface AnalyticsData {
  kpis: {
    tiempo_promedio: number;
    eficiencia: number;
    total_procesados: number;
    satisfaccion: number;
  };
  tendencias: ChartPoint[];
  distribucion_estados: Array<{
    estado: string;
    cantidad: number;
    porcentaje: number;
    color: string;
  }>;
  dependencias: Array<{
    id: string;
    nombre: string;
    tramites_procesados: number;
    tiempo_promedio: number;
    eficiencia: number;
    estado: string;
  }>;
  licensing_status: LicensingStatusSummary;
  review_status: ReviewStatusSummary;
}

export const handle = {
  title: 'director:analytics.title',
  breadcrumb: 'director:analytics.breadcrumb',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  const authToken = await getAccessToken(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Unauthorized access', { status: 403 });
  }

  if (!authToken) {
    throw new Response('Authentication token required', { status: 401 });
  }

  try {
    const analyticsData = await getCompleteAnalytics(authToken);

    return { user, analytics: analyticsData };
  } catch (error) {
    console.error('Error loading analytics data:', error);

    const fallbackData: AnalyticsData = {
      kpis: {
        tiempo_promedio: 8.5,
        eficiencia: 87,
        total_procesados: 0,
        satisfaccion: 4.2,
      },
      tendencias: [
        { name: 'Ene', value: 234, extra: 1 },
        { name: 'Feb', value: 267, extra: 2 },
        { name: 'Mar', value: 298, extra: 3 },
        { name: 'Abr', value: 312, extra: 4 },
        { name: 'May', value: 289, extra: 5 },
        { name: 'Jun', value: 325, extra: 6 },
      ],
      distribucion_estados: [
        {
          estado: 'Completados',
          cantidad: 0,
          porcentaje: 0,
          color: 'bg-green-500',
        },
        {
          estado: 'En Proceso',
          cantidad: 0,
          porcentaje: 0,
          color: 'bg-blue-500',
        },
        {
          estado: 'Pendientes',
          cantidad: 0,
          porcentaje: 0,
          color: 'bg-yellow-500',
        },
        {
          estado: 'Rechazados',
          cantidad: 0,
          porcentaje: 0,
          color: 'bg-red-500',
        },
      ],
      dependencias: [],
      licensing_status: {
        consultation: 0,
        initiated: 0,
        under_review: 0,
        issued: 0,
      },
      review_status: {
        approved: 0,
        under_review: 0,
        corrected: 0,
        discarded: 0,
      },
    };

    return { user, analytics: fallbackData };
  }
}

export default function DirectorAnalytics() {
  const { t } = useTranslation('director');
  const { analytics } = useLoaderData<typeof loader>();
  const [selectedPeriod, setSelectedPeriod] = useState('30d');
  const [selectedReport, setSelectedReport] = useState('general');
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const { generatePDF } = useAnalyticsPDF();

  const handleRefresh = () => {
    setIsLoading(true);
    window.location.reload();
  };

  const handleExportPdf = async () => {
    setIsExporting(true);
    try {
      const result = await generatePDF(analytics, selectedPeriod);

      if (!result.success) {
        // Optionally show an error message
        console.error('Error al generar PDF:', result.error);
      }
    } catch (error) {
      console.error('Error inesperado al generar PDF:', error);
      alert('Error inesperado al generar el PDF');
    } finally {
      setIsExporting(false);
    }
  };

  const getStatusColor = (estado: string) => {
    switch (estado) {
      case 'excellent':
        return 'text-green-600 bg-green-100';
      case 'good':
        return 'text-blue-600 bg-blue-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'poor':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusText = (estado: string) => {
    switch (estado) {
      case 'excellent':
        return t('analytics.performance.statusLevels.excellent');
      case 'good':
        return t('analytics.performance.statusLevels.good');
      case 'warning':
        return t('analytics.performance.statusLevels.warning');
      case 'poor':
        return t('analytics.performance.statusLevels.poor');
      default:
        return t('analytics.performance.statusLevels.na');
    }
  };

  const getTranslatedStatusName = (estado: string) => {
    const statusMapping: Record<string, string> = {
      Consultas: t('analytics.statuses.consultations'),
      Iniciados: t('analytics.statuses.initiated'),
      'En Revisión': t('analytics.statuses.underReview'),
      Emitidos: t('analytics.statuses.issued'),
      Completados: t('analytics.statuses.completed'),
      'En Proceso': t('analytics.statuses.inProcess'),
      Pendientes: t('analytics.statuses.pending'),
      Rechazados: t('analytics.statuses.rejected'),
      Consultations: t('analytics.statuses.consultations'),
      Initiated: t('analytics.statuses.initiated'),
      'Under Review': t('analytics.statuses.underReview'),
      Issued: t('analytics.statuses.issued'),
    };
    return statusMapping[estado] || estado;
  };

  const getTranslatedDependencyName = (nombre: string) => {
    const dependencyMapping: Record<string, string> = {
      'Revisiones Aprobadas': t(
        'analytics.performance.dependencyNames.approvedReviews'
      ),
      'En Revisión': t('analytics.performance.dependencyNames.underReview'),
      'Para Corrección': t(
        'analytics.performance.dependencyNames.forCorrection'
      ),
      Descartados: t('analytics.performance.dependencyNames.discarded'),
      'Approved Reviews': t(
        'analytics.performance.dependencyNames.approvedReviews'
      ),
      'Under Review': t('analytics.performance.dependencyNames.underReview'),
      'For Correction': t(
        'analytics.performance.dependencyNames.forCorrection'
      ),
      Discarded: t('analytics.performance.dependencyNames.discarded'),
    };
    return dependencyMapping[nombre] || nombre;
  };

  return (
    <div className="space-y-6 px-5 md:px-8 lg:px-10 py-6 md:py-8 lg:py-10">
      {/* Header de la página */}
      <div className="border-b border-gray-200 pb-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {t('analytics.title')}
            </h2>
            <p className="text-gray-600 mt-1">{t('analytics.subtitle')}</p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={handleRefresh}
              disabled={isLoading}
              className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <RefreshCw
                className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`}
              />
              {isLoading ? t('common.loading') : t('analytics.refresh')}
            </button>
            <button
              onClick={handleExportPdf}
              disabled={isExporting}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Download
                className={`w-4 h-4 mr-2 ${isExporting ? 'animate-pulse' : ''}`}
              />
              {isExporting
                ? t('analytics.exporting')
                : t('analytics.exportPdf')}
            </button>
          </div>
        </div>
      </div>

      {/* Filtros de período */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div>
              <label
                htmlFor="periodo"
                className="block text-sm font-medium text-gray-700"
              >
                {t('analytics.filters.period')}
              </label>
              <select
                id="periodo"
                value={selectedPeriod}
                onChange={e => setSelectedPeriod(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="7d">{t('analytics.filters.periods.7d')}</option>
                <option value="30d">
                  {t('analytics.filters.periods.30d')}
                </option>
                <option value="90d">
                  {t('analytics.filters.periods.90d')}
                </option>
                <option value="1y">{t('analytics.filters.periods.1y')}</option>
              </select>
            </div>
            <div>
              <label
                htmlFor="tipo-reporte"
                className="block text-sm font-medium text-gray-700"
              >
                {t('analytics.filters.reportType')}
              </label>
              <select
                id="tipo-reporte"
                value={selectedReport}
                onChange={e => setSelectedReport(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="general">
                  {t('analytics.filters.reportTypes.general')}
                </option>
                <option value="eficiencia">
                  {t('analytics.filters.reportTypes.efficiency')}
                </option>
                <option value="dependencias">
                  {t('analytics.filters.reportTypes.dependencies')}
                </option>
                <option value="tipos">
                  {t('analytics.filters.reportTypes.types')}
                </option>
              </select>
            </div>
          </div>
          <div className="flex items-center text-sm text-gray-500">
            <Calendar className="w-4 h-4 mr-1" />
            {t('analytics.lastUpdate')}: {new Date().toLocaleDateString()}
          </div>
        </div>
      </div>

      {/* KPIs principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">
                {t('analytics.kpis.averageTime')}
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {analytics.kpis.tiempo_promedio}{' '}
                {t('analytics.kpis.units.days')}
              </p>
              <p className="text-sm text-green-600 flex items-center mt-1">
                <TrendingUp className="w-3 h-3 mr-1" />
                {t('analytics.kpis.trends.decrease', { value: 12 })}
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">
                {t('analytics.kpis.efficiency')}
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {analytics.kpis.eficiencia}
                {t('analytics.kpis.units.percentage')}
              </p>
              <p className="text-sm text-green-600 flex items-center mt-1">
                <TrendingUp className="w-3 h-3 mr-1" />
                {t('analytics.kpis.trends.increase', { value: 5 })}
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">
                {t('analytics.kpis.totalProcessed')}
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {analytics.kpis.total_procesados.toLocaleString()}
              </p>
              <p className="text-sm text-green-600 flex items-center mt-1">
                <TrendingUp className="w-3 h-3 mr-1" />
                {t('analytics.kpis.trends.increase', { value: 23 })}
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">
                {t('analytics.kpis.satisfaction')}
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {analytics.kpis.satisfaccion}
                {t('analytics.kpis.units.rating')}
              </p>
              <p className="text-sm text-green-600 flex items-center mt-1">
                <TrendingUp className="w-3 h-3 mr-1" />
                {t('analytics.kpis.trends.rating_increase', { value: '0.3' })}
              </p>
            </div>
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Star className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {t('analytics.charts.monthlyTrends')}
          </h3>
          <div className="h-64">
            <div className="flex items-end justify-between h-48 border-b border-gray-200">
              {analytics.tendencias.map((item, index) => (
                <div key={index} className="flex flex-col items-center">
                  <div
                    className="bg-blue-500 rounded-t"
                    style={{
                      height: `${Math.max((item.value / 350) * 100, 5)}%`,
                      width: '24px',
                    }}
                  />
                  <span className="text-xs text-gray-600 mt-2">
                    {item.name}
                  </span>
                  <span className="text-xs font-medium text-gray-900">
                    {item.value}
                  </span>
                </div>
              ))}
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-2">
              <span>{t('analytics.charts.months.january')}</span>
              <span>{t('analytics.charts.months.december')}</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {t('analytics.charts.statusDistribution')}
          </h3>
          <div className="space-y-4">
            {analytics.distribucion_estados.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className={`w-3 h-3 rounded-full ${item.color} mr-3`} />
                  <span className="text-sm font-medium text-gray-900">
                    {getTranslatedStatusName(item.estado)}
                  </span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${item.color}`}
                      style={{ width: `${item.porcentaje}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-600 w-12 text-right">
                    {item.porcentaje}%
                  </span>
                  <span className="text-sm font-medium text-gray-900 w-16 text-right">
                    {item.cantidad}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">
              {t('analytics.performance.title')}
            </h3>
            <button className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700">
              <Filter className="w-4 h-4 mr-1" />
              {t('analytics.filters.filter')}
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('analytics.performance.columns.dependency')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('analytics.performance.columns.processedProcedures')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('analytics.performance.columns.averageTime')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('analytics.performance.columns.efficiency')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('analytics.performance.columns.status')}
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {analytics.dependencias.map(dep => (
                <tr key={dep.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {getTranslatedDependencyName(dep.nombre)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {dep.tramites_procesados.toLocaleString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {dep.tiempo_promedio} {t('analytics.kpis.units.days')}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2 mr-3">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${dep.eficiencia}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-900">
                        {dep.eficiencia}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(
                        dep.estado
                      )}`}
                    >
                      {getStatusText(dep.estado)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PieChart
          data={analytics.distribucion_estados.map(item => ({
            ...item,
            estado: getTranslatedStatusName(item.estado),
          }))}
          title={t('analytics.charts.statusDistribution')}
        />

        <BarChart
          data={analytics.tendencias.map(item => ({
            mes: item.name,
            tramites: item.value,
            eficiencia: 85,
          }))}
          title={t('analytics.charts.monthlyTrends')}
        />
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          {t('analytics.charts.municipalSummary')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {analytics.licensing_status.consultation}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.consultations')}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {analytics.licensing_status.initiated}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.initiated')}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {analytics.licensing_status.under_review}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.underReview')}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {analytics.licensing_status.issued}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.issued')}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          {t('analytics.charts.departmentalReviews')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {analytics.review_status.approved}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.approved')}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {analytics.review_status.under_review}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.underReview')}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {analytics.review_status.corrected}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.corrected')}
            </div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              {analytics.review_status.discarded}
            </div>
            <div className="text-sm text-gray-600">
              {t('analytics.statuses.discarded')}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
