#!/usr/bin/env python3
"""
Business License Histories Test Data Seeder
This script inserts fake test data into the business_license_histories table
"""

import sys
import os
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from config.settings import get_database_url
from models.business_license_histories import BusinessLicenseHistory

def create_test_data():
    """Create test data for business license histories"""
    
    test_records = [
        # Restaurant License
        {
            'license_folio': 'LIC-2024-001',
            'issue_date': '2024-01-15',
            'business_line': 'Restaurante',
            'detailed_description': 'Servicio de alimentos y bebidas',
            'business_line_code': 'REST-001',
            'business_area': 'Zona Centro',
            'street': 'Av. Juárez',
            'exterior_number': '123',
            'interior_number': 'A',
            'neighborhood': 'Centro',
            'cadastral_key': 'CAD-001-2024',
            'reference': 'Frente a la plaza principal',
            'coordinate_x': '19.4326',
            'coordinate_y': '-99.1332',
            'owner_first_name': 'Juan Carlos',
            'owner_last_name_p': 'García',
            'owner_last_name_m': 'López',
            'user_tax_id': 'GALO800815ABC',
            'national_id': 'GALO800815HDFMRN01',
            'owner_phone': '555-0101',
            'business_name': 'Restaurante El Buen Sabor',
            'owner_email': 'juan.garcia@email.com',
            'owner_street': 'Calle Morelos',
            'owner_exterior_number': '456',
            'owner_interior_number': '2',
            'owner_neighborhood': 'Roma Norte',
            'alcohol_sales': 'Sí',
            'schedule': 'Lunes a Domingo 8:00-22:00',
            'municipality_id': 1,
            'status': 1,
            'applicant_first_name': 'María Elena',
            'applicant_last_name_p': 'Hernández',
            'applicant_last_name_m': 'Ruiz',
            'applicant_user_tax_id': 'HERM850920XYZ',
            'applicant_national_id': 'HERM850920MDFRNR08',
            'applicant_phone': '555-0102',
            'applicant_street': 'Calle Reforma',
            'applicant_email': 'maria.hernandez@email.com',
            'applicant_postal_code': '06700',
            'owner_postal_code': '11000',
            'property_street': 'Av. Juárez',
            'property_neighborhood': 'Centro',
            'property_interior_number': 'A',
            'property_exterior_number': '123',
            'property_postal_code': '06000',
            'property_type': 'Local comercial',
            'business_trade_name': 'El Buen Sabor S.A. de C.V.',
            'investment': '500000',
            'number_of_employees': '15',
            'number_of_parking_spaces': '5',
            'license_year': '2024',
            'license_type': 'Comercial',
            'license_status': 'Activa',
            'payment_status': 'Pagado',
            'opening_time': '08:00',
            'closing_time': '22:00',
            'alternate_license_year': '2024',
            'payment_user_id': 1,
            'payment_date': datetime(2024, 1, 20, 10, 30),
            'step_1': 1,
            'step_2': 1,
            'step_3': 1,
            'step_4': 1
        },
        # Pharmacy License
        {
            'license_folio': 'LIC-2024-002',
            'issue_date': '2024-02-10',
            'business_line': 'Farmacia',
            'detailed_description': 'Venta de medicamentos y productos farmacéuticos',
            'business_line_code': 'FARM-002',
            'business_area': 'Zona Residencial',
            'street': 'Calle Hidalgo',
            'exterior_number': '789',
            'neighborhood': 'Las Flores',
            'cadastral_key': 'CAD-002-2024',
            'reference': 'Esquina con Av. Independencia',
            'coordinate_x': '19.4285',
            'coordinate_y': '-99.1276',
            'owner_first_name': 'Ana Patricia',
            'owner_last_name_p': 'Martínez',
            'owner_last_name_m': 'Sánchez',
            'user_tax_id': 'MASA751201DEF',
            'national_id': 'MASA751201MDFRNN02',
            'owner_phone': '555-0201',
            'business_name': 'Farmacia San Rafael',
            'owner_email': 'ana.martinez@email.com',
            'owner_street': 'Calle Revolución',
            'owner_exterior_number': '321',
            'owner_neighborhood': 'Doctores',
            'alcohol_sales': 'No',
            'schedule': 'Lunes a Sábado 7:00-21:00',
            'municipality_id': 1,
            'status': 1,
            'applicant_first_name': 'Roberto',
            'applicant_last_name_p': 'Jiménez',
            'applicant_last_name_m': 'Castro',
            'applicant_user_tax_id': 'JICR800515GHI',
            'applicant_national_id': 'JICR800515HDFMBT05',
            'applicant_phone': '555-0202',
            'applicant_street': 'Av. Universidad',
            'applicant_email': 'roberto.jimenez@email.com',
            'applicant_postal_code': '03100',
            'owner_postal_code': '06760',
            'property_street': 'Calle Hidalgo',
            'property_neighborhood': 'Las Flores',
            'property_exterior_number': '789',
            'property_postal_code': '03000',
            'property_type': 'Local comercial',
            'business_trade_name': 'Farmacia San Rafael S.C.',
            'investment': '300000',
            'number_of_employees': '8',
            'number_of_parking_spaces': '3',
            'license_year': '2024',
            'license_type': 'Comercial',
            'license_status': 'Activa',
            'payment_status': 'Pagado',
            'opening_time': '07:00',
            'closing_time': '21:00',
            'alternate_license_year': '2024',
            'payment_user_id': 2,
            'payment_date': datetime(2024, 2, 15, 14, 15),
            'step_1': 1,
            'step_2': 1,
            'step_3': 1,
            'step_4': 0
        },
        # Grocery Store License (Municipality 2)
        {
            'license_folio': 'LIC-2024-003',
            'issue_date': '2024-03-05',
            'business_line': 'Abarrotes',
            'detailed_description': 'Venta de productos de primera necesidad',
            'business_line_code': 'ABAR-003',
            'business_area': 'Zona Popular',
            'street': 'Calle Aldama',
            'exterior_number': '456',
            'interior_number': 'B',
            'neighborhood': 'San Juan',
            'cadastral_key': 'CAD-003-2024',
            'reference': 'A media cuadra del mercado',
            'coordinate_x': '19.4240',
            'coordinate_y': '-99.1420',
            'owner_first_name': 'Luis Fernando',
            'owner_last_name_p': 'Rodríguez',
            'owner_last_name_m': 'Morales',
            'user_tax_id': 'ROML690830JKL',
            'national_id': 'ROML690830HDFDRR03',
            'owner_phone': '555-0301',
            'business_name': 'Abarrotes La Esquina',
            'owner_email': 'luis.rodriguez@email.com',
            'owner_street': 'Calle Allende',
            'owner_exterior_number': '654',
            'owner_interior_number': '1',
            'owner_neighborhood': 'Guerrero',
            'alcohol_sales': 'Sí',
            'schedule': 'Todos los días 6:00-23:00',
            'municipality_id': 2,
            'status': 1,
            'applicant_first_name': 'Carmen',
            'applicant_last_name_p': 'López',
            'applicant_last_name_m': 'Vega',
            'applicant_user_tax_id': 'LOVC901012MNO',
            'applicant_national_id': 'LOVC901012MDFPGR06',
            'applicant_phone': '555-0302',
            'applicant_street': 'Calle Mina',
            'applicant_email': 'carmen.lopez@email.com',
            'applicant_postal_code': '06300',
            'owner_postal_code': '06050',
            'property_street': 'Calle Aldama',
            'property_neighborhood': 'San Juan',
            'property_interior_number': 'B',
            'property_exterior_number': '456',
            'property_postal_code': '06200',
            'property_type': 'Local comercial',
            'business_trade_name': 'Abarrotes La Esquina',
            'investment': '150000',
            'number_of_employees': '5',
            'number_of_parking_spaces': '2',
            'license_year': '2024',
            'license_type': 'Comercial',
            'license_status': 'Activa',
            'payment_status': 'Pagado',
            'opening_time': '06:00',
            'closing_time': '23:00',
            'alternate_license_year': '2024',
            'payment_user_id': 3,
            'payment_date': datetime(2024, 3, 10, 9, 45),
            'step_1': 1,
            'step_2': 1,
            'step_3': 0,
            'step_4': 0
        },
        # Beauty Salon License (Pending status)
        {
            'license_folio': 'LIC-2024-004',
            'issue_date': '2024-04-12',
            'business_line': 'Estética',
            'detailed_description': 'Servicios de belleza y cuidado personal',
            'business_line_code': 'EST-004',
            'business_area': 'Zona Comercial',
            'street': 'Av. Insurgentes',
            'exterior_number': '1001',
            'interior_number': '3',
            'neighborhood': 'Condesa',
            'cadastral_key': 'CAD-004-2024',
            'reference': 'Plaza comercial nivel 2',
            'coordinate_x': '19.4120',
            'coordinate_y': '-99.1700',
            'owner_first_name': 'Sofía',
            'owner_last_name_p': 'Mendoza',
            'owner_last_name_m': 'Ramírez',
            'user_tax_id': 'MERS840607PQR',
            'national_id': 'MERS840607MDFNMF04',
            'owner_phone': '555-0401',
            'business_name': 'Estética Bella Vista',
            'owner_email': 'sofia.mendoza@email.com',
            'owner_street': 'Calle Amsterdam',
            'owner_exterior_number': '78',
            'owner_interior_number': '4',
            'owner_neighborhood': 'Hipódromo',
            'alcohol_sales': 'No',
            'schedule': 'Martes a Domingo 9:00-19:00',
            'municipality_id': 1,
            'status': 1,
            'applicant_first_name': 'Diego',
            'applicant_last_name_p': 'Vargas',
            'applicant_last_name_m': 'Herrera',
            'applicant_user_tax_id': 'VAHD770925STU',
            'applicant_national_id': 'VAHD770925HDFRRG07',
            'applicant_phone': '555-0402',
            'applicant_street': 'Av. Chapultepec',
            'applicant_email': 'diego.vargas@email.com',
            'applicant_postal_code': '06140',
            'owner_postal_code': '11560',
            'property_street': 'Av. Insurgentes',
            'property_neighborhood': 'Condesa',
            'property_interior_number': '3',
            'property_exterior_number': '1001',
            'property_postal_code': '06100',
            'property_type': 'Local en plaza',
            'business_trade_name': 'Bella Vista Estética S.A.',
            'investment': '200000',
            'number_of_employees': '6',
            'number_of_parking_spaces': '0',
            'license_year': '2024',
            'license_type': 'Servicios',
            'license_status': 'Pendiente',
            'reason': 'Documentación incompleta',
            'payment_status': 'Pendiente',
            'opening_time': '09:00',
            'closing_time': '19:00',
            'alternate_license_year': '2024',
            'payment_user_id': 4,
            'step_1': 1,
            'step_2': 1,
            'step_3': 0,
            'step_4': 0
        },
        # Auto Repair Shop License (Municipality 2)
        {
            'license_folio': 'LIC-2024-005',
            'issue_date': '2024-05-08',
            'business_line': 'Taller Mecánico',
            'detailed_description': 'Reparación y mantenimiento automotriz',
            'business_line_code': 'TALL-005',
            'business_area': 'Zona Industrial',
            'street': 'Calle Taller',
            'exterior_number': '200',
            'neighborhood': 'Industrial',
            'cadastral_key': 'CAD-005-2024',
            'reference': 'Zona de talleres',
            'coordinate_x': '19.3850',
            'coordinate_y': '-99.1580',
            'owner_first_name': 'Miguel Ángel',
            'owner_last_name_p': 'Torres',
            'owner_last_name_m': 'Guerrero',
            'user_tax_id': 'TOGM820403VWX',
            'national_id': 'TOGM820403HDFRRG08',
            'owner_phone': '555-0501',
            'business_name': 'Taller Automotriz El Rayo',
            'owner_email': 'miguel.torres@email.com',
            'owner_street': 'Calle Industria',
            'owner_exterior_number': '567',
            'owner_neighborhood': 'Obrera',
            'alcohol_sales': 'No',
            'schedule': 'Lunes a Viernes 8:00-18:00',
            'municipality_id': 2,
            'status': 1,
            'applicant_first_name': 'Leticia',
            'applicant_last_name_p': 'Flores',
            'applicant_last_name_m': 'Díaz',
            'applicant_user_tax_id': 'FODL880212YZA',
            'applicant_national_id': 'FODL880212MDFLLR09',
            'applicant_phone': '555-0502',
            'applicant_street': 'Av. Trabajo',
            'applicant_email': 'leticia.flores@email.com',
            'applicant_postal_code': '03400',
            'owner_postal_code': '08100',
            'property_street': 'Calle Taller',
            'property_neighborhood': 'Industrial',
            'property_exterior_number': '200',
            'property_postal_code': '03300',
            'property_type': 'Nave industrial',
            'business_trade_name': 'Automotriz El Rayo S.A.',
            'investment': '800000',
            'number_of_employees': '12',
            'number_of_parking_spaces': '15',
            'license_year': '2024',
            'license_type': 'Industrial',
            'license_status': 'Activa',
            'payment_status': 'Pagado',
            'opening_time': '08:00',
            'closing_time': '18:00',
            'alternate_license_year': '2024',
            'payment_user_id': 5,
            'payment_date': datetime(2024, 5, 15, 11, 20),
            'step_1': 1,
            'step_2': 1,
            'step_3': 1,
            'step_4': 1
        },
        # Inactive License for testing soft deletes
        {
            'license_folio': 'LIC-2023-099',
            'issue_date': '2023-12-01',
            'business_line': 'Panadería',
            'detailed_description': 'Elaboración y venta de productos de panadería',
            'business_line_code': 'PAN-099',
            'business_area': 'Zona Centro',
            'street': 'Calle Madero',
            'exterior_number': '99',
            'neighborhood': 'Centro Histórico',
            'cadastral_key': 'CAD-099-2023',
            'reference': 'Cerca del zócalo',
            'coordinate_x': '19.4338',
            'coordinate_y': '-99.1370',
            'owner_first_name': 'Fernando',
            'owner_last_name_p': 'Gutiérrez',
            'owner_last_name_m': 'Silva',
            'user_tax_id': 'GUSF650101BCD',
            'national_id': 'GUSF650101HDFLLR10',
            'owner_phone': '555-0099',
            'business_name': 'Panadería Tradicional',
            'owner_email': 'fernando.gutierrez@email.com',
            'owner_street': 'Calle 16 de Septiembre',
            'owner_exterior_number': '88',
            'owner_neighborhood': 'Centro',
            'alcohol_sales': 'No',
            'schedule': 'Martes a Domingo 6:00-20:00',
            'municipality_id': 1,
            'status': 0,  # Inactive status
            'applicant_first_name': 'Rosa María',
            'applicant_last_name_p': 'Castillo',
            'applicant_last_name_m': 'Núñez',
            'applicant_user_tax_id': 'CANR720815EFG',
            'applicant_national_id': 'CANR720815MDFSTR11',
            'applicant_phone': '555-0098',
            'applicant_street': 'Calle 5 de Mayo',
            'applicant_email': 'rosa.castillo@email.com',
            'applicant_postal_code': '06000',
            'owner_postal_code': '06010',
            'property_street': 'Calle Madero',
            'property_neighborhood': 'Centro Histórico',
            'property_exterior_number': '99',
            'property_postal_code': '06000',
            'property_type': 'Local comercial',
            'business_trade_name': 'Panadería Tradicional',
            'investment': '120000',
            'number_of_employees': '4',
            'number_of_parking_spaces': '1',
            'license_year': '2023',
            'license_type': 'Comercial',
            'license_status': 'Cancelada',
            'reason': 'Cierre del negocio',
            'deactivation_status': 'Cancelada por solicitud del propietario',
            'payment_status': 'Cancelado',
            'opening_time': '06:00',
            'closing_time': '20:00',
            'alternate_license_year': '2023',
            'payment_user_id': 6,
            'payment_date': datetime(2023, 12, 15, 16, 30),
            'step_1': 1,
            'step_2': 1,
            'step_3': 1,
            'step_4': 1
        }
    ]
    
    return test_records

