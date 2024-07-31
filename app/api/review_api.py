from flask import Blueprint, jsonify, request
from models.review import Review
from models.users import User
from models.place import Place
from persistence.datamanager import DataManager
from db import db
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

review_api = Blueprint("review_api", __name__)
datamanager = DataManager(flag=4)


@review_api.route("/places/<string:id>/reviews", methods=["POST", "GET"])
def handle_place_review(id):
    """
    Endpoint to handle creation and retrieval of reviews for a place identified
    by 'id'.

    POST method:
    Creates a new review for the specified place with JSON data containing
    'user_id', 'rating', and 'comment'.
    Validates the input data and checks if the user exists, if the place exists
    and if the user is not the host.
    Returns a success message and the created review data if successful, or an
    error message if failed.

    GET method:
    Retrieves all reviews for the specified place identified by 'id'.
    Returns a JSON array of review objects containing 'id', 'user_id',
    'place_id', 'rating', and 'comment'.
    Returns an error message if no reviews are found for the place.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """
    if request.method == "POST":
        current_user = get_jwt_identity()
        if current_user:
            place_id = id
            review_data = request.get_json()

            if not review_data:
                return jsonify({"Error": "Problem during review creation"}), 400

            user_id = review_data.get("user_id")
            rating = review_data.get("rating")
            comment = review_data.get("comment")

            if not isinstance(rating, int):
                return jsonify({"Error": "rating must be an integer."}), 400

            if not 1 <= rating <= 5:
                return jsonify({"Error": "rating must be between 1 and 5."}), 400

            if not isinstance(comment, str):
                return jsonify({"Error": "comment must be a string."}), 400

            # Validate user and place existence
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            place = Place.query.get(place_id)
            if not place:
                return jsonify({"error": "No place found"}), 404

            # Check if the user is trying to rate their own place
            if place.host_id == user_id:
                return jsonify({"error": "Can't rate your own place"}), 404

            # Check if the user has already reviewed this place
            existing_review = Review.query.filter_by(user_id=user_id,
                                                    place_id=place_id).first()
            if existing_review:
                return jsonify({"error": "You can't review the" +
                                "same place twice"}), 404

            new_review = Review(user_id=user_id, place_id=place_id,
                                rating=rating, comment=comment)

            try:
                db.session.add(new_review)
                db.session.commit()
                return jsonify({"message": "Review added successfully",
                                "review": new_review.to_dict()}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
            finally:
                db.session.close()

    elif request.method == "GET":
        reviews = Review.query.filter_by(place_id=id).all()
        if reviews:
            reviews_list = [review.to_dict() for review in reviews]
            return jsonify(reviews_list), 200
        else:
            return jsonify({"error": "No reviews found for this place"}), 404


@review_api.route("/users/<string:id>/reviews", methods=['GET'])
def user_review(id):
    """
    Retrieves all reviews associated with a specific user identified by 'id'.

    GET method:
    Retrieves all reviews associated with the user identified by 'id'.
    Returns a JSON array of review objects containing 'id', 'user_id',
    'place_id', 'rating', and 'comment'.
    Returns an error message if no reviews are found for the user.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "No user found"}), 404

        reviews = Review.query.filter_by(user_id=id).all()

        review_list = [review.to_dict() for review in reviews]
        return jsonify(review_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@review_api.route("/reviews/<string:id>", methods=['GET', 'PUT', 'DELETE'])
def review_info(id):
    """
    Retrieves, updates, or deletes a specific review identified by 'id'.

    GET method:
    Retrieves the details of the review identified by 'id'.
    Returns a JSON object with 'id', 'user_id', 'place_id', 'rating', and
    'comment'.
    Returns an error message if no review is found.

    PUT method:
    Updates the details of the review identified by 'id' with provided
    JSON data.
    Returns a success message and the updated review data if successful, or
    an error message if failed.

    DELETE method:
    Deletes the review identified by 'id'.
    Returns a success message upon successful deletion.

    Args:
        id (str): The unique identifier of the review.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """

    try:
        review = Review.query.get(id)

        if not review:
            return jsonify({"error": "No review found"}), 404

        if request.method == "GET":
            return jsonify(review.to_dict()), 200

        if request.method == "PUT":
            review_data = request.get_json()
            review.rating = review_data.get("rating", review.rating)
            review.comment = review_data.get("comment", review.comment)
            db.session.commit()
            return jsonify({"Success": "Review updated!",
                            "review": review.to_dict()}), 200

        if request.method == "DELETE":
            db.session.delete(review)
            db.session.commit()
            return jsonify({"Success": "The review has been removed" +
                            "successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()
