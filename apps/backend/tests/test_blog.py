import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
import base64
from datetime import datetime, date

from app.main import app
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from config.settings import get_db


class TestBlog:
    def setup_method(self):
        """Setup for each test method."""
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.client = TestClient(app)
        
        # Override database dependency
        app.dependency_overrides[get_db] = lambda: self.mock_db

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    def create_mock_blog(self, blog_id=1, title="Test Blog", content="Test content"):
        """Helper to create a mock blog object."""
        blog = MagicMock(spec=Blog)
        blog.id = blog_id
        blog.title = title
        blog.slug = f"test-blog-{blog_id}"  # Add slug field
        blog.summary = f"Summary for {title}"
        blog.image = "test_image.jpg"
        blog.link = f"test-blog-{blog_id}"
        blog.body = content
        blog.news_date = date.today()
        blog.blog_type = 1
        blog.municipality_id = 2  # Add municipality_id field
        return blog

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_list_published_success(self):
        """Test successful retrieval of published blogs."""
        # Arrange
        mock_blogs = [
            self.create_mock_blog(1, "Blog 1", "Content 1"),
            self.create_mock_blog(2, "Blog 2", "Content 2")
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_blogs
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/blog/")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    def test_list_published_empty(self):
        """Test retrieval when no published blogs exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/blog/")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_create_blog_success(self):
        """Test successful blog creation."""
        # Arrange
        blog_data = {
            "title": "New Blog",
            "summary": "New blog summary",
            "image": "new_blog.jpg",
            "link": "new-blog",
            "news_date": "2025-06-03",
            "body": "New content",
            "password": "test_password"
        }
        
        mock_blog = self.create_mock_blog(1, "New Blog", "New content")
        
        # Mock max ID query
        mock_max_result = MagicMock()
        mock_max_result.scalar.return_value = 5
        self.mock_db.execute.return_value = mock_max_result
        self.mock_db.refresh.return_value = None

        # Act
        response = self.client.post("/v1/blog/", json=blog_data)

        # Assert
        assert response.status_code == 200
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_create_blog_invalid_password(self):
        """Test blog creation with invalid password."""
        # Arrange
        blog_data = {
            "title": "New Blog",
            "summary": "New blog summary",
            "image": "new_blog.jpg",
            "link": "new-blog",
            "news_date": "2025-06-03",
            "body": "New content",
            "password": "wrong_password"
        }

        # Act
        response = self.client.post("/v1/blog/", json=blog_data)

        # Assert
        assert response.status_code == 403
        assert response.json()["detail"] == "Permission denied"
        self.mock_db.add.assert_not_called()

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_create_blog_no_password(self):
        """Test blog creation without password."""
        # Arrange
        blog_data = {
            "title": "New Blog",
            "summary": "New blog summary",
            "image": "new_blog.jpg",
            "link": "new-blog",
            "news_date": "2025-06-03",
            "body": "New content"
        }

        # Act
        response = self.client.post("/v1/blog/", json=blog_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_get_blog_success(self):
        """Test successful blog retrieval by ID."""
        # Arrange
        mock_blog = self.create_mock_blog(1, "Test Blog", "Test content")
        self.mock_db.get.return_value = mock_blog

        # Act
        response = self.client.get("/v1/blog/1")

        # Assert
        assert response.status_code == 200
        self.mock_db.get.assert_called_once_with(Blog, 1)

    def test_get_blog_not_found(self):
        """Test blog retrieval when blog doesn't exist."""
        # Arrange
        self.mock_db.get.return_value = None

        # Act
        response = self.client.get("/v1/blog/999")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Blog not found"

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_update_blog_success(self):
        """Test successful blog update."""
        # Arrange
        update_data = {
            "title": "Updated Blog",
            "summary": "Updated blog summary",
            "image": "updated_blog.jpg",
            "link": "updated-blog",
            "news_date": "2025-06-03",
            "body": "Updated content",
            "password": "test_password"
        }
        
        mock_blog = self.create_mock_blog(1, "Original Blog", "Original content")
        self.mock_db.get.return_value = mock_blog

        # Act
        response = self.client.put("/v1/blog/1", json=update_data)

        # Assert
        assert response.status_code == 200
        self.mock_db.get.assert_called_once_with(Blog, 1)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_update_blog_invalid_password(self):
        """Test blog update with invalid password."""
        # Arrange
        update_data = {
            "title": "Updated Blog",
            "summary": "Updated blog summary",
            "image": "updated_blog.jpg",
            "link": "updated-blog",
            "news_date": "2025-06-03",
            "body": "Updated content",
            "password": "wrong_password"
        }

        # Act
        response = self.client.put("/v1/blog/1", json=update_data)

        # Assert
        assert response.status_code == 403
        assert response.json()["detail"] == "Permission denied"
        self.mock_db.get.assert_not_called()

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_update_blog_not_found(self):
        """Test blog update when blog doesn't exist."""
        # Arrange
        update_data = {
            "title": "Updated Blog",
            "summary": "Updated blog summary",
            "image": "updated_blog.jpg",
            "link": "updated-blog",
            "news_date": "2025-06-03",
            "body": "Updated content",
            "password": "test_password"
        }
        
        self.mock_db.get.return_value = None

        # Act
        response = self.client.put("/v1/blog/1", json=update_data)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Blog not found"

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_delete_blog_success(self):
        """Test successful blog deletion."""
        # Arrange
        mock_blog = self.create_mock_blog(1, "Test Blog", "Test content")
        self.mock_db.get.return_value = mock_blog
        
        # Encode password
        encoded_password = base64.b64encode("test_password".encode()).decode()

        # Act
        response = self.client.delete(f"/v1/blog/1/{encoded_password}")

        # Assert
        assert response.status_code == 200
        assert response.json() == 1
        self.mock_db.get.assert_called_once_with(Blog, 1)
        self.mock_db.delete.assert_called_once_with(mock_blog)
        self.mock_db.commit.assert_called_once()

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_delete_blog_invalid_password(self):
        """Test blog deletion with invalid password."""
        # Arrange
        encoded_password = base64.b64encode("wrong_password".encode()).decode()

        # Act
        response = self.client.delete(f"/v1/blog/1/{encoded_password}")

        # Assert
        assert response.status_code == 403
        assert response.json()["detail"] == "Permission denied"
        self.mock_db.get.assert_not_called()

    def test_delete_blog_invalid_encoding(self):
        """Test blog deletion with invalid base64 encoding."""
        # Arrange
        invalid_encoded = "invalid_base64!"

        # Act
        response = self.client.delete(f"/v1/blog/1/{invalid_encoded}")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid password encoding"

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_delete_blog_not_found(self):
        """Test blog deletion when blog doesn't exist."""
        # Arrange
        self.mock_db.get.return_value = None
        encoded_password = base64.b64encode("test_password".encode()).decode()

        # Act
        response = self.client.delete(f"/v1/blog/1/{encoded_password}")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Blog not found"

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_get_all_blogs_success(self):
        """Test successful retrieval of all blogs for admin."""
        # Arrange
        mock_blogs = [
            self.create_mock_blog(1, "Blog 1", "Content 1"),
            self.create_mock_blog(2, "Blog 2", "Content 2")
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_blogs
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/blog/user/test_password")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_get_all_blogs_invalid_key(self):
        """Test retrieval of all blogs with invalid key."""
        # Act
        response = self.client.get("/v1/blog/user/wrong_key")

        # Assert
        assert response.status_code == 403
        assert response.json()["detail"] == "Permission denied"
        self.mock_db.execute.assert_not_called()

    @pytest.mark.parametrize("blog_data,expected_error", [
        ({"title": "", "summary": "Summary", "image": "test.jpg", "link": "test", "news_date": "2025-06-03", "body": "Content", "password": "test_password"}, "Field cannot be empty"),
        ({"title": "Title", "summary": "", "image": "test.jpg", "link": "test", "news_date": "2025-06-03", "body": "Content", "password": "test_password"}, "Field cannot be empty"),
        ({"title": "Title", "summary": "Summary", "image": "", "link": "test", "news_date": "2025-06-03", "body": "Content", "password": "test_password"}, "Field cannot be empty"),
        ({"title": "Title", "summary": "Summary", "image": "test.jpg", "link": "", "news_date": "2025-06-03", "body": "Content", "password": "test_password"}, "Field cannot be empty"),
        ({"title": "Title", "summary": "Summary", "image": "test.jpg", "link": "test", "news_date": "2025-06-03", "body": "Content", "municipality_id": -1, "password": "test_password"}, "Municipality ID must be positive"),
    ])
    @patch('config.settings.settings.APP_BLOG_PASS', 'test_password')
    def test_create_blog_validation_errors(self, blog_data, expected_error):
        """Test blog creation with various validation errors."""
        # Act
        response = self.client.post("/v1/blog/", json=blog_data)

        # Assert
        assert response.status_code == 422  # Validation error
        error_detail = response.json()["detail"]
        # Check if the expected error message is in the validation errors
        assert any(expected_error in str(error) for error in error_detail)

    def test_database_error_handling(self):
        """Test handling of database errors."""
        # Arrange
        self.mock_db.execute.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            response = self.client.get("/v1/blog/")
