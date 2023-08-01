from main.db import db,Base
from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.sql import func
from datetime import datetime
from flask_security import UserMixin, RoleMixin

fsqla.FsModels.set_db_info(db)

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='subquery'))
    
    def getName(self):
        return self.first_name + " " + self.last_name
    
    def getUserName(self):
        return self.username
    
    # Custom User Payload
    def get_security_payload(self):
        rv = super().get_security_payload()

        rv['name'] = self.getName()
        rv['username'] = self.getUserName()
        rv['isAdmin'] = self.has_role('admin')

        return rv
    

##########################################################################

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

languages = db.Table('languages',
    db.Column('lang_id', db.Integer, db.ForeignKey('Language.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class Language(db.Model):
    __tablename__ = 'Language'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    #img_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    location = db.Column(db.String(30))
    city = db.Column(db.String(30))
    capacity = db.Column(db.Integer)
    shows = db.relationship('Show',secondary='Allocation',lazy='subquery', viewonly=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return "< Venue : "+self.name+">"

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    #img_name = db.Column(db.String(50), unique=True)
    rating = db.Column(db.Integer)
    duration = db.Column(db.String(20))
    languages = db.relationship('Language', secondary=languages, lazy='subquery',
        backref=db.backref('show', lazy=True))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('show', lazy=True))
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    venues = db.relationship('Venue',secondary='Allocation',lazy='subquery', viewonly=True)
    reviews = db.relationship('MovieReview', backref='show', lazy='subquery', viewonly=True)

    def __repr__(self):
        return "< Show : "+self.name+">"

class Allocation(db.Model):
    __tablename__ = 'Allocation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('Show.id'), nullable=False)
    timeslot = db.Column(db.DateTime(timezone=True), nullable=False) # contains both date and time of show
    totSeats = db.Column('Total Seats',db.Integer,nullable=False)
    avSeats =db.Column('Available Seats',db.Integer,nullable=False)
    price = db.Column('Ticket Price',db.Numeric(10,2), nullable=False)

    bookings = db.relationship('BookTicket', backref='allocShow',lazy='subquery')
    venue = db.relationship('Venue')
    show = db.relationship('Show')
    #venue = db.relationship('Venue', backref= db.backref('DayAllocation', cascade='all, delete-orphan' ))
    #show = db.relationship('Show', backref= db.backref('DayAllocation', cascade='all, delete-orphan' ))

    def __repr__(self):
        return "< Allocation : "+self.venue.name+","+self.show.name+","+str(self.timeslot)+","+str(self.timeslot)+">"

class BookTicket(db.Model):
    __tablename__ = 'BookTicket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    showAllocId = db.Column(db.Integer,db.ForeignKey('Allocation.id'),nullable=False)
    user_email = db.Column(db.String(40),nullable=False)
    allocSeats = db.Column('Seats Booked',db.Integer,nullable=False)
    totPrice = db.Column('Total Price',db.Numeric(12,2))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    allocation =  db.relationship('Allocation',lazy='subquery', viewonly=True)
    venue = db.relationship('Venue',secondary='Allocation',lazy='subquery', viewonly=True)
    show = db.relationship('Show',secondary='Allocation',lazy='subquery', viewonly=True)

class MovieReview(db.Model):
    __tablename__ = 'MovieReview'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(40),nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('Show.id'),nullable=False)
    comment = db.Column(db.String(220),nullable=False)
    gRating = db.Column(db.Integer,nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    #user =  db.relationship('User',lazy='subquery', viewonly=True)

    def __repr__(self):
        return "< Review : "+str(self.comment)+","+str(self.gRating)+","+self.user_email+">"

class CalcReview(db.Model):
    __tablename__ = 'CalcReview'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id = db.Column(db.Integer, nullable=False)
    oneStarRatings = db.Column(db.Integer, nullable=False)
    twoStarRatings = db.Column(db.Integer, nullable=False)
    threeStarRatings = db.Column(db.Integer, nullable=False)
    fourStarRatings = db.Column(db.Integer, nullable=False)
    fiveStarRatings = db.Column(db.Integer, nullable=False)
    totalRatings = db.Column(db.Integer, nullable=False)
    avRating = db.Column(db.String, nullable=False)
