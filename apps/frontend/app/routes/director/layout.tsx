import { useState } from 'react';
import { Outlet, useLoaderData, Link, useLocation } from 'react-router';
import type { LoaderFunctionArgs } from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireAuth } from '../../utils/auth/auth.server';
import {
  checkDirectorPermissions,
  getMunicipalityName,
} from '../../utils/auth/director';
import {
  NotificationsSystem,
  useNotifications,
} from '../../components/Director/NotificationsSystem';
import {
  BarChart3,
  CheckSquare,
  FileText,
  Home,
  Settings,
  Users,
  Bell,
  LogOut,
  BookOpen,
} from 'lucide-react';

export const handle = {
  breadcrumb: 'nav:director',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);

  // Validar que el usuario tenga permisos de Director
  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  return {
    user,
    municipalityName: getMunicipalityName(user),
  };
}

const getNavigationItems = (t: any) => [
  {
    name: t('navigation.dashboard'),
    href: '/director/dashboard',
    icon: Home,
    badge: null,
  },
  {
    name: t('navigation.reviews'),
    href: '/director/reviews',
    icon: FileText,
    badge: '12', // Este número vendría de una API en implementación real
  },
  {
    name: t('navigation.approvals'),
    href: '/director/approvals',
    icon: CheckSquare,
    badge: '5',
  },
  {
    name: t('navigation.analytics'),
    href: '/director/analytics',
    icon: BarChart3,
    badge: null,
  },
  {
    name: t('navigation.users'),
    href: '/director/users',
    icon: Users,
    badge: null,
  },
  {
    name: t('navigation.blog'),
    href: '/director/blog',
    icon: BookOpen,
    badge: null,
  },
  {
    name: t('navigation.settings'),
    href: '/director/settings',
    icon: Settings,
    badge: null,
  },
];

export default function DirectorLayout() {
  const { t } = useTranslation('director');
  const { user, municipalityName } = useLoaderData<typeof loader>();
  const location = useLocation();
  const [showNotifications, setShowNotifications] = useState(false);
  const { unreadCount } = useNotifications();

  const navigationItems = getNavigationItems(t);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header del Director */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link to="/">
                <img
                  src="/logos/visor-urbano.svg"
                  alt="Visor Urbano"
                  className="h-8 w-auto"
                />
              </Link>
              <div className="border-l border-gray-300 pl-4">
                <h1 className="text-xl font-semibold text-gray-900">
                  {t('title')}
                </h1>
                <p className="text-sm text-gray-600">{municipalityName}</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notificaciones */}
              <button
                onClick={() => setShowNotifications(true)}
                className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Bell className="h-5 w-5" />
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </button>

              {/* Información del usuario */}
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">
                    {user.name}
                  </p>
                  <p className="text-xs text-gray-600">{user.role_name}</p>
                </div>
                <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-white">
                    {user.name.charAt(0).toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Logout */}
              <Link
                to="/logout"
                className="p-2 text-gray-600 hover:text-red-600 hover:bg-gray-100 rounded-lg transition-colors"
                title={t('common.logout')}
              >
                <LogOut className="h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Layout principal con sidebar y contenido */}
      <div className="flex">
        {/* Sidebar de navegación */}
        <nav className="w-64 bg-white shadow-sm h-screen sticky top-0 border-r border-gray-200">
          <div className="p-4">
            <div className="space-y-1">
              {navigationItems.map(item => {
                const isActive = location.pathname === item.href;
                const Icon = item.icon;

                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`
                      flex items-center justify-between w-full px-3 py-2 text-sm font-medium rounded-lg transition-colors
                      ${
                        isActive
                          ? 'bg-blue-50 text-blue-700 border border-blue-200'
                          : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }
                    `}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon
                        className={`h-5 w-5 ${isActive ? 'text-blue-700' : 'text-gray-500'}`}
                      />
                      <span>{item.name}</span>
                    </div>

                    {item.badge && (
                      <span
                        className={`
                        px-2 py-1 text-xs font-medium rounded-full
                        ${
                          isActive
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-red-100 text-red-800'
                        }
                      `}
                      >
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>

            {/* Información del municipio */}
            <div className="mt-8 p-3 bg-gray-50 rounded-lg">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                {t('common.municipality')}
              </h3>
              <p className="text-sm font-medium text-gray-900">
                {municipalityName}
              </p>
              {user.municipality_data?.director && (
                <p className="text-xs text-gray-600 mt-1">
                  {t('common.director')}: {user.municipality_data.director}
                </p>
              )}
            </div>
          </div>
        </nav>

        {/* Contenido principal */}
        <main className="flex-1 p-6 bg-gray-50">
          <Outlet />
        </main>
      </div>

      {/* Sistema de Notificaciones */}
      <NotificationsSystem
        isOpen={showNotifications}
        onClose={() => setShowNotifications(false)}
      />
    </div>
  );
}
