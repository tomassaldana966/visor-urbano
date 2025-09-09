import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  X,
  Plus,
  Trash2,
  AlertTriangle,
  FileText,
  Building,
  Users,
  Scale,
  Settings,
  ChevronDown,
  Info,
} from 'lucide-react';

interface WorkflowModalProps {
  isOpen: boolean;
  onClose: () => void;
  workflow?: WorkflowData | null;
  onSave: (workflow: WorkflowData) => void;
}

interface WorkflowData {
  id: string;
  name: string;
  type: string;
  steps: number;
  avgDays: number;
  active: boolean;

  // Extended properties for comprehensive workflow
  documentType?: string;
  description?: string;
  legalFoundation?: string;
  requirements?: WorkflowRequirement[];
  conditions?: WorkflowCondition[];
  dependencies?: WorkflowDependency[];
  approvals?: WorkflowApproval[];
  departments?: string[];
}

interface WorkflowRequirement {
  id: string;
  title: string;
  description: string;
  mandatory: boolean;
  departmentIssued: boolean;
  conditionalLogic?: ConditionRule[];
}

interface WorkflowCondition {
  id: string;
  type:
    | 'property_size'
    | 'activity_surface'
    | 'applicant_type'
    | 'person_type'
    | 'alcohol_sales'
    | 'activity_type';
  operator: '>' | '<' | '=' | '>=' | '<=' | '!=' | 'includes' | 'excludes';
  value: string | number;
  action: 'require' | 'exclude' | 'modify';
  targetRequirementId?: string;
}

interface WorkflowDependency {
  id: string;
  dependsOn: string; // workflow id
  condition: 'approved' | 'rejected' | 'completed';
  description: string;
}

interface WorkflowApproval {
  id: string;
  stepNumber: number;
  department: string;
  role: string;
  required: boolean;
  parallelApproval: boolean;
  isBlocking: boolean;
  fileType: string;
  legalFoundation: string;
  isExternalDepartment: boolean;
  estimatedDays: number;
}

interface ConditionRule {
  field: string;
  operator: string;
  value: string;
  logic?: 'AND' | 'OR';
}

