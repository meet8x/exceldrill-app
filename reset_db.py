import os
from backend.app.db.session import engine, SessionLocal
from backend.app.db.base import Base
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def reset_db():
    # 1. Delete existing DB file
    db_file = "sql_app.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted {db_file}")

    # 2. Create tables
    print("Creating tables...")
    # Import all models to ensure they are registered with Base
    # (User is already imported)
    Base.metadata.create_all(bind=engine)

    # 3. Seed Admin User
    print("Seeding admin user...")
    db = SessionLocal()
    try:
        admin_user = User(
            email="admin@exceldrill.ai",
            hashed_password=get_password_hash("admin@2024"),
            is_active=True,
            is_paid=True,
            plan_type="lifetime",
            preferred_color_scheme="kpmg",
            is_verified=True,
            full_name="Admin User",
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created: admin@exceldrill.ai / admin@2024")
    except Exception as e:
        print(f"Error seeding user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_db()
