from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request
import json
from ..models import Show, Venue, Tag, Language, Allocation, BookTicket
from sqlalchemy import select, join, func, exc, desc
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from datetime import datetime as dt
from flask_security import auth_required, roles_accepted

# api for handling shows

tag_output_fields = {
    "name" : fields.String
}

language_output_fields = {
    "name" : fields.String
}

userShow_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "rating" : fields.Integer,
    "duration" : fields.String,
    "tags" : fields.List(fields.Nested(tag_output_fields)),
    "languages" : fields.List(fields.Nested(language_output_fields)),
    "timestamp" : fields.DateTime(dt_format='rfc822')
}

chooseShow_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "duration" : fields.String
}
