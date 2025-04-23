import mysql.connector
# import pymysql
# from pymysql.err import IntegrityError
import bcrypt


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kaasp",
        # cursorclass=pymysql.cursors.DictCursor
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
    values = (username, first_name, last_name, email, hashed.decode('utf-8'))

    try:
        cursor.execute(sql, values)
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

def check_customerdetails(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM customers WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return True
    else:
        return False

def view_submissions():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "Select query_ID, username, subject_id, message, date, customer_id from contactus"
    cursor.execute(sql)

    result_set = cursor.fetchall()
    submission_list = []
    for submission in result_set:
        submission_list.append({'query_id': submission[0], 'username': submission[1], 'subject_id': submission[2], 'message': submission[3], 'date': submission[4], 'customer_id': submission[5]})
    return submission_list
