"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

initial_members = [
    {"first_name":"Jhon", "last_name":"Jackson", "age":33, "lucky_numbers":[7,13,22]}, 
    {"first_name":"Jane", "last_name":"Jackson", "age":33, "lucky_numbers":[10,14,3]},
    {"first_name":"Jimmy", "last_name":"Jackson", "age":5, "lucky_numbers":[1]}
]


# create the jackson family object
# Crear la instancia de FamilyStructure con los miembros iniciales
jackson_family = FamilyStructure(initial_members)

# Verificar los miembros iniciales
# print("Miembros iniciales:", jackson_family.get_all_members())


# for member in initial_members:
#     jackson_family.add_member(member)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    # print("memmmmmbersss...", members)
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def create_member():
    body = request.get_json()
    first_name = body.get("first_name", None)
    last_name = body.get("last_name", None)
    age = body.get("age", None)
    lucky_numbers = body.get("lucky_numbers", None)
    id = body.get("id", None)

    if first_name is None:
        return jsonify({"error": "El first_name es requerido"}), 400
    if last_name is None:
        return jsonify({"error": "El last_name es requerido"}), 400
    if age is None:
        return jsonify({"error": "El age es requerido"}), 400
    if lucky_numbers is None:
        return jsonify({"error": "El lucky_number es requerido"}), 400
    
    member = {
        "first_name": first_name, 
        "last_name": last_name,
        "age": age,
        "lucky_numbers": lucky_numbers
    }
    
    if id is not None: 
        member["id"] = id

    jackson_family.add_member(member)
    return jsonify(member), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

