import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash


class UserResource(Resource): # this is a flask resource, needs a different name

	def post(self, username=None):

		parser = reqparse.RequestParser()
		parser.add_argument('username', type=str, required=True, help="username field cannot be left blank!")
		parser.add_argument('password', type=str, required=True, help="password field cannot be left blank!")
		parser.add_argument('first_name', type=str, required=True, help="first_name field cannot be left blank!")
		parser.add_argument('last_name', type=str, required=True, help="last_name field cannot be left blank!")
		parser.add_argument('email_address', type=str, required=True, help="email_address field cannot be left blank!")

		if username is not None:
			return {"message": "Ambiguous username field, please specify username in the JSON payload"}, 400

		data = parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {"message": "User already exists."}, 400

		user = UserModel(data['username'], generate_password_hash(data['password']), data['first_name'], data['last_name'], data['email_address'])
		user.save_to_db()

		return {"message": "User created successfully."}, 201

	@jwt_required()
	def put(self, username=None):

		parser = reqparse.RequestParser()
		parser.add_argument('password', type=str, required=True, help="password field cannot be left blank!")
		parser.add_argument('first_name', type=str, required=True, help="first_name field cannot be left blank!")
		parser.add_argument('last_name', type=str, required=True, help="last_name field cannot be left blank!")
		parser.add_argument('email_address', type=str, required=True, help="email_address field cannot be left blank!")

		data = parser.parse_args()

		# user = UserModel.find_by_username(username)
		user = current_identity
		# if the username passed matches the currently logged in user
		user.password = generate_password_hash(data['password'])
		user.first_name = data['first_name']
		user.last_name = data['last_name']
		user.email_address = data['email_address']
		user.save_to_db()
		return {"message": "User updated."}, 400
		
	@jwt_required()
	def get(self, username=None):
		# if user has requested anyone but their own username
		if ((username is not None) and (username != current_identity.username)):
					user = UserModel.find_by_username(username)
					if user:
						return {"user": user.limited_json()}, 200
					else:
						return {"message": "No user found"}, 400

		return {"user": current_identity.json()}, 200
