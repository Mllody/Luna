import os
from datetime import timedelta
from flask_jwt_extended import JWTManager, create_access_token
from passlib.context import CryptContext

# --- konfiguracja kontekstu haszowania ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def configure_jwt(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "luna_secret_key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    jwt = JWTManager(app)
    return jwt

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(username: str, role: str) -> str:
    return create_access_token(identity={"username": username, "role": role})
