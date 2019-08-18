import sqlalchemy
from application import db
from datetime import datetime

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())
    modifiedAt = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())
    description = db.Column(db.Text, nullable=True)
    favorite_things = db.relationship('FavoriteThing', backref='categories',  lazy=True)

    def __repr__(self):
        return f"Category('{self.title}', '{self.description}', '{self.createdAt}')"

class FavoriteThing(db.Model):

    __tablename__ = 'favorite_things'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())
    modifiedAt = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())