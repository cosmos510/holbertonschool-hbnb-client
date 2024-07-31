from flask import Blueprint, jsonify, request
from models.amenity import Amenity
from persistence.datamanager import DataManager
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

amenities_api = Blueprint("amenities_api", __name__)
datamanager = DataManager(flag=3)


@amenities_api.route("/amenities", methods=["POST", 'GET'])
def add_amenity():
    """
    Endpoint to manage amenities in the database.

    POST method:
    Creates a new amenity based on JSON data provided in the request body.
    Checks if the amenity already exists.
    Saves the new amenity to the database using DataManager.

    Returns:
        JSON: Success message if amenity is added successfully, or error
        message if failed.

    GET method:
    Retrieves all amenities from the database.

    Returns:
        JSON: List of dictionaries containing details of all amenities.
    """
    
    if request.method == "POST":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403
        amenity_data = request.get_json()

        if not amenity_data:
            return jsonify({"Error": "Problem during amenity creation."}), 400

        name = amenity_data.get("name")

        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        new_amenity = Amenity(name)

        if not new_amenity:
            return jsonify({"Error": "setting up new amenity"}), 500
        else:
            existing_amenities = Amenity.query.filter_by(name=name).first()
            if existing_amenities:
                return jsonify({"Error": "Amenity already exists"}), 409

            new_amenity = Amenity(name=name)

            datamanager.save_to_database(new_amenity)
            return jsonify({"Success": "Amenity added"}), 201
    else:
        try:
            amenities = Amenity.query.all()
            amenity_list = []
            for amenity in amenities:
                amenity_list.append({
                    "id": amenity.id,
                    "name": amenity.name
                })
            return jsonify(amenity_list), 200
        except Exception as e:
            return jsonify({"Error": "No amenity found"}), 404


@amenities_api.route("/amenities/<string:id>",
                     methods=['GET', 'DELETE', 'PUT'])
def get_amenity(id):
    """
    Endpoint to retrieve, update, or delete a specific amenity by its ID.

    GET method:
    Retrieves details of the amenity by its ID from the database.

    Returns:
        JSON: Dictionary containing details of the requested amenity, or
        error message if amenity is not found.

    DELETE method:
    Deletes the amenity from the database based on its ID.

    Returns:
        JSON: Success message if amenity is deleted successfully, or error
        message if amenity is not found.

    PUT method:
    Updates details of the amenity based on JSON data provided in the request
    body.

    Returns:
        JSON: Success message if amenity is updated successfully, or error
        message if update failed.
    """
    amenities = Amenity.query.filter_by(id=id).first()

    if request.method == "GET":
        if amenities:
            return jsonify({"id": str(amenities.id),
                            "name": amenities.name}), 200

        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404

    if request.method == "DELETE":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403
        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404
        else:
            datamanager.delete_from_database(Amenity, id)
            return jsonify({"Success": "Amenity deleted"}), 200

    if request.method == "PUT":

        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404

        amenity_data = request.get_json()
        amenities.name = amenity_data.get("name", amenities.name)

        try:
            datamanager.update_database(Amenity, id, amenity_data)
            return jsonify({"Success": "Amenity updated"}), 200
        except Exception as e:
            return jsonify({"Error": "An error occurred"}), 500
