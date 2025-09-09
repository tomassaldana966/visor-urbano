import type { AuthUser } from './auth.server';

/**
 * Role ID enumeration for better type safety and readability
 * Based on backend seed data
 */
export enum RoleId {
  CITIZEN = 1,
  COUNTER = 2,
  REVIEWER = 3,
  DIRECTOR = 4,
  ADMIN = 5,
  TECHNICIAN = 6,
  SPECIALIZED_DEPT_7 = 7,
  SPECIALIZED_DEPT_8 = 8,
  SPECIALIZED_REVIEWER = 9,
  SPECIALIZED_DEPT_10 = 10,
  SPECIALIZED_DEPT_11 = 11,
  SPECIALIZED_DEPT_12 = 12,
}

/**
 * Role-based permissions using role_id for consistency
 * Based on backend seed data:
 * 1=Citizen, 2=Counter, 3=Reviewer, 4=Director, 5=Admin, 6=Technician
 */
export const RolePermissions = {
  // Role name arrays for string-based role checking
  ADMIN_ROLES: [
    'admin',
    'administrator',
    'administrador',
    'director',
    'director_admin',
  ] as readonly string[],

  DIRECTOR_ROLES: [
    'director',
    'director_admin',
    'director_municipal',
  ] as readonly string[],

  SUPERVISOR_ROLES: ['supervisor', 'jefe', 'coordinador'] as readonly string[],

  // Admin role IDs - only true administrators (NOT citizens)
  ADMIN_ROLE_IDS: [RoleId.ADMIN] as readonly number[],

  // Reviewer/Supervisor role IDs - can access procedure approvals but CANNOT issue licenses
  // Includes Reviewer and all Specialized Reviewer roles (role_id > 4)
  REVIEWER_ROLE_IDS: [
    RoleId.REVIEWER,
    RoleId.SPECIALIZED_REVIEWER,
    // All roles > 4 are considered custom reviewers
  ] as readonly number[],

  // All roles that can access procedure approvals
  // This includes directors, admins, reviewers, technicians, etc. (but NOT citizens or counter staff)
  PROCEDURE_APPROVAL_ROLE_IDS: [
    RoleId.REVIEWER,
    RoleId.DIRECTOR,
    RoleId.ADMIN,
    RoleId.TECHNICIAN,
    RoleId.SPECIALIZED_DEPT_7,
    RoleId.SPECIALIZED_DEPT_8,
    RoleId.SPECIALIZED_REVIEWER,
    RoleId.SPECIALIZED_DEPT_10,
    RoleId.SPECIALIZED_DEPT_11,
    RoleId.SPECIALIZED_DEPT_12,
    // Note: All roles > 4 are handled dynamically in permission functions
  ] as readonly number[],
} as const;

/**
 * Check if user has Director permissions (can issue licenses)
 * @param user - The authenticated user object
 * @returns boolean - true if user has director permissions
 */
export function checkDirectorPermissions(user: AuthUser | null): boolean {
  if (!user) {
    return false;
  }

  // Check if user has role_id
  const userRoleId = user.role_id;
  if (!userRoleId) {
    return false;
  }

  // Admin users are also directors
  if (RolePermissions.ADMIN_ROLE_IDS.includes(userRoleId)) {
    return true;
  }

  // Check if user is specifically a reviewer (cannot be director)
  if (RolePermissions.REVIEWER_ROLE_IDS.includes(userRoleId)) {
    return false;
  }

  // Check if user can access procedure approvals (meaning they have some role)
  // If they can access procedure approvals AND are not a reviewer, they are a director
  const canAccessProcedureApprovals =
    RolePermissions.PROCEDURE_APPROVAL_ROLE_IDS.includes(userRoleId);
  const isDirector = canAccessProcedureApprovals && userRoleId > RoleId.COUNTER; // Exclude Citizen and Counter roles

  return isDirector;
}

/**
 * Check if user has Admin permissions
 * @param user - The authenticated user object
 * @returns boolean - true if user has admin permissions
 */
export function checkAdminPermissions(user: AuthUser | null): boolean {
  if (!user) {
    return false;
  }

  const userRoleId = user.role_id;
  if (!userRoleId) {
    return false;
  }

  // Check if user's role_id is in admin roles list
  return RolePermissions.ADMIN_ROLE_IDS.includes(userRoleId);
}

