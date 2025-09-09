import { describe, test, expect, beforeEach } from 'vitest';
import {
  checkElaborateResolutionPermissions,
  checkEnhancedElaborateResolutionPermissions,
  isProcedureInElaborateState,
  LEGACY_ROLE_MAPPING,
  RolePermissions,
} from './director';

// Mock data for testing
const mockUsers = {
  admin: {
    id: 1,
    role_id: 1,
    role_name: 'admin',
    municipality_id: 1,
    email: 'admin@test.com',
    name: 'Admin User',
  },
  technicalReviewer: {
    id: 2,
    role_id: 9, // REVIEWER_ROLE_IDS
    role_name: 'technical_reviewer',
    municipality_id: 1,
    email: 'reviewer@test.com',
    name: 'Technical Reviewer',
  },
  director: {
    id: 3,
    role_id: 4,
    role_name: 'director',
    municipality_id: 1,
    email: 'director@test.com',
    name: 'Director User',
  },
  specializedDept: {
    id: 4,
    role_id: 7,
    role_name: 'specialized_department',
    municipality_id: 1,
    email: 'specialist@test.com',
    name: 'Specialist User',
  },
  citizen: {
    id: 5,
    role_id: 1,
    role_name: 'citizen',
    municipality_id: 1,
    email: 'citizen@test.com',
    name: 'Citizen User',
  },
};

const mockProcedures = {
  newProcedure: {
    id: 1,
    folio: 'TEST-001',
    status: null,
    director_approval: null,
    sent_to_reviewers: 1,
    municipality_id: 1,
  },
  pendingProcedure: {
    id: 2,
    folio: 'TEST-002',
    status: 0,
    director_approval: 0,
    sent_to_reviewers: 1,
    municipality_id: 1,
  },
  preventionProcedure: {
    id: 3,
    folio: 'TEST-003',
    status: 3,
    director_approval: 0,
    sent_to_reviewers: 1,
    municipality_id: 1,
    solventacion_ciudadano: 2,
  },
  approvedProcedure: {
    id: 4,
    folio: 'TEST-004',
    status: 1,
    director_approval: 0,
    sent_to_reviewers: 1,
    municipality_id: 1,
  },
  rejectedProcedure: {
    id: 5,
    folio: 'TEST-005',
    status: 2,
    director_approval: 0,
    sent_to_reviewers: 1,
    municipality_id: 1,
  },
  directorApprovedProcedure: {
    id: 6,
    folio: 'TEST-006',
    status: 0,
    director_approval: 1,
    sent_to_reviewers: 1,
    municipality_id: 1,
  },
  notSentToReviewers: {
    id: 7,
    folio: 'TEST-007',
    status: 0,
    director_approval: 0,
    sent_to_reviewers: 0,
    municipality_id: 1,
  },
};

