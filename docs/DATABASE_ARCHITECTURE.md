# Visor Urbano Database Architecture Documentation

## Overview

The Visor Urbano database architecture is designed to support a comprehensive urban planning and business licensing system municipalities. The system manages user authentication, business procedures, licensing workflows, geographical data, and administrative processes.

## Database Technology Stack

- **Database Engine**: PostgreSQL with PostGIS extension
- **ORM**: SQLAlchemy (Async/Sync)
- **Connection Pool**: AsyncPG for async operations
- **Migrations**: Alembic
- **Geospatial Data**: GeoAlchemy2 with PostGIS
- **Coordinate System**: EPSG:32613 (WGS 84 / UTM Zone 13N) and EPSG:4326 (WGS 84)

## Core System Architecture

### 1. Multi-tenancy Design

The system is designed with municipality-based multi-tenancy where each municipality operates as a separate tenant with its own:

- Users and roles
- Business procedures
- Licensing configurations
- Map layers and geospatial data
- Departments and workflows

### 2. Module Organization

The database is organized into the following functional modules:

#### 2.1 Authentication & Authorization Module

- User management with role-based access control
- JWT token-based authentication
- Django-compatible authentication fields
- Municipality-specific user isolation

#### 2.2 Business Licensing Module

- Business license management
- License histories and renewals
- Business types and sectors
- Provisional openings
- Payment tracking

#### 2.3 Procedure Management Module

- Procedure registration and tracking
- Multi-step workflow management
- Document management
- Review processes

#### 2.4 Geospatial Data Module

- Map layer management
- Geospatial procedure registration
- Zoning and urban development data
- Building and land parcel footprints

#### 2.5 Administrative Module

- Department management
- Technical sheets
- Notifications
- Blog and content management

---

## Detailed Entity Relationship Documentation

### Core Entities

#### 1. Users and Authentication

##### UserModel (users)

**Primary Entity**: Central user management table

| Column               | Type            | Description                                    |
| -------------------- | --------------- | ---------------------------------------------- |
| id                   | BigInteger (PK) | Primary key                                    |
| name                 | String(50)      | First name (Spanish: nombre)                   |
| paternal_last_name   | String(50)      | Father's last name (Spanish: apellido_paterno) |
| maternal_last_name   | String(50)      | Mother's last name (Spanish: apellido_materno) |
| user_tax_id          | String(50)      | Tax identification number (RFC)                |
| national_id          | String(50)      | National identification (CURP)                 |
| cellphone            | String(50)      | Mobile phone number                            |
| email                | String(100)     | Email address                                  |
| password             | String(100)     | Encrypted password                             |
| api_token            | String(100)     | API access token                               |
| api_token_expiration | DateTime        | Token expiration date                          |
| subrole_id           | Integer (FK)    | Reference to sub_roles.id                      |
| municipality_id      | Integer (FK)    | Reference to municipalities.id                 |
| role_id              | BigInteger (FK) | Reference to user_roles.id                     |
| username             | String(150)     | Django-compatible username                     |
| is_active            | Boolean         | Active status                                  |
| is_staff             | Boolean         | Staff privileges                               |
| is_superuser         | Boolean         | Superuser privileges                           |
| created_at           | DateTime        | Creation timestamp                             |
| updated_at           | DateTime        | Last update timestamp                          |
| deleted_at           | DateTime        | Soft deletion timestamp                        |
| last_login           | DateTime        | Last login timestamp                           |
| date_joined          | DateTime        | Registration date                              |

**Relationships**:

- `Municipality` (many-to-one): User belongs to a municipality
- `UserRoleModel` (many-to-one): User has a role
- `SubRoleModel` (many-to-one): User has a sub-role
- `ClientTaxID` (one-to-one): Tax ID details
- `UserNationalID` (one-to-one): National ID details
- `Answer` (one-to-many): User answers to requirements

##### UserRoleModel (user_roles)

**Role Definition**: Defines user roles within municipalities

| Column          | Type            | Description                    |
| --------------- | --------------- | ------------------------------ |
| id              | BigInteger (PK) | Primary key                    |
| name            | String(20)      | Role name                      |
| description     | String(200)     | Role description               |
| municipality_id | Integer (FK)    | Reference to municipalities.id |
| deleted_at      | DateTime        | Soft deletion timestamp        |
| created_at      | DateTime        | Creation timestamp             |
| updated_at      | DateTime        | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Role belongs to a municipality
- `UserModel` (one-to-many): Role assigned to users
- `UserRoleAssignment` (one-to-many): Role assignment tracking
- `DepartmentRole` (one-to-many): Department assignments

