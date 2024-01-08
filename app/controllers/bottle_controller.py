from app import db
from app.controllers.shelf_controller import ShelfController
from app.controllers.wine_controller import WineController
from app.models.Bottle import Bottle


class BottleController(Bottle):
    @staticmethod
    def get_by_id(bottle_id):
        """
        Get a bottle by its ID.
        """
        return Bottle.query.get(bottle_id)

    @staticmethod
    def get_all():
        """
        Get all bottles.
        """
        return Bottle.query.all()

    @staticmethod
    def create(wine_id, shelf_id):
        """
        Create a new bottle and add it to the database.
        """
        if not isinstance(wine_id, int):
            raise TypeError("Wine ID must be an integer")
        if not WineController.get_by_id(wine_id):
            raise ValueError(f"Wine with ID {wine_id} does not exist")

        if not isinstance(shelf_id, int):
            raise TypeError("Shelf ID must be an integer")
        if not ShelfController.get_by_id(shelf_id):
            raise ValueError(f"Shelf with ID {shelf_id} does not exist")

        try:
            bottle = Bottle(wine_id=wine_id, shelf_id=shelf_id)
            ShelfController.add_bottle(shelf_id)
            db.session.add(bottle)
            db.session.commit()
            return bottle
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(bottle_id):
        """
        Delete a bottle from the database.
        """
        bottle = BottleController.get_by_id(bottle_id)
        if not bottle:
            raise ValueError(f"Bottle with ID {bottle_id} does not exist")
        try:
            ShelfController.remove_bottle(bottle.shelf_id)
            db.session.delete(bottle)
            db.session.commit()
            return bottle
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_wine_id(wine_id):
        """
        Get all bottles of a wine.
        """
        return Bottle.query.filter_by(wine_id=wine_id).all()
