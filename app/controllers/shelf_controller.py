from app import db
from app.controllers.cellar_controller import CellarController
from app.controllers.region_controller import RegionController
from app.models.Shelf import Shelf


class ShelfController(Shelf):
    @staticmethod
    def create(number, region_id, available_spaces, bottles_per_shelf, cellar_id):
        """
        Create a new shelf and add it to the database.
        """
        if not isinstance(number, int):
            raise TypeError("Number must be an integer")
        if not (1 <= number <= 100):
            raise ValueError("Number must be between 1 and 100")

        if not isinstance(region_id, int):
            raise TypeError("Region ID must be an integer")
        region = RegionController.get_by_id(region_id)
        if not region:
            raise ValueError(f"Region with ID {region_id} does not exist")

        if not isinstance(available_spaces, int):
            raise TypeError("Available spaces must be an integer")
        if not (0 <= available_spaces <= bottles_per_shelf):
            raise ValueError("Available spaces must be between 0 and bottles per shelf")

        if not isinstance(bottles_per_shelf, int):
            raise TypeError("Bottles per shelf must be an integer")
        if not (1 <= bottles_per_shelf):
            raise ValueError("Bottles per shelf must be greater than 0")
        if not (1 <= bottles_per_shelf <= 10000):
            raise ValueError("Number of bottles must be between 1 and 10000")

        if not isinstance(cellar_id, int):
            raise TypeError("Cellar ID must be an integer")
        if not CellarController.get_by_id(cellar_id):
            raise ValueError(f"Cellar with ID {cellar_id} does not exist")

        shelf = Shelf(
            number=number,
            region=region,
            available_spaces=available_spaces,
            bottles_per_shelf=bottles_per_shelf,
            cellar_id=cellar_id,
        )
        db.session.add(shelf)
        db.session.commit()
        return shelf

    @staticmethod
    def get_by_id(shelf_id):
        """
        Get a shelf by its ID.
        """
        return Shelf.query.get(shelf_id)

    @staticmethod
    def get_all():
        """
        Get all shelves.
        """
        return Shelf.query.all()

    @staticmethod
    def remove_bottle(shelf_id):
        """
        Remove a bottle from a shelf.
        """
        shelf = ShelfController.get_by_id(shelf_id)
        if not shelf:
            raise ValueError(f"Shelf with ID {shelf_id} does not exist")

        if shelf.available_spaces == shelf.bottles_per_shelf:
            raise ValueError(f"Shelf with ID {shelf_id} is already empty")

        shelf.available_spaces += 1
        db.session.commit()
        return shelf

    @staticmethod
    def add_bottle(shelf_id):
        """
        Add a bottle to a shelf.
        """
        shelf = ShelfController.get_by_id(shelf_id)
        if not shelf:
            raise ValueError(f"Shelf with ID {shelf_id} does not exist")

        if shelf.available_spaces == 0:
            raise ValueError(f"Shelf with ID {shelf_id} is already full")

        shelf.available_spaces -= 1
        db.session.commit()
        return shelf

    @staticmethod
    def get_by_cellar_id(cellar_id):
        """
        Get all shelves in a cellar.
        """
        return Shelf.query.filter_by(cellar_id=cellar_id).all()

    @staticmethod
    def get_by_number(cellar_id, number):
        """
        Get a shelf by its number.
        """
        return Shelf.query.filter_by(cellar_id=cellar_id, number=number).first()
