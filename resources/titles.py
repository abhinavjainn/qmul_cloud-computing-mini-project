
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.title import TitlesModel


class Title(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('remarks',
                        type=str,
                        required=True,
                        help="Please give remarks."
                        )

    @jwt_required()
    def get(self, listname):
        titles = TitlesModel.find_by_name(listname)
        if title:
            return titles.json()
        return {'message': 'Title not found'}, 404

    def post(self, listname):
        if TitlesModel.find_by_name(listname):
            return {'message': "An title with listname '{}' already exists.".format(listname)}, 400

        data = Title.parser.parse_args()

        titles = TitlesModel(listname, **data)

        try:
            titles.save_to_db()
        except:
            return {"message": "An error occurred inserting the title."}, 500

        return titles.json(), 201

    def delete(self, litsname):
        titles = TitlesModel.find_by_name(listname)
        if titles:
            item.delete_from_db()

        return {'message': 'Title deleted'}

    def put(self, listname):
        data = Title.parser.parse_args()

        titles = TitlesModel.find_by_name(listname)

        if titles is None:
            titles = TitlesModel(listname, **data)
        else:
            titles.title = data['title']

        titles.save_to_db()

        return titles.json()


class TitlesList(Resource):
    def get(self):
        return {'titles': [x.json() for x in TitlesModel.query.all()]}
