import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash


class UserResource(Resource): # this is a flask resource, needs a different name

	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help="username field cannot be left blank!")
	parser.add_argument('password', type=str, required=True, help="password field cannot be left blank!")
	parser.add_argument('first_name', type=str, required=True, help="first_name field cannot be left blank!")
	parser.add_argument('last_name', type=str, required=True, help="last_name field cannot be left blank!")
	parser.add_argument('email_address', type=str, required=True, help="email_address field cannot be left blank!")

	def post(self):

		data = UserResource.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {"message": "User already exists."}, 400

		password_hash = generate_password_hash(data['password'])
		print(password_hash)

		user = UserModel(data['username'], password_hash, data['first_name'], data['last_name'], data['email_address'])
		user.save_to_db()

		return {"message": "User created successfully."}, 201


	@jwt_required()
	def put(self):

		data = UserResource.parser.parse_args()

		user = UserModel.find_by_username(data['username'])

		if (current_identity.username == data['username']):
			if user is None:
				user = UserModel(**data)
				user.save_to_db()
				return {"message": "User created successfully."}, 201
			else:
				user.password = data['password']
				user.save_to_db();
				return {"message": "User password updated."}, 400
		else:
				return {"message": "You can only update your own user: '{}'.".format(current_identity.username)}, 403

	@jwt_required()
	def get(self):
		return {"user": current_identity.json()}, 200
