import { Breadcrumbs } from '@root/app/components/Breadcrumbs/Breadcrumbs';
import { Button } from '@root/app/components/Button/Button';
import { LoadingModal } from '@root/app/components/LoadingModal/LoadingModal';
import { BloombergLogo } from '@root/app/components/Logos/Bloomberg';
import { CityLogo } from '@root/app/components/Logos/City';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@root/app/components/Popover/Popover';
import { cn, capitalizeWords } from '@root/app/lib/utils';
import { requireUser } from '@root/app/utils/auth/utils';
import { checkDirectorPermissions } from '@root/app/utils/auth/director';
import type { AuthUser } from '@root/app/utils/auth/auth.server';
import { useMapNavigation } from '@root/app/hooks/useMapNavigation';
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleUserRound,
  FileText,
  LogOut,
  Mail,
  MapPin,
  Plus,
  BarChart3,
  Menu,
  X,
  Languages,
  ShieldCheck,
  Award,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react';
import i18n from '@root/app/i18n';

import {
  Link,
  NavLink,
  Outlet,
  useLoaderData,
  useMatches,
  type LoaderFunctionArgs,
} from 'react-router';

function LanguageSelector({ inverted = false }: { inverted?: boolean }) {
  const { t: tHeader } = useTranslation('header');
  const languages = Object.getOwnPropertyNames(
    tHeader('languages', { returnObjects: true })
  );

  return (
    <Popover>
      <PopoverTrigger asChild>
        <button
          type="button"
          className={`cursor-pointer p-2 rounded-lg ${
            inverted
              ? 'text-white hover:bg-white/10'
              : 'hover:bg-white text-primary'
          }`}
        >
          <Languages
            size={24}
            className={inverted ? 'text-white' : 'text-primary'}
          />
        </button>
      </PopoverTrigger>
      <PopoverContent>
        <ul className="flex flex-col gap-4">
          {languages.map(language => (
            <li key={language}>
              <button
                type="button"
                className="cursor-pointer hover:bg-gray-100 p-2 rounded w-full text-left"
                onClick={() => {
                  i18n.changeLanguage(language);
                }}
              >
                {tHeader(`languages.${language}`)}
              </button>
            </li>
          ))}
        </ul>
      </PopoverContent>
    </Popover>
  );
}

export const handle = {
  title: 'procedures:myProcedures',
  breadcrumb: 'header:menu.home',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const auth = await requireUser(request);
  return { auth };
}

export default function ProceduresLayout() {
  const { t: tHeader, ready: headerReady } = useTranslation('header');
  const { t: tNav, ready: navReady } = useTranslation('nav');
  const { t: tProcedures, ready: proceduresReady } =
    useTranslation('procedures');
  const { t: tDirector, ready: directorReady } = useTranslation('director');
  const { t: tLicenses, ready: licensesReady } = useTranslation('licenses');
  const { t: tProcedureApprovals, ready: procedureApprovalsReady } =
    useTranslation('procedureApprovals');
  const { t: tCommon, ready: commonReady } = useTranslation('common');

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isDesktop, setIsDesktop] = useState(false);

  const { isMapLoading, navigateToMap } = useMapNavigation();

  useEffect(() => {
    const checkIsDesktop = () => {
      const isDesktopSize = window.innerWidth >= 1024;
      setIsDesktop(isDesktopSize);
      // Auto-close mobile menu when switching to desktop
      if (isDesktopSize && isSidebarOpen) {
        setIsSidebarOpen(false);
      }
    };

    // Debounce function to reduce frequency of resize event handling
    const debounce = (func: () => void, wait: number) => {
      let timeout: NodeJS.Timeout;
      return () => {
        clearTimeout(timeout);
        timeout = setTimeout(func, wait);
      };
    };

    checkIsDesktop();
    const debouncedCheckIsDesktop = debounce(checkIsDesktop, 150);
    window.addEventListener('resize', debouncedCheckIsDesktop);
    return () => window.removeEventListener('resize', debouncedCheckIsDesktop);
  }, [isSidebarOpen]);

  // Close sidebar when clicking outside on mobile
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isSidebarOpen && !isDesktop) {
        setIsSidebarOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isSidebarOpen, isDesktop]);

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (!isDesktop && isSidebarOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isSidebarOpen, isDesktop]);

  const loaderData = useLoaderData<typeof loader>();
  const routes = useMatches();

  if (
    !headerReady ||
    !navReady ||
    !proceduresReady ||
    !directorReady ||
    !licensesReady ||
    !procedureApprovalsReady ||
    !commonReady
  ) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{tCommon('loading.translations')}</p>
        </div>
      </div>
    );
  }

  const currentRoute = routes[routes.length - 1] as {
    handle?: { title?: string };
  };

  const rawRouteTitle = currentRoute?.handle?.title;

  const getTranslatedTitle = (
    title: string | undefined
  ): string | undefined => {
    if (!title) return undefined;
    if (title.includes(':')) {
      const [namespace, key] = title.split(':', 2);
      switch (namespace) {
        case 'director':
          return tDirector(key);
        case 'procedures':
          return tProcedures(key);
        case 'procedureApprovals':
          return tProcedureApprovals(key);
        case 'nav':
          return tNav(key);
        case 'header':
          return tHeader(key);
        case 'licenses':
          return tLicenses(key);
        default:
          return title;
      }
    }
    return title;
  };

  const routeTitle = getTranslatedTitle(rawRouteTitle);

  const isProceduresRoute = routes.some(match =>
    match.pathname.includes('procedures')
  );

  const isNewProcedureRoute = routes.some(
    match => match.pathname === '/procedures/new'
  );

  const userForPermissions = {
    id: loaderData.auth.user?.id || 0,
    email: loaderData.auth.user?.email || '',
    name: loaderData.auth.user?.name || '',
    role_name: loaderData.auth.user?.role_name,
    role_id: loaderData.auth.user?.role_id,
  };

  const hasDirectorPermissions = checkDirectorPermissions(userForPermissions);

  const navigationItems = [
    {
      path: '/map',
      label: tNav('map'),
      icon: <MapPin size={isSidebarCollapsed ? 20 : 16} />,
      onClick: navigateToMap,
    },
    {
      path: '/procedures/new',
      label: tNav('newProcedure'),
      icon: <Plus size={isSidebarCollapsed ? 20 : 16} />,
    },
    {
      path: '/procedures',
      label: tNav('myProcedures'),
      icon: <FileText size={isSidebarCollapsed ? 20 : 16} />,
    },
    {
      path: '/notifications',
      label: tNav('notifications'),
      icon: <Mail size={isSidebarCollapsed ? 20 : 16} />,
    },
  ];

  const userRoleId = loaderData.auth.user?.role_id;
  if (userRoleId && userRoleId > 1) {
    navigationItems.push({
      path: '/procedure-approvals',
      label: tNav('procedureApprovals'),
      icon: <ShieldCheck size={isSidebarCollapsed ? 20 : 16} />,
    });
  }

  if (hasDirectorPermissions) {
    navigationItems.push({
      path: '/licenses-issued',
      label: tNav('issuedLicenses'),
      icon: <Award size={isSidebarCollapsed ? 20 : 16} />,
    });
  }
  if (hasDirectorPermissions) {
    navigationItems.push({
      path: '/director/dashboard',
      label: tDirector('navigation.dashboard'),
      icon: <BarChart3 size={isSidebarCollapsed ? 20 : 16} />,
    });
  }

  return (
    <div className="min-h-screen bg-white">
      {!isDesktop && isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
      <aside
        className={cn(
          'bg-white h-screen fixed left-0 top-0 z-50 transition-all duration-300 ease-in-out shadow-lg will-change-transform',
          {
            // Mobile styles
            'lg:hidden': !isDesktop,
            'translate-x-0': !isDesktop && isSidebarOpen,
            '-translate-x-full': !isDesktop && !isSidebarOpen,
            // Desktop styles
            'lg:translate-x-0': isDesktop,
          }
        )}
        style={{
          width: isDesktop
            ? isSidebarCollapsed
              ? '64px'
              : '256px'
            : !isDesktop && isSidebarOpen
              ? '80%'
              : '256px',
        }}
      >
        <nav className="h-full bg-white flex flex-col overflow-hidden">
          <div
            className={cn(
              'bg-zinc-500 flex items-center min-h-[60px] flex-shrink-0 relative',
              isSidebarCollapsed && isDesktop
                ? 'px-2 justify-center'
                : 'px-6 justify-between'
            )}
          >
            <h2
              className={cn(
                'text-white text-sm font-medium tracking-wide transition-all ease-in-out',
                isSidebarCollapsed && isDesktop
                  ? 'opacity-0 scale-95 pointer-events-none duration-200'
                  : 'opacity-100 scale-100 duration-300 delay-200'
              )}
            >
              {tNav('applications')}
            </h2>
            {!isDesktop && (
              <button
                onClick={() => setIsSidebarOpen(false)}
                className="text-white hover:text-gray-300 p-1"
                aria-label="Cerrar menú"
              >
                <X size={20} />
              </button>
            )}
          </div>
          <div className="bg-zinc-600 flex-1 flex flex-col overflow-y-auto">
            <div className="flex-1 px-2 py-4">
              <ul className="flex flex-col gap-1">
                {navigationItems.map(item => (
                  <li key={item.path}>
                    {item.onClick ? (
                      <button
                        onClick={() => {
                          item.onClick();
                          setIsSidebarOpen(false);
                        }}
                        className={cn(
                          'w-full flex items-center text-white text-sm transition-all duration-200 rounded-lg relative group hover:bg-zinc-700',
                          {
                            'p-3 gap-3': !isSidebarCollapsed || !isDesktop,
                            'p-4 justify-center':
                              isSidebarCollapsed && isDesktop,
                          }
                        )}
                      >
                        <div
                          className={cn(
                            'flex items-center justify-center',
                            isSidebarCollapsed && isDesktop
                              ? 'w-6 h-6'
                              : 'w-5 h-5 flex-shrink-0'
                          )}
                        >
                          {item.icon}
                        </div>
                        {(!isSidebarCollapsed || !isDesktop) && (
                          <span className="font-medium truncate">
                            {item.label}
                          </span>
                        )}
                        {isSidebarCollapsed && isDesktop && (
                          <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none">
                            {item.label}
                          </div>
                        )}
                      </button>
                    ) : (
                      <NavLink
                        end
                        className={({ isActive }) => {
                          return cn(
                            'flex items-center text-white text-sm transition-all duration-200 rounded-lg relative group',
                            {
                              'bg-primary shadow-lg': isActive,
                              'hover:bg-zinc-700': !isActive,
                              'p-3 gap-3': !isSidebarCollapsed || !isDesktop,
                              'p-4 justify-center':
                                isSidebarCollapsed && isDesktop,
                            }
                          );
                        }}
                        to={item.path}
                        onClick={() => setIsSidebarOpen(false)}
                      >
                        <div
                          className={cn(
                            'flex items-center justify-center',
                            isSidebarCollapsed && isDesktop
                              ? 'w-6 h-6'
                              : 'w-5 h-5 flex-shrink-0'
                          )}
                        >
                          {item.icon}
                        </div>
                        {(!isSidebarCollapsed || !isDesktop) && (
                          <span className="font-medium truncate">
                            {item.label}
                          </span>
                        )}
                        {isSidebarCollapsed && isDesktop && (
                          <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none">
                            {item.label}
                          </div>
                        )}
                      </NavLink>
                    )}
                  </li>
                ))}
              </ul>
            </div>
            {isDesktop && (
              <div className="p-2 border-t border-zinc-500">
                <button
                  onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
                  className={cn(
                    'w-full flex items-center justify-center text-white hover:bg-zinc-700 rounded-lg transition-colors p-2',
                    isSidebarCollapsed ? 'px-3' : 'gap-2'
                  )}
                  title={
                    isSidebarCollapsed
                      ? tCommon('sidebar.expand')
                      : tCommon('sidebar.collapse')
                  }
                  aria-label={
                    isSidebarCollapsed
                      ? tCommon('sidebar.expand')
                      : tCommon('sidebar.collapse')
                  }
                >
                  {isSidebarCollapsed ? (
                    <ChevronRight size={18} />
                  ) : (
                    <>
                      <ChevronLeft size={16} />
                      <span className="text-xs font-medium">
                        {tCommon('sidebar.collapse')}
                      </span>
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
          <footer className="bg-white border-t border-gray-200 flex-shrink-0">
            <div
              className={cn(
                'flex items-center justify-center py-3',
                isSidebarCollapsed && isDesktop ? 'px-2' : 'px-4'
              )}
            >
              <BloombergLogo
                className={cn(
                  'transition-all duration-300',
                  isSidebarCollapsed && isDesktop ? 'h-6' : 'h-8'
                )}
              />
            </div>
            <div
              className={cn(
                'flex items-center justify-center py-3',
                isSidebarCollapsed && isDesktop ? 'px-2' : 'px-4'
              )}
            >
              <CityLogo />
            </div>
          </footer>
        </nav>
      </aside>
      <div
        className={cn(
          'flex flex-col min-h-screen bg-white transition-all duration-300 ease-in-out',
          {
            'lg:ml-64': isDesktop && !isSidebarCollapsed,
            'lg:ml-16': isDesktop && isSidebarCollapsed,
            'ml-0': !isDesktop,
          }
        )}
      >
        <main className="bg-vu-light-gray flex-1">
          <section className="bg-primary px-6 py-3 text-white relative z-10">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4 min-w-0 flex-1">
                <button
                  onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                  className="lg:hidden p-2 text-white hover:text-gray-200 hover:bg-white/10 rounded-lg flex-shrink-0 transition-colors"
                  aria-label="Abrir menú"
                >
                  <Menu size={24} />
                </button>
                <Link
                  to="/"
                  className="cursor-pointer hover:opacity-90 transition-opacity flex-shrink-0"
                >
                  <img
                    src="/logos/visor-urbano-white.svg"
                    alt="Visor Urbano"
                    className="h-8 w-auto"
                    onError={e => {
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                </Link>
                <div className="flex items-center gap-3 min-w-0 flex-1">
                  <Breadcrumbs />
                  {routeTitle ? (
                    <>
                      <span className="text-white/60">|</span>
                      <h1 className="font-semibold text-lg truncate">
                        {routeTitle}
                      </h1>
                    </>
                  ) : null}
                </div>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                {isNewProcedureRoute ? (
                  <Button variant="secondary" asChild className="ml-2">
                    <Link to="/procedures">
                      <Plus />
                      <span className="hidden sm:inline">
                        {tProcedures('new.form.newTramiteButton')}
                      </span>
                    </Link>
                  </Button>
                ) : isProceduresRoute ? (
                  <Button variant="secondary" asChild className="ml-2">
                    <Link to="/procedures/new">
                      <Plus />
                      <span className="hidden sm:inline">
                        {tProcedures('new.buttonText')}
                      </span>
                    </Link>
                  </Button>
                ) : null}
                <LanguageSelector inverted />
                <Popover>
                  <PopoverTrigger asChild>
                    <button className="flex gap-2 items-center p-2 cursor-pointer hover:bg-white/10 rounded-lg ml-2">
                      <CircleUserRound className="text-white" size={32} />
                      <div className="hidden sm:flex flex-col text-right">
                        <span className="text-sm font-semibold">
                          {loaderData.auth.user?.name ?? '--'}
                        </span>
                        <span className="text-xs text-white/80">
                          {capitalizeWords(
                            loaderData.auth.user?.role_name ?? '--'
                          )}
                        </span>
                      </div>
                      <ChevronDown size={12} />
                    </button>
                  </PopoverTrigger>
                  <PopoverContent>
                    <ul>
                      <li>
                        <Link
                          className="flex gap-2 items-center p-2 hover:bg-vu-light-gray rounded"
                          to="/change-password"
                        >
                          {tHeader('changePassword')}
                        </Link>
                      </li>
                      <li>
                        <Link
                          className="flex gap-2 items-center p-2 hover:bg-vu-light-gray rounded"
                          to="/logout"
                        >
                          <LogOut size={16} /> {tHeader('logout')}
                        </Link>
                      </li>
                    </ul>
                  </PopoverContent>
                </Popover>
              </div>
            </div>
          </section>
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>

      <LoadingModal isOpen={isMapLoading} type="map" />
    </div>
  );
}
