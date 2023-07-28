from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    favorite = db.relationship("Favorites", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String, nullable=False, unique=True)
    climate = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    diameter = db.Column(db.String, nullable=False)
    gravity = db.Column(db.String, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    favorite = db.relationship("Favorites", backref="planet", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "climate": self.climate,
            "created": self.created,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            "edited": self.edited
            
            # do not serialize the password, its a security breach
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String, nullable=False, unique=True)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    length = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String, nullable=False)
    vehicle_class = db.Column(db.String, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    favorite = db.relationship("Favorites", backref="vehicle", lazy=True)


    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "cargo_capacity": self.cargo_capacity,
            "created": self.created,
            "crew": self.crew,
            "manufacturer": self.manufacturer,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "edited": self.edited

            # do not serialize the password, its a security breach
        }
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String, nullable=False)
    skin_color = db.Column(db.String, nullable=False)
    eye_color = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    homeworld = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    favorite = db.relationship("Favorites", backref="character", lazy=True)
    
    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "created": self.created,
            "edited": self.edited
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_fk = db.Column(db.Integer, db.ForeignKey("planet.id"))
    vehicle_fk = db.Column(db.Integer, db.ForeignKey("vehicle.id"))
    character_fk = db.Column(db.Integer, db.ForeignKey("character.id"))


    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_fk": self.user_fk,
            "planet_fk": self.planet_fk,
            "vehicle_fk": self.vehicle_fk,
            "character_fk": self.character_fk
            # do not serialize the password, its a security breach
        }