export function WorkflowModal({
  isOpen,
  onClose,
  workflow,
  onSave,
}: WorkflowModalProps) {
  const { t } = useTranslation('director');
  const [activeTab, setActiveTab] = useState('basic');

  // Sample data for demonstration
  const getSampleData = (): WorkflowData => ({
    id: workflow?.id || Date.now().toString(),
    name: workflow?.name || 'Licencia de Construcción Residencial',
    type: workflow?.type || 'construction',
    steps: workflow?.steps || 5,
    avgDays: workflow?.avgDays || 45,
    active: workflow?.active ?? true,
    documentType: workflow?.documentType || 'permit',
    description:
      workflow?.description ||
      'Licencia para la construcción de viviendas unifamiliares y multifamiliares en zonas residenciales. Incluye revisión de planos arquitectónicos, estructurales y cumplimiento de normativas urbanas.',
    legalFoundation:
      workflow?.legalFoundation ||
      'Artículo 115 de la Constitución Política, Ley General de Asentamientos Humanos, Ordenamiento Territorial y Desarrollo Urbano, Reglamento de Construcciones Municipal',
    requirements: workflow?.requirements || [
      {
        id: '1',
        title: 'Identificación Oficial del Solicitante',
        description:
          'Credencial de elector vigente, pasaporte vigente o cédula profesional. Debe estar en original y copia para cotejo.',
        mandatory: true,
        departmentIssued: false,
        conditionalLogic: [],
      },
      {
        id: '2',
        title: 'Escritura de Propiedad o Documento de Posesión',
        description:
          'Escritura pública registrada ante el Registro Público de la Propiedad, contrato de compraventa con firma ante notario, o documento que acredite la posesión legal del inmueble.',
        mandatory: true,
        departmentIssued: false,
        conditionalLogic: [
          {
            field: 'applicant_type',
            operator: '=',
            value: 'empresa',
            logic: 'AND',
          },
        ],
      },
      {
        id: '3',
        title: 'Planos Arquitectónicos',
        description:
          'Planos arquitectónicos a escala 1:100 o 1:50, con plantas, cortes, fachadas y ubicación. Firmados por arquitecto con cédula profesional vigente.',
        mandatory: true,
        departmentIssued: false,
        conditionalLogic: [],
      },
      {
        id: '4',
        title: 'Proyecto Estructural',
        description:
          'Memorias de cálculo y planos estructurales firmados por ingeniero civil con cédula profesional. Requerido para construcciones mayores a 60m² o de más de un nivel.',
        mandatory: false,
        departmentIssued: false,
        conditionalLogic: [
          {
            field: 'property_size',
            operator: '>',
            value: '60',
            logic: 'OR',
          },
          {
            field: 'building_levels',
            operator: '>',
            value: '1',
          },
        ],
      },
      {
        id: '5',
        title: 'Estudio de Impacto Ambiental',
        description:
          'Evaluación de impacto ambiental realizada por especialista certificado. Obligatorio para construcciones en zonas de conservación o mayores a 200m².',
        mandatory: false,
        departmentIssued: true,
        conditionalLogic: [
          {
            field: 'property_size',
            operator: '>',
            value: '200',
            logic: 'OR',
          },
          {
            field: 'zone_type',
            operator: '=',
            value: 'conservacion',
          },
        ],
      },
    ],
    conditions: workflow?.conditions || [
      {
        id: '1',
        type: 'property_size',
        operator: '>',
        value: 120,
        action: 'require',
        targetRequirementId: '4',
      },
      {
        id: '2',
        type: 'applicant_type',
        operator: '=',
        value: 'empresa',
        action: 'require',
        targetRequirementId: '2',
      },
      {
        id: '3',
        type: 'activity_surface',
        operator: '>',
        value: 200,
        action: 'require',
        targetRequirementId: '5',
      },
      {
        id: '4',
        type: 'person_type',
        operator: '=',
        value: 'extranjero',
        action: 'modify',
        targetRequirementId: '1',
      },
    ],
    dependencies: workflow?.dependencies || [
      {
        id: '1',
        dependsOn: 'uso-suelo-001',
        condition: 'approved',
        description:
          'Debe contar con dictamen de uso de suelo compatible aprobado',
      },
      {
        id: '2',
        dependsOn: 'factibilidad-servicios-001',
        condition: 'approved',
        description:
          'Factibilidad de servicios básicos (agua, drenaje, electricidad) confirmada',
      },
    ],
    approvals: workflow?.approvals || [
      {
        id: '1',
        stepNumber: 1,
        department: 'Atención Ciudadana',
        role: 'reviewer',
        required: true,
        parallelApproval: false,
        isBlocking: true,
        fileType: 'document',
        legalFoundation: 'Artículo 42 del Reglamento de Construcciones',
        isExternalDepartment: false,
        estimatedDays: 3,
      },
      {
        id: '2',
        stepNumber: 2,
        department: 'Desarrollo Urbano',
        role: 'specialist',
        required: true,
        parallelApproval: true,
        isBlocking: true,
        fileType: 'technical_drawing',
        legalFoundation: 'Artículo 45-48 del Reglamento de Construcciones',
        isExternalDepartment: false,
        estimatedDays: 15,
      },
      {
        id: '3',
        stepNumber: 2,
        department: 'Protección Civil',
        role: 'specialist',
        required: true,
        parallelApproval: true,
        isBlocking: true,
        fileType: 'certificate',
        legalFoundation: 'Ley de Protección Civil Municipal Artículo 23',
        isExternalDepartment: false,
        estimatedDays: 10,
      },
      {
        id: '4',
        stepNumber: 3,
        department: 'Licencias de Construcción',
        role: 'supervisor',
        required: true,
        parallelApproval: false,
        isBlocking: true,
        fileType: 'inspection_report',
        legalFoundation: 'Artículo 52 del Reglamento de Construcciones',
        isExternalDepartment: false,
        estimatedDays: 10,
      },
      {
        id: '5',
        stepNumber: 4,
        department: 'Dirección General',
        role: 'director',
        required: true,
        parallelApproval: false,
        isBlocking: false,
        fileType: 'certificate',
        legalFoundation: 'Artículo 115 Constitucional fracción V',
        isExternalDepartment: false,
        estimatedDays: 7,
      },
    ],
    departments: workflow?.departments || [
      'Atención Ciudadana',
      'Desarrollo Urbano',
      'Protección Civil',
      'Licencias de Construcción',
      'Dirección General',
    ],
  });

  const [formData, setFormData] = useState<WorkflowData>(getSampleData());

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
    onClose();
  };

  if (!isOpen) return null;

  const tabs = [
    { id: 'basic', name: 'Información Básica', icon: FileText },
    { id: 'requirements', name: 'Requisitos', icon: Building },
    { id: 'conditions', name: 'Condiciones', icon: Scale },
    { id: 'dependencies', name: 'Dependencias', icon: Settings },
    { id: 'approvals', name: 'Aprobaciones', icon: Users },
  ];

  const documentTypes = [
    { value: 'permit', label: 'Permiso/Licencia' },
    { value: 'certificate', label: 'Certificado' },
    { value: 'authorization', label: 'Autorización' },
    { value: 'registration', label: 'Registro' },
    { value: 'notification', label: 'Notificación' },
    { value: 'inspection', label: 'Inspección' },
  ];

  const conditionTypes = [
    { value: 'property_size', label: 'Tamaño de Propiedad (m²)' },
    { value: 'activity_surface', label: 'Superficie de Actividad (m²)' },
    { value: 'applicant_type', label: 'Tipo de Solicitante' },
    { value: 'person_type', label: 'Tipo de Persona' },
    { value: 'alcohol_sales', label: 'Venta de Alcohol' },
    { value: 'activity_type', label: 'Tipo de Actividad' },
  ];

  const operators = [
    { value: '>', label: 'Mayor que' },
    { value: '<', label: 'Menor que' },
    { value: '=', label: 'Igual a' },
    { value: '>=', label: 'Mayor o igual' },
    { value: '<=', label: 'Menor o igual' },
    { value: '!=', label: 'Diferente de' },
    { value: 'includes', label: 'Incluye' },
    { value: 'excludes', label: 'Excluye' },
  ];

  const departments = [
    'Licencias de Construcción',
    'Obras Públicas',
    'Desarrollo Urbano',
    'Protección Civil',
    'Medio Ambiente',
    'Atención Ciudadana',
    'Dirección General',
  ];

  const fileTypes = [
    { value: 'document', label: 'Documento (PDF o imagen)' },
    { value: 'form', label: 'Formulario a llenar' },
    { value: 'certificate', label: 'Certificado/Constancia' },
    { value: 'identification', label: 'Identificación oficial' },
    { value: 'proof_address', label: 'Comprobante de domicilio' },
    { value: 'property_deed', label: 'Escritura de propiedad' },
    { value: 'technical_drawing', label: 'Plano técnico' },
    { value: 'photograph', label: 'Fotografía' },
    { value: 'payment_receipt', label: 'Comprobante de pago' },
    { value: 'inspection_report', label: 'Reporte de inspección' },
  ];

  const addRequirement = () => {
    const newRequirement: WorkflowRequirement = {
      id: Date.now().toString(),
      title: '',
      description: '',
      mandatory: true,
      departmentIssued: false,
      conditionalLogic: [],
    };
    setFormData({
      ...formData,
      requirements: [...(formData.requirements || []), newRequirement],
    });
  };

  const addCondition = () => {
    const newCondition: WorkflowCondition = {
      id: Date.now().toString(),
      type: 'property_size',
      operator: '>',
      value: '',
      action: 'require',
    };
    setFormData({
      ...formData,
      conditions: [...(formData.conditions || []), newCondition],
    });
  };

  const addDependency = () => {
    const newDependency: WorkflowDependency = {
      id: Date.now().toString(),
      dependsOn: '',
      condition: 'approved',
      description: '',
    };
    setFormData({
      ...formData,
      dependencies: [...(formData.dependencies || []), newDependency],
    });
  };

  const addApproval = () => {
    const newApproval: WorkflowApproval = {
      id: Date.now().toString(),
      stepNumber: (formData.approvals?.length || 0) + 1,
      department: departments[0],
      role: 'reviewer',
      required: true,
      parallelApproval: false,
      isBlocking: true,
      fileType: 'document',
      legalFoundation: '',
      isExternalDepartment: false,
      estimatedDays: 1,
    };
    setFormData({
      ...formData,
      approvals: [...(formData.approvals || []), newApproval],
    });
  };

  const removeItem = (
    type: 'requirements' | 'conditions' | 'dependencies' | 'approvals',
    id: string
  ) => {
    setFormData({
      ...formData,
      [type]: formData[type]?.filter(item => item.id !== id) || [],
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 className="text-xl font-semibold text-gray-900">
            {workflow ? 'Editar Workflow' : 'Nuevo Workflow'}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-500"
          >
            <X size={24} />
          </button>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon size={16} />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-180px)]">
          <form onSubmit={handleSubmit} className="p-6">
            {/* Basic Information Tab */}
            {activeTab === 'basic' && (
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nombre del Workflow
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={e =>
                        setFormData({ ...formData, name: e.target.value })
                      }
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tipo de Documento/Información
                    </label>
                    <select
                      value={formData.documentType}
                      onChange={e =>
                        setFormData({
                          ...formData,
                          documentType: e.target.value,
                        })
                      }
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {documentTypes.map(doc => (
                        <option key={doc.value} value={doc.value}>
                          {doc.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descripción Detallada
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={e =>
                      setFormData({ ...formData, description: e.target.value })
                    }
                    rows={4}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Describe el propósito y alcance del workflow..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fundamento Legal
                  </label>
                  <textarea
                    value={formData.legalFoundation}
                    onChange={e =>
                      setFormData({
                        ...formData,
                        legalFoundation: e.target.value,
                      })
                    }
                    rows={3}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Artículo, reglamento o ley que sustenta este proceso..."
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tipo de Proceso
                    </label>
                    <select
                      value={formData.type}
                      onChange={e =>
                        setFormData({ ...formData, type: e.target.value })
                      }
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="construction">Construcción</option>
                      <option value="commercial">Comercial</option>
                      <option value="land_use">Uso de Suelo</option>
                      <option value="environmental">Ambiental</option>
                      <option value="social">Social</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Pasos del Proceso
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={formData.steps}
                      onChange={e =>
                        setFormData({
                          ...formData,
                          steps: parseInt(e.target.value),
                        })
                      }
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Días Promedio
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={formData.avgDays}
                      onChange={e =>
                        setFormData({
                          ...formData,
                          avgDays: parseInt(e.target.value),
                        })
                      }
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="active"
                    checked={formData.active}
                    onChange={e =>
                      setFormData({ ...formData, active: e.target.checked })
                    }
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label
                    htmlFor="active"
                    className="ml-2 block text-sm text-gray-900"
                  >
                    Workflow Activo
                  </label>
                </div>
              </div>
            )}

            {/* Requirements Tab */}
            {activeTab === 'requirements' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-medium text-gray-900">
                    Requisitos del Workflow
                  </h4>
                  <button
                    type="button"
                    onClick={addRequirement}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    <Plus size={16} />
                    Agregar Requisito
                  </button>
                </div>

                {formData.requirements?.map((requirement, index) => (
                  <div
                    key={requirement.id}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h5 className="font-medium text-gray-900">
                        Requisito #{index + 1}
                      </h5>
                      <button
                        type="button"
                        onClick={() =>
                          removeItem('requirements', requirement.id)
                        }
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>

                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Título del Requisito
                        </label>
                        <input
                          type="text"
                          value={requirement.title}
                          onChange={e => {
                            const updated = formData.requirements?.map(req =>
                              req.id === requirement.id
                                ? { ...req, title: e.target.value }
                                : req
                            );
                            setFormData({ ...formData, requirements: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Ej: Identificación oficial vigente"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Descripción Detallada
                        </label>
                        <textarea
                          value={requirement.description}
                          onChange={e => {
                            const updated = formData.requirements?.map(req =>
                              req.id === requirement.id
                                ? { ...req, description: e.target.value }
                                : req
                            );
                            setFormData({ ...formData, requirements: updated });
                          }}
                          rows={3}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Describe qué documentos específicos se necesitan, formato, etc."
                        />
                      </div>

                      <div className="flex items-center gap-6">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={requirement.mandatory}
                            onChange={e => {
                              const updated = formData.requirements?.map(req =>
                                req.id === requirement.id
                                  ? { ...req, mandatory: e.target.checked }
                                  : req
                              );
                              setFormData({
                                ...formData,
                                requirements: updated,
                              });
                            }}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">
                            Obligatorio
                          </span>
                        </label>

                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={requirement.departmentIssued}
                            onChange={e => {
                              const updated = formData.requirements?.map(req =>
                                req.id === requirement.id
                                  ? {
                                      ...req,
                                      departmentIssued: e.target.checked,
                                    }
                                  : req
                              );
                              setFormData({
                                ...formData,
                                requirements: updated,
                              });
                            }}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">
                            Emitido por la dependencia
                          </span>
                        </label>
                      </div>
                    </div>
                  </div>
                ))}

                {(!formData.requirements ||
                  formData.requirements.length === 0) && (
                  <div className="text-center py-8 text-gray-500">
                    <FileText
                      size={48}
                      className="mx-auto mb-4 text-gray-300"
                    />
                    <p>No hay requisitos definidos para este workflow</p>
                    <p className="text-sm">
                      Haz clic en "Agregar Requisito" para comenzar
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Conditions Tab */}
            {activeTab === 'conditions' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">
                      Condiciones del Workflow
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Define reglas que afectan los requisitos basadas en
                      características del solicitante o propiedad
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={addCondition}
                    className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    <Plus size={16} />
                    Agregar Condición
                  </button>
                </div>

                {formData.conditions?.map((condition, index) => (
                  <div
                    key={condition.id}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h5 className="font-medium text-gray-900">
                        Condición #{index + 1}
                      </h5>
                      <button
                        type="button"
                        onClick={() => removeItem('conditions', condition.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>

                    <div className="grid grid-cols-4 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Campo
                        </label>
                        <select
                          value={condition.type}
                          onChange={e => {
                            const updated = formData.conditions?.map(cond =>
                              cond.id === condition.id
                                ? { ...cond, type: e.target.value as any }
                                : cond
                            );
                            setFormData({ ...formData, conditions: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {conditionTypes.map(type => (
                            <option key={type.value} value={type.value}>
                              {type.label}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Operador
                        </label>
                        <select
                          value={condition.operator}
                          onChange={e => {
                            const updated = formData.conditions?.map(cond =>
                              cond.id === condition.id
                                ? { ...cond, operator: e.target.value as any }
                                : cond
                            );
                            setFormData({ ...formData, conditions: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {operators.map(op => (
                            <option key={op.value} value={op.value}>
                              {op.label}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Valor
                        </label>
                        <input
                          type="text"
                          value={condition.value}
                          onChange={e => {
                            const updated = formData.conditions?.map(cond =>
                              cond.id === condition.id
                                ? { ...cond, value: e.target.value }
                                : cond
                            );
                            setFormData({ ...formData, conditions: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Valor o texto"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Acción
                        </label>
                        <select
                          value={condition.action}
                          onChange={e => {
                            const updated = formData.conditions?.map(cond =>
                              cond.id === condition.id
                                ? { ...cond, action: e.target.value as any }
                                : cond
                            );
                            setFormData({ ...formData, conditions: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="require">Requerir</option>
                          <option value="exclude">Excluir</option>
                          <option value="modify">Modificar</option>
                        </select>
                      </div>
                    </div>
                  </div>
                ))}

                {(!formData.conditions || formData.conditions.length === 0) && (
                  <div className="text-center py-8 text-gray-500">
                    <Scale size={48} className="mx-auto mb-4 text-gray-300" />
                    <p>No hay condiciones definidas para este workflow</p>
                    <p className="text-sm">
                      Las condiciones permiten hacer el proceso dinámico basado
                      en características específicas
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Dependencies Tab */}
            {activeTab === 'dependencies' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">
                      Dependencias
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Define qué otros workflows deben completarse antes de este
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={addDependency}
                    className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                  >
                    <Plus size={16} />
                    Agregar Dependencia
                  </button>
                </div>

                {formData.dependencies?.map((dependency, index) => (
                  <div
                    key={dependency.id}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h5 className="font-medium text-gray-900">
                        Dependencia #{index + 1}
                      </h5>
                      <button
                        type="button"
                        onClick={() =>
                          removeItem('dependencies', dependency.id)
                        }
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Workflow Dependiente
                        </label>
                        <input
                          type="text"
                          value={dependency.dependsOn}
                          onChange={e => {
                            const updated = formData.dependencies?.map(dep =>
                              dep.id === dependency.id
                                ? { ...dep, dependsOn: e.target.value }
                                : dep
                            );
                            setFormData({ ...formData, dependencies: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="ID o nombre del workflow"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Condición
                        </label>
                        <select
                          value={dependency.condition}
                          onChange={e => {
                            const updated = formData.dependencies?.map(dep =>
                              dep.id === dependency.id
                                ? { ...dep, condition: e.target.value as any }
                                : dep
                            );
                            setFormData({ ...formData, dependencies: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="approved">Aprobado</option>
                          <option value="rejected">Rechazado</option>
                          <option value="completed">Completado</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Descripción
                        </label>
                        <input
                          type="text"
                          value={dependency.description}
                          onChange={e => {
                            const updated = formData.dependencies?.map(dep =>
                              dep.id === dependency.id
                                ? { ...dep, description: e.target.value }
                                : dep
                            );
                            setFormData({ ...formData, dependencies: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Razón de la dependencia"
                        />
                      </div>
                    </div>
                  </div>
                ))}

                {(!formData.dependencies ||
                  formData.dependencies.length === 0) && (
                  <div className="text-center py-8 text-gray-500">
                    <Settings
                      size={48}
                      className="mx-auto mb-4 text-gray-300"
                    />
                    <p>No hay dependencias definidas para este workflow</p>
                    <p className="text-sm">
                      Las dependencias aseguran que ciertos procesos se
                      completen en orden
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Approvals Tab */}
            {activeTab === 'approvals' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">
                      Flujo de Aprobaciones
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Define los pasos de aprobación y los departamentos
                      involucrados
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={addApproval}
                    className="flex items-center gap-2 px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700"
                  >
                    <Plus size={16} />
                    Agregar Paso de Aprobación
                  </button>
                </div>

                {formData.approvals?.map((approval, index) => (
                  <div
                    key={approval.id}
                    className="border border-gray-200 rounded-lg p-6"
                  >
                    <div className="flex items-center justify-between mb-6">
                      <h5 className="font-medium text-gray-900 text-lg">
                        Paso #{approval.stepNumber}
                      </h5>
                      <button
                        type="button"
                        onClick={() => removeItem('approvals', approval.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>

                    {/* Información básica del paso */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Tipo de Archivo/Documento
                        </label>
                        <select
                          value={approval.fileType}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? { ...app, fileType: e.target.value }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {fileTypes.map(type => (
                            <option key={type.value} value={type.value}>
                              {type.label}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Departamento Responsable
                        </label>
                        <select
                          value={approval.department}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? { ...app, department: e.target.value }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {departments.map(dept => (
                            <option key={dept} value={dept}>
                              {dept}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {/* Fundamento legal */}
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Fundamento Legal
                      </label>
                      <input
                        type="text"
                        value={approval.legalFoundation}
                        onChange={e => {
                          const updated = formData.approvals?.map(app =>
                            app.id === approval.id
                              ? { ...app, legalFoundation: e.target.value }
                              : app
                          );
                          setFormData({ ...formData, approvals: updated });
                        }}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Artículo, reglamento o ley que sustenta este requisito"
                      />
                    </div>

                    {/* Configuración del paso */}
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Rol Requerido
                        </label>
                        <select
                          value={approval.role}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? { ...app, role: e.target.value }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="reviewer">Revisor</option>
                          <option value="supervisor">Supervisor</option>
                          <option value="director">Director</option>
                          <option value="specialist">Especialista</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Días Estimados
                        </label>
                        <input
                          type="number"
                          min="1"
                          value={approval.estimatedDays}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? {
                                    ...app,
                                    estimatedDays: parseInt(e.target.value),
                                  }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>

                    {/* Opciones del paso */}
                    <div className="flex flex-wrap items-center gap-6">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={approval.required}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? { ...app, required: e.target.checked }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">
                          Obligatorio
                        </span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={approval.isBlocking}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? { ...app, isBlocking: e.target.checked }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">
                          Paso Bloqueante
                        </span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={approval.parallelApproval}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? { ...app, parallelApproval: e.target.checked }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">
                          Aprobación Paralela
                        </span>
                      </label>

                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={approval.isExternalDepartment}
                          onChange={e => {
                            const updated = formData.approvals?.map(app =>
                              app.id === approval.id
                                ? {
                                    ...app,
                                    isExternalDepartment: e.target.checked,
                                  }
                                : app
                            );
                            setFormData({ ...formData, approvals: updated });
                          }}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">
                          Dependencia Externa
                        </span>
                      </label>
                    </div>
                  </div>
                ))}

                {(!formData.approvals || formData.approvals.length === 0) && (
                  <div className="text-center py-8 text-gray-500">
                    <Users size={48} className="mx-auto mb-4 text-gray-300" />
                    <p>No hay pasos de aprobación definidos</p>
                    <p className="text-sm">
                      Define quién debe aprobar cada paso del proceso
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Footer */}
            <div className="flex justify-end gap-3 pt-6 border-t border-gray-200 mt-8">
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Guardar Workflow
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
