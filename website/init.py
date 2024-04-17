from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager

# Initializes database object
db = SQLAlchemy()
DB_NAME = "database.db"

# Generates a random key with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

def create_app():
    # Creates a Flask application instance
    app = Flask(__name__, template_folder='./template')
    

    # Sets the secret key
    app.config['SECRET_KEY'] = secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    migrate = Migrate(app, db)
    
    # Imports blueprints
    from .views import views
    from .auth import auth

    # Registers blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
 
    from .models import User

    # Creates database
    create_database(app)

    # Sets up Flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Checks if database already exists. If it doesn't exist, creates a new one.
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        with app.app_context():
            db.create_all()

