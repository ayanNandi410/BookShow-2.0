from jinja2 import Template
from weasyprint import HTML
import uuid, os
from datetime import datetime, timedelta
from ..workers import celeryObj
from ..models import User, Role, BookTicket, MovieReview
from ..db import db
from ..send_email import send_email
from celery.schedules import crontab

@celeryObj.on_after_finalize.connect
def alert_month_everyUser(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17,minute=42,day_of_week=2),
        MontlyEnmtReportJob.s(),
        name = 'at every month'
    )


def format_report(temp_file,bookings,reviews,user):
    with open(temp_file) as file:
        template = Template(file.read())
        return template.render(bookings=bookings,reviews=reviews,user=user)
    
def create_report(bookings,reviews,user,type):
    message = format_report('templates/report_template.html',bookings,reviews,user)
    print(message)
    html = HTML(string=message)
    file_name = str(user['name']+"_"+datetime.today().strftime("%d %b %Y"))+'.pdf'
    print(file_name)

    if type=='pdf':
        html.write_pdf(target="files/"+file_name)
    else:
        pass

@celeryObj.task()
def MontlyEnmtReportJob(type='pdf'):
    print("Started JOB -> Montly Entertainment Job")
    role = db.session.query(Role).filter(Role.name == 'user').first()
    user_list = role.users
    #print(user_list)

    startMonth = datetime.now().replace(day=1,hour=0,minute=0,second=0)

    for user in user_list:
        bookings = db.session.query(BookTicket).filter(BookTicket.user_email == user.email, BookTicket.timestamp > startMonth).all()
        reviews = db.session.query(MovieReview).filter(MovieReview.user_email == user.email, MovieReview.timestamp > startMonth).all()
        curUser = {
            "name": user.getName(),
            "email": user.email,
        }
        print(bookings)
        create_report(bookings,reviews,curUser,type)
        #send_email(address=user.email, subject="Hurry! Movies coming up in your local theatres",message="Hey "+ firstName +",\n\nYou haven't checked out the recent releases! Seats booking fast! Go to BookShow and book your favorite show now.")
