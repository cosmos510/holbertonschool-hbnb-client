from flask import Flask, render_template, request, Blueprint
from models.city import City
import requests
index_api = Blueprint("index_api", __name__)
place = Blueprint("place", __name__)



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


@index_api.route("/", methods=["GET"])
def index():
    places = fetch_places()
    for place in places:
        city = City.query.filter_by(id=place['city_id']).first()
        if city:
            place['city_name'] = city.name
        else:
            place['city_name'] = "Unknown City"
    return render_template('index.html', places=places)

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
