from project import db

db.create_all()

# commit the changes
db.session.commit()

