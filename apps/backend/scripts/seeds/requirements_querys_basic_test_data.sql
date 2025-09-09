-- Requirements Querys Test Data
-- Basic test data for requirements_querys table to support dependency revisions testing

-- Insert basic requirements_querys test data
INSERT INTO requirements_querys (
    folio,
    street,
    neighborhood,
    municipality_name,
    municipality_id,
    scian_code,
    scian_name,
    property_area,
    activity_area,
    applicant_name,
    applicant_character,
    person_type,
    minimap_url,
    restrictions,
    status,
    user_id,
    created_at,
    updated_at,
    year_folio,
    alcohol_sales,
    primary_folio
) VALUES 
-- Test requirements query 1
('TEST-RQ-001', 'Av. Principal 123', 'Centro', 'Test Municipality', 1, '722513', 'Restaurantes con servicio de preparación de alimentos a la carta o de comida corrida', 150.50, 120.00, 'Juan Pérez García', 'Propietario', 'Física', 'https://maps.example.com/test1', '{}', 1, 1, '2024-01-01 10:00:00', '2024-01-01 10:00:00', 2024, 0, 'TEST-RQ-001-2024'),

-- Test requirements query 2
('TEST-RQ-002', 'Calle Comercio 456', 'Industrial', 'Test Municipality', 1, '465211', 'Comercio al por menor de ferretería y tlapalería', 250.75, 200.00, 'María López Rodríguez', 'Representante Legal', 'Moral', 'https://maps.example.com/test2', '{"parking": true, "loading_zone": true}', 1, 1, '2024-01-05 11:00:00', '2024-01-05 11:00:00', 2024, 0, 'TEST-RQ-002-2024'),

-- Test requirements query 3
('TEST-RQ-003', 'Boulevard Norte 789', 'Residencial', 'Test Municipality', 1, '811219', 'Otros servicios de limpieza', 100.25, 80.00, 'Carlos Martínez Silva', 'Propietario', 'Física', 'https://maps.example.com/test3', '{"noise_restrictions": true}', 1, 1, '2024-01-10 12:00:00', '2024-01-10 12:00:00', 2024, 0, 'TEST-RQ-003-2024'),

-- Test requirements query 4
('TEST-RQ-004', 'Av. Turística 321', 'Zona Turística', 'Test Municipality', 1, '722412', 'Centros nocturnos, bares, cantinas y similares', 300.00, 250.00, 'Ana Fernández Torres', 'Representante Legal', 'Moral', 'https://maps.example.com/test4', '{"alcohol_license": true, "noise_permit": true}', 1, 1, '2024-01-15 13:00:00', '2024-01-15 13:00:00', 2024, 1, 'TEST-RQ-004-2024');

COMMIT;
