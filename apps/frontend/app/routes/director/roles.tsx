import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import { useState } from 'react';
import { useLoaderData, useFetcher } from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireAccessToken, requireAuth } from '../../utils/auth/auth.server';
import { checkDirectorPermissions } from '../../utils/auth/director';
import { DataTable } from '../../components/Director/Charts/DataTable';
import { Input } from '../../components/Input/Input';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/Dialog/Dialog';
import { Shield, Plus, Edit, Trash2, CheckCircle } from 'lucide-react';
import {
  getRoles,
  createRole,
  updateRole,
  deleteRole,
} from '../../utils/api/api.server';
import type { Role, CreateRoleData, UpdateRoleData } from '../../schemas/roles';

export const handle = {
  title: 'director:navigation.roles',
  breadcrumb: 'director:navigation.roles',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  try {
    const session = await import('../../utils/sessions.server').then(
      m => m.getSession
    );
    const sessionData = await session(request.headers.get('Cookie'));
    const authToken = sessionData.get('access_token');

    if (!authToken) {
      throw new Error('No auth token found');
    }

    const roles = await getRoles(authToken);

    return { user, roles };
  } catch (error) {
    console.error('Error fetching roles:', error);
    return { user, roles: [] };
  }
}

export async function action({ request }: ActionFunctionArgs) {
  const user = await requireAuth(request);
  const accessToken = await requireAccessToken(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  const formData = await request.formData();
  const intent = formData.get('intent') as string;

  try {
    switch (intent) {
      case 'create': {
        const roleData: CreateRoleData = {
          name: formData.get('name') as string,
          description: formData.get('description') as string,
        };
        const newRole = await createRole(accessToken, roleData);
        return { success: true, role: newRole };
      }

      case 'update': {
        const id = parseInt(formData.get('id') as string);
        const roleData: UpdateRoleData = {
          name: formData.get('name') as string,
          description: formData.get('description') as string,
        };
        const updatedRole = await updateRole(accessToken, id, roleData);
        return { success: true, role: updatedRole };
      }

      case 'delete': {
        const id = parseInt(formData.get('id') as string);
        await deleteRole(accessToken, id);
        return { success: true };
      }

      default:
        throw new Error('Invalid intent');
    }
  } catch (error) {
    console.error('Action error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export default function DirectorRoles() {
  const { user, roles } = useLoaderData<typeof loader>();
  const { t: tDirector } = useTranslation('director');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState<Role | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState<Role | null>(null);
  const fetcher = useFetcher();

  const handleCreateRole = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    formData.set('intent', 'create');
    fetcher.submit(formData, { method: 'post' });
    setShowAddModal(false);
  };

  const handleUpdateRole = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    formData.set('intent', 'update');
    if (showEditModal) {
      formData.set('id', showEditModal.id.toString());
    }
    fetcher.submit(formData, { method: 'post' });
    setShowEditModal(null);
  };

  const handleDeleteRole = () => {
    if (showDeleteModal) {
      const formData = new FormData();
      formData.set('intent', 'delete');
      formData.set('id', showDeleteModal.id.toString());
      fetcher.submit(formData, { method: 'post' });
      setShowDeleteModal(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const roleColumns = [
    {
      key: 'name' as keyof Role,
      label: tDirector('roles.table.role'),
      sortable: true,
      render: (value: string, role: Role) => (
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
            <Shield className="text-blue-600" size={16} />
          </div>
          <div>
            <div className="font-medium text-gray-900">{value}</div>
            <div className="text-sm text-gray-500">{role.description}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'municipality_id' as keyof Role,
      label: tDirector('roles.table.municipality'),
      render: (value: number) => (
        <span className="text-sm text-gray-600">ID: {value}</span>
      ),
    },
    {
      key: 'created_at' as keyof Role,
      label: tDirector('roles.table.creationDate'),
      sortable: true,
      render: (value: string) => formatDate(value),
    },
    {
      key: 'updated_at' as keyof Role,
      label: tDirector('roles.table.lastUpdate'),
      sortable: true,
      render: (value: string) => formatDate(value),
    },
    {
      key: 'id' as keyof Role,
      label: tDirector('roles.table.actions'),
      render: (_: unknown, role: Role) => (
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEditModal(role)}
            className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded"
            title={tDirector('roles.tooltips.edit')}
          >
            <Edit size={16} />
          </button>
          <button
            onClick={() => setShowDeleteModal(role)}
            className="p-1 text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
            title={tDirector('roles.tooltips.delete')}
          >
            <Trash2 size={16} />
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6 px-5 md:px-8 lg:px-10 py-6 md:py-8 lg:py-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {tDirector('roles.title')}
          </h1>
          <p className="text-gray-600 mt-1">{tDirector('roles.subtitle')}</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus size={16} />
          {tDirector('roles.addRole')}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Shield className="text-blue-600" size={20} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">
                {tDirector('roles.stats.totalRoles')}
              </p>
              <p className="text-2xl font-bold text-gray-900">{roles.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="text-green-600" size={20} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">
                {tDirector('roles.stats.activeRoles')}
              </p>
              <p className="text-2xl font-bold text-gray-900">
                {roles.filter(role => !role.deleted_at).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      <DataTable
        data={[...roles].sort((a, b) => a.name.localeCompare(b.name))}
        columns={roleColumns}
        title={tDirector('roles.table.title')}
        exportable={true}
        searchable={true}
        filterable={true}
      />

      <Dialog open={showAddModal} onOpenChange={setShowAddModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>{tDirector('roles.modals.add.title')}</DialogTitle>
          </DialogHeader>

          <form onSubmit={handleCreateRole} className="space-y-4">
            <Input
              label={tDirector('roles.fields.name')}
              type="text"
              id="name"
              name="name"
              required
              placeholder={tDirector('roles.modals.add.placeholder.name')}
            />

            <div>
              <label
                htmlFor="description"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                {tDirector('roles.fields.description')}
              </label>
              <textarea
                id="description"
                name="description"
                required
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder={tDirector(
                  'roles.modals.add.placeholder.description'
                )}
              />
            </div>

            <DialogFooter className="gap-3 pt-4">
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                {tDirector('roles.modals.add.buttons.cancel')}
              </button>
              <button
                type="submit"
                disabled={fetcher.state === 'submitting'}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {fetcher.state === 'submitting'
                  ? tDirector('roles.modals.add.buttons.creating')
                  : tDirector('roles.modals.add.buttons.create')}
              </button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <Dialog
        open={!!showEditModal}
        onOpenChange={open => !open && setShowEditModal(null)}
      >
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>
              {tDirector('roles.modals.edit.title', {
                name: showEditModal?.name ?? '',
              })}
            </DialogTitle>
          </DialogHeader>

          {showEditModal && (
            <form onSubmit={handleUpdateRole} className="space-y-4">
              <Input
                label={tDirector('roles.fields.name')}
                type="text"
                id="edit-name"
                name="name"
                required
                defaultValue={showEditModal.name}
                placeholder={tDirector('roles.modals.add.placeholder.name')}
              />

              <div>
                <label
                  htmlFor="edit-description"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  {tDirector('roles.fields.description')}
                </label>
                <textarea
                  id="edit-description"
                  name="description"
                  required
                  rows={3}
                  defaultValue={showEditModal.description}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder={tDirector(
                    'roles.modals.add.placeholder.description'
                  )}
                />
              </div>

              <DialogFooter className="gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowEditModal(null)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  {tDirector('roles.modals.edit.buttons.cancel')}
                </button>
                <button
                  type="submit"
                  disabled={fetcher.state === 'submitting'}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {fetcher.state === 'submitting'
                    ? tDirector('roles.modals.edit.buttons.saving')
                    : tDirector('roles.modals.edit.buttons.save')}
                </button>
              </DialogFooter>
            </form>
          )}
        </DialogContent>
      </Dialog>

      <Dialog
        open={!!showDeleteModal}
        onOpenChange={open => !open && setShowDeleteModal(null)}
      >
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle>{tDirector('roles.modals.delete.title')}</DialogTitle>
          </DialogHeader>

          {showDeleteModal && (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                  <Trash2 className="text-red-600" size={20} />
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {tDirector('roles.modals.delete.question', {
                      name: showDeleteModal.name,
                    })}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {tDirector('roles.modals.delete.warning')}
                  </p>
                </div>
              </div>

              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-sm text-red-800">
                  <strong>{tDirector('roles.modals.delete.alertTitle')}</strong>{' '}
                  {tDirector('roles.modals.delete.alert')}
                </p>
              </div>

              <DialogFooter className="gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowDeleteModal(null)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  {tDirector('roles.modals.delete.buttons.cancel')}
                </button>
                <button
                  type="button"
                  onClick={handleDeleteRole}
                  disabled={fetcher.state === 'submitting'}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
                >
                  {fetcher.state === 'submitting'
                    ? tDirector('roles.modals.delete.buttons.deleting')
                    : tDirector('roles.modals.delete.buttons.delete')}
                </button>
              </DialogFooter>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
