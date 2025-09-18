from flask import Flask
from config import Config
from models import db
from file_uploads import upload_bp
from sqlalchemy import create_engine
from flask_cors import  CORS
from sqlalchemy.exc import OperationalError
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    # Ensure upload directories exist
    os.makedirs(Config.CHUNK_DIR, exist_ok=True)
    os.makedirs(Config.FINAL_DIR, exist_ok=True)

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(upload_bp, url_prefix="/api/v1")

    return app

def check_database_exists(database_uri):
    try:
        engine = create_engine(database_uri)
        with engine.connect():
            return True
    except OperationalError:
        return False

if __name__ == '__main__':
    app = create_app()

    # Check if database exists before creating tables
    if not check_database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        raise RuntimeError("Database does not exist or is unreachable.")

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
