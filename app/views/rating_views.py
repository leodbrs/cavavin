import json

from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required

from app.controllers.rating_controller import RatingController
from app.controllers.wine_controller import WineController

rating = Blueprint("rating", __name__)


@rating.route("/api/v1/rating", methods=["GET"])
def ratings_get():
    ratings = RatingController.get_all()
    return jsonify([rating.to_dict() for rating in ratings])


@rating.route("/api/v1/rating", methods=["POST"])
@login_required
def post():
    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON format. Must be a JSON object.")
    except (json.JSONDecodeError, ValueError):
        abort(400, "Invalid JSON format. Must be a JSON object.")
    # Extract parameters from the request data
    user_id = data.get("user_id")
    wine_id = data.get("wine_id")
    value = data.get("value")
    text = data.get("text")

    try:
        new_rating = RatingController.create(
            user_id=user_id,
            wine_id=wine_id,
            value=value,
            text=text,
        )
        WineController.update_community_rating_by_id(wine_id)
    except TypeError as e:
        abort(400, str(e))
    except ValueError as e:
        abort(400, str(e))

    return jsonify(
        {"message": "Rating created successfully.", "rating": new_rating.to_dict()}
    ), 201


@rating.route("/api/v1/rating/<int:rating_id>", methods=["DELETE"])
@login_required
def delete(rating_id):
    rating = RatingController.get_by_id(rating_id)
    wine_id = rating.wine_id

    if not rating.user_id == current_user.id:
        abort(403, "You can only delete your own ratings.")

    try:
        RatingController.delete_by_id(rating_id)
        WineController.update_community_rating_by_id(wine_id)
    except TypeError as e:
        abort(400, str(e))
    except ValueError as e:
        abort(400, str(e))

    return jsonify({"message": "Rating deleted successfully."}), 200
