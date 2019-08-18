from sqlalchemy import event
from application import db
from datetime import datetime

class LoggableMixin:

    @staticmethod
    def log_after_insert(mapper, connection, target):
        #do some stuff for the insert
        from pprint import pprint
        print("Inserted ##########################################")
        pprint(target)
        pprint(connection)
        pprint(mapper)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    @staticmethod
    def log_after_update(mapper, connection, target):
        #do some stuff for the insert, maybe saving the changed fields values using get_history
        from pprint import pprint
        print('Updated ############################################')
        pprint(target)
        pprint(connection)
        pprint(mapper)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    
    @staticmethod
    def log_after_delete(mapper, connection, target):
        #do some stuff after deletion
        from pprint import pprint
        print('Deleted #############################################')
        pprint(target)
        pprint(connection)
        pprint(mapper)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "after_insert", cls.log_after_insert)
        event.listen(cls, "after_update", cls.log_after_update)
        event.listen(cls, "after_delete", cls.log_after_delete)


class Category(LoggableMixin, db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    description = db.Column(db.Text, nullable=True)
    favorite_things = db.relationship('FavoriteThing', backref='categories',  lazy=True)

    def __repr__(self):
        return f"Category(Title:'{self.title}', '{self.description}', Created_at:'{self.createdAt}')"

class FavoriteThing(LoggableMixin, db.Model):

    __tablename__ = 'favorite_things'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Favorite Thing (Title:'{self.title}', '{self.description}', Category: '{self.categories.title}' Created_at:'{self.createdAt}')"


class AuditLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(), doc="Time logged or time of transaction")
    log_name = db.Column(db.String(50), nullable=False, doc="Name of the logged field")
    log_id = db.Column(db.Integer, nullable=False)