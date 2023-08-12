from ..workers import celeryObj
from ..models import CalcReview, Show
from ..db import db
from sqlalchemy import exc

@celeryObj.task()
def recalcReview(showId,rating):
    print("Started JOB -> Recalculate Review")

    try:
            rowR = db.session.query(CalcReview).filter(CalcReview.show_id == showId).first()

            if not rowR:
                rowR = CalcReview(show_id=showId,oneStarRatings=0,twoStarRatings=0,threeStarRatings=0,fourStarRatings=0,fiveStarRatings=0,totalRatings=0,avRating="0")
            
            rt = round(rating/2)
            add = 0
            
            if rt <= 1:
                rowR.oneStarRatings += 1
                add = 1
            elif rt == 2:
                rowR.twoStarRatings += 1
                add = 2
            elif rt == 3:
                rowR.threeStarRatings += 1
                add = 3
            elif rt == 4:
                rowR.fourStarRatings += 1
                add = 4
            else:
                rowR.fiveStarRatings += 1
                add = 5

            newAvgRating = round(((float(rowR.avRating)*rowR.totalRatings) + add)/(rowR.totalRatings+1),2)
            rowR.totalRatings += 1

            rowR.avRating = str(newAvgRating)
            
            db.session.add(rowR)

            # update show rating
            show = db.session.query(Show).filter(Show.id == showId).first()
            show.rating = round(int(newAvgRating)*2)

            db.session.add(show)

            db.session.commit()
            print("Review Calculation executed successfully")
    except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            print("Recalculation for Review failed")
