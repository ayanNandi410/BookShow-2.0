# Api initialization
from flask_restful import Resource, Api
from .api.auth import RegisterAPI
from .api.test import TestAPI
from .api.cityApi import GetAllCitiesAPI
from .api.adminVenueApi import AdminVenueListByCityAPI, AdminVenueAPI
from .api.adminShowApi import PopularShowsApi, ShowAPI, ListShowByVenueApi
from .api.userVenueApi import UserVenueListByCityAPI, GetVenueByNameApi
from .api.allocationApi import AllocationBetweenDatesAPI, AllocationAPI
    
def getConfiguredApi(app):
    apiV = Api(app)

    # Common
    apiV.add_resource(RegisterAPI,"/api/register",endpoint="/register")
    apiV.add_resource(TestAPI,"/api/test",endpoint="/test")
    apiV.add_resource(GetAllCitiesAPI,"/api/city/all",endpoint="/city/all")
    apiV.add_resource(GetVenueByNameApi,"/api/venueByName/<string:name>",endpoint="/venueByName")
    #apiV.add_resource(VenueListByCityAPI,"/api/venues/byCity/<string:city>",endpoint="/venues/byCity")

    # for Admin
    apiV.add_resource(AdminVenueListByCityAPI,"/api/venuesforAdmin/byCity/<string:city>",endpoint="/venuesforAdmin/byCity")
    apiV.add_resource(AdminVenueAPI,"/api/venue/<string:id>","/api/venue",endpoint="/venue")
    apiV.add_resource(PopularShowsApi,"/api/popularShows",endpoint="/popularShows")
    apiV.add_resource(ShowAPI,"/api/show/<string:id>","/api/show",endpoint="/show")
    apiV.add_resource(ListShowByVenueApi,"/api/show/byVenue/<string:vid>",endpoint="/show/byVenue")
    apiV.add_resource(AllocationBetweenDatesAPI,"/api/timingWithRange",endpoint="/timingWithRange")
    apiV.add_resource(AllocationAPI,"/api/timing/<string:aid>",endpoint="/timing/<string:aid>")
    

    # for User
    apiV.add_resource(UserVenueListByCityAPI,"/api/venuesforUser/byCity/<string:city>",endpoint="/venuesforUser/byCity")

    return apiV