from app import db
from models import Users

#create the database and the db tables
db.create_all()

#insert
db.session.add(Users("admin", "admin"))
db.session.add(Users("uri", "1234"))

#commit the changes
db.session.commit()