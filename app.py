from functools import wraps
import sys
import os
import pyrebase
from flask import *

config = {
  "apiKey": "",
  "authDomain": "doc-checker.firebaseapp.com",
  "databaseURL": "https://doc-checker.firebaseio.com",
  "projectId": "doc-checker",
  "storageBucket": "",
  "messagingSenderId": "586419082384",
  "appId": "1:586419082384:web:a10c1f28960e3f00ee7415",
  "measurementId": "G-8YGVD4P971"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
app.secret_key = os.urandom(24)

#decorator to protect routes
def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #check for the variable that pyrebase creates
        if not auth.current_user != None:
            return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function

#index route
@app.route('/index')
def index():
	if 'email' in session:
  		return render_template('index.html', id=session['email'])
	return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['password']
		try:
			user = auth.sign_in_with_email_and_password(email, password)
			user_id = user['idToken']
			user_email = email
			session['usr'] = user_id
			session['email'] = user_email
			return redirect(url_for('index'))
		except:
			return render_template('login.html', message="Wrong credentials")

	return render_template('login.html')


@app.route('/registration')
def register():
    return render_template('signup.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			auth.create_user_with_email_and_password(email, password)
			user = auth.sign_in_with_email_and_password(email, password)
			user_id = user['idToken']
			user_email = email
			session['usr'] = user_id
			session['email'] = user_email
			return redirect('/index')
		except:
			return render_template('login.html', message="This email is already taken")
	return render_template('signup.html')

#logout route
@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None
    #also remove the session
    #session['usr'] = ""
    #session["email"] = ""
    session.clear()
    return redirect("/");


#profile route
@app.route('/profile')
def profile():
	if 'email' in session:
  		return render_template('profile.html', id=session['email'])
	return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)




























