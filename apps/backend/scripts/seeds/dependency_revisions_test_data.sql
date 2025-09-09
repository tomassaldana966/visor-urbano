-- Dependency Revisions Test Data
-- Insert comprehensive test data for dependency_revisions table
-- This data supports testing of dependency revision router endpoints

-- Clear existing test data
DELETE FROM dependency_revisions WHERE revision_notes LIKE 'TEST-%';

-- Insert comprehensive test data for dependency revisions
INSERT INTO dependency_revisions (
    dependency_id,
    revision_notes,
    revised_at,
    created_at,
    updated_at
) VALUES 
-- Test data for requirements_query_id 2 (multiple revisions showing progression)
(2, 'TEST-REV-001: Initial review - Documentation incomplete. Missing building permits and safety certificates.', 
 '2024-01-15 09:00:00', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),

(2, 'TEST-REV-002: Second review - Building permits submitted but safety certificates still pending. Fire department approval required.', 
 '2024-01-22 14:30:00', '2024-01-22 14:30:00', '2024-01-22 14:30:00'),

(2, 'TEST-REV-003: Third review - All documents submitted. Technical review in progress. Minor corrections needed in structural plans.', 
 '2024-01-29 11:15:00', '2024-01-29 11:15:00', '2024-01-29 11:15:00'),

(2, 'TEST-REV-004: Final review - All requirements met. Approved for next phase. License ready for issuance.', 
 '2024-02-05 16:45:00', '2024-02-05 16:45:00', '2024-02-05 16:45:00'),

-- Test data for requirements_query_id 3 (environmental concerns)
(3, 'TEST-REV-005: Environmental impact assessment required. Property located near protected wetlands. Additional studies needed.', 
 '2024-01-18 10:20:00', '2024-01-18 10:20:00', '2024-01-18 10:20:00'),

(3, 'TEST-REV-006: Environmental studies submitted. Mitigation plan approved. Proceed with standard review process.', 
 '2024-02-01 13:45:00', '2024-02-01 13:45:00', '2024-02-01 13:45:00'),

-- Test data for requirements_query_id 4 (zoning issues)
(4, 'TEST-REV-007: Zoning compliance review - Current zoning allows commercial use but density restrictions apply. Variance may be required.', 
 '2024-01-20 08:30:00', '2024-01-20 08:30:00', '2024-01-20 08:30:00'),

(4, 'TEST-REV-008: Zoning variance approved. Parking requirements modified. Additional landscaping required along street frontage.', 
 '2024-02-03 15:20:00', '2024-02-03 15:20:00', '2024-02-03 15:20:00'),

-- Test data for requirements_query_id 5 (technical issues)
(5, 'TEST-REV-009: Technical review - HVAC system specifications do not meet current building codes. Updated plans required.', 
 '2024-01-25 12:10:00', '2024-01-25 12:10:00', '2024-01-25 12:10:00'),

(5, 'TEST-REV-010: Electrical system review - Load calculations incorrect. Professional engineer certification required.', 
 '2024-01-30 09:45:00', '2024-01-30 09:45:00', '2024-01-30 09:45:00'),

-- Additional test data for various scenarios and edge cases
(2, 'TEST-REV-011: Post-approval revision - Minor modification to façade design. Does not affect structural integrity.', 
 '2024-02-10 14:00:00', '2024-02-10 14:00:00', '2024-02-10 14:00:00'),

(3, 'TEST-REV-012: Compliance check - Site inspection completed. All requirements met according to approved plans.', 
 '2024-02-08 11:30:00', '2024-02-08 11:30:00', '2024-02-08 11:30:00'),

(4, 'TEST-REV-013: Amendment request - Business scope expansion requires additional review. New SCIAN classification needed.', 
 '2024-02-12 16:15:00', '2024-02-12 16:15:00', '2024-02-12 16:15:00'),

(5, 'TEST-REV-014: Emergency revision - Code violation reported. Immediate compliance required for safety systems.', 
 '2024-02-15 08:00:00', '2024-02-15 08:00:00', '2024-02-15 08:00:00'),

-- Test data for different time periods (older revisions)
(2, 'TEST-REV-015: Historical revision - Legacy system migration. Previous approvals verified and documented.', 
 '2023-12-01 10:00:00', '2023-12-01 10:00:00', '2023-12-01 10:00:00'),

(3, 'TEST-REV-016: Annual review - Periodic compliance check. All permits current and valid.', 
 '2023-11-15 14:30:00', '2023-11-15 14:30:00', '2023-11-15 14:30:00'),

-- Test data for recent revisions (current month)
(4, 'TEST-REV-017: Current revision - New accessibility requirements. ADA compliance assessment in progress.', 
 '2024-06-01 09:15:00', '2024-06-01 09:15:00', '2024-06-01 09:15:00'),

(5, 'TEST-REV-018: Latest revision - Digital submission review. Electronic documents verified and accepted.', 
 '2024-06-01 15:45:00', '2024-06-01 15:45:00', '2024-06-01 15:45:00'),

-- Test data for edge cases and special characters
(2, 'TEST-REV-019: Special characters test - Revisión con caracteres especiales: ñáéíóú. Review completed successfully.', 
 '2024-05-28 12:00:00', '2024-05-28 12:00:00', '2024-05-28 12:00:00'),

