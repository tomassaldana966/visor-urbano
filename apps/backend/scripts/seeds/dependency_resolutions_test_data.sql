-- Seed data for dependency_resolutions table for testing endpoints
-- This script provides comprehensive test data to validate the dependency_resolutions router

-- Clean existing test data first
DELETE FROM dependency_resolutions WHERE procedure_id IN (1, 2, 3, 4, 5);

-- Insert test dependency resolution records
-- Note: Using NULL for user_id since auth_user table is empty
-- Using existing procedure IDs (1, 2, 3, 4, 5) from procedures table

INSERT INTO dependency_resolutions (
    procedure_id, 
    role, 
    user_id, 
    resolution_status, 
    resolution_text, 
    resolution_file, 
    signature, 
    created_at, 
    updated_at
) VALUES
-- Procedure ID 1 (PROC-001) - Multiple resolutions for testing by_folio endpoint
(1, 1, NULL, 1, 'Resolución administrativa aprobada para el trámite PROC-001. Se autoriza el procedimiento solicitado conforme a la normativa vigente.', 'resolution_proc001_admin.pdf', 'admin_signature_001', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
(1, 2, NULL, 1, 'Resolución directiva confirmando la aprobación del trámite PROC-001. Procede según lo establecido en el reglamento municipal.', 'resolution_proc001_director.pdf', 'director_signature_001', '2024-01-15 14:30:00', '2024-01-15 14:30:00'),
(1, 3, NULL, 2, 'Observaciones técnicas sobre el trámite PROC-001. Se requieren ajustes menores en la documentación presentada.', 'resolution_proc001_tech.pdf', 'tech_signature_001', '2024-01-16 10:15:00', '2024-01-17 16:45:00'),

-- Procedure ID 2 (PROC-002) - Rejected resolution
(2, 1, NULL, 3, 'Resolución de rechazo para el trámite PROC-002. No cumple con los requisitos mínimos establecidos en el artículo 15 del reglamento.', 'resolution_proc002_rejected.pdf', 'admin_signature_002', '2024-01-18 11:20:00', '2024-01-18 11:20:00'),
(2, 2, NULL, 3, 'Confirmación directiva del rechazo del trámite PROC-002. Se notifica al solicitante para subsanar las deficiencias identificadas.', 'resolution_proc002_director_reject.pdf', 'director_signature_002', '2024-01-19 08:45:00', '2024-01-19 08:45:00'),

-- Procedure ID 3 (string folio) - Pending resolution
(3, 1, NULL, 4, 'Resolución en proceso de revisión para el trámite con folio string. Pendiente de validación técnica por parte del departamento especializado.', NULL, NULL, '2024-01-20 13:30:00', '2024-01-22 09:15:00'),
(3, 3, NULL, 4, 'Evaluación técnica pendiente. Se requiere inspección en campo antes de emitir resolución definitiva.', NULL, NULL, '2024-01-21 15:00:00', '2024-01-23 11:30:00'),

-- Procedure ID 4 (PROC-004) - Approved with conditions
(4, 1, NULL, 5, 'Resolución aprobada con condiciones para PROC-004. Se autoriza con las restricciones especificadas en el anexo técnico adjunto.', 'resolution_proc004_conditional.pdf', 'admin_signature_004', '2024-01-24 10:00:00', '2024-01-24 10:00:00'),
(4, 2, NULL, 5, 'Validación directiva de la aprobación condicional. El solicitante debe cumplir con las medidas correctivas en un plazo de 30 días.', 'resolution_proc004_director_conditional.pdf', 'director_signature_004', '2024-01-24 16:20:00', '2024-01-24 16:20:00'),

-- Procedure ID 5 (PROC-005) - Multiple status transitions for testing updates
(5, 1, NULL, 1, 'Resolución inicial aprobada para PROC-005. Autorización preliminar otorgada conforme a solicitud presentada.', 'resolution_proc005_initial.pdf', 'admin_signature_005_v1', '2024-01-25 09:30:00', '2024-01-26 14:15:00'),
(5, 1, NULL, 2, 'Resolución modificada para PROC-005. Se requieren documentos adicionales antes de la autorización final.', 'resolution_proc005_modified.pdf', 'admin_signature_005_v2', '2024-01-26 14:15:00', '2024-01-28 10:45:00'),
(5, 2, NULL, 1, 'Resolución directiva final para PROC-005. Aprobación definitiva tras cumplimiento de requisitos adicionales.', 'resolution_proc005_final.pdf', 'director_signature_005_final', '2024-01-28 10:45:00', '2024-01-28 10:45:00'),

-- Additional test data for edge cases
-- Long resolution text for testing text handling
(1, 1, NULL, 1, 'Esta es una resolución con texto extenso para probar el manejo de contenido largo en el sistema. La resolución abarca múltiples aspectos técnicos, legales y administrativos que deben ser considerados en el proceso de evaluación. Se incluyen referencias a normativas municipales, estatales y federales aplicables al caso. Además, se especifican las condiciones particulares que debe cumplir el solicitante, los plazos establecidos para cada etapa del proceso, y las consecuencias del incumplimiento de cualquiera de las disposiciones establecidas en la presente resolución administrativa. La autoridad competente se reserva el derecho de realizar inspecciones periódicas para verificar el cumplimiento de todas las condiciones aquí establecidas.', 'resolution_long_text.pdf', 'signature_long_001', '2024-01-29 08:00:00', '2024-01-29 08:00:00'),

-- Resolution without file for testing optional fields
(2, 3, NULL, 4, 'Resolución sin archivo adjunto para pruebas de campos opcionales. Esta resolución se encuentra en proceso de digitalización.', NULL, NULL, '2024-01-30 12:00:00', '2024-01-30 12:00:00'),

-- Recent resolution for testing date ordering
(3, 2, NULL, 1, 'Resolución reciente para pruebas de ordenamiento por fecha. Esta es la resolución más actualizada en el sistema de pruebas.', 'resolution_recent.pdf', 'recent_signature', '2024-02-01 16:30:00', '2024-02-01 16:30:00');

-- Verify the inserted data
SELECT 
    id,
    procedure_id,
    role,
    resolution_status,
    LEFT(resolution_text, 50) || '...' as resolution_preview,
    resolution_file,
    created_at
FROM dependency_resolutions 
ORDER BY procedure_id, created_at;

-- Show count by procedure
SELECT 
    procedure_id,
    COUNT(*) as resolution_count,
    MIN(created_at) as first_resolution,
    MAX(updated_at) as last_update
FROM dependency_resolutions 
GROUP BY procedure_id 
ORDER BY procedure_id;

-- Show count by status
SELECT 
    resolution_status,
    COUNT(*) as count,
    CASE resolution_status
        WHEN 1 THEN 'Aprobado'
        WHEN 2 THEN 'Observaciones'
        WHEN 3 THEN 'Rechazado'
        WHEN 4 THEN 'Pendiente'
        WHEN 5 THEN 'Aprobado con condiciones'
        ELSE 'Desconocido'
    END as status_description
FROM dependency_resolutions 
GROUP BY resolution_status 
ORDER BY resolution_status;

-- Show count by role
SELECT 
    role,
    COUNT(*) as count,
    CASE role
        WHEN 1 THEN 'Administrador'
        WHEN 2 THEN 'Director'
        WHEN 3 THEN 'Técnico'
        ELSE 'Otro'
    END as role_description
FROM dependency_resolutions 
GROUP BY role 
ORDER BY role;
