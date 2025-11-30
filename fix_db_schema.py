import os
from sqlalchemy import create_engine
from backend.app.db.base import Base
from backend.app.models.user import User
from backend.app.core.security import get_password_hash
from backend.app.db.session import SessionLocal

# Delete existing database
db_path = "sql_app.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted existing database: {db_path}")

# Create new database with updated schema
engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
print("Created new database with updated schema")

# Create admin user
db = SessionLocal()
try:
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        is_active=True,
        is_paid=True,
        plan_type="lifetime",
        preferred_color_scheme="kpmg"
    )
    db.add(admin)
    db.commit()
    print("Created admin user: admin@example.com")
except Exception as e:
    print(f"Error creating admin user: {e}")
    db.rollback()
finally:
    db.close()
