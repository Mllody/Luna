from flask import Flask
from flask_cors import CORS
from .database import Base, engine
from .models import User, Task, Process, Queue, Execution
from routes.auth_routes import auth_bp
from utils.security import configure_jwt


def create_app():
    app = Flask(__name__)
    CORS(app)

    # --- konfiguracja JWT i inicjalizacja bazy danych ---
    configure_jwt(app)
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        print("[LUNA] Baza danych gotowa ✅")

    # --- rejestracja tras (API) ---
    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        return "🚀 LUNA backend (Flask 3.x) działa poprawnie i nowocześnie"

    return app
