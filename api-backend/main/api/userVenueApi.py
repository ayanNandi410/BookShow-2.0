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
    "capacity" : fields.Integer,
}


# Get Venue List for a city
class UserVenueListByCityAPI(Resource):

    @marshal_with(venue_output_fields)
    def get(self,city):
        venues = db.session.query(Venue).filter(Venue.city == city).order_by(desc(Venue.timestamp)).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for this city',status_code=404,error_code="VN009")
        
    def post(self):
        raise BusinessValidationError(status_code=405,error_code="VN050",error_message="Method not allowed")
    

# Get Venue List by Venue Name
class GetVenueByNameApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,name):
        venues = db.session.query(Venue).filter(Venue.name.ilike(f'%{name}%')).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venue found for this name',status_code=404,error_code="VN010")
        