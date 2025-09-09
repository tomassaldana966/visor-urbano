#!/usr/bin/env python3
"""
Seeder script for creating Spanish business permit fields.
This script creates fields with Spanish names and descriptions that match
the legacy API structure but with English property names in responses.
"""

import asyncio
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import SessionLocal
from app.models.field import Field
from sqlalchemy.ext.asyncio import AsyncSession

async def create_spanish_fields():
    """Create Spanish business permit fields for testing"""
    
    # Spanish fields matching legacy API structure
    spanish_fields = [
        {
            "name": "nombre_empresa",
            "field_type": "text",
            "description": "Nombre legal de la empresa o establecimiento",
            "description_rec": "Ingrese el nombre exacto como aparece en documentos oficiales",
            "rationale": "Requerido para identificación y licenciamiento del negocio",
            "step": 1,
            "sequence": 1,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "correo_empresa",
            "field_type": "email", 
            "description": "Dirección de correo electrónico principal para comunicaciones comerciales",
            "description_rec": "Proporcione una dirección de correo válida que revise regularmente",
            "rationale": "Requerido para comunicaciones oficiales y notificaciones",
            "step": 1,
            "sequence": 2,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "rfc_empresa",
            "field_type": "text",
            "description": "Registro Federal de Contribuyentes de la empresa",
            "description_rec": "Formato: AAAA######AAA para personas morales",
            "rationale": "Obligatorio para fines fiscales y de registro",
            "step": 1,
            "sequence": 3,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "telefono_empresa",
            "field_type": "text",
            "description": "Número de teléfono principal del negocio",
            "description_rec": "Incluya código de área. Formato: (55) 1234-5678",
            "rationale": "Para contacto directo y verificación",
            "step": 1,
            "sequence": 4,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "direccion_establecimiento",
            "field_type": "textarea",
            "description": "Dirección completa donde operará el establecimiento",
            "description_rec": "Incluya calle, número, colonia, código postal",
            "rationale": "Requerido para inspección y ubicación del negocio",
            "step": 2,
            "sequence": 5,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "tipo_giro",
            "field_type": "select",
            "description": "Tipo de giro comercial o actividad principal",
            "description_rec": "Seleccione la actividad principal del negocio",
            "rationale": "Determina los requisitos específicos y permisos necesarios",
            "options": "Restaurante|Tienda de Abarrotes|Farmacia|Consultoría|Manufactura|Servicios|Otro",
            "options_description": "Restaurante - Servicio de alimentos|Tienda de Abarrotes - Venta de productos básicos|Farmacia - Venta de medicamentos|Consultoría - Servicios profesionales|Manufactura - Producción de bienes|Servicios - Servicios diversos|Otro - Especificar en comentarios",
            "step": 2,
            "sequence": 6,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "numero_empleados",
            "field_type": "number",
            "description": "Número aproximado de empleados",
            "description_rec": "Incluya empleados de tiempo completo y parcial",
            "rationale": "Para determinar requisitos de seguridad y capacidad",
            "step": 2,
            "sequence": 7,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "fecha_inicio_operaciones",
            "field_type": "date",
            "description": "Fecha prevista de inicio de operaciones",
            "description_rec": "Seleccione la fecha cuando planea abrir el negocio",
            "rationale": "Para programar inspecciones y seguimiento",
            "step": 2,
            "sequence": 8,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "venta_alcohol",
            "field_type": "boolean",
            "description": "¿El establecimiento venderá bebidas alcohólicas?",
            "description_rec": "Marque si planea vender cualquier tipo de bebida alcohólica",
            "rationale": "Requiere permisos adicionales específicos",
            "step": 2,
            "sequence": 9,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "horario_operacion",
            "field_type": "text",
            "description": "Horario de operación del establecimiento",
            "description_rec": "Ejemplo: Lunes a Viernes 9:00-18:00, Sábados 9:00-14:00",
            "rationale": "Para verificar cumplimiento de regulaciones locales",
            "step": 3,
            "sequence": 10,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        }
    ]
    
    # Additional fields for municipality 2
    additional_fields = [
        {
            "name": "comentarios_adicionales",
            "field_type": "textarea",
            "description": "Comentarios o información adicional",
            "description_rec": "Proporcione cualquier información relevante no cubierta en otros campos",
            "rationale": "Para aclaraciones y información complementaria",
            "step": 3,
            "sequence": 11,
            "required": 0,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "acepta_terminos",
            "field_type": "boolean",
            "description": "Acepto los términos y condiciones",
            "description_rec": "Debe aceptar para continuar con el trámite",
            "rationale": "Confirmación legal requerida",
            "step": 3,
            "sequence": 12,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        },
        {
            "name": "firma_solicitante",
            "field_type": "text",
            "description": "Nombre completo del solicitante para firma digital",
            "description_rec": "Escriba su nombre completo como aparece en identificación oficial",
            "rationale": "Validación de identidad del solicitante",
            "step": 3,
            "sequence": 13,
            "required": 1,
            "municipality_id": 2,
            "procedure_type": "oficial",
            "status": 1
        }
    ]
    
    async with SessionLocal() as session:
        try:
            print("Creating Spanish business permit fields...")
            
            # Create municipality-specific fields
            for field_data in spanish_fields:
                field = Field(**field_data)
                session.add(field)
                print(f"  ✓ Added field: {field_data['name']}")
            
            # Create additional fields for municipality 2
            for field_data in additional_fields:
                field = Field(**field_data)
                session.add(field)
                print(f"  ✓ Added additional field: {field_data['name']}")
            
            await session.commit()
            print(f"\n✅ Successfully created {len(spanish_fields + additional_fields)} Spanish fields!")
            print("   - Municipality-specific fields (municipality_id=2):", len(spanish_fields))
            print("   - Additional fields (municipality_id=2):", len(additional_fields))
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error creating fields: {e}")
            raise

async def main():
    print("🌱 Spanish Fields Seeder")
    print("=" * 50)
    await create_spanish_fields()
    print("\n🎉 Seeding completed!")

if __name__ == "__main__":
    asyncio.run(main())
