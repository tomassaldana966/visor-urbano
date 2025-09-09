import type { LoaderFunctionArgs } from 'react-router';
import { useState, useEffect } from 'react';
import { useLoaderData } from 'react-router';
import { useTranslation } from 'react-i18next';
import {
  Building2,
  Users,
  ClipboardList,
  Plus,
  Minus,
  Loader2,
  AlertCircle,
  CheckCircle2,
  Settings,
} from 'lucide-react';
import { Button } from '../../components/Button/Button';
import { Badge } from '../../components/Badge/Badge';
import { Modal } from '../../components/Modal/Modal';
import { Switch } from '../../components/Switch/Switch';
import {
  getDepartments,
  getDepartmentUsers,
  getDepartmentRequirements,
  performQuickAction,
  updateDepartment,
  createDepartment,
  toggleUserActivationForReviews,
  type DepartmentFullInfo,
  type DepartmentUser,
  type DepartmentRequirement,
  AVAILABLE_DEPARTMENT_ROLES,
} from '../../utils/api/departments';
import { getRoles, type Role } from '../../utils/api/roles';
import { getFields } from '../../utils/api/fields';
import type { DynamicField } from '@root/app/schemas/requirements';

export const handle = {
  title: 'director:dependencies.title',
  breadcrumb: 'director:dependencies.breadcrumb',
};

interface LoaderData {
  accessToken: string;
  hasAccess: boolean;
}

export async function loader({
  request,
}: LoaderFunctionArgs): Promise<LoaderData> {
  const { getAccessToken, requireAuth, getAuthUser } = await import(
    '../../utils/auth/auth.server'
  );
  const { checkAdminOrDirectorPermissions } = await import(
    '../../utils/auth/director'
  );

  // Require authentication
  const user = await requireAuth(request);

  // Get access token
  const accessToken = await getAccessToken(request);

  if (!accessToken) {
    throw new Response('Unauthorized', { status: 401 });
  }

  // Check director permissions
  const hasAccess = checkAdminOrDirectorPermissions(user);

  if (!hasAccess) {
    throw new Response('Forbidden - Director access required', { status: 403 });
  }

  return {
    accessToken,
    hasAccess,
  };
}

