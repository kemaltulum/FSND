import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
GET /drinks
    public endpoint
    retrieves drinks with their short representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure

'''
@app.route('/drinks', methods=['GET'])
def retrieve_drinks():
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404, 'No drinks found')

    drinks = list(map(lambda drink: drink.short(), drinks))

    return jsonify({
        "success": True,
        "drinks": drinks
    })


'''
    GET /drinks-detail
    requires the 'get:drinks-detail' permission
    retrieves drinks with their long representation (For Barista Role)
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_with_detail(payload):
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404, 'No drinks found')

    drinks = list(map(lambda drink: drink.long(), drinks))

    return jsonify({
        "success": True,
        "drinks": drinks
    })


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if not title or not recipe:
        abort(400, 'Title or recipe is missing')

    if not isinstance(recipe, list):
        recipe = [recipe]

    try:
        new_drink = Drink(title=title, recipe=str(json.dumps(recipe)))
        new_drink.insert()
    except Exception as e:
        print(e)
        abort(400, "New drink cannot be created due to violation on unique constraint: drink.title")

    
    return jsonify({
        "success": True,
        "drinks": [new_drink.long()]
    })


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):

    updated_drink = Drink.query.get(id)

    if not updated_drink:
        abort(404, 'Drink with id: ' + str(id) + ' could not be found.')

    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title:
        updated_drink.title = title
    if recipe:
        updated_drink.recipe = recipe

    updated_drink.update()

    return jsonify({
        "success": True,
        "drinks": [updated_drink.long()]
    })

'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):

    deleted_drink = Drink.query.get(id)

    if not deleted_drink:
        abort(404, 'Drink with id: ' + str(id) + ' could not be found.')

    deleted_drink.delete()

    return jsonify({
        "success": True,
        "delete": id
    })

def get_error_message(error, default_message):
    try:
        return error.description
    except:
        return default_message

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": get_error_message(error, "unprocessable"),
        }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": get_error_message(error, "resource not found")
        }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": get_error_message(error, "bad request")
        }), 400

@app.errorhandler(AuthError)
def auth_error(auth_error):
    return jsonify({
        "success": False, 
        "error": auth_error.status_code,
        "message": auth_error.error['description']
        }), auth_error.status_code
