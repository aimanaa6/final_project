import mysql.connector
import bcrypt

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kaasp"
    )

# Function to insert a new customer with hashed password
def register_customer(username, first_name, last_name, email, plain_password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    sql = """
        INSERT INTO customers (username, first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (username, first_name, last_name,email, hashed.decode('utf-8'))

    try:
        cursor.execute(sql, values)
        conn.commit()
        return True
    # Trying to insert a duplicate value in a column with UNIQUE constraint (e.g., username already exists).
    except mysql.connector.IntegrityError:
        return False
    # This block always runs, whether an error happened or not.
    finally:
        cursor.close()
        conn.close()


# Login with hashed password
def check_customerdetails(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM customers WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # Check if user exists and password matches
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return True
    else:
        return False