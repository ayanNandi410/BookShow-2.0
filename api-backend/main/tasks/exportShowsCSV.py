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
    for i in range(len(el)):
        if i != (len(el)-1):
            res += el[i].name + ", "
        else:
            res += el[i].name
    return res

@celeryObj.task()
def ShowsCSV(vid):

    venue = db.session.query(Venue).get(vid)

    with open('files/'+venue.name+'_Details.csv','w') as f:
        
        fnames = ['Show Name','Rating','Duration','Tags','Languages','Booking Count']
        writer = csv.DictWriter(f, fieldnames=fnames)
        writer.writeheader()

        shows = venue.shows
        for show in shows:
            bookings = db.session.query(BookTicket).filter(BookTicket.venue.contains(venue),BookTicket.show.contains(show)).all()
            count = len(bookings)

            writer.writerow({'Show Name': show.name, 
                             'Rating': show.rating,
                             'Duration': show.duration, 
                             'Tags': ListToString(show.tags), 
                             'Languages': ListToString(show.languages),
                             'Booking Count': count
                            })
        f.close()
    




