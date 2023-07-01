from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String, nullable=False, unique=True)
    climate = db.Column(db.String, nullable=False)
    created = db.Column(db.String, nullable=False)
    diameter = db.Column(db.String, nullable=False)
    gravity = db.Column(db.String, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    


class Vehicle(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String, nullable=False, unique=True)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    created = db.Column(db.String, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    length = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String, nullable=False)
    vehicle_class = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    pilots = db.relationship('Pilots', secondary=pilots, lazy='subquery',
        backref=db.backref('vehicle', lazy=True))
    passengers = db.relationship('Passengers', secondary=passengers, lazy='subquery',
        backref=db.backref('vehicle', lazy=True))

   
   

pilots = db.Table(
    "Pilots",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("vehicle_id", db.ForeignKey(Vehicle.id)),
    db.Column("pilot_id", db.ForeignKey(Character.id)),
)

passengers = db.Table(
    "passengers",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("vehicle_id", db.ForeignKey(Vehicle.id)),
    db.Column("passenger_id", db.ForeignKey(Character.id)),
)  
 
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
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
