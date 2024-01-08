import json

from flask import Blueprint, abort, jsonify, request

from app.controllers.user_controller import UserController

user = Blueprint("user", __name__)


@user.route("/api/v1/users", methods=["GET"])
def users_get():
    users_list = UserController.get_all()
    return jsonify([user.to_dict() for user in users_list])


@user.route("/api/v1/user/<int:user_id>", methods=["GET"])
def user_get(user_id):
    user = UserController.get_user_by_id(user_id)
    if user is None:
        abort(404, f"User with ID {user_id} does not exist")
    return jsonify(user.to_dict())


@user.route("/api/v1/user", methods=["POST"])
def user_post():
    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON format. Must be a JSON object.")
    except (json.JSONDecodeError, ValueError):
        abort(400, "Invalid JSON format. Must be a JSON object.")
    # Extract parameters from the request data
    username = data.get("username")
    password = data.get("password")
    try:
        user = UserController.create(username=username, password=password)
        return jsonify(user)
    except (TypeError, ValueError) as e:
        abort(400, description=str(e))
