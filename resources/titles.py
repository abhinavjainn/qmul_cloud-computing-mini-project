
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.titles import TitlesModel
from models.sessions import SessionModel
from models.users import UserModel
from flask import jsonify
import json
import requests
import requests_cache
# user, session id, title, remarks


class Browse(Resource):

    def get(self, title):
        url_template = "http://api.tvmaze.com/search/shows?q={title}"
        url = url_template.format(title=title)
        resp = requests.get(url)
        if resp.ok:
            if resp.text == "[]":
                return {"message": "Title not found, please check the spellings and separators carefully."}, 404
            return jsonify(resp.json())
        else:
            return {"message": "Title not found"}, 404


# class CreateList(Resource):
#     parser = reqparse.RequestParser()

#     parser.add_argument('username',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )

#     parser.add_argument('sid',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )

#     parser.add_argument('listname',
#                         type=str,
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
#                         required=False,
#                         help="This field cannot be left blank!"
#                         )

#     def post(self):
#         data = CreateList.parser.parse_args()

#         # Check if user session is valid, if user doesn't have a valid active session => Error
#         if SessionModel.find_by_user_sid_status(
#                 username=data['username'],sid=data['sid'],status='Active') == None:
#             return {'message': 'Invalid session ID'}, 404

#         # Check if a list already exists for the user
#         if UserModel.find_by_user_and_list(data['username'], data["listname"]):
#             return {"message": "A listname already exists for the user"}, 400

#         # Check if listname already exists
#         if TitlesModel.find_by_listname(listname=data['listname']):
#             return {"message": "Listname already selected, please select a different list name"}, 403

#         # Save data to DB
#         titles = TitlesModel(data["listname"], data["title"], data["remarks"])
#         titles.save_to_db()
#         return {'message': 'List created successfully'}, 201


class AddToList(Resource):
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

    def put(self):
        data = AddToList.parser.parse_args()
        # Check if user session is valid, if user doesn't have a valid active session => Error
        if SessionModel.find_by_user_sid_status(
                username=data['username'],sid=data['sid'],status='Active') == None:
            return {'message': 'Invalid session ID'}, 403

        # Check if list name is valid for the user
        if UserModel.find_by_user_and_list(username=data['username'],listname=data['listname']) == None:
            return {'message': 'Invalid list name for the user'}, 403

        # Add new title to list if title doesn't exit, if exists then return error    
        if TitlesModel.find_by_listname_title(listname=data['listname'], title=data['title']) == None:
            item = TitlesModel(listname = data["listname"], title = data["title"], remarks = data["remarks"])
            item.save_to_db()
            return {'message': 'Title added successfully'}, 201
        else:
            return {"message" : "Title already exists" }, 403    


class DeleteFromList(Resource):
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

    def delete(self):
        data = DeleteFromList.parser.parse_args()

        # Check if user session is valid, if user doesn't have a valid active session => Error
        if SessionModel.find_by_user_sid_status(
                username=data['username'],sid=data['sid'],status='Active') == None:
            return {'message': 'Invalid session ID'}, 403

        # Check if list name is valid for the user
        if UserModel.find_by_user_and_list(username=data['username'],listname=data['listname']) == None:
            return {'message': 'Invalid list name for the user'}, 403

        # Check if title to be deleted exists, if not then return error
        if TitlesModel.find_by_listname_title(listname=data['listname'],title=data['title']) == None:
            return {'message': 'The requested title does not exist in the list'}, 404

        # Title found, Delete title from list
        title = TitlesModel.find_by_listname_title(listname = data['listname'], title= data['title'])
        title.delete_from_db()
        return {'message': 'Title has been deleted from the list'}, 200


# class DeleteList(Resource):
#     parser = reqparse.RequestParser()

#     parser.add_argument('username',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     parser.add_argument('sid',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     parser.add_argument('listname',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )

#     def delete(self):
#         data = DeleteList.parser.parse_args()

#         # Check if user session is valid, if user doesn't have a valid active session => Error
#         if SessionModel.find_by_user_sid_status(
#                 username=data['username'],sid=data['sid'],status='Active') == None:
#             return {'message': 'Invalid session ID'}, 404

#         # Check if list to be deleted exists, if not then return an error message
#         if UserModel.find_by_user_and_list(
#             username=data['username'],listname=data['listname']) == None:
#             return {'message': 'The list to be deleted does not exist for the user'}, 400

#         # Delete the list
#         title = TitlesModel(listname = data['listname'], title=data['title'])    
#         title.delete_from_db()
#        # Update user table by removing the list reference
#         user = UserModel.find_by_username(data['username'])
#         user.listname = ""
#         user.update_db()          
#         return {'message': 'List has been deleted successfully'}, 200
   
class ViewList(Resource):

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

    def get(self):
        data = ViewList.parser.parse_args()
        # Check if user session is valid, if user doesn't have a valid active session => Error
        if SessionModel.find_by_user_sid_status(
                username=data['username'],sid=data['sid'],status='Active') == None:
            return {'message': 'Invalid session ID'}, 403

        # Check if list name is valid for the user
        if UserModel.find_by_user_and_list(username=data['username'],listname=data['listname']) == None:
            return {'message': 'Invalid list name for the user'}, 403    

        # Return all titles
        return {'titles': [x.json() for x in TitlesModel.find_by_listname_all(listname=data['listname'])]}