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
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Hent database URI fra miljøvariabler
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "hemmelignøgle")

    # Initialiser udvidelser
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    from app.models import User, Scan, Analyze, GeneratedDocument, Payment

    # Import routes after initializing extensions
    from app.routes.auth_routes import auth_bp
    from app.routes.documents_routes import document_bp
    from app.routes.analyze_routes import analyze_bp

    # Register blueprints after importing models
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(analyze_bp)

    return app