/**
 * Check if user has Admin or Director permissions
 * @param user - The authenticated user object
 * @returns boolean - true if user has admin or director permissions
 */
export function checkAdminOrDirectorPermissions(
  user: AuthUser | null
): boolean {
  return checkAdminPermissions(user) || checkDirectorPermissions(user);
}

/**
 * Check if user has Supervisor permissions
 * @param user - The authenticated user object
 * @returns boolean - true if user has supervisor permissions
 */
export function checkSupervisorPermissions(user: AuthUser | null): boolean {
  if (!user) {
    return false;
  }

  const userRoleId = user.role_id;
  if (!userRoleId) {
    return false;
  }

  // Check if user's role_id is in reviewer roles list
  return RolePermissions.REVIEWER_ROLE_IDS.includes(userRoleId);
}

/**
 * Check if user belongs to a specific municipality
 * @param user - The authenticated user object
 * @param requiredMunicipalityId - The required municipality ID
 * @returns boolean - true if user belongs to the municipality or is admin
 */
export function checkMunicipalityAccess(
  user: AuthUser | null,
  requiredMunicipalityId?: number
): boolean {
  if (!user) {
    return false;
  }

  // If no specific municipality required, allow access
  if (!requiredMunicipalityId) {
    return true;
  }

  // Check if user belongs to the required municipality
  if (user.municipality_id === requiredMunicipalityId) {
    return true;
  }

  // Admins can access any municipality
  if (checkAdminPermissions(user)) {
    return true;
  }

  return false;
}

/**
 * Get user's municipality name safely
 * @param user - The authenticated user object
 * @returns string - Municipality name or default message
 */
export function getMunicipalityName(user: AuthUser | null): string {
  if (!user?.municipality_data?.name) {
    return 'Sin municipio';
  }
  return user.municipality_data.name;
}

/**
 * Check if user can perform administrative actions in their municipality
 * @param user - The authenticated user object
 * @returns boolean - true if user can perform admin actions
 */
export function canPerformMunicipalityAdminActions(
  user: AuthUser | null
): boolean {
  if (!user) {
    return false;
  }

  // Must have director or admin permissions
  if (!checkAdminOrDirectorPermissions(user)) {
    return false;
  }

  // Must be associated with a municipality (unless global admin)
  if (!user.municipality_id && !checkAdminPermissions(user)) {
    return false;
  }

  return true;
}

/**
 * Check if user has permissions to access procedure approvals
 * @param user - The authenticated user object
 * @returns boolean - true if user has procedure approval permissions
 */
export function checkProcedureApprovalPermissions(
  user: AuthUser | null
): boolean {
  if (!user || !user.role_id || user.role_id <= RoleId.CITIZEN) {
    return false;
  }

  // Check if user has admin or director permissions first
  if (checkAdminOrDirectorPermissions(user)) {
    return true;
  }

  // Use the centralized procedure approval role IDs
  if (RolePermissions.PROCEDURE_APPROVAL_ROLE_IDS.includes(user.role_id)) {
    return true;
  }

  // ALL ROLES > 4 are considered custom reviewers and can access procedure approvals
  if (user.role_id > RoleId.DIRECTOR) {
    return true;
  }

  return false;
}

/**
 * Check if user can elaborate resolution for a specific procedure
 * Based on legacy analysis adapted to new department system
 * @param procedure - The procedure approval object
 * @param user - The authenticated user object
 * @returns Object with canElaborate boolean and isDirector flag
 */
