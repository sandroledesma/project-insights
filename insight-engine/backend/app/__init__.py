from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Configure database - using SQLite for easier setup
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///insight_engine.db'  # Changed to SQLite
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Import and register blueprints
    from app.routes.ai_tools import ai_tools_bp
    from app.routes.luxe_appliances import luxe_appliances_bp
    from app.routes.test import test_bp
    from app.routes.debug import debug_bp
    
    app.register_blueprint(ai_tools_bp, url_prefix='/api')
    app.register_blueprint(luxe_appliances_bp, url_prefix='/api')
    app.register_blueprint(test_bp, url_prefix='/api')
    app.register_blueprint(debug_bp, url_prefix='/api')
    
    # Import models to ensure they're registered with SQLAlchemy
    from app.models.ai_tool import AITool
    from app.models.aggregated_review import AggregatedReview
    from app.models.luxe_appliance import LuxeAppliance
    from app.models.luxe_review import LuxeReview
    
    return app 