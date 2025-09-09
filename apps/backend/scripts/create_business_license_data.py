#!/usr/bin/env python3
"""
Script to create BusinessLicense data for testing business commercial procedures
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import get_sync_db
from app.models.procedures import Procedure
from app.models.business_license import BusinessLicense
from app.models.municipality import Municipality
from app.models.business_sectors import BusinessSector
from datetime import datetime

def create_business_license_data():
    """Create BusinessLicense data for testing"""
    
    db = next(get_sync_db())
    try:
        print("Creating BusinessLicense data for testing...")
        
        # Get GIRO procedures
        giro_procedures = db.query(Procedure).filter(
            Procedure.procedure_type.like('%giro%')
        ).all()
        
        print(f"Found {len(giro_procedures)} GIRO procedures")
        
        if not giro_procedures:
            print("No GIRO procedures found!")
            return
        
        for proc in giro_procedures:
            print(f"  {proc.folio} - {proc.procedure_type} - Municipality: {proc.municipality_id}")
        
        # Get business sectors for SCIAN codes
        business_sectors = db.query(BusinessSector).all()
        sector_codes = [sector.code for sector in business_sectors]
        print(f"Available SCIAN codes: {sector_codes}")
        
        # Business activities and corresponding SCIAN codes
        business_data = [
            {
                "activity": "Restaurante",
                "scian": "722511",
                "owner": "María González Pérez",
                "area": "150 m²",
                "opening": "08:00",
                "closing": "22:00"
            },
            {
                "activity": "Farmacia",
                "scian": "461110", 
                "owner": "Carlos Rodríguez López",
                "area": "80 m²",
                "opening": "07:00",
                "closing": "23:00"
            },
            {
                "activity": "Tienda de Abarrotes",
                "scian": "461130",
                "owner": "Ana Patricia Morales",
                "area": "120 m²", 
                "opening": "06:00",
                "closing": "21:00"
            },
            {
                "activity": "Panadería",
                "scian": "311811",
                "owner": "José Luis Martínez",
                "area": "90 m²",
                "opening": "05:00", 
                "closing": "20:00"
            }
        ]
        
        created_count = 0
        for i, procedure in enumerate(giro_procedures):
            print(f"\nProcessing procedure {procedure.folio}...")
            
            # Check if license already exists
            existing = db.query(BusinessLicense).filter(
                BusinessLicense.license_folio == procedure.folio
            ).first()
            
            if existing:
                print(f"  License already exists for {procedure.folio}")
                continue
            
            # Use business data cyclically
            business_info = business_data[i % len(business_data)]
            
            print(f"  Creating license with data: {business_info}")
            
            # Create new business license
            new_license = BusinessLicense(
                owner=business_info["owner"],
                license_folio=procedure.folio,
                commercial_activity=business_info["activity"],
                industry_classification_code=business_info["scian"],
                authorized_area=business_info["area"],
                opening_time=business_info["opening"],
                closing_time=business_info["closing"],
                license_year=2024,
                license_category=1,
                generated_by_user_id=1,
                municipality_id=procedure.municipality_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.add(new_license)
            created_count += 1
            print(f"  Created license for {procedure.folio}: {business_info['activity']} ({business_info['scian']})")
        
        print(f"\nCommitting {created_count} business licenses...")
        db.commit()
        print(f"Successfully created {created_count} business licenses!")
        
        # Verify the data
        total_licenses = db.query(BusinessLicense).count()
        print(f"Total business licenses in database: {total_licenses}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Script starting...")
    create_business_license_data()
    print("Script finished.")
