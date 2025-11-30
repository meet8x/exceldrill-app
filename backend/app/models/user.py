from sqlalchemy import Boolean, Column, Integer, String
from backend.app.db.base import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_paid = Column(Boolean(), default=False)
    plan_type = Column(String, nullable=True) # '24h', 'monthly', 'lifetime'
    plan_expiry = Column(String, nullable=True) # ISO format datetime string
    preferred_color_scheme = Column(String, default="kpmg")
    full_name = Column(String, nullable=True)
    is_verified = Column(Boolean(), default=False)
    otp = Column(String, nullable=True)
    is_admin = Column(Boolean(), default=False)
