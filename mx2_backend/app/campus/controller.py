from flask_restx import Namespace, Resource, fields
from .model import Campus

campus_api = Namespace('campus', description='Campus related operations')

@campus_api.route('/')
class CampusList(Resource):
    def get(self):
        return [campus.to_dict() for campus in Campus.objects()], 200