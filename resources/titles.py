
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.titles import TitlesModel
from models.sessions import SessionModel
from models.users import UserModel
from flask import jsonify
import json
import requests, requests_cache
# user, session id, title, remarks


class Browse(Resource):

    def get(self, title):
        url_template = "http://api.tvmaze.com/search/shows?q={title}"
        url = url_template.format(title = title)
        resp = requests.get(url)
        if resp.ok:
            if resp.text == "[]":
                return {"message": "Title not found, please check the spellings and separators carefully."}, 404
            return jsonify(resp.json())
        else:
            return {"message": "Title not found"}, 404      

class CreateList(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('sid',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )    

    parser.add_argument('listname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('remarks',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )                        
    def post(self):
        data = CreateList.parser.parse_args()     
#       Check if user session is valid
            # TBD####
#       Check if user already has a list, if yes => error
        if UserModel.find_by_user_and_list(data['username'],data["listname"]):
            return {"message": "A listname already exists for the user"}, 400    

        # Save data to DB
        titles = TitlesModel(data["listname"],data["title"],data["remarks"])
        titles.save_to_db()



# class Title(Resource):
#     parser = reqparse.RequestParser()

#     parser.add_argument('username',
#                         type=String,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )

#     parser.add_argument('sid',
#                         type=Str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     parser.add_argument('title',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     parser.add_argument('remarks',
#                         type=str,
#                         required=True,
#                         help="Please give remarks."
#                         )

#     # @jwt_required()
#     # user, session id
#     def get(self, listname):
#         data = Title.parser.parse_args()
#         item = TitlesModel.find_by_listname(listname)
#         if len(item) == 0:
#             return {"error": 'Title name not found'}, 404
#         else:
#             if SessionModel.find_by_sid(data['sid']) and UserModel.find_by_username(data['username']):
#                 return item  # .jason()

#     # replace multiple time not allowed!
#     def post(self, listname):
#         data = Title.parser.parse_args()
#         item = TitlesModel.find_by_listname(listname)

#         if TitlesModel.find_by_listname(item):
#             return {'message': "A title with listname '{}' already exists.".format(item)}, 400

#         item = TitlesModel(listname, **data)

#         try:
#             item.save_to_db()
#         except:
#             return {"message": "An error occurred inserting the title."}, 500

#         return item.json(), 201
#     # delete item from list: user, session id, title

#     def delete(self, litsname):
#         item = TitlesModel.find_by_name(listname)

#         if titles:
#             item.delete_from_db()

#         return {'message': 'Title deleted'}

#     # add item to list: user, session id, title
#     # replace multiple time no problem! hence idempotent
#     def put(self, listname):
#         data = Title.parser.parse_args()
#         item = TitlesModel.find_by_name(listname)
#         #sess = SessionModel.find_by_sid()

#         if item is None:
#             item = TitlesModel(listname, **data)
#         else:
#             item.listname = data['listname']
#             item.remarks = data['remarks']
#             item.title = data['title']

#         item.save_to_db()

#         return item.json()


# class TitlesList(Resource):
#     def get(self):
#         return {'titles': [x.json() for x in TitlesModel.query.all()]}
