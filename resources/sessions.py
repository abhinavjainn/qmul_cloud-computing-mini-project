import hashlib
import uuid

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
    def post(username, password):
        data = Login.parser.parse_args()

        # Hashed Password
        hash = hashlib.new('ripemd160')
        hashed_pswd=hash.update(data['password'].encode("utf-8"))

        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return {"message": "Username or Password is incorrect"}
        elif hashed_pswd.hexdigest() != user.password:
            return{"message" : "Username or Password is incorrect"}
        else:
            session_id = str(uuid.uuid4())
            return {"message" : "User successfully logged in and the Session id :{}".format(session_id)}
       
       # Save Session_id to DB
        session_id = SessionModel(data["username"],data["sid"],data["status"])
        print("Status : Active Session ID")
        session_id.save_to_db()
        

    