def seed_database():
    """Seed the database with test data"""
    
    try:
        # Get database URL
        database_url = get_database_url()
        print(f"Connecting to database: {database_url}")
        
        # Create engine and session
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        print("🌱 Starting database seeding for Business License Histories...")
        
        # Check if test data already exists
        existing_count = session.query(BusinessLicenseHistory).filter(
            BusinessLicenseHistory.license_folio.like('LIC-2024-%')
        ).count()
        
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing test records. Skipping seeding.")
            print("   Delete existing test data first if you want to re-seed.")
            return
        
        # Create test records
        test_records = create_test_data()
        records_added = 0
        
        for record_data in test_records:
            try:
                # Create new record
                record = BusinessLicenseHistory(**record_data)
                session.add(record)
                records_added += 1
                print(f"✅ Added: {record_data['license_folio']} - {record_data['business_name']}")
                
            except Exception as e:
                print(f"❌ Error adding record {record_data.get('license_folio', 'Unknown')}: {str(e)}")
                continue
        
        # Commit all changes
        session.commit()
        print(f"\n🎉 Successfully seeded {records_added} business license history records!")
        
        # Print summary by municipality
        mun1_count = session.query(BusinessLicenseHistory).filter(
            BusinessLicenseHistory.municipality_id == 1,
            BusinessLicenseHistory.license_folio.like('LIC-2024-%')
        ).count()
        
        mun2_count = session.query(BusinessLicenseHistory).filter(
            BusinessLicenseHistory.municipality_id == 2,
            BusinessLicenseHistory.license_folio.like('LIC-2024-%')
        ).count()
        
        active_count = session.query(BusinessLicenseHistory).filter(
            BusinessLicenseHistory.status == 1,
            BusinessLicenseHistory.license_folio.like('LIC-%')
        ).count()
        
        inactive_count = session.query(BusinessLicenseHistory).filter(
            BusinessLicenseHistory.status == 0,
            BusinessLicenseHistory.license_folio.like('LIC-%')
        ).count()
        
        print(f"\n📊 Summary:")
        print(f"   Municipality 1: {mun1_count} records")
        print(f"   Municipality 2: {mun2_count} records")
        print(f"   Active records: {active_count}")
        print(f"   Inactive records: {inactive_count}")
        
        print(f"\n🚀 You can now test the API endpoints!")
        print(f"   Run: bash scripts/test_business_license_histories_api.sh")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        if 'session' in locals():
            session.rollback()
        return False
        
    finally:
        if 'session' in locals():
            session.close()
    
    return True

if __name__ == "__main__":
    print("Business License Histories Test Data Seeder")
    print("==========================================")
    
    if seed_database():
        print("\n✅ Seeding completed successfully!")
    else:
        print("\n❌ Seeding failed!")
        sys.exit(1)
