from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#create the application object
app = Flask(__name__)

bcrypt = Bcrypt(app)

#config
app.config.from_object('config.BaseConfig')
#create the sqlalchemy object
db = SQLAlchemy(app)

from project.users.views import users_blueprint

#register our blueprints
app.register_blueprint(users_blueprint)
