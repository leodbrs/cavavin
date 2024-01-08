import json

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.controllers.user_controller import UserController
from app.forms import LoginForm, SignupForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
@auth.route("/api/v1/login", methods=["POST"])
def login():
    if request.path.startswith("/api/"):
        if current_user.is_authenticated:
            return jsonify({"error": "Already logged in."}), 409
        try:
            data = request.get_json(force=True)
            if not isinstance(data, dict):
                raise ValueError("Invalid JSON format. Must be a JSON object.")
        except (json.JSONDecodeError, ValueError):
            return jsonify(
                {"error": "Invalid JSON format. Must be a JSON object."}
            ), 400
        # Extract parameters from the request data
        username = data.get("username")
        password = data.get("password")
        remember_me = data.get("remember_me")

        user = UserController.login(username, password)
        if user:
            login_user(user, remember=remember_me)
            return jsonify({"success": True, "message": "Logged in successfully."})
        else:
            return jsonify({"error": "Invalid username or password."}), 401
    else:
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        form = LoginForm()

        print(form.validate_on_submit())
        print(form.errors)
        if form.validate_on_submit():
            user = UserController.login(form.username.data, form.password.data)
            if user:
                login_user(user, remember=form.remember_me.data)
                return jsonify({"success": True, "message": "Logged in successfully."})
            else:
                return jsonify({"error": "Invalid username or password."}), 401
        return render_template("login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if UserController.get_user_by_username(form.username.data):
            return jsonify({"error": "Username already exists."}), 409
        try:
            UserController.create(form.username.data, form.password.data)
            return jsonify(
                {"success": True, "message": "Account created successfully."}
            )
        except Exception:
            return jsonify({"error": "Account creation failed."}), 500
    return render_template("signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        return jsonify({"success": True, "message": "Logout successful."})
    except Exception:
        return jsonify({"error": "Logout failed."}), 500
