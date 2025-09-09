import { Badge } from '../Badge/Badge';
import { Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

interface StatusBadgeProps {
  status?: string | number | null;
  step?: number | null;
  t: any;
}

export function StatusBadge({ status, step, t }: StatusBadgeProps) {
  // Handle string status values (for main procedure status)
  if (typeof status === 'string') {
    switch (status) {
      case 'approved':
        return (
          <Badge variant="success">
            <CheckCircle size={12} className="mr-1" />
            {t('detail.status.approved')}
          </Badge>
        );
      case 'in_review':
        return (
          <Badge variant="warning">
            <Clock size={12} className="mr-1" />
            {t('detail.status.inReview')}
          </Badge>
        );
      case 'rejected':
        return (
          <Badge variant="destructive">
            <XCircle size={12} className="mr-1" />
            {t('detail.status.rejected')}
          </Badge>
        );
      case 'pending_review':
        return (
          <Badge variant="secondary">
            <Clock size={12} className="mr-1" />
            {t('detail.status.pending')}
          </Badge>
        );
      default:
        return (
          <Badge variant="outline">
            <AlertCircle size={12} className="mr-1" />
            {t('detail.status.unknown')}
          </Badge>
        );
    }
  }

  // Handle numeric status values (for step statuses)
  if (status === 1) {
    return (
      <Badge variant="success">
        <CheckCircle size={12} className="mr-1" />
        {t('detail.status.active')}
      </Badge>
    );
  } else if (status === 0) {
    return (
      <Badge variant="secondary">
        <Clock size={12} className="mr-1" />
        {t('detail.status.pending')}
      </Badge>
    );
  } else if (status === -1) {
    return (
      <Badge variant="destructive">
        <XCircle size={12} className="mr-1" />
        {t('detail.status.rejected')}
      </Badge>
    );
  }

  return (
    <Badge variant="outline">
      <AlertCircle size={12} className="mr-1" />
      {t('detail.status.unknown')}
    </Badge>
  );
}
