
from db import db
from models.admin import AdminModel
import hashlib

class UserModel(db.Model):
    __tablename__ = 'users'

    username  = db.Column(db.String(20), primary_key=True)
    firstname = db.Column(db.String(30))
    lastname  = db.Column(db.String(30))
    country   = db.Column(db.String(20))
    listname  = db.Column(db.String(20))
    role      = db.Column(db.String(10))
    password  = db.Column(db.String(20))

    def __init__(self, username, firstname, lastname, country, listname, role, password):
        self.username  = username
        self.password  = password
        self.firstname = firstname
        self.lastname  = lastname
        self.country   = country
        self.listname  = listname
        self.role      = role
        self.admincode = ""

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    @classmethod    
    def check_admin_code(cls,admincodein):
        o_hash = hashlib.new('ripemd160')
        o_hash.update(admincodein.encode("utf-8"))
        if o_hash.hexdigest() == AdminModel.get_id():
            return True
        else:
            return False       