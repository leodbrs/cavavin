from flask import Blueprint, abort, jsonify, request
from flask_login import login_required

from app import app
from app.controllers.bottle_controller import BottleController
from app.controllers.shelf_controller import ShelfController
from app.controllers.wine_controller import WineController

bottle = Blueprint("bottle", __name__)


@bottle.route("/api/v1/bottle/test", methods=["GET"])
def bottle_test():
    try:
        bottle = BottleController.create(1, 1)
        return jsonify([bottle.to_dict()])
    except (TypeError, ValueError) as e:
        app.logger.error(f"Type error: {e}")
        abort(400, description=str(e))


@bottle.route("/api/v1/bottle/<int:bottle_id>", methods=["DELETE"])
@login_required
def delete(bottle_id):
    try:
        BottleController.delete(bottle_id)
        return jsonify({"success": True, "message": "Bottle deleted successfully."})
    except (TypeError, ValueError) as e:
        app.logger.error(f"Type error: {e}")
        abort(400, description=str(e))


@bottle.route("/api/v1/bottle", methods=["POST"])
@login_required
def bottle_post():
    try:
        wine_id = request.json.get("wine_id")
        shelf_id = request.json.get("shelf_id")

        if not isinstance(wine_id, int):
            raise TypeError("Wine ID must be an integer")

        wine = WineController.get_by_id(wine_id)
        if not wine:
            raise ValueError(f"Wine with ID {wine_id} does not exist")

        if not isinstance(shelf_id, int):
            raise TypeError("Shelf ID must be an integer")

        shelf = ShelfController.get_by_id(shelf_id)
        if not shelf:
            raise ValueError(f"Shelf with ID {shelf_id} does not exist")

        if shelf.region_id != wine.region_id:
            raise ValueError("Shelf and wine must belong to the same region")

        bottle = BottleController.create(wine_id, shelf_id)
        return jsonify(
            {
                "success": True,
                "message": "Bottle created successfully.",
                "bottle": bottle.to_dict(),
            }
        )
    except (TypeError, ValueError) as e:
        app.logger.error(f"Type error: {e}")
        abort(400, description=str(e))
