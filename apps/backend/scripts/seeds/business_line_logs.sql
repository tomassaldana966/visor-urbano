-- Business Line Logs Seed Data
-- This file contains sample data for the business_line_logs table
-- for testing and development purposes

-- Clear existing test data (optional - uncomment if needed)
-- DELETE FROM business_line_logs WHERE action LIKE '%TEST%' OR action LIKE '%SAMPLE%';

-- Insert sample business line logs
INSERT INTO business_line_logs (
    action, 
    previous, 
    user_id, 
    log_type, 
    procedure_id, 
    host, 
    user_ip, 
    role_id, 
    user_agent, 
    post_request,
    created_at,
    updated_at
) VALUES 

-- Authentication logs (log_type = 1)
(
    'Usuario inició sesión',
    'Usuario sin sesión activa',
    1,
    1,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"login_method": "password", "remember_me": true, "ip_address": "192.168.1.100"}',
    NOW() - INTERVAL '2 hours',
    NOW() - INTERVAL '2 hours'
),

(
    'Usuario cerró sesión',
    'Sesión activa desde 2024-05-31 08:00:00',
    1,
    1,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"logout_method": "manual", "session_duration": "120 minutes"}',
    NOW() - INTERVAL '30 minutes',
    NOW() - INTERVAL '30 minutes'
),

-- Commercial License logs (log_type = 2)
(
    'Creó nueva licencia comercial',
    'Sin licencias previas',
    2,
    2,
    101,
    'visor-urbano.local',
    '192.168.1.101',
    2,
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    '{"business_type": "restaurant", "area": "150m2", "alcohol_sales": false, "business_name": "Restaurante El Buen Sabor"}',
    NOW() - INTERVAL '1 day',
    NOW() - INTERVAL '1 day'
),

(
    'Modificó licencia comercial',
    'Licencia en estado: PENDIENTE',
    1,
    2,
    101,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"field_changed": "business_area", "old_value": "120m2", "new_value": "150m2"}',
    NOW() - INTERVAL '6 hours',
    NOW() - INTERVAL '6 hours'
),

(
    'Aprobó licencia comercial',
    'Licencia en estado: EN_REVISION',
    1,
    2,
    101,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"approval_date": "2024-05-31", "notes": "Documentación completa", "inspector_id": 5}',
    NOW() - INTERVAL '3 hours',
    NOW() - INTERVAL '3 hours'
),

-- Provisional Opening logs (log_type = 3)
(
    'Creó solicitud de apertura provisional',
    'Sin solicitudes previas',
    2,
    3,
    102,
    'visor-urbano.local',
    '192.168.1.101',
    2,
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    '{"duration_days": 60, "conditions": "Standard opening conditions", "inspection_required": true}',
    NOW() - INTERVAL '5 days',
    NOW() - INTERVAL '5 days'
),

(
    'Aprobó apertura provisional',
    'Solicitud en estado: PENDIENTE',
    1,
    3,
    102,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"approval_date": "2024-05-26", "valid_until": "2024-07-25", "conditions_met": true}',
    NOW() - INTERVAL '5 days',
    NOW() - INTERVAL '5 days'
),

-- Procedure logs (log_type = 4)
(
    'Creó nuevo trámite',
    'Sin trámites activos',
    3,
    4,
    103,
    'visor-urbano.local',
    '192.168.1.102',
    3,
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    '{"procedure_type": "license_renewal", "business_id": 45, "status": "initiated"}',
    NOW() - INTERVAL '2 days',
    NOW() - INTERVAL '2 days'
),

(
    'Completó trámite',
    'Trámite en proceso',
    1,
    4,
    103,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"completion_date": "2024-05-31", "final_status": "approved", "processing_time": "48 hours"}',
    NOW() - INTERVAL '1 hour',
    NOW() - INTERVAL '1 hour'
),

-- System logs (log_type = 5)
(
    'Realizó respaldo de base de datos',
    'Último respaldo: 2024-05-30',
    1,
    5,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'VisorUrbano-System-Service/1.0',
    '{"backup_type": "full", "size": "2.5GB", "duration": "15 minutes", "status": "success"}',
    NOW() - INTERVAL '12 hours',
    NOW() - INTERVAL '12 hours'
),

(
    'Configuró parámetros del sistema',
    'Configuración anterior guardada',
    1,
    5,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"module": "notifications", "setting": "email_frequency", "old_value": "daily", "new_value": "weekly"}',
    NOW() - INTERVAL '8 hours',
    NOW() - INTERVAL '8 hours'
),

-- Report logs (log_type = 6)
(
    'Generó reporte de licencias',
    NULL,
    1,
    6,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"report_type": "monthly_licenses", "date_range": "2024-05", "format": "pdf", "records_count": 156}',
    NOW() - INTERVAL '4 hours',
    NOW() - INTERVAL '4 hours'
),

(
    'Exportó datos de trámites',
    NULL,
    2,
    6,
    NULL,
    'visor-urbano.local',
    '192.168.1.101',
    2,
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    '{"export_type": "procedures", "format": "excel", "date_filter": "last_30_days", "total_records": 89}',
    NOW() - INTERVAL '1 day',
    NOW() - INTERVAL '1 day'
),

-- User management logs (log_type = 7)
(
    'Creó nuevo usuario',
    'Sin usuarios nuevos hoy',
    1,
    7,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"user_type": "operator", "role_assigned": "municipal_agent", "municipality": "Guadalajara"}',
    NOW() - INTERVAL '6 hours',
    NOW() - INTERVAL '6 hours'
),

