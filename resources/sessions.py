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
    def post(self):
        print("post triggered")
        data = Login.parser.parse_args()

        # Hashed Password
        o_hash = hashlib.new('ripemd160')
        o_hash.update(data['password'].encode("utf-8"))

        user = UserModel.find_by_username(username=data['username'])
        if user is None:
            return {"message": "Username or Password is incorrect"}, 401
        elif o_hash.hexdigest() != user.password:
            return{"message": "Username or Password is incorrect"}, 401
        else:
            session_id = str(uuid.uuid4())
        #   Save Session_id to DB
            session = SessionModel(username=data['username'],sid=session_id,status="Active")
            session.save_to_db()
            return {"message" : "User successfully logged in.",
                    "sid" : session_id}, 201

# Logout User
class Logout(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username cannot be blank."
                        )
    parser.add_argument('sid',
                        type=str,
                        required=True,
                        help="sid cannot be blank."
                        )

    def delete(self):
        data = Logout.parser.parse_args()
        session = SessionModel.find_by_user_sid_status(
            sid=data['sid'], status='Active', username=data['username'])
        if session == None:
            return {'message': 'No active session found'}, 404
        else:
            session.delete_from_db()
            return {'message': 'User logged out!'}, 200