export function checkElaborateResolutionPermissions(
  procedure: any,
  user: AuthUser | null
): { canElaborate: boolean; isDirector: boolean } {
  if (!user) {
    return { canElaborate: false, isDirector: false };
  }

  const userRoleId = user.role_id;
  if (!userRoleId || userRoleId <= RoleId.CITIZEN) {
    return { canElaborate: false, isDirector: false };
  }

  // Check if user has basic procedure approval permissions
  if (!checkProcedureApprovalPermissions(user)) {
    return { canElaborate: false, isDirector: false };
  }

  // Check procedure state first
  const procedureState = isProcedureInElaborateState(procedure);
  if (!procedureState.canElaborate) {
    return { canElaborate: false, isDirector: false };
  }

  // Use legacy role mapping for consistency
  const isDirector = LEGACY_ROLE_MAPPING.isLegacyDirector(userRoleId);
  const isTechnicalReviewer =
    LEGACY_ROLE_MAPPING.isLegacyTechnicalReviewer(userRoleId);
  const isSpecializedDept =
    LEGACY_ROLE_MAPPING.isLegacySpecializedDept(userRoleId);

  // Legacy logic adapted to new system:

  // 1. TECHNICAL REVIEWERS - equivalent to legacy role 3
  if (isTechnicalReviewer) {
    // Technical reviewers cannot elaborate on approved (status 2) or director-approved (status 4) procedures
    if (procedure.status === 2 || procedure.status === 4) {
      return { canElaborate: false, isDirector: false };
    }

    // Allow elaboration when status is null, 0, 1 (pending_review), or 3
    const canElaborate =
      procedure.status === null ||
      procedure.status === 0 ||
      procedure.status === 1 ||
      procedure.status === 3;

    return { canElaborate, isDirector: false };
  }

  // 2. DIRECTORS - equivalent to legacy role 4
  if (isDirector) {
    // Directors still respect procedure state restrictions
    return { canElaborate: procedureState.canElaborate, isDirector: true };
  }

  // 3. SPECIALIZED DEPARTMENTS - equivalent to legacy role > 6
  if (isSpecializedDept) {
    // Specialized departments still respect procedure state restrictions
    return { canElaborate: procedureState.canElaborate, isDirector: false };
  }

  return { canElaborate: false, isDirector: false };
}

/**
 * Enhanced permission check that can be extended to include department assignments
 * This function can be improved to make API calls to verify user's department assignments
 * for the specific procedure, providing more granular access control
 *
 * TODO: Integrate with DependencyReview API to check specific assignments
 * @param procedure - The procedure approval object
 * @param user - The authenticated user object
 * @returns Object with detailed permission information
 */
export function checkEnhancedElaborateResolutionPermissions(
  procedure: any,
  user: AuthUser | null
): {
  canElaborate: boolean;
  isDirector: boolean;
  reason: string;
  isAssignedReviewer?: boolean;
  departmentAssignment?: string;
} {
  const basicCheck = checkElaborateResolutionPermissions(procedure, user);

  if (!basicCheck.canElaborate) {
    return {
      ...basicCheck,
      reason:
        'Basic permission check failed - user role or procedure state not suitable',
    };
  }

  // For now, return the basic check with additional metadata
  // In the future, this can be enhanced to:
  // 1. Call API to check DependencyReview table for user assignment
  // 2. Verify if user is in DepartmentUserAssignment for relevant departments
  // 3. Check workflow state in DependencyReviewWorkflow table

  return {
    ...basicCheck,
    reason: basicCheck.isDirector
      ? 'Director can elaborate resolution for reviewed procedures'
      : 'User has reviewer permissions for this procedure state',
    isAssignedReviewer: !basicCheck.isDirector, // Non-directors are reviewers
    departmentAssignment: user?.role_name || 'Unknown',
  };
}

/**
 * Utility function to determine if a procedure is in a state that allows resolution elaboration
 * Based on legacy system analysis - these are the core business rules
 */
export function isProcedureInElaborateState(procedure: any): {
  canElaborate: boolean;
  stateReason: string;
} {
  // Legacy rule: Director approval blocks further elaboration
  if (procedure.director_approval === 1) {
    return {
      canElaborate: false,
      stateReason: 'Director has already approved this procedure',
    };
  }

  // Legacy rule: Must be sent to reviewers first
  if (procedure.sent_to_reviewers !== 1) {
    return {
      canElaborate: false,
      stateReason: 'Procedure has not been sent to reviewers yet',
    };
  }

  // Legacy rule: Final states block elaboration
  // Status 1 = pending_review (should ALLOW elaboration)
  // Status 2 = rejected (blocks elaboration)
  // Status 3 = prevention (should ALLOW elaboration)
  // Status 4 = director approved (blocks elaboration)
  // Status 7 = license issued (blocks elaboration)

  if (procedure.status === 2) {
    return {
      canElaborate: false,
      stateReason: 'Procedure is rejected (status 2)',
    };
  }

  if (procedure.status === 4) {
    return {
      canElaborate: false,
      stateReason: 'Procedure is director approved (status 4)',
    };
  }

  if (procedure.status === 7) {
    return {
      canElaborate: false,
      stateReason: 'Procedure license is issued (status 7)',
    };
  }

  // Pending review procedures can be elaborated (status 1)
  if (procedure.status === 1) {
    return {
      canElaborate: true,
      stateReason:
        'Procedure is in pending review state - can elaborate resolution',
    };
  }

  // Prevention procedures can be elaborated (status 3)
  if (procedure.status === 3) {
    return {
      canElaborate: true,
      stateReason:
        'Procedure is in prevention state - can elaborate resolution',
    };
  }

  // Valid states for elaboration: null, 0 (draft)
  if (procedure.status === null || procedure.status === 0) {
    return {
      canElaborate: true,
      stateReason: 'Procedure is in pending state - can elaborate resolution',
    };
  }

  return {
    canElaborate: false,
    stateReason: `Unknown procedure status: ${procedure.status}`,
  };
}

