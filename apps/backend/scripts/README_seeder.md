# Test Users Seeder

This script creates 6 test users for the FastAPI backend with predefined roles and credentials.

## What it creates

The seeder creates 6 users with the following pattern:

| User | Email | Password | Role ID | Municipality ID |
|------|--------|----------|---------|-----------------|
| TestUser1 | user1@@bloombergcities.jhu.edu | BloombergcitiesTest2025. | 1 | (specified) |
| TestUser2 | user2@@bloombergcities.jhu.edu | BloombergcitiesTest2025. | 2 | (specified) |
| TestUser3 | user3@@bloombergcities.jhu.edu | BloombergcitiesTest2025. | 3 | (specified) |
| TestUser4 | user4@@bloombergcities.jhu.edu | BloombergcitiesTest2025. | 4 | (specified) |
| TestUser5 | user5@@bloombergcities.jhu.edu | BloombergcitiesTest2025. | 5 | (specified) |
| TestUser6 | user6@@bloombergcities.jhu.edu | BloombergcitiesTest2025. | 6 | (specified) |

## How to run

### Using the main setup script (Recommended)

The easiest way is to use the main setup script from the project root:

```bash
./setup.sh
```

This will:
1. Create a new municipality (asking for information)
2. Automatically run the user seeder with the new municipality ID

### Manual execution

1. Make sure your database is running and accessible
2. Navigate to the backend directory:
   ```bash
   cd apps/backend
   ```

3. Run the seeder script with a municipality ID:
   ```bash
   python scripts/seed_test_users.py --municipality-id <MUNICIPALITY_ID>
   ```

   Or use the default municipality ID (2):
   ```bash
   python scripts/seed_test_users.py
   ```

## What it does

1. **Creates required roles**: Ensures roles 1-6 exist with proper names and descriptions
2. **Creates/updates test users**: Generates 6 test users with the specified credentials
3. **Assigns roles**: Creates proper role assignments for each user
4. **Sets municipality**: All users are assigned to the specified municipality_id

## Important Notes

- The script will **create or update existing users** with the same email addresses
- All passwords are hashed using the same security mechanism as the main application
- Users are created with `is_active: true` and proper role assignments
- The script uses async/await for database operations to match the FastAPI pattern
- Municipality ID can be specified via `--municipality-id` parameter

## Error Handling

If the script fails, it will:
- Roll back any partial changes
- Display a clear error message
- Exit with status code 1

The script is designed to be idempotent - you can run it multiple times safely.

## Command Line Options

- `--municipality-id <ID>`: Specify the municipality ID for all users (default: 2)

## Examples

```bash
# Use default municipality ID (2)
python scripts/seed_test_users.py

# Specify municipality ID
python scripts/seed_test_users.py --municipality-id 5

# Create municipality first, then users
python scripts/create_municipality.py "Test Municipality"
python scripts/seed_test_users.py --municipality-id 3
```
