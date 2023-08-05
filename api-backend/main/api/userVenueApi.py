from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from ..models import Venue, Allocation, Show
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc, exc
from flask_security import auth_required, roles_accepted

# Output JSON format
venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "location" : fields.String,
    "capacity" : fields.Integer,
    "city": fields.String,
    "description": fields.String,
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
        
class UserVenueAPI(Resource):

    # get Venue by Name
    @marshal_with(venue_output_fields)
    def get(self,id):
        venue = db.session.query(Venue).filter(Venue.id == id).first()

        if venue:
            return venue
        else:
            raise NotFoundError(error_message='Venue not found',status_code=404,error_code="VN001")
        

# Get Venue List by Show Name
class VenueListByShowApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,sid):
        city = request.args.get('city',None)
           
        show = db.session.query(Show).get(sid)
        venues = show.venues


        if city is not None: 
            venueList = []
            for venue in venues:
                if venue.city == city:
                    venueList.append(venue)
            if venueList != []:
                return venueList
            else:
                raise NotFoundError(error_message='No Venues found for show with city name',status_code=404,error_code="VN012")
        
        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for show',status_code=404,error_code="VN011")
        