"""
This module analyzes the web application.
"""
from flask import Flask
import secrets
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Generates a random key with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

# Creates a Flask application instance
app = Flask(__name__, template_folder='./template')

# Sets the secret key
app.config['SECRET_KEY'] = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@localhost:5432/postgres'
db = SQLAlchemy(app)

# Defines the allowed file extensions for each survey
ALLOWED_EXTENSIONS = {
    'pdf': ['npsSurvey', 'candidateExperienceRating', 'retentionSurvey', 'workplaceEnviornmentSurvey']
}

# Set the folder where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_app():     
    # Imports blueprints
    from .views import views
    from .auth import auth
    from .submission import submissions

    # Registers blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(submissions, url_prefix='/')

    from .models import User
    # Sets up Flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

