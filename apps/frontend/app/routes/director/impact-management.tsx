import type { LoaderFunctionArgs } from 'react-router';
import { useLoaderData, useNavigate } from 'react-router';
import { useTranslation } from 'react-i18next';
import { useState } from 'react';
import { requireUser } from '../../utils/auth/utils';
import { checkDirectorPermissions } from '@root/app/utils/auth/director';
import { DataTable } from '../../components/Director/Charts/DataTable';
import { Modal } from '../../components/Modal/Modal';
import { Input } from '../../components/Input/Input';
import { Button } from '../../components/Button/Button';
import {
  Plus,
  Target,
  Eye,
  Edit,
  Trash2,
  Search,
  Download,
  BarChart3,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Clock,
  FileText,
} from 'lucide-react';

export const handle = {
  title: 'director:navigation.impactManagement',
  breadcrumb: 'director:navigation.impactManagement',
};

interface ImpactIndicator {
  id: string;
  name: string;
  description: string;
  category: 'environmental' | 'social' | 'economic' | 'infrastructure';
  unit: string;
  targetValue: number;
  currentValue: number;
  trend: 'up' | 'down' | 'stable';
  status: 'good' | 'warning' | 'critical';
  lastMeasurement: string;
  frequency: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  dataSource: string;
  responsible: string;
  notes?: string;
}

