from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# 🔹 API Endpoint: Register en ny bruger
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if not first_name or not last_name or not email or not password:
        return jsonify({'message': 'Alle felter skal udfyldes'}), 400

    # Tjek om brugeren allerede eksisterer
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email er allerede i brug'}), 409

    # Hash password
    new_user = User(first_name=first_name, last_name=last_name, email=email)
    new_user.set_password(password)  # Hash password korrekt

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Bruger oprettet succesfuldt'}), 201

from flask_jwt_extended import create_access_token

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200

    return jsonify({'message': 'Ugyldigt login'}), 401
