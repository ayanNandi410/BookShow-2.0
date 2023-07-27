from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from ..validation import BusinessValidationError, NotFoundError
from flask import current_app as app
import werkzeug, secrets, string
from flask import abort
from flask_security import auth_required, roles_accepted, utils
from ..models import User, Role
from ..db import db



class TestAPI(Resource):

    @auth_required('token','session')
    @roles_accepted('anonymous','user')
    def get(self):
        return "Success", 200