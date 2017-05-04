from app import db

class Users(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self, name, password):
		self.name = name
		self.password = password

	def __repr__(self):
		return '{}-{}'.format(self.name, self.password)