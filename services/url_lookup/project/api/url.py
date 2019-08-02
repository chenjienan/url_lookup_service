from flask import Blueprint, request
from flask_restful import Resource, Api

from sqlalchemy import exc

from project import db
from project.api.models import Url

url_blueprint = Blueprint('url', __name__)
api = Api(url_blueprint)


class UrlList(Resource):
    def post(self):
        post_data = request.get_json()

        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }

        if not post_data:
            return response_object, 400

        url = post_data.get('url')
        try:
            get_url = Url.query.filter_by(url=url).first()
            if not get_url:
                db.session.add(Url(url=url))
                db.session.commit()
                response_object['status'] = 'success'
                response_object['message'] = f'{url} was added!'
                return response_object, 201
            else:
                response_object['message'] = 'That url already exists.'
                return response_object, 400

        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400


class UrlPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(UrlPing, '/urlinfo/ping')
api.add_resource(UrlList, '/urls')
