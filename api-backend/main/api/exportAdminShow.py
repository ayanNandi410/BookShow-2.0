from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request, send_file
import json
from ..models import Show, Venue, Tag, Language, Allocation, BookTicket
from sqlalchemy import select, join, func, exc, desc
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from datetime import datetime as dt
from flask_security import auth_required, roles_accepted
from ..tasks.exportShowsCSV import ShowsCSV
import time
import os

baseDir = os.path.abspath(os.getcwd())

        

class ExportShowAPI(Resource):

    @auth_required('token')
    @roles_accepted('admin')
    def get(self,vid):
        job = ShowsCSV.delay(vid)
        result = job.wait()
        return { "result": "Success" }, 200
    
class DownloadCSVAPI(Resource):

    def get(self,name):
        return send_file(
        baseDir+'/files/'+name+'_Details.csv',
        mimetype='text/csv',
        download_name=name+'_Details.csv',
        as_attachment=True)
    

