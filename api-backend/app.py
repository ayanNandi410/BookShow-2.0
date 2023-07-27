from main.constants import BASE_URL
from main.init_api import getConfiguredApi
from flask import Flask, render_template
from main.config import LocalDevConfig
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required, roles_accepted, hash_password, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests, secrets, string
from flask_cors import CORS
from main.models import User, Role, RolesUsers
from main.testData import addData
from main.db import db

# template_dir = os.path.abspath(os.getcwd())
# static_dir =  os.path.abspath(os.getcwd())
# print(static_dir)

app = None
api = None


def create_app():
    app = Flask(__name__)

    # Local Development Configuration
    app.config.from_object(LocalDevConfig)

    # Setup Flask-Security
    from main.datastore import user_datastore
    app.security = Security(app, user_datastore)

    db.init_app(app)
    app.app_context().push()


    with app.app_context():
        db.drop_all()
        db.create_all()

        adminUser = app.security.datastore.create_user(
            email="admin@bookshow.com",
            password=hash_password("admin123"),
            username="admin_init"
            )
        app.security.datastore.create_role(name="user")
        app.security.datastore.create_role(name="admin")
        app.security.datastore.add_role_to_user(adminUser,"admin")
        app.security.datastore.commit()
        db.session.commit()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('NotFound.html', errorMessage=e), 404
    
    @app.route('/')
    def home():
        return "<h1>Flask App Running</h1>"
    
    @app.route('/addRole/user/<string:email>')
    def addUserRole(email):
        user = app.security.datastore.find_user(email=email)
        result = app.security.datastore.add_role_to_user(user,"user")
        app.security.datastore.commit()
        db.session.commit()
        if result:
            return "Success"
        else:
            return "Failure"

    @app.route('/addRole/admin/<email>')
    @roles_accepted('admin')
    def addAdminRole(email):
        user = app.security.datastore.find_user(email=email)
        result = app.security.datastore.add_role_to_user(user,"admin")
        app.security.datastore.commit()
        db.session.commit()
        if result:
            return "Success"
        else:
            return "Failure"
 
    
    # attach configured Api's
    getConfiguredApi(app)

    addData(db)

    # allow cross-origin requests
    CORS(app)

    return app, api


app, api = create_app()

if __name__ == '__main__':
    app.run("127.0.0.1", debug=True)
