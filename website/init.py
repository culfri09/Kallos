from flask import Flask
import secrets

# Generates a random key with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

def create_app():
    # Creates a Flask application instance
    app = Flask(__name__, template_folder='./template')

    # Sets the secret key
    app.config['SECRET_KEY'] = secret_key

    # Imports blueprints
    from .views import views
    from .auth import auth

    # Registers blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
