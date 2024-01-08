import json

from flask import Blueprint, abort, jsonify, request
from flask_login import login_required
from sqlalchemy.exc import DataError

from app.controllers.wine_controller import (
    WineController,
)
from app.models.Wine import WineType

wine = Blueprint("wine", __name__)


@wine.route("/api/v1/wines", methods=["GET"])
def wines_get():
    return jsonify([wine.to_dict() for wine in WineController.get_all()])


@wine.route("/api/v1/wine", methods=["POST"])
@login_required
def wine_post():
    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON format. Must be a JSON object.")
    except (json.JSONDecodeError, ValueError):
        abort(400, "Invalid JSON format. Must be a JSON object.")
    # Extract parameters from the request data
    vineyard = data.get("vineyard")
    name = data.get("name")
    wine_type = data.get("wine_type")
    year = data.get("year")
    region_id = data.get("region_id")
    description = data.get("description")
    community_rating = data.get("community_rating")
    label_photo = data.get("label_photo")
    price = data.get("price")
    archived = data.get("archived")

    try:
        wine_type_obj = WineType[wine_type]
    except KeyError:
        abort(
            400,
            f"Wine type must be one of: {', '.join(WineType.__members__.keys())}",
        )

    try:
        new_wine = WineController.create(
            vineyard=vineyard,
            name=name,
            wine_type=wine_type_obj,
            year=year,
            region_id=region_id,
            description=description,
            community_rating=community_rating,
            label_photo=label_photo,
            price=price,
            archived=archived,
        )

    except DataError as e:
        if "Data too long for column 'label_photo'" in str(e):
            abort(400, "label_photo url must be less than 255 characters")
    except TypeError as e:
        abort(400, e)
    except ValueError as e:
        abort(400, e)

    return jsonify({"message": "Wine created successfully", "wine": new_wine.to_dict()})


@wine.route("/api/v1/wine/<int:wine_id>", methods=["GET"])
def wine_get(wine_id):
    wine = WineController.get_by_id(wine_id)
    if wine is None:
        abort(404, f"Wine with ID {wine_id} does not exist")
    return jsonify(wine.to_dict())


@wine.route("/api/v1/wine/<int:wine_id>", methods=["DELETE"])
def wine_delete(wine_id):
    try:
        WineController.delete_by_id(wine_id)
    except ValueError as e:
        abort(404, e)
    return jsonify({"message": "Wine deleted successfully"})
