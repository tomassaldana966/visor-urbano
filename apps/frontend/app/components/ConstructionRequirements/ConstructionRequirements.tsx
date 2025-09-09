import React from 'react';
import { FileText, Building, AlertCircle } from 'lucide-react';

export interface ConstructionRequirement {
  title: string;
  description: string;
  department_issued: boolean;
}

interface ConstructionRequirementsProps {
  requirements: ConstructionRequirement[];
  folio: string;
  municipalityName: string;
  address: string;
  interestedParty: string;
}

export function ConstructionRequirementsDisplay({
  requirements,
  folio,
  municipalityName,
  address,
  interestedParty,
}: ConstructionRequirementsProps) {
  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="border-b border-gray-200 pb-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-orange-100 rounded-lg">
            <Building className="w-6 h-6 text-orange-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Requisitos para Licencia de Construcción
            </h1>
            <p className="text-gray-600">Municipio de {municipalityName}</p>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Folio:</span>
              <span className="ml-2 font-mono bg-orange-100 px-2 py-1 rounded">
                {folio}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Interesado:</span>
              <span className="ml-2">{interestedParty}</span>
            </div>
            <div className="md:col-span-2">
              <span className="font-medium text-gray-700">
                Domicilio del predio:
              </span>
              <span className="ml-2">{address}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Requirements List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            Lista de Requisitos ({requirements.length})
          </h2>
          <div className="text-sm text-gray-500">
            {requirements.filter(req => req.department_issued).length} expedidos
            por el municipio
          </div>
        </div>

        <div className="grid gap-4">
          {requirements.map((requirement, index) => (
            <div
              key={`${requirement.title}-${index}`}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-semibold text-orange-700">
                      {index + 1}
                    </span>
                  </div>
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-medium text-gray-900">
                      {requirement.title}
                    </h3>
                    {requirement.department_issued && (
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
                        <Building className="w-3 h-3" />
                        Municipio
                      </span>
                    )}
                  </div>

                  <p className="text-gray-600 text-sm leading-relaxed">
                    {requirement.description}
                  </p>
                </div>

                <div className="flex-shrink-0">
                  <FileText className="w-5 h-5 text-gray-400" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Information */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <h4 className="font-medium text-amber-800 mb-1">
                Información Importante
              </h4>
              <ul className="text-amber-700 space-y-1">
                <li>
                  • Los requisitos pueden variar según el tipo y magnitud del
                  proyecto
                </li>
                <li>
                  • Algunos documentos requieren firma de perito responsable
                  autorizado
                </li>
                <li>
                  • Es recomendable verificar requisitos adicionales en
                  ventanilla
                </li>
                <li>
                  • Los documentos expedidos por el municipio tienen vigencia
                  limitada
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-4 text-center text-sm text-gray-500">
          Documento generado el{' '}
          {new Date().toLocaleDateString('es-MX', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          })}{' '}
          • Municipio de {municipalityName}
        </div>
      </div>
    </div>
  );
}

// Hook para usar en el contexto de PropertyInfo
export function useConstructionRequirements() {
  const [requirements, setRequirements] = React.useState<
    ConstructionRequirement[]
  >([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const generateRequirements = React.useCallback(
    async (constructionData: {
      folio: string;
      municipality_id: number;
      address: string;
      interested_party: string;
    }) => {
      setLoading(true);
      setError(null);

      try {
        // Esta función se conectaría con el backend para obtener los requisitos específicos
        // Por ahora, simulamos la respuesta
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Los requisitos vendrían del backend después de la implementación completa
        const mockRequirements: ConstructionRequirement[] = [
          {
            title: 'Identificación oficial del propietario',
            description:
              'Presentar identificación oficial vigente (credencial de elector, pasaporte o cédula profesional).',
            department_issued: false,
          },
          {
            title: 'Licencia de uso de suelo',
            description:
              'Licencia de uso de suelo vigente o dictamen de uso de suelo favorable.',
            department_issued: true,
          },
          // ... más requisitos serían cargados desde el backend
        ];

        setRequirements(mockRequirements);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Error al generar requisitos'
        );
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    requirements,
    loading,
    error,
    generateRequirements,
  };
}
