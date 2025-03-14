"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicles, Planets
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

@app.route('/api/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([{
        "uid": person.uid,
        "name": person.name,
        "gender": person.gender,
        "hair_color": person.hair_color,
        "eyes_color": person.eyes_color
    } for person in people])

# Obtener una persona por UID
@app.route('/api/people/<uid>', methods=['GET'])
def get_person(uid):
    person = People.query.filter_by(uid=uid).first()
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({
        "uid": person.uid,
        "name": person.name,
        "gender": person.gender,
        "hair_color": person.hair_color,
        "eyes_color": person.eyes_color
    })

# Obtener todos los vehículos
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    return jsonify([{
        "uid": vehicle.uid,
        "name": vehicle.name,
        "length": vehicle.length,
        "max_speed": vehicle.max_speed
    } for vehicle in vehicles])

# Obtener un vehículo por UID
@app.route('/api/vehicles/<uid>', methods=['GET'])
def get_vehicle(uid):
    vehicle = Vehicles.query.filter_by(uid=uid).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify({
        "uid": vehicle.uid,
        "name": vehicle.name,
        "length": vehicle.length,
        "max_speed": vehicle.max_speed
    })

# Obtener todos los planetas
@app.route('/api/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([{
        "uid": planet.uid,
        "name": planet.name,
        "population": planet.population,
        "climate": planet.climate
    } for planet in planets])

# Obtener un planeta por UID
@app.route('/api/planets/<uid>', methods=['GET'])
def get_planet(uid):
    planet = Planets.query.filter_by(uid=uid).first()
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify({
        "uid": planet.uid,
        "name": planet.name,
        "population": planet.population,
        "climate": planet.climate
    })


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
