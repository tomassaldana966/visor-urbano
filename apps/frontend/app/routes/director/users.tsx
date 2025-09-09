import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import { useState } from 'react';
import { useLoaderData, useFetcher } from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireAuth, requireAccessToken } from '../../utils/auth/auth.server';
import { checkDirectorPermissions } from '../../utils/auth/director';
import { DataTable } from '../../components/Director/Charts/DataTable';
import { Input } from '../../components/Input/Input';
import { Select, Option } from '../../components/Select/Select';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/Dialog/Dialog';
import {
  Users,
  UserPlus,
  Shield,
  Edit,
  Trash2,
  CheckCircle,
  AlertTriangle,
} from 'lucide-react';
import {
  getUsers,
  createUser,
  updateUser,
  deleteUser,
  getRoles,
  getMunicipalities,
} from '../../utils/api/api.server';
import type { User, CreateUserData, UpdateUserData } from '../../schemas/users';
import type { Role } from '../../schemas/roles';
import type { Municipality } from '../../schemas/municipalities';

export const handle = {
  title: 'director:navigation.users',
  breadcrumb: 'director:navigation.users',
};

interface LoaderData {
  user: any;
  users: User[];
  roles: Role[];
  municipalities: Municipality[];
}

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  try {
    const accessToken = await requireAccessToken(request);

    const [users, roles, municipalities] = await Promise.all([
      getUsers(accessToken),
      getRoles(accessToken),
      getMunicipalities(),
    ]);

    return { user, users, roles, municipalities };
  } catch (error) {
    console.error('Error loading user data:', error);
    return { user, users: [], roles: [], municipalities: [] };
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
        const userData: CreateUserData = {
          name: formData.get('name') as string,
          paternal_last_name: formData.get('paternal_last_name') as string,
          maternal_last_name:
            (formData.get('maternal_last_name') as string) || undefined,
          cellphone: formData.get('cellphone') as string,
          email: formData.get('email') as string,
          password: formData.get('password') as string,
          municipality_id: parseInt(formData.get('municipality_id') as string),
          role_id: parseInt(formData.get('role_id') as string),
        };
        const newUser = await createUser(accessToken, userData);
        return { success: true, user: newUser };
      }

      case 'update': {
        const id = parseInt(formData.get('id') as string);
        const userData: UpdateUserData = {
          name: formData.get('name') as string,
          paternal_last_name: formData.get('paternal_last_name') as string,
          maternal_last_name:
            (formData.get('maternal_last_name') as string) || undefined,
          cellphone: formData.get('cellphone') as string,
          email: formData.get('email') as string,
          municipality_id: parseInt(formData.get('municipality_id') as string),
          role_id: parseInt(formData.get('role_id') as string),
        };

        const password = formData.get('password') as string;
        if (password?.trim()) {
          userData.password = password;
        }

        const updatedUser = await updateUser(accessToken, id, userData);
        return { success: true, user: updatedUser };
      }

      case 'delete': {
        const id = parseInt(formData.get('id') as string);
        await deleteUser(accessToken, id);
        return { success: true };
      }

      default:
        throw new Error('Invalid intent');
    }
  } catch (error) {
    console.error('Action error:', error);
    const errorMessage =
      error instanceof Error ? error.message : 'Error desconocido';
    return {
      success: false,
      error: errorMessage,
    };
  }
}

