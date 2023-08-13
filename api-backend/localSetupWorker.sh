#! /bin/sh

# Activate virtual env
# ../env/bin/activate
export ENV=development
celery -A app.celery worker -l info
deactivate