

from flask import render_template, url_for, request, redirect, session
import bcrypt

import app


@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/aboutus')
def welcome():
    return render_template('aboutus.html', title='About Us')

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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        # Handle the form submission (e.g., save to database, send email, etc.)

        session['show_modal'] = True  # ✅ Set modal trigger for thank_you page
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/newjoincommunitypage')
def newjoincommunitypage():
    if 'username' in session:
        username = session['username']
        return render_template('newjoincommunitypage.html', username=username, title='Community Page')
    return render_template('newjoincommunitypage.html', username=False, title='Community Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ""
    register_form = RegisterForm()

    if request.method == 'POST':
        username = register_form.username.data
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        email = register_form.email.data
        password = register_form.password.data

        if len(username) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(password) == 0:
            error = 'Please supply all details'
        else:
            # Encrypt the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Store the user details with the hashed password
            people.append({
                'Username': username,
                'Firstname': first_name,
                'Lastname': last_name,
                'Email': email,
                'Password': hashed_password
            })

            add_person(username, first_name, last_name, email, hashed_password)

            session['show_modal'] = True  # ✅ Set modal trigger for newjoincommunitypage
            return redirect(url_for('newjoincommunitypage'))

    return render_template('register.html', form=register_form, title='Add Person', message=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['loggedIn'] = True
        session['role'] = 'admin'
        return redirect(url_for('communitypage'))
    return render_template('loginfailed.html', username=False, title='Login Failed')


@app.route('/logout')
def logout():
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
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['loggedIn'] = True
        session['role'] = 'admin'
        return redirect(url_for('adminviewsubmissions'))
    return render_template('loginfailed.html', title="Login Failed")
