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
#create the database and the db tables
db.create_all()
#commit the changes
db.session.commit()

from project.users.views import users_blueprint

#register our blueprints
app.register_blueprint(users_blueprint)

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
    session.pop('_flashes', None)
    if request.method == 'POST':
        if request.form['firstButton'] == "Enter my page":
            return redirect(url_for('login'))
        elif request.form['firstButton'] == "Create my User!":
            return redirect(url_for('signup'))

    elif request.method == 'GET':
       return render_template("welcome.html") # render a template

##############
####routes####
##################################


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/signup', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))



@app.route('/dm_bar', methods=['GET', 'POST'])
@login_required
def dm_bar():
    if (session['first'] == False):
        flash('Welcome ' + session['name'] + '!')
    if request.method == 'POST':
        if request.form['homeButton'] == "Logout":
            return redirect(url_for('logout'))
        if request.form['homeButton'] == "Create a World":
            return redirect(url_for('world_creation'))
        if request.form['homeButton'] == "My Worlds":
            return redirect(url_for('worlds'))

    elif request.method == 'GET':
        return render_template("dm_bar.html") # render a template


@app.route('/worlds', methods=['GET', 'POST'])
@login_required
def worlds():
    session.pop('_flashes', None)
    if request.method == 'POST':
        if request.form['worldsButton'] == "Logout":
            return redirect(url_for('logout'))

    elif request.method == 'GET':
        worlds = World.query.filter(World.user_id == session['id']).all()
        return render_template("worlds.html", title="Worlds", worlds=worlds)

@app.route('/world_creation', methods=['GET', 'POST'])
@login_required
def world_creation():
    session.pop('_flashes', None)
    if request.method == 'POST':
        worldName = str(request.form['worldName'])
        world_description = str(request.form['worldDescription'])
        world = World(session['id'], request.form.get('worldName'), request.form.get('worldDescription'), 0)
        db.session.add(world)
        db.session.commit()

        #if request.form['worldsButton'] == "worldName":
            #return redirect(url_for('logout'))
        return redirect(url_for('worlds'))

    elif request.method == 'GET':
        return render_template("world_creation.html") # render a template



#start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
