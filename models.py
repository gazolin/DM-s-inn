from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
import datetime

class User(db.Model):

	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self, name, password):
		self.name = name
		self.password = password

	def __repr__(self):
		return '{}-{}'.format(self.name, self.password)


class World(db.Model):

	__tablename__ = "world"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	playersCount = db.Column(db.Integer, nullable=False)
	creationTime = db.Column(db.DateTime, onupdate=datetime.datetime.now)



	def __init__(self, name, password):
		self.user_id = user_id
		self.worldName = worldName