export default function DirectorUsers() {
  const { user, users, roles, municipalities } = useLoaderData<LoaderData>();
  const { t: tDirector } = useTranslation('director');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState<User | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState<User | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const fetcher = useFetcher();

  const filteredUsers = users.filter(user => {
    const matchesSearch =
      !searchTerm ||
      user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesRole = !roleFilter || user.role_name === roleFilter;

    return matchesSearch && matchesRole;
  });

  const handleCreateUser = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    formData.set('intent', 'create');
    fetcher.submit(formData, { method: 'post' });
    setShowAddModal(false);
  };

  const handleUpdateUser = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    formData.set('intent', 'update');
    if (showEditModal) {
      formData.set('id', showEditModal.id.toString());
    }
    fetcher.submit(formData, { method: 'post' });
    setShowEditModal(null);
  };

  const handleDeleteUser = () => {
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
    });
  };

  const getFullName = (user: User) => {
    return `${user.name} ${user.paternal_last_name} ${user.maternal_last_name ?? ''}`.trim();
  };

  const uniqueRoles = Array.from(
    new Set(users.map(u => u.role_name).filter(Boolean))
  );

  const userColumns = [
    {
      key: 'name' as keyof User,
      label: tDirector('users.fields.user'),
      sortable: true,
      render: (value: string, user: User) => (
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
            <span className="text-blue-600 text-sm font-medium">
              {getFullName(user)
                .split(' ')
                .map(n => n[0])
                .join('')
                .slice(0, 2)}
            </span>
          </div>
          <div>
            <div className="font-medium text-gray-900">{getFullName(user)}</div>
            <div className="text-sm text-gray-500">{user.email}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'role_name' as keyof User,
      label: tDirector('users.fields.role'),
      sortable: true,
      render: (value: string) => (
        <span className="inline-flex px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {value || tDirector('users.table.noRole')}
        </span>
      ),
    },
    {
      key: 'cellphone' as keyof User,
      label: tDirector('users.fields.phone'),
      sortable: true,
    },
    {
      key: 'municipality_data' as keyof User,
      label: tDirector('users.fields.municipality'),
      render: (value: any) => (
        <span className="text-sm text-gray-600">
          {value?.name ?? tDirector('users.table.notAssigned')}
        </span>
      ),
    },
    {
      key: 'id' as keyof User,
      label: tDirector('users.fields.actions'),
      render: (_: any, user: User) => (
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEditModal(user)}
            className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded"
            title={tDirector('users.tooltips.edit')}
          >
            <Edit size={16} />
          </button>
          <button
            onClick={() => setShowDeleteModal(user)}
            className="p-1 text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
            title={tDirector('users.tooltips.delete')}
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
            {tDirector('users.title')}
          </h1>
          <p className="text-gray-600 mt-1">{tDirector('users.subtitle')}</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <UserPlus size={16} />
          {tDirector('users.addUser')}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Users className="text-blue-600" size={20} />
            </div>
            <div>
              <div className="text-sm text-gray-600">
                {tDirector('users.stats.totalUsers')}
              </div>
              <div className="text-xl font-bold text-gray-900">
                {users.length}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="text-green-600" size={20} />
            </div>
            <div>
              <div className="text-sm text-gray-600">
                {tDirector('users.stats.withRole')}
              </div>
              <div className="text-xl font-bold text-gray-900">
                {users.filter(u => u.role_name).length}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Shield className="text-purple-600" size={20} />
            </div>
            <div>
              <div className="text-sm text-gray-600">
                {tDirector('users.stats.municipalities')}
              </div>
              <div className="text-xl font-bold text-gray-900">
                {municipalities.length}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Input
              label={tDirector('users.search.label')}
              id="search"
              type="text"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              placeholder={tDirector('users.search.placeholder')}
            />
          </div>
          <div>
            <Select
              label={tDirector('users.filters.role')}
              value={roleFilter}
              onValueChange={setRoleFilter}
              placeholder={tDirector('users.filters.allRoles')}
            >
              {uniqueRoles.map(role => (
                <Option key={role} value={role}>
                  {role}
                </Option>
              ))}
            </Select>
          </div>
        </div>
      </div>

      <DataTable
        data={filteredUsers}
        columns={userColumns}
        title={tDirector('users.table.title')}
        exportable={true}
        searchable={false}
        filterable={false}
      />

      <Dialog open={showAddModal} onOpenChange={setShowAddModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Agregar Nuevo Usuario</DialogTitle>
          </DialogHeader>

          <form onSubmit={handleCreateUser} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Nombre"
                type="text"
                name="name"
                required
                placeholder="Nombre del usuario"
              />
              <Input
                label="Apellido Paterno"
                type="text"
                name="paternal_last_name"
                required
                placeholder="Apellido paterno"
              />
            </div>

            <Input
              label="Apellido Materno"
              type="text"
              name="maternal_last_name"
              placeholder="Apellido materno (opcional)"
            />

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Teléfono"
                type="tel"
                name="cellphone"
                required
                placeholder="Número de teléfono"
              />
              <Input
                label="Email"
                type="email"
                name="email"
                required
                placeholder="correo@ejemplo.com"
              />
            </div>

            <Input
              label="Contraseña"
              type="password"
              name="password"
              required
              placeholder="Contraseña segura"
            />

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Select
                  label="Municipio"
                  name="municipality_id"
                  required
                  placeholder="Seleccionar municipio"
                >
                  {municipalities.map(municipality => (
                    <Option
                      key={municipality.id}
                      value={municipality.id.toString()}
                    >
                      {municipality.name}
                    </Option>
                  ))}
                </Select>
              </div>

              <div>
                <Select
                  label="Rol"
                  name="role_id"
                  required
                  placeholder="Seleccionar rol"
                >
                  {roles.map(role => (
                    <Option key={role.id} value={role.id.toString()}>
                      {role.name}
                    </Option>
                  ))}
                </Select>
              </div>
            </div>

            <DialogFooter className="gap-3 pt-4">
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={fetcher.state === 'submitting'}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {fetcher.state === 'submitting'
                  ? 'Creando...'
                  : 'Crear Usuario'}
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
              Editar Usuario: {showEditModal ? getFullName(showEditModal) : ''}
            </DialogTitle>
          </DialogHeader>

          {showEditModal && (
            <form onSubmit={handleUpdateUser} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Nombre"
                  type="text"
                  name="name"
                  required
                  defaultValue={showEditModal.name}
                  placeholder="Nombre del usuario"
                />
                <Input
                  label="Apellido Paterno"
                  type="text"
                  name="paternal_last_name"
                  required
                  defaultValue={showEditModal.paternal_last_name}
                  placeholder="Apellido paterno"
                />
              </div>

              <Input
                label="Apellido Materno"
                type="text"
                name="maternal_last_name"
                defaultValue={showEditModal.maternal_last_name ?? ''}
                placeholder="Apellido materno (opcional)"
              />

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Teléfono"
                  type="tel"
                  name="cellphone"
                  required
                  defaultValue={showEditModal.cellphone}
                  placeholder="Número de teléfono"
                />
                <Input
                  label="Email"
                  type="email"
                  name="email"
                  required
                  defaultValue={showEditModal.email}
                  placeholder="correo@ejemplo.com"
                />
              </div>

              <Input
                label="Nueva Contraseña"
                type="password"
                name="password"
                placeholder="Dejar vacío para mantener la actual"
              />

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Select
                    label="Municipio"
                    name="municipality_id"
                    required
                    defaultValue={
                      showEditModal.municipality_data?.id?.toString() ?? ''
                    }
                    placeholder="Seleccionar municipio"
                  >
                    {municipalities.map(municipality => (
                      <Option
                        key={municipality.id}
                        value={municipality.id.toString()}
                      >
                        {municipality.name}
                      </Option>
                    ))}
                  </Select>
                </div>

                <div>
                  <Select
                    label="Rol"
                    name="role_id"
                    required
                    defaultValue={
                      roles
                        .find(role => role.name === showEditModal.role_name)
                        ?.id?.toString() ?? ''
                    }
                    placeholder="Seleccionar rol"
                  >
                    {roles.map(role => (
                      <Option key={role.id} value={role.id.toString()}>
                        {role.name}
                      </Option>
                    ))}
                  </Select>
                </div>
              </div>

              <DialogFooter className="gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowEditModal(null)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={fetcher.state === 'submitting'}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {fetcher.state === 'submitting'
                    ? 'Guardando...'
                    : 'Guardar Cambios'}
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
            <DialogTitle>Confirmar Eliminación</DialogTitle>
          </DialogHeader>

          {showDeleteModal && (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                  <AlertTriangle className="text-red-600" size={20} />
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    ¿Eliminar usuario {getFullName(showDeleteModal)}?
                  </h3>
                  <p className="text-sm text-gray-500">
                    Esta acción no se puede deshacer.
                  </p>
                </div>
              </div>

              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-sm text-red-800">
                  <strong>¡Atención!</strong> Al eliminar este usuario se
                  perderán todos sus datos y no podrá acceder al sistema.
                </p>
              </div>

              <DialogFooter className="gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowDeleteModal(null)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleDeleteUser}
                  disabled={fetcher.state === 'submitting'}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
                >
                  {fetcher.state === 'submitting'
                    ? 'Eliminando...'
                    : 'Eliminar Usuario'}
                </button>
              </DialogFooter>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
