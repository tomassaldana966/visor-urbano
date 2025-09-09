import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.routers.procedure_registrations import router
from config.settings import get_db

app = FastAPI()
app.include_router(router, prefix="/v1/procedure-registrations")

FAKE_PROCEDURE_REGISTRATIONS = [
    {
        "id": 1,
        "reference": "TEST-001",
        "area": 150.5,
        "business_sector": "Commercial",
        "procedure_type": "License",
        "procedure_origin": "Municipal",
        "historical_id": 1001,
        "bbox": "32.5,-117.2,32.6,-117.1",
        "municipality_id": 1,
        "geom": {
            "type": "Polygon",
            "coordinates": [[
                [-117.2, 32.5],
                [-117.1, 32.5],
                [-117.1, 32.6],
                [-117.2, 32.6],
                [-117.2, 32.5]
            ]]
        }
    },
    {
        "id": 2,
        "reference": "TEST-002",
        "area": 200.0,
        "business_sector": "Industrial",
        "procedure_type": "Permit",
        "procedure_origin": "State",
        "historical_id": 1002,
        "bbox": "32.6,-117.3,32.7,-117.2",
        "municipality_id": 1,
        "geom": {
            "type": "Polygon",
            "coordinates": [[
                [-117.3, 32.6],
                [-117.2, 32.6],
                [-117.2, 32.7],
                [-117.3, 32.7],
                [-117.3, 32.6]
            ]]
        }
    },
    {
        "id": 3,
        "reference": "TEST-003",
        "area": 75.25,
        "business_sector": "Residential",
        "procedure_type": "License",
        "procedure_origin": "Municipal",
        "historical_id": 1003,
        "bbox": "32.7,-117.4,32.8,-117.3",
        "municipality_id": 2,
        "geom": None
    }
]

class FakeResult:
    def __init__(self, data):
        self.data = data

    def scalars(self):
        return FakeScalars(self.data)

    def scalar_one_or_none(self):
        if self.data:
            mock_obj = Mock()
            for key, value in self.data[0].items():
                setattr(mock_obj, key, value)
            return mock_obj
        return None

    def fetchall(self):
        """Add fetchall method for geometry endpoints"""
        result = []
        for item in self.data:
            # Create a mock object that simulates the row returned by ST_AsGeoJSON query
            mock_row = Mock()
            mock_row.id = item.get("id")
            mock_row.reference = item.get("reference")
            mock_row.area = item.get("area")
            mock_row.business_sector = item.get("business_sector")
            mock_row.procedure_type = item.get("procedure_type")
            mock_row.procedure_origin = item.get("procedure_origin")
            mock_row.historical_id = item.get("historical_id")
            mock_row.bbox = item.get("bbox")
            mock_row.municipality_id = item.get("municipality_id")
            # Simulate ST_AsGeoJSON output
            geom = item.get("geom")
            if geom:
                import json
                mock_row.geom_json = json.dumps(geom)
            else:
                mock_row.geom_json = None
            result.append(mock_row)
        return result

    def fetchone(self):
        """Add fetchone method for single geometry record endpoints"""
        if self.data:
            item = self.data[0]
            mock_row = Mock()
            mock_row.id = item.get("id")
            mock_row.reference = item.get("reference")
            mock_row.area = item.get("area")
            mock_row.business_sector = item.get("business_sector")
            mock_row.procedure_type = item.get("procedure_type")
            mock_row.procedure_origin = item.get("procedure_origin")
            mock_row.historical_id = item.get("historical_id")
            mock_row.bbox = item.get("bbox")
            mock_row.municipality_id = item.get("municipality_id")
            # Simulate ST_AsGeoJSON output
            geom = item.get("geom")
            if geom:
                import json
                mock_row.geom_json = json.dumps(geom)
            else:
                mock_row.geom_json = None
            return mock_row
        return None

class FakeScalars:
    def __init__(self, data):
        self.data = data

    def all(self):
        result = []
        for item in self.data:
            mock_obj = Mock()
            for key, value in item.items():
                setattr(mock_obj, key, value)
            result.append(mock_obj)
        return result

    def first(self):
        if self.data:
            mock_obj = Mock()
            for key, value in self.data[0].items():
                setattr(mock_obj, key, value)
            return mock_obj
        return None

