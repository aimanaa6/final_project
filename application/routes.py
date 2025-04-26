from flask import render_template, url_for, request, redirect, session
import bcrypt
from application import app
from application.register_customer import register_customer, check_customerdetails, get_db_connection, view_submissions
import datetime

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome to Kaasp Bakery')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', title='Our Story')

@app.route('/admin')
def admin_dashboard():
    if session.get('admin'):
        return "Welcome to the admin dashboard!"  # Replace with render_template for your real admin page
    return redirect(url_for('adminviewsubmissions'))

@app.route('/founders')
def founders():
    return render_template('founders.html', title='Founders')

@app.route('/menu')
def menu():
    return render_template('menu.html', title='Our Menu')

@app.route('/locations')
def locations():
    return render_template('locations.html', title='Locations')

@app.route('/featuredproduct')
def featuredproduct():
    return render_template('featuredproduct.html', title='Product of the Month')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('first_name')
        lastname = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not firstname or not lastname or not email or not password:
            error = "All fields are required!"
            return render_template('register.html', error=error)

        if register_customer(username, firstname, lastname, email, password):
            session['username'] = username
            session['show_modal'] = True  # ⚡ Set flag to show modal
            return redirect(url_for('newjoincommunitypage'))
        else:
            error = "Username or email already exists. Please try again."
            return render_template('register.html', error=error)

    return render_template('register.html')


@app.route('/newjoincommunitypage')
def newjoincommunitypage():
    if 'username' in session:
        username = session['username']
        return render_template('newjoincommunitypage.html', username=username, title='Thank You for Joining!')
    else:
        return redirect(url_for('register'))  # 🔥 Important: if no username, go back to register


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password').encode('utf-8')

        # Hardcoded admin credentials
        admin_username = 'admin'
        admin_password = 'admin123'
        admin_password_hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())


        if username == admin_username and bcrypt.checkpw(password, admin_password_hashed):
            session['username'] = username
            session['admin'] = True
            return redirect(url_for('adminviewsubmissions'))

        if check_customerdetails(username, password.decode('utf-8')):
            session['username'] = username
            session.pop('admin', None)
            return redirect(url_for('community_page'))

        error = 'Incorrect username or password.'

    return render_template('login.html', error=error)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Handle form submission
    if request.method == 'POST':
        # Check if logged in
        if 'username' not in session:
            # Save form data in session to repopulate later
            session['contact_form_data'] = {
                'subject_id': request.form.get('subject_id'),
                'message': request.form.get('message')
            }
            return redirect(url_for('login', next=url_for('contact')))

        # Process form for logged-in users
        username = session['username']
        subject_id = request.form.get('subject_id')
        message = request.form.get('message')
        date = datetime.date.today()

        conn = get_db_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                # Get user and subject info
                cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (username,))
                user_result = cursor.fetchone()

                cursor.execute("SELECT subject_id FROM subjects WHERE subject_description = %s", (subject_id,))
                subject_result = cursor.fetchone()

                if not user_result:
                    return "User not found", 404
                if not subject_result:
                    return "Subject not found", 404

                # Insert message
                insert_query = """
                    INSERT INTO contactus (username, subject_id, message, date, customer_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    username,
                    subject_result['subject_id'],
                    message,
                    date,
                    user_result['customer_id']
                ))
                conn.commit()

                # Clear saved form data
                session.pop('contact_form_data', None)

                # Set modal flag in session
                session['show_modal'] = True

                # Redirect to contact page (so modal can show)
                return redirect(url_for('contact'))
        finally:
            conn.close()

    # If GET, just render the page
    return render_template('contact.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))

@app.route('/adminviewsubmissions', methods=['GET', 'POST'])
def adminviewsubmissions():
    if 'username' not in session or not session.get('admin'):
        # If user is not logged in or not an admin, redirect to admin login
        return redirect(url_for('login'))

    username = session['username']
    submission_list_db = view_submissions()
    print(submission_list_db)  # Debugging purpose

    return render_template(
        'adminviewsubmissions.html',
        title='View Submissions',
        current_date=datetime.date.today(),
        contactus=submission_list_db
    )

@app.route('/community_page')
def community_page():
    if 'username' not in session:
        return redirect(url_for('login', next=url_for('community_page')))

    username = session['username']
    return render_template('community_page.html', username=username, title='Community Page')

@app.route('/find_branch', methods=['GET', 'POST'])
def find_branch():
    branches = []
    message = None

    if request.method == 'POST':
        town = request.form.get('town')

        if not town:
            message = "Please enter a town."
        else:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT b.branch_name, b.opening_times, l.location_name
                FROM branches b
                JOIN locations l ON b.location_id = l.location_id
                WHERE LOWER(l.location_name) = LOWER(%s)
            """

            cursor.execute(query, (town,))
            branches = cursor.fetchall()

            if not branches:
                message = f"No branches found in {town.title()}."

    return render_template('find_branch.html', branches=branches, message=message)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500









