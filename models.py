from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(3), unique=True)
