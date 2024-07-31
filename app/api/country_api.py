from flask import Blueprint, jsonify, request
from models.country import Country
from models.city import City
from persistence.datamanager import DataManager
import json
import pycountry
from db import db

country_api = Blueprint("country_api", __name__)


@country_api.route("/countries", methods=["POST"])
def add_country():
    """
    Endpoint to add countries to the database using ISO country codes.

    POST method:
    Retrieves ISO country codes using `pycountry` module.
    Creates Country objects for each retrieved country code.
    Commits all Country objects to the database.

    Returns:
        JSON: Success message if countries are added successfully, or
        error message if failed.
    """
    try:
        for country in pycountry.countries:
            new_country = Country(name=country.name, code=country.alpha_2)
            db.session.add(new_country)
        db.session.commit()
        return jsonify({"message": "Countries added successfully"}), 201
    except Exception as e:
        # Rollback changes if an error occurs
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure session is properly closed
        db.session.close()


@country_api.route("/countries", methods=["GET"])
def get_countries():
    """
    Endpoint to retrieve all countries from the database.

    GET method:
    Queries all Country objects from the database.
    Converts each Country object to a dictionary representation.

    Returns:
        JSON: List of dictionaries containing details of all countries.
    """
    countries = Country.query.all()
    country_list = [country.to_dict() for country in countries]
    return jsonify(country_list), 200


@country_api.route("/countries/<country_code>", methods=["GET"])
def get_country(country_code):
    """
    Endpoint to retrieve details of a specific country by its ISO code.

    GET method:
    Uses `pycountry` module to fetch details of the country by its alpha_2
    code.
    Converts the retrieved country details into a dictionary representation.

    Args:
        country_code (str): ISO alpha-2 code of the country.

    Returns:
        JSON: Dictionary containing details of the requested country.
    """
    country = pycountry.countries.get(alpha_2=country_code.upper())

    if country:
        country_details = Country(country.name, country.alpha_2).to_dict()
        return jsonify(country_details), 200
    else:
        return jsonify({"error": "Country not found"}), 404


@country_api.route("/countries/<country_code>/cities", methods=["POST"])
def add_city_to_country(country_code):
    """
    Endpoint to add a city to a specific country.

    POST method:
    Checks if the country exists in the database using its ISO code.
    Retrieves city name from the request JSON data.
    Creates a new City object linked to the identified country.
    Commits the new City object to the database.

    Args:
        country_code (str): ISO alpha-2 code of the country.

    Returns:
        JSON: Dictionary representation of the newly added city.
    """
    country = Country.query.filter_by(code=country_code.upper()).first()
    if not country:
        return jsonify({"error": "Country not found"}), 404

    data = request.get_json()
    city_name = data.get('name')

    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    new_city = City(name=city_name, country_id=country.id)
    db.session.add(new_city)
    db.session.commit()

    return jsonify(new_city.to_dict()), 201


@country_api.route("/countries/<country_code>/cities", methods=["GET"])
def get_country_cities(country_code):
    """
    Endpoint to retrieve all cities belonging to a specific country.

    GET method:
    Retrieves the country from the database using its ISO code.
    Queries all City objects associated with the identified country.
    Converts each City object to a dictionary representation.

    Args:
        country_code (str): ISO alpha-2 code of the country.

    Returns:
        JSON: List of dictionaries containing details of all cities belonging
        to the country.
    """
    country = Country.query.filter_by(code=country_code.upper()).first()
    if country:
        cities = City.query.filter_by(country_id=country.id).all()
        if cities:
            city_list = [city.to_dict() for city in cities]
            return jsonify(city_list), 200
        else:
            return jsonify({"error": "Cities not found"}), 404
    else:
        return jsonify({"error": "Country not found"}), 404