(
    'Actualizó permisos de usuario',
    'Permisos básicos asignados',
    1,
    7,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"target_user_id": 4, "permissions_added": ["approve_licenses"], "permissions_removed": []}',
    NOW() - INTERVAL '2 hours',
    NOW() - INTERVAL '2 hours'
),

-- Configuration logs (log_type = 8)
(
    'Actualizó configuración de notificaciones',
    'Configuración por defecto',
    1,
    8,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"setting_category": "notifications", "email_enabled": true, "sms_enabled": false, "frequency": "immediate"}',
    NOW() - INTERVAL '10 hours',
    NOW() - INTERVAL '10 hours'
),

(
    'Configuró integración externa',
    'Sin integraciones configuradas',
    1,
    8,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"service": "payment_gateway", "provider": "stripe", "test_mode": true, "webhook_configured": true}',
    NOW() - INTERVAL '1 day',
    NOW() - INTERVAL '1 day'
),

-- Additional sample logs with various timestamps
(
    'Subió documentos adjuntos',
    'Sin archivos previos',
    2,
    2,
    104,
    'visor-urbano.local',
    '192.168.1.101',
    2,
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
    '{"files": ["id_copy.pdf", "business_plan.docx"], "total_size": "3.2MB", "upload_method": "mobile"}',
    NOW() - INTERVAL '3 days',
    NOW() - INTERVAL '3 days'
),

(
    'Consultó estadísticas del sistema',
    NULL,
    1,
    6,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"dashboard": "admin", "metrics_viewed": ["active_licenses", "pending_procedures", "monthly_revenue"]}',
    NOW() - INTERVAL '30 minutes',
    NOW() - INTERVAL '30 minutes'
),

(
    'Envió notificación masiva',
    'Última notificación: 2024-05-28',
    1,
    5,
    NULL,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"notification_type": "system_maintenance", "recipients": 234, "delivery_method": "email", "scheduled": false}',
    NOW() - INTERVAL '2 days',
    NOW() - INTERVAL '2 days'
),

(
    'Rechazó solicitud de licencia',
    'Solicitud en revisión',
    1,
    2,
    105,
    'visor-urbano.local',
    '192.168.1.100',
    1,
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '{"rejection_reason": "incomplete_documentation", "missing_docs": ["tax_certificate", "fire_safety"], "resubmission_allowed": true}',
    NOW() - INTERVAL '4 days',
    NOW() - INTERVAL '4 days'
);

-- Insert additional logs for different users and time periods to simulate real usage
INSERT INTO business_line_logs (action, previous, user_id, log_type, procedure_id, host, user_ip, role_id, user_agent, post_request, created_at, updated_at)
SELECT 
    CASE 
        WHEN random() < 0.2 THEN 'Usuario inició sesión'
        WHEN random() < 0.4 THEN 'Consultó lista de licencias'
        WHEN random() < 0.6 THEN 'Descargó documento'
        WHEN random() < 0.8 THEN 'Actualizó estado de trámite'
        ELSE 'Generó reporte'
    END,
    CASE 
        WHEN random() < 0.3 THEN NULL
        WHEN random() < 0.6 THEN 'Estado anterior registrado'
        ELSE 'Última acción completada'
    END,
    CASE 
        WHEN random() < 0.4 THEN 1
        WHEN random() < 0.7 THEN 2
        ELSE 3
    END,
    FLOOR(random() * 8 + 1)::integer,
    CASE WHEN random() < 0.5 THEN FLOOR(random() * 200 + 100)::integer ELSE NULL END,
    'visor-urbano.local',
    '192.168.1.' || FLOOR(random() * 200 + 100)::text,
    CASE 
        WHEN random() < 0.4 THEN 1
        WHEN random() < 0.7 THEN 2
        ELSE 3
    END,
    'Mozilla/5.0 (Various User Agents)',
    '{"automated": true, "sample_data": true}',
    NOW() - (random() * INTERVAL '30 days'),
    NOW() - (random() * INTERVAL '30 days')
FROM generate_series(1, 50);

-- Create a view for easy querying of logs with user information
CREATE OR REPLACE VIEW business_line_logs_with_users AS
SELECT 
    bll.id,
    bll.action,
    bll.previous,
    bll.log_type,
    CASE bll.log_type
        WHEN 1 THEN 'Autenticación'
        WHEN 2 THEN 'Licencias Comerciales'
        WHEN 3 THEN 'Aperturas Provisionales'
        WHEN 4 THEN 'Trámites'
        WHEN 5 THEN 'Sistema'
        WHEN 6 THEN 'Reportes'
        WHEN 7 THEN 'Usuarios'
        WHEN 8 THEN 'Configuración'
        ELSE 'Otro'
    END as log_type_name,
    bll.procedure_id,
    bll.host,
    bll.user_ip,
    bll.role_id,
    bll.user_agent,
    bll.post_request,
    bll.created_at,
    bll.updated_at,
    u.name as user_name,
    u.paternal_last_name,
    u.email as user_email
FROM business_line_logs bll
LEFT JOIN users u ON bll.user_id = u.id
ORDER BY bll.created_at DESC;

-- Add some indexes for better query performance if they don't exist
CREATE INDEX IF NOT EXISTS idx_business_line_logs_created_at ON business_line_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_business_line_logs_user_type ON business_line_logs(user_id, log_type);
CREATE INDEX IF NOT EXISTS idx_business_line_logs_action_search ON business_line_logs USING gin(to_tsvector('spanish', action));

-- Display summary of inserted data
SELECT 
    'Resumen de datos insertados:' as info,
    COUNT(*) as total_logs,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT log_type) as log_types_used,
    MIN(created_at) as earliest_log,
    MAX(created_at) as latest_log
FROM business_line_logs;
