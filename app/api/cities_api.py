from flask import Blueprint, jsonify, request
from models.city import City
from persistence.datamanager import DataManager
import json
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

import os

datamanager = DataManager(flag=5)
cities_api = Blueprint("cities_api", __name__)


@cities_api.route("/cities", methods=["POST", 'GET'])
def cities():
    """
    Endpoint to manage cities in the database.

    POST method:
    Creates a new city based on JSON data provided in the request body.
    Checks if the city already exists.
    Saves the new city to the database using DataManager.

    Returns:
        JSON: Success message if city is added successfully, or error message
        if failed.

    GET method:
    Retrieves all cities from the database.

    Returns:
        JSON: List of dictionaries containing details of all cities.
    """
    if request.method == "POST":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403
        city_data = request.get_json()
        if not city_data:
            return jsonify({"Error": "Problem during city creation."}), 400

        name = city_data.get("name")
        country = city_data.get("country_id")

        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        new_city = City(name, country)

        if not new_city:
            return jsonify({"Error": "setting up new city"}), 500
        else:
            existing_cities = City.query.filter_by(name=name).first()
            if existing_cities:
                return jsonify({"Error": "City already exists"}), 409

            new_city = City(name=name, country_id=country)

            datamanager.save_to_database(new_city)
            return jsonify({"Success": "City added"}), 201

    if request.method == "GET":
        try:
            cities = City.query.all()
            city_list = []
            for city in cities:
                city_list.append({
                    "id": city.id,
                    "name": city.name,
                    "country_id": city.country_id
                })
            return jsonify(city_list), 200
        except Exception as e:
            return jsonify({"Error": "No city found"}), 404


@cities_api.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def get_city(city_id):
    """
    Endpoint to retrieve, update, or delete a specific city by its ID.

    GET method:
    Retrieves details of the city by its ID from the database.

    Returns:
        JSON: Dictionary containing details of the requested city, or error
        message if city is not found.

    PUT method:
    Updates details of the city based on JSON data provided in the request
    body.

    Returns:
        JSON: Success message if city is updated successfully, or error message
        if failed.

    DELETE method:
    Deletes the city from the database based on its ID.

    Returns:
        JSON: Success message if city is deleted successfully, or error message
        if city is not found.
    """
    if request.method == "GET":
        city = City.query.filter_by(id=city_id).first()

        if city:
            return jsonify({"id": str(city.id),
                            "name": city.name,
                            "country_id": city.country_id}), 200
        return jsonify({"Error": "City not found"}), 404

    if request.method == "PUT":
        city_data = request.get_json()

        if not city_data:
            return jsonify({"Error": "Problem during city update."}), 400

        name = city_data.get("name")
        country = city_data.get("country_id")

        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        city = City.query.filter_by(id=city_id).first()
        if not city:
            return jsonify({"Error": "City not found"}), 404

        city.name = name
        city.country_id = country

        datamanager.update_database(City, city_id, city_data)
        return jsonify({"Success": "City updated"}), 200

    if request.method == "DELETE":
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        city = City.query.filter_by(id=city_id).first()
        if not city:
            return jsonify({"Error": "City not found"}), 404
        datamanager.delete_from_database(City, city_id)
        return jsonify({"Success": "City deleted"}), 200
