from celery import Celery
from flask import current_app as app

celeryObj = Celery("Application Jobs")

class ContextTask(celeryObj.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run( *args, **kwargs)