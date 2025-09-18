from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.String(100), unique=True, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    mime_type =db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
