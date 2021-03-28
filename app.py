import os

from flask import Flask
from flask_restful import Api

from resources.users import UserRegister
from resources.titles import Browse
# from resources.sessions import 

app = Flask(__name__)

# app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'QMUL_CC_T12'
api = Api(app)

api.add_resource(UserRegister, '/register')
api.add_resource(Browse, '/browse/<title>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            from models.admin import AdminModel
            db.create_all()
            AdminModel().save_to_db()

    app.run(host='0.0.0.0')
    # app.run(port=5000)

