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
		return '<User %r>' % (self.id)


class World(db.Model):

	__tablename__ = "world"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	charCount = db.Column(db.Integer, nullable=False)
	#creationTime = db.Column(db.DateTime, onupdate=datetime.datetime.now)

 	def __repr__(self):
		return '<World %r>' % (self.name)



	def __init__(self, user_id, name, description, charCount):
		self.user_id = user_id
		self.name = name
		self.description = description
		self.charCount = charCount
		#self.creationTime = creationTime

class Character(db.Model):

	__tablename__ = "character"

	id = db.Column(db.Integer, primary_key=True)
	world_id = db.Column(db.Integer, ForeignKey('world.id'))
	name = db.Column(db.String, nullable=False)
	char_class = db.Column(db.String, nullable=False)
	backgroundStory = db.Column(db.String, nullable=False)


	def __init__(self, world_id, name, char_class, backgroundStory):
		self.world_id = world_id
		self.name = name
		self.char_class = char_class
		self.backgroundStory = backgroundStory

class Story(db.Model):

	__tablename__ = "story"

	id = db.Column(db.Integer, primary_key=True)
	world_id = db.Column(db.Integer, ForeignKey('world.id'))	
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	events = db.Column(db.String, nullable=False)
	


	def __init__(self, user_id, name, decription, events):
		self.user_id = user_id
		self.name = name
		self.description = description
		self.events = events
		
