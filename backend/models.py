from sqlalchemy import event
from application import db
from datetime import datetime


def get_doc_info(data):
    return {
        'table_name': data.__tablename__,
        'doc_id': data.id,
        'doc_name': data.title,
    }


def save_data(data):
    db.session.add(data)
    try:
        db.session.commit()
    except Exception as exp:
        print(exp)
        db.session.rollback()
        raise Exception('Unable to save to db')


def get_modified_fields(data):
    """returns a list of fieldChange Objects, each of this Object will have the field_name, the old value and the new value"""

    from sqlalchemy.orm.attributes import get_history
    fields: list = []
    print(data)
    for field in data:
        change = get_history(data, field)
        if change.has_changes():
            old = change.deleted[0]
            new = change.added[0]
            print(field, old, new)


class LoggableMixin:

    @staticmethod
    def log_after_insert(mapper, connection, target):
        #do some stuff for the insert
        data = get_doc_info(target)
        connection.execute(
            AuditLog.__table__.insert(), log_group=data.get('table_name'), log_item=data.get('doc_name'), log_id=data.get('doc_id'), log_action='insert'
        )
        log = AuditLog(log_group=data.get('table_name'), log_item=data.get('doc_name'), log_id=data.get('doc_id'), log_action='insert')
        # save_data(log)
        print(log)

    @staticmethod
    def log_after_update(mapper, connection, target):
        #do some stuff for the insert, maybe saving the changed fields values using get_history
        get_modified_fields(target)
    
    @staticmethod
    def log_after_delete(mapper, connection, target):
        #do some stuff after deletion
        data = get_doc_info(target)
        connection.execute(
            AuditLog.__table__.insert(), log_group=data.get('table_name'), log_item=data.get('doc_name'), log_id=data.get('doc_id'), log_action='delete'
        )
        log = AuditLog(log_group=data.get('table_name'), log_item=data.get('doc_name'), log_id=data.get('doc_id'), log_action='delete')
        # save_data(log)
        print(log)

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
        return f"Category(Title:'{self.title}', '{self.description}', Created_at:'{self.created_at}')"


class FavoriteThing(LoggableMixin, db.Model):

    __tablename__ = 'favorite_things'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Favorite Thing (Title:'{self.title}', '{self.description}', Category: '{self.categories.title}' Created_at:'{self.created_at}')"


class AuditLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(), doc="Time logged or time of transaction")
    log_group = db.Column(db.String(50), nullable=False, doc="Name of the logged Class")
    log_item = db.Column(db.String(50), nullable=False, doc="Name of the logged item")
    log_id = db.Column(db.Integer, nullable=False)
    log_action = db.Column(db.String(50), nullable=False, doc="Name of the action that triggered the log")