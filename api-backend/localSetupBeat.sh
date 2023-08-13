#! /bin/sh

# Activate virtual env
# ../env/bin/activate
export ENV=development
celery -A app.celery beat --max-interval 1 -l info
deactivate