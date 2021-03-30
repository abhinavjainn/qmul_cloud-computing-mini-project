
from db import db
from models.users import UserModel

class SessionModel(db.Model):
    __tablename__ = 'sessions'

    username  = db.Column(db.String(20),db.ForeignKey(UserModel.username),primary_key=True)
    sid = db.Column(db.String(36), primary_key=True)
    status = db.Column(db.String(10))

    def __init__(self, username, sid, status):
        self.username  = username
        self.sid = sid
        self.status = status


    def json(self):
        return {'sid': self.sid}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_sid(cls, sid):
        return cls.query.filter_by(sid=sid).first()

    @classmethod
    def find_by_user_sid(cls, username, sid):
        return cls.query.filter_by(username=username,sid=sid).first()

    @classmethod
    def find_by_user_sid_status(cls, username, sid, status):
        return cls.query.filter_by(username = username, sid = sid, status = status).first()        