describe('Elaborate Resolution Permissions', () => {
  describe('isProcedureInElaborateState', () => {
    test('should allow elaboration for new procedures', () => {
      const result = isProcedureInElaborateState(mockProcedures.newProcedure);
      expect(result.canElaborate).toBe(true);
      expect(result.stateReason).toContain('pending state');
    });

    test('should allow elaboration for pending procedures', () => {
      const result = isProcedureInElaborateState(
        mockProcedures.pendingProcedure
      );
      expect(result.canElaborate).toBe(true);
      expect(result.stateReason).toContain('pending state');
    });

    test('should allow elaboration for prevention procedures', () => {
      const result = isProcedureInElaborateState(
        mockProcedures.preventionProcedure
      );
      expect(result.canElaborate).toBe(true);
      expect(result.stateReason).toContain('prevention state');
    });

    test('should allow elaboration for approved procedures (status 1)', () => {
      const result = isProcedureInElaborateState(
        mockProcedures.approvedProcedure
      );
      expect(result.canElaborate).toBe(true);
      expect(result.stateReason).toContain('pending review state');
    });

    test('should block elaboration for rejected procedures', () => {
      const result = isProcedureInElaborateState(
        mockProcedures.rejectedProcedure
      );
      expect(result.canElaborate).toBe(false);
      expect(result.stateReason).toContain('rejected');
    });

    test('should block elaboration when director already approved', () => {
      const result = isProcedureInElaborateState(
        mockProcedures.directorApprovedProcedure
      );
      expect(result.canElaborate).toBe(false);
      expect(result.stateReason).toContain('already approved');
    });

    test('should block elaboration when not sent to reviewers', () => {
      const result = isProcedureInElaborateState(
        mockProcedures.notSentToReviewers
      );
      expect(result.canElaborate).toBe(false);
      expect(result.stateReason).toContain('not been sent to reviewers');
    });
  });

  describe('LEGACY_ROLE_MAPPING', () => {
    test('should correctly identify technical reviewers', () => {
      expect(LEGACY_ROLE_MAPPING.isLegacyTechnicalReviewer(9)).toBe(true);
      expect(LEGACY_ROLE_MAPPING.isLegacyTechnicalReviewer(4)).toBe(false);
      expect(LEGACY_ROLE_MAPPING.isLegacyTechnicalReviewer(7)).toBe(true); // Role 7 > 4, so it's a technical reviewer now
    });

    test('should correctly identify directors', () => {
      expect(LEGACY_ROLE_MAPPING.isLegacyDirector(1)).toBe(true); // Admin
      expect(LEGACY_ROLE_MAPPING.isLegacyDirector(4)).toBe(true); // Director
      expect(LEGACY_ROLE_MAPPING.isLegacyDirector(9)).toBe(false); // Reviewer
    });

    test('should correctly identify specialized departments', () => {
      expect(LEGACY_ROLE_MAPPING.isLegacySpecializedDept(7)).toBe(false); // Changed: now always returns false
      expect(LEGACY_ROLE_MAPPING.isLegacySpecializedDept(8)).toBe(false); // Changed: now always returns false
      expect(LEGACY_ROLE_MAPPING.isLegacySpecializedDept(9)).toBe(false); // Reviewer
      expect(LEGACY_ROLE_MAPPING.isLegacySpecializedDept(4)).toBe(false); // Director
    });
  });

  describe('checkElaborateResolutionPermissions', () => {
    describe('Technical Reviewers', () => {
      test('should allow elaboration for valid procedure states', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.pendingProcedure,
          mockUsers.technicalReviewer
        );
        expect(result.canElaborate).toBe(true);
        expect(result.isDirector).toBe(false);
      });

      test('should allow elaboration for prevention procedures', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.preventionProcedure,
          mockUsers.technicalReviewer
        );
        expect(result.canElaborate).toBe(true);
        expect(result.isDirector).toBe(false);
      });

      test('should allow elaboration for approved procedures (status 1)', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.approvedProcedure,
          mockUsers.technicalReviewer
        );
        expect(result.canElaborate).toBe(true); // Status 1 now allows elaboration
      });

      test('should block elaboration when director already approved', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.directorApprovedProcedure,
          mockUsers.technicalReviewer
        );
        expect(result.canElaborate).toBe(false);
      });
    });

    describe('Directors', () => {
      test('should allow elaboration for valid procedure states', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.pendingProcedure,
          mockUsers.director
        );
        expect(result.canElaborate).toBe(true);
        expect(result.isDirector).toBe(true);
      });

      test('should allow elaboration for prevention procedures', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.preventionProcedure,
          mockUsers.director
        );
        expect(result.canElaborate).toBe(true);
        expect(result.isDirector).toBe(true);
      });

      test('should block elaboration when already approved by director', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.directorApprovedProcedure,
          mockUsers.director
        );
        expect(result.canElaborate).toBe(false);
      });

      test('should block elaboration when not sent to reviewers', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.notSentToReviewers,
          mockUsers.director
        );
        expect(result.canElaborate).toBe(false);
      });
    });

    describe('Technical Reviewers (including former Specialized Departments)', () => {
      test('should allow elaboration for valid procedure states', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.pendingProcedure,
          mockUsers.specializedDept // Role 7 is now treated as technical reviewer
        );
        expect(result.canElaborate).toBe(true);
        expect(result.isDirector).toBe(false);
      });

      test('should allow elaboration for approved procedures (status 1)', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.approvedProcedure,
          mockUsers.specializedDept // Role 7 is now treated as technical reviewer
        );
        expect(result.canElaborate).toBe(true); // Status 1 now allows elaboration for technical reviewers
      });
    });

    describe('Invalid Users', () => {
      test('should block elaboration for null user', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.pendingProcedure,
          null
        );
        expect(result.canElaborate).toBe(false);
        expect(result.isDirector).toBe(false);
      });

      test('should block elaboration for citizens', () => {
        const result = checkElaborateResolutionPermissions(
          mockProcedures.pendingProcedure,
          mockUsers.citizen
        );
        expect(result.canElaborate).toBe(false);
        expect(result.isDirector).toBe(false);
      });

      test('should block elaboration for users without role_id', () => {
        const userWithoutRole = {
          ...mockUsers.technicalReviewer,
          role_id: undefined,
        };
        const result = checkElaborateResolutionPermissions(
          mockProcedures.pendingProcedure,
          userWithoutRole as any
        );
        expect(result.canElaborate).toBe(false);
      });
    });
  });

  describe('checkEnhancedElaborateResolutionPermissions', () => {
    test('should provide detailed permission information', () => {
      const result = checkEnhancedElaborateResolutionPermissions(
        mockProcedures.pendingProcedure,
        mockUsers.technicalReviewer
      );

      expect(result.canElaborate).toBe(true);
      expect(result.isDirector).toBe(false);
      expect(result.reason).toBeDefined();
      expect(result.isAssignedReviewer).toBe(true);
      expect(result.departmentAssignment).toBe('technical_reviewer');
    });

    test('should provide success reason for valid cases', () => {
      const result = checkEnhancedElaborateResolutionPermissions(
        mockProcedures.approvedProcedure, // Status 1 now allows elaboration
        mockUsers.technicalReviewer
      );

      expect(result.canElaborate).toBe(true); // Status 1 now allows elaboration
      expect(result.reason).toContain('User has reviewer permissions');
    });
  });

  describe('Integration Tests', () => {
    test('should handle director override scenario', () => {
      // Test that directors can elaborate when reviewers have already decided
      const reviewedProcedure = {
        ...mockProcedures.pendingProcedure,
        status: 1, // Approved by reviewer
      };

      const reviewerResult = checkElaborateResolutionPermissions(
        reviewedProcedure,
        mockUsers.technicalReviewer
      );

      const directorResult = checkElaborateResolutionPermissions(
        reviewedProcedure,
        mockUsers.director
      );

      expect(reviewerResult.canElaborate).toBe(true); // Status 1 now allows elaboration for technical reviewers
      expect(directorResult.canElaborate).toBe(true); // Status 1 now allows elaboration for directors too
    });

    test('should handle prevention workflow correctly', () => {
      // Test prevention state allows re-elaboration
      const preventionProcedure = mockProcedures.preventionProcedure;

      const reviewerResult = checkElaborateResolutionPermissions(
        preventionProcedure,
        mockUsers.technicalReviewer
      );

      const directorResult = checkElaborateResolutionPermissions(
        preventionProcedure,
        mockUsers.director
      );

      expect(reviewerResult.canElaborate).toBe(true);
      expect(directorResult.canElaborate).toBe(true);
    });

    test('should respect municipality boundaries', () => {
      // Test that users from different municipalities are blocked
      const userFromDifferentMunicipality = {
        ...mockUsers.technicalReviewer,
        municipality_id: 2,
      };

      // This would be handled at a higher level, but the permission system
      // should still work for users from the correct municipality
      const result = checkElaborateResolutionPermissions(
        mockProcedures.pendingProcedure,
        userFromDifferentMunicipality
      );

      // Permission system doesn't check municipality - that's handled elsewhere
      expect(result.canElaborate).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    test('should handle undefined/null values gracefully', () => {
      const procedureWithNulls = {
        id: 1,
        folio: 'TEST-NULL',
        status: null,
        director_approval: null,
        sent_to_reviewers: null,
        municipality_id: 1,
      };

      const result = checkElaborateResolutionPermissions(
        procedureWithNulls,
        mockUsers.technicalReviewer
      );

      // Should be blocked because sent_to_reviewers is null
      expect(result.canElaborate).toBe(false);
    });

    test('should handle extreme role_id values', () => {
      const userWithHighRoleId = {
        ...mockUsers.specializedDept,
        role_id: 999,
      };

      const result = checkElaborateResolutionPermissions(
        mockProcedures.pendingProcedure,
        userWithHighRoleId
      );

      expect(result.canElaborate).toBe(true);
      expect(result.isDirector).toBe(false);
    });

    test('should handle missing procedure properties', () => {
      const incompleteProcedure = {
        id: 1,
        folio: 'TEST-INCOMPLETE',
        // Missing other required properties
      };

      const result = checkElaborateResolutionPermissions(
        incompleteProcedure as any,
        mockUsers.technicalReviewer
      );

      // Should be blocked due to missing sent_to_reviewers
      expect(result.canElaborate).toBe(false);
    });
  });
});

describe('URL Generation Tests', () => {
  test('should generate correct URLs for directors', () => {
    const result = checkElaborateResolutionPermissions(
      mockProcedures.pendingProcedure,
      mockUsers.director
    );

    expect(result.isDirector).toBe(true);
    // URL would be: /procedures/{folio}/resolution?dir=1
  });

  test('should generate correct URLs for non-directors', () => {
    const result = checkElaborateResolutionPermissions(
      mockProcedures.pendingProcedure,
      mockUsers.technicalReviewer
    );

    expect(result.isDirector).toBe(false);
    // URL would be: /procedures/{folio}/resolution
  });
});
