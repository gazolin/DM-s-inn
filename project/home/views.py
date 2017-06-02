from project import app, db
from project.models import User, World
from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from functools import wraps

home_blueprint = Blueprint(
    'home', __name__,
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
            return redirect(url_for('users.login'))
    return wrap


##############
####routes####
##################################


@home_blueprint.route('/', methods=['GET', 'POST'])
def welcome():
    session.pop('_flashes', None)
    if request.method == 'POST':
        if request.form['firstButton'] == "Enter my page":
            return redirect(url_for('users.login'))
        elif request.form['firstButton'] == "Create my User!":
            return redirect(url_for('users.signup'))

    elif request.method == 'GET':
       return render_template("welcome.html") # render a template


@home_blueprint.route('/dm_bar', methods=['GET', 'POST'])
@login_required
def dm_bar():
    if (session['first'] == False):
        flash('Welcome ' + session['name'] + '!')
    if request.method == 'POST':
        if request.form['homeButton'] == "Logout":
            return redirect(url_for('users.logout'))
        if request.form['homeButton'] == "Create a World":
            return redirect(url_for('home.world_creation'))
        if request.form['homeButton'] == "My Worlds":
            return redirect(url_for('home.worlds'))

    elif request.method == 'GET':
        return render_template("dm_bar.html") # render a template


@home_blueprint.route('/worlds', methods=['GET', 'POST'])
@login_required
def worlds():
    session.pop('_flashes', None)
    if request.method == 'POST':
        if request.form['worldsButton'] == "Logout":
            return redirect(url_for('users.logout'))

    elif request.method == 'GET':
        worlds = World.query.filter(World.user_id == session['id']).all()
        return render_template("worlds.html", title="Worlds", worlds=worlds)

@home_blueprint.route('/world_creation', methods=['GET', 'POST'])
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
        return redirect(url_for('home.worlds'))

    elif request.method == 'GET':
        return render_template("world_creation.html") # render a template




