import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '../Dialog/Dialog';
import { Badge } from '../Badge/Badge';
import { Button } from '../Button/Button';
import {
  Bell,
  Calendar,
  FileText,
  User,
  Building,
  Clock,
  CheckCircle,
  AlertTriangle,
  Info,
  XCircle,
  ExternalLink,
} from 'lucide-react';
import { encodeFolio } from '../../utils/folio';

export interface NotificationData {
  id: number;
  folio: string;
  notification_type: number;
  notifying_department: number;
  comment: string;
  creation_date: string;
  notified?: number | null;
  user_id?: number;
  applicant_email: string;
}

interface NotificationModalProps {
  notification: NotificationData | null;
  isOpen: boolean;
  onClose: () => void;
  onMarkAsRead?: (notificationId: number) => void;
}

export function NotificationModal({
  notification,
  isOpen,
  onClose,
  onMarkAsRead,
}: NotificationModalProps) {
  const { t } = useTranslation('notifications');
  const navigate = useNavigate();

  if (!notification) return null;

  // Helper functions that use translations
  const getNotificationTypeLabel = (type: number): string => {
    return t(`types.${type}`, { defaultValue: t('types.default') });
  };

  const getDepartmentName = (dept: number): string => {
    return t(`departments.${dept}`, { defaultValue: t('departments.default') });
  };

  const getNotificationIcon = (type: number) => {
    switch (type) {
      case 1:
        return <Info className="w-5 h-5 text-blue-500" />;
      case 2:
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 3:
        return <Calendar className="w-5 h-5 text-orange-500" />;
      case 4:
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 5:
        return <FileText className="w-5 h-5 text-purple-500" />;
      default:
        return <Bell className="w-5 h-5 text-gray-500" />;
    }
  };

  const getNotificationTypeColor = (
    type: number
  ): 'default' | 'success' | 'warning' | 'destructive' => {
    switch (type) {
      case 2:
        return 'success';
      case 3:
      case 4:
        return 'warning';
      case 6:
        return 'destructive';
      default:
        return 'default';
    }
  };

  const isRead = notification.notified === 1;
  const notificationType = getNotificationTypeLabel(
    notification.notification_type
  );
  const departmentName = getDepartmentName(notification.notifying_department);
  const creationDate = new Date(notification.creation_date);
  const typeColor = getNotificationTypeColor(notification.notification_type);

  const handleMarkAsRead = () => {
    if (!isRead && onMarkAsRead) {
      onMarkAsRead(notification.id);
    }
  };

  const handleViewProcedure = () => {
    // Navigate to procedure detail page using the folio
    navigate(`/procedures/${encodeFolio(notification.folio)}/detail`);
    onClose(); // Close the modal after navigating
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto w-[95vw] sm:w-full">
        <DialogHeader className="pb-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            {getNotificationIcon(notification.notification_type)}
            <div>
              <DialogTitle className="text-xl font-semibold text-gray-900 mb-1">
                {t('modal.title')}
              </DialogTitle>
              <div className="flex items-center gap-2">
                <Badge variant={typeColor} className="text-xs">
                  {notificationType}
                </Badge>
                {!isRead && (
                  <Badge
                    variant="default"
                    className="text-xs bg-blue-100 text-blue-800"
                  >
                    {t('modal.status.unread')}
                  </Badge>
                )}
              </div>
            </div>
          </div>
        </DialogHeader>

        <div className="py-6 space-y-6">
          {/* Main notification message */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <FileText size={16} />
              {t('modal.fields.message')}
            </h3>
            <p className="text-gray-900 leading-relaxed">
              {notification.comment}
            </p>
          </div>

          {/* Notification details grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Folio */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <FileText size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">
                  {t('modal.fields.folio')}
                </span>
              </div>
              <p className="text-lg font-semibold text-primary break-all">
                {notification.folio}
              </p>
            </div>

            {/* Department */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Building size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">
                  {t('modal.fields.department')}
                </span>
              </div>
              <p className="text-gray-900">{departmentName}</p>
            </div>

            {/* Date */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Calendar size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">
                  {t('modal.fields.date')}
                </span>
              </div>
              <p className="text-gray-900">
                {creationDate.toLocaleDateString('es-ES', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>

            {/* Applicant */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <User size={16} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">
                  {t('modal.fields.applicant')}
                </span>
              </div>
              <p className="text-gray-900 break-all text-sm">
                {notification.applicant_email}
              </p>
            </div>
          </div>

          {/* Status information */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <Clock size={16} className="text-gray-500" />
              <span className="text-sm font-medium text-gray-700">
                {t('modal.fields.notificationStatus')}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {isRead ? (
                  <CheckCircle size={20} className="text-green-500" />
                ) : (
                  <Bell size={20} className="text-blue-500" />
                )}
                <span
                  className={`font-medium ${isRead ? 'text-green-700' : 'text-blue-700'}`}
                >
                  {isRead ? t('modal.status.read') : t('modal.status.unread')}
                </span>
              </div>
              {!isRead && (
                <Button
                  onClick={handleMarkAsRead}
                  variant="secondary"
                  className="flex items-center gap-2"
                >
                  <CheckCircle size={16} />
                  {t('modal.actions.markAsRead')}
                </Button>
              )}
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200">
            <Button
              onClick={handleViewProcedure}
              variant="primary"
              className="flex items-center gap-2 flex-1"
            >
              <ExternalLink size={16} />
              {t('modal.actions.viewProcedure')}
            </Button>
            <Button
              onClick={onClose}
              variant="tertiary"
              className="flex-shrink-0"
            >
              {t('modal.actions.close')}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