##### SubRoleModel (sub_roles)

**Sub-role Definition**: Defines specialized roles within user roles

| Column          | Type         | Description                    |
| --------------- | ------------ | ------------------------------ |
| id              | Integer (PK) | Primary key                    |
| name            | String(100)  | Sub-role name                  |
| description     | String(200)  | Sub-role description           |
| municipality_id | Integer (FK) | Reference to municipalities.id |
| created_at      | DateTime     | Creation timestamp             |
| updated_at      | DateTime     | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Sub-role belongs to a municipality
- `UserModel` (one-to-many): Sub-role assigned to users

---

#### 2. Municipality Management

##### Municipality (municipalities)

**Central Tenant Entity**: Represents each municipality in the system

| Column                         | Type            | Description                      |
| ------------------------------ | --------------- | -------------------------------- |
| id                             | BigInteger (PK) | Primary key                      |
| name                           | String(250)     | Municipality name                |
| image                          | String(250)     | Municipality logo/image          |
| director                       | String(250)     | Director name                    |
| director_signature             | String(250)     | Director's signature file        |
| process_sheet                  | Integer         | Process sheet identifier         |
| solving_days                   | Integer         | Standard resolution days         |
| issue_license                  | Integer         | License issuance flag            |
| address                        | String(255)     | Municipality address             |
| phone                          | String(255)     | Contact phone                    |
| email                          | String(255)     | Contact email                    |
| website                        | String(255)     | Municipality website             |
| responsible_area               | String(250)     | Responsible area name            |
| allow_online_procedures        | Boolean         | Online procedures enabled        |
| allow_window_reviewer_licenses | Boolean         | Window reviewer licenses enabled |
| low_impact_license_cost        | String(255)     | Low impact license cost          |
| license_additional_text        | Text            | Additional license text          |
| theme_color                    | String(7)       | Theme color (hex)                |
| created_at                     | DateTime        | Creation timestamp               |
| updated_at                     | DateTime        | Last update timestamp            |
| deleted_at                     | DateTime        | Soft deletion timestamp          |
| window_license_generation      | Integer         | Window license generation flag   |
| license_restrictions           | Text            | License restrictions             |
| license_price                  | String(255)     | License price                    |
| initial_folio                  | Integer         | Initial folio number             |
| has_zoning                     | Boolean         | Zoning information available     |

**Relationships**:

- `UserModel` (one-to-many): Municipality users
- `RequirementsQuery` (one-to-many): Municipality requirements
- `UserRoleModel` (one-to-many): Municipality roles
- `SubRoleModel` (one-to-many): Municipality sub-roles
- `TechnicalSheet` (one-to-many): Municipality technical sheets
- `BusinessLicense` (one-to-many): Municipality business licenses
- `BusinessLicenseHistory` (one-to-many): License histories
- `ProvisionalOpening` (one-to-many): Provisional openings
- `ZoningControlRegulation` (one-to-many): Zoning regulations
- `ProcedureRegistration` (one-to-many): Procedure registrations
- `MapLayer` (many-to-many): Associated map layers
- `Department` (one-to-many): Municipality departments
- `Field` (one-to-many): Municipality fields
- `Requirement` (one-to-many): Municipality requirements

---

#### 3. Business Licensing System

##### BusinessLicense (business_licenses)

**Business License Entity**: Manages issued business licenses

