from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app.controllers.bottle_controller import BottleController
from app.controllers.cellar_controller import CellarController
from app.controllers.region_controller import RegionController
from app.controllers.shelf_controller import ShelfController
from app.controllers.wine_controller import WineController
from app.forms import (
    CreateCellarForm,
    CreateShelfForm,
    DeleteCellarForm,
    RenameCellarForm,
)
from app.models.Wine import WineType

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    wines = WineController.get_all()
    bottles = BottleController.get_all()
    return render_template("index.html", wines=wines, bottles=bottles)


@main.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html", name=current_user.username)


@main.route("/wine/<int:wine_id>", methods=["GET"])
def wine(wine_id):
    wine = WineController.get_by_id(wine_id)
    bottles = BottleController.get_by_wine_id(wine_id)
    number_of_bottle = len(bottles)
    if number_of_bottle > 0:
        first_available_bottle = bottles[0]
    else:
        first_available_bottle = None
    print(first_available_bottle)
    return render_template(
        "wine.html",
        wine=wine,
        number_of_bottle=number_of_bottle,
        first_available_bottle=first_available_bottle,
    )


@main.route("/cellar", methods=["GET", "POST"])
@login_required
def cellar():
    create_cellar_form = CreateCellarForm()
    rename_cellar_form = RenameCellarForm()
    create_shelf_form = CreateShelfForm()
    delete_cellar_form = DeleteCellarForm()

    if create_cellar_form.validate_on_submit():
        if CellarController.get_by_user_id(current_user.id):
            return jsonify({"error": "You already have a cellar."}), 409
        if CellarController.get_by_name(create_cellar_form.name.data):
            return jsonify({"error": "Cellar name already exists."}), 409
        CellarController.create(create_cellar_form.name.data, current_user.id)
        return jsonify(
            {"success": True, "message": "Cellar created successfully."}
        ), 201
    if rename_cellar_form.validate_on_submit():
        cellar = CellarController.get_by_user_id(current_user.id)
        if CellarController.get_by_name(rename_cellar_form.new_name.data):
            return jsonify({"error": "Cellar name already exists."}), 409
        CellarController.rename(cellar.id, rename_cellar_form.new_name.data)
        return jsonify(
            {"success": True, "message": "Cellar renamed successfully."}
        ), 200

    if create_shelf_form.validate_on_submit():
        cellar = CellarController.get_by_user_id(current_user.id)
        if ShelfController.get_by_number(cellar.id, int(create_shelf_form.number.data)):
            return jsonify({"error": "Shelf number already exists."}), 409
        try:
            shelf = ShelfController.create(
                number=create_shelf_form.number.data,
                region_id=int(create_shelf_form.region.data),
                available_spaces=create_shelf_form.bottles_per_shelf.data,
                bottles_per_shelf=create_shelf_form.bottles_per_shelf.data,
                cellar_id=cellar.id,
            )
            if not shelf:
                return jsonify({"error": "Could not create shelf."}), 500
            return jsonify(
                {"success": True, "message": "Shelf created successfully."}
            ), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    if delete_cellar_form.validate_on_submit():
        cellar = CellarController.get_by_user_id(current_user.id)
        if not cellar:
            return jsonify({"error": "Cellar does not exist."}), 404
        if not CellarController.delete_by_id(cellar.id):
            return jsonify({"error": "Could not delete cellar."}), 500
        return jsonify(
            {"success": True, "message": "Cellar deleted successfully."}
        ), 200
    cellar = CellarController.get_by_user_id(current_user.id)
    if not cellar:
        return render_template(
            "create_cellar.html",
            create_cellar_form=create_cellar_form,
        )
    shelfs = ShelfController.get_by_cellar_id(cellar.id)
    return render_template(
        "cellar.html",
        cellar=cellar,
        shelfs=shelfs,
        rename_cellar_form=rename_cellar_form,
        create_shelf_form=create_shelf_form,
        delete_cellar_form=delete_cellar_form,
    )


@main.route("/shelf/<int:shelf_id>", methods=["GET"])
@login_required
def shelf(shelf_id):
    shelf = ShelfController.get_by_id(shelf_id)
    return render_template("manage_shelf.html", shelf=shelf)


@main.route("/bottle", methods=["GET"])
@login_required
def bottle():
    shelf_id = request.args.get("shelf_id")
    shelf = ShelfController.get_by_id(shelf_id)
    regions = RegionController.get_all()
    wines = WineController.get_by_region_id(shelf.region_id)
    types = [type for type in WineType]
    return render_template(
        "add_bottle.html", shelf=shelf, wines=wines, regions=regions, types=types
    )
