# Api initialization
from flask_restful import Resource, Api

from .api.test import TestAPI
from .api.cityApi import GetAllCitiesAPI
from .api.adminVenueApi import AdminVenueListByCityAPI, AdminVenueAPI
from .api.adminShowApi import PopularShowsApi, ShowAPI, ListShowByVenueApi, ShowsByNameApi
from .api.userVenueApi import UserVenueListByCityAPI, GetVenueByNameApi, UserVenueAPI, VenueListByShowApi
from .api.allocationApi import AllocationBetweenDatesAPI, AllocationAPI, AllocationForSevenDaysAPI
from .api.exportAdminShow import ExportShowAPI, DownloadCSVAPI
from .api.userShowApi import FilterShowsApi

from .api.bookingApi import BookTicketAPI
from .api.reviewApi import MovieReviewAPI
from .api.calcReviewApi import CalcReviewAPI
    
def getConfiguredApi(app):

    apiV = Api(app)

    # Common
    apiV.add_resource(TestAPI,"/api/test",endpoint="/test")
    apiV.add_resource(GetAllCitiesAPI,"/api/city/all",endpoint="/city/all")
    
    # venue
    apiV.add_resource(GetVenueByNameApi,"/api/venueByName/<string:name>",endpoint="/venueByName")
    apiV.add_resource(ShowsByNameApi,"/api/showByName/<string:name>",endpoint="/showByName")
    apiV.add_resource(VenueListByShowApi,"/api/venue/byShow/<string:sid>",endpoint="/venue/byShow")

    # show
    apiV.add_resource(ListShowByVenueApi,"/api/show/byVenue/<string:vid>",endpoint="/show/byVenue")
    apiV.add_resource(FilterShowsApi,"/api/filterShow",endpoint="/filterShow")

    # for Admin
    apiV.add_resource(AdminVenueListByCityAPI,"/api/venuesforAdmin/byCity/<string:city>",endpoint="/venuesforAdmin/byCity")
    apiV.add_resource(AdminVenueAPI,"/api/venue/<string:id>","/api/venue",endpoint="/venue")
    apiV.add_resource(PopularShowsApi,"/api/popularShows",endpoint="/popularShows")
    apiV.add_resource(ShowAPI,"/api/show/<string:id>","/api/show",endpoint="/show")
    apiV.add_resource(AllocationBetweenDatesAPI,"/api/timingWithRange",endpoint="/timingWithRange")
    apiV.add_resource(AllocationAPI,"/api/timing/<string:aid>","/api/timing",endpoint="/timing/<string:aid>")
    apiV.add_resource(AllocationForSevenDaysAPI,"/api/timing/sevenDays",endpoint="/sevenDays")

    # for User
    apiV.add_resource(UserVenueListByCityAPI,"/api/venuesforUser/byCity/<string:city>",endpoint="/venuesforUser/byCity")
    apiV.add_resource(UserVenueAPI,"/api/user/venue/<string:id>","/api/venue",endpoint="/user/venue")

    apiV.add_resource(BookTicketAPI,"/api/booking","/api/booking/<string:email>",endpoint="/booking")
    apiV.add_resource(MovieReviewAPI,"/api/review","/api/review/<int:sid>",endpoint="/review")
    apiV.add_resource(CalcReviewAPI,"/api/updateReview","/api/updateReview/<string:sid>",endpoint="/updateReview")

    apiV.add_resource(ExportShowAPI,"/api/exportVenue/<vid>",endpoint="/exportVenue")
    apiV.add_resource(DownloadCSVAPI,"/api/venue/downloadCSV/<name>",endpoint="/venue/downloadCSV")


    return apiV