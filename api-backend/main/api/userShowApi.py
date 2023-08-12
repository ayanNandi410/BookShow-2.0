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

filter_show_parser = reqparse.RequestParser()
filter_show_parser.add_argument('rating',type=int)
filter_show_parser.add_argument('runningShows')
filter_show_parser.add_argument('tags', type=str, action='append', location='json')
filter_show_parser.add_argument('languages', type=str, action='append', location='json')


# filter on all shows       
class FilterShowsApi(Resource):

    @marshal_with(userShow_output_fields)
    @auth_required('token')
    @roles_accepted('user')
    def post(self):
        vn_args = filter_show_parser.parse_args()
        tags = vn_args.get('tags',[])
        languages = vn_args.get('languages',[])
        rating = vn_args.get('rating',None)
        runShows = vn_args.get('runningShows',None)
        print(runShows,tags,languages)
        
        tagList = []
        langList = []
        shows = []

        if tags != [] and tags is not None:
            for tagName in tags:
                tag = db.session.query(Tag).filter(Tag.name == tagName).first()
                if not tag:
                    raise BusinessValidationError(status_code=400,error_code="SW0021",error_message="Tag "+tagName+" not found")
                tagList.append(tag)

            for tag in tagList:
                for show in tag.show:
                    if show not in shows:
                        shows.append(show)

        if languages != [] and languages is not None:
            for langName in languages:
                lng = db.session.query(Language).filter(Language.name == langName).first()
                if not lng:
                    raise BusinessValidationError(status_code=400,error_code="SW0022",error_message="Language "+langName+" not found")
                langList.append(lng)

            for lang in langList:
                for show in lang.show:
                    if show not in shows:
                        shows.append(show)

        if rating is not None and rating != '':
            for show in shows:
                if show.rating < rating:
                    shows.remove(show)
        if runShows is not None and runShows == 'yes':
            for show in shows:
                if show.venues == []:
                    shows.remove(show)

        if shows:
            return list(shows)
        else:
            raise NotFoundError(error_message='No Shows found',status_code=404,error_code="SW013")
        
