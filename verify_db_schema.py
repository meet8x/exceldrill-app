import sys
import os
from sqlalchemy import inspect

# Add the current directory to sys.path to make backend imports work
sys.path.append(os.getcwd())

from backend.app.db.base import Base
from backend.app.db.session import engine
from backend.app.models.user import User

def verify_schema():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Inspecting schema...")
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('user')]
    
    with open("schema_result.txt", "w") as f:
        f.write(f"User table columns: {columns}\n")
        
        required_columns = ['plan_type', 'plan_expiry', 'is_paid']
        missing = [col for col in required_columns if col not in columns]
        
        if missing:
            f.write(f"ERROR: Missing columns: {missing}\n")
            sys.exit(1)
        else:
            f.write("SUCCESS: All required columns present.\n")

if __name__ == "__main__":
    verify_schema()