class FakeAsyncSession:
    def __init__(self, data=None):
        self.data = data if data is not None else FAKE_PROCEDURE_REGISTRATIONS
        self._committed = False
        self._refreshed_objects = []
        self._new_record_id = 100
        self._query_id = None

    async def execute(self, statement):
        import re
        query_str = str(statement).lower()
        if "select" in query_str:
            # Handle geometry queries (with ST_AsGeoJSON)
            if "st_asgeojson" in query_str or "geom_json" in query_str:
                if "municipality_id" in query_str and "=" in query_str:
                    filtered_data = [record for record in self.data if record.get("municipality_id") == 1]
                    return FakeResult(filtered_data)
                if "business_sector" in query_str and "ilike" in query_str:
                    filtered_data = [record for record in self.data if "Commercial" in record.get("business_sector", "")]
                    return FakeResult(filtered_data)
                if "reference" in query_str and "ilike" in query_str:
                    filtered_data = [record for record in self.data if "TEST" in record.get("reference", "")]
                    return FakeResult(filtered_data)
                if "where" in query_str and "id" in query_str and "=" in query_str:
                    id_match = re.search(r'id\s*=\s*(\d+)', query_str)
                    if id_match:
                        search_id = int(id_match.group(1))
                    else:
                        search_id = getattr(self, '_query_id', 1)
                    record_data = [record for record in self.data if record.get("id") == search_id]
                    return FakeResult(record_data)
                return FakeResult(self.data)
            
            # Handle regular queries
            if "municipality_id" in query_str and "=" in query_str:
                filtered_data = [record for record in self.data if record.get("municipality_id") == 1]
                return FakeResult(filtered_data)
            if "business_sector" in query_str and "ilike" in query_str:
                filtered_data = [record for record in self.data if "Commercial" in record.get("business_sector", "")]
                return FakeResult(filtered_data)
            if "reference" in query_str and "ilike" in query_str:
                filtered_data = [record for record in self.data if "TEST" in record.get("reference", "")]
                return FakeResult(filtered_data)
            if "where" in query_str and "id" in query_str and "=" in query_str:
                id_match = re.search(r'id\s*=\s*(\d+)', query_str)
                if id_match:
                    search_id = int(id_match.group(1))
                else:
                    search_id = getattr(self, '_query_id', 1)
                record_data = [record for record in self.data if record.get("id") == search_id]
                return FakeResult(record_data)
            return FakeResult(self.data)
        return FakeResult([])

    def set_query_id(self, id_value):
        self._query_id = id_value

    def add(self, obj):
        if hasattr(obj, 'reference'):
            obj.id = self._new_record_id
            self._new_record_id += 1
            for key, value in FAKE_PROCEDURE_REGISTRATIONS[0].items():
                if not hasattr(obj, key) and key != 'id':
                    setattr(obj, key, value)

    async def commit(self):
        self._committed = True

    async def refresh(self, obj):
        self._refreshed_objects.append(obj)
        if hasattr(obj, 'reference'):
            for key, value in FAKE_PROCEDURE_REGISTRATIONS[0].items():
                if not hasattr(obj, key):
                    setattr(obj, key, value)

    async def delete(self, obj):
        """Mock delete method"""
        pass

def get_fake_db():
    return FakeAsyncSession()

app.dependency_overrides[get_db] = get_fake_db

client = TestClient(app)

