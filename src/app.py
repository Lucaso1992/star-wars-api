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

@app.route('/user/<int:user_id>', methods=['GET'])
def load_user(user_id):
    user_query = User.query.filter_by(id = user_id).first()
    if user_query:
        response_body = {
            "msg": "Usuario encontrado",
            "result": user_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "Usuario no existe!"
        }
        return jsonify(response_body), 404

@app.route('/users', methods=['GET'])
def load_characters():
    user_query = User.query.all()
    load_user = [User.serialize() for User in user_query]
    response_body = {
        "msg": "Ok",
        "result": load_user
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


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def load_user_favorites(user_id):
    user_favorites_query = Favorites.query.filter_by(user_fk == user_id).all()
    user_favorites = list(map(lambda item : item.serialize(), user_favorites_query))
    response_body = {
        "msg": "Ok",
        "result": user_favorites
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.json
    user_query = User.query.filter_by(email = request_body["email"]).first()
    if user_query is None:
        create_user = User(email = request_body["email"], password = request_body["password"], is_active = request_body["is_active"])
        db.session.add(create_user)
        db.session.commit()
        response_body = {
             "msg": "Usuario creado con exito"
            }

        return jsonify(response_body), 200
    else:
        response_body = {
             "msg": "Usuario ya existe"
            }
        return jsonify(response_body), 404


@app.route('/planet', methods=['POST'])
def create_planet():
    request_body = request.json
    planet_query = Planet.query.filter_by(name = request_body["name"]).first()
    if planet_query is None:
        create_planet = Planet(name = request_body["name"], url = request_body["url"], climate = request_body["climate"], 
        created = request_body["created"], 
        diameter = request_body["diameter"], 
        gravity = request_body["gravity"], 
        orbital_period = request_body["orbital_period"], 
        population = request_body["population"],
        rotation_period = request_body["rotation_period"],
        surface_water = request_body["surface_water"],
        terrain = request_body["terrain"],
        edited = request_body["edited"],
        favorite = request_body["favorite"],)
        db.session.add(create_user)
        db.session.commit()
        response_body = {
             "msg": "Usuario creado con exito"
            }

        return jsonify(response_body), 200
    else:
        response_body = {
             "msg": "Usuario ya existe"
            }
        return jsonify(response_body), 404


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
    request_body = request.json
    planet_favorite = Favorites(user_fk = request_body["user_id"], planet_fk = planet_id)
    db.session.add(planet_favorite)
    db.session.commit()
    response_body = {
        "msg": "Planeta creado con exito"
    }

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_character(people_id):
    request_body = request.json
    people_favorite = Favorites(user_fk = request_body["user_id"], character_fk = people_id)
    db.session.add(people_favorite)
    db.session.commit()
    response_body = {
        "msg": "Personaje creado con exito"
    }

    return jsonify(response_body), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def create_favorite_vehicle(vehicle_id):
    request_body = request.json
    vehicle_favorite = Favorites(user_fk = request_body["user_id"], vehicle_fk = vehicle_id)
    db.session.add(vehicle_favorite)
    db.session.commit()
    response_body = {
        "msg": "Vehiculo creado con exito"
    }

    return jsonify(response_body), 200


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    request_body = request.json
    vehicle_delete = Favorites.query.filter_by(user_fk = request_body["user_id"], vehicle_fk = vehicle_id).first()
    if vehicle_delete: 
        db.session.delete(vehicle_delete)
        db.session.commit()
        response_body = {
            "msg": "Vehiculo eliminado con exito"
        }
        return jsonify(response_body), 200 
    else: 
        response_body = {
            "msg" : "Vehiculo no existe!"
        }
        return jsonify(response_body), 404 

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    request_body = request.json
    planet_delete = Favorites.query.filter_by(user_fk = request_body["user_id"], planet_fk = planet_id).first()
    if planet_delete: 
        db.session.delete(planet_delete)
        db.session.commit()
        response_body = {
            "msg": "Planeta eliminado con exito"
        }

        return jsonify(response_body), 200 
    else: 
        response_body = {
        "msg" : "Planeta no existe!"
        }
        return jsonify(response_body), 404 

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    request_body = request.json
    character_delete = Favorites.query.filter_by(user_fk = request_body["user_id"], character_fk = people_id).first()
    if character_delete: 
        db.session.delete(character_delete)
        db.session.commit()
        response_body = {
            "msg": "Personaje eliminado con exito"
        }

        return jsonify(response_body), 200 
    else: 
        response_body = {
        "msg" : "Personaje no existe!"
        }
        return jsonify(response_body), 404 


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False) 
