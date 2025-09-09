import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@root/app/components/Dialog/Dialog';
import { Button } from '@root/app/components/Button/Button';
import { Badge } from '@root/app/components/Badge/Badge';
import { useTranslation } from 'react-i18next';
import {
  FileText,
  Calendar,
  User,
  MapPin,
  Building,
  Clock,
} from 'lucide-react';
import type { ProcedureData } from '@root/app/types/procedures';

interface ProcedureModalProps {
  isOpen: boolean;
  onClose: () => void;
  procedure: ProcedureData | null;
  onContinue?: (procedure: ProcedureData) => void;
  onViewFiles?: (procedure: ProcedureData) => void;
}

export function ProcedureModal({
  isOpen,
  onClose,
  procedure,
  onContinue,
  onViewFiles,
}: ProcedureModalProps) {
  const { t: tProcedures } = useTranslation('procedures');

  if (!procedure) return null;

  // Helper function to format date
  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return '--';
    try {
      return new Date(dateString).toLocaleDateString('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return '--';
    }
  };

  // Helper function to format address
  const formatAddress = (procedure: ProcedureData) => {
    const parts = [
      procedure.street,
      procedure.exterior_number,
      procedure.interior_number && `Int. ${procedure.interior_number}`,
      procedure.neighborhood,
      procedure.municipality,
      procedure.postal_code,
    ].filter(Boolean);

    return parts.length > 0 ? parts.join(', ') : '--';
  };

  // Helper function to get status badge variant
  const getStatusVariant = (status: string | null | undefined) => {
    switch (status) {
      case 'approved':
        return 'success' as const;
      case 'in_review':
        return 'warning' as const;
      case 'rejected':
        return 'destructive' as const;
      case 'pending_review':
        return 'secondary' as const;
      default:
        return 'secondary' as const;
    }
  };

  // Helper function to get status text
  const getStatusText = (status: string | null | undefined) => {
    switch (status) {
      case 'approved':
        return tProcedures('status.approved');
      case 'in_review':
        return tProcedures('status.inProgress');
      case 'rejected':
        return tProcedures('status.rejected');
      case 'pending_review':
        return tProcedures('status.pending');
      default:
        return tProcedures('status.noStatus');
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText size={20} />
            {tProcedures('modal.title')} - {procedure.folio}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Status Section */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Badge variant={getStatusVariant(procedure.status)}>
                {getStatusText(procedure.status)}
              </Badge>
              {procedure.current_step && (
                <Badge variant="secondary">
                  {tProcedures('modal.step')} {procedure.current_step}
                </Badge>
              )}
            </div>
            {procedure.procedure_type && (
              <Badge variant="secondary">{procedure.procedure_type}</Badge>
            )}
          </div>

          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="font-semibold text-lg flex items-center gap-2">
                <User size={18} />
                {tProcedures('modal.basicInfo')}
              </h3>

              <div className="space-y-2">
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    {tProcedures('modal.folio')}
                  </label>
                  <p className="text-sm">{procedure.folio ?? '--'}</p>
                </div>

                {procedure.official_applicant_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      {tProcedures('modal.applicant')}
                    </label>
                    <p className="text-sm">
                      {procedure.official_applicant_name}
                    </p>
                  </div>
                )}

                {procedure.business_name && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      {tProcedures('modal.businessName')}
                    </label>
                    <p className="text-sm">{procedure.business_name}</p>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-semibold text-lg flex items-center gap-2">
                <MapPin size={18} />
                {tProcedures('modal.location')}
              </h3>

              <div className="space-y-2">
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    {tProcedures('modal.address')}
                  </label>
                  <p className="text-sm">{formatAddress(procedure)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Business Information */}
          {(procedure.scian_code || procedure.scian_description) && (
            <div className="space-y-4">
              <h3 className="font-semibold text-lg flex items-center gap-2">
                <Building size={18} />
                {tProcedures('modal.businessInfo')}
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {procedure.scian_code && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      {tProcedures('modal.scianCode')}
                    </label>
                    <p className="text-sm">{procedure.scian_code}</p>
                  </div>
                )}

                {procedure.scian_description && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      {tProcedures('modal.scianDescription')}
                    </label>
                    <p className="text-sm">{procedure.scian_description}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Dates Section */}
          <div className="space-y-4">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              <Clock size={18} />
              {tProcedures('modal.dates')}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-600">
                  {tProcedures('modal.createdAt')}
                </label>
                <p className="text-sm">{formatDate(procedure.created_at)}</p>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600">
                  {tProcedures('modal.updatedAt')}
                </label>
                <p className="text-sm">{formatDate(procedure.updated_at)}</p>
              </div>

              {procedure.procedure_start_date && (
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    {tProcedures('modal.startDate')}
                  </label>
                  <p className="text-sm">
                    {formatDate(procedure.procedure_start_date)}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t">
            {onContinue && procedure.status === 'in_review' && (
              <Button
                variant="primary"
                onClick={() => onContinue(procedure)}
                className="flex items-center gap-2"
              >
                <Calendar size={16} />
                {tProcedures('actions.continue')}
              </Button>
            )}

            <Button variant="tertiary" onClick={onClose}>
              {tProcedures('modal.close')}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
