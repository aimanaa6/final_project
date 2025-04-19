from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Hardcoded admin credentials
admin_username = 'admin'
admin_password_hashed = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', title='About Us')

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

if __name__ == '__main__':
    app.run(debug=True)





























