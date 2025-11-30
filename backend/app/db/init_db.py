from sqlalchemy.orm import Session
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from backend.app.db.session import SessionLocal

def init_db():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@example.com").first()
        if not user:
            print("Creating admin user...")
            user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("adminpassword"),
                is_active=True,
                is_paid=True,
                is_verified=True,
                is_admin=True,
                plan_type="lifetime",
                full_name="Admin User"
            )
            db.add(user)
            db.commit()
            print("Admin user created successfully")
        else:
            # Ensure existing admin has admin privileges
            if not user.is_admin:
                user.is_admin = True
                db.commit()
                print("Admin privileges granted to existing admin user")
            print("Admin user already exists")
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        db.close()
