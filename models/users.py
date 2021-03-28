
from db import db
from models.admin import AdminModel
import hashlib
from werkzeug.security import safe_str_cmp

class UserModel(db.Model):
    __tablename__ = 'users'

    username  = db.Column(db.String(20), primary_key=True)
    password  = db.Column(db.String(20))    
    firstname = db.Column(db.String(30))
    lastname  = db.Column(db.String(30))
    country   = db.Column(db.String(20))
    listname  = db.Column(db.String(20))
    role      = db.Column(db.String(10))

    def __init__(self, username, password, firstname, lastname, country, listname, role, adminkey):
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
    def find_by_user_and_list(cls,username,listname):
        return cls.__qualname__filter_by(username=username,listname=listname).first()

    @classmethod    
    def check_admin_code(cls,admincodein):
        o_hash = hashlib.new('ripemd160')
        o_hash.update(admincodein.encode("utf-8"))
        if safe_str_cmp(AdminModel.get_id(), o_hash.hexdigest()) == True:    
            return True
        else:
            return False       