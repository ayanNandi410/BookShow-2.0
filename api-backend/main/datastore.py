from flask_security import SQLAlchemyUserDatastore
from main.models import Role, User
from .db import db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)