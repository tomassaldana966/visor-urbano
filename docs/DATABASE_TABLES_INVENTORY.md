# Database Tables Inventory

## 📊 Complete Database Tables Inventory for Visor Urbano

This document provides a comprehensive inventory of all database tables in the Visor Urbano system, organized by functional category. Each table includes its purpose, key relationships, and primary use cases.

---

## 📝 Table of Contents

1. [Core System Tables](#core-system-tables)
2. [User Management Tables](#user-management-tables)
3. [Municipality & Administration Tables](#municipality--administration-tables)
4. [Procedure Management Tables](#procedure-management-tables)
5. [Business License Management Tables](#business-license-management-tables)
6. [Business Classification Tables](#business-classification-tables)
7. [Department & Workflow Tables](#department--workflow-tables)
8. [Geospatial & Mapping Tables](#geospatial--mapping-tables)
9. [Content Management Tables](#content-management-tables)
10. [Configuration & Reference Tables](#configuration--reference-tables)
11. [Authentication & Authorization Tables](#authentication--authorization-tables)
12. [Audit & Logging Tables](#audit--logging-tables)
13. [Legacy & System Tables](#legacy--system-tables)

---

## Core System Tables

### 1. `municipalities`

**Purpose**: Central tenant table that represents each municipality using the system

- **Primary Use**: Multi-tenant data isolation and municipality-specific configuration
- **Key Fields**: name, director, theme_color, license_price, allow_online_procedures
- **Relationships**: Central hub connecting to 20+ other tables
- **Business Logic**: Controls system features and branding per municipality

### 2. `users`

**Purpose**: Main user authentication and profile management

- **Primary Use**: User authentication, profile management, and system access control
- **Key Fields**: name, email, password, municipality_id, role_id, national_id
- **Relationships**: Connected to municipality, roles, procedures, and business licenses
- **Business Logic**: Supports both citizens and municipal staff with different access levels

### 3. `user_roles`

**Purpose**: Role-based access control system

- **Primary Use**: Define user permissions and access levels within each municipality
- **Key Fields**: name, description, municipality_id
- **Relationships**: Links users to permissions and departments
- **Business Logic**: Enables granular permission control (citizen, staff, director, etc.)

---

## User Management Tables

### 4. `sub_roles`

**Purpose**: Additional role refinement within main user roles

- **Primary Use**: Provide more granular role definitions beyond main user roles
- **Key Fields**: name, description, municipality_id
- **Relationships**: Linked to users and municipalities
- **Business Logic**: Allows fine-tuned permission management

### 5. `user_roles_assignments`

**Purpose**: Many-to-many relationship between users and roles

- **Primary Use**: Manage complex role assignments and role transitions
- **Key Fields**: user_id, role_id, pending_role_id, assignment_date
- **Relationships**: Links users to current and pending roles
- **Business Logic**: Supports role change workflows and approvals

### 6. `user_tax_id`

**Purpose**: Store user tax identification numbers

- **Primary Use**: Business license applications and tax compliance
- **Key Fields**: user_id, tax_id_number, tax_id_type (RFC, TIN, etc.)
- **Relationships**: One-to-one with users
- **Business Logic**: Required for business-related procedures

### 7. `national_id`

**Purpose**: Store national identification numbers

- **Primary Use**: User identity verification and government compliance
- **Key Fields**: user_id, national_id_number, national_id_type (CURP, SSN, etc.)
- **Relationships**: One-to-one with users
- **Business Logic**: Required for identity verification in procedures

### 8. `password_recovery`

**Purpose**: Manage password reset tokens and recovery process

- **Primary Use**: Secure password reset functionality
- **Key Fields**: user_id, token, expires_at, used
- **Relationships**: Links to users
- **Business Logic**: Enables secure self-service password recovery

---

## Municipality & Administration Tables

### 9. `municipality_signatures`

**Purpose**: Store digital signatures for municipality officials

- **Primary Use**: Digital signing of business licenses and official documents
- **Key Fields**: municipality_id, signer_name, department, signature, order_index
- **Relationships**: Belongs to municipalities
- **Business Logic**: Enables multiple authorized signers per municipality

### 10. `technical_sheets`

**Purpose**: Store technical documentation and property information sheets

- **Primary Use**: Property analysis and technical documentation generation
- **Key Fields**: uuid, address, coordinates, image, municipality_id
- **Relationships**: Links to municipalities and downloads
- **Business Logic**: Provides technical property information for procedures

### 11. `technical_sheet_downloads`

**Purpose**: Track downloads of technical sheets

- **Primary Use**: Analytics and user tracking for technical documentation
- **Key Fields**: name, email, sector, municipality_id, address
- **Relationships**: Links to technical sheets and municipalities
- **Business Logic**: Provides usage analytics and user demographics

### 12. `blog`

**Purpose**: Content management for municipality news and announcements

- **Primary Use**: Public communication and news publishing
- **Key Fields**: title, slug, content, municipality_id, news_date
- **Relationships**: Belongs to municipalities
- **Business Logic**: Enables municipality-specific content management

---

## Procedure Management Tables

### 13. `procedures`

**Purpose**: Main table for all municipal procedures and applications

- **Primary Use**: Track application lifecycle from submission to completion
- **Key Fields**: folio, user_id, status, procedure_type, current_step
- **Relationships**: Central to the procedure workflow system
- **Business Logic**: Core business process management for all municipal services

### 14. `historical_procedures`

**Purpose**: Archive of completed or cancelled procedures

- **Primary Use**: Historical record keeping and analytics
- **Key Fields**: Same as procedures table with archival metadata
- **Relationships**: Mirrors procedure relationships
- **Business Logic**: Maintains audit trail and enables historical reporting

### 15. `procedure_registrations`

**Purpose**: Geospatial registration of procedures with location data

- **Primary Use**: Map-based procedure tracking and spatial analysis
- **Key Fields**: reference, area, geom (spatial), business_sector
- **Relationships**: Links to municipalities with spatial indexing
- **Business Logic**: Enables location-based procedure analysis and mapping

### 16. `requirements_querys`

**Purpose**: Define dynamic form requirements for different procedure types

- **Primary Use**: Configure what information is required for each procedure type
- **Key Fields**: name, description, municipality_id
- **Relationships**: Links to fields, answers, and procedures
- **Business Logic**: Enables municipality-specific procedure customization

### 17. `fields`

**Purpose**: Define individual form fields and their properties

- **Primary Use**: Create dynamic forms for procedure applications
- **Key Fields**: name, field_type, required, procedure_type, step
- **Relationships**: Part of requirements system, linked to answers
- **Business Logic**: Enables flexible form generation for different procedures

### 18. `requirements`

**Purpose**: Links fields to municipalities with specific requirements

- **Primary Use**: Municipality-specific field requirements configuration
- **Key Fields**: municipality_id, field_id, requirement_code
- **Relationships**: Links municipalities to required fields
- **Business Logic**: Allows different requirements per municipality

### 19. `answers`

**Purpose**: Store user responses to procedure form fields

- **Primary Use**: Capture application data from users
- **Key Fields**: procedure_id, user_id, field_id, value
- **Relationships**: Links procedures, users, and fields
- **Business Logic**: Stores dynamic form responses for procedure processing

---

## Business License Management Tables

### 20. `business_licenses`

**Purpose**: Issued business licenses with all license details

- **Primary Use**: Official business license records and management
- **Key Fields**: license_folio, owner, commercial_activity, opening_time
- **Relationships**: Links to municipalities, users, and business types
- **Business Logic**: Central business license lifecycle management

### 21. `business_license_histories`

**Purpose**: Track all changes made to business licenses

- **Primary Use**: Audit trail for business license modifications
- **Key Fields**: license_id, change_type, old_values, new_values
- **Relationships**: Links to business licenses and users
- **Business Logic**: Maintains complete change history for compliance

### 22. `business_license_status_logs`

**Purpose**: Track status changes in business license lifecycle

- **Primary Use**: Monitor license status transitions and approval workflow
- **Key Fields**: license_id, previous_status, new_status, reason
- **Relationships**: Links to business licenses and users
- **Business Logic**: Enables status-based workflow management

### 23. `provisional_openings`

**Purpose**: Temporary business operation permits

- **Primary Use**: Allow business operation while full license is processed
- **Key Fields**: folio, business_name, opening_date, expiration_date
- **Relationships**: Links to municipalities
- **Business Logic**: Provides interim operating authority

### 24. `inactive_businesses`

**Purpose**: Track businesses that have ceased operations

- **Primary Use**: Monitor business closure and maintain historical records
- **Key Fields**: business_line_id, municipality_id
- **Relationships**: Links to business lines and municipalities
- **Business Logic**: Enables business lifecycle tracking

---

## Business Classification Tables

### 25. `business_types`

**Purpose**: Classification system for different types of businesses

- **Primary Use**: Categorize businesses for regulatory and reporting purposes
- **Key Fields**: name, description, code (SCIAN), related_words
- **Relationships**: Links to configurations and procedures
- **Business Logic**: Enables business type-specific processing rules

### 26. `business_type_configurations`

**Purpose**: Municipality-specific configuration for business types

- **Primary Use**: Enable/disable business types and set requirements per municipality
- **Key Fields**: business_type_id, municipality_id, is_disabled, impact_level
- **Relationships**: Links business types to municipalities
- **Business Logic**: Allows municipality-specific business type management

### 27. `business_sectors`

**Purpose**: Industry classification using SCIAN codes

- **Primary Use**: Standardized business classification for regulatory compliance
- **Key Fields**: code, SCIAN, related_words
- **Relationships**: Links to impacts, certificates, and configurations
- **Business Logic**: Provides standardized industry classification

### 28. `business_sector_impacts`

**Purpose**: Define environmental/social impact levels per sector

- **Primary Use**: Risk assessment and regulatory requirement determination
- **Key Fields**: business_sector_id, impact, municipality_id
- **Relationships**: Links business sectors to municipalities
- **Business Logic**: Enables impact-based regulatory requirements

### 29. `business_sector_certificates`

**Purpose**: Required certificates for specific business sectors

- **Primary Use**: Define mandatory certifications per business type
- **Key Fields**: business_sector_id, municipality_id
- **Relationships**: Links business sectors to municipalities
- **Business Logic**: Enforces sector-specific certification requirements

### 30. `business_sector_configurations`

**Purpose**: Configuration flags for business sector processing

- **Primary Use**: Control which business sector features are enabled
- **Key Fields**: business_sector_id, municipality_id, various flags
- **Relationships**: Links business sectors to municipalities
- **Business Logic**: Enables municipality-specific sector configurations

### 31. `business_lines`

**Purpose**: Broad business activity categories

- **Primary Use**: High-level business classification for reporting
- **Key Fields**: name
- **Relationships**: Links to inactive businesses
- **Business Logic**: Provides general business activity classification

### 32. `business_line_configurations`

**Purpose**: Configuration settings for business line processing

- **Primary Use**: Control business line specific behaviors
- **Key Fields**: business_line_id, municipality_id, configuration flags
- **Relationships**: Links business lines to municipalities
- **Business Logic**: Enables customized business line processing

### 33. `business_line_logs`

**Purpose**: Activity logs for business line operations

- **Primary Use**: Track business line related activities and changes
- **Key Fields**: business_line_id, action, user_id, timestamp
- **Relationships**: Links to business lines and users
- **Business Logic**: Provides audit trail for business line operations

---

## Department & Workflow Tables

### 34. `departments`

**Purpose**: Organizational units within municipalities for procedure review

- **Primary Use**: Structure municipal organization and assign review responsibilities
- **Key Fields**: name, code, municipality_id, can_approve_procedures
- **Relationships**: Central to workflow and user assignment
- **Business Logic**: Enables departmental procedure review workflows

### 35. `department_roles`

**Purpose**: Link departments to user roles

- **Primary Use**: Define which roles can work in which departments
- **Key Fields**: department_id, role_id, municipality_id
- **Relationships**: Links departments to user roles
- **Business Logic**: Controls departmental access by role

### 36. `department_user_assignments`

**Purpose**: Assign specific users to departments

- **Primary Use**: Manage user assignments to departmental work
- **Key Fields**: department_id, user_id, assigned_at, is_active
- **Relationships**: Links departments to specific users
- **Business Logic**: Enables dynamic user-department assignments

### 37. `requirement_department_assignments`

**Purpose**: Assign specific requirements to departments for review

- **Primary Use**: Define which departments review which requirements
- **Key Fields**: field_id, department_id, is_required, can_approve
- **Relationships**: Links requirements to departments
- **Business Logic**: Routes specific requirements to appropriate departments

### 38. `dependency_reviews`

**Purpose**: Track departmental reviews of procedures

- **Primary Use**: Manage multi-department procedure review process
- **Key Fields**: procedure_id, department_id, reviewer_id, review_status
- **Relationships**: Links procedures, departments, and reviewers
- **Business Logic**: Core workflow for departmental procedure review

### 39. `dependency_resolutions`

**Purpose**: Record resolution of dependency review issues

- **Primary Use**: Track how review issues are resolved
- **Key Fields**: dependency_review_id, resolution_status, resolved_by
- **Relationships**: Links to dependency reviews and users
- **Business Logic**: Enables issue resolution tracking

### 40. `procedure_department_flows`

**Purpose**: Define the sequence of departments for procedure review

- **Primary Use**: Configure department review order for different procedures
- **Key Fields**: procedure_type, department_id, sequence_order
- **Relationships**: Links procedure types to departments
- **Business Logic**: Enables configurable multi-department workflows

### 41. `dependency_review_workflows`

**Purpose**: Workflow configuration for dependency reviews

- **Primary Use**: Define review process rules and sequences
- **Key Fields**: department_id, workflow_step, required_action
- **Relationships**: Links departments to workflow steps
- **Business Logic**: Configures complex review workflows

### 42. `prevention_requests`

**Purpose**: Handle prevention requests in procedure workflows

- **Primary Use**: Manage prevention and objection processes
- **Key Fields**: procedure_id, request_type, status, assigned_to
- **Relationships**: Links to procedures and users
- **Business Logic**: Handles prevention workflow in procedures

### 43. `director_approvals`

**Purpose**: Track director-level approvals for procedures

- **Primary Use**: Manage final approval by municipal directors
- **Key Fields**: procedure_id, director_id, approval_status, notes
- **Relationships**: Links procedures to director users
- **Business Logic**: Enables director-level procedure approval

---

## Geospatial & Mapping Tables

### 44. `map_layers`

**Purpose**: Define map layers available in the system

- **Primary Use**: Configure interactive map layers and data sources
- **Key Fields**: label, type, url, layers, visible, projection
- **Relationships**: Many-to-many with municipalities
- **Business Logic**: Enables municipality-specific map configurations

### 45. `maplayer_municipality`

**Purpose**: Junction table linking map layers to municipalities

- **Primary Use**: Control which map layers are available per municipality
- **Key Fields**: maplayer_id, municipality_id
- **Relationships**: Links map layers to municipalities
- **Business Logic**: Enables municipality-specific map layer visibility

### 46. `base_map_layer`

**Purpose**: Base map layer definitions for the mapping system

- **Primary Use**: Define fundamental map layers (streets, satellite, etc.)
- **Key Fields**: name, url, type, attribution, opacity
- **Relationships**: Links to municipality associations
- **Business Logic**: Provides base mapping infrastructure

### 47. `municipality_map_layer_base`

**Purpose**: Associate municipalities with base map layers

- **Primary Use**: Configure which base layers are available per municipality
- **Key Fields**: map_layer_id, municipality_id
- **Relationships**: Links municipalities to base map layers
- **Business Logic**: Enables municipality-specific base map configuration

### 48. `building_footprints`

**Purpose**: Building geometry and metadata for mapping

- **Primary Use**: Display building information on maps and spatial analysis
- **Key Fields**: building_code, area_m2, geom, neighborhood_id
- **Relationships**: Links to neighborhoods, localities, and municipalities
- **Business Logic**: Enables building-level spatial analysis

### 49. `land_parcel_mapping`

**Purpose**: Property boundaries and parcel information

- **Primary Use**: Property mapping and land use analysis
- **Key Fields**: parcel_id, owner_name, area, geom
- **Relationships**: Links to neighborhoods and municipalities
- **Business Logic**: Provides property boundary data for procedures

### 50. `block_footprints`

**Purpose**: City block geometry and information

- **Primary Use**: Urban planning and block-level analysis
- **Key Fields**: block_code, area_m2, geom
- **Relationships**: Geospatial relationships with other mapping entities
- **Business Logic**: Enables block-level urban planning analysis

### 51. `water_body_footprints`

**Purpose**: Water body geometry for environmental analysis

- **Primary Use**: Environmental impact assessment and spatial planning
- **Key Fields**: area_m2, geom
- **Relationships**: Spatial relationships with other geographic features
- **Business Logic**: Supports environmental compliance checking

### 52. `public_space_mapping`

**Purpose**: Public spaces and recreational areas

- **Primary Use**: Public space management and urban planning
- **Key Fields**: name, space_type, geom
- **Relationships**: Spatial relationships with municipalities
- **Business Logic**: Enables public space analysis and planning

### 53. `base_neighborhood`

**Purpose**: Neighborhood boundaries and basic information

- **Primary Use**: Geographic organization and address lookup
- **Key Fields**: name, postal_code, geom, municipality_id
- **Relationships**: Contains buildings and parcels
- **Business Logic**: Provides neighborhood-level geographic organization

### 54. `base_locality`

**Purpose**: Locality/town boundaries within municipalities

- **Primary Use**: Sub-municipal geographic organization
- **Key Fields**: name, locality_code, geom, municipality_id
- **Relationships**: Contains neighborhoods and buildings
- **Business Logic**: Enables locality-level administration

### 55. `base_municipality`

**Purpose**: Municipality boundary definitions

- **Primary Use**: Define official municipal boundaries
- **Key Fields**: name, entity_code, municipality_code, geom
- **Relationships**: Top-level geographic container
- **Business Logic**: Provides official municipal boundary data

### 56. `base_administrative_division`

**Purpose**: Administrative divisions and regions

- **Primary Use**: Higher-level administrative organization
- **Key Fields**: name, code, division_type, geom
- **Relationships**: Contains municipalities
- **Business Logic**: Enables state/regional level organization

---

## Content Management Tables

### 57. `notifications`

**Purpose**: System notifications and alerts for users

- **Primary Use**: User communication and system alerts
- **Key Fields**: user_id, title, message, notification_type, read_status
- **Relationships**: Links to users
- **Business Logic**: Enables user notification system

### 58. `reviewers_chat`

**Purpose**: Communication between reviewers and applicants

- **Primary Use**: Facilitate communication during procedure review
- **Key Fields**: procedure_id, reviewer_id, comment, attached_file
- **Relationships**: Links procedures to users
- **Business Logic**: Enables reviewer-applicant communication

### 59. `business_signatures`

**Purpose**: Digital signatures for business-related documents

- **Primary Use**: Digital signing of business licenses and certificates
- **Key Fields**: signature_data, certificate_info, municipality_id
- **Relationships**: Links to municipalities and procedures
- **Business Logic**: Enables digital document signing

---

## Configuration & Reference Tables

### 60. `zoning_control_regulations`

**Purpose**: Zoning rules and regulations per municipality

- **Primary Use**: Define land use regulations and compliance rules
- **Key Fields**: municipality_id, zone_code, regulation_text
- **Relationships**: Links to municipalities
- **Business Logic**: Enforces zoning compliance in procedures

### 61. `urban_development_zonings`

**Purpose**: Urban development zoning classifications

- **Primary Use**: Define development zones and permitted uses
- **Key Fields**: district, sub_district, area_classification
- **Relationships**: Spatial relationships with procedures
- **Business Logic**: Enables zoning-based procedure validation

### 62. `urban_development_zonings_standard`

**Purpose**: Standardized urban development zoning definitions

- **Primary Use**: Provide standard zoning classifications
- **Key Fields**: district, area_classification, publication_date
- **Relationships**: Reference data for zoning
- **Business Logic**: Provides standardized zoning reference

### 63. `zoning_impact_level`

**Purpose**: Define impact levels for zoning analysis

- **Primary Use**: Assess development impact on urban zones
- **Key Fields**: level_name, level_code, description, priority
- **Relationships**: Used in zoning analysis
- **Business Logic**: Enables impact-based zoning decisions

### 64. `economic_activity_base`

**Purpose**: Base classification of economic activities

- **Primary Use**: Standardized economic activity classification
- **Key Fields**: name
- **Relationships**: Links to economic units directory
- **Business Logic**: Provides economic activity standardization

### 65. `economic_activity_sector`

**Purpose**: Economic sector classifications

- **Primary Use**: Sector-based economic analysis and reporting
- **Key Fields**: name
- **Relationships**: Used in economic analysis
- **Business Logic**: Enables sector-based business classification

### 66. `economic_units_directory`

**Purpose**: Directory of economic units (DENUE data)

- **Primary Use**: Economic unit registry and business directory
- **Key Fields**: commercial_name, economic_activity, geom
- **Relationships**: Links to economic activities and locations
- **Business Logic**: Provides comprehensive business directory

### 67. `economic_support`

**Purpose**: Economic support programs and assistance

- **Primary Use**: Track economic support programs for businesses
- **Key Fields**: support_type, description, eligibility_criteria
- **Relationships**: May link to businesses and municipalities
- **Business Logic**: Enables economic development program management

---

## Authentication & Authorization Tables

### 68. `auth_group`

**Purpose**: Django-style authentication groups

- **Primary Use**: Group-based permission management
- **Key Fields**: name
- **Relationships**: Links to users and permissions
- **Business Logic**: Provides group-based access control

### 69. `auth_permission`

**Purpose**: System permissions and access rights

- **Primary Use**: Define granular system permissions
- **Key Fields**: name, content_type_id, codename
- **Relationships**: Links to groups and users
- **Business Logic**: Enables fine-grained permission control

### 70. `auth_group_permissions`

**Purpose**: Link groups to permissions

- **Primary Use**: Assign permissions to user groups
- **Key Fields**: group_id, permission_id
- **Relationships**: Links groups to permissions
- **Business Logic**: Enables group-based permission assignment

### 71. `auth_user_groups`

**Purpose**: Assign users to authentication groups

- **Primary Use**: User group membership management
- **Key Fields**: user_id, group_id
- **Relationships**: Links users to groups
- **Business Logic**: Enables user group assignments

### 72. `auth_user_user_permissions`

**Purpose**: Direct user permission assignments

- **Primary Use**: Assign specific permissions to individual users
- **Key Fields**: user_id, permission_id
- **Relationships**: Links users to permissions
- **Business Logic**: Enables individual user permission overrides

### 73. `authtoken_token`

**Purpose**: API authentication tokens

- **Primary Use**: API access token management
- **Key Fields**: key, user_id, created
- **Relationships**: Links to users
- **Business Logic**: Enables API authentication

---

## Audit & Logging Tables

### 74. `business_logs`

**Purpose**: Comprehensive business activity logging

- **Primary Use**: Track all business-related actions and changes
- **Key Fields**: action, user_id, procedure_id, previous_value
- **Relationships**: Links to users and procedures
- **Business Logic**: Provides complete audit trail for business activities

### 75. `issue_resolution`

**Purpose**: Track resolution of system issues and problems

- **Primary Use**: Issue tracking and resolution management
- **Key Fields**: issue_description, resolution_notes, resolved_by
- **Relationships**: May link to procedures and users
- **Business Logic**: Enables systematic issue resolution

### 76. `permit_renewals`

**Purpose**: Track permit and license renewal processes

- **Primary Use**: Manage renewal workflows for permits and licenses
- **Key Fields**: permit_id, renewal_date, expiration_date, status
- **Relationships**: Links to licenses and procedures
- **Business Logic**: Enables automated renewal management

### 77. `renewal_files`

**Purpose**: Files associated with renewal processes

- **Primary Use**: Document management for renewals
- **Key Fields**: renewal_id, file_path, file_type, upload_date
- **Relationships**: Links to renewals
- **Business Logic**: Supports document requirements for renewals

### 78. `renewal_file_histories`

**Purpose**: History of renewal file changes

- **Primary Use**: Track changes to renewal documentation
- **Key Fields**: renewal_file_id, change_type, changed_by, change_date
- **Relationships**: Links to renewal files and users
- **Business Logic**: Maintains audit trail for renewal documents

### 79. `renewals`

**Purpose**: Main renewal tracking table

- **Primary Use**: Core renewal process management
- **Key Fields**: permit_id, renewal_type, status, due_date
- **Relationships**: Links to permits and files
- **Business Logic**: Central renewal process management

---

## Legacy & System Tables

### 80. `migrations`

**Purpose**: Database migration tracking (Laravel-style)

- **Primary Use**: Track applied database migrations
- **Key Fields**: migration, batch
- **Relationships**: System table
- **Business Logic**: Ensures database schema consistency

### 81. `answers_json`

**Purpose**: JSON-formatted answer storage (legacy/alternative)

- **Primary Use**: Alternative answer storage format
- **Key Fields**: procedure_id, json_data, metadata
- **Relationships**: Alternative to structured answers table
- **Business Logic**: Supports flexible answer formats

### 82. `dependency_revision`

**Purpose**: Legacy dependency review system

- **Primary Use**: Historical dependency tracking (may be deprecated)
- **Key Fields**: procedure_id, revision_status, notes
- **Relationships**: Links to procedures
- **Business Logic**: Legacy workflow support

---

## 📊 Table Statistics Summary

### By Category:

- **Core System**: 3 tables
- **User Management**: 6 tables
- **Municipality & Administration**: 4 tables
- **Procedure Management**: 7 tables
- **Business License Management**: 5 tables
- **Business Classification**: 8 tables
- **Department & Workflow**: 10 tables
- **Geospatial & Mapping**: 13 tables
- **Content Management**: 3 tables
- **Configuration & Reference**: 8 tables
- **Authentication & Authorization**: 6 tables
- **Audit & Logging**: 6 tables
- **Legacy & System**: 3 tables

### **Total Tables**: 82 tables

### Key Relationships:

- **Municipality-centric**: 45+ tables directly relate to municipalities
- **User-connected**: 25+ tables link to user activities
- **Spatial-enabled**: 13+ tables include geospatial data
- **Audit-enabled**: 15+ tables include change tracking

---

## 🎯 Usage Patterns

### **Most Critical Tables**:

1. `municipalities` - Central tenant management
2. `users` - Authentication and access control
3. `procedures` - Core business process
4. `business_licenses` - Primary business outcome
5. `departments` - Workflow organization

### **Most Connected Tables**:

1. `municipalities` - Hub for multi-tenancy
2. `users` - Connected to all user activities
3. `procedures` - Central to workflow processes
4. `fields` - Dynamic form generation
5. `departments` - Workflow routing

### **Spatial Tables** (PostGIS-enabled):

- All `base_*` geographic tables
- `*_footprints` tables
- `procedure_registrations`
- `urban_development_zonings*`
- `public_space_mapping`

---

_Last updated: July 2025_
