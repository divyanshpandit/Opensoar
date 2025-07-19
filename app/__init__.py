from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # Enable CORS for the app
    CORS(app)
    # Load config
    app.config.from_object('config.Config')

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.incidents import incident_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(incident_bp, url_prefix='/api/incidents')
    return app
