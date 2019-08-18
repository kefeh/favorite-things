from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234567890QWERTYUIOP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:myboy12tobe12@localhost:3306/brightcore'

db = SQLAlchemy(app)