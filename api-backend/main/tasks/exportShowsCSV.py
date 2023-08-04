from datetime import datetime, timedelta
from ..workers import celeryObj
from ..models import User, Role
from ..db import db
from celery.schedules import crontab
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request
import json
from ..models import Show, Venue, Tag, Language, Allocation, BookTicket
from sqlalchemy import select, join, func, exc, desc
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from datetime import datetime as dt
from flask_security import auth_required, roles_accepted
import csv, os

def ListToString(el):
    res = ""
    for x in el:
        res += x.name
    return res

@celeryObj.task()
def ShowsCSV(vid):

    venue = db.session.query(Venue).get(vid)

    with open('files/'+venue.name+'_Details.csv','w') as f:
        writer = csv.writer(f)

        writer.writerow(['Show Name','Rating','Duration','Tags','Languages','Booking Count'])

        shows = venue.shows
        for show in shows:
            bookings = db.session.query(BookTicket).filter(BookTicket.venue.contains(venue),BookTicket.show.contains(show)).all()
            count = len(bookings)

            writer.writerow([show.name,show.rating,show.duration,ListToString(show.tags),ListToString(show.languages),count])
        
        f.close()
    




