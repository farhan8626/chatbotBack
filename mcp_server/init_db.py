import mysql.connector
import os

# Connect to the MySQL server (without specifying a database yet)
print("Attempting to connect to MySQL...")
try:
    # Try with password 'root' (common default)
    conn = mysql.connector.connect(host="localhost", user="root", password="Farhan@8626")
except mysql.connector.Error:
    try:
        # Try with empty password (common for XAMPP/WAMP)
        conn = mysql.connector.connect(host="localhost", user="root", password="")
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        print("Please ensure MySQL is running and the root password is correct.")
        exit(1)

print("Connected successfully! Executing setup_db.sql...")
cursor = conn.cursor()

# Read the SQL file
script_dir = os.path.dirname(os.path.abspath(__file__))
sql_file_path = os.path.join(script_dir, "setup_db.sql")

with open(sql_file_path, 'r') as file:
    sql_script = file.read()

# Split by ';' to execute statements one by one, 
# ignoring empty statements
statements = sql_script.split(';')
for statement in statements:
    if statement.strip():
        try:
            cursor.execute(statement)
        except mysql.connector.Error as err:
            print(f"Error executing statement: {err}\nStatement: {statement}")

conn.commit()
cursor.close()
conn.close()
print("Database 'quantan_db' and all dummy data initialized successfully!")