/**
 * Role mapping from new system to legacy system for compatibility
 * This helps maintain consistency with the original button logic
 */
export const LEGACY_ROLE_MAPPING = {
  // Legacy roles from the analysis
  CITIZEN: RoleId.CITIZEN,
  WINDOW: RoleId.COUNTER,
  TECHNICAL_REVIEWER: RoleId.REVIEWER,
  DIRECTOR: RoleId.DIRECTOR,
  SPECIALIZED_DEPT_MIN: RoleId.TECHNICIAN,

  // Modern role mapping helper
  isLegacyTechnicalReviewer: (roleId: number): boolean => {
    // Include predefined reviewer roles
    if (RolePermissions.REVIEWER_ROLE_IDS.includes(roleId)) {
      return true;
    }
    // ALL ROLES > 4 are considered custom/technical reviewers
    if (roleId > RoleId.DIRECTOR) {
      return true;
    }
    return false;
  },

  isLegacyDirector: (roleId: number): boolean => {
    // Admin role IDs are directors
    if (RolePermissions.ADMIN_ROLE_IDS.includes(roleId)) {
      return true;
    }
    // Role ID 1 (CITIZEN) is admin in legacy system
    if (roleId === RoleId.CITIZEN) {
      return true;
    }
    // Role ID 4 (DIRECTOR) is director
    if (roleId === RoleId.DIRECTOR) {
      return true;
    }
    // Specialized departments (roleId > TECHNICIAN) are NOT directors
    if (roleId > RoleId.TECHNICIAN) {
      return false;
    }
    // Other role IDs that can access procedure approvals and are not reviewers
    return (
      roleId > RoleId.COUNTER &&
      RolePermissions.PROCEDURE_APPROVAL_ROLE_IDS.includes(roleId) &&
      !RolePermissions.REVIEWER_ROLE_IDS.includes(roleId)
    );
  },

  isLegacySpecializedDept: (roleId: number): boolean => {
    // Since ALL roles > 4 are now technical reviewers,
    // we don't have specialized departments anymore in this classification
    // Keep this for backward compatibility but always return false
    return false;
  },
} as const;

/**
 * Check if user has specific role by role name
 * @param user - The authenticated user object
 * @param roleType - The type of role to check ('admin', 'director', 'supervisor')
 * @returns boolean - true if user has the specified role type
 */
export function checkRoleByName(
  user: AuthUser | null,
  roleType: 'admin' | 'director' | 'supervisor'
): boolean {
  if (!user?.role_name) {
    return false;
  }

  const roleName = user.role_name.toLowerCase();

  switch (roleType) {
    case 'admin':
      return RolePermissions.ADMIN_ROLES.some(role =>
        roleName.includes(role.toLowerCase())
      );
    case 'director':
      return RolePermissions.DIRECTOR_ROLES.some(role =>
        roleName.includes(role.toLowerCase())
      );
    case 'supervisor':
      return RolePermissions.SUPERVISOR_ROLES.some(role =>
        roleName.includes(role.toLowerCase())
      );
    default:
      return false;
  }
}

/**
 * Get user's role category based on role name
 * @param user - The authenticated user object
 * @returns string - The role category or 'unknown'
 */
export function getUserRoleCategory(user: AuthUser | null): string {
  if (!user) return 'unknown';

  if (checkRoleByName(user, 'admin')) return 'admin';
  if (checkRoleByName(user, 'director')) return 'director';
  if (checkRoleByName(user, 'supervisor')) return 'supervisor';

  return user.role_name || 'unknown';
}
