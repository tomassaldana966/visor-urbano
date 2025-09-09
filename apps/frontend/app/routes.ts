import {
  type RouteConfig,
  index,
  layout,
  route,
} from '@react-router/dev/routes';

export default [
  index('routes/home.tsx'),
  route('about', 'routes/about.tsx'),
  route('change-password', 'routes/forgot.tsx'),
  route('reset-password', 'routes/reset-password.tsx'),
  route('login', 'routes/login.tsx'),
  route('logout', 'routes/logout.tsx'),
  route('map', 'routes/map.tsx'),
  route('register', 'routes/register.tsx'),
  route('licenses', 'routes/licenses.tsx'),
  route('technical-sheet/:uuid', 'routes/technical-sheet.tsx'),
  route(
    'requirements-queries/:folio/requirements/pdf',
    'routes/requirements-pdf.tsx'
  ),
  route('news', 'routes/news/index.tsx'),
  route('news/:year/:month/:slug', 'routes/news/article.tsx'),
  route('news/:id', 'routes/news/legacy.tsx'),
  layout('routes/procedures/layout.tsx', [
    route('procedures', 'routes/procedures/index.tsx'),
    route('procedures/new', 'routes/procedures/new.tsx'),
    route('procedures/:folio/detail', 'routes/procedures/detail.tsx'),
    route('procedures/:folio/edit', 'routes/procedures/edit.tsx'),
    route('procedure-approvals', 'routes/procedure-approvals.tsx'),
    route('notifications', 'routes/notifications.tsx'),
    route('licenses-issued', 'routes/licenses-issued.tsx'),
    route('director/dashboard', 'routes/director/dashboard.tsx'),
    route('director/dependencies', 'routes/director/dependencies.tsx'),
    route('director/impact-map', 'routes/director/impact-map.tsx'),
    route('director/analytics', 'routes/director/analytics.tsx'),
    route('director/users', 'routes/director/users.tsx'),
    route('director/settings', 'routes/director/settings.tsx'),
    route('director/roles', 'routes/director/roles.tsx'),
    route('director/requirements', 'routes/director/requirements.tsx'),
    route('/director/blog', 'routes/director/blog.tsx'),
    route('director/business-types', 'routes/director/business-types.tsx'),
    route('director/municipal-layers', 'routes/director/municipal-layers.tsx'),
    route(
      'director/impact-management',
      'routes/director/impact-management.tsx'
    ),
  ]),
] satisfies RouteConfig;
