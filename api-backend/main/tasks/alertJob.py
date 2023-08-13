from datetime import datetime, timedelta
from ..workers import celeryObj
from ..models import User, Role
from ..db import db
from ..send_email import send_email
from celery.schedules import crontab

@celeryObj.on_after_finalize.connect
def alert_evening_everyUser(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13,minute=30),
        reminder.s(),
        name = 'alertMail at every day'
    )


@celeryObj.task()
def reminder():
    print("Started JOB -> Reminder")
    role = db.session.query(Role).filter(Role.name == 'user').first()
    user_list = role.users
    #print(user_list)

    for user in user_list:
        visited = booked = False
        startDT = datetime.utcnow() - timedelta(hours=17)

        if(user.last_login_at > startDT):
            visited = True
        print(user.email,visited)
        if not visited:
            send_email(address=user.email, subject="Hurry! Movies coming up in your local theatres...",
                        message="Hey "+ user.getFirstName() +",<br/><br/>You haven't checked out the releases today! <br/><br/>Seats booking fast! Go to BookShow and book your favorite show now.")

        