import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity # our other file
from resources.user import UserResource
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask_jwt import JWTError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # allows to default to sqlite for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This turns off the flask sqlalchemy modification tracker, and uses the SQLalchemy one instead
app.config['DEBUG'] = False
app.secret_key = 'jose'
errors = {
    'JWTError': {
        'message': "There was an error with your JWT token (it probably expired).",
        'status': 401,
    }
}

api = Api(app, errors=errors)

jwt = JWT(app, authenticate, identity) # this creates /auth endpoint that we pass a username and password to, this then uses the authenticate function

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserResource, '/user/<string:username>', '/user', endpoint = 'user')

if __name__ == '__main__': # this prevents running on import, as opposed to when executing directly
	from db import db # importing this here prevents multiple libs importing the same thing
	db.init_app(app)
 
 	# This is needed for a dev environment
	if app.config['DEBUG']:
		@app.before_first_request
		def create_tables():
			db.create_all()
 
	app.run(port=5000)
