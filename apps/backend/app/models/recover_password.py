from sqlalchemy import Column, Integer, String, DateTime, func, Index
from config.settings import Base
from datetime import datetime, timedelta, timezone


def get_utc_naive_now():
    """Get current UTC datetime as naive (for consistency with database storage)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def ensure_naive_datetime(dt):
    """Ensure datetime is naive by removing timezone info if present"""
    if dt is None:
        return None
    if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


class PasswordRecovery(Base):
    __tablename__ = 'password_recoveries'  

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    expiration_date = Column(DateTime, nullable=False)
    used = Column(Integer, default=0, nullable=False)  # 0 = unused, 1 = used

    # Timezone-aware datetime columns with automatic naive conversion
    created_at = Column(DateTime, default=get_utc_naive_now, nullable=False)
    updated_at = Column(DateTime, default=get_utc_naive_now, onupdate=get_utc_naive_now, nullable=False)

    __table_args__ = (
        Index('idx_email_token', 'email', 'token'),
        Index('idx_expiration_used', 'expiration_date', 'used'),
    )

    def is_expired(self):
        """Check if the token has expired"""
        current_time = get_utc_naive_now()
        expiration_time = ensure_naive_datetime(self.expiration_date)
        return current_time > expiration_time

    def is_valid(self):
        """Check if the token is valid (not expired and not used)"""
        return not self.is_expired() and self.used == 0

    @classmethod
    def get_expiration_time(cls, hours=24):
        """Get expiration time (default 24 hours from now) as naive datetime"""
        return (get_utc_naive_now() + timedelta(hours=hours))
