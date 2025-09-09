-- Dependency Reviews Test Data
-- Insert test data for dependency reviews endpoints

-- Clear existing test data
DELETE FROM dependency_reviews WHERE folio LIKE 'TEST-%';

-- Insert test dependency reviews
INSERT INTO dependency_reviews (
    procedure_id,
    municipality_id,
    folio,
    role,
    start_date,
    update_date,
    current_status,
    current_file,
    signature,
    user_id,
    created_at,
    updated_at
) VALUES 
-- Test data for different roles and statuses
(1, 1, 'TEST-DR-001', 1, '2024-01-15 09:00:00', '2024-01-15 09:00:00', 1, 'file_001.pdf', 'signature_001', NULL, '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
(2, 1, 'TEST-DR-002', 2, '2024-01-16 10:30:00', '2024-01-16 14:20:00', 2, 'file_002.pdf', 'signature_002', NULL, '2024-01-16 10:30:00', '2024-01-16 14:20:00'),
(3, 2, 'TEST-DR-003', 1, '2024-01-17 11:45:00', '2024-01-17 16:15:00', 3, 'file_003.pdf', 'signature_003', NULL, '2024-01-17 11:45:00', '2024-01-17 16:15:00'),
(1, 2, 'TEST-DR-004', 3, '2024-01-18 08:20:00', '2024-01-18 12:40:00', 1, 'file_004.pdf', 'signature_004', NULL, '2024-01-18 08:20:00', '2024-01-18 12:40:00'),
(2, 3, 'TEST-DR-005', 2, '2024-01-19 13:15:00', '2024-01-19 17:30:00', 2, 'file_005.pdf', 'signature_005', NULL, '2024-01-19 13:15:00', '2024-01-19 17:30:00'),

-- More test data for different months and years for line_time_admin endpoint
(1, 1, 'TEST-DR-006', 1, '2024-02-01 09:00:00', '2024-02-01 09:00:00', 1, 'file_006.pdf', 'signature_006', NULL, '2024-02-01 09:00:00', '2024-02-01 09:00:00'),
(2, 1, 'TEST-DR-007', 2, '2024-02-15 10:30:00', '2024-02-15 14:20:00', 2, 'file_007.pdf', 'signature_007', NULL, '2024-02-15 10:30:00', '2024-02-15 14:20:00'),
(3, 2, 'TEST-DR-008', 1, '2024-03-01 11:45:00', '2024-03-01 16:15:00', 3, 'file_008.pdf', 'signature_008', NULL, '2024-03-01 11:45:00', '2024-03-01 16:15:00'),
(1, 2, 'TEST-DR-009', 3, '2024-03-15 08:20:00', '2024-03-15 12:40:00', 1, 'file_009.pdf', 'signature_009', NULL, '2024-03-15 08:20:00', '2024-03-15 12:40:00'),
(2, 3, 'TEST-DR-010', 2, '2024-04-01 13:15:00', '2024-04-01 17:30:00', 2, 'file_010.pdf', 'signature_010', NULL, '2024-04-01 13:15:00', '2024-04-01 17:30:00'),

-- Test data for 2023 (different year)
(1, 1, 'TEST-DR-011', 1, '2023-12-01 09:00:00', '2023-12-01 09:00:00', 1, 'file_011.pdf', 'signature_011', NULL, '2023-12-01 09:00:00', '2023-12-01 09:00:00'),
(2, 1, 'TEST-DR-012', 2, '2023-12-15 10:30:00', '2023-12-15 14:20:00', 2, 'file_012.pdf', 'signature_012', NULL, '2023-12-15 10:30:00', '2023-12-15 14:20:00'),
(3, 2, 'TEST-DR-013', 1, '2023-11-01 11:45:00', '2023-11-01 16:15:00', 3, 'file_013.pdf', 'signature_013', NULL, '2023-11-01 11:45:00', '2023-11-01 16:15:00'),
(1, 2, 'TEST-DR-014', 3, '2023-11-15 08:20:00', '2023-11-15 12:40:00', 1, 'file_014.pdf', 'signature_014', NULL, '2023-11-15 08:20:00', '2023-11-15 12:40:00'),
(2, 3, 'TEST-DR-015', 2, '2023-10-01 13:15:00', '2023-10-01 17:30:00', 2, 'file_015.pdf', 'signature_015', NULL, '2023-10-01 13:15:00', '2023-10-01 17:30:00'),

-- Test data with NULL values for edge cases
(1, 1, 'TEST-DR-016', 1, NULL, NULL, NULL, NULL, NULL, NULL, '2024-05-01 09:00:00', '2024-05-01 09:00:00'),
(2, 2, 'TEST-DR-017', 2, '2024-05-02 10:00:00', NULL, 1, 'file_017.pdf', NULL, NULL, '2024-05-02 10:00:00', '2024-05-02 10:00:00'),

-- Test data for different municipalities and procedures
(1, 19, 'TEST-DR-018', 1, '2024-05-03 08:00:00', '2024-05-03 12:00:00', 2, 'file_018.pdf', 'signature_018', NULL, '2024-05-03 08:00:00', '2024-05-03 12:00:00'),
(4, 19, 'TEST-DR-019', 3, '2024-05-04 09:30:00', '2024-05-04 15:45:00', 3, 'file_019.pdf', 'signature_019', NULL, '2024-05-04 09:30:00', '2024-05-04 15:45:00'),
(5, 1, 'TEST-DR-020', 2, '2024-05-05 11:00:00', '2024-05-05 16:30:00', 1, 'file_020.pdf', 'signature_020', NULL, '2024-05-05 11:00:00', '2024-05-05 16:30:00');

-- Insert some test data for technical_sheet_downloads table with correct structure
INSERT INTO technical_sheet_downloads (
    city,
    email,
    age,
    name,
    sector,
    uses,
    municipality_id,
    address,
    created_at,
    updated_at
) VALUES 
('Test City 1', 'test1@example.com', '25-35', 'John Doe', 'Commercial', 'Restaurant operations', 1, '123 Main St', '2024-01-15 10:00:00', '2024-01-15 10:00:00'),
('Test City 2', 'test2@example.com', '35-45', 'Jane Smith', 'Industrial', 'Manufacturing', 2, '456 Industrial Blvd', '2024-01-16 11:00:00', '2024-01-16 11:00:00'),
('Test City 3', 'test3@example.com', '45-55', 'Bob Johnson', 'Residential', 'Housing development', 3, '789 Residential Ave', '2024-01-17 12:00:00', '2024-01-17 12:00:00'),
('Test City 4', 'test4@example.com', '25-35', 'Alice Brown', 'Commercial', 'Retail store', 19, '321 Commerce St', '2024-01-18 13:00:00', '2024-01-18 13:00:00'),
('Test City 5', 'test5@example.com', '35-45', 'Charlie Wilson', 'Mixed', 'Office and retail complex', 2, '654 Mixed Use Rd', '2024-01-19 14:00:00', '2024-01-19 14:00:00');

-- Commit the transaction
COMMIT;
