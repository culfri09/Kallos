from .import init
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(init.db.Model, UserMixin):
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

    #Defines a relationship with the User table
    user_relation = init.db.relationship('User', backref='user_answers')