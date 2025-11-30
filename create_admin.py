from backend.app.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@example.com").first()
        if user:
            print("User admin@example.com exists. Updating password...")
            user.hashed_password = get_password_hash("adminpassword")
            user.is_active = True
            user.is_paid = True
            user.plan_type = "lifetime"
        else:
            print("User admin@example.com does not exist. Creating...")
            user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("adminpassword"),
                is_active=True,
                is_paid=True,
                plan_type="lifetime"
            )
            db.add(user)
        
        db.commit()
        print("Admin user setup complete.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
