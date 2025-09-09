# WorkflowModal Component

## Overview

The WorkflowModal is a comprehensive component for managing workflows in the director dashboard. It provides a complete interface for creating and editing complex workflow processes with multiple tabs and features.

## Features

### 1. Basic Information Tab

- **Workflow Name**: Name of the workflow process
- **Document Type**: Type of document/information (permit, certificate, authorization, etc.)
- **Description**: Detailed description of the workflow purpose
- **Legal Foundation**: Legal basis for the workflow
- **Process Type**: Construction, Commercial, Land Use, Environmental, Social
- **Steps & Days**: Number of steps and average processing days
- **Active Status**: Whether the workflow is currently active

### 2. Requirements Tab

- **Requirement Management**: Add, edit, and remove requirements
- **Detailed Requirements**: Each requirement includes:
  - Title and detailed description
  - Mandatory/Optional status
  - Department issued flag
  - Conditional logic support

### 3. Conditions Tab

- **Dynamic Conditions**: Rules that affect requirements based on:
  - Property size
  - Activity surface
  - Applicant type
  - Person type (citizen, foreigner)
  - Alcohol sales
  - Activity type
- **Operators**: Greater than, less than, equal to, includes, excludes
- **Actions**: Require, exclude, or modify requirements

### 4. Dependencies Tab

- **Workflow Dependencies**: Define prerequisite workflows
- **Conditions**: Approved, rejected, or completed status
- **Descriptions**: Clear explanation of dependency reasons

### 5. Approvals Tab

- **Multi-step Approval Process**: Define complex approval workflows
- **Department Assignment**: Assign specific departments
- **File Types**: 10 different file types supported
- **Legal Foundation**: Legal basis for each approval step
- **Advanced Features**:
  - Parallel approvals
  - Blocking/non-blocking steps
  - External department handling
  - Estimated processing days
  - Role-based assignments

## Sample Data

The component includes comprehensive sample data for "Licencia de Construcción Residencial" featuring:

### Requirements (5 items)

1. **Identificación Oficial** - Basic ID requirement
2. **Escritura de Propiedad** - Property deed with conditional logic
3. **Planos Arquitectónicos** - Architectural plans
4. **Proyecto Estructural** - Structural project (conditional)
5. **Estudio de Impacto Ambiental** - Environmental impact (conditional)

### Conditions (4 rules)

- Property size > 120m² requires structural project
- Enterprise applicants require additional property documentation
- Large activity surfaces require environmental studies
- Foreign applicants have modified ID requirements

### Dependencies (2 items)

- Land use approval (uso-suelo-001)
- Basic services feasibility (factibilidad-servicios-001)

### Approvals (5 steps)

1. **Atención Ciudadana** - Initial review (3 days)
2. **Desarrollo Urbano** - Technical review (15 days, parallel)
3. **Protección Civil** - Safety review (10 days, parallel)
4. **Licencias de Construcción** - Construction license review (10 days)
5. **Dirección General** - Final approval (7 days, non-blocking)

## File Types Supported

- Document (PDF or image)
- Form to fill
- Certificate/Constancy
- Official identification
- Proof of address
- Property deed
- Technical drawing
- Photograph
- Payment receipt
- Inspection report

## Usage

```tsx
<WorkflowModal
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  workflow={selectedWorkflow}
  onSave={handleSaveWorkflow}
/>
```

## Integration

The component is fully integrated with:

- React i18n for multilingual support
- Director settings page
- Workflow management system
- Translation keys in Spanish and English
