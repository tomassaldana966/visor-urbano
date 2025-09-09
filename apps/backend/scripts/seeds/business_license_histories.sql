-- Test data for business_license_histories table
-- This file contains fake data for testing the business license histories endpoints

-- Insert test municipalities if they don't exist
INSERT INTO municipalities (id, name, image, director, process_sheet, solving_days, issue_license, address, phone, responsible_area, created_at, updated_at) 
VALUES 
(1, 'Guadalajara', 'https://example.com/guadalajara.jpg', 'Juan Pérez González', 1, 15, 1, 'Av. Hidalgo 400, Centro', '33-3333-3333', 'Dirección de Desarrollo Urbano', NOW(), NOW()),
(2, 'Zapopan', 'https://example.com/zapopan.jpg', 'María López Sánchez', 1, 10, 1, 'Av. López Mateos 1600', '33-4444-4444', 'Secretaría de Desarrollo Urbano', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert test business license histories
INSERT INTO business_license_histories (
    license_folio, 
    issue_date, 
    business_line, 
    detailed_description,
    business_line_code, 
    business_area,
    street,
    exterior_number,
    interior_number,
    neighborhood,
    cadastral_key,
    reference,
    coordinate_x,
    coordinate_y,
    owner_first_name, 
    owner_last_name_p, 
    owner_last_name_m,
    user_tax_id,
    national_id,
    owner_phone,
    business_name,
    owner_email,
    owner_street,
    owner_exterior_number,
    owner_interior_number,
    owner_neighborhood,
    alcohol_sales,
    schedule,
    municipality_id, 
    status,
    applicant_first_name,
    applicant_last_name_p,
    applicant_last_name_m,
    applicant_user_tax_id,
    applicant_national_id,
    applicant_phone,
    applicant_street,
    applicant_email,
    applicant_postal_code,
    owner_postal_code,
    property_street,
    property_neighborhood,
    property_interior_number,
    property_exterior_number,
    created_at,
    updated_at
) VALUES 
-- License 1 - Restaurant
('LIC-2024-001', '2024-01-15', 'Restaurante', 'Servicio de comida mexicana tradicional', 'REST-001', 'Zona Centro', 'Av. Juárez', '123', 'A', 'Centro Histórico', 'CAT-001-2024', 'Frente al parque principal', '-103.3496', '20.6597', 'Carlos', 'Hernández', 'García', 'HEGC850101ABC', 'HEGC850101HDFRRR01', '33-1234-5678', 'Tacos El Güero', 'carlos@tacosguero.com', 'Calle Morelos', '456', NULL, 'Americana', 'No', 'Lunes a Domingo 9:00-22:00', 1, 1, 'Carlos', 'Hernández', 'García', 'HEGC850101ABC', 'HEGC850101HDFRRR01', '33-1234-5678', 'Calle Morelos 456', 'carlos@tacosguero.com', '44100', '44100', 'Av. Juárez 123', 'Centro Histórico', 'A', '123', NOW(), NOW()),

-- License 2 - Coffee Shop
('LIC-2024-002', '2024-02-20', 'Cafetería', 'Venta de café y repostería artesanal', 'CAF-002', 'Zona Rosa', 'Calle Chapultepec', '789', NULL, 'Zona Rosa', 'CAT-002-2024', 'Esquina con Av. México', '-103.3500', '20.6700', 'Ana', 'Martínez', 'López', 'MALA890215DEF', 'MALA890215MDFRRR02', '33-2345-6789', 'Café Luna', 'ana@cafeluna.com', 'Calle Independencia', '321', '2', 'Lafayette', 'No', 'Lunes a Sábado 7:00-20:00', 1, 1, 'Ana', 'Martínez', 'López', 'MALA890215DEF', 'MALA890215MDFRRR02', '33-2345-6789', 'Calle Independencia 321', 'ana@cafeluna.com', '44140', '44140', 'Calle Chapultepec 789', 'Zona Rosa', NULL, '789', NOW(), NOW()),

-- License 3 - Bar
('LIC-2024-003', '2024-03-10', 'Bar', 'Venta de bebidas alcohólicas y botanas', 'BAR-003', 'Zona Chapultepec', 'Av. México', '555', 'B', 'Americana', 'CAT-003-2024', 'A dos cuadras del Arco de la Minerva', '-103.3600', '20.6800', 'Roberto', 'Sánchez', 'Pérez', 'SAPR920318GHI', 'SAPR920318HDFRRR03', '33-3456-7890', 'La Cantina', 'roberto@lacantina.com', 'Av. Patria', '888', '1', 'Providencia', 'Sí', 'Miércoles a Sábado 18:00-02:00', 1, 1, 'Roberto', 'Sánchez', 'Pérez', 'SAPR920318GHI', 'SAPR920318HDFRRR03', '33-3456-7890', 'Av. Patria 888', 'roberto@lacantina.com', '44630', '44630', 'Av. México 555', 'Americana', 'B', '555', NOW(), NOW()),

-- License 4 - Bakery (Zapopan)
('LIC-2024-004', '2024-04-05', 'Panadería', 'Elaboración y venta de productos de panadería', 'PAN-004', 'Zona Residencial', 'Calle Real', '111', NULL, 'Real de Acosta', 'CAT-004-2024', 'Cerca del Centro Comercial', '-103.3800', '20.7200', 'Lucía', 'González', 'Ramírez', 'GORL870525JKL', 'GORL870525MDFRRR04', '33-4567-8901', 'Panadería Doña Lucía', 'lucia@panaderia.com', 'Calle Azucenas', '222', NULL, 'Jardines del Bosque', 'No', 'Lunes a Domingo 6:00-21:00', 2, 1, 'Lucía', 'González', 'Ramírez', 'GORL870525JKL', 'GORL870525MDFRRR04', '33-4567-8901', 'Calle Azucenas 222', 'lucia@panaderia.com', '45160', '45160', 'Calle Real 111', 'Real de Acosta', NULL, '111', NOW(), NOW()),

-- License 5 - Pharmacy
('LIC-2024-005', '2024-05-12', 'Farmacia', 'Venta de medicamentos y productos de salud', 'FAR-005', 'Zona Comercial', 'Av. López Mateos', '333', 'C', 'Del Valle', 'CAT-005-2024', 'Plaza comercial segundo nivel', '-103.4000', '20.7000', 'Fernando', 'Ruiz', 'Torres', 'RUTF911207MNO', 'RUTF911207HDFRRR05', '33-5678-9012', 'Farmacia San Miguel', 'fernando@farmaciasm.com', 'Calle Volcanes', '444', '3', 'Residencial Victoria', 'No', 'Lunes a Domingo 8:00-22:00', 2, 1, 'Fernando', 'Ruiz', 'Torres', 'RUTF911207MNO', 'RUTF911207HDFRRR05', '33-5678-9012', 'Calle Volcanes 444', 'fernando@farmaciasm.com', '45010', '45010', 'Av. López Mateos 333', 'Del Valle', 'C', '333', NOW(), NOW()),

-- License 6 - Inactive record for testing soft delete
('LIC-2024-006', '2024-06-01', 'Tienda de Abarrotes', 'Venta de productos básicos y abarrotes', 'TDA-006', 'Zona Popular', 'Calle Hidalgo', '666', NULL, 'Santa Tere', 'CAT-006-2024', 'Esquina con Calle Morelos', '-103.3200', '20.6400', 'Pedro', 'Jiménez', 'Flores', 'JIFP880814PQR', 'JIFP880814HDFRRR06', '33-6789-0123', 'Abarrotes Don Pedro', 'pedro@abarrotes.com', 'Calle Libertad', '777', NULL, 'Santa Tere', 'No', 'Lunes a Domingo 7:00-23:00', 1, 0, 'Pedro', 'Jiménez', 'Flores', 'JIFP880814PQR', 'JIFP880814HDFRRR06', '33-6789-0123', 'Calle Libertad 777', 'pedro@abarrotes.com', '44200', '44200', 'Calle Hidalgo 666', 'Santa Tere', NULL, '666', NOW(), NOW());

-- Set sequence values to avoid conflicts
SELECT setval('business_license_histories_id_seq', (SELECT MAX(id) FROM business_license_histories) + 1, false);