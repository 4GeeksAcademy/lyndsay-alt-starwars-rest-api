from flask import Blueprint, jsonify, request
from models import db, User, People, Planet, Favorite

api = Blueprint("api", __name__)


def get_current_user_id() -> int:
    return 1


@api.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200


@api.route("/people/<int:people_id>", methods=["GET"])
def get_single_person(people_id: int):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200


@api.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id: int):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@api.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    current_user_id = get_current_user_id()
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    return jsonify([f.serialize() for f in favorites]), 200


@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id: int):
    current_user_id = get_current_user_id()

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    existing = Favorite.query.filter_by(
        user_id=current_user_id, planet_id=planet_id
    ).first()
    if existing:
        return jsonify({"msg": "Planet already in favorites"}), 400

    favorite = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201


@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id: int):
    current_user_id = get_current_user_id()

    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404

    existing = Favorite.query.filter_by(
        user_id=current_user_id, people_id=people_id
    ).first()
    if existing:
        return jsonify({"msg": "Person already in favorites"}), 400

    favorite = Favorite(user_id=current_user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201


@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id: int):
    current_user_id = get_current_user_id()

    favorite = Favorite.query.filter_by(
        user_id=current_user_id, planet_id=planet_id
    ).first()
    if not favorite:
        return jsonify({"msg": "Favorite planet not found for current user"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet removed"}), 200


@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id: int):
    current_user_id = get_current_user_id()

    favorite = Favorite.query.filter_by(
        user_id=current_user_id, people_id=people_id
    ).first()
    if not favorite:
        return jsonify({"msg": "Favorite person not found for current user"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person removed"}), 200


@api.route("/people", methods=["POST"])
def create_person():
    data = request.get_json() or {}
    name = data.get("name")

    if not name:
        return jsonify({"msg": "Field 'name' is required"}), 400

    person = People(
        name=name,
        height=data.get("height"),
        mass=data.get("mass"),
        hair_color=data.get("hair_color"),
        skin_color=data.get("skin_color"),
        eye_color=data.get("eye_color"),
        birth_year=data.get("birth_year"),
        gender=data.get("gender"),
    )
    db.session.add(person)
    db.session.commit()
    return jsonify(person.serialize()), 201


@api.route("/people/<int:people_id>", methods=["PUT"])
def update_person(people_id: int):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404

    data = request.get_json() or {}
    for field in [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
    ]:
        if field in data:
            setattr(person, field, data[field])

    db.session.commit()
    return jsonify(person.serialize()), 200


@api.route("/people/<int:people_id>", methods=["DELETE"])
def delete_person(people_id: int):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404

    db.session.delete(person)
    db.session.commit()
    return jsonify({"msg": "Person deleted"}), 200


@api.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json() or {}
    name = data.get("name")

    if not name:
        return jsonify({"msg": "Field 'name' is required"}), 400

    planet = Planet(
        name=name,
        climate=data.get("climate"),
        population=data.get("population"),
        terrain=data.get("terrain"),
        diameter=data.get("diameter"),
        rotation_period=data.get("rotation_period"),
        orbital_period=data.get("orbital_period"),
    )
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 201


@api.route("/planets/<int:planet_id>", methods=["PUT"])
def update_planet(planet_id: int):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    data = request.get_json() or {}
    for field in [
        "name",
        "climate",
        "population",
        "terrain",
        "diameter",
        "rotation_period",
        "orbital_period",
    ]:
        if field in data:
            setattr(planet, field, data[field])

    db.session.commit()
    return jsonify(planet.serialize()), 200


@api.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id: int):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted"}), 200
