from app import app
from db import db

db.init_app(app)

 
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@app.before_first_request
def create_tables():
	db.create_all()
