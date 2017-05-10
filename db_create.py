from app import db
from models import User

#create the database and the db tables
db.create_all()

#insert
db.session.add(User("admin", "admin"))
db.session.add(User("uri", "1234"))

#commit the changes
db.session.commit()