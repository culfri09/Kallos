

# 1. conectarse a la base de datos

# 2. insertar row con data en la tabla User

# 3. Cerrar conexion







from flask import Flask

from flask_sqlalchemy import SQLAlchemy




# Initializes database object
db = SQLAlchemy()


def create_app():
    # Creates a Flask application instance
    app = Flask(__name__, template_folder='./template')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # PostgreSQL connection URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@localhost:5432/postgres'

    db.init_app(app)

    try:
    # Try to create a temporary connection to check if it's successful
        db.session.connection().execute("SELECT 1")
        print("Connection to the database successful!")
    except Exception as e:
        print("Failed to connect to the database:", e)


    return app

