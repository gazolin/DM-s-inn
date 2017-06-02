from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint 
from app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from functools import wraps

users_blueprint = Blueprint(
	'users', __name__,
	template_folder='templates'
)


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

####routes####

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        userName = str(request.form['username'])
        password = str(request.form['password'])
        query = db.session.query(User).filter(User.name.in_([userName]), User.password.in_([password]) )
        if (query.first() == None):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['name'] = userName
            session['first'] = False
            session['id'] = str(query.first())
            return redirect(url_for('dm_bar'))

    return render_template('login.html', error=error)

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        userName = str(request.form['username'])
        password = str(request.form['password'])
        query = db.session.query(User).filter(User.name.in_([userName])) 
        if (query.first() != None):
            error = 'Name already exists. Please pick another.'
        else: 
            user = User(request.form.get('username'), request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            query = db.session.query(User).filter(User.name.in_([userName]), User.password.in_([password]) )
            session['logged_in'] = True
            session['name'] = userName
            session['first'] = True
            session['id'] = str(query.first())
            flash('Welcome ' + userName)
            flash('It was everyones first time once. ~WinK~')
 
            return redirect(url_for('dm_bar'))

    return render_template('signup.html', error=error)

@users_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))