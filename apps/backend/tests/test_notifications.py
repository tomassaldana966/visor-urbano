import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from app.utils.notifications import send_notification


class TestNotificationUtils:
    """Test cases for notification utilities."""

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_with_email(self, mock_send_email, mock_notification_class):
        """Test sending notification with email."""
        # Mock the notification instance and database session
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_send_email.return_value = True
        mock_db_session = Mock()

        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="Test comment",
            folio="TEST-001",
            send_email_notification=True
        )

        # Verify notification was created
        mock_notification_class.assert_called_once()
        mock_db_session.add.assert_called_once_with(mock_notification)
        mock_db_session.commit.assert_called()
        assert result == mock_notification

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_without_email(self, mock_send_email, mock_notification_class):
        """Test sending notification without email."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_db_session = Mock()

        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="Test comment",
            send_email_notification=False
        )

        # Verify email was not sent
        mock_send_email.assert_not_called()
        # Verify notification was still created
        mock_notification_class.assert_called_once()
        mock_db_session.add.assert_called_once_with(mock_notification)
        mock_db_session.commit.assert_called()
        assert result == mock_notification

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_email_failure(self, mock_send_email, mock_notification_class):
        """Test notification creation when email fails."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_send_email.return_value = False  # Email failed
        mock_db_session = Mock()

        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="Test comment",
            folio="TEST-001",
            send_email_notification=True
        )

        # Verify notification was still created despite email failure
        mock_notification_class.assert_called_once()
        mock_db_session.add.assert_called_once_with(mock_notification)
        mock_db_session.commit.assert_called()
        assert result == mock_notification

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_with_optional_folio(self, mock_send_email, mock_notification_class):
        """Test notification creation with optional folio parameter."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_db_session = Mock()

        # Test without folio
        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="Test comment",
            send_email_notification=False
        )

        mock_notification_class.assert_called_once()
        assert result == mock_notification

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_database_error(self, mock_send_email, mock_notification_class):
        """Test notification handling when database operation fails."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_db_session = Mock()
        mock_db_session.commit.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            send_notification(
                db=mock_db_session,
                applicant_email="test@example.com",
                comment="Test comment",
                send_email_notification=False
            )

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_different_parameters(self, mock_send_email, mock_notification_class):
        """Test notification with different parameter combinations."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_db_session = Mock()

        # Test with all parameters
        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="Full test comment",
            folio="FULL-TEST-001",
            send_email_notification=True
        )

        # Verify all parameters were used correctly
        mock_notification_class.assert_called_once()
        mock_send_email.assert_called_once()
        assert result == mock_notification

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_empty_comment(self, mock_send_email, mock_notification_class):
        """Test notification with empty comment."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_db_session = Mock()

        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="",
            send_email_notification=False
        )

        mock_notification_class.assert_called_once()
        assert result == mock_notification

    @patch('app.utils.notifications.Notification')
    @patch('app.utils.notifications.send_email')
    def test_send_notification_none_folio(self, mock_send_email, mock_notification_class):
        """Test notification with None folio."""
        mock_notification = Mock()
        mock_notification_class.return_value = mock_notification
        mock_db_session = Mock()

        result = send_notification(
            db=mock_db_session,
            applicant_email="test@example.com",
            comment="Test with None folio",
            folio=None,
            send_email_notification=False
        )

        mock_notification_class.assert_called_once()
        assert result == mock_notification
