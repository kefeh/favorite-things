from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_type):
    """Constructs the core application"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_type])

    db.init_app(app)
    from .api.routes import test
    app.register_blueprint(test)

    #create tables for our database
    with app.app_context():
        db.create_all()

    return app