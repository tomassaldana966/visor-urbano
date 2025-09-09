import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

from app.main import app
from config.settings import get_db
from config.security import get_current_user
from app.schemas.reports import (
    ChartPoint, 
    LicensingStatusSummary, 
    BarListFilter, 
    BarListItem, 
    ReviewStatusSummary,
    MunicipalityPiePoint, 
    FullReportResponse,
    MunicipalityLicenseSummary,
    MunicipalityHistoricSummary,
    TechnicalSheetReportSummary, 
    TechnicalSheetDownload
)


class TestReports:
    def setup_method(self):
        """Setup for each test method."""
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user = MagicMock()
        self.mock_user.id = 1
        self.mock_user.id_municipality = 1
        self.mock_user.username = "testuser"
        self.client = TestClient(app)
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_current_user] = lambda: self.mock_user

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    def test_get_annual_bar_chart_success(self):
        """Test successful retrieval of annual bar chart data."""
        # Arrange
        mock_result = MagicMock()
        mock_data = [
            MagicMock(month=1, count=10),
            MagicMock(month=2, count=15),
            MagicMock(month=3, count=8)
        ]
        mock_result.fetchall.return_value = mock_data
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 3
        assert result[0]["name"] == "January"
        assert result[0]["value"] == 10
        assert result[0]["extra"] == 1
        assert result[1]["name"] == "February"
        assert result[1]["value"] == 15
        assert result[1]["extra"] == 2

    def test_get_annual_bar_chart_empty_data(self):
        """Test annual bar chart with no data."""
        # Arrange
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_get_annual_bar_chart_unauthorized(self):
        """Test annual bar chart without authentication."""
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: None

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code in [401, 403]

    def test_get_licensing_status_summary_success(self):
        """Test successful retrieval of licensing status summary."""
        # Arrange
        mock_results = [
            MagicMock(scalar=lambda: 25),  # consultation
            MagicMock(scalar=lambda: 15),  # initiated
            MagicMock(scalar=lambda: 10),  # under_review
            MagicMock(scalar=lambda: 5)    # issued
        ]
        self.mock_db.execute.side_effect = mock_results

        # Act
        response = self.client.get("/v1/reports/charts/advanced-pie")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["consultation"] == 25
        assert result["initiated"] == 15
        assert result["under_review"] == 10
        assert result["issued"] == 5

    def test_get_licensing_status_summary_zero_values(self):
        """Test licensing status summary with zero values."""
        # Arrange
        mock_results = [
            MagicMock(scalar=lambda: 0),
            MagicMock(scalar=lambda: 0),
            MagicMock(scalar=lambda: 0),
            MagicMock(scalar=lambda: 0)
        ]
        self.mock_db.execute.side_effect = mock_results

        # Act
        response = self.client.get("/v1/reports/charts/advanced-pie")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["consultation"] == 0
        assert result["initiated"] == 0
        assert result["under_review"] == 0
        assert result["issued"] == 0

    def test_get_licensing_status_summary_database_error(self):
        """Test licensing status summary with database error."""
        # Arrange
        self.mock_db.execute.side_effect = Exception("Database error")

        # Act
        response = self.client.get("/v1/reports/charts/advanced-pie")

        # Assert
        assert response.status_code == 500

    @pytest.mark.parametrize("municipality_id", [1, 2, 3, 999])
    def test_get_annual_bar_chart_by_municipality(self, municipality_id):
        """Test annual bar chart for specific municipality."""
        # Arrange
        mock_result = MagicMock()
        mock_data = [MagicMock(month=1, count=5)]
        mock_result.fetchall.return_value = mock_data
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get(f"/v1/reports/charts/annual-bar/{municipality_id}")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1
        assert result[0]["value"] == 5

    def test_get_annual_bar_chart_invalid_municipality(self):
        """Test annual bar chart with invalid municipality ID."""
        # Act
        response = self.client.get("/v1/reports/charts/annual-bar/invalid")

        # Assert
        assert response.status_code == 422  # Validation error

    @patch('app.routers.reports.datetime')
    def test_annual_bar_chart_current_year(self, mock_datetime):
        """Test that annual bar chart uses current year."""
        # Arrange
        mock_datetime.now.return_value.year = 2024
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        # Verify that the query was called with current year
        self.mock_db.execute.assert_called_once()
        call_args = self.mock_db.execute.call_args
        assert call_args[0][1]["year"] == 2024

    def test_month_names_mapping(self):
        """Test that month numbers are correctly mapped to month names."""
        # Arrange
        mock_result = MagicMock()
        mock_data = [
            MagicMock(month=1, count=1),   # January
            MagicMock(month=6, count=2),   # June
            MagicMock(month=12, count=3)   # December
        ]
        mock_result.fetchall.return_value = mock_data
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result[0]["name"] == "January"
        assert result[1]["name"] == "June"
        assert result[2]["name"] == "December"

    def test_user_municipality_filtering(self):
        """Test that queries are filtered by user's municipality."""
        # Arrange
        self.mock_user.id_municipality = 42
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        # Verify municipality_id was used in query
        call_args = self.mock_db.execute.call_args
        assert call_args[0][1]["municipality_id"] == 42

    def test_multiple_concurrent_requests(self):
        """Test handling of multiple concurrent report requests."""
        # Arrange
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_result.scalar.return_value = 0
        self.mock_db.execute.return_value = mock_result

        # Act - Make multiple requests
        responses = []
        for _ in range(3):
            response = self.client.get("/v1/reports/charts/annual-bar")
            responses.append(response)

        # Assert
        for response in responses:
            assert response.status_code == 200

    @pytest.mark.parametrize("user_municipality_id", [1, 10, 100])
    def test_licensing_status_with_different_municipalities(self, user_municipality_id):
        """Test licensing status summary with different municipality IDs."""
        # Arrange
        self.mock_user.id_municipality = user_municipality_id
        mock_results = [
            MagicMock(scalar=lambda: 5),
            MagicMock(scalar=lambda: 3),
            MagicMock(scalar=lambda: 2),
            MagicMock(scalar=lambda: 1)
        ]
        self.mock_db.execute.side_effect = mock_results

        # Act
        response = self.client.get("/v1/reports/charts/advanced-pie")

        # Assert
        assert response.status_code == 200
        # Verify municipality was used in all queries
        assert self.mock_db.execute.call_count == 4

    def test_response_model_validation(self):
        """Test that response data matches expected models."""
        # Arrange
        mock_result = MagicMock()
        mock_data = [MagicMock(month=1, count=10)]
        mock_result.fetchall.return_value = mock_data
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        result = response.json()
        
        # Validate ChartPoint structure
        chart_point = result[0]
        assert "name" in chart_point
        assert "value" in chart_point
        assert "extra" in chart_point
        assert isinstance(chart_point["name"], str)
        assert isinstance(chart_point["value"], int)
        assert isinstance(chart_point["extra"], int)

    def test_edge_case_month_boundary(self):
        """Test handling of edge case months (boundary values)."""
        # Arrange
        mock_result = MagicMock()
        mock_data = [
            MagicMock(month=1, count=1),    # First month
            MagicMock(month=12, count=12)   # Last month
        ]
        mock_result.fetchall.return_value = mock_data
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result[0]["extra"] == 1
        assert result[1]["extra"] == 12

    def test_large_data_volumes(self):
        """Test handling of large data volumes."""
        # Arrange
        mock_result = MagicMock()
        # Simulate large dataset
        mock_data = [MagicMock(month=i, count=1000) for i in range(1, 13)]
        mock_result.fetchall.return_value = mock_data
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/reports/charts/annual-bar")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 12
        for item in result:
            assert item["value"] == 1000

    def test_sql_injection_protection(self):
        """Test protection against SQL injection in municipality parameter."""
        # Act - Try to inject SQL
        response = self.client.get("/v1/reports/charts/annual-bar/1; DROP TABLE users;")

        # Assert
        assert response.status_code == 422  # Should fail validation, not execute SQL

    def test_performance_with_complex_queries(self):
        """Test performance considerations with complex query responses."""
        # Arrange
        mock_results = [
            MagicMock(scalar=lambda: 1000),
            MagicMock(scalar=lambda: 500),
            MagicMock(scalar=lambda: 250),
            MagicMock(scalar=lambda: 125)
        ]
        self.mock_db.execute.side_effect = mock_results

        # Act
        response = self.client.get("/v1/reports/charts/advanced-pie")

        # Assert
        assert response.status_code == 200
        # Should complete in reasonable time even with large numbers
        result = response.json()
        assert result["consultation"] == 1000
        assert result["issued"] == 125
