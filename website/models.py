from .import init
from flask_login import UserMixin

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
