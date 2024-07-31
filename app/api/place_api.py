from flask import Blueprint, jsonify, request
from models.place import Place
from models.amenity import Amenity
from persistence.datamanager import DataManager
import json
from flask_jwt_extended import get_jwt, verify_jwt_in_request
place_api = Blueprint("place_api", __name__)
datamanager = DataManager(flag=2)


@place_api.route("/places", methods=["POST", "GET"])
def add_place():
    """
    Endpoint to create and list places.

    POST method:
    Creates a new place with JSON data containing 'name', 'description',
    'address', 'latitude', 'longitude',
    'num_rooms', 'num_bathrooms', 'price_per_night', 'max_guests', 'host_id',
    'amenity_ids', 'city_id'.
    Validates input data and checks for required fields.
    Checks if amenities exist before saving.
    Returns a success message if place is created successfully, or an error
    message if failed.

    GET method:
    Retrieves a list of all places.
    Returns a JSON array of place objects containing 'id', 'name',
    'description', 'address', 'city_id', 'latitude',
    'longitude', 'host_id', 'num_rooms', 'num_bathrooms', 'price_per_night',
    'max_guests', 'amenity_ids'.
    Returns an error message if no places are found.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """
    if request.method == "POST":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403
        place_data = request.get_json()
        if not place_data:
            return jsonify({"Error": "Problem during place creation"})

        name = place_data.get("name")
        description = place_data.get("description")
        address = place_data.get("address")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")
        num_rooms = place_data.get("num_rooms")
        num_bathrooms = place_data.get("num_bathrooms")
        price_per_night = place_data.get("price_per_night")
        max_guests = place_data.get("max_guests")
        host_id = place_data.get("host_id")
        amenity_ids = place_data.get("amenity_ids")
        city_id = place_data.get("city_id")

        if not all([name, description, address, latitude, longitude,
                    num_rooms, num_bathrooms, price_per_night, max_guests,
                    city_id, host_id]):
            return jsonify({"Error": "Missing required field."}), 400

        if not (isinstance(arg, str)
                for arg in (name, description, address)):
            raise TypeError({"Error": "TypeError"})
        if not (isinstance(arg, int)
                for arg in (num_bathrooms, num_rooms, max_guests)):
            raise TypeError({"Error": "TypeError"})
        if not (isinstance(arg, (float, int))
                for arg in (latitude, longitude, price_per_night)):
            raise TypeError({"Error": "TypeError"})

        new_place = Place(name, description, address, city_id, latitude,
                          longitude, host_id, num_rooms, num_bathrooms,
                          price_per_night, max_guests, amenity_ids)
        if not new_place:
            return jsonify({"Error": "setting up new place"}), 500
        else:
            if amenity_ids:
                am_ex = Amenity.query.filter_by(id=amenity_ids).all()
                if not am_ex:
                    return jsonify({"Error": "Amenity does not exist"}), 404
                else:
                    datamanager.save_to_database(new_place)
                    return jsonify({"Success": "Place added"}), 201
            else:
                datamanager.save_to_database(new_place)
                return jsonify({"Success": "Place added"}), 201

    else:
        try:
            places = Place.query.all()
            place_list = []
            for place in places:
                place_list.append({
                    "id": place.id,
                    "name": place.name,
                    "description": place.description,
                    "address": place.address,
                    "city_id": place.city_id,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                    "host_id": place.host_id,
                    "num_rooms": place.num_rooms,
                    "num_bathrooms": place.num_bathrooms,
                    "price_per_night": place.price_per_night,
                    "max_guests": place.max_guests,
                    "amenity_ids": place.amenity_ids
                })
            return jsonify(place_list), 200
        except Exception as e:
            return jsonify({"Error": "No place found"}), 404


@place_api.route("/places/<string:id>", methods=["GET", "DELETE", "PUT"])
def get_place(id):
    """
    Endpoint to retrieve, update or delete a specific place identified by 'id'.

    GET method:
    Retrieves details of the place identified by 'id'.
    Returns a JSON object with 'id', 'name', 'description', 'address',
    'city_id', 'latitude', 'longitude',
    'host_id', 'num_rooms', 'num_bathrooms', 'price_per_night', 'max_guests',
    'amenity_ids'.
    Returns an error message if place is not found.

    DELETE method:
    Deletes the place identified by 'id'.
    Returns a success message upon successful deletion.
    Returns an error message if place is not found.

    PUT method:
    Updates the place identified by 'id' with provided JSON data.
    Returns a success message upon successful update.
    Returns an error message if place is not found or update fails.

    Args:
        id (str): The unique identifier of the place.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """
    place = Place.query.filter_by(id=id).first()

    if request.method == "GET":
        places = datamanager.get_from_database(Place, id)
        if not place:
            return jsonify({"Error": "Place not found"}), 404
        return jsonify({
            "id": str(places.id),
            "name": places.name,
            "description": places.description,
            "address": places.address,
            "city_id": places.city_id,
            "latitude": places.latitude,
            "longitude": places.longitude,
            "host_id": places.host_id,
            "num_rooms": places.num_rooms,
            "num_bathrooms": places.num_bathrooms,
            "price_per_night": places.price_per_night,
            "max_guests": places.max_guests,
            "amenity_ids": places.amenity_ids
        }), 200

    if request.method == "DELETE":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403
        if not place:
            return jsonify({"Error": "Place not found"}), 404
        else:
            datamanager.delete_from_database(Place, id)
            return jsonify({"Success": "Place deleted"}), 200

    if request.method == "PUT":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403
        if not place:
            return jsonify({"Error": "Place not found"}), 404
        place_data = request.get_json()
        place.name = place_data.get("name", place.name)
        place.description = place_data.get("description", place.description)
        place.address = place_data.get("address", place.address)
        place.city_id = place_data.get("city_id", place.city_id)
        place.latitude = place_data.get("latitude", place.latitude)
        place.longitude = place_data.get("longitude", place.longitude)
        place.host_id = place_data.get("host_id", place.host_id)
        place.num_rooms = place_data.get("num_rooms", place.num_rooms)
        place.num_bathrooms = place_data.get("num_bathrooms",
                                             place.num_bathrooms)
        place.price_per_night = place_data.get("price_per_night",
                                               place.price_per_night)
        place.max_guests = place_data.get("max_guests", place.max_guests)
        place.amenity_ids = place_data.get("amenity_ids", place.amenity_ids)
        datamanager.update_database(Place, id, place_data)
        return jsonify({"Success": "Place updated"}), 200
