from db import db
import sqlite3

class UserModel(db.Model):

	# Table
	__tablename__ = 'users'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	email_address = db.Column(db.String(80))

	def __init__(self, username, password, first_name, last_name, email_address):
		self.username = username
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.email_address = email_address

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def json(self):
		return {'username':self.username, 'first_name':self.first_name, 'last_name': self.last_name, 'email_address': self.email_address}

	def limited_json(self):
		return {'first_name':self.first_name}

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()
		