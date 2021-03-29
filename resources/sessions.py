import hashlib
import uuid
import sqlite3
from flask_restful import Resource, reqparse
from models.users import UserModel
from models.sessions import SessionModel

# Login user
class Login(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password cannot be blank."
                        )

    # Authenticate User
    def post(self, username, password):
        data = Login.parser.parse_args()

        # Hashed Password
        hash = hashlib.new('ripemd160')
        hashed_pswd = hash.update(data['password'].encode("utf-8"))

        user = UserModel.find_by_username(username=username)
        if user is None:
            return {"message": "Username or Password is incorrect"}
        elif hashed_pswd.hexdigest() != user.password:
            return{"message": "Username or Password is incorrect"}
        else:
            session_id = uuid.uuid4()
            data['sid'] = session_id

        # Save Session_id to DB
            session = SessionModel(**data)
            session.save_to_db()
            return {"message" : "User successfully logged in.",
                    "Session id" : session_id}, 201

# Logout User
class Logout(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username cannot be blank."
                        )
    parser.add_argument('session_id',
                        type=str,
                        required=True,
                        help="Session_id cannot be blank."
                        )

    def delete_user(self):
        data = Logout.parser.parse_args()
        session = SessionModel.find_by_user_sid_status(
            sid=data['session_id'], status='Active', username=data['username'])
        if session == None:
            return {'message': 'No active session found'}, 404
        else:
            session.delete_from_db(**data)
            session.commit()
            return {'message': 'User logged out!'}, 200
