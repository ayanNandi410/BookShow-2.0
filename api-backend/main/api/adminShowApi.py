from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request
import json
from ..models import Show, Venue, Tag, Language, Allocation, BookTicket
from sqlalchemy import select, join, func, exc, desc
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from datetime import datetime as dt
from flask_security import auth_required, roles_accepted
from ..cachedTasks import cache

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

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('id',type=int)
create_show_parser.add_argument('name')
create_show_parser.add_argument('rating',type=int)
create_show_parser.add_argument('tags', type=str, action='append', location='json')
create_show_parser.add_argument('languages', type=str, action='append', location='json')
create_show_parser.add_argument('duration')


# get all recently allocated shows
class PopularShowsApi(Resource):

    @marshal_with(userShow_output_fields)
    @auth_required('token')
    @roles_accepted('admin','user')
    def get(self):

        shows = db.session.query(Show).order_by(desc(Show.timestamp)).limit(20).all()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Shows found',status_code=404,error_code="SW013")
        

class ShowsByNameApi(Resource):

    @marshal_with(userShow_output_fields)
    @auth_required('token')
    @roles_accepted('admin','user')
    def get(self,name):

        from ..cachedTasks import getShowsByName
        shows = getShowsByName(name)

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Shows found',status_code=404,error_code="SW013")
        

class ShowAPI(Resource):

    # get a show by show name. Show names are assumed to be unique
    @marshal_with(userShow_output_fields)
    @auth_required('token')
    @roles_accepted('admin')
    def get(self,name):
        shows = db.session.query(Show).filter(Show.name == name).first()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='Show not found',status_code=404,error_code="SW001")

    # create a new show
    @auth_required('token')
    @roles_accepted('admin')
    def post(self):
        vn_args = create_show_parser.parse_args()
        name = vn_args.get('name',None)
        tags = vn_args.get('tags',[])
        languages = vn_args.get('languages',[])
        rating = vn_args.get('rating',None)
        duration = vn_args.get('duration',None)

        cache.delete('getShowsByName')

        if name is None or name == '':
            raise BusinessValidationError(status_code=400,error_code="SW002",error_message="Name is required")
    
        if tags is []:
            raise BusinessValidationError(status_code=400,error_code="SW003",error_message="A Single Tag is required")

        if languages is []:
            raise BusinessValidationError(status_code=400,error_code="SW004",error_message="Some Language is required")

        if rating is None:
            raise BusinessValidationError(status_code=400,error_code="SW005",error_message="Initial rating is required")

        if int(rating) < 0 or int(rating) > 10:
            raise BusinessValidationError(status_code=400,error_code="SW006",error_message="Invalid value for rating")

        if duration is None:
            raise BusinessValidationError(status_code=400,error_code="SW007",error_message="Duration is required")


        show = db.session.query(Show).filter(Show.name == name).first()

        if show:
            raise BusinessValidationError(status_code=400,error_code="SW008",error_message="Show already exists")

        tagList = []
        langList = []
        for tagName in tags:
            tag = db.session.query(Tag).filter(Tag.name == tagName).first()
            if not tag:
                raise BusinessValidationError(status_code=400,error_code="SW0021",error_message="Tag "+tagName+" not found")
            tagList.append(tag)

        for langName in languages:
            lng = db.session.query(Language).filter(Language.name == langName).first()
            if not lng:
                raise BusinessValidationError(status_code=400,error_code="SW0022",error_message="Language "+langName+" not found")
            langList.append(lng)

        from datetime import datetime
        timestamp = datetime.now()

        try:
            new_show = Show(name=name,rating=rating,duration=duration,timestamp=timestamp)
            new_show.tags = tagList
            new_show.languages = langList

            db.session.add(new_show)
            db.session.commit()

            showId = db.session.query(Show).filter(Show.name == name,Show.timestamp==timestamp,Show.duration==duration).first()

            return { "id": showId.id, "result": "Success" }, 201
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="SW017",error_message="Add Transaction failed. Try again")

    # update existing show
    @auth_required('token')
    @roles_accepted('admin')
    def put(self):
        vn_args = create_show_parser.parse_args()
        id = vn_args.get('id',None)
        name = vn_args.get('name',None)
        tags = vn_args.get('tags',[])
        languages = vn_args.get('languages',[])
        rating = vn_args.get('rating',None)
        duration = vn_args.get('duration',None)

        cache.delete('getShowsByName')

        if name is None or name == '':
            raise BusinessValidationError(status_code=400,error_code="SW002",error_message="Name is required")
    
        if tags is []:
            raise BusinessValidationError(status_code=400,error_code="SW003",error_message="A Single Tag is required")

        if languages is []:
            raise BusinessValidationError(status_code=400,error_code="SW004",error_message="Some Language is required")

        if rating is None:
            raise BusinessValidationError(status_code=400,error_code="SW005",error_message="Initial rating is required")

        if int(rating) < 0 or int(rating) > 10:
            raise BusinessValidationError(status_code=400,error_code="SW006",error_message="Invalid value for rating")

        if duration is None:
            raise BusinessValidationError(status_code=400,error_code="SW007",error_message="Duration is required")


        show = db.session.query(Show).get(id)

        if not show:
            raise BusinessValidationError(status_code=400,error_code="SW0015",error_message="Show does not exist")

        tagList = []
        langList = []
        for tagName in tags:
            tag = db.session.query(Tag).filter(Tag.name == tagName).first()
            if not tag:
                raise BusinessValidationError(status_code=400,error_code="SW0021",error_message="Tag "+tagName+" not found")
            tagList.append(tag)

        for langName in languages:
            lng = db.session.query(Language).filter(Language.name == langName).first()
            if not lng:
                raise BusinessValidationError(status_code=400,error_code="SW0022",error_message="Language "+langName+" not found")
            langList.append(lng)

        from datetime import datetime
        timestamp = datetime.now()

        try:
            
            show.name = name
            show.rating = int(rating)
            show.duration = duration
            show.tags = tagList
            show.languages = langList
        
            db.session.add(show)
            db.session.commit()

            return "Success", 201
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="SW018",error_message="Update Transaction failed. Try again")

    # delete existing show
    @auth_required('token')
    @roles_accepted('admin')
    def delete(self,id):

        cache.delete('getShowsByName')

        show = db.session.query(Show).filter(Show.id == id).first()

        if not show:
            raise BusinessValidationError(status_code=400,error_code="SW001",error_message="Show not found with such name")
        
        # check for dependency
        venueForShow = db.session.query(Allocation).filter(Allocation.show == show).first()

        if venueForShow:
            raise BusinessValidationError(status_code=400,error_code="SW008",error_message="Show has been allocated to venues")

        try:
            db.session.delete(show)
            db.session.commit()
            return "Success", 200
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="VN013",error_message="Delete Transaction failed. Try again")


# get shows for a particular venue
class ListShowByVenueApi(Resource):

    @marshal_with(userShow_output_fields)
    @auth_required('token')
    @roles_accepted('admin','user')
    def get(self,vid):
        venue = db.session.query(Venue).filter(Venue.id == vid).first()
        shows = venue.shows
        
        if len(shows) == 0:
            raise NotFoundError(error_message='No Shows found for this venue',status_code=404,error_code="SW009")
        else:
            return shows
        
    def post(self):
        pass