-- Provisional Openings Test Data
-- Insert fake data for testing provisional openings endpoints

-- First, ensure we have test municipalities and users
-- (These should already exist, but we'll insert if they don't)

-- Insert test municipalities if they don't exist
INSERT INTO municipalities (id, name, image, director, process_sheet, solving_days, issue_license, address, phone, responsible_area, created_at, updated_at) 
VALUES 
(1, 'Guadalajara', 'https://example.com/guadalajara.jpg', 'Juan Pérez González', 1, 15, 1, 'Av. Hidalgo 400, Centro', '33-3333-3333', 'Dirección de Desarrollo Urbano', NOW(), NOW()),
(2, 'Zapopan', 'https://example.com/zapopan.jpg', 'María López Sánchez', 1, 10, 1, 'Av. López Mateos 1600', '33-4444-4444', 'Secretaría de Desarrollo Urbano', NOW(), NOW()),
(3, 'Tlaquepaque', 'https://example.com/tlaquepaque.jpg', 'Carlos Ruiz Mendoza', 1, 12, 1, 'Av. Revolución 115', '33-5555-5555', 'Urbanismo y Obras Públicas', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert test users if they don't exist
INSERT INTO users (id, name, paternal_last_name, maternal_last_name, cellphone, email, password, municipality_id, created_at, updated_at, is_active) 
VALUES 
(1, 'Carlos', 'González', 'López', '33-1111-1111', 'carlos.gonzalez@municipio.gob.mx', '$2b$12$LQv3c1yqBwBHV9Z', 1, NOW(), NOW(), true),
(2, 'Ana', 'Martínez', 'Ruiz', '33-2222-2222', 'ana.martinez@municipio.gob.mx', '$2b$12$LQv3c1yqBwBHV9Z', 1, NOW(), NOW(), true),
(3, 'Roberto', 'Jiménez', 'Castro', '33-3333-3333', 'roberto.jimenez@municipio.gob.mx', '$2b$12$LQv3c1yqBwBHV9Z', 2, NOW(), NOW(), true),
(4, 'María', 'Hernández', 'Silva', '33-4444-4444', 'maria.hernandez@municipio.gob.mx', '$2b$12$LQv3c1yqBwBHV9Z', 2, NOW(), NOW(), true),
(5, 'Luis', 'Rodríguez', 'Morales', '33-5555-5555', 'luis.rodriguez@municipio.gob.mx', '$2b$12$LQv3c1yqBwBHV9Z', 3, NOW(), NOW(), true),
(6, 'Carmen', 'López', 'Vega', '33-6666-6666', 'carmen.lopez@municipio.gob.mx', '$2b$12$LQv3c1yqBwBHV9Z', 1, NOW(), NOW(), true)
ON CONFLICT (id) DO NOTHING;

-- Insert test procedures if they don't exist
INSERT INTO procedures (id, folio, status, procedure_type, created_at, updated_at) 
VALUES 
(1, 'PROC-001', 1, 'Commercial License', NOW(), NOW()),
(2, 'PROC-002', 1, 'Industrial License', NOW(), NOW()),
(3, 'PROC-003', 1, 'Service License', NOW(), NOW()),
(4, 'PROC-004', 1, 'Food Service License', NOW(), NOW()),
(5, 'PROC-005', 1, 'Automotive Service', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert provisional openings test data
INSERT INTO provisional_openings (
    folio,
    procedure_id,
    counter,
    granted_by_user_id,
    granted_role,
    start_date,
    end_date,
    status,
    municipality_id,
    created_by,
    created_at,
    updated_at
) VALUES 
-- Active Provisional Opening #1 - Restaurant (Municipality 1)
(
    'QU9ELTAwMS0yMDI0', -- Base64 encoded: 'APO-001-2024'
    1,
    1001,
    1,
    1,
    '2024-12-01 08:00:00',
    '2025-01-31 18:00:00',
    1,
    1,
    1,
    NOW(),
    NOW()
),
-- Active Provisional Opening #2 - Pharmacy (Municipality 1) 
(
    'QU9ELTAwMi0yMDI0', -- Base64 encoded: 'APO-002-2024'
    1,
    1002,
    2,
    1,
    '2024-12-05 09:00:00',
    '2025-02-05 17:00:00',
    1,
    1,
    2,
    NOW(),
    NOW()
),
-- Active Provisional Opening #3 - Auto Repair Shop (Municipality 2)
(
    'QU9ELTAwMy0yMDI0', -- Base64 encoded: 'APO-003-2024'
    5,
    2001,
    3,
    1,
    '2024-12-10 07:30:00',
    '2025-02-10 18:30:00',
    1,
    2,
    3,
    NOW(),
    NOW()
),
-- Expired Provisional Opening #4 - Coffee Shop (Municipality 1)
(
    'QU9ELTAwNC0yMDI0', -- Base64 encoded: 'APO-004-2024'
    3,
    1003,
    1,
    1,
    '2024-10-01 08:00:00',
    '2024-11-30 20:00:00',
    0,
    1,
    1,
    '2024-10-01 10:15:00',
    '2024-11-30 20:00:00'
),
-- Near Expiry Provisional Opening #5 - Beauty Salon (Municipality 2)
(
    'QU9ELTAwNS0yMDI0', -- Base64 encoded: 'APO-005-2024'
    3,
    2002,
    4,
    1,
    '2024-12-15 09:00:00',
    '2025-01-15 19:00:00',
    1,
    2,
    4,
    NOW(),
    NOW()
),
-- Active Provisional Opening #6 - Grocery Store (Municipality 3)
(
    'QU9ELTAwNi0yMDI0', -- Base64 encoded: 'APO-006-2024'
    1,
    3001,
    5,
    1,
    '2024-12-20 06:00:00',
    '2025-03-20 22:00:00',
    1,
    3,
    5,
    NOW(),
    NOW()
),
-- Suspended Provisional Opening #7 - Bar (Municipality 1)
(
    'QU9ELTAwNy0yMDI0', -- Base64 encoded: 'APO-007-2024'
    1,
    1004,
    2,
    1,
    '2024-11-15 18:00:00',
    '2025-01-15 02:00:00',
    2,
    1,
    2,
    '2024-11-15 20:30:00',
    NOW()
),
-- Active Provisional Opening #8 - Hardware Store (Municipality 2)
(
    'QU9ELTAwOC0yMDI0', -- Base64 encoded: 'APO-008-2024'
    1,
    2003,
    3,
    1,
    '2024-12-22 08:30:00',
    '2025-04-22 19:30:00',
    1,
    2,
    3,
    NOW(),
    NOW()
),
-- Cancelled Provisional Opening #9 - Bakery (Municipality 3)
(
    'QU9ELTAwOS0yMDI0', -- Base64 encoded: 'APO-009-2024'
    4,
    3002,
    5,
    1,
    '2024-11-01 05:00:00',
    '2024-12-31 21:00:00',
    3,
    3,
    5,
    '2024-11-01 08:45:00',
    '2024-12-01 14:20:00'
),
-- Active Provisional Opening #10 - Electronics Store (Municipality 1)
(
    'QU9ELTAxMC0yMDI0', -- Base64 encoded: 'APO-010-2024'
    1,
    1005,
    1,
    1,
    '2024-12-25 10:00:00',
    '2025-05-25 20:00:00',
    1,
    1,
    1,
    NOW(),
    NOW()
),
-- Active Provisional Opening #11 - Dental Clinic (Municipality 2)
(
    'QU9ELTAxMS0yMDI0', -- Base64 encoded: 'APO-011-2024'
    3,
    2004,
    4,
    1,
    '2024-12-28 07:00:00',
    '2025-03-28 19:00:00',
    1,
    2,
    4,
    NOW(),
    NOW()
),
-- Recently Expired #12 - Fitness Center (Municipality 3)
(
    'QU9ELTAxMi0yMDI0', -- Base64 encoded: 'APO-012-2024'
    3,
    3003,
    5,
    1,
    '2024-09-15 06:00:00',
    '2024-12-15 22:00:00',
    0,
    3,
    5,
    '2024-09-15 11:30:00',
    '2024-12-15 22:00:00'
),
-- Under Review #13 - Laundromat (Municipality 1)
(
    'QU9ELTAxMy0yMDI0', -- Base64 encoded: 'APO-013-2024'
    3,
    1006,
    2,
    1,
    '2025-01-01 08:00:00',
    '2025-06-01 20:00:00',
    4,
    1,
    2,
    NOW(),
    NOW()
),
-- Active Long-term #14 - Warehouse (Municipality 2)
(
    'QU9ELTAxNC0yMDI0', -- Base64 encoded: 'APO-014-2024'
    2,
    2005,
    3,
    1,
    '2024-12-01 07:00:00',
    '2025-12-01 18:00:00',
    1,
    2,
    3,
    NOW(),
    NOW()
),
-- Active Recent #15 - Print Shop (Municipality 3)
(
    'QU9ELTAxNS0yMDI0', -- Base64 encoded: 'APO-015-2024'
    1,
    3004,
    5,
    1,
    '2024-12-30 09:00:00',
    '2025-03-30 18:00:00',
    1,
    3,
    5,
    NOW(),
    NOW()
);

-- Additional test data for edge cases and comprehensive testing

-- Test cases with different status values:
-- Status 0: Expired/Inactive
-- Status 1: Active  
-- Status 2: Suspended
-- Status 3: Cancelled
-- Status 4: Under Review/Pending

-- Test data includes:
-- - Different municipalities (1, 2, 3)
-- - Different procedures (1-5)
-- - Different users as granted_by and created_by
-- - Different date ranges (past, current, future)
-- - Various statuses for comprehensive endpoint testing
-- - Base64 encoded folios for testing decoding functionality

-- Update sequence if needed (handle case where sequence might not exist)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'provisional_openings_id_seq') THEN
        PERFORM setval('provisional_openings_id_seq', (SELECT COALESCE(MAX(id), 0) FROM provisional_openings) + 1, false);
    END IF;
END
$$;
