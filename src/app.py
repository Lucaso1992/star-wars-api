"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

    
@app.route('/people', methods=['GET'])
def load_character():
    character_query = Character.query.all()
    load_character = list(map(lambda item : item.serialize(), character_query))
    response_body = {
        "msg": "Ok",
        "result": load_character
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def people_id(people_id):
    people_query = Character.query.filter_by(id = people_id ).first()
    response_body = {
        "msg": "Ok",
        "result": people_query
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def load_planet():
    planet_query = Planet.query.all()
    planet = list(map(lambda item : item.serialize(), planet_query))
    response_body = {
        "msg": "Ok",
        "result": load_planet
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def planet_id(planet_id):
    planet_query = Planet.query.filter_by(id = planet_id ).first()
    response_body = {
        "msg": "Ok",
        "result": planet_query
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def load_user():
    user_query = User.query.all()
    user = list(map(lambda item : item.serialize(), user_query))
    response_body = {
        "msg": "Ok",
        "result": load_user
    }

    return jsonify(response_body), 200


@app.route('/users/favorites', methods=['GET'])
def load_user_favorites():
    user_favorites_query = User.Favorites.query.all()
    user_favorites = list(map(lambda item : item.serialize(), user_favorites_query))
    response_body = {
        "msg": "Ok",
        "result": load_user_favorites
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False) 
