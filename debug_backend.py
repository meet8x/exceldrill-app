import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    with open("debug_log.txt", "w") as f:
        f.write("Attempting to import backend.main...\n")
        from backend.main import app
        f.write("Import successful!\n")
    with open("debug_success.txt", "w") as f:
        f.write("Success")
except Exception as e:
    with open("debug_fail.txt", "w") as f:
        f.write(f"Import failed: {e}\n")
        import traceback
        traceback.print_exc(file=f)