export async function loader({ request }: LoaderFunctionArgs) {
  const auth = await requireUser(request);

  const userForPermissions = {
    id: auth.user?.id || 0,
    email: auth.user?.email || '',
    name: auth.user?.name || '',
    role_name: auth.user?.role_name,
    role_id: auth.user?.role_id,
  };

  if (!checkDirectorPermissions(userForPermissions)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  // TODO: Replace with actual API call
  const mockIndicators: ImpactIndicator[] = [
    {
      id: '1',
      name: 'Calidad del Aire (PM2.5)',
      description: 'Concentración de partículas PM2.5 en el aire ambiente',
      category: 'environmental',
      unit: 'μg/m³',
      targetValue: 15,
      currentValue: 18,
      trend: 'down',
      status: 'warning',
      lastMeasurement: '2024-01-20T14:30:00Z',
      frequency: 'daily',
      dataSource: 'Estación de Monitoreo Ambiental',
      responsible: 'Secretaría de Medio Ambiente',
    },
    {
      id: '2',
      name: 'Índice de Desarrollo Social',
      description:
        'Medición del bienestar social en las comunidades municipales',
      category: 'social',
      unit: 'Índice (0-100)',
      targetValue: 75,
      currentValue: 72,
      trend: 'up',
      status: 'good',
      lastMeasurement: '2024-01-15T00:00:00Z',
      frequency: 'quarterly',
      dataSource: 'INEGI y Encuestas Locales',
      responsible: 'Desarrollo Social',
    },
    {
      id: '3',
      name: 'Generación de Empleo',
      description: 'Número de empleos formales generados en el municipio',
      category: 'economic',
      unit: 'Empleos/mes',
      targetValue: 120,
      currentValue: 95,
      trend: 'down',
      status: 'warning',
      lastMeasurement: '2024-01-18T00:00:00Z',
      frequency: 'monthly',
      dataSource: 'IMSS y Cámara de Comercio',
      responsible: 'Desarrollo Económico',
    },
    {
      id: '4',
      name: 'Cobertura de Agua Potable',
      description: 'Porcentaje de población con acceso a agua potable',
      category: 'infrastructure',
      unit: '%',
      targetValue: 95,
      currentValue: 92,
      trend: 'up',
      status: 'good',
      lastMeasurement: '2024-01-17T00:00:00Z',
      frequency: 'monthly',
      dataSource: 'Sistema Municipal de Agua',
      responsible: 'Servicios Públicos',
    },
    {
      id: '5',
      name: 'Deforestación',
      description:
        'Hectáreas de bosque perdidas por actividades no autorizadas',
      category: 'environmental',
      unit: 'hectáreas/año',
      targetValue: 5,
      currentValue: 12,
      trend: 'up',
      status: 'critical',
      lastMeasurement: '2024-01-10T00:00:00Z',
      frequency: 'quarterly',
      dataSource: 'Análisis Satelital CONAFOR',
      responsible: 'Ecología Municipal',
    },
    {
      id: '6',
      name: 'Satisfacción Ciudadana',
      description: 'Nivel de satisfacción con los servicios municipales',
      category: 'social',
      unit: 'Puntuación (1-10)',
      targetValue: 8,
      currentValue: 7.2,
      trend: 'stable',
      status: 'good',
      lastMeasurement: '2024-01-12T00:00:00Z',
      frequency: 'quarterly',
      dataSource: 'Encuesta de Satisfacción',
      responsible: 'Comunicación Social',
    },
  ];

  return { auth, indicators: mockIndicators };
}

export default function ImpactManagement() {
  const { t: tDirector } = useTranslation('director');
  const { indicators } = useLoaderData<typeof loader>();
  const navigate = useNavigate();

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedIndicator, setSelectedIndicator] =
    useState<ImpactIndicator | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  const categories = [
    { value: 'environmental', label: 'Ambiental' },
    { value: 'social', label: 'Social' },
    { value: 'economic', label: 'Económico' },
    { value: 'infrastructure', label: 'Infraestructura' },
  ];

  const statuses = [
    { value: 'good', label: 'Bueno' },
    { value: 'warning', label: 'Advertencia' },
    { value: 'critical', label: 'Crítico' },
  ];

  const filteredIndicators = indicators.filter(indicator => {
    const matchesSearch =
      indicator.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      indicator.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory =
      filterCategory === '' || indicator.category === filterCategory;
    const matchesStatus =
      filterStatus === '' || indicator.status === filterStatus;
    return matchesSearch && matchesCategory && matchesStatus;
  });

  const getProgressPercentage = (current: number, target: number) => {
    return Math.min((current / target) * 100, 100);
  };

  const handleEdit = (indicator: ImpactIndicator) => {
    setSelectedIndicator(indicator);
    setIsEditModalOpen(true);
  };

  const handleView = (indicator: ImpactIndicator) => {
    // TODO: Navigate to detailed view or analytics
  };

  const handleDelete = (indicator: ImpactIndicator) => {
    // TODO: Implement delete functionality
  };
  const columns = [
    {
      key: 'name' as keyof ImpactIndicator,
      label: 'Indicador',
      render: (value: any, row: ImpactIndicator) => (
        <div className="flex items-center space-x-2">
          <Target className="h-4 w-4 text-gray-400" />
          <div>
            <div className="font-medium text-gray-900">{row.name}</div>
            <div className="text-sm text-gray-500">{row.description}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'category' as keyof ImpactIndicator,
      label: 'Categoría',
      render: (value: any, row: ImpactIndicator) => {
        const categoryLabels: Record<string, string> = {
          environmental: 'Ambiental',
          social: 'Social',
          economic: 'Económico',
          infrastructure: 'Infraestructura',
        };
        return (
          <span
            className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
              row.category === 'environmental'
                ? 'bg-green-100 text-green-800'
                : row.category === 'social'
                  ? 'bg-blue-100 text-blue-800'
                  : row.category === 'economic'
                    ? 'bg-purple-100 text-purple-800'
                    : 'bg-orange-100 text-orange-800'
            }`}
          >
            {categoryLabels[row.category]}
          </span>
        );
      },
    },
    {
      key: 'currentValue' as keyof ImpactIndicator,
      label: 'Progreso',
      render: (value: any, row: ImpactIndicator) => {
        const progress = getProgressPercentage(
          row.currentValue,
          row.targetValue
        );
        return (
          <div className="flex items-center space-x-2">
            <div className="w-16 bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${
                  progress >= 80
                    ? 'bg-green-600'
                    : progress >= 60
                      ? 'bg-yellow-600'
                      : 'bg-red-600'
                }`}
                style={{ width: `${Math.min(progress, 100)}%` }}
              />
            </div>
            <span className="text-sm text-gray-600">
              {row.currentValue} / {row.targetValue} {row.unit}
            </span>
          </div>
        );
      },
    },
    {
      key: 'trend' as keyof ImpactIndicator,
      label: 'Tendencia',
      render: (value: any, row: ImpactIndicator) => (
        <div className="flex items-center space-x-1">
          {row.trend === 'up' ? (
            <TrendingUp className="h-4 w-4 text-green-600" />
          ) : row.trend === 'down' ? (
            <TrendingDown className="h-4 w-4 text-red-600" />
          ) : (
            <BarChart3 className="h-4 w-4 text-gray-600" />
          )}
          <span
            className={`text-sm ${
              row.trend === 'up'
                ? 'text-green-600'
                : row.trend === 'down'
                  ? 'text-red-600'
                  : 'text-gray-600'
            }`}
          >
            {row.trend === 'up'
              ? 'Ascendente'
              : row.trend === 'down'
                ? 'Descendente'
                : 'Estable'}
          </span>
        </div>
      ),
    },
    {
      key: 'status' as keyof ImpactIndicator,
      label: 'Estado',
      render: (value: any, row: ImpactIndicator) => (
        <span
          className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
            row.status === 'good'
              ? 'bg-green-100 text-green-800'
              : row.status === 'warning'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-red-100 text-red-800'
          }`}
        >
          {row.status === 'good'
            ? 'Bueno'
            : row.status === 'warning'
              ? 'Advertencia'
              : 'Crítico'}
        </span>
      ),
    },
    {
      key: 'id' as keyof ImpactIndicator, // Usar 'id' en lugar de 'actions'
      label: 'Acciones',
      render: (value: any, row: ImpactIndicator) => (
        <div className="flex items-center space-x-2">
          <Button variant="tertiary" onClick={() => handleView(row)}>
            <Eye className="h-4 w-4" />
          </Button>
          <Button variant="tertiary" onClick={() => handleEdit(row)}>
            <Edit className="h-4 w-4" />
          </Button>
          <Button variant="destructive" onClick={() => handleDelete(row)}>
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ),
    },
  ];

  const goodIndicators = indicators.filter(i => i.status === 'good').length;
  const warningIndicators = indicators.filter(
    i => i.status === 'warning'
  ).length;
  const criticalIndicators = indicators.filter(
    i => i.status === 'critical'
  ).length;
  const averageProgress =
    indicators.reduce(
      (sum, indicator) =>
        sum +
        getProgressPercentage(indicator.currentValue, indicator.targetValue),
      0
    ) / indicators.length;

  return (
    <div className="space-y-6 px-5 md:px-8 lg:px-10 py-6 md:py-8 lg:py-10">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Gestión de Impacto
          </h1>
          <p className="text-gray-600 mt-1">
            Monitoreo y seguimiento de indicadores de impacto municipal
          </p>
        </div>
        <Button onClick={() => setIsAddModalOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Agregar Indicador
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Indicadores Buenos
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {goodIndicators}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-yellow-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  En Advertencia
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {warningIndicators}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Críticos
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {criticalIndicators}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Target className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Progreso Promedio
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {averageProgress.toFixed(1)}%
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                type="text"
                placeholder="Buscar indicadores..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          <div className="sm:w-48">
            <select
              value={filterCategory}
              onChange={e => setFilterCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Todas las categorías</option>
              {categories.map(category => (
                <option key={category.value} value={category.value}>
                  {category.label}
                </option>
              ))}
            </select>
          </div>
          <div className="sm:w-48">
            <select
              value={filterStatus}
              onChange={e => setFilterStatus(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Todos los estados</option>
              {statuses.map(status => (
                <option key={status.value} value={status.value}>
                  {status.label}
                </option>
              ))}
            </select>
          </div>
          <Button variant="secondary">
            <Download className="h-4 w-4 mr-2" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <DataTable
          data={filteredIndicators}
          columns={columns}
          title="Indicadores de Impacto"
          exportable={true}
          searchable={true}
          filterable={true}
        />
      </div>

      {/* Add Indicator Modal */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        title="Agregar Nuevo Indicador"
        size="lg"
      >
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre del Indicador
            </label>
            <Input type="text" placeholder="Ej: Calidad del Agua" required />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Descripción
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              rows={3}
              placeholder="Descripción del indicador y su importancia..."
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Categoría
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                {categories.map(category => (
                  <option key={category.value} value={category.value}>
                    {category.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Unidad de Medida
              </label>
              <Input type="text" placeholder="Ej: %, μg/m³, número" required />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Valor Meta
              </label>
              <Input
                type="number"
                step="any"
                placeholder="Valor objetivo"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Valor Actual
              </label>
              <Input
                type="number"
                step="any"
                placeholder="Valor actual"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Frecuencia de Medición
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                <option value="daily">Diaria</option>
                <option value="weekly">Semanal</option>
                <option value="monthly">Mensual</option>
                <option value="quarterly">Trimestral</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Estado
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                {statuses.map(status => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fuente de Datos
            </label>
            <Input
              type="text"
              placeholder="Ej: Sistema de Monitoreo Ambiental"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Responsable
            </label>
            <Input
              type="text"
              placeholder="Ej: Secretaría de Medio Ambiente"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notas Adicionales
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              rows={2}
              placeholder="Información adicional relevante..."
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsAddModalOpen(false)}
            >
              Cancelar
            </Button>
            <Button type="submit">Agregar Indicador</Button>
          </div>
        </form>
      </Modal>

      {/* Edit Indicator Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedIndicator(null);
        }}
        title="Editar Indicador"
        size="lg"
      >
        {selectedIndicator && (
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nombre del Indicador
              </label>
              <Input
                type="text"
                defaultValue={selectedIndicator.name}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Descripción
              </label>
              <textarea
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                defaultValue={selectedIndicator.description}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Categoría
                </label>
                <select
                  defaultValue={selectedIndicator.category}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  {categories.map(category => (
                    <option key={category.value} value={category.value}>
                      {category.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Unidad de Medida
                </label>
                <Input
                  type="text"
                  defaultValue={selectedIndicator.unit}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Valor Meta
                </label>
                <Input
                  type="number"
                  step="any"
                  defaultValue={selectedIndicator.targetValue}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Valor Actual
                </label>
                <Input
                  type="number"
                  step="any"
                  defaultValue={selectedIndicator.currentValue}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Frecuencia de Medición
                </label>
                <select
                  defaultValue={selectedIndicator.frequency}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="daily">Diaria</option>
                  <option value="weekly">Semanal</option>
                  <option value="monthly">Mensual</option>
                  <option value="quarterly">Trimestral</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Estado
                </label>
                <select
                  defaultValue={selectedIndicator.status}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  {statuses.map(status => (
                    <option key={status.value} value={status.value}>
                      {status.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fuente de Datos
              </label>
              <Input
                type="text"
                defaultValue={selectedIndicator.dataSource}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Responsable
              </label>
              <Input
                type="text"
                defaultValue={selectedIndicator.responsible}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Notas Adicionales
              </label>
              <textarea
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                rows={2}
                defaultValue={selectedIndicator.notes}
              />
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <Button
                type="button"
                variant="secondary"
                onClick={() => {
                  setIsEditModalOpen(false);
                  setSelectedIndicator(null);
                }}
              >
                Cancelar
              </Button>
              <Button type="submit">Guardar Cambios</Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}
