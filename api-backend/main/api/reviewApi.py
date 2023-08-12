from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request, jsonify
from flask_login import current_user
from datetime import datetime as dt
from ..models import BookTicket, Show, Venue, Allocation, MovieReview
from main.db import db
from main.validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc, exc
from ..tasks.recalcReview import recalcReview
from flask_security import auth_required, roles_accepted

# Api to handle user reviews


review_output_fields = {
    "user_email" : fields.String,
    "comment" : fields.String,
    "gRating" : fields.Integer,
    "timestamp" : fields.DateTime(dt_format='rfc822')
}

create_review_parser = reqparse.RequestParser()
create_review_parser.add_argument('sid')
create_review_parser.add_argument('user_email')
create_review_parser.add_argument('rating',type=int, help="Rating must be an integer")
create_review_parser.add_argument('comment')

class MovieReviewAPI(Resource):

    # get user reviews by show name
    @marshal_with(review_output_fields)
    @auth_required('token')
    @roles_accepted('user')
    def get(self,sid):
        show = db.session.query(Show).get(sid)

        if not show:
           raise NotFoundError(error_message='Show name not found',status_code=404,error_code="RW001") 

        reviews = db.session.query(MovieReview).filter(MovieReview.show_id == show.id).order_by(desc(MovieReview.timestamp)).limit(30).all()
        print(reviews)
        if not reviews:
            raise NotFoundError(error_message='No Review found',status_code=404,error_code="RW002")
        else:
            return reviews, 200

    # submit user review for a show
    @auth_required('token')
    @roles_accepted('user')
    def post(self):
        bk_args = create_review_parser.parse_args()
        sid = bk_args.get('sid',None)
        email = bk_args.get('user_email',None)
        rating = bk_args.get('rating',None)
        comment = bk_args.get('comment',None)
    
        if sid is None or sid == '':
            raise BusinessValidationError(status_code=400,error_code="RW003",error_message="Show Id is required")

        if email is None or email == '':
            raise BusinessValidationError(status_code=400,error_code="RW004",error_message="Email is required")

        if rating is None:
            raise BusinessValidationError(status_code=400,error_code="RW005",error_message="Rating is required")

        if int(rating)<0 or int(rating)>10:
            raise BusinessValidationError(status_code=400,error_code="RW006",error_message="Invalid value for rating")

        if comment is None or comment == '':
            raise BusinessValidationError(status_code=400,error_code="RW007",error_message="Comment is required")

        
        show = db.session.query(Show).get(sid)

        if not show:
            raise BusinessValidationError(status_code=400,error_code="RW008",error_message="Show does not exist")

        review = db.session.query(MovieReview).filter(MovieReview.show_id == show.id,MovieReview.user_email == email).first()

        if review:
            raise BusinessValidationError(status_code=400,error_code="RW009",error_message="Already reviewed")

        timestamp = dt.now()

        try:
            new_review = MovieReview(user_email=email,show_id=sid,comment=comment,gRating=int(rating),timestamp=timestamp)
            db.session.add(new_review)
            db.session.commit()

            # update average rating
            job = recalcReview.apply_async((sid,int(rating)), countdown=3, retry=True, retry_policy={
                'max_retries': 5,
                'interval_step': 1,
            })

            return "Success", 200
        
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="RW020",error_message="Add Transaction failed. Try again")

    # other requests
    def put(self,name):
        raise BusinessValidationError(status_code=405,error_code="RW010",error_message="Method not allowed")
    
    def delete(self,name):
        raise BusinessValidationError(status_code=405,error_code="RW011",error_message="Method not allowed")