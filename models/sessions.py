
import sqlite3
from db import db

class SessionModel(db.Model):
    __tablename__ = 'sessions'

    username  = db.Column(db.String(20), primary_key=True, db.ForeignKey(users.username))
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

    @classmethod
    def find_by_sid(cls, sid):
        return cls.query.filter_by(sid=sid).first()