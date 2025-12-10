import mysql.connector
from mysql.connector import errorcode

db_config = {
    'host': '192.168.31.236',
    'user': 'Anurag', 
    'password': 'Anurag@123' 
}

DB_NAME = 'quiz_app'

TABLES = {}
TABLES['attempts'] = (
    "CREATE TABLE `attempts` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `test_id` varchar(255) NOT NULL,"
    "  `student_name` varchar(255) NOT NULL,"
    "  `score` int(11) NOT NULL,"
    "  `total_questions` int(11) NOT NULL,"
    "  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

cnx = None
try:
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    try:
        cursor.execute(f"USE {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Database {DB_NAME} does not exist.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print(f"Database {DB_NAME} created successfully.")
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()
    print("Database setup completed successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
