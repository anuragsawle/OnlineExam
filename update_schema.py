import mysql.connector
from mysql.connector import errorcode

db_config = {
    'host': '192.168.31.236',
    'user': 'Anurag', 
    'password': 'Anurag@123',
    'database': 'quiz_app'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Add column if it doesn't exist
    print("Adding student_class column...")
    try:
        cursor.execute("ALTER TABLE attempts ADD COLUMN student_class VARCHAR(50) AFTER student_name")
        print("Column 'student_class' added successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_FIELDNAME:
            print("Column 'student_class' already exists.")
        else:
            print(f"Error adding column: {err}")
    
    conn.commit()
    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Connection failed: {err}")
