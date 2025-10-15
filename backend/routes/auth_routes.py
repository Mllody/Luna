from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import SessionLocal
from app.models import User
from utils.security import hash_password, verify_password, create_token


auth_bp = Blueprint("auth", __name__)

# --- Logowanie ---
@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return jsonify({"error": "Nieprawidłowy login lub hasło"}), 401

    token = create_token(user.username, user.role)
    return jsonify({"access_token": token, "role": user.role}), 200


# --- Rejestracja użytkownika (tylko admin) ---
@auth_bp.route("/api/auth/register", methods=["POST"])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"error": "Brak uprawnień"}), 403

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "operator")

    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        return jsonify({"error": "Użytkownik już istnieje"}), 400

    new_user = User(username=username, password=hash_password(password), role=role)
    db.add(new_user)
    db.commit()

    return jsonify({"message": f"Utworzono użytkownika {username}"}), 201