| Column                       | Type            | Description                      |
| ---------------------------- | --------------- | -------------------------------- |
| id                           | BigInteger (PK) | Primary key                      |
| owner                        | String(200)     | Business owner name              |
| license_folio                | String(200)     | License folio number             |
| commercial_activity          | String(200)     | Commercial activity description  |
| industry_classification_code | String(200)     | Industry classification (SCIAN)  |
| authorized_area              | String(200)     | Authorized area in square meters |
| opening_time                 | String(200)     | Business opening time            |
| closing_time                 | String(200)     | Business closing time            |
| owner_last_name_p            | String(200)     | Owner's paternal last name       |
| owner_last_name_m            | String(200)     | Owner's maternal last name       |
| national_id                  | String(200)     | Owner's national ID              |
| owner_profile                | String(200)     | Owner profile                    |
| logo_image                   | Text            | Business logo image              |
| signature                    | Text            | Digital signature                |
| minimap_url                  | Text            | Minimap URL for location         |
| scanned_pdf                  | Text            | Scanned PDF document             |
| license_year                 | Integer         | License year                     |
| license_category             | Integer         | License category                 |
| generated_by_user_id         | Integer         | User who generated the license   |
| deleted_at                   | DateTime        | Soft deletion timestamp          |
| created_at                   | DateTime        | Creation timestamp               |
| updated_at                   | DateTime        | Last update timestamp            |
| payment_status               | Integer         | Payment status flag              |
| payment_user_id              | Integer         | User who processed payment       |
| deactivation_status          | Integer         | Deactivation status              |
| payment_date                 | DateTime        | Payment date                     |
| payment_receipt_file         | Text            | Payment receipt file             |
| deactivation_date            | DateTime        | Deactivation date                |
| secondary_folio              | String(200)     | Secondary folio number           |
| deactivation_reason          | Text            | Deactivation reason              |
| deactivated_by_user_id       | Integer         | User who deactivated             |
| signer_name_1                | String(255)     | First signer name                |
| department_1                 | String(255)     | First signer department          |
| signature_1                  | String(255)     | First signature                  |
| signer_name_2                | String(255)     | Second signer name               |
| department_2                 | String(255)     | Second signer department         |
| signature_2                  | String(255)     | Second signature                 |
| signer_name_3                | String(255)     | Third signer name                |
| department_3                 | String(255)     | Third signer department          |
| signature_3                  | String(255)     | Third signature                  |
| signer_name_4                | String(255)     | Fourth signer name               |
| department_4                 | String(255)     | Fourth signer department         |

**Relationships**:

- `Municipality` (many-to-one): License belongs to a municipality
- `BusinessLicenseHistory` (one-to-many): License change history
- `BusinessLicenseStatusLog` (one-to-many): Status change logs

##### BusinessLicenseHistory (business_license_histories)

**License History Tracking**: Tracks changes to business licenses

| Column              | Type            | Description                                      |
| ------------------- | --------------- | ------------------------------------------------ |
| id                  | BigInteger (PK) | Primary key                                      |
| business_license_id | Integer (FK)    | Reference to business_licenses.id                |
| municipality_id     | Integer (FK)    | Reference to municipalities.id                   |
| change_type         | String(50)      | Type of change (created, updated, renewed, etc.) |
| changed_by_user_id  | Integer         | User who made the change                         |
| change_date         | DateTime        | Date of change                                   |
| old_values          | JSON            | Previous values                                  |
| new_values          | JSON            | New values                                       |
| notes               | Text            | Additional notes                                 |
| created_at          | DateTime        | Creation timestamp                               |

**Relationships**:

- `BusinessLicense` (many-to-one): History belongs to a license
- `Municipality` (many-to-one): History belongs to a municipality

---

#### 4. Procedure Management System

##### Procedure (procedures)

**Procedure Entity**: Manages business procedures and applications

| Column                    | Type            | Description                         |
| ------------------------- | --------------- | ----------------------------------- |
| id                        | BigInteger (PK) | Primary key                         |
| folio                     | String(255)     | Procedure folio number              |
| current_step              | Integer         | Current step in workflow            |
| user_signature            | String(255)     | User signature file                 |
| user_id                   | Integer (FK)    | Reference to users.id               |
| window_user_id            | Integer (FK)    | Window user reference               |
| entry_role                | Integer         | Entry role identifier               |
| documents_submission_date | DateTime        | Document submission date            |
| procedure_start_date      | DateTime        | Procedure start date                |
| window_seen_date          | DateTime        | Window review date                  |
| license_delivered_date    | DateTime        | License delivery date               |
| has_signature             | Integer         | Signature status flag               |
| no_signature_date         | DateTime        | No signature date                   |
| official_applicant_name   | String(255)     | Official applicant name             |
| responsibility_letter     | String(255)     | Responsibility letter file          |
| sent_to_reviewers         | Integer         | Sent to reviewers flag              |
| sent_to_reviewers_date    | DateTime        | Sent to reviewers date              |
| license_pdf               | String(255)     | License PDF file                    |
| payment_order             | String(255)     | Payment order file                  |
| status                    | Integer         | Procedure status                    |
| step_one                  | Integer         | Step one completion flag            |
| step_two                  | Integer         | Step two completion flag            |
| step_three                | Integer         | Step three completion flag          |
| step_four                 | Integer         | Step four completion flag           |
| director_approval         | Integer         | Director approval flag              |
| created_at                | DateTime        | Creation timestamp                  |
| updated_at                | DateTime        | Last update timestamp               |
| window_license_generated  | Integer         | Window license generation flag      |
| procedure_type            | String(255)     | Type of procedure                   |
| license_status            | String(255)     | License status                      |
| reason                    | String(255)     | Reason for status                   |
| renewed_folio             | String(255)     | Renewed folio number                |
| requirements_query_id     | Integer (FK)    | Reference to requirements_querys.id |
| street                    | String(255)     | Street address                      |
| exterior_number           | String(100)     | Exterior number                     |
| interior_number           | String(100)     | Interior number                     |
| neighborhood              | String(255)     | Neighborhood                        |
| reference                 | String(500)     | Address reference                   |
| project_municipality_id   | Integer (FK)    | Project municipality                |