(3, 'TEST-REV-020: Long note test - This is a very long revision note intended to test the system''s handling of extensive text content. It includes multiple sentences and various punctuation marks to ensure proper storage and retrieval. The note covers several aspects of the review process including technical specifications, compliance requirements, environmental considerations, and administrative procedures. This comprehensive note should help validate the text field capacity and performance under realistic conditions where detailed revision comments are necessary for proper documentation and audit trails.', 
 '2024-05-30 17:30:00', '2024-05-30 17:30:00', '2024-05-30 17:30:00'),

-- Test data for NULL revision_notes (edge case)
(4, NULL, 
 '2024-05-25 10:45:00', '2024-05-25 10:45:00', '2024-05-25 10:45:00'),

-- Test data for empty revision_notes (edge case)
(5, '', 
 '2024-05-26 13:20:00', '2024-05-26 13:20:00', '2024-05-26 13:20:00'),

-- Test data for pagination testing (additional bulk data)
(2, 'TEST-REV-021: Pagination test 1 - Routine review and approval process.', 
 '2024-03-01 09:00:00', '2024-03-01 09:00:00', '2024-03-01 09:00:00'),

(2, 'TEST-REV-022: Pagination test 2 - Standard compliance verification.', 
 '2024-03-02 09:00:00', '2024-03-02 09:00:00', '2024-03-02 09:00:00'),

(2, 'TEST-REV-023: Pagination test 3 - Document review and processing.', 
 '2024-03-03 09:00:00', '2024-03-03 09:00:00', '2024-03-03 09:00:00'),

(3, 'TEST-REV-024: Pagination test 4 - Environmental assessment follow-up.', 
 '2024-03-04 09:00:00', '2024-03-04 09:00:00', '2024-03-04 09:00:00'),

(3, 'TEST-REV-025: Pagination test 5 - Safety inspection completed.', 
 '2024-03-05 09:00:00', '2024-03-05 09:00:00', '2024-03-05 09:00:00'),

(4, 'TEST-REV-026: Pagination test 6 - Zoning verification process.', 
 '2024-03-06 09:00:00', '2024-03-06 09:00:00', '2024-03-06 09:00:00'),

(4, 'TEST-REV-027: Pagination test 7 - Technical specifications review.', 
 '2024-03-07 09:00:00', '2024-03-07 09:00:00', '2024-03-07 09:00:00'),

(5, 'TEST-REV-028: Pagination test 8 - Final approval documentation.', 
 '2024-03-08 09:00:00', '2024-03-08 09:00:00', '2024-03-08 09:00:00'),

(5, 'TEST-REV-029: Pagination test 9 - Post-approval monitoring.', 
 '2024-03-09 09:00:00', '2024-03-09 09:00:00', '2024-03-09 09:00:00'),

(2, 'TEST-REV-030: Pagination test 10 - Archive and documentation.', 
 '2024-03-10 09:00:00', '2024-03-10 09:00:00', '2024-03-10 09:00:00');

-- Insert additional test data for comprehensive endpoint testing
INSERT INTO dependency_revisions (
    dependency_id,
    revision_notes,
    revised_at,
    created_at,
    updated_at
) VALUES 
-- Data for filtering tests by dependency_id
(3, 'TEST-FILTER-001: Filter test for dependency_id 3 - Environmental compliance verified.', 
 '2024-04-01 10:00:00', '2024-04-01 10:00:00', '2024-04-01 10:00:00'),

(3, 'TEST-FILTER-002: Filter test for dependency_id 3 - Additional environmental documentation.', 
 '2024-04-02 10:00:00', '2024-04-02 10:00:00', '2024-04-02 10:00:00'),

(4, 'TEST-FILTER-003: Filter test for dependency_id 4 - Zoning compliance documentation.', 
 '2024-04-03 10:00:00', '2024-04-03 10:00:00', '2024-04-03 10:00:00'),

-- Data for date range testing
(2, 'TEST-DATE-RANGE-001: Date range test - Early 2024 revision.', 
 '2024-01-01 08:00:00', '2024-01-01 08:00:00', '2024-01-01 08:00:00'),

(2, 'TEST-DATE-RANGE-002: Date range test - Mid 2024 revision.', 
 '2024-03-15 12:00:00', '2024-03-15 12:00:00', '2024-03-15 12:00:00'),

(2, 'TEST-DATE-RANGE-003: Date range test - Recent 2024 revision.', 
 '2024-05-31 18:00:00', '2024-05-31 18:00:00', '2024-05-31 18:00:00'),

-- Data for search functionality testing
(5, 'TEST-SEARCH-001: Search test containing keyword URGENT for priority handling.', 
 '2024-04-10 14:00:00', '2024-04-10 14:00:00', '2024-04-10 14:00:00'),

(5, 'TEST-SEARCH-002: Search test containing keyword APPROVED for status tracking.', 
 '2024-04-11 14:00:00', '2024-04-11 14:00:00', '2024-04-11 14:00:00'),

(5, 'TEST-SEARCH-003: Search test containing keyword REJECTED for negative cases.', 
 '2024-04-12 14:00:00', '2024-04-12 14:00:00', '2024-04-12 14:00:00');

COMMIT;