class TestProcedureRegistrations:
    def test_list_procedure_registrations_all(self):
        response = client.get("/v1/procedure-registrations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["reference"] == "TEST-001"
        assert data[0]["business_sector"] == "Commercial"

    def test_list_procedure_registrations_with_municipality_filter(self):
        response = client.get("/v1/procedure-registrations/?municipio_id=1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_procedure_registrations_with_business_sector_filter(self):
        response = client.get("/v1/procedure-registrations/?business_sector=Commercial")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_procedure_registrations_with_reference_filter(self):
        response = client.get("/v1/procedure-registrations/?reference=TEST")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_procedure_registrations_with_all_filters(self):
        response = client.get(
            "/v1/procedure-registrations/?municipio_id=1&business_sector=Commercial&reference=TEST"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_procedure_registration_success(self):
        response = client.get("/v1/procedure-registrations/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["reference"] == "TEST-001"
        assert data["business_sector"] == "Commercial"

    def test_get_procedure_registration_not_found(self):
        def get_fake_db_empty():
            session = FakeAsyncSession()
            original_execute = session.execute
            async def mock_execute(statement):
                query_str = str(statement).lower()
                if "where" in query_str and "id" in query_str:
                    return FakeResult([])
                return await original_execute(statement)
            session.execute = mock_execute
            return session
        app.dependency_overrides[get_db] = get_fake_db_empty
        response = client.get("/v1/procedure-registrations/99999")
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Record not found"
        app.dependency_overrides[get_db] = get_fake_db

    def test_list_procedure_registrations_with_geometry(self):
        response = client.get("/v1/procedure-registrations/geometry")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_procedure_registrations_with_geometry_filtered(self):
        response = client.get("/v1/procedure-registrations/geometry?municipio_id=1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_procedure_registration_with_geometry_success(self):
        response = client.get("/v1/procedure-registrations/geometry/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["reference"] == "TEST-001"

    def test_get_procedure_registration_with_geometry_not_found(self):
        def get_fake_db_empty():
            session = FakeAsyncSession()
            original_execute = session.execute
            async def mock_execute(statement):
                query_str = str(statement).lower()
                if "where" in query_str and "id" in query_str:
                    return FakeResult([])
                return await original_execute(statement)
            session.execute = mock_execute
            return session
        app.dependency_overrides[get_db] = get_fake_db_empty
        response = client.get("/v1/procedure-registrations/geometry/99999")
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Record not found"
        app.dependency_overrides[get_db] = get_fake_db

    def test_create_procedure_registration_success(self):
        registration_data = {
            "reference": "NEW-TEST-001",
            "area": 100.0,
            "business_sector": "Technology",
            "procedure_type": "License",
            "procedure_origin": "Municipal",
            "historical_id": 2001,
            "bbox": "32.8,-117.5,32.9,-117.4",
            "municipality_id": 1,
            "geom": {
                "type": "Polygon",
                "coordinates": [[
                    [-117.5, 32.8],
                    [-117.4, 32.8],
                    [-117.4, 32.9],
                    [-117.5, 32.9],
                    [-117.5, 32.8]
                ]]
            }
        }
        response = client.post("/v1/procedure-registrations/", json=registration_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["reference"] == "NEW-TEST-001"
        assert data["business_sector"] == "Technology"

    def test_create_procedure_registration_minimal_data(self):
        registration_data = {
            "area": 50.0
        }
        response = client.post("/v1/procedure-registrations/", json=registration_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["area"] == 50.0

    def test_update_procedure_registration_success(self):
        update_data = {
            "reference": "UPDATED-TEST-001",
            "area": 175.0,
            "business_sector": "Updated Commercial"
        }
        response = client.patch("/v1/procedure-registrations/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["reference"] == "UPDATED-TEST-001"
        assert data["area"] == 175.0

    def test_update_procedure_registration_not_found(self):
        def get_fake_db_empty():
            session = FakeAsyncSession()
            original_execute = session.execute
            async def mock_execute(statement):
                query_str = str(statement).lower()
                if "where" in query_str and "id" in query_str:
                    return FakeResult([])
                return await original_execute(statement)
            session.execute = mock_execute
            return session
        app.dependency_overrides[get_db] = get_fake_db_empty
        update_data = {
            "reference": "UPDATED-TEST-999",
            "area": 175.0
        }
        response = client.patch("/v1/procedure-registrations/99999", json=update_data)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Record not found"
        app.dependency_overrides[get_db] = get_fake_db

    def test_update_procedure_registration_geom_success(self):
        geom_data = {
            "properties": {
                "folio": "GEOM-TEST-001",
                "giro": "Updated Business",
                "area": 250.0,
                "municipio": 2
            }
        }
        response = client.patch("/v1/procedure-registrations/geometry/1", json=geom_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_update_procedure_registration_geom_legacy_fields(self):
        geom_data = {
            "properties": {
                "folio": "LEGACY-001",
                "giro": "Legacy Business",
                "area": 300.0,
                "municipio": 3
            }
        }
        response = client.patch("/v1/procedure-registrations/geometry/1", json=geom_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_update_procedure_registration_geom_partial_properties(self):
        geom_data = {
            "properties": {
                "folio": "PARTIAL-001"
            }
        }
        response = client.patch("/v1/procedure-registrations/geometry/1", json=geom_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_update_procedure_registration_geom_empty_properties(self):
        geom_data = {
            "properties": {}
        }
        response = client.patch("/v1/procedure-registrations/geometry/1", json=geom_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_update_procedure_registration_geom_no_properties(self):
        geom_data = {}
        response = client.patch("/v1/procedure-registrations/geometry/1", json=geom_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_update_procedure_registration_geom_not_found(self):
        def get_fake_db_empty():
            session = FakeAsyncSession()
            original_execute = session.execute
            async def mock_execute(statement):
                query_str = str(statement).lower()
                if "where" in query_str and "id" in query_str:
                    return FakeResult([])
                return await original_execute(statement)
            session.execute = mock_execute
            return session
        app.dependency_overrides[get_db] = get_fake_db_empty
        geom_data = {
            "properties": {
                "folio": "NOT-FOUND-001"
            }
        }
        response = client.patch("/v1/procedure-registrations/geometry/99999", json=geom_data)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Record not found"
        app.dependency_overrides[get_db] = get_fake_db

    def test_create_procedure_registration_with_invalid_geom(self):
        registration_data = {
            "area": 100.0,
            "geom": {
                "type": "InvalidGeometry",
                "coordinates": "invalid"
            }
        }
        response = client.post("/v1/procedure-registrations/", json=registration_data)
        assert response.status_code in [200, 422]

    def test_update_procedure_registration_empty_data(self):
        response = client.patch("/v1/procedure-registrations/1", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_list_procedure_registrations_with_invalid_filters(self):
        response = client.get("/v1/procedure-registrations/?municipio_id=invalid")
        assert response.status_code == 422

    def test_get_procedure_registration_with_invalid_id(self):
        response = client.get("/v1/procedure-registrations/invalid")
        assert response.status_code in [404, 422]

    def test_update_procedure_registration_with_invalid_id(self):
        update_data = {"area": 100.0}
        response = client.patch("/v1/procedure-registrations/invalid", json=update_data)
        assert response.status_code in [404, 422]
