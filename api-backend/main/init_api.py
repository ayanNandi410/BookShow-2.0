# Api initialization
from flask_restful import Resource, Api
from .api.auth import RegisterAPI
from .api.test import TestAPI
from .api.cityApi import GetAllCitiesAPI
from .api.venueApi import VenueListByCityAPI
    
def getConfiguredApi(app):
    apiV = Api(app)

    apiV.add_resource(RegisterAPI,"/api/register",endpoint="/register")
    apiV.add_resource(TestAPI,"/api/test",endpoint="/test")
    apiV.add_resource(GetAllCitiesAPI,"/api/city/all",endpoint="/city/all")
    apiV.add_resource(VenueListByCityAPI,"/api/venues/byCity/<string:city>",endpoint="/venues/byCity")
    
    return apiV