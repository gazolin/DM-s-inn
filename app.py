from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

#create the application object
app = Flask(__name__)

#config
app.config.from_object('config.BaseConfig')

#create the sqlalchemy object
db = SQLAlchemy(app)

from models import *

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        if request.form['firstButton'] == "Enter my page":
            return redirect(url_for('login'))
        elif request.form['firstButton'] == "Create my User!":
            return redirect(url_for('signup'))

    elif request.method == 'GET':
	   return render_template("welcome.html") # render a template

@app.route('/dm_bar', methods=['GET', 'POST'])
@login_required
def dm_bar():
    flash('Welcome ' + session['name'] + '!')
    if request.method == 'POST':
        if request.form['logout'] == "Logout":
            return redirect(url_for('logout'))

    elif request.method == 'GET':
       return render_template("dm_bar.html") # render a template
    

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
 
    error = None
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        query = db.session.query(User).filter(User.name.in_( [POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
        if (query.first() == None):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['name'] = POST_USERNAME
            return redirect(url_for('dm_bar'))

    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        query = db.session.query(User).filter(User.name.in_([POST_USERNAME])) 
        if (query.first() != None):
            error = 'Name already exists. Please pick another.'
        else: 
            user = User(request.form.get('username'), request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            session['logged_in'] = True
            flash('Welcome ' + POST_USERNAME)
            flash('It was everyones first time once. ~WinK~')
 
            return redirect(url_for('dm_bar'))

    return render_template('signup.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

#start the server with the 'run()' method
if __name__ == '__main__':
	app.run(debug=True)
