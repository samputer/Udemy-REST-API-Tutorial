from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity # our other file
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This turns off the flask sqlalchemy modification tracker, and uses the SQLalchemy one instead
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity) # this creates /auth endpoint that we pass a username and password to, this then uses the authenticate function

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__': # this prevents running on import, as opposed to when executing directly
	from db import db # importing thi here prevents multiple libs importing the same thing
	db.init_app(app)
	app.run(port=5000, debug=True)