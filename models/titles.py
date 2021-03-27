from db import db
from models.users import UserModel

class TitlesModel(db.Model):
    __tablename__ = 'titles'

    listname = db.Column(db.String(20), db.ForeignKey(UserModel.listname, primary_key=True))
    title = db.Column(db.String(50), primary_key=True)
    remarks = db.Column(db.String(80))

    def __init__(self, listname, title, remarks):
        self.listname = listname
        self.title = title
        self.remarks = remarks

    def json(self):
        return {'title': self.title}

    @classmethod
    def find_by_listname(cls,listname):
        return cls.query.filter_by(listname=listname).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()