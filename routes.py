from flask import render_template, url_for, request, redirect, session
from flask import render_template, url_for, request, redirect, session

from application import app
from application.register_customer import register_customer, check_customerdetails, get_db_connection
import datetime


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/aboutus')
def welcome():
    return render_template('aboutus.html',title = 'About Us')

@app.route('/founders')
def founders():
    return render_template('founders.html', title='Founders')


@app.route('/menu')
def menu():
    return render_template('menu.html', title='Menu')


@app.route('/locations')
def locations():
    return render_template('locations.html', title='Locations')

@app.route('/productofthemonth')
def productofthemonth():
    return render_template('productofthemonth.html', title='Product of the Month')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('first_name')
        lastname = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not firstname or not lastname or not email or not password:
            return "All fields are required!"

        if register_customer(username, firstname, lastname,email, password):
            return f"User {username} registered successfully!"
        else:
            return "Username or email already exists"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error = "Please fill in all fields."
            return render_template('login.html', error=error)

        if check_customerdetails(username, password):
            # Redirect with username in URL
            return redirect(url_for('contact', username=username))
        else:
            error = "Incorrect Username or Password."

    return render_template('login.html', error=error)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Get username from the URL if coming via redirect
    username = request.args.get('username')

    if request.method == 'POST':
        # On form submit, get from hidden field
        username = request.form.get('username')
        subject_id = request.form.get('subject_id')
        message = request.form.get('message')
        date = datetime.date.today()

        if not username:
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (username,))
        user_result = cursor.fetchone()

        cursor.execute("SELECT subject_id FROM subjects WHERE subject_description = %s", (subject_id,))
        subject_result = cursor.fetchone()

        if user_result and subject_result:
            customer_id = user_result['customer_id']
            subject_id = subject_result['subject_id']

            insert_query = """
                INSERT INTO contactus (username, subject_id, message, date, customer_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (username, subject_id, message, date, customer_id))
            conn.commit()
            return "Thanks for getting in touch!"
        else:
            if not user_result:
                return "User not found"
            if not subject_result:
                return "subject not found"

    return render_template('contact.html', username=username)


# Logout route
@app.route('/logout')
def logout():
    return redirect(url_for('logout_confirmation'))  # Redirect to logout confirmation page

# Logout confirmation route (to show that the user has logged out)
@app.route('/logout_confirmation')
def logout_confirmation():
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)


























# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     error = ""
#     register_form = RegisterForm()
#
#     if request.method == 'POST':
#         username = register_form.username.data
#         first_name = register_form.first_name.data
#         last_name = register_form.last_name.data
#         email = register_form.email.data
#         password = register_form.password.data
#
#         if len(username) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(password) == 0:
#             error = 'Please supply all details'
#         # include others
#         else:
#             people.append({'Username': username, 'Firstname': first_name, 'Lastname': last_name, 'Email': email, 'Password': password})
#             add_person(username, first_name, last_name, email, password)
#             return redirect(url_for('newjoincommunitypage'))
#
#     return render_template('register.html', form=register_form, title='Add Person', message=error)

@app.route('/newjoincommunitypage')
def newjoincommunitypage():
    if 'username' in session:
        username = session['username']
        return render_template('newjoincommunitypage.html', username=username, title='Community Page')
# add a notification of success

@app.route('/login', methods=['GET', 'POST'])
def login():
    # app.logger.debug("Start of login")
    if request.method == 'POST':
        session['username'] = request.form['username']
        # app.logger.debug("Username is: " + session['username'])
        session['loggedIn'] = True
        session['role'] = 'admin'
        return redirect(url_for('communitypage'))
    return render_template('loginfailed.html', username=False, title='Login Failed')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))


@app.route('/adminlogin')
def adminlogin():
    if 'username' in session:
        username = session['username']
        return render_template('adminlogin.html', username=username, title='Admin Login')
    return render_template('adminlogin.html', username=False, title='Admin Login')


@app.route('/adminviewsubmissions', methods=['GET', 'POST'])
def adminviewsubmissions():
    # select username
    if 'username' in session:
        username = session['username']
        print('You are logged in as Admin')
        print(username)
        return render_template('adminviewsubmissions.html', username=username, title='View Submissions')
    return render_template('adminlogin.html', username=False, title='Admin Login')


@app.route('/communitypage')
def communitypage():
    if 'username' in session:
        username = session['username']
        return render_template('communitypage.html', username=username, title='Community Page')
    return render_template('incorrectdetails.html', username=False, title='Wrong credentials')

@app.route('/loginfailed', methods=['GET', 'POST'])
def loginfailed():
    # app.logger.debug("Start of login")
    if request.method == 'POST':
        session['username'] = request.form['username']
        # app.logger.debug("Username is: " + session['username'])
        session['loggedIn'] = True
        session['role'] = 'admin'
        return redirect(url_for('adminviewsubmissions'))
    return render_template('loginfailed.html', title="Login Failed")
# how do we display the login failed message?




