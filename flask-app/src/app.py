from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- Database Configuration from Environment Variables ---
    DB_NAME = os.getenv("DB_NAME", "ipfs_billing")
    DB_USER = os.getenv("DB_USER", "billing_user")
    DB_PASS = os.getenv("DB_PASS", "a_very_secure_password_123!")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    db.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.main)
        
        # Register dashboard blueprint
        from .dashboard_routes import dashboard_bp
        app.register_blueprint(dashboard_bp)
    
    return app
