import { ChevronRight, House } from 'lucide-react';
import { Link, useMatches, type UIMatch } from 'react-router';
import { useTranslation } from 'react-i18next';

function isBreadcrumb(
  route: UIMatch
): route is UIMatch & { handle: { breadcrumb: string } } {
  return (
    !!route.handle &&
    typeof route.handle === 'object' &&
    'breadcrumb' in route.handle
  );
}

export function Breadcrumbs() {
  const routes = useMatches();
  const { t: tNav } = useTranslation('nav');
  const { t: tDirector } = useTranslation('director');
  const { t: tProcedures } = useTranslation('procedures');
  const { t: tHeader } = useTranslation('header');
  const { t: tProcedureApprovals } = useTranslation('procedureApprovals');

  const breadcrumbs = routes.filter(route => isBreadcrumb(route));

  // Function to translate breadcrumb titles that use namespace:key format
  const getTranslatedBreadcrumb = (breadcrumb: string): string => {
    // Check if breadcrumb has namespace format (namespace:key)
    if (breadcrumb.includes(':')) {
      const [namespace, key] = breadcrumb.split(':', 2);

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
        default:
          return breadcrumb; // Return original if namespace not recognized
      }
    }

    // Return breadcrumb as-is if it doesn't have namespace format
    return breadcrumb;
  };

  return (
    <nav>
      <ul className="flex gap-2">
        {breadcrumbs.map((route, index) => (
          <li key={route.pathname} className="flex items-center">
            {route.pathname === '/' ? (
              <House size={14} />
            ) : (
              <Link to={route.pathname} className="flex gap-2 items-center ">
                {index !== 0 ? <ChevronRight size={14} /> : null}
                <span className="text-xs">
                  {getTranslatedBreadcrumb(route.handle.breadcrumb)}
                </span>
              </Link>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}
