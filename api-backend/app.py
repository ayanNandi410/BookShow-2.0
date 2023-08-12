from main.constants import BASE_URL
from main.controllers import *
from flask import Flask, render_template
from main.config import LocalDevConfig
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required, roles_accepted, hash_password, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from main.workers import celeryObj, ContextTask
import os, json
import requests, secrets, string
from flask_cors import CORS
from main.models import User, Role, RolesUsers
from main.testData import addData
from main.db import db
from main.tasks.alertJob import reminder
from flask_caching import Cache

# template_dir = os.path.abspath(os.getcwd())
# static_dir =  os.path.abspath(os.getcwd())
# print(static_dir)

app = None
api = None
celery = None
BASE_URL = "http://127.0.0.1:5000"

def create_app():
    app = Flask(__name__)

    # Local Development Configuration
    app.config.from_object(LocalDevConfig)

    # allow cross-origin requests
    CORS(app)

    
    # attach configured Api's
    from main.init_api import getConfiguredApi
    api = getConfiguredApi(app)

    # Setup Flask-Security
    from main.datastore import user_datastore
    app.security = Security(app, user_datastore, register_form=ExtendedRegisterForm, confirm_register_form=ExtendedConfRegisterForm)

    celery = celeryObj
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )

    celery.Task = ContextTask
    app.config.enable_utc = True
    app.app_context().push()


    db.init_app(app)
    app.app_context().push()

    #cache = Cache(app)
    #app.app_context().push()
    from main.cachedTasks import cache
    cache.init_app(app)
    cache.clear()

    with app.app_context():
        db.drop_all()
        db.create_all()

        adminUser = app.security.datastore.create_user(
            first_name = "Admin",
            last_name = "User 1",
            username = "admin1BookShow",
            email="admin@bookshow.com",
            password="admin123"
            )
        app.security.datastore.create_role(name="user")
        app.security.datastore.create_role(name="admin")
        app.security.datastore.add_role_to_user(adminUser,"admin")
        app.security.datastore.commit()
        db.session.commit()
 
    setup_controllers(app)

    addData(db)
    print("-------------------- Test Data Added ----------------------")

    return app, celery, api


app, celery, api = create_app()

# import requests

# adminUserDetails = {}
# adminUserDetails['first_name'] = "Admin"
# adminUserDetails['last_name'] = "User 1"
# adminUserDetails['username'] = "admin1BookShow"
# adminUserDetails['email'] = "admin@bookshow.com"
# adminUserDetails['password'] = "admin123"

# res1 = requests.post(BASE_URL+"/register",data=json.dumps(adminUserDetails))
# print("-------------- Add Admin User: "+res1+" -------------------")

# res2 = requests.get(BASE_URL+"/addRole/admin/admin@bookshow.com")
# print("-------------- Add Role to Admin User: "+res1+" -------------------")


if __name__ == '__main__':
    app.run(BASE_URL[7:16], debug=True)
