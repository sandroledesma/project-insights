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
    """
    Application factory pattern for Flask app initialization
    """
    app = Flask(__name__)
    
    # Configure database - using SQLite for easier setup
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'sqlite:///insight_engine.db'  # Changed to SQLite
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)  # Enable CORS for all routes
    
    # Register blueprints
    from app.routes.ai_tools import ai_tools_bp
    app.register_blueprint(ai_tools_bp, url_prefix='/api')
    
    return app 