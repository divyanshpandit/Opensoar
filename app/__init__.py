from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables from .env (should be in project root)
load_dotenv()

# Initialize extensions outside the app factory
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    # Select configuration based on the FLASK_ENV environment variable
    env = os.environ.get('FLASK_ENV', 'development').lower()
    config_map = {
        'development': 'config.DevelopmentConfig',
        'testing': 'config.TestingConfig',
        'production': 'config.ProductionConfig'
    }
    config_class = config_map.get(env, 'config.DevelopmentConfig')

    # Flask instance, set template/static folder correctly if you deploy with new directory structure
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # Load config object (pulls secret key, DB URI etc. from env or defaults)
    app.config.from_object(config_class)

    # Enable CORS (adjust origins in production!)
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.incidents import incident_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(incident_bp, url_prefix='/api/incidents')

    return app
