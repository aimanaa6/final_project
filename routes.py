from flask import Flask, render_template, url_for, request, redirect, session
import bcrypt

# from application import app
# from datetime import datetime
# from application.utilities import get_time_of_day
# from application.fake_data import products, people
# import os
# from application.forms.register_form import RegisterForm
# from application.data_access import add_person, get_people

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Hardcoded admin credentials
admin_username = 'admin'
admin_password_hashed = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome to Kaasp Bakery')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', title='Our Story')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if username == admin_username and bcrypt.checkpw(password, admin_password_hashed):
            session['username'] = username
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid admin credentials."

    return render_template('adminlogin.html', title='Admin Login', error=error)

@app.route('/admin')
def admin_dashboard():
    if session.get('admin'):
        return "Welcome to the admin dashboard!"  # Replace with render_template for your real admin page
    return redirect(url_for('adminlogin'))


# ------- THIS IS THE END OF POOJA's ROUTES ----------


@app.route('/founders')
def founders():
    return render_template('founders.html', title='Founders')


@app.route('/menu')
def menu():
    return render_template('menu.html', title='Menu')


@app.route('/locations')
def locations():
    return render_template('locations.html', title='Locations')

@app.route('/featuredproduct')
def featuredproduct():
    return render_template('featuredproduct.html', title='Product of the Month')

people = []


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': username = request.form.get('username')
    firstname = request.form.get('first_name')
    lastname = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    if not username or not firstname or not lastname or not email or not password:
        return "All fields are required!"
    if register_customer(username, firstname, lastname, email, password):
        return f"User {username} registered successfully!"
    else:
        return "Username or email already exists"

    return render_template('register.html')

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



if __name__ == '__main__':
    app.run(debug=True)

