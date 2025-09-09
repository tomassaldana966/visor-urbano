import base64
import io
import json
import logging
import os
import traceback
from datetime import datetime

import qrcode
from fastapi import HTTPException, status
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from weasyprint import HTML, CSS

from app.models.answer import Answer
from app.models.field import Field
from app.models.municipality import Municipality
from app.models.procedures import Procedure
from app.models.requirements import Requirement
from app.models.requirements_query import RequirementsQuery
from app.schemas.requirements_queries import (
    ProcedureInfoSchema,
    ProcedureRenewalInfoSchema,
    ProcedureTypeInfoSchema,
    RequirementsPdfSchema,
    RequirementsQueryCreateSchema,
    RequirementsQueryCreateWithDynamicFieldsSchema,
    RequirementsQueryOutSchema,
)

logger = logging.getLogger(__name__)

# Get the absolute path to the templates directory
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")

# Initialize Jinja2 environment for PDF templates
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(["html", "xml"])
)


class RequirementsQueriesService:
    @staticmethod
    async def get_procedure_info(folio: str, db: AsyncSession) -> ProcedureInfoSchema:
        try:
            stmt = select(RequirementsQuery).filter(
                RequirementsQuery.folio == folio
            )
            result = await db.execute(stmt)
            query = result.scalar_one_or_none()
            
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Procedure with folio {folio} not found"
                )
            
            proc_stmt = select(Procedure).filter(
                Procedure.requirements_query_id == query.id
            )
            proc_result = await db.execute(proc_stmt)
            procedures = proc_result.scalars().all()
            
            procedure_data = {
                "id": query.id,
                "folio": query.folio,
                "street": query.street,
                "neighborhood": query.neighborhood,
                "municipality_name": query.municipality_name,
                "scian_code": query.scian_code,
                "scian_name": query.scian_name,
                "property_area": float(query.property_area),
                "activity_area": float(query.activity_area),
                "applicant_name": query.applicant_name,
                "status": query.status,
                "created_at": query.created_at.isoformat() if query.created_at else None
            }
            
            requirements = [
                {
                    "id": proc.id,
                    "name": proc.name,
                    "status": proc.status,
                    "requirements": proc.requirements or []
                }
                for proc in procedures
            ]
            
            return ProcedureInfoSchema(
                folio=folio,
                procedure_data=procedure_data,
                requirements=requirements,
                status="active" if query.status == 1 else "inactive"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting procedure info for folio {folio}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while retrieving procedure information"
            )

    @staticmethod
    async def get_procedure_info_type(folio: str, db: AsyncSession) -> ProcedureTypeInfoSchema:
        try:
            stmt = select(RequirementsQuery).filter(
                RequirementsQuery.folio == folio
            )
            result = await db.execute(stmt)
            query = result.scalar_one_or_none()
            
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Procedure with folio {folio} not found"
                )
            
            procedure_type = "standard"
            if query.alcohol_sales == 1:
                procedure_type = "alcohol_sales"
            elif "industrial" in query.scian_name.lower():
                procedure_type = "industrial"
            elif "commercial" in query.scian_name.lower():
                procedure_type = "commercial"
            
            type_data = {
                "type": procedure_type,
                "scian_code": query.scian_code,
                "scian_name": query.scian_name,
                "alcohol_sales": query.alcohol_sales,
                "property_area": float(query.property_area),
                "activity_area": float(query.activity_area)
            }
            
            return ProcedureTypeInfoSchema(
                folio=folio,
                procedure_type=procedure_type,
                type_data=type_data
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting procedure type for folio {folio}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while retrieving procedure type"
            )

    @staticmethod
    async def get_procedure_info_renewal(folio: str, db: AsyncSession) -> ProcedureRenewalInfoSchema:
        try:
            stmt = select(RequirementsQuery).filter(
                RequirementsQuery.folio == folio
            )
            result = await db.execute(stmt)
            query = result.scalar_one_or_none()
            
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Procedure with folio {folio} not found"
                )
            
            renewals_data = []
            for renewal in query.renewals:
                renewals_data.append({
                    "id": renewal.id,
                    "renewal_date": renewal.created_at.isoformat() if renewal.created_at else None,
                    "procedure_id": renewal.procedure_id,
                    "notes": f"Renewal for procedure {renewal.procedure_id}" if renewal.procedure_id else "General renewal"
                })
            
            renewal_data = {
                "original_folio": query.folio,
                "primary_folio": query.primary_folio,
                "renewals_count": len(renewals_data),
                "renewals": renewals_data
            }
            
            renewal_requirements = [
                {"name": "Updated business license", "required": True},
                {"name": "Property verification", "required": True},
                {"name": "Tax compliance certificate", "required": True}
            ]
            
            return ProcedureRenewalInfoSchema(
                folio=folio,
                renewal_data=renewal_data,
                renewal_requirements=renewal_requirements
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting renewal info for folio {folio}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while retrieving renewal information"
            )

    @staticmethod
    async def get_requirements_pdf(folio: str, requirement_id: int, db: AsyncSession) -> RequirementsPdfSchema:
        try:
            stmt = select(RequirementsQuery).filter(
                RequirementsQuery.folio == folio
            )
            result = await db.execute(stmt)
            query = result.scalar_one_or_none()
            
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Procedure with folio {folio} not found"
                )
            
            proc_stmt = select(Procedure).filter(
                and_(
                    Procedure.requirements_query_id == query.id,
                    Procedure.id == requirement_id
                )
            )
            proc_result = await db.execute(proc_stmt)
            procedure = proc_result.scalar_one_or_none()
            
            if not procedure:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Requirement {requirement_id} not found for folio {folio}"
                )
            
            # Generate QR code for verification
            verification_url = f"https://visorurbano.jalisco.gob.mx/verify/{folio}/{requirement_id}"
            qr = qrcode.make(verification_url)
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            qr_code_base64 = base64.b64encode(buf.getvalue()).decode()
            
            # Prepare data for template
            address = f"{query.street}, {query.neighborhood}" if query.street and query.neighborhood else "Address not specified"
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # Parse restrictions if available
            restrictions = {
                "schools": 0,
                "health_centers": 0, 
                "government_buildings": 0,
                "construction_blocks": 0,
                "water_bodies": 0
            }
            
            if query.restrictions:
                try:
                    if isinstance(query.restrictions, str):
                        restrictions_data = json.loads(query.restrictions)
                    else:
                        restrictions_data = query.restrictions
                    
                    restrictions.update({
                        "schools": restrictions_data.get("schools", restrictions_data.get("escuelas", 0)),
                        "health_centers": restrictions_data.get("health_centers", restrictions_data.get("centros_salud", 0)),
                        "government_buildings": restrictions_data.get("government_buildings", restrictions_data.get("edificios_gobierno", 0)),
                        "construction_blocks": restrictions_data.get("construction_blocks", restrictions_data.get("bloque_construccion_actividad", 0)),
                        "water_bodies": restrictions_data.get("water_bodies", restrictions_data.get("cuerpos_agua", 0))
                    })
                except Exception as e:
                    logger.warning(f"Error parsing restrictions: {e}")
            
            # Map alcohol sales value to English description
            alcohol_sales_mapping = {
                0: "Does not include",
                1: "Low alcohol content beverages in closed bottles",
                2: "Low alcohol content beverages in open bottles", 
                3: "High alcohol content beverages in closed bottles",
                4: "High alcohol content beverages in open bottles"
            }
            alcohol_sales_desc = alcohol_sales_mapping.get(query.alcohol_sales or 0, "Does not include")
            
            # Fetch requirements based on license type
            if hasattr(query, 'license_type') and query.license_type == 'construction':
                # Use construction-specific requirements
                requirements = await RequirementsQueriesService._get_construction_requirements(
                    query.municipality_id, db
                )
            else:
                # Use standard commercial requirements
                requirements = await RequirementsQueriesService._get_requirements_for_municipality(
                    query.municipality_id, db
                )
            
            # If procedure has specific requirements, use those instead
            if hasattr(procedure, 'requirements') and procedure.requirements:
                requirements = []
                for i, req in enumerate(procedure.requirements):
                    requirements.append({
                        "title": f"Requirement {i+1}",
                        "description": req if isinstance(req, str) else str(req),
                        "department_issued": False
                    })
            
            template_data = {
                "folio": query.folio,
                "address": address,
                "municipality": query.municipality_name or "Municipality",
                "current_date": current_date,
                "procedure_id": procedure.id,
                "requirements": requirements,
                "qr_code": qr_code_base64,
                
                # License type information
                "license_type": getattr(query, 'license_type', 'commercial'),
                "interested_party": getattr(query, 'interested_party', None),
                
                # Applicant information
                "applicant_name": query.applicant_name or "Not specified",
                "applicant_type": "Individual" if query.person_type in ["fisica", "individual"] else "Legal entity" if query.person_type in ["moral", "legal"] else "Individual",
                "applicant_character": query.applicant_character or "Owner",
                
                # Property and activity information  
                "activity_name": query.scian_name or "General commercial activity",
                "activity_code": query.scian_code or "N/A",
                "alcohol_sales": alcohol_sales_desc,
                "property_surface": str(query.property_area) if query.property_area else "N/A",
                "activity_surface": str(query.activity_area) if query.activity_area else "N/A",
                
                # Department contact information
                "department_address": "Address not provided",
                "department_phone": "Phone not provided",
                
                # Map information
                "minimap_url": query.minimap_url,
                
                # Restrictions
                "restrictions": restrictions,
                
                # License fee (placeholder)
                "license_fee": "$2,500.00",
                
                # Information requests (placeholder)
                "information_requests": [
                    {
                        "description": "Type of business establishment",
                        "response": query.scian_name or "Not specified"
                    },
                    {
                        "description": "Includes alcohol sales",
                        "response": "Yes" if query.alcohol_sales and query.alcohol_sales > 0 else "No"
                    }                 
                ]
            }
            
            # Load and render the HTML template
            try:
                template = env.get_template("requirements_pdf_template.html")
                html_content = template.render(**template_data)
            except Exception as template_error:
                logger.error(f"Error loading template: {str(template_error)}")
                logger.error(f"Template error type: {type(template_error)}")
                
                logger.error(f"Full traceback: {traceback.format_exc()}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error loading PDF template: {str(template_error)}"
                )
            
            # Generate PDF using WeasyPrint
            try:
                pdf_bytes = HTML(string=html_content).write_pdf(
                    stylesheets=[
                        CSS(string='@page { size: A4; margin: 2cm }')
                    ]
                )
                pdf_base64 = base64.b64encode(pdf_bytes).decode()
            except Exception as pdf_error:
                logger.error(f"Error generating PDF: {str(pdf_error)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error generating PDF document"
                )
            
            filename = f"requirements_{folio}_{requirement_id}.pdf"
            
            return RequirementsPdfSchema(
                folio=folio,
                requirement_id=requirement_id,
                pdf_data=pdf_base64,
                filename=filename
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error generating PDF for folio {folio}, requirement {requirement_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while generating requirements PDF"
            )

    @staticmethod
    async def submit_requirements_query(data: RequirementsQueryCreateSchema, db: AsyncSession) -> RequirementsQueryOutSchema:
        try:
            if not data.folio:
                current_year = datetime.now().year
                count_stmt = select(RequirementsQuery).filter(
                    RequirementsQuery.year_folio == current_year
                )
                count_result = await db.execute(count_stmt)
                year_count = len(count_result.scalars().all()) + 1
                data.folio = f"REQ-{current_year}-{year_count:06d}"
            
            # Fetch municipality to get issue_license value
            municipality_stmt = select(Municipality).filter(Municipality.id == data.municipality_id)
            municipality_result = await db.execute(municipality_stmt)
            municipality = municipality_result.scalars().first()
            issue_license_value = municipality.issue_license if municipality else 0
            
            new_query = RequirementsQuery(
                folio=data.folio,
                street=data.street,
                neighborhood=data.neighborhood,
                municipality_name=data.municipality_name,
                municipality_id=data.municipality_id,
                scian_code=data.scian_code,
                scian_name=data.scian_name,
                property_area=data.property_area,
                activity_area=data.activity_area,
                applicant_name=data.applicant_name,
                applicant_character=data.applicant_character,
                person_type=data.person_type,
                minimap_url=data.minimap_url,
                restrictions=data.restrictions,
                alcohol_sales=data.alcohol_sales,
                primary_folio=data.primary_folio,
                issue_license=issue_license_value,
                status=1,
                user_id=1,
                year_folio=datetime.now().year,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.add(new_query)
            await db.commit()
            await db.refresh(new_query)
            
            return RequirementsQueryOutSchema.model_validate(new_query)
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error submitting requirements query: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while submitting requirements query"
            )

    @staticmethod
    async def submit_requirements_query_with_dynamic_fields(
        data: RequirementsQueryCreateWithDynamicFieldsSchema, 
        db: AsyncSession,
        current_user = None
    ) -> dict:
        try:
            municipality_id = data.municipality_id
            current_year = datetime.now().year
            
            count_stmt = select(RequirementsQuery).filter(
                and_(
                    RequirementsQuery.municipality_id == municipality_id,
                    RequirementsQuery.year_folio == current_year
                )
            )
            count_result = await db.execute(count_stmt)
            municipality_count = len(count_result.scalars().all()) + 1
            
            # Check license type first to determine folio format
            license_type = data.license_type or (data.dynamic_fields.get('license_type') if data.dynamic_fields else None)
            
            if license_type == 'construction':
                folio = f"CONS-{current_year}-{municipality_count:04d}"
            else:
                folio = f"{municipality_id}-{municipality_count}/{current_year}"
            
            # Fetch municipality to get issue_license value
            municipality_stmt = select(Municipality).filter(Municipality.id == municipality_id)
            municipality_result = await db.execute(municipality_stmt)
            municipality = municipality_result.scalars().first()
            issue_license_value = municipality.issue_license if municipality else 0
            
            # Check license type from direct field or dynamic fields (already checked above)
            
            # Prepare base fields
            base_fields = {
                "folio": folio,
                "street": data.street or "",
                "neighborhood": data.neighborhood or "",
                "municipality_name": data.municipality_name or "",
                "municipality_id": data.municipality_id,
                "property_area": data.property_area or 0,
                "applicant_name": data.applicant_name or "",
                "applicant_character": data.applicant_character or "",
                "person_type": data.person_type or "",
                "minimap_url": data.minimap_url or "",
                "restrictions": data.restrictions,
                "primary_folio": data.primary_folio,
                "issue_license": issue_license_value,
                "status": 1,
                "user_id": current_user.id if current_user else 1,
                "year_folio": current_year,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "license_type": license_type
            }
            
            # Handle specific fields based on license type
            if license_type == 'construction':
                # For construction licenses, auto-generate fields and get specific data
                base_fields.update({
                    "scian_code": "CONST",  # Default for construction
                    "scian_name": "Construcción",  # Default for construction
                    "activity_area": data.activity_area or 0,
                    "alcohol_sales": 0,  # Default for construction
                    "entry_date": datetime.now().date(),  # Auto-generate current date
                    "interested_party": data.interested_party or (data.dynamic_fields.get('interested_party') if data.dynamic_fields else ""),
                    "last_resolution": "",  # Empty as requested
                    "resolution_sense": ""  # Empty as requested
                })
            else:
                # For commercial licenses (default behavior)
                base_fields.update({
                    "scian_code": data.scian_code or "",
                    "scian_name": data.scian_name or "",
                    "activity_area": data.activity_area or 0,
                    "alcohol_sales": data.alcohol_sales or 0
                })
                
                # Add commercial-specific fields if present
                if data.scian:
                    base_fields["scian"] = data.scian
                if data.entry_date:
                    base_fields["entry_date"] = data.entry_date
                else:
                    base_fields["entry_date"] = datetime.now().date()  # Auto-generate for commercial too
            
            new_query = RequirementsQuery(**base_fields)
            
            db.add(new_query)
            await db.commit()
            await db.refresh(new_query)
            
            # NOTE: We don't create the procedure automatically here anymore.
            # The procedure will be created later when the authenticated user 
            # calls the /procedures/entry endpoint with the requirements_query_id.
            
            # Save dynamic field answers to the answers table WITHOUT procedure ID
            # These answers will be associated with the procedure later when it's created
            # Save dynamic field answers for later retrieval during procedure editing
            # These answers are associated with the requirements_query initially
            # and will be copied to the procedure when it's created
            if data.dynamic_fields:
                for field_name, field_value in data.dynamic_fields.items():
                    if field_value is not None and field_value != "":  # Only save non-empty values
                        answer = Answer(
                            procedure_id=None,  # Will be set when procedure is created
                            requirements_query_id=new_query.id,  # Associate with requirements_query
                            name=field_name,
                            value=str(field_value),
                            user_id=None,  # Anonymous user since this is pre-authentication
                            status=1,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        db.add(answer)
                
                # Commit the answers
                await db.commit()
            
            # Process requirements based on license type
            if license_type == 'construction':
                # For construction licenses, generate construction-specific requirements
                construction_requirements = await RequirementsQueriesService._get_construction_requirements(
                    data.municipality_id, 
                    db
                )
                requirements_data = {
                    "folio": folio,
                    "license_type": "construction",
                    "requirements": construction_requirements,
                    "total_requirements": len(construction_requirements),
                    "municipality_name": data.municipality_name or "",
                    "address": f"{data.street or ''}, {data.neighborhood or ''}".strip(', '),
                    "interested_party": data.interested_party or ""
                }
            else:
                # For commercial licenses, use original dynamic requirements processing
                requirements_data = await RequirementsQueriesService._process_dynamic_requirements(
                    new_query.id, 
                    data.municipality_id, 
                    data.scian_code,
                    data.dynamic_fields or {}, 
                    db
                )
            
            # Fetch municipality to get issue_license value
            municipality_stmt = select(Municipality).filter(Municipality.id == data.municipality_id)
            municipality_result = await db.execute(municipality_stmt)
            municipality = municipality_result.scalars().first()
            issue_license_value = municipality.issue_license if municipality else 0
            
            response_data = {
                **requirements_data,
                "url": f"requirements-queries/{RequirementsQueriesService._encode_folio(folio)}/requirements/pdf",
                "folio": folio,
                "issue_license": issue_license_value
            }
            
            return {
                "data": response_data
            }
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error submitting requirements query with dynamic fields: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while processing requirements query"
            )

    @staticmethod
    async def _process_dynamic_requirements(
        query_id: int, 
        municipality_id: int, 
        scian_code: str,
        dynamic_fields: dict, 
        db: AsyncSession
    ) -> dict:
        try:
            requirements_structure = {}
            for field_name, field_value in dynamic_fields.items():
                requirements_structure[field_name] = {
                    "name": field_name,
                    "answer": field_value,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            standard_requirements = [
                "owner_identification",
                "property_document", 
                "owner_first_name",
                "owner_last_name_1",
                "owner_last_name_2",
                "owner_curp",
                "owner_rfc",
                "owner_email",
                "owner_address",
                "owner_ext_number",
                "owner_int_number",
                "owner_neighborhood",
                "owner_postal_code",
                "property_street",
                "property_ext_number",
                "property_int_number",
                "property_neighborhood",
                "property_postal_code",
                "property_type",
                "business_name",
                "employee_count",
                "estimated_investment",
                "parking_spaces",
                "activity_description",
                "property_tax",
                "property_parking_photo",
                "property_outside_photo",
                "owner_phone",
                "sign_info"
            ]
            
            for req_name in standard_requirements:
                requirements_structure[req_name] = {
                    "field": {
                        "name": req_name,
                        "type": "file" if "photo" in req_name or req_name in ["owner_identification", "property_document", "property_tax"] else "input",
                        "description": RequirementsQueriesService._get_field_description(req_name),
                        "required": 1,
                        "step": RequirementsQueriesService._get_field_step(req_name),
                        "procedure_type": "official"
                    },
                    "type": "file" if "photo" in req_name or req_name in ["owner_identification", "property_document", "property_tax"] else "input",
                    "name": req_name,
                    "answer": None,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            return {
                "license_type": "commercial",
                "requirements": requirements_structure,
                "total_requirements": len(requirements_structure)
            }
            
        except Exception as e:
            logger.error(f"Error processing dynamic requirements: {str(e)}")
            raise
    
    @staticmethod
    def _encode_folio(folio: str) -> str:
        return base64.b64encode(folio.encode()).decode()
    
    @staticmethod 
    def _get_field_description(field_name: str) -> str:
        descriptions = {
            "owner_identification": "Owner identification",
            "property_document": "Document proving property ownership", 
            "owner_first_name": "Owner's first name",
            "owner_last_name_1": "Owner's last name",
            "owner_last_name_2": "Owner's second last name",
            "owner_curp": "Owner's CURP",
            "owner_rfc": "Owner's RFC",
            "owner_email": "Owner's email",
            "owner_address": "Owner's address",
            "owner_ext_number": "Exterior number and/or letter",
            "owner_int_number": "Interior number and/or letter",
            "owner_neighborhood": "Neighborhood",
            "owner_postal_code": "Postal code",
            "property_street": "Official property street",
            "property_ext_number": "Property exterior number and/or letter",
            "property_int_number": "Property interior number and/or letter", 
            "property_neighborhood": "Property neighborhood",
            "property_postal_code": "Property postal code",
            "property_type": "Property type",
            "business_name": "Business name",
            "employee_count": "Number of employees",
            "estimated_investment": "Estimated investment",
            "parking_spaces": "Number of parking spaces",
            "activity_description": "Description of activity to be performed",
            "property_tax": "Updated property tax payment receipt",
            "property_parking_photo": "Photos of the property and parking",
            "property_outside_photo": "3 photos of the property from outside",
            "owner_phone": "Owner's phone number",
            "sign_info": "Sign information"
        }
        return descriptions.get(field_name, field_name.replace("_", " ").title())
    
    @staticmethod
    def _get_field_step(field_name: str) -> int:
        if "owner" in field_name:
            return 2
        elif "property" in field_name:
            return 3
        else:
            return 4

    @staticmethod
    async def _get_requirements_for_municipality(municipality_id: int, db: AsyncSession) -> list:
        """
        Fetch requirements from the database for a given municipality.
        
        Args:
            municipality_id: The ID of the municipality
            db: Database session
            
        Returns:
            List of requirement dictionaries with title, description, and department_issued fields
        """
        try:
            # Query requirements for the municipality with field details
            stmt = select(Requirement, Field).join(
                Field, Requirement.field_id == Field.id
            ).filter(
                Requirement.municipality_id == municipality_id
            ).order_by(Field.sequence.asc(), Field.name.asc())
            
            result = await db.execute(stmt)
            requirement_records = result.all()
            
            if not requirement_records:
                logger.warning(f"No requirements found for municipality {municipality_id}, using default requirements")
                # Return default requirements if none found in database
                return [
                    {
                        "title": "Official identification of the owner",
                        "description": "Present valid official identification (voting card, passport, or professional license).",
                        "department_issued": False
                    },
                    {
                        "title": "Property ownership proof", 
                        "description": "Document proving legal ownership of the property (public deed, purchase contract, etc.).",
                        "department_issued": False
                    },
                    {
                        "title": "Proof of address",
                        "description": "Proof of address no older than 3 months.",
                        "department_issued": False
                    },
                    {
                        "title": "Property tax payment",
                        "description": "Updated property tax payment receipt for the current year.",
                        "department_issued": False
                    }
                ]
            
            # Convert database records to the expected format
            requirements = []
            for requirement, field in requirement_records:
                requirements.append({
                    "title": field.name,
                    "description": field.description or field.description_rec or "No description available",
                    "department_issued": bool(field.required_official) if field.required_official is not None else False
                })
            
            logger.info(f"Found {len(requirements)} requirements for municipality {municipality_id}")
            return requirements
            
        except Exception as e:
            logger.error(f"Error fetching requirements for municipality {municipality_id}: {str(e)}")
            # Return default requirements on error
            return [
                {
                    "title": "Official identification of the owner", 
                    "description": "Present valid official identification (voting card, passport, or professional license).",
                    "department_issued": False
                },
                {
                    "title": "Property ownership proof",
                    "description": "Document proving legal ownership of the property (public deed, purchase contract, etc.).",
                    "department_issued": False
                },
                {
                    "title": "Proof of address",
                    "description": "Proof of address no older than 3 months.",
                    "department_issued": False
                },
                {
                    "title": "Property tax payment",
                    "description": "Updated property tax payment receipt for the current year.",
                    "department_issued": False
                }
            ]

    @staticmethod
    async def get_folio_requirements_pdf(folio: str, db: AsyncSession) -> RequirementsPdfSchema:
        """
        Generate PDF with all requirements for a given folio.
        This function doesn't require a specific requirement_id.
        """
        try:
            stmt = select(RequirementsQuery).filter(
                RequirementsQuery.folio == folio
            )
            result = await db.execute(stmt)
            query = result.scalar_one_or_none()
            
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Procedure with folio {folio} not found"
                )
            
            # Generate QR code for verification (without requirement_id)
            verification_url = f"https://visorurbano.jalisco.gob.mx/verify/{folio}"
            qr = qrcode.make(verification_url)
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            qr_code_base64 = base64.b64encode(buf.getvalue()).decode()
            
            # Prepare data for template
            address = f"{query.street}, {query.neighborhood}" if query.street and query.neighborhood else "Address not specified"
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # Parse restrictions if available
            restrictions = {
                "schools": 0,
                "health_centers": 0, 
                "government_buildings": 0,
                "construction_blocks": 0,
                "water_bodies": 0
            }
            
            if query.restrictions:
                try:
                    if isinstance(query.restrictions, str):
                        restrictions_data = json.loads(query.restrictions)
                    else:
                        restrictions_data = query.restrictions
                    
                    restrictions.update({
                        "schools": restrictions_data.get("schools", restrictions_data.get("escuelas", 0)),
                        "health_centers": restrictions_data.get("health_centers", restrictions_data.get("centros_salud", 0)),
                        "government_buildings": restrictions_data.get("government_buildings", restrictions_data.get("edificios_gobierno", 0)),
                        "construction_blocks": restrictions_data.get("construction_blocks", restrictions_data.get("bloque_construccion_actividad", 0)),
                        "water_bodies": restrictions_data.get("water_bodies", restrictions_data.get("cuerpos_agua", 0))
                    })
                except Exception as e:
                    logger.warning(f"Error parsing restrictions: {e}")
            
            # Map alcohol sales value to English description
            alcohol_sales_mapping = {
                0: "Does not include",
                1: "Low alcohol content beverages in closed bottles",
                2: "Low alcohol content beverages in open bottles", 
                3: "High alcohol content beverages in closed bottles",
                4: "High alcohol content beverages in open bottles"
            }
            alcohol_sales_desc = alcohol_sales_mapping.get(query.alcohol_sales or 0, "Does not include")
            
            # Generate requirements based on license type
            if hasattr(query, 'license_type') and query.license_type == 'construction':
                # Use construction-specific requirements
                construction_requirements = await RequirementsQueriesService._get_construction_requirements(
                    query.municipality_id, db
                )
                requirements_for_template = construction_requirements
            else:
                # Fetch requirements from database for commercial licenses
                fields_stmt = select(Field).filter(
                    Field.municipality_id == query.municipality_id
                ).order_by(Field.step, Field.name)
                fields_result = await db.execute(fields_stmt)
                fields = fields_result.scalars().all()
                
                # Group requirements by step
                requirements_by_step = {}
                for field in fields:
                    step = field.step or 1
                    if step not in requirements_by_step:
                        requirements_by_step[step] = []
                    
                    requirements_by_step[step].append({
                        'name': field.name,
                        'description': field.description,
                        'type': field.field_type,
                        'required': bool(field.required)
                    })
                
                # Convert to template format
                requirements_for_template = [
                    {
                        'title': field['name'].replace('_', ' ').title(),
                        'description': field['description'],
                        'department_issued': field['type'] == 'system'
                    }
                    for step_requirements in requirements_by_step.values()
                    for field in step_requirements
                ]
            
            # Prepare template data
            template_data = {
                'folio': folio,
                'municipality': query.municipality_name or "Municipality",
                'address': address,
                'license_type': getattr(query, 'license_type', 'commercial'),
                'interested_party': getattr(query, 'interested_party', None),
                'applicant_name': query.applicant_name or "Not specified",
                'applicant_character': query.applicant_character or "Not specified",
                'person_type': query.person_type or "Not specified", 
                'activity_name': query.scian_name or "Not specified",
                'activity_code': query.scian_code or "N/A",
                'alcohol_sales': alcohol_sales_desc,
                'property_surface': str(query.property_area or 0),
                'activity_surface': str(query.activity_area or 0),
                'restrictions': restrictions,
                'requirements': requirements_for_template,
                'qr_code': qr_code_base64,
                'current_date': current_date,
                'minimap_url': query.minimap_url
            }
            
            # Load and render Jinja2 template
            try:
                from jinja2 import Environment, FileSystemLoader
                templates_dir = os.path.join(os.path.dirname(__file__), "../../templates")                
                env = Environment(loader=FileSystemLoader(templates_dir))
                template = env.get_template('requirements_pdf_template.html')
                
                html_content = template.render(**template_data)
                    
            except Exception as template_error:
                logger.error(f"Error loading template: {str(template_error)}")
                logger.error(f"Template error type: {type(template_error)}")
                
                logger.error(f"Full traceback: {traceback.format_exc()}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error loading PDF template: {str(template_error)}"
                )
            
            # Generate PDF using WeasyPrint
            try:
                pdf_bytes = HTML(string=html_content).write_pdf(
                    stylesheets=[
                        CSS(string='@page { size: A4; margin: 2cm }')
                    ]
                )
                pdf_base64 = base64.b64encode(pdf_bytes).decode()
            except Exception as pdf_error:
                logger.error(f"Error generating PDF: {str(pdf_error)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error generating PDF document"
                )
            
            filename = f"requirements_{folio}_all.pdf"
            
            return RequirementsPdfSchema(
                folio=folio,
                requirement_id=0,  # 0 indicates all requirements
                pdf_data=pdf_base64,
                filename=filename
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error generating PDF for folio {folio}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while generating requirements PDF"
            )

    @staticmethod
    async def _get_construction_requirements(municipality_id: int, db: AsyncSession) -> list:
        """Get requirements specifically for construction permits from database"""
        try:
            logger.info(f"Fetching construction requirements from database for municipality {municipality_id}")
            
            # Query construction requirements from database
            stmt = (
                select(Field)
                .where(
                    and_(
                        Field.municipality_id == municipality_id,
                        Field.procedure_type == "permits_building_license",
                        Field.status == 1  # Active fields only
                    )
                )
                .order_by(Field.sequence.asc())
            )
            
            result = await db.execute(stmt)
            construction_fields = result.scalars().all()
            
            if not construction_fields:
                logger.warning(f"No construction requirements found in database for municipality {municipality_id}, using fallback")
                return await RequirementsQueriesService._get_fallback_construction_requirements()
            
            # Convert database fields to the expected format
            construction_requirements = []
            for field in construction_fields:
                requirement = {
                    "title": field.name,
                    "description": field.description or field.description_rec or field.name,
                    "department_issued": bool(field.required_official)  # Convert 1/0 to True/False
                }
                construction_requirements.append(requirement)
            
            logger.info(f"Loaded {len(construction_requirements)} construction requirements from database for municipality {municipality_id}")
            return construction_requirements
            
        except Exception as e:
            logger.error(f"Error fetching construction requirements from database for municipality {municipality_id}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Return fallback requirements on error
            return await RequirementsQueriesService._get_fallback_construction_requirements()

    @staticmethod
    async def _get_fallback_construction_requirements() -> list:
        """Fallback construction requirements when database lookup fails"""
        logger.info("Using fallback construction requirements")
        return [
            {
                "title": "Owner official identification",
                "description": "Present valid official identification.",
                "department_issued": False
            },
            {
                "title": "Property public deed",
                "description": "Document that proves ownership of the property.",
                "department_issued": False
            },
            {
                "title": "Architectural project",
                "description": "Architectural plans for the construction project.",
                "department_issued": False
            },
            {
                "title": "Land use permit",
                "description": "Valid land use permit.",
                "department_issued": True
            },
            {
                "title": "Civil protection approval",
                "description": "Civil protection assessment report.",
                "department_issued": True
            }
        ]

async def get_procedure_info(folio: str, db: AsyncSession) -> ProcedureInfoSchema:
    return await RequirementsQueriesService.get_procedure_info(folio, db)

async def get_procedure_info_type(folio: str, db: AsyncSession) -> ProcedureTypeInfoSchema:
    return await RequirementsQueriesService.get_procedure_info_type(folio, db)

async def get_procedure_info_renewal(folio: str, db: AsyncSession) -> ProcedureRenewalInfoSchema:
    return await RequirementsQueriesService.get_procedure_info_renewal(folio, db)

async def get_requirements_pdf(folio: str, requirement_id: int, db: AsyncSession) -> RequirementsPdfSchema:
    return await RequirementsQueriesService.get_requirements_pdf(folio, requirement_id, db)

async def submit_requirements_query(data: RequirementsQueryCreateSchema, db: AsyncSession) -> RequirementsQueryOutSchema:
    return await RequirementsQueriesService.submit_requirements_query(data, db)

async def get_folio_requirements_pdf(folio: str, db: AsyncSession) -> RequirementsPdfSchema:
    """Wrapper function for get_folio_requirements_pdf"""
    return await RequirementsQueriesService.get_folio_requirements_pdf(folio, db)
