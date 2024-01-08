from flask import Blueprint, abort, jsonify

from app import app
from app.controllers.shelf_controller import ShelfController

shelf = Blueprint("shelf", __name__)


@shelf.route("/api/v1/shelf/test", methods=["GET"])
def shelf_test():
    try:
        # Create a shelf with valid parameters
        shelf = ShelfController.create(
            number=11,
            region_id=6,
            available_spaces=10,
            bottles_per_shelf=20,
            cellar_id=2,
        )

        return jsonify([shelf.to_dict()])
    except (TypeError, ValueError) as e:
        app.logger.error(f"Type error: {e}")
        abort(400, description=str(e))
