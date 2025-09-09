#!/usr/bin/env python3
"""
Script to create test data for notifications endpoints
User ID: 29, Municipality ID: 2
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_data():
    """Create test data for notifications endpoints"""
    
    # Create database connection
    from config.settings import SYNC_DATABASE_URL
    engine = create_engine(SYNC_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        try:
            # Test data configuration
            USER_ID = 29  # For procedures only
            MUNICIPALITY_ID = 2
            USER_EMAIL = "test.user29@visorurbano.com"
            
            logger.info(f"Creating test data with Procedures for User ID: {USER_ID}, Municipality ID: {MUNICIPALITY_ID}")
            logger.info("Requirements queries will be created anonymously (user_id = NULL)")
            
            # 1. Create requirements_querys (folios) - Created anonymously
            folios_data = [
                {
                    "folio": "REQ-2025-000001",
                    "street": "Av. Revolución 123",
                    "neighborhood": "Centro",
                    "municipality_name": "Guadalajara",
                    "scian_code": "461110",
                    "scian_name": "Comercio al por menor de abarrotes, alimentos, bebidas, hielo y tabaco",
                    "property_area": Decimal("150.50"),
                    "activity_area": Decimal("100.25"),
                    "applicant_name": "Juan Pérez García",
                    "applicant_character": "Propietario",
                    "person_type": "Física"
                },
                {
                    "folio": "REQ-2025-000002", 
                    "street": "Calle Morelos 456",
                    "neighborhood": "Zona Rosa",
                    "municipality_name": "Guadalajara",
                    "scian_code": "722513",
                    "scian_name": "Cafeterías, fuentes de sodas, neverías, refresquerías y similares",
                    "property_area": Decimal("80.00"),
                    "activity_area": Decimal("60.00"),
                    "applicant_name": "María González López",
                    "applicant_character": "Representante Legal",
                    "person_type": "Moral"
                },
                {
                    "folio": "REQ-2025-000003",
                    "street": "Blvd. Independencia 789",
                    "neighborhood": "Americana",
                    "municipality_name": "Guadalajara", 
                    "scian_code": "722411",
                    "scian_name": "Restaurantes con servicio de bar",
                    "property_area": Decimal("200.00"),
                    "activity_area": Decimal("180.00"),
                    "applicant_name": "Roberto Martín Sánchez",
                    "applicant_character": "Propietario",
                    "person_type": "Física"
                }
            ]
            
            # Insert requirements_querys
            for i, folio_data in enumerate(folios_data, 1):
                query = text("""
                    INSERT INTO requirements_querys (
                        id, folio, street, neighborhood, municipality_name, municipality_id,
                        scian_code, scian_name, property_area, activity_area, 
                        applicant_name, applicant_character, person_type,
                        status, user_id, created_at, updated_at, year_folio, alcohol_sales
                    ) VALUES (
                        :id, :folio, :street, :neighborhood, :municipality_name, :municipality_id,
                        :scian_code, :scian_name, :property_area, :activity_area,
                        :applicant_name, :applicant_character, :person_type,
                        1, :user_id, :created_at, :updated_at, 2025, :alcohol_sales
                    )
                    ON CONFLICT (id) DO NOTHING
                """)
                
                db.execute(query, {
                    "id": i,
                    "folio": folio_data["folio"],
                    "street": folio_data["street"],
                    "neighborhood": folio_data["neighborhood"],
                    "municipality_name": folio_data["municipality_name"],
                    "municipality_id": MUNICIPALITY_ID,
                    "scian_code": folio_data["scian_code"],
                    "scian_name": folio_data["scian_name"],
                    "property_area": folio_data["property_area"],
                    "activity_area": folio_data["activity_area"],
                    "applicant_name": folio_data["applicant_name"],
                    "applicant_character": folio_data["applicant_character"],
                    "person_type": folio_data["person_type"],
                    "user_id": None,  # Requirements queries are created anonymously
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "alcohol_sales": 1 if "bar" in folio_data["scian_name"].lower() else 0
                })
            
            # 2. Create procedures for each requirements_query
            for i, folio_data in enumerate(folios_data, 1):
                query = text("""
                    INSERT INTO procedures (
                        id, folio, current_step, user_id, status, 
                        procedure_start_date, requirements_query_id,
                        created_at, updated_at
                    ) VALUES (
                        :id, :folio, 1, :user_id, 1,
                        :procedure_start_date, :requirements_query_id,
                        :created_at, :updated_at
                    )
                    ON CONFLICT (id) DO NOTHING
                """)
                
                db.execute(query, {
                    "id": i,
                    "folio": folio_data["folio"],
                    "user_id": USER_ID,
                    "procedure_start_date": datetime.now() - timedelta(days=i),
                    "requirements_query_id": i,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })
            
            # 3. Create notifications
            notifications_data = [
                {
                    "id": 1,
                    "folio": "REQ-2025-000001",
                    "comment": "Su documentación ha sido recibida y está en proceso de revisión. Se requiere complementar información adicional.",
                    "notification_type": 1,
                    "notified": 0,  # Not read yet
                    "notifying_department": 1
                },
                {
                    "id": 2,
                    "folio": "REQ-2025-000002",
                    "comment": "La licencia comercial ha sido aprobada. Puede proceder con el pago de los derechos correspondientes.",
                    "notification_type": 2,
                    "notified": 1,  # Already read
                    "notifying_department": 2
                },
                {
                    "id": 3,
                    "folio": "REQ-2025-000003",
                    "comment": "Se requiere documentación adicional para procesar su solicitud de licencia de bar. Favor de revisar los requisitos.",
                    "notification_type": 1,
                    "notified": 0,  # Not read yet
                    "notifying_department": 3
                },
                {
                    "id": 4,
                    "folio": "REQ-2025-000001",
                    "comment": "Su trámite ha avanzado a la siguiente etapa. Se ha programado una inspección para verificar las condiciones del local.",
                    "notification_type": 3,
                    "notified": 0,  # Not read yet
                    "notifying_department": 1
                },
                {
                    "id": 5,
                    "folio": "REQ-2025-000002",
                    "comment": "Recordatorio: El pago de derechos debe realizarse dentro de los próximos 5 días hábiles.",
                    "notification_type": 4,
                    "notified": 1,  # Already read
                    "notifying_department": 4
                }
            ]
            
            for notification in notifications_data:
                query = text("""
                    INSERT INTO notifications (
                        id, user_id, applicant_email, comment, folio,
                        creation_date, seen_date, notified, notifying_department,
                        notification_type, resolution_id, created_at, updated_at
                    ) VALUES (
                        :id, :user_id, :applicant_email, :comment, :folio,
                        :creation_date, :seen_date, :notified, :notifying_department,
                        :notification_type, 0, :created_at, :updated_at
                    )
                    ON CONFLICT (id) DO NOTHING
                """)
                
                seen_date = datetime.now() - timedelta(hours=2) if notification["notified"] == 1 else None
                
                db.execute(query, {
                    "id": notification["id"],
                    "user_id": USER_ID,
                    "applicant_email": USER_EMAIL,
                    "comment": notification["comment"],
                    "folio": notification["folio"],
                    "creation_date": datetime.now() - timedelta(days=notification["id"]),
                    "seen_date": seen_date,
                    "notified": notification["notified"],
                    "notifying_department": notification["notifying_department"],
                    "notification_type": notification["notification_type"],
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })
            
            # 4. Create some test files for getFileTipo endpoint
            # First, create some test renewals (refrendos)
            refrendos_data = [
                {"id": 1, "id_tramite": 1, "year": 2025, "status": 1},
                {"id": 2, "id_tramite": 2, "year": 2025, "status": 1},
                {"id": 3, "id_tramite": 3, "year": 2025, "status": 1}
            ]
            
            # Note: The original query references tables that might not exist in the new schema
            # We'll create mock data that matches what the endpoint expects
            for refrendo in refrendos_data:
                try:
                    # Check if refrendos table exists, if not skip this part
                    check_table = text("SELECT 1 FROM information_schema.tables WHERE table_name = 'refrendos' LIMIT 1")
                    result = db.execute(check_table)
                    if result.fetchone():
                        query = text("""
                            INSERT INTO refrendos (id, id_tramite, year, status, created_at, updated_at)
                            VALUES (:id, :id_tramite, :year, :status, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        
                        db.execute(query, {
                            "id": refrendo["id"],
                            "id_tramite": refrendo["id_tramite"],
                            "year": refrendo["year"],
                            "status": refrendo["status"],
                            "created_at": datetime.now(),
                            "updated_at": datetime.now()
                        })
                        
                        # Create corresponding archive files
                        check_archive_table = text("SELECT 1 FROM information_schema.tables WHERE table_name = 'refrendo_archivos' LIMIT 1")
                        archive_result = db.execute(check_archive_table)
                        if archive_result.fetchone():
                            archive_query = text("""
                                INSERT INTO refrendo_archivos (id, id_refrendo, file_path, file_type, created_at, updated_at)
                                VALUES (:id, :id_refrendo, :file_path, :file_type, :created_at, :updated_at)
                                ON CONFLICT (id) DO NOTHING
                            """)
                            
                            # Create multiple files per refrendo
                            file_types = ["scanned_pdf", "reason_file", "additional_doc"]
                            for j, file_type in enumerate(file_types, 1):
                                file_id = (refrendo["id"] - 1) * 3 + j
                                db.execute(archive_query, {
                                    "id": file_id,
                                    "id_refrendo": refrendo["id"],
                                    "file_path": f"/uploads/refrendos/{refrendo['id']}/{file_type}_{file_id}.pdf",
                                    "file_type": file_type,
                                    "created_at": datetime.now(),
                                    "updated_at": datetime.now()
                                })
                except Exception as e:
                    logger.warning(f"Could not create refrendo data (table might not exist): {e}")
                    # Continue without creating refrendo data
                    pass
            
            # Commit all changes
            db.commit()
            
            logger.info("✅ Test data created successfully!")
            logger.info("\n📋 Summary of created data:")
            logger.info(f"👤 User ID: {USER_ID}")
            logger.info(f"🏛️  Municipality ID: {MUNICIPALITY_ID}")
            logger.info(f"📧 User Email: {USER_EMAIL}")
            logger.info(f"📁 Requirements Queries: {len(folios_data)}")
            logger.info(f"⚙️  Procedures: {len(folios_data)}")
            logger.info(f"🔔 Notifications: {len(notifications_data)}")
            logger.info(f"📄 Refrendos: {len(refrendos_data)} (if table exists)")
            
            logger.info("\n🧪 Test endpoints with:")
            logger.info("1. GET /v1/notifications/ - List notifications")
            logger.info("2. PATCH /v1/notifications/{id}/read - Mark notification as read")
            logger.info("3. GET /v1/notifications/procedure/{id}/files - Get procedure files")
            
            logger.info("\n🔗 Legacy compatibility endpoints:")
            logger.info("1. GET /v1/notifications/listadoNotificaciones")
            logger.info("2. GET /v1/notifications/updateNotificacion/{id}")
            logger.info("3. GET /v1/notifications/getFileTipo/{id}")
            
        except Exception as e:
            logger.error(f"❌ Error creating test data: {e}")
            db.rollback()
            raise

def cleanup_test_data():
    """Clean up test data"""
    from config.settings import SYNC_DATABASE_URL
    engine = create_engine(SYNC_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        try:
            logger.info("🧹 Cleaning up test data...")
            
            # Clean up in reverse order of dependencies
            cleanup_queries = [
                "DELETE FROM refrendo_archivos WHERE id_refrendo IN (1, 2, 3)",
                "DELETE FROM refrendos WHERE id IN (1, 2, 3)",
                "DELETE FROM notifications WHERE id IN (1, 2, 3, 4, 5)",
                "DELETE FROM procedures WHERE id IN (1, 2, 3)",
                "DELETE FROM requirements_querys WHERE id IN (1, 2, 3)"
            ]
            
            for query_str in cleanup_queries:
                try:
                    db.execute(text(query_str))
                except Exception as e:
                    logger.warning(f"Could not execute cleanup query (table might not exist): {e}")
            
            db.commit()
            logger.info("✅ Test data cleaned up successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up test data: {e}")
            db.rollback()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage test data for notifications endpoints")
    parser.add_argument("--cleanup", action="store_true", help="Clean up test data instead of creating it")
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_test_data()
    else:
        create_test_data()
