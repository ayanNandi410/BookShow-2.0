from flask_restful import Resource, fields, marshal_with, reqparse
from ..models import Venue
from main.db import db
from ..cachedTasks import get_all_cities
from main.validation import NotFoundError, BusinessValidationError
# get all cities where venues exist

city_output_fields = {
    "cities": fields.List(fields.String)
}

class GetAllCitiesAPI(Resource):

    @marshal_with(city_output_fields)
    def get(self):
        cities = get_all_cities()

        if len(cities)!=0:
            return { 'cities': cities}
        else:
            raise NotFoundError(error_message='No City found',status_code=404,error_code="CN001")
        
    def post(self):
        pass
