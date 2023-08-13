from jinja2 import Template
from weasyprint import HTML
import uuid, os
from datetime import datetime, timedelta
from ..workers import celeryObj
from ..models import User, Role, BookTicket, MovieReview
from ..db import db
from ..send_email import send_email
from celery.schedules import crontab

CurMonth = datetime.now().strftime("%B, %Y")

@celeryObj.on_after_finalize.connect
def alert_month_everyUser(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13,minute=1,day_of_month=1),
        MontlyEnmtReportJob.s(),
        name = 'entertainment report at every month'
    )


def format_report(temp_file,bookings,reviews,user):
    with open(temp_file) as file:
        template = Template(file.read())
        return template.render(bookings=bookings,reviews=reviews,user=user,month=CurMonth)
    
def create_report(bookings,reviews,user,type):
    message = format_report('templates/report_template.html',bookings,reviews,user)
    html = HTML(string=message)
    file_name = user['name']+"_"+CurMonth+'.pdf'
    print(file_name)

    #if type=='pdf':
    html.write_pdf(target="files/"+file_name)
        #return "success"
    #else:
    return message

@celeryObj.task()
def MontlyEnmtReportJob():
    print("Started JOB -> Montly Entertainment Job")
    role = db.session.query(Role).filter(Role.name == 'user').first()
    user_list = role.users
    #print(user_list)

    startMonth = datetime.now().replace(day=1,hour=0,minute=0,second=0)

    for user in user_list:
        bookings = db.session.query(BookTicket)\
        .filter(BookTicket.user_email == user.email, BookTicket.timestamp > startMonth)\
        .all()

        bookingList = []

        for entry in bookings:
            bookingData = {}
            bookingData['showName'] = entry.show[0].name
            bookingData['timeslot'] = datetime.strftime(entry.allocation.timeslot,"%Y-%m-%d, at %I:%M %p")
            bookingData['venueName'] = entry.venue[0].name
            bookingData['venueLoc'] = entry.venue[0].location+", "+entry.venue[0].city
            bookingData['seats'] = entry.allocSeats
            bookingData['price'] = entry.totPrice
            bookingList.append(bookingData)


        reviews = db.session.query(MovieReview).filter(MovieReview.user_email == user.email, MovieReview.timestamp > startMonth).all()
        curUser = {
            "name": user.getName(),
            "email": user.email,
        }
        print(bookings[0])
        msgHtml = create_report(bookingList,reviews,curUser,"html")
        
        attch_name = curUser['name']+"_"+CurMonth+'.pdf'
        send_email(address=user.email, subject="Your "+CurMonth+" Monthly Report is here!",message=msgHtml,attachment=attch_name)
