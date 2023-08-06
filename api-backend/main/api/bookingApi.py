from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request, jsonify
from flask_login import current_user
from datetime import datetime as dt
from ..models import BookTicket, Show, Venue, Allocation
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc, exc
from flask_security import auth_required, roles_accepted

# Api for handling user booking

class MyDate(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')
    
class MyTime(fields.Raw):
    def format(self, value):
        return value.strftime('%H-%M-%S')

venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String
}

show_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String
}

alloc_output_fields = {
    "timeslot" : fields.DateTime(dt_format='rfc822'),
    "price" : fields.String
}

booking_output_fields = {
    "venue" : fields.Nested(venue_output_fields),
    "show" : fields.Nested(show_output_fields),
    "allocation": fields.Nested(alloc_output_fields),
    "totPrice" : fields.String,
    "allocSeats" : fields.Integer,
    "timestamp" : fields.DateTime(dt_format='rfc822')
}

create_booking_parser = reqparse.RequestParser()
create_booking_parser.add_argument('vid')
create_booking_parser.add_argument('sid')
create_booking_parser.add_argument('aid')
create_booking_parser.add_argument('email')
create_booking_parser.add_argument('allocSeats',type=int, help="Seats must be an integer")
create_booking_parser.add_argument('totPrice', type=float, help="Not a valid number or price")

class BookTicketAPI(Resource):

    # get booking details for a given user
    @marshal_with(booking_output_fields)
    @auth_required('token')
    @roles_accepted('user')
    def get(self,email):

        bookings = db.session.query(BookTicket).filter(BookTicket.user_email == email).order_by(desc(BookTicket.timestamp)).limit(20).all()

        if not bookings:
            raise NotFoundError(error_message='No Booking found',status_code=404,error_code="BK001")
        else:
            return bookings, 200

    # create a new booking
    @auth_required('token')
    @roles_accepted('user')
    def post(self):
        bk_args = create_booking_parser.parse_args()
        vid = bk_args.get('vid',None)
        sid = bk_args.get('sid',None)
        aid = bk_args.get('aid',None)
        email = bk_args.get('email',None)
        allcSeats = bk_args.get('allocSeats',None)
        ticketPrice = bk_args.get('totPrice',None)

        if vid is None or vid == '':
            raise BusinessValidationError(status_code=400,error_code="AL001",error_message="Venue Name is required")
    
        if sid is None or sid == '':
            raise BusinessValidationError(status_code=400,error_code="AL002",error_message="Show Name is required")

        if email is None or email == '':
            raise BusinessValidationError(status_code=400,error_code="AL0017",error_message="Email is required")

        if float(ticketPrice) < 0.0:
            raise BusinessValidationError(status_code=400,error_code="AL003",error_message="Invalid value for Ticket Price")

        if allcSeats is None:
            raise BusinessValidationError(status_code=400,error_code="AL006",error_message="Allocated seat count is required")

        if int(allcSeats) <= 0:
            raise BusinessValidationError(status_code=400,error_code="AL007",error_message="Invalid seat count")

        
        show = db.session.query(Show).get(sid)

        if not show:
            raise BusinessValidationError(status_code=400,error_code="AL008",error_message="Show does not exist")

        venue = db.session.query(Venue).get(vid)
        if not venue:
            raise BusinessValidationError(status_code=400,error_code="AL009",error_message="Venue does not exist")

        
    
        allocation = db.session.query(Allocation).get(aid)
        if not allocation:
            raise BusinessValidationError(status_code=400,error_code="AL0019",error_message="Allocation not found")

        if int(allcSeats) > int(allocation.avSeats):
            message = "Only " + str(allocation.avSeats) + " seats available"
            raise BusinessValidationError(status_code=400,error_code="AL0016",error_message=message)

        # allows multiple bookings
        try:
            new_booking = BookTicket(user_email=email,allocation=allocation,showAllocId=allocation.id,allocSeats=allcSeats,totPrice=ticketPrice)
            allocation.avSeats = int(allocation.avSeats) - int(allcSeats)
            db.session.add(allocation) # update available seats
            db.session.add(new_booking)

            db.session.commit()
            return "Success", 201
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="AL020",error_message="Add Transaction failed. Try again")


    def put(self,name):
        pass
    
    def delete(self,name):
        pass