**Relationships**:

- `UserModel` (many-to-one): Procedure belongs to a user
- `UserModel` (many-to-one): Window user assignment
- `Municipality` (many-to-one): Project municipality
- `RequirementsQuery` (many-to-one): Associated requirements

##### ProcedureRegistration (procedure_registrations)

**Geospatial Procedure Registration**: Manages spatial data for procedures

| Column           | Type              | Description                     |
| ---------------- | ----------------- | ------------------------------- |
| id               | Integer (PK)      | Primary key                     |
| reference        | String(100)       | Reference identifier            |
| area             | Float             | Area in square meters           |
| business_sector  | String(150)       | Business sector                 |
| procedure_type   | String(30)        | Type of procedure               |
| procedure_origin | String(30)        | Origin of procedure             |
| historical_id    | Integer           | Historical reference ID         |
| bbox             | String(200)       | Bounding box coordinates        |
| geom             | Geometry(POLYGON) | Spatial geometry (UTM Zone 13N) |
| municipality_id  | Integer (FK)      | Reference to municipalities.id  |

**Relationships**:

- `Municipality` (many-to-one): Registration belongs to a municipality

---

#### 5. Requirements and Fields System

##### Field (fields)

**Form Field Definition**: Defines form fields for procedures

| Column               | Type            | Description                           |
| -------------------- | --------------- | ------------------------------------- |
| id                   | BigInteger (PK) | Primary key                           |
| name                 | String(100)     | Field name                            |
| field_type           | String(100)     | Field type (text, select, file, etc.) |
| description          | Text            | Field description                     |
| description_rec      | Text            | Recommended description               |
| rationale            | String(255)     | Field rationale                       |
| options              | String(255)     | Field options (for select fields)     |
| options_description  | String(255)     | Options description                   |
| step                 | Integer         | Workflow step                         |
| sequence             | Integer         | Field sequence                        |
| required             | Integer         | Required flag                         |
| visible_condition    | String(255)     | Visibility condition                  |
| affected_field       | String(100)     | Affected field                        |
| procedure_type       | String(100)     | Applicable procedure type             |
| dependency_condition | String(255)     | Dependency condition                  |
| trade_condition      | String(255)     | Trade condition                       |
| status               | Integer         | Field status                          |
| municipality_id      | Integer (FK)    | Reference to municipalities.id        |
| editable             | Integer         | Editable flag                         |
| static_field         | Integer         | Static field flag                     |
| created_at           | DateTime        | Creation timestamp                    |
| updated_at           | DateTime        | Last update timestamp                 |
| deleted_at           | DateTime        | Soft deletion timestamp               |
| required_official    | Integer         | Required for official flag            |

**Relationships**:

- `Municipality` (many-to-one): Field belongs to a municipality
- `Requirement` (one-to-many): Field requirements
- `RequirementDepartmentAssignment` (one-to-many): Department assignments

##### Requirement (requirements)

**Requirement Definition**: Links fields to municipalities

| Column           | Type            | Description                    |
| ---------------- | --------------- | ------------------------------ |
| id               | BigInteger (PK) | Primary key                    |
| municipality_id  | Integer (FK)    | Reference to municipalities.id |
| field_id         | Integer (FK)    | Reference to fields.id         |
| requirement_code | String(300)     | Requirement code               |
| created_at       | DateTime        | Creation timestamp             |
| updated_at       | DateTime        | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Requirement belongs to a municipality
- `Field` (many-to-one): Requirement references a field