export default function DependenciesQuickAction() {
  const { t } = useTranslation('director');
  const { accessToken } = useLoaderData<LoaderData>();

  const [departments, setDepartments] = useState<DepartmentFullInfo[]>([]);
  const [selectedDepartment, setSelectedDepartment] =
    useState<DepartmentFullInfo | null>(null);
  const [departmentUsers, setDepartmentUsers] = useState<DepartmentUser[]>([]);
  const [departmentRequirements, setDepartmentRequirements] = useState<
    DepartmentRequirement[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [loadingRequirements, setLoadingRequirements] = useState(false);
  const [showQuickAction, setShowQuickAction] = useState(false);
  const [quickActionType, setQuickActionType] = useState<
    'add_field' | 'remove_field' | 'add_role' | 'remove_role'
  >('add_field');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<
    'requirements' | 'users' | 'roles'
  >('requirements');

  // New states for toggles and create modal
  const [showInactiveDepartments, setShowInactiveDepartments] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newDepartmentData, setNewDepartmentData] = useState({
    name: '',
    description: '',
    code: '',
  });
  const [allRoles, setAllRoles] = useState<Role[]>([]);
  const [allFields, setAllFields] = useState<DynamicField[]>([]);
  const [selectedFieldForAdd, setSelectedFieldForAdd] =
    useState<DynamicField | null>(null);
  const [selectedRoleForAdd, setSelectedRoleForAdd] = useState<Role | null>(
    null
  );

  // Load departments on component mount
  useEffect(() => {
    loadDepartments();
  }, []);

  // Reload departments when toggle changes
  useEffect(() => {
    loadDepartments();
  }, [showInactiveDepartments]);

  // Load department details when selection changes
  useEffect(() => {
    if (selectedDepartment) {
      loadDepartmentUsers(selectedDepartment.id);
      loadDepartmentRequirements(selectedDepartment.id);
    }
  }, [selectedDepartment]);

  const showToast = (message: string, type: 'success' | 'error') => {
    if (type === 'success') {
      setSuccess(message);
      setError(null);
    } else {
      setError(message);
      setSuccess(null);
    }
    setTimeout(() => {
      setSuccess(null);
      setError(null);
    }, 5000);
  };

  const loadDepartments = async () => {
    try {
      setLoading(true);
      setError(null);

      // Add timeout for the request
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(
          () => reject(new Error(t('dependencies.messages.backendTimeout'))),
          10000
        )
      );

      const dataPromise = getDepartments(accessToken, showInactiveDepartments);
      const data = (await Promise.race([
        dataPromise,
        timeoutPromise,
      ])) as DepartmentFullInfo[];

      setDepartments(data);

      // Auto-select first department if available
      if (data.length > 0) {
        setSelectedDepartment(data[0]);
      }
    } catch (error) {
      console.error('Error loading departments:', error);
      const errorMessage =
        error instanceof Error
          ? error.message
          : t('dependencies.error.loadDepartments');
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadDepartmentUsers = async (departmentId: number) => {
    try {
      setLoadingUsers(true);
      const response = await getDepartmentUsers(accessToken, departmentId);
      setDepartmentUsers(response.users);
    } catch (error) {
      showToast(
        error instanceof Error
          ? error.message
          : t('dependencies.error.loadUsers'),
        'error'
      );
    } finally {
      setLoadingUsers(false);
    }
  };

  const loadDepartmentRequirements = async (departmentId: number) => {
    try {
      setLoadingRequirements(true);
      const response = await getDepartmentRequirements(
        accessToken,
        departmentId
      );
      setDepartmentRequirements(response.requirements);
    } catch (error) {
      console.error('Error loading requirements:', error);
      // Silenciar errores de requirements por ahora ya que no hay datos de prueba
      setDepartmentRequirements([]);
    } finally {
      setLoadingRequirements(false);
    }
  };

  const handleQuickAction = async (actionData: any) => {
    if (!selectedDepartment) return;

    try {
      const response = await performQuickAction(accessToken, {
        department_id: selectedDepartment.id,
        ...actionData,
      });

      if (response.success) {
        showToast(response.message, 'success');

        // Refresh department data
        await loadDepartments();
        if (selectedDepartment) {
          await loadDepartmentUsers(selectedDepartment.id);
          await loadDepartmentRequirements(selectedDepartment.id);
        }
      } else {
        throw new Error(response.message);
      }
    } catch (error) {
      showToast(
        error instanceof Error
          ? error.message
          : t('dependencies.error.actionFailed'),
        'error'
      );
    }
    setShowQuickAction(false);
  };

  const toggleDepartmentStatus = async (
    departmentId: number,
    currentStatus: boolean
  ) => {
    try {
      await updateDepartment(accessToken, departmentId, {
        is_active: !currentStatus,
      });

      const newStatus = !currentStatus;

      // If we're deactivating a department and "Show inactive" is false,
      // remove it from the list immediately
      if (!newStatus && !showInactiveDepartments) {
        const filteredDepartments = departments.filter(
          dept => dept.id !== departmentId
        );
        setDepartments(filteredDepartments);

        // If the deactivated department was selected, select the first available one
        if (selectedDepartment?.id === departmentId) {
          if (filteredDepartments.length > 0) {
            setSelectedDepartment(filteredDepartments[0]);
          } else {
            setSelectedDepartment(null);
          }
        }
      } else {
        // Otherwise, just update the department status in the list
        const updatedDepartments = departments.map(dept =>
          dept.id === departmentId ? { ...dept, is_active: newStatus } : dept
        );
        setDepartments(updatedDepartments);

        // Update selected department if it's the one being toggled
        if (selectedDepartment?.id === departmentId) {
          setSelectedDepartment({
            ...selectedDepartment,
            is_active: newStatus,
          });
        }
      }

      showToast(
        t(
          `dependencies.messages.department${newStatus ? 'Activated' : 'Deactivated'}`
        ),
        'success'
      );
    } catch (error) {
      showToast(t('dependencies.error.updateDepartmentStatus'), 'error');
    }
  };

  const createNewDepartment = async (departmentData: {
    name: string;
    code: string;
    description?: string;
  }) => {
    try {
      await createDepartment(accessToken, {
        ...departmentData,
        municipality_id: 1, // TODO: Get actual municipality ID from context/user
        is_active: true,
        can_approve_procedures: true,
        can_reject_procedures: true,
        requires_all_requirements: false,
      });

      showToast(t('dependencies.messages.newDepartmentCreated'), 'success');
      setShowCreateModal(false);
      setNewDepartmentData({ name: '', code: '', description: '' });
      await loadDepartments(); // Reload departments
    } catch (error) {
      showToast(t('dependencies.error.createDepartment'), 'error');
    }
  };

  const toggleUserActivationForReviewsHandler = async (
    userId: number,
    currentStatus: boolean
  ) => {
    if (!selectedDepartment) return;

    try {
      const result = await toggleUserActivationForReviews(
        accessToken,
        selectedDepartment.id,
        userId,
        !currentStatus
      );

      showToast(
        t(
          `dependencies.messages.user${!currentStatus ? 'Activated' : 'Deactivated'}ForReviews`
        ),
        'success'
      );

      // Reload department users
      await loadDepartmentUsers(selectedDepartment.id);
    } catch (error) {
      showToast(
        error instanceof Error
          ? error.message
          : t('dependencies.error.updateUserActivation'),
        'error'
      );
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">{t('dependencies.loading', 'Loading...')}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Notifications */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg flex items-center gap-2">
          <AlertCircle className="h-5 w-5" />
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5" />
          {success}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">
            {t('dependencies.title', 'Dependencies Management')}
          </h2>
          <p className="text-gray-600">
            {t(
              'dependencies.description',
              'Manage departments, requirements and user roles'
            )}
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-3">
          {/* Dynamic action button for selected department */}
          {selectedDepartment && activeTab !== 'users' && (
            <Button
              variant="outline"
              onClick={() => {
                if (activeTab === 'requirements') {
                  setQuickActionType('add_field');
                } else if (activeTab === 'roles') {
                  setQuickActionType('add_role');
                }
                setShowQuickAction(true);
              }}
              className="flex items-center gap-2 min-w-[140px]"
            >
              <Plus className="h-4 w-4" />
              {activeTab === 'requirements' &&
                t('dependencies.actions.addField', 'Add Field')}
              {activeTab === 'roles' &&
                t('dependencies.actions.addRole', 'Add Role')}
            </Button>
          )}

          {/* Create new department button */}
          <Button
            variant="secondary"
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 min-w-[140px]"
          >
            <Plus className="h-4 w-4" />
            {t('dependencies.createDepartment.button', 'New Department')}
          </Button>
        </div>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          <div className="text-center space-y-2">
            <p className="text-gray-600">
              {t('dependencies.loading', 'Loading departments...')}
            </p>
            <p className="text-sm text-gray-500">
              {t('dependencies.messages.connectingBackend')}
            </p>
          </div>
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <AlertCircle className="h-12 w-12 text-red-500" />
          <div className="text-center space-y-2">
            <h3 className="text-lg font-semibold text-red-700">
              {t('dependencies.messages.connectionError')}
            </h3>
            <p className="text-gray-600 max-w-md">
              {t('dependencies.messages.noBackendConnection')}
            </p>
            <Button
              onClick={loadDepartments}
              variant="outline"
              className="mt-4"
            >
              {t('dependencies.messages.retry')}
            </Button>
          </div>
        </div>
      )}

      {/* Content - only show when not loading and no error */}
      {!loading && !error && (
        <>
          {/* Department Selection */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Building2 className="h-5 w-5" />
                  {t('dependencies.departments.title', 'Departments')}
                </h3>

                {/* Toggle to show inactive departments */}
                <div className="flex items-center gap-2">
                  <Switch
                    checked={showInactiveDepartments}
                    onCheckedChange={setShowInactiveDepartments}
                    aria-label="Show inactive departments"
                  />
                  <span className="text-sm text-gray-600">
                    {t('dependencies.showInactive')}
                  </span>
                </div>
              </div>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {departments.map(dept => (
                  <div
                    key={dept.id}
                    className={`cursor-pointer transition-colors border rounded-lg p-4 ${
                      selectedDepartment?.id === dept.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:bg-gray-50'
                    }`}
                    onClick={() => setSelectedDepartment(dept)}
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="font-semibold">{dept.name}</h4>
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={dept.is_active ? 'success' : 'secondary'}
                          >
                            {dept.is_active
                              ? t('common.active')
                              : t('common.inactive')}
                          </Badge>
                          <Switch
                            checked={dept.is_active}
                            onCheckedChange={() =>
                              toggleDepartmentStatus(dept.id, dept.is_active)
                            }
                            aria-label={`Toggle ${dept.name} status`}
                            className="ml-2"
                          />
                        </div>
                      </div>
                      <p className="text-sm text-gray-600">{dept.code}</p>
                      <div className="flex gap-4 text-xs text-gray-500">
                        <span className="flex items-center gap-1">
                          <Users className="h-3 w-3" />
                          {dept.user_count} {t('dependencies.users', 'users')}
                        </span>
                        <span className="flex items-center gap-1">
                          <ClipboardList className="h-3 w-3" />
                          {dept.requirement_count}{' '}
                          {t('dependencies.requirements', 'requirements')}
                        </span>
                      </div>
                      {dept.pending_procedures > 0 && (
                        <Badge variant="outline" className="text-orange-600">
                          {dept.pending_procedures}{' '}
                          {t('dependencies.pendingWork', 'pending')}
                        </Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Department Details */}
          {selectedDepartment && (
            <div className="bg-white rounded-lg shadow border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex space-x-8">
                  <button
                    className={`pb-2 font-medium text-sm ${
                      activeTab === 'requirements'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                    onClick={() => setActiveTab('requirements')}
                  >
                    <ClipboardList className="h-4 w-4 inline mr-2" />
                    {t('dependencies.tabs.requirements', 'Requirements')}
                  </button>
                  <button
                    className={`pb-2 font-medium text-sm ${
                      activeTab === 'users'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                    onClick={() => setActiveTab('users')}
                  >
                    <Users className="h-4 w-4 inline mr-2" />
                    {t('dependencies.tabs.users', 'Users')}
                  </button>
                  <button
                    className={`pb-2 font-medium text-sm ${
                      activeTab === 'roles'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                    onClick={() => setActiveTab('roles')}
                  >
                    <Building2 className="h-4 w-4 inline mr-2" />
                    {t('dependencies.tabs.roles', 'Roles')}
                  </button>
                </div>
              </div>

              <div className="p-6">
                {activeTab === 'requirements' && (
                  <div className="space-y-6">
                    {/* Requirements Section */}
                    <div>
                      <h4 className="font-semibold mb-4">
                        {t(
                          'dependencies.departmentRequirements.title',
                          'Department Requirements'
                        )}
                      </h4>
                      {loadingRequirements ? (
                        <div className="flex items-center justify-center py-8">
                          <Loader2 className="h-6 w-6 animate-spin" />
                        </div>
                      ) : departmentRequirements.length === 0 ? (
                        <p className="text-gray-500 py-8 text-center">
                          {t(
                            'dependencies.departmentRequirements.empty',
                            'No requirements assigned to this department'
                          )}
                        </p>
                      ) : (
                        <div className="space-y-3">
                          {departmentRequirements.map(req => (
                            <div
                              key={req.id}
                              className="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
                            >
                              <div>
                                <p className="font-medium">{req.field_label}</p>
                                <p className="text-sm text-gray-600">
                                  {req.procedure_type}
                                </p>
                              </div>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() =>
                                  handleQuickAction({
                                    action: 'remove_field',
                                    field_id: req.field_id,
                                    procedure_type: req.field_type,
                                  })
                                }
                              >
                                <Minus className="h-4 w-4" />
                              </Button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {activeTab === 'users' && (
                  <div>
                    <h4 className="font-semibold mb-4">
                      {t(
                        'dependencies.departmentUsers.title',
                        'Department Users'
                      )}
                    </h4>
                    {loadingUsers ? (
                      <div className="flex items-center justify-center py-8">
                        <Loader2 className="h-6 w-6 animate-spin" />
                      </div>
                    ) : departmentUsers.length === 0 ? (
                      <p className="text-gray-500 py-8 text-center">
                        {t(
                          'dependencies.departmentUsers.empty',
                          'No users assigned to this department'
                        )}
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {departmentUsers.map(user => (
                          <div
                            key={user.id}
                            className="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
                          >
                            <div className="flex-1">
                              <p className="font-medium">{user.name}</p>
                              <p className="text-sm text-gray-600">
                                {user.email}
                              </p>
                              {user.role_name && (
                                <p className="text-xs text-gray-500 mt-1">
                                  {t('dependencies.messages.roleLabel')}{' '}
                                  {user.role_name}
                                </p>
                              )}
                            </div>
                            <div className="flex items-center gap-3">
                              <div className="flex flex-col gap-1">
                                <Badge variant="outline">
                                  {user.role_name}
                                </Badge>
                                <Badge
                                  variant={
                                    user.is_active ? 'success' : 'secondary'
                                  }
                                >
                                  {user.is_active
                                    ? t('common.active')
                                    : t('common.inactive')}
                                </Badge>
                              </div>

                              {/* Switch para activar/desactivar revisiones */}
                              <div className="flex flex-col items-center gap-1">
                                <Switch
                                  checked={user.is_active_for_reviews || false}
                                  onCheckedChange={() =>
                                    toggleUserActivationForReviewsHandler(
                                      user.id,
                                      user.is_active_for_reviews || false
                                    )
                                  }
                                  aria-label={`Toggle ${user.name} activation for reviews`}
                                />
                                <span className="text-xs text-gray-500">
                                  {t('dependencies.reviewsActive')}
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'roles' && (
                  <div>
                    <h4 className="font-semibold mb-4">
                      {t(
                        'dependencies.departmentRoles.title',
                        'Department Roles'
                      )}
                    </h4>
                    {selectedDepartment.roles.length === 0 ? (
                      <p className="text-gray-500 py-8 text-center">
                        {t(
                          'dependencies.departmentRoles.empty',
                          'No roles assigned for approval in this department'
                        )}
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {selectedDepartment.roles.map(role => (
                          <div
                            key={role.id}
                            className="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
                          >
                            <div>
                              <p className="font-medium">{role.role_name}</p>
                              <p className="text-sm text-gray-600">
                                {t(
                                  'dependencies.departmentRoles.canApprove',
                                  'Can approve procedures for this department'
                                )}
                              </p>
                            </div>
                            <div className="flex items-center gap-2">
                              <Badge variant="success">
                                {t(
                                  'dependencies.departmentRoles.approver',
                                  'Approver'
                                )}
                              </Badge>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  setQuickActionType('remove_role');
                                  setShowQuickAction(true);
                                }}
                              >
                                <Minus className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {/* Quick Action Modal */}
      {showQuickAction && selectedDepartment && (
        <QuickActionModal
          department={selectedDepartment}
          actionType={quickActionType}
          onClose={() => setShowQuickAction(false)}
          onAction={handleQuickAction}
        />
      )}

      {/* Create Department Modal */}
      {showCreateModal && (
        <CreateDepartmentModal
          onClose={() => setShowCreateModal(false)}
          onCreate={createNewDepartment}
        />
      )}
    </div>
  );
}

// Quick Action Modal Component
function QuickActionModal({
  department,
  actionType,
  onClose,
  onAction,
}: {
  department: DepartmentFullInfo;
  actionType: 'add_field' | 'remove_field' | 'add_role' | 'remove_role';
  onClose: () => void;
  onAction: (data: any) => void;
}) {
  const { t } = useTranslation('director');
  const [selectedFieldId, setSelectedFieldId] = useState<number | null>(null);
  const [selectedFieldType, setSelectedFieldType] = useState<string | null>(
    null
  );
  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);
  const [procedureType, setProcedureType] = useState<string>('');
  const [availableRoles, setAvailableRoles] = useState<Role[]>([]);
  const [availableFields, setAvailableFields] = useState<DynamicField[]>([]);
  const [loadingRoles, setLoadingRoles] = useState(false);
  const [loadingFields, setLoadingFields] = useState(false);

  const { accessToken } = useLoaderData<LoaderData>();

  // Load roles when modal opens for role actions
  useEffect(() => {
    if (actionType === 'add_role' || actionType === 'remove_role') {
      loadRoles();
    }
    if (actionType === 'add_field' || actionType === 'remove_field') {
      loadFields();
    }
  }, [actionType]);

  const loadRoles = async () => {
    try {
      setLoadingRoles(true);
      const roles = await getRoles(accessToken);
      // Filter out deleted roles (roles with deleted_at set)
      const activeRoles = roles.filter(role => !role.deleted_at);
      setAvailableRoles(activeRoles);
    } catch (error) {
      console.error('Error loading roles:', error);
      // Fallback to empty array if loading fails
      setAvailableRoles([]);
    } finally {
      setLoadingRoles(false);
    }
  };

  const loadFields = async () => {
    try {
      setLoadingFields(true);
      const fields = await getFields(accessToken);
      // Filter out deleted fields and only get active ones
      const activeFields = fields.filter(field => field.status === 1);
      setAvailableFields(activeFields);
    } catch (error) {
      console.error('Error loading fields:', error);
      // Fallback to empty array if loading fails
      setAvailableFields([]);
    } finally {
      setLoadingFields(false);
    }
  };

  const handleSubmit = () => {
    const actionData: any = { action: actionType };

    if (actionType === 'add_field' || actionType === 'remove_field') {
      if (!selectedFieldId) {
        alert(t('dependencies.modal.selectField'));
        return;
      }
      actionData.field_id = selectedFieldId;
      actionData.procedure_type = selectedFieldType;
      actionData.procedure_type = selectedFieldType;
    } else if (actionType === 'add_role' || actionType === 'remove_role') {
      if (!selectedRoleId) {
        alert(t('dependencies.modal.selectRole'));
        return;
      }
      actionData.role_id = selectedRoleId;
    }

    onAction(actionData);
  };

  return (
    <Modal
      isOpen={true}
      onClose={onClose}
      title={t(`dependencies.actions.${actionType}`, actionType)}
    >
      <div className="space-y-4">
        <p className="text-gray-600">
          {t('dependencies.modal.department', 'Department')}:{' '}
          <strong>{department.name}</strong>
        </p>

        {(actionType === 'add_field' || actionType === 'remove_field') && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('dependencies.modal.field', 'Field')}
            </label>
            <select
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
              value={selectedFieldId || ''}
              onChange={e => {
                const fieldId = Number(e.target.value) || null;
                setSelectedFieldId(fieldId);

                // Find the selected field and save its field_type
                if (fieldId) {
                  const selectedField = availableFields.find(
                    field => field.id === fieldId
                  );
                  setSelectedFieldType(selectedField?.field_type || null);
                } else {
                  setSelectedFieldType(null);
                }
              }}
              disabled={loadingFields}
            >
              <option value="">
                {loadingFields
                  ? t('common.loading')
                  : t('dependencies.modal.selectField')}
              </option>
              {availableFields
                .filter(field => field.id !== null)
                .map(field => (
                  <option key={field.id} value={field.id!}>
                    {field.description || field.name} ({field.field_type})
                  </option>
                ))}
            </select>
            {loadingFields && (
              <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
                <Loader2 className="h-4 w-4 animate-spin" />
                {t('common.loading')}
              </div>
            )}
          </div>
        )}

        {(actionType === 'add_role' || actionType === 'remove_role') && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('dependencies.modal.role', 'Role')}
            </label>
            <select
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
              value={selectedRoleId || ''}
              onChange={e =>
                setSelectedRoleId(
                  e.target.value ? Number(e.target.value) : null
                )
              }
              disabled={loadingRoles}
            >
              <option value="">
                {loadingRoles
                  ? t('common.loading')
                  : t('dependencies.modal.selectRole')}
              </option>
              {availableRoles.map(role => (
                <option key={role.id} value={role.id}>
                  {role.name} - {role.description}
                </option>
              ))}
            </select>
            {loadingRoles && (
              <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
                <Loader2 className="h-4 w-4 animate-spin" />
                {t('common.loading')}
              </div>
            )}
          </div>
        )}

        <div className="flex gap-2 justify-end pt-4">
          <Button variant="outline" onClick={onClose}>
            {t('common.cancel')}
          </Button>
          <Button onClick={handleSubmit}>{t('common.confirm')}</Button>
        </div>
      </div>
    </Modal>
  );
}

// Create Department Modal Component
function CreateDepartmentModal({
  onClose,
  onCreate,
}: {
  onClose: () => void;
  onCreate: (data: {
    name: string;
    code: string;
    description?: string;
  }) => void;
}) {
  const { t } = useTranslation('director');
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name || !code) {
      return alert(t('dependencies.createDepartment.fillFields'));
    }

    setLoading(true);
    try {
      await onCreate({ name, code, description });
      setName('');
      setCode('');
      setDescription('');
    } catch (error) {
      alert(t('dependencies.createDepartment.error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={true}
      onClose={onClose}
      title={t('dependencies.createDepartment.title', 'Create New Department')}
    >
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('dependencies.createDepartment.name', 'Department Name')}
          </label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('dependencies.createDepartment.code', 'Department Code')}
          </label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            value={code}
            onChange={e => setCode(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('dependencies.createDepartment.description', 'Description')}
          </label>
          <textarea
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            value={description}
            onChange={e => setDescription(e.target.value)}
            rows={3}
          />
        </div>

        <div className="flex gap-2 justify-end pt-4">
          <Button variant="outline" onClick={onClose}>
            {t('common.cancel')}
          </Button>
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? t('common.loading') : t('common.create')}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
