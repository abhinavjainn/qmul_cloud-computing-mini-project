
import sqlite3
from db import db

class AdminModel(db.Model):
    __tablename__ = 'admin'

    adminid  = db.Column(db.String(40), primary_key=True)

    def __init__(self):
        self.adminid = "34fce8e54af2a418da63ce05b265cc8ea98cc1ef"
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_id(cls):
        return cls.query.filter_by().first().adminid