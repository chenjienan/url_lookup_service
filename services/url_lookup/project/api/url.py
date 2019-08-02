from flask import Blueprint, request
from flask_restful import Resource, Api

from project import db
from project.api.models import Url

url_blueprint = Blueprint('url', __name__)
api = Api(url_blueprint)

class UrlList(Resource):
    def post(self):
        post_data = request.get_json()
        url = post_data.get('url')
        db.session.add(Url(url=url))
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{url} was added!'
        }
        return response_object, 201


class UrlPing(Resource):
    def get(self):
        return {
        'status': 'success',
        'message': 'pong!'
    }


api.add_resource(UrlPing, '/urlinfo/ping')
api.add_resource(UrlList, '/urls')