##### RequirementsQuery (requirements_querys)

**Requirements Query**: Groups requirements for procedures

| Column          | Type         | Description                    |
| --------------- | ------------ | ------------------------------ |
| id              | Integer (PK) | Primary key                    |
| name            | String(100)  | Query name                     |
| description     | String(250)  | Query description              |
| municipality_id | Integer (FK) | Reference to municipalities.id |
| created_at      | DateTime     | Creation timestamp             |
| updated_at      | DateTime     | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Query belongs to a municipality
- `Procedure` (one-to-many): Procedures using this query

##### Answer (answers)

**User Answers**: Stores user answers to requirement fields

| Column      | Type            | Description            |
| ----------- | --------------- | ---------------------- |
| id          | BigInteger (PK) | Primary key            |
| user_id     | Integer (FK)    | Reference to users.id  |
| field_id    | Integer (FK)    | Reference to fields.id |
| answer_text | Text            | Text answer            |
| answer_json | JSON            | JSON answer data       |
| created_at  | DateTime        | Creation timestamp     |
| updated_at  | DateTime        | Last update timestamp  |

**Relationships**:

- `UserModel` (many-to-one): Answer belongs to a user
- `Field` (many-to-one): Answer references a field

---

#### 6. Department and Review System

##### Department (departments)

**Department Entity**: Manages municipal departments

| Column                    | Type         | Description                    |
| ------------------------- | ------------ | ------------------------------ |
| id                        | Integer (PK) | Primary key                    |
| name                      | String(100)  | Department name                |
| description               | Text         | Department description         |
| code                      | String(20)   | Unique department code         |
| municipality_id           | Integer (FK) | Reference to municipalities.id |
| is_active                 | Boolean      | Active status                  |
| can_approve_procedures    | Boolean      | Approval permission            |
| can_reject_procedures     | Boolean      | Rejection permission           |
| requires_all_requirements | Boolean      | All requirements needed        |
| created_at                | DateTime     | Creation timestamp             |
| updated_at                | DateTime     | Last update timestamp          |
| deleted_at                | DateTime     | Soft deletion timestamp        |

**Relationships**:

- `Municipality` (many-to-one): Department belongs to a municipality
- `DepartmentRole` (one-to-many): Department roles
- `DepartmentUserAssignment` (one-to-many): User assignments
- `DependencyReview` (one-to-many): Department reviews
- `RequirementDepartmentAssignment` (one-to-many): Requirement assignments

##### DependencyReview (dependency_reviews)

**Review Process**: Manages department reviews of procedures

| Column           | Type         | Description                 |
| ---------------- | ------------ | --------------------------- |
| id               | Integer (PK) | Primary key                 |
| procedure_id     | Integer (FK) | Reference to procedures.id  |
| department_id    | Integer (FK) | Reference to departments.id |
| reviewer_user_id | Integer (FK) | Reference to users.id       |
| review_status    | String(50)   | Review status               |
| review_date      | DateTime     | Review date                 |
| comments         | Text         | Review comments             |
| created_at       | DateTime     | Creation timestamp          |
| updated_at       | DateTime     | Last update timestamp       |

**Relationships**:

- `Procedure` (many-to-one): Review belongs to a procedure
- `Department` (many-to-one): Review by department
- `UserModel` (many-to-one): Review by user

---

#### 7. Geospatial and Mapping System

##### MapLayer (map_layers)

**Map Layer Definition**: Defines map layers for visualization

| Column      | Type         | Description                     |
| ----------- | ------------ | ------------------------------- |
| id          | Integer (PK) | Primary key                     |
| value       | String(100)  | Layer value                     |
| label       | String(180)  | Layer label                     |
| type        | String(20)   | Layer type (WMS, WFS, etc.)     |
| url         | String(255)  | Layer URL                       |
| layers      | String(60)   | Layer names                     |
| visible     | Boolean      | Visible by default              |
| active      | Boolean      | Active status                   |
| attribution | String(100)  | Attribution text                |
| opacity     | Decimal(3,2) | Layer opacity                   |
| server_type | String(60)   | Server type                     |
| projection  | String(20)   | Projection (default: EPSG:4326) |
| version     | String(10)   | WMS version                     |
| format      | String(60)   | Image format                    |
| order       | Integer      | Layer order                     |
| editable    | Boolean      | Editable flag                   |
| type_geom   | String(20)   | Geometry type                   |
| cql_filter  | String(255)  | CQL filter                      |

