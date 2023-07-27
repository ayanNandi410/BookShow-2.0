from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from ..validation import BusinessValidationError, NotFoundError
from flask import current_app as app
import werkzeug, secrets, string
from flask import abort
from flask_security import auth_required, utils
from ..models import User, Role
from ..db import db

user_resource_fields = {
    'name': fields.String,
    'email': fields.String,
    'password':  fields.String,
    'username': fields.String
}

reg_user_parser = reqparse.RequestParser()
reg_user_parser.add_argument('name')
reg_user_parser.add_argument('email')
reg_user_parser.add_argument('password')
reg_user_parser.add_argument('username')


class RegisterAPI(Resource):

    def post(self):

        return "Success", 200