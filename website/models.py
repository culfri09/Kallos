"""
Module defining the database models for the application.
"""
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .import init

class User(init.db.Model, UserMixin):
    """Model representing a user in the application."""

    __tablename__ = 'kallosusers'
    # Defines Users table in db
    id = init.db.Column(init.db.Integer, primary_key=True)
    email = init.db.Column(init.db.String(150), unique=True)
    password = init.db.Column(init.db.String(150))
    first_name = init.db.Column(init.db.String(150))
    company_name = init.db.Column(init.db.String(150))
    job_title = init.db.Column(init.db.String(150))
    department = init.db.Column(init.db.String(150))

    # Establish one-to-many relationship with Answers table
    answers = relationship('Answers', backref='user')

class Answers(init.db.Model):
    """Model representing answers provided by users."""

    __tablename__ = 'usersanswers'
    # Defines Answers table in db
    id = init.db.Column(init.db.Integer, primary_key=True)
    kallosusers_id = init.db.Column(init.db.Integer, ForeignKey('kallosusers.id'))
    benchmark_companies = init.db.Column(init.db.String())
    time_to_fill = init.db.Column(init.db.String())
    demographic_breakdown = init.db.Column(init.db.String())
    leadership_diversity = init.db.Column(init.db.String())
    net_promoter_score = init.db.Column(init.db.String())
    employer_brand_familiarity = init.db.Column(init.db.String())
    timestamp = init.db.Column(init.db.DateTime())
    channels = init.db.Column(init.db.String())
    investment = init.db.Column(init.db.String())
    development = init.db.Column(init.db.String())
    #Defines a relationship with the User table
    user_relation = init.db.relationship('User', backref='user_answers')


class Surveys(init.db.Model):
    """Model representing surveys provided by users."""

    __tablename__ = 'usersurveys'
    # Defines Answers table in db
    id = init.db.Column(init.db.Integer, primary_key=True)
    kallosusers_id = init.db.Column(init.db.Integer, ForeignKey('kallosusers.id'))
    enps = init.db.Column(init.db.Number())
    candidate_rate = init.db.Column(init.db.Number())
    retention_rate = init.db.Column(init.db.Number())
    workplace_rate = init.db.Column(init.db.Number())
    timestamp = init.db.Column(init.db.DateTime())
    #Defines a relationship with the User table
    user_relation = init.db.relationship('User', backref='user_surveys')