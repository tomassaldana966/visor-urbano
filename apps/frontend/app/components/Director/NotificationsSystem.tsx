import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Bell,
  Check,
  X,
  AlertTriangle,
  Info,
  CheckCircle,
  XCircle,
  Clock,
  Users,
  FileText,
  Settings,
} from 'lucide-react';

interface Notification {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  category: 'system' | 'permits' | 'users' | 'deadlines';
  priority: 'low' | 'medium' | 'high' | 'critical';
  actionUrl?: string;
  actionText?: string;
}

interface NotificationSystemProps {
  isOpen: boolean;
  onClose: () => void;
}

export function NotificationsSystem({
  isOpen,
  onClose,
}: NotificationSystemProps) {
  const { t } = useTranslation('director');
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [filter, setFilter] = useState<
    'all' | 'unread' | 'system' | 'permits' | 'users' | 'deadlines'
  >('all');
  const [realTimeEnabled, setRealTimeEnabled] = useState(true);

  // Mock notifications data
  useEffect(() => {
    const mockNotifications: Notification[] = [
      {
        id: '1',
        type: 'warning',
        title: 'Licencia próxima a vencer',
        message: 'La licencia de construcción PER-2024-001234 vence en 3 días',
        timestamp: new Date(Date.now() - 10 * 60 * 1000),
        read: false,
        category: 'deadlines',
        priority: 'high',
        actionUrl: '/director/reviews',
        actionText: 'Revisar',
      },
      {
        id: '2',
        type: 'success',
        title: 'Nuevo usuario registrado',
        message: 'María González se ha registrado en el sistema',
        timestamp: new Date(Date.now() - 30 * 60 * 1000),
        read: false,
        category: 'users',
        priority: 'low',
      },
      {
        id: '3',
        type: 'error',
        title: 'Error en el sistema',
        message: 'Falla temporal en el servicio de notificaciones por correo',
        timestamp: new Date(Date.now() - 60 * 60 * 1000),
        read: true,
        category: 'system',
        priority: 'critical',
        actionUrl: '/director/settings',
        actionText: 'Configurar',
      },
      {
        id: '4',
        type: 'info',
        title: 'Actualización programada',
        message:
          'Mantenimiento del sistema programado para mañana a las 2:00 AM',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
        read: true,
        category: 'system',
        priority: 'medium',
      },
      {
        id: '5',
        type: 'warning',
        title: 'Múltiples solicitudes pendientes',
        message: '15 solicitudes han estado pendientes por más de 10 días',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000),
        read: false,
        category: 'permits',
        priority: 'high',
        actionUrl: '/director/approvals',
        actionText: 'Ver Solicitudes',
      },
    ];
    setNotifications(mockNotifications);
  }, []);

  // Simulate real-time notifications
  useEffect(() => {
    if (!realTimeEnabled) return;

    const interval = setInterval(() => {
      const newNotification: Notification = {
        id: Date.now().toString(),
        type: Math.random() > 0.5 ? 'info' : 'warning',
        title: 'Nueva notificación',
        message: `Notificación en tiempo real - ${new Date().toLocaleTimeString()}`,
        timestamp: new Date(),
        read: false,
        category: 'system',
        priority: 'low',
      };

      setNotifications(prev => [newNotification, ...prev.slice(0, 19)]); // Keep only 20 most recent
    }, 30000); // Every 30 seconds

    return () => clearInterval(interval);
  }, [realTimeEnabled]);

  const getIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="text-green-500" size={20} />;
      case 'warning':
        return <AlertTriangle className="text-yellow-500" size={20} />;
      case 'error':
        return <XCircle className="text-red-500" size={20} />;
      case 'info':
        return <Info className="text-blue-500" size={20} />;
    }
  };

  const getCategoryIcon = (category: Notification['category']) => {
    switch (category) {
      case 'system':
        return <Settings size={16} />;
      case 'permits':
        return <FileText size={16} />;
      case 'users':
        return <Users size={16} />;
      case 'deadlines':
        return <Clock size={16} />;
    }
  };

  const getPriorityColor = (priority: Notification['priority']) => {
    switch (priority) {
      case 'critical':
        return 'border-l-red-500 bg-red-50';
      case 'high':
        return 'border-l-orange-500 bg-orange-50';
      case 'medium':
        return 'border-l-yellow-500 bg-yellow-50';
      case 'low':
        return 'border-l-blue-500 bg-blue-50';
    }
  };

  const formatTime = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Ahora';
    if (minutes < 60) return `Hace ${minutes}m`;
    if (hours < 24) return `Hace ${hours}h`;
    return `Hace ${days}d`;
  };

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(notif => (notif.id === id ? { ...notif, read: true } : notif))
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(notif => ({ ...notif, read: true })));
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  };

  const filteredNotifications = notifications.filter(notif => {
    if (filter === 'all') return true;
    if (filter === 'unread') return !notif.read;
    return notif.category === filter;
  });

  const unreadCount = notifications.filter(n => !n.read).length;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <Bell className="text-blue-600" size={24} />
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Centro de Notificaciones
              </h2>
              <p className="text-sm text-gray-600">
                {unreadCount > 0
                  ? `${unreadCount} notificaciones sin leer`
                  : 'Todas las notificaciones leídas'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Marcar todas como leídas
              </button>
            )}
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={realTimeEnabled}
                onChange={e => setRealTimeEnabled(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              Tiempo real
            </label>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <X size={24} />
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-medium text-gray-700">
              Filtrar por:
            </span>
            {[
              { key: 'all', label: 'Todas', icon: null },
              { key: 'unread', label: 'Sin leer', icon: null },
              { key: 'system', label: 'Sistema', icon: Settings },
              { key: 'permits', label: 'Permisos', icon: FileText },
              { key: 'users', label: 'Usuarios', icon: Users },
              { key: 'deadlines', label: 'Vencimientos', icon: Clock },
            ].map(filterOption => (
              <button
                key={filterOption.key}
                onClick={() => setFilter(filterOption.key as any)}
                className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
                  filter === filterOption.key
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-300'
                }`}
              >
                {filterOption.icon && <filterOption.icon size={14} />}
                {filterOption.label}
              </button>
            ))}
          </div>
        </div>

        {/* Notifications List */}
        <div className="flex-1 overflow-y-auto max-h-96">
          {filteredNotifications.length === 0 ? (
            <div className="text-center py-12">
              <Bell className="mx-auto text-gray-400 mb-4" size={48} />
              <h3 className="text-gray-500 font-medium">
                No hay notificaciones
              </h3>
              <p className="text-gray-400 text-sm">
                No tienes notificaciones{' '}
                {filter !== 'all' ? `de ${filter}` : ''}
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredNotifications.map(notification => (
                <div
                  key={notification.id}
                  className={`p-4 border-l-4 ${getPriorityColor(notification.priority)} ${
                    !notification.read ? 'bg-white' : 'bg-gray-50'
                  } hover:bg-gray-100 transition-colors`}
                >
                  <div className="flex items-start gap-3">
                    {getIcon(notification.type)}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h4
                          className={`font-medium ${!notification.read ? 'text-gray-900' : 'text-gray-700'}`}
                        >
                          {notification.title}
                        </h4>
                        {!notification.read && (
                          <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                        )}
                        <div className="flex items-center gap-1 text-gray-400">
                          {getCategoryIcon(notification.category)}
                          <span className="text-xs uppercase">
                            {notification.category}
                          </span>
                        </div>
                      </div>
                      <p
                        className={`text-sm ${!notification.read ? 'text-gray-800' : 'text-gray-600'}`}
                      >
                        {notification.message}
                      </p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-xs text-gray-500">
                          {formatTime(notification.timestamp)}
                        </span>
                        <div className="flex items-center gap-2">
                          {notification.actionUrl && (
                            <button className="text-xs text-blue-600 hover:text-blue-800 font-medium">
                              {notification.actionText || 'Ver detalles'}
                            </button>
                          )}
                          {!notification.read && (
                            <button
                              onClick={() => markAsRead(notification.id)}
                              className="text-xs text-gray-500 hover:text-gray-700"
                            >
                              <Check size={14} />
                            </button>
                          )}
                          <button
                            onClick={() => deleteNotification(notification.id)}
                            className="text-xs text-gray-500 hover:text-red-600"
                          >
                            <X size={14} />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 bg-gray-50 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Mostrando {filteredNotifications.length} de {notifications.length}{' '}
            notificaciones
          </div>
          <div className="flex items-center gap-3">
            <button className="text-sm text-gray-600 hover:text-gray-800">
              Configurar notificaciones
            </button>
            <button className="text-sm text-red-600 hover:text-red-800">
              Eliminar todas
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Hook for notifications
export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const count = notifications.filter(n => !n.read).length;
    setUnreadCount(count);
  }, [notifications]);

  const addNotification = (
    notification: Omit<Notification, 'id' | 'timestamp' | 'read'>
  ) => {
    const newNotification: Notification = {
      ...notification,
      id: Date.now().toString(),
      timestamp: new Date(),
      read: false,
    };
    setNotifications(prev => [newNotification, ...prev]);
  };

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(notif => (notif.id === id ? { ...notif, read: true } : notif))
    );
  };

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  };

  return {
    notifications,
    unreadCount,
    addNotification,
    markAsRead,
    removeNotification,
  };
}
