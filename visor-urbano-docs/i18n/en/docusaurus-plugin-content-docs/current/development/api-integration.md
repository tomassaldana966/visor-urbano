# 🔗 API-Storybook-Swagger Integration

This section documents the complete integration between frontend routes, Storybook components, and backend API endpoints, providing a unified development experience.

## 🎯 Objective

Create a clear and accessible mapping that allows developers to:

- **Navigate quickly** between frontend and backend
- **Find reusable components** in Storybook
- **Understand available API endpoints** in Swagger
- **Maintain consistency** in development

## 📊 Quick Links

| Tool               | Local URL                                           | Description                            |
| ------------------ | --------------------------------------------------- | -------------------------------------- |
| 🎨 **Storybook**   | [localhost:6006](http://localhost:6006)             | Interactive UI component documentation |
| 📡 **Swagger API** | [localhost:8000/docs](http://localhost:8000/docs)   | Complete REST endpoint documentation   |
| 🔧 **ReDoc API**   | [localhost:8000/redoc](http://localhost:8000/redoc) | Alternative and elegant API view       |
| 📖 **Docusaurus**  | [localhost:3000](http://localhost:3000)             | This technical documentation           |

## 🗺️ Interactive Mapping

import ApiIntegrationTable from '@site/src/components/ApiIntegrationTable';

<ApiIntegrationTable />

## 🛠️ How to Use This Documentation

### For Frontend Developers

1. **Before creating a new component:**

   - Search Storybook for similar existing components
   - Review established design patterns
   - Check the integration table for usage examples

2. **When working on a route:**

   - Identify which endpoints you need from the table
   - Check Swagger documentation to understand schemas
   - Use existing Storybook components when possible

3. **To maintain consistency:**
   - Follow patterns established in similar routes
   - Use the same base components for common elements
   - Keep naming consistent with the rest of the project

### For Backend Developers

1. **When creating new endpoints:**

   - Document clearly in Swagger with examples
   - Use consistent naming with similar endpoints
   - Group related endpoints in the same router

2. **For frontend integration:**

   - Review which frontend routes will consume your API
   - Ensure schemas are clear and complete
   - Consider error cases and validate responses

3. **Maintenance:**
   - Update documentation when changing endpoints
   - Run the generation script after important changes

### For DevOps and QA

1. **Integration validation:**

   - Use direct links to test each component
   - Verify endpoints respond correctly
   - Validate that documentation is up to date

2. **Automation:**
   - The `generate-api-docs.sh` script should run in CI/CD
   - Links should be automatically validated
   - Documentation should regenerate with each deployment

## 🔄 Automation

### Regenerate Documentation

```bash
# Method 1: Direct script
./scripts/generate-api-docs.sh

# Method 2: npm/pnpm command
pnpm docs:generate-api

# Method 3: As part of development workflow
pnpm dev:docs  # Includes automatic regeneration
```

### CI/CD Configuration

To keep documentation always updated, add this to your pipeline:

```yaml
# .github/workflows/docs.yml
- name: Generate API Documentation
  run: |
    ./scripts/generate-api-docs.sh
    git add docs/development/generated-api-integration.md
    git commit -m "docs: update API integration mapping" || true
```

## 📋 Conventions

### Story Naming

```typescript
// ✅ Correct
export default {
  title: 'Components/Forms/LoginForm',
  component: LoginForm,
};

// ❌ Avoid
export default {
  title: 'login-form',
  component: LoginForm,
};
```

### Endpoint Documentation

```python
# ✅ Correct
@router.get("/business-licenses/",
    summary="List business licenses",
    description="Retrieve a paginated list of business licenses with optional filtering",
    response_model=BusinessLicenseResponse
)

# ❌ Avoid
@router.get("/licenses/")  # Without documentation
```

### Route Structure

```typescript
// ✅ Correct - file: routes/licenses.tsx
export default function LicensesRoute() {
  // Import specific components from Storybook
  // Use documented endpoints from Swagger
}

// ❌ Avoid - complex logic without componentization
```

## 🎨 Design Patterns

### Base Components

| Component | Usage         | Storybook                                                                      |
| --------- | ------------- | ------------------------------------------------------------------------------ |
| `Button`  | All actions   | [View in Storybook](http://localhost:6006/?path=/docs/components-button--docs) |
| `Input`   | Forms         | [View in Storybook](http://localhost:6006/?path=/docs/components-input--docs)  |
| `Table`   | Data listings | [View in Storybook](http://localhost:6006/?path=/docs/components-table--docs)  |
| `Modal`   | Popup windows | [View in Storybook](http://localhost:6006/?path=/docs/components-modal--docs)  |

### API Patterns

| Pattern | Endpoint                   | Description          |
| ------- | -------------------------- | -------------------- |
| List    | `GET /v1/resource/`        | List with pagination |
| Detail  | `GET /v1/resource/{id}`    | Get by ID            |
| Create  | `POST /v1/resource/`       | Create new resource  |
| Update  | `PUT /v1/resource/{id}`    | Update existing      |
| Delete  | `DELETE /v1/resource/{id}` | Delete resource      |

## 🔍 Search and Navigation

### Finding Components

1. **By functionality:** Use search in the interactive table above
2. **By category:** Navigate directly in Storybook by folders
3. **By route:** Find which components each page uses

### Finding Endpoints

1. **By router:** Use automatically generated documentation
2. **By functionality:** Search in Swagger by tags and operations
3. **By frontend route:** Check the integration table

## 📚 Additional Resources

- [Auto-Generated Documentation](./generated-api-integration) - Complete updated mapping
- [Development README](./README.md) - Guide for contributors
- [Project Architecture](../getting-started/overview) - System overview

## 🤝 Contributing

1. **Adding new components:** Create corresponding story in Storybook
2. **New endpoints:** Document in Swagger and run generation script
3. **New routes:** Ensure you map used components and APIs
4. **Improvements:** Suggest improvements to this documentation or automation script

---

> 💡 **Tip:** This documentation is a starting point. The exact and updated mapping will always be in the [auto-generated documentation](./generated-api-integration).
