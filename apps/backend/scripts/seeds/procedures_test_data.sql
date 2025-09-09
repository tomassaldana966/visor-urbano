-- Seed data for procedures and historical_procedures tables

-- Clean up existing data (if needed)
-- DELETE FROM procedures WHERE folio LIKE 'TEST-%';
-- DELETE FROM historical_procedures WHERE folio LIKE 'HIST-%';

-- Regular procedures
INSERT INTO procedures (
    folio, current_step, user_signature, user_id, window_user_id, 
    entry_role, documents_submission_date, procedure_start_date, 
    window_seen_date, license_delivered_date, has_signature, 
    no_signature_date, official_applicant_name, responsibility_letter, 
    sent_to_reviewers, sent_to_reviewers_date, license_pdf, 
    payment_order, status, step_one, step_two, step_three, step_four,
    director_approval, window_license_generated, procedure_type, 
    license_status, reason, renewed_folio, requirements_query_id
) VALUES 
-- Regular active procedure
(
    'TEST-001', -- folio
    2, -- current_step
    'user_signature_data_1', -- user_signature
    1, -- user_id
    2, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '30 days', -- documents_submission_date
    NOW() - INTERVAL '29 days', -- procedure_start_date
    NOW() - INTERVAL '28 days', -- window_seen_date
    NULL, -- license_delivered_date (not delivered yet)
    1, -- has_signature
    NULL, -- no_signature_date
    'Juan Pérez', -- official_applicant_name
    NULL, -- responsibility_letter
    0, -- sent_to_reviewers
    NULL, -- sent_to_reviewers_date
    NULL, -- license_pdf
    '/uploads/payment_orders/order_test_001.pdf', -- payment_order
    1, -- status (active)
    1, -- step_one (completed)
    1, -- step_two (completed)
    0, -- step_three (not completed)
    0, -- step_four (not completed)
    0, -- director_approval
    0, -- window_license_generated
    'licencia_construccion', -- procedure_type
    'en_proceso', -- license_status
    NULL, -- reason
    NULL, -- renewed_folio
    1  -- requirements_query_id
),
-- Completed procedure
(
    'TEST-002', -- folio
    4, -- current_step (completed all steps)
    'user_signature_data_2', -- user_signature
    2, -- user_id
    3, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '90 days', -- documents_submission_date
    NOW() - INTERVAL '89 days', -- procedure_start_date
    NOW() - INTERVAL '85 days', -- window_seen_date
    NOW() - INTERVAL '30 days', -- license_delivered_date
    1, -- has_signature
    NULL, -- no_signature_date
    'María González', -- official_applicant_name
    'responsibility_letter_2.pdf', -- responsibility_letter
    1, -- sent_to_reviewers
    NOW() - INTERVAL '80 days', -- sent_to_reviewers_date
    '/uploads/licenses/license_test_002.pdf', -- license_pdf
    '/uploads/payment_orders/order_test_002.pdf', -- payment_order
    2, -- status (completed)
    1, -- step_one (completed)
    1, -- step_two (completed)
    1, -- step_three (completed)
    1, -- step_four (completed)
    1, -- director_approval
    1, -- window_license_generated
    'licencia_comercial', -- procedure_type
    'completado', -- license_status
    NULL, -- reason
    NULL, -- renewed_folio
    2  -- requirements_query_id
),
-- Renewal procedure with reference to original
(
    'TEST-003', -- folio
    3, -- current_step
    'user_signature_data_3', -- user_signature
    2, -- user_id
    3, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '15 days', -- documents_submission_date
    NOW() - INTERVAL '14 days', -- procedure_start_date
    NOW() - INTERVAL '12 days', -- window_seen_date
    NULL, -- license_delivered_date (not delivered yet)
    1, -- has_signature
    NULL, -- no_signature_date
    'María González', -- official_applicant_name
    'responsibility_letter_3.pdf', -- responsibility_letter
    1, -- sent_to_reviewers
    NOW() - INTERVAL '10 days', -- sent_to_reviewers_date
    NULL, -- license_pdf
    '/uploads/payment_orders/order_test_003.pdf', -- payment_order
    1, -- status (active)
    1, -- step_one (completed)
    1, -- step_two (completed)
    1, -- step_three (completed)
    0, -- step_four (not completed)
    0, -- director_approval
    0, -- window_license_generated
    'refrendo', -- procedure_type
    'en_proceso', -- license_status
    'Renovación anual', -- reason
    'TEST-002', -- renewed_folio (points to the original)
    3  -- requirements_query_id
),
-- Rejected procedure
(
    'TEST-004', -- folio
    2, -- current_step
    'user_signature_data_4', -- user_signature
    3, -- user_id
    4, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '45 days', -- documents_submission_date
    NOW() - INTERVAL '44 days', -- procedure_start_date
    NOW() - INTERVAL '40 days', -- window_seen_date
    NULL, -- license_delivered_date
    1, -- has_signature
    NULL, -- no_signature_date
    'Carlos Rodríguez', -- official_applicant_name
    NULL, -- responsibility_letter
    1, -- sent_to_reviewers
    NOW() - INTERVAL '38 days', -- sent_to_reviewers_date
    NULL, -- license_pdf
    '/uploads/payment_orders/order_test_004.pdf', -- payment_order
    3, -- status (rejected)
    1, -- step_one (completed)
    0, -- step_two (failed)
    0, -- step_three (not reached)
    0, -- step_four (not reached)
    0, -- director_approval
    0, -- window_license_generated
    'licencia_construccion', -- procedure_type
    'rechazado', -- license_status
    'Documentación incompleta', -- reason
    NULL, -- renewed_folio
    4  -- requirements_query_id
);

