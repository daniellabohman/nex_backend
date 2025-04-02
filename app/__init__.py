import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS

# Initialiser SQLAlchemy og Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Indlæs miljøvariabler fra .env
    load_dotenv()

    # Opret Flask-applikationen
    app = Flask(__name__)

    # Enable Cross-Origin Resource Sharing (CORS) for the specified frontend URL
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Hent database URI fra miljøvariabler
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "hemmelignøgle")  # Default secret key for JWT if not set

    # Initialize the database and migration tools
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize JWT Manager for authentication
    JWTManager(app)

    # Import models after initializing db
    from app.models import User, Scan, Analyze, GeneratedDocument, Payment

    # Import routes after initializing extensions
    from app.routes.auth_routes import auth_bp
    from app.routes.documents_routes import document_bp
    from app.routes.analyze_routes import analyze_bp
    from app.routes.scan_routes import scan_bp  # <-- Import the new scan routes

    # Register blueprints for the routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(scan_bp)  # <-- Register the scan blueprint

    # Optionally: Add error handling or logging here if needed

    return app
