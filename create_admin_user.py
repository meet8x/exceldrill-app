import sys
import os
from sqlalchemy.orm import Session

# Add the current directory to sys.path to make backend imports work
sys.path.append(os.getcwd())

from backend.app.db.base import Base
from backend.app.db.session import engine, SessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def create_admin_user():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    output = []
    try:
        email = "admin@example.com"
        password = "adminpassword"
        
        user = db.query(User).filter(User.email == email).first()
        if user:
            output.append(f"User {email} already exists. Updating to premium...")
            user.is_paid = True
            user.plan_type = "lifetime"
            user.plan_expiry = None
            # Update password just in case
            user.hashed_password = get_password_hash(password)
        else:
            output.append(f"Creating new premium user {email}...")
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_paid=True,
                plan_type="lifetime",
                plan_expiry=None
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)
        output.append(f"Successfully configured user: {user.email}")
        output.append(f"Password: {password}")
        output.append(f"Plan: {user.plan_type}")
        
    except Exception as e:
        output.append(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()
    
    with open("admin_user_result.txt", "w") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    create_admin_user()
