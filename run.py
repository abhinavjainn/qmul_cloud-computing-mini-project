from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    from models.admin import AdminModel
    db.create_all()
    if AdminModel.get_id() == None:  #comment for local execution
        AdminModel().save_to_db()    #Unindent for local execution