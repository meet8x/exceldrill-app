import sqlite3

# Connect to database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

try:
    # Add the missing column
    cursor.execute("ALTER TABLE user ADD COLUMN preferred_color_scheme TEXT DEFAULT 'kpmg'")
    conn.commit()
    print("Successfully added preferred_color_scheme column")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column already exists")
    else:
        print(f"Error: {e}")
finally:
    conn.close()
