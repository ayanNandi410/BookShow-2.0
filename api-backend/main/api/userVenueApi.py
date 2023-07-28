from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from ..models import Venue, Allocation, Show
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc, exc

# Output JSON format
venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "location" : fields.String,
    "city" : fields.String,
    "capacity" : fields.Integer,
    "description" : fields.String,
    "timestamp" : fields.DateTime(dt_format='rfc822')

}

# for POST and PUT request
create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('id',type=int)
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('location')
create_venue_parser.add_argument('city')
create_venue_parser.add_argument('capacity',type=int, help='Capacity cannot be converted')
create_venue_parser.add_argument('description')