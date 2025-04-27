import mysql.connector
import bcrypt
# import pymysql
# from pymysql.err import IntegrityError

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="kaasp",
        # cursorclass = pymysql.cursors.DictCursor
    )
# Function to insert a new customer with hashed password
def register_customer(username, first_name, last_name, email, plain_password):
    conn = get_db_connection()
    # cursor = conn.cursor()
    cursor = conn.cursor(dictionary=True)
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
    # Trying to insert a duplicate value in a column with UNIQUE constraint (e.g., username already exists). - IntegrityError PyMySQL
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
    # cursor = conn.cursor()
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

def view_submissions():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "Select query_ID, username, subject_id, message, date, customer_id from contactus"
    cursor.execute(sql)

    result_set = cursor.fetchall()
    submission_list = []
    for submission in result_set:
        submission_list.append(submission)
    return submission_list


# from flask import render_template, url_for, request, redirect, session
#
# from application import app
# from application.register_customer import register_customer, check_customerdetails, get_db_connection
# import datetime
#
#
# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template('home.html', title='Home')
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         firstname = request.form.get('first_name')
#         lastname = request.form.get('last_name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#
#         if not username or not firstname or not lastname or not email or not password:
#             return "All fields are required!"
#
#         if register_customer(username, firstname, lastname,email, password):
#             return f"User {username} registered successfully!"
#         else:
#             return "Username or email already exists"
#
#     return render_template('register.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         if not username or not password:
#             error = "Please fill in all fields."
#             return render_template('login.html', error=error)
#
#         if check_customerdetails(username, password):
#             # Redirect with username in URL
#             return redirect(url_for('contact', username=username))
#         else:
#             error = "Incorrect Username or Password."
#
#     return render_template('login.html', error=error)
#
#
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     # Get username from the URL if coming via redirect
#     username = request.args.get('username')
#
#     if request.method == 'POST':
#         # On form submit, get from hidden field
#         username = request.form.get('username')
#         subject_id = request.form.get('subject_id')
#         message = request.form.get('message')
#         date = datetime.date.today()
#
#         if not username:
#             return redirect(url_for('login'))
#
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#
#         cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (username,))
#         user_result = cursor.fetchone()
#
#         cursor.execute("SELECT subject_id FROM subjects WHERE subject_description = %s", (subject_id,))
#         subject_result = cursor.fetchone()
#
#         if user_result and subject_result:
#             customer_id = user_result['customer_id']
#             subject_id = subject_result['subject_id']
#
#             insert_query = """
#                 INSERT INTO contactus (username, subject_id, message, date, customer_id)
#                 VALUES (%s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_query, (username, subject_id, message, date, customer_id))
#             conn.commit()
#             return "Thanks for getting in touch!"
#         else:
#             if not user_result:
#                 return "User not found"
#             if not subject_result:
#                 return "subject not found"
#
#     return render_template('contact.html', username=username)
#
#
# # Logout route
# @app.route('/logout')
# def logout():
#     return redirect(url_for('logout_confirmation'))  # Redirect to logout confirmation page
#
# # Logout confirmation route (to show that the user has logged out)
# @app.route('/logout_confirmation')
# def logout_confirmation():
#     return render_template('logout.html')
