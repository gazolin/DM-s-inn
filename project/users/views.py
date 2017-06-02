from project import app, db
from project.models import User, bcrypt
from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint 
from functools import wraps
from forms import LoginForm

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

##############
####routes####
##############################

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(User.name == request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['name'] = user.name
                session['first'] = False
                session['id'] = user.id
                return redirect(url_for('home.dm_bar'))
                
        else:
             error = 'Invalid Credentials. Please try again.'  

    return render_template('login.html', form=form, error=error)

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(User.name == request.form['username']).first()
            if user is not None:
                error = 'Name already exists. Please pick another.'
        else: 
            user = User(request.form.get('username'), request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            query = db.session.query(User).filter(User.name.in_([request.form['username']]), User.password.in_([request.form['password']]) )
            session['logged_in'] = True
            session['name'] = request.form['username']
            session['first'] = True
            session['id'] = str(user)
            flash('Welcome ' + request.form['username'])
            flash('It was everyones first time once. ~WinK~')
 
            return redirect(url_for('home.dm_bar'))

    return render_template('signup.html', error=error)

@users_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    flash('You were just logged out!')
    return redirect(url_for('home.welcome'))