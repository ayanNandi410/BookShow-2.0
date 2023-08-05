from jinja2 import Template
from weasyprint import HTML
import uuid, os
from datetime import datetime, timedelta
from ..workers import celeryObj
from ..models import User, Role
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


def format_report(temp_file,data={}):
    with open(temp_file) as file:
        template = Template(file.read())
        return template.render(data=data)
    
def create_report(type,data):
    message = format_report('report_template.html', data=data)
    html = HTML(string=message)
    file_name = str(uuid.uuid4())+'.pdf'
    print(file_name)

    if type=='pdf':
        html.write(target=file_name)
    else:
        pass

@celeryObj.task()
def MontlyEnmtReportJob(type='html'):
    print("Started JOB -> Montly Entertainment Job")
    role = db.session.query(Role).filter(Role.name == 'user').first()
    user_list = role.users
    #print(user_list)

    for user in user_list:
        pass

        #send_email(address=user.email, subject="Hurry! Movies coming up in your local theatres",message="Hey "+ firstName +",\n\nYou haven't checked out the recent releases! Seats booking fast! Go to BookShow and book your favorite show now.")