**Relationships**:

- `Municipality` (many-to-many): Associated municipalities

##### Building/Land Footprints

**Geospatial Footprints**: Various geospatial footprint entities

- `BuildingFootprint` (building_footprints): Building footprints
- `LandParcelMapping` (land_parcel_mapping): Land parcel mappings
- `WaterBodyFootprint` (water_body_footprints): Water body footprints
- `BlockFootprint` (block_footprints): Block footprints

All footprint entities contain:

- Geometry columns with spatial data
- Municipality references
- Metadata fields

---

#### 8. Business Classification System

##### BusinessSector (business_sectors)

**Business Sector Classification**: Defines business sectors

| Column      | Type         | Description           |
| ----------- | ------------ | --------------------- |
| id          | Integer (PK) | Primary key           |
| name        | String(100)  | Sector name           |
| code        | String(20)   | Sector code           |
| description | Text         | Sector description    |
| created_at  | DateTime     | Creation timestamp    |
| updated_at  | DateTime     | Last update timestamp |

**Relationships**:

- `BusinessSectorImpact` (one-to-many): Sector impacts
- `BusinessSectorCertificate` (one-to-many): Required certificates
- `BusinessSectorConfiguration` (one-to-many): Sector configurations

##### BusinessType (business_types)

**Business Type Definition**: Defines business types

| Column      | Type         | Description               |
| ----------- | ------------ | ------------------------- |
| id          | Integer (PK) | Primary key               |
| name        | String(100)  | Business type name        |
| code        | String(20)   | Business type code        |
| description | Text         | Business type description |
| created_at  | DateTime     | Creation timestamp        |
| updated_at  | DateTime     | Last update timestamp     |

**Relationships**:

- `BusinessTypeConfig` (one-to-many): Type configurations

---

#### 9. Zoning and Urban Development

##### ZoningControlRegulation (zoning_control_regulations)

**Zoning Regulations**: Manages zoning control regulations

| Column          | Type         | Description                    |
| --------------- | ------------ | ------------------------------ |
| id              | Integer (PK) | Primary key                    |
| municipality_id | Integer (FK) | Reference to municipalities.id |
| zone_code       | String(50)   | Zone code                      |
| regulation_text | Text         | Regulation text                |
| created_at      | DateTime     | Creation timestamp             |
| updated_at      | DateTime     | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Regulation belongs to a municipality

##### UrbanDevelopmentZoning (urban_development_zonings)

**Urban Development Zoning**: Manages urban development zones

| Column      | Type         | Description           |
| ----------- | ------------ | --------------------- |
| id          | Integer (PK) | Primary key           |
| zone_name   | String(100)  | Zone name             |
| zone_code   | String(50)   | Zone code             |
| description | Text         | Zone description      |
| regulations | Text         | Zone regulations      |
| created_at  | DateTime     | Creation timestamp    |
| updated_at  | DateTime     | Last update timestamp |

---

#### 10. Content Management

##### Blog (blogs)

**Blog Content**: Manages blog posts and content

| Column          | Type         | Description                    |
| --------------- | ------------ | ------------------------------ |
| id              | Integer (PK) | Primary key                    |
| title           | String(200)  | Blog title                     |
| content         | Text         | Blog content                   |
| slug            | String(200)  | URL slug                       |
| municipality_id | Integer (FK) | Reference to municipalities.id |
| created_at      | DateTime     | Creation timestamp             |
| updated_at      | DateTime     | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Blog belongs to a municipality

##### TechnicalSheet (technical_sheets)

**Technical Documentation**: Manages technical sheets

| Column          | Type         | Description                    |
| --------------- | ------------ | ------------------------------ |
| id              | Integer (PK) | Primary key                    |
| name            | String(100)  | Sheet name                     |
| description     | Text         | Sheet description              |
| file_path       | String(255)  | File path                      |
| municipality_id | Integer (FK) | Reference to municipalities.id |
| created_at      | DateTime     | Creation timestamp             |
| updated_at      | DateTime     | Last update timestamp          |

**Relationships**:

- `Municipality` (many-to-one): Sheet belongs to a municipality
- `TechnicalSheetDownload` (one-to-many): Download tracking

---

