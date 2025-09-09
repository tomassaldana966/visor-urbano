from logging.config import fileConfig
import geoalchemy2 # type: ignore  # noqa: F401
import os
import sys
import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy import engine_from_config, create_engine  # noqa: F401
from sqlalchemy import pool  # noqa: F401
from config.settings import Base
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.models import (
    auth_token,
    national_id,
    technical_sheets,
    field,
    urban_development_zonings_standard,
    business_line_configuration,
    economic_activity_sector,
    auth_permission,
    base_neighborhood,
    user,
    business_license,
    sub_role,
    public_space_mapping,
    recover_password,
    municipality,
    business_sector_certificates,
    answer,
    business_sector_impacts,
    land_parcel_mapping,
    requirements_query,
    building_footprints,
    base_administrative_division,
    business_license_histories,
    auth_group,    
    issue_resolution,
    municipality_signature,
    economic_units_directory,
    procedure_registrations,
    base_map_layer,
    auth_user_user_permissions,
    business_logs,
    economic_activity_base,
    answers_json,
    business_sectors,
    base_locality,
    user_tax_id,
    renewal_files,
    business_sector_configurations,
    renewal,
    user_roles,
    auth_group_permissions,
    permit_renewals,
    requirements,
    economic_support,
    dependency_resolutions,
    business_signatures,
    business_line_log,
    business_line,
    water_body_footprints,
    dependency_revision,
    inactive_businesses,
    base_municipality,
    reviewers_chat,
    notifications,
    dependency_reviews,
    zoning_impact_level,
    auth_user_groups,
    procedures,
    blog,
    urban_development_zonings,
    zoning_control_regulations,
    renewal_file_history,
    provisional_openings,
    municipality_map_layer_base,
    block_footprints,
    technical_sheet_downloads,
    user_roles_assignments,
)  # noqa: F401


print("Registered models:")
for name, obj in inspect.getmembers(sys.modules["app.models"]):
    if inspect.isclass(obj) and isinstance(obj, DeclarativeMeta):
        print(f" - {name}")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def include_object(_object, _name, type_, _reflected, _compare_to):         
    EXCLUDE_TABLES = [
        'spatial_ref_sys',
        'geography_columns',
        'geometry_columns',    
        'addr',
        'bg',
        'county',
        'county_lookup',
        'countysub_lookup',
        'cousub',
        'direction_lookup',
        'edges',
        'faces',
        'featnames',
        'geocode_settings',
        'layer',
        'pagc_gaz',
        'pagc_lex',
        'pagc_rules',
        'place',
        'place_lookup',
        'secondary_unit_lookup',
        'state',
        'state_lookup',
        'street_type_lookup',
        'tabblock',
        'tabblock20',
        'topology',
        'tract',
        'us_gaz',
        'us_lex',
        'us_rules',
        'zip_lookup',
        'zip_lookup_all',
        'zip_state',
        'zip_state_loc',        
        'loader_lookuptables',  
        'loader_platform',
        'loader_variables',
        'tiger',
        'tiger_data',
        'zcta5',
        'postgis_tiger_geocoder',
        'addrfeat',
        'geocode_settings_default',
        'geocode_settings_default_legacy',   
        'zip_lookup_base',     
    ]
    
    if type_ == "table" and _name in EXCLUDE_TABLES:
        return False
    return True


def process_revision_directives(_context, _revision, directives):
    if directives and directives[0].upgrade_ops.is_empty():
        directives[:] = []
        return
    
    # Always add geoalchemy2 import
    if directives and hasattr(directives[0], 'imports'):
        directives[0].imports.add("import geoalchemy2")

def get_database_url():
    db_connection = os.environ.get("DATABASE_CONNECTION", "postgresql")
    db_host = os.environ.get("DATABASE_HOST", "localhost")
    db_port = os.environ.get("DATABASE_PORT", "5432")
    db_name = os.environ.get("DATABASE_NAME", "visorurbano_prod")
    db_user = os.environ.get("DATABASE_USERNAME", "visorurbano")
    db_pass = os.environ.get("DATABASE_PASSWORD", "visorurbano123456")
    
    return f"{db_connection}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        process_revision_directives=process_revision_directives
    )

    with context.begin_transaction():
        try:
            context.run_migrations()
        except ProgrammingError as e:
            if "already exists" in str(e):
                pass  
            else:
                raise

def run_migrations_online() -> None:
    # Use environment variables directly
    url = get_database_url()
    connectable = create_engine(url)
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
            # Add this to make migrations more resilient
            render_as_batch=True
        )

        with context.begin_transaction():
            try:
                context.run_migrations()
            except (ProgrammingError, IntegrityError) as e:
                # Handle errors for objects that already exist (e.g. DuplicateTable or index already exists)
                if 'already exists' in str(e) or 'DuplicateTable' in str(e):
                    print(f"Warning: Some objects already exist. Continuing anyway: {e}")
                    pass
                else:
                    raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