# PYMYSQL version
# from flask import render_template, url_for, request, redirect, session
# import bcrypt
# from application import app
# from application.register_customer import register_customer, check_customerdetails, get_db_connection
# import datetime
#
# # Hardcoded admin credentials
# admin_username = 'admin'
# admin_password_hashed = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
#
# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template('home.html', title='Welcome to Kaasp Bakery')
#
# @app.route('/aboutus')
# def aboutus():
#     return render_template('aboutus.html', title='Our Story')
#

# @app.route('/admin')
# def admin_dashboard():
#     if session.get('admin'):
#         return "Welcome to the admin dashboard!"  # Replace with render_template for your real admin page
#     return redirect(url_for('adminlogin'))
#
# @app.route('/founders')
# def founders():
#     return render_template('founders.html', title='Founders')
#
# @app.route('/menu')
# def menu():
#     return render_template('menu.html', title='Our Menu')
#
# @app.route('/locations')
# def locations():
#     return render_template('locations.html', title='Locations')
#
# @app.route('/featuredproduct')
# def featuredproduct():
#     return render_template('featuredproduct.html', title='Product of the Month')
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         firstname = request.form.get('first_name')
#         lastname = request.form.get('last_name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         if not username or not firstname or not lastname or not email or not password:
#             return "All fields are required!"
#         if register_customer(username, firstname, lastname, email, password):
#             return f"User {username} registered successfully!"
#         else:
#             return "Username or email already exists"
#     return render_template('register.html')
#
# @app.route('/newjoincommunitypage')
# def newjoincommunitypage():
#     if 'username' in session:
#         username = session['username']
#         return render_template('newjoincommunitypage.html', username=username, title='Community Page')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password').encode('utf-8')
#
#         # Hardcoded admin credentials
#         admin_username = 'admin'
#         admin_password = 'admin123'
#         admin_password_hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
#
#
#         if username == admin_username and bcrypt.checkpw(password, admin_password_hashed):
#             session['username'] = username
#             session['admin'] = True
#             return redirect(url_for('adminviewsubmissions'))
#
#         if check_customerdetails(username, password.decode('utf-8')):
#             session['username'] = username
#             session.pop('admin', None)
#             return redirect(url_for('community_page'))
#
#         error = 'Incorrect username or password.'
#
#     return render_template('login.html', error=error)
#
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     # Handle form submission
#     if request.method == 'POST':
#         # Check if logged in
#         if 'username' not in session:
#             # Save form data in session to repopulate later
#             session['contact_form_data'] = {
#                 'subject_id': request.form.get('subject_id'),
#                 'message': request.form.get('message')
#             }
#             return redirect(url_for('login', next=url_for('contact')))
#
#         # Process form for logged-in users
#         username = session['username']
#         subject_id = request.form.get('subject_id')
#         message = request.form.get('message')
#         date = datetime.date.today()
#
#         conn = get_db_connection()
#         try:
#             with conn.cursor() as cursor:
#                 # Get user and subject info
#                 cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (username,))
#                 user_result = cursor.fetchone()
#
#                 cursor.execute("SELECT subject_id FROM subjects WHERE subject_description = %s", (subject_id,))
#                 subject_result = cursor.fetchone()
#
#                 if not user_result:
#                     return "User not found", 404
#                 if not subject_result:
#                     return "Subject not found", 404
#
#                 # Insert message
#                 insert_query = """
#                     INSERT INTO contactus (username, subject_id, message, date, customer_id)
#                     VALUES (%s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(insert_query, (
#                     username,
#                     subject_result['subject_id'],
#                     message,
#                     date,
#                     user_result['customer_id']
#                 ))
#                 conn.commit()
#
#                 # Clear saved form data
#                 session.pop('contact_form_data', None)
#
#                 # Set modal flag in session
#                 session['show_modal'] = True
#
#                 # Redirect to contact page (so modal can show)
#                 return redirect(url_for('contact'))
#         finally:
#             conn.close()
#
#     # If GET, just render the page
#     return render_template('contact.html')
#
# @app.route('/logout')
# def logout():
#     # remove the username from the session if it is there
#     session.pop('username', None)
#     session.pop('role', None)
#     session['loggedIn'] = False
#     return redirect(url_for('home'))
#
# @app.route('/adminviewsubmissions', methods=['GET', 'POST'])
# def adminviewsubmissions():
#     # select username
#     if 'username' in session:
#         username = session['username']
#         print('You are logged in as Admin')
#         print(username)
#         return render_template('adminviewsubmissions.html', username=username, title='View Submissions')
#     return render_template('adminlogin.html', username=False, title='Admin Login')
#
# @app.route('/community_page')
# def community_page():
#     if 'username' not in session:
#         return redirect(url_for('login', next=url_for('community_page')))
#
#     username = session['username']
#     return render_template('community_page.html', username=username, title='Community Page')
