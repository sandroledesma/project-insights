from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """
    Application factory pattern for creating Flask app instances
    """
    app = Flask(__name__)
    
    # Import configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/insight_engine.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Insight Engine startup')
    
    # Register blueprints
    from project.api import ai_tools_bp, luxury_appliances_bp
    
    app.register_blueprint(ai_tools_bp, url_prefix='/api')
    app.register_blueprint(luxury_appliances_bp, url_prefix='/api')
    
    # Import models to ensure they're registered with SQLAlchemy
    from project.models import AITool, LuxuryAppliance, AggregatedReview
    
    # Create a simple health check route
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Insight Engine API is running'}
    
    return app 