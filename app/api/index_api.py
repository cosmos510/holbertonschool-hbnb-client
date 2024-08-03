from flask import Flask, render_template, request, Blueprint
from models.city import City
from models.users import User
import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

index_api = Blueprint("index_api", __name__)
place = Blueprint("place", __name__)
auth2 = Blueprint('auth2', __name__)
test = Blueprint('test', __name__)



def fetch_places():
    response = requests.get('http://127.0.0.1:5000/places')
    if response.status_code == 200:
        return response.json()
    return []

def fetch_place_details(place_id):
    response = requests.get(f'http://127.0.0.1:5000/places/{place_id}') 
    if response.status_code == 200:
        return response.json()
    return {}

def fetch_user_details(user_id):
    response2 = requests.get(f'http://127.0.0.1:5000/users/{user_id}')
    if response2.status_code == 200:
        return response2.json()
    return {}

def fetch_place_reviews(place_id):
    response = requests.get(f'http://127.0.0.1:5000/places/{place_id}/reviews')
    if response.status_code == 200:
        return response.json()
    return []
def fetch_city():
    response = requests.get(f'http://127.0.0.1:5000/countries')
    if response.status_code == 200:
        return response.json()
    
    


@index_api.route("/", methods=["GET"])
def index():
    places = fetch_places()
    countries = fetch_city()
    for place in places:
        city = City.query.filter_by(id=place['city_id']).first()
        if city:
            place['city_name'] = city.name
        else:
            place['city_name'] = "Unknown City"
    return render_template('index.html', places=places, countries=countries)

@place.route("/detail/<place_id>", methods=["GET"])
def detail(place_id):
    place = fetch_place_details(place_id)
    user = fetch_user_details(place['host_id'])
    reviews = fetch_place_reviews(place_id)
    if place:
        city = City.query.filter_by(id=place['city_id']).first()
        if city :
            place['city_name'] = city.name
        else:
            place['city_name'] = "Unknown City"
        return render_template('place.html', place=place, user=user, reviews=reviews)
    else:
        return "Place not found", 404

@auth2.route('/login', methods=["GET"])
def login_page():
    return render_template('login.html')

@auth2.route('/login', methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query_filter_by(email=email)
        if user and check_password_hash(user.password, password):
            additional_claims = {"is_admin": user.is_admin}
            access_token = create_access_token(
                identity={'username': email, 'role': user.is_admin},
                additional_claims=additional_claims
            )
            return jsonify(access_token=access_token)
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"error": "Invalid Content-Type"}), 400
