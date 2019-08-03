from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api

from sqlalchemy import exc

from project import db
from project.api.models import Url

from urllib.parse import unquote, urlparse

url_blueprint = Blueprint('url', __name__)
api = Api(url_blueprint)


class UrlList(Resource):
    def get(self):
        """ Get all urls """
        response_obj = {
            'status': 'success',
            'data':{
                'urls':[url.to_json() for url in Url.query.all()]
            }
        }

        return response_obj, 200


    def post(self):
        """ add url to the system """

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


class UrlInfo(Resource):

    def get(self, path=None):
        """ Get url details """

        response_obj = {
            'status': 'fail',
            'url': None,
            'target_url': None,
            'isMalware': None
        }
            
        path = request.full_path
        url = unquote(path)[9:]        
        
        try:
            cur_url = Url.query.filter_by(url=url).first()
            # for testing purpose
            response_obj['url'] = url
            response_obj['target_url'] = cur_url
            response_obj['status'] = 'success'
            if not cur_url:
                response_obj['isMalware'] = 'false'
                return response_obj, 200
            # elif cur_url and not cur_url.active:
            #     response_obj['isMalware'] = 'false'
            #     return response_obj, 200 
            
            response_obj['isMalware'] = 'true'
            return response_obj, 200
        
        except ValueError:
            return response_obj, 404


class UrlPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(UrlPing, '/ping')
api.add_resource(UrlList, '/urls')
api.add_resource(UrlInfo, '/urlinfo/<path:path>')
