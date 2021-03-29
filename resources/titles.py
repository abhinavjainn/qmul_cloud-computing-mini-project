
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
        # Check if user session is valid
        # TBD####
        # Check if user already has a list, if yes => error
        if UserModel.find_by_user_and_list(data['username'], data["listname"]):
            return {"message": "A listname already exists for the user"}, 400

        # Save data to DB
        titles = TitlesModel(data["listname"], data["title"], data["remarks"])
        titles.save_to_db()


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
        data = AddtoList.parser.parse_args()
        # check if list name exists, if not create one with required parameters
        item = TitlesModel.find_by_listname(data['listname'])
        # Check if user session is valid
        session_id_valid = SessionModel(data['sid'])
        # if user doesn't have a valid active sessions
        if session_id_valid is None:
            return {'message': 'Inter a valid session ID'}, 404
        else:
            # Check if user already has a list, if yes => error
            if UserModel.find_by_user_and_list(data['username'], data["listname"]):
                return {"message": "A listname already exists for the user"}, 404
            if item is None:
                item = TitlesModel(data["listname"], data["title"], data["remarks"])
                return {'message': 'Resource updated successfully'}, 204
                item.save_to_db()


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

    def delete_from_list(self):
        data = DeliteList.parser.parse_args()
        # title to delete
        list_to_delete = TitlesModel.find_by_listname_and_title(data['username'], data["title"])
        # Check if user session is valid
        valid_session_id = SessionModel(data['sid'])
        # if user doesn't have a valid active sessions, error
        if valid_session_id is None:
            return {'message': 'No active sessions found'}, 404
        else:
            if TitlesModel(data['title']) not in list_to_delete:  # len(list_to_delete) == 0:
                return {'message': 'The requested title doesnt exist in the list'}, 400
            else:
                TitlesModel(data['title']).delete_from_db()
                # TitlesModel(data['title']).delete_from_db()
                return {'message': 'List has been deleted from the database'}, 200


class DeleteList(Resource):
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

    def delete_list(self):
        data = DeliteList.parser.parse_args()
        # list to delete
        list_to_delete = UserModel.find_by_username(data['listname'])
        # Check if user session is valid
        valid_session_id = SessionModel(data['sid'])
        # if user doesn't have a valid active sessions, error
        if session_id_valid is None:
            return {'message': 'No active sessions found'}, 404
        else:
            if len(list_to_delete) == 0:
                return {'message': 'The request item doesnt exist in the database'}, 400
            else:
                # delete title from user
                List = UserModel(data['listname'])
                List.delete_from_db()
                # TitlesModel(data['title']).delete_from_db()
                return {'message': 'List has been deleted successfully'}, 200


class TitlesList(Resource):
    def get(self):
        return {'titles': [x.json() for x in TitlesModel.query.all()]}
