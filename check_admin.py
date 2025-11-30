import sqlite3

# Connect to database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Check if admin user exists
cursor.execute("SELECT email, is_active, is_paid, plan_type, preferred_color_scheme FROM user WHERE email = 'admin@example.com'")
result = cursor.fetchone()

if result:
    print("Admin user found:")
    print(f"  Email: {result[0]}")
    print(f"  Active: {result[1]}")
    print(f"  Paid: {result[2]}")
    print(f"  Plan Type: {result[3]}")
    print(f"  Color Scheme: {result[4]}")
else:
    print("Admin user NOT found")

conn.close()