-- Insert sample historical procedures
INSERT INTO historical_procedures (
    folio, current_step, user_signature, user_id, window_user_id, 
    entry_role, documents_submission_date, procedure_start_date, 
    window_seen_date, license_delivered_date, has_signature, 
    no_signature_date, official_applicant_name, responsibility_letter, 
    sent_to_reviewers, sent_to_reviewers_date, license_pdf, 
    payment_order, status, step_one, step_two, step_three, step_four,
    director_approval, window_license_generated, procedure_type, 
    license_status, reason, renewed_folio, requirements_query_id
) VALUES 
-- Historical completed procedure from 2 years ago
(
    'HIST-001', -- folio
    4, -- current_step (completed all steps)
    'user_signature_data_hist_1', -- user_signature
    1, -- user_id
    2, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '2 years', -- documents_submission_date
    NOW() - INTERVAL '2 years', -- procedure_start_date
    NOW() - INTERVAL '2 years' + INTERVAL '5 days', -- window_seen_date
    NOW() - INTERVAL '2 years' + INTERVAL '30 days', -- license_delivered_date
    1, -- has_signature
    NULL, -- no_signature_date
    'Juan Pérez', -- official_applicant_name
    'responsibility_letter_hist_1.pdf', -- responsibility_letter
    1, -- sent_to_reviewers
    NOW() - INTERVAL '2 years' + INTERVAL '10 days', -- sent_to_reviewers_date
    '/uploads/licenses/license_hist_001.pdf', -- license_pdf
    '/uploads/payment_orders/order_hist_001.pdf', -- payment_order
    2, -- status (completed)
    1, -- step_one (completed)
    1, -- step_two (completed)
    1, -- step_three (completed)
    1, -- step_four (completed)
    1, -- director_approval
    1, -- window_license_generated
    'licencia_construccion', -- procedure_type
    'completado', -- license_status
    NULL, -- reason
    NULL, -- renewed_folio
    1  -- requirements_query_id
),
-- Historical completed procedure from 1 year ago
(
    'HIST-002', -- folio
    4, -- current_step (completed all steps)
    'user_signature_data_hist_2', -- user_signature
    2, -- user_id
    3, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '1 year', -- documents_submission_date
    NOW() - INTERVAL '1 year', -- procedure_start_date
    NOW() - INTERVAL '1 year' + INTERVAL '5 days', -- window_seen_date
    NOW() - INTERVAL '1 year' + INTERVAL '30 days', -- license_delivered_date
    1, -- has_signature
    NULL, -- no_signature_date
    'María González', -- official_applicant_name
    'responsibility_letter_hist_2.pdf', -- responsibility_letter
    1, -- sent_to_reviewers
    NOW() - INTERVAL '1 year' + INTERVAL '10 days', -- sent_to_reviewers_date
    '/uploads/licenses/license_hist_002.pdf', -- license_pdf
    '/uploads/payment_orders/order_hist_002.pdf', -- payment_order
    2, -- status (completed)
    1, -- step_one (completed)
    1, -- step_two (completed)
    1, -- step_three (completed)
    1, -- step_four (completed)
    1, -- director_approval
    1, -- window_license_generated
    'licencia_comercial', -- procedure_type
    'completado', -- license_status
    NULL, -- reason
    NULL, -- renewed_folio
    2  -- requirements_query_id
),
-- Historical rejected procedure
(
    'HIST-003', -- folio
    2, -- current_step
    'user_signature_data_hist_3', -- user_signature
    3, -- user_id
    4, -- window_user_id
    1, -- entry_role 
    NOW() - INTERVAL '1 year' - INTERVAL '6 months', -- documents_submission_date
    NOW() - INTERVAL '1 year' - INTERVAL '6 months', -- procedure_start_date
    NOW() - INTERVAL '1 year' - INTERVAL '6 months' + INTERVAL '5 days', -- window_seen_date
    NULL, -- license_delivered_date
    1, -- has_signature
    NULL, -- no_signature_date
    'Carlos Rodríguez', -- official_applicant_name
    NULL, -- responsibility_letter
    1, -- sent_to_reviewers
    NOW() - INTERVAL '1 year' - INTERVAL '6 months' + INTERVAL '10 days', -- sent_to_reviewers_date
    NULL, -- license_pdf
    '/uploads/payment_orders/order_hist_003.pdf', -- payment_order
    3, -- status (rejected)
    1, -- step_one (completed)
    0, -- step_two (failed)
    0, -- step_three (not reached)
    0, -- step_four (not reached)
    0, -- director_approval
    0, -- window_license_generated
    'licencia_construccion', -- procedure_type
    'rechazado', -- license_status
    'Documentación incompatible con zona', -- reason
    NULL, -- renewed_folio
    3  -- requirements_query_id
);

-- Add sample answers for procedures
INSERT INTO answers (procedure_id, question_name, value) VALUES
(1, 'construction_type', 'residential'),
(1, 'area_sq_meters', '250'),
(1, 'floors_number', '2'),
(1, 'parking_spaces', '2'),
(2, 'business_name', 'Café La Esquina'),
(2, 'business_type', 'restaurant'),
(2, 'employee_count', '12'),
(2, 'has_liquor_license', 'true'),
(3, 'business_name', 'Café La Esquina'),
(3, 'business_type', 'restaurant'),
(3, 'employee_count', '15'),
(3, 'has_liquor_license', 'true'),
(4, 'construction_type', 'commercial'),
(4, 'area_sq_meters', '450'),
(4, 'floors_number', '3'),
(4, 'parking_spaces', '8');
