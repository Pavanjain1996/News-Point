from flask_sqlalchemy import SQLAlchemy
from core import app

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    redirect_url = db.Column(db.String(400), nullable=False)
    data_from = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return headline