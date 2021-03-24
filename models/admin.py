
import sqlite3
from db import db

class AdminModel(db.Model):
    __tablename__ = 'admin'

    adminid  = db.Column(db.String(40), primary_key=True)

    def __init__(self, username, sid, status):
        self.adminid = "34fce8e54af2a418da63ce05b265cc8ea98cc1ef"

    @classmethod
    def get_id(self):
        return self.adminid