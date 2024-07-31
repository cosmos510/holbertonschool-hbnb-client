import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from db import db
from config import get_config

# Models imports
from models.users import User
from models.amenity import Amenity
from models.place import Place
from models.country import Country
from models.review import Review
from models.city import City

# Logging module import to capture app logs
import logging

# Routes imports
from api.user_api import user_api
from api.country_api import country_api
from api.place_api import place_api
from api.amenities_api import amenities_api
from api.review_api import review_api
from api.cities_api import cities_api
from api.auth import auth
#---------------------------------------------------------------------
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.config.from_object(get_config())

#-------------------------------------------------------------
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
jwt = JWTManager(app)

db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'



swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

# Blueprints imports
app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(user_api)
app.register_blueprint(country_api)
app.register_blueprint(place_api)
app.register_blueprint(amenities_api)
app.register_blueprint(review_api)
app.register_blueprint(cities_api)
app.register_blueprint(auth)

if __name__ == "__main__":
    with app.app_context():

        logging.debug("Creating database tables...")

        # Creation of our tables when app is running
        db.create_all()

        logging.debug("Tables created.")

    # Using specified port (5000)
    port = os.getenv("PORT", 5000)

    logging.debug(f"Starting app on port {port}")

    app.run(debug=True, host='0.0.0.0', port=port)
