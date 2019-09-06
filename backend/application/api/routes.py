from flask import Blueprint, request, jsonify
from models import *

print(__name__)
test = Blueprint('test', __name__)

@test.route('/add/category', methods=['POST'])
def hello_world():
    data = request.get_json()
    title = data.get('title')
    desc = data.get('description')

    category = Category(title=title, description=desc)
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify(data={'result': 'success'})
    except Exception as exp:
        print(exp)
        return jsonify(data={'result': 'Failure'})

@test.route('/remove/category', methods=['DELETE'])
def remove_world():
    category = db.session.query(Category).filter(Category.title == "Another").one()
    db.session.delete(category)
    db.session.commit()
    return jsonify(results={'value': "success"})

@test.route('/remove/category', methods=['PUT'])
def update_world():
    category = db.session.query(Category).filter(Category.title == "Another").one()
    category.title = "OhGod"
    db.session.commit()
    return jsonify(results={'value': "success"})