from app import db
from models import Users

#create the database and the db tables
db.create_all()

#insert


#commit the changes
db.session.commit()