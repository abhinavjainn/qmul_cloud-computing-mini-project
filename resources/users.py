import sqlite3
from flask_restful import Resource, reqparse
from models.users import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username cannot be blank."
    )
    parser.add_argument('firstname',
        type=str,
        required=False,
        help="First Name."
    )
    parser.add_argument('lastname',
        type=str,
        required=False,
        help="Last Name."
    )
    parser.add_argument('country',
        type=str,
        required=False,
        help="Country"
    )        
    parser.add_argument('listname',
        type=str,
        required=True,
        help="ListName field cannot be blank."
    )    
    parser.add_argument('role',
        type=str,
        required=True,
        help="Role of the user cannot be blank (must be user or admin)."   
    )     
    parser.add_argument('adminkey',
        type=str,
        required=False,
        help="Admin key if the role is admin."          
    )      
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with the given username already exists"}, 400
        if data["role"] == "admin":
            if UserModel.check_admin_code(data["admincode"]) == False:
                return{"Invalid admin code"}, 401
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201