# Procedures API Testing

This directory contains scripts to seed test data for the Procedures API and test the endpoints.

## Setup and Testing

1. **Seed the database with test data**:
   ```bash
   cd /path/to/visor-urbano/apps/backend
   python scripts/seed_procedures.py
   ```

2. **Start the FastAPI server** (if not already running):
   ```bash
   cd /path/to/visor-urbano/apps/backend
   uvicorn app.main:app --reload
   ```

3. **Run the API tests**:
   ```bash
   cd /path/to/visor-urbano/apps/backend
   ./scripts/test_procedures_api.sh
   ```

## Available Test Data

### Regular Procedures
- `TEST-001`: Active procedure (construction license)
- `TEST-002`: Completed procedure (commercial license)
- `TEST-003`: Renewal procedure referencing `TEST-002`
- `TEST-004`: Rejected procedure

### Historical Procedures
- `HIST-001`: Historical construction license (2 years old)
- `HIST-002`: Historical commercial license (1 year old)
- `HIST-003`: Historical rejected procedure (1.5 years old)

### Answers
Answer records are available for all procedures with various property values.

## Endpoints Tested

The test script verifies all the procedures API endpoints including:
- List procedures (with various filters)
- Get procedure details
- Create new procedures
- Copy procedures
- Upload payment orders
- and more...

## Modifying Test Data

To modify the test data, edit the SQL file at:
```
scripts/seeds/procedures_test_data.sql
```
Then run the seeder script again to update the database.
