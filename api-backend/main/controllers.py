from flask import render_template
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required, roles_accepted, hash_password, current_user
from main.db import db
from main.models import User
from .tasks.alertJob import reminder

def setup_controllers(app):
    
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
        
    @app.route('/test/<vid>')
    def test(vid):
        job = reminder.delay()
        return "success"
        

from flask_security.forms import RegisterForm, ConfirmRegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('first_name', [DataRequired()])
    last_name = StringField('last_name', [DataRequired()])

class ExtendedConfRegisterForm(ConfirmRegisterForm):
    first_name = StringField('first_name', [DataRequired()])
    last_name = StringField('last_name', [DataRequired()])

 