## Database Relationships Summary

### Primary Entity Relationships

1. **Municipality** → Central hub connecting all entities
   - One-to-many: Users, Departments, Fields, Requirements, Procedures, Licenses
   - Many-to-many: MapLayers

2. **UserModel** → Core user entity
   - Many-to-one: Municipality, UserRole, SubRole
   - One-to-many: Procedures, Answers, Reviews

3. **Procedure** → Main business process entity
   - Many-to-one: User, Municipality, RequirementsQuery
   - One-to-many: DependencyReviews

4. **BusinessLicense** → License management
   - Many-to-one: Municipality
   - One-to-many: BusinessLicenseHistory, StatusLogs

5. **Department** → Administrative unit
   - Many-to-one: Municipality
   - One-to-many: DependencyReviews, UserAssignments

### Key Foreign Key Relationships

```sql
-- User to Municipality
users.municipality_id → municipalities.id

-- User to Role
users.role_id → user_roles.id

-- Procedure to User
procedures.user_id → users.id

-- Procedure to Municipality
procedures.project_municipality_id → municipalities.id

-- Business License to Municipality
business_licenses.municipality_id → municipalities.id

-- Department to Municipality
departments.municipality_id → municipalities.id

-- Field to Municipality
fields.municipality_id → municipalities.id

-- Requirement to Municipality and Field
requirements.municipality_id → municipalities.id
requirements.field_id → fields.id

-- Dependency Review connections
dependency_reviews.procedure_id → procedures.id
dependency_reviews.department_id → departments.id
dependency_reviews.reviewer_user_id → users.id
```

---

## Database Indexes and Performance

### Spatial Indexes

- PostGIS spatial indexes on all geometry columns
- UTM Zone 13N (EPSG:32613) for Mexican coordinate system
- WGS 84 (EPSG:4326) for global compatibility

### Performance Indexes

- Primary key indexes on all tables
- Foreign key indexes for relationship optimization
- Composite indexes for frequently queried combinations:
  - (municipality_id, status) on procedures
  - (municipality_id, is_active) on departments
  - (user_id, created_at) on answers

---

## Security and Access Control

### Row-Level Security

- Municipality-based data isolation
- User role-based access control
- Soft deletion for audit trails

### Authentication

- JWT token-based authentication
- API token management
- Password recovery system

### Data Protection

- Sensitive data encryption
- Audit logging for critical changes
- Soft deletion for data retention

---

## Migration Strategy

### Alembic Configuration

- Sequential migration versioning
- Both upgrade and downgrade paths
- Schema validation and constraints
- Data migration support

### Recent Migration Highlights

- Spanish to English column name standardization
- Department-based intelligent routing
- Enhanced business license tracking
- Improved spatial data management

---

## Backup and Recovery

### Database Backup Strategy

- Full database backups
- Incremental backups for large datasets
- Point-in-time recovery capability
- Geospatial data backup considerations

### Data Retention

- Soft deletion for business records
- Audit trail preservation
- Historical data archival
- Compliance with data retention policies

---

## Performance Optimization

### Query Optimization

- Proper indexing strategy
- Connection pooling
- Async query execution
- Spatial query optimization

### Caching Strategy

- Application-level caching
- Database query result caching
- Static content caching
- Geospatial data caching

---

## Monitoring and Maintenance

### Database Monitoring

- Performance metrics tracking
- Query execution analysis
- Connection pool monitoring
- Disk space management

### Maintenance Tasks

- Regular VACUUM and ANALYZE
- Index maintenance
- Statistics updates
- Backup verification

---

## Future Considerations

### Scalability

- Database sharding possibilities
- Read replica implementation
- Caching layer enhancement
- API rate limiting

### Feature Enhancements

- Advanced spatial analysis
- Real-time notifications
- Enhanced reporting
- Mobile application support

---

## Conclusion

The Visor Urbano database architecture provides a robust foundation for managing urban planning and business licensing operations across multiple municipalities. The design emphasizes data integrity, scalability, and maintainability while supporting complex business workflows and geospatial operations.

The multi-tenant architecture ensures proper data isolation while allowing for shared functionality across municipalities. The comprehensive audit trail and soft deletion patterns provide necessary data protection and compliance capabilities.

The integration of PostgreSQL with PostGIS enables powerful geospatial capabilities essential for urban planning applications, while the SQLAlchemy ORM provides flexibility and performance for application development.
