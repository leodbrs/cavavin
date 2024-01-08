from app import db
from app.controllers.user_controller import UserController
from app.models.Cellar import Cellar


class CellarController(Cellar):
    @staticmethod
    def create(name, user_id):
        """
        Create a new cellar and add it to the database.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")
        if not UserController.get_user_by_id(user_id):
            raise ValueError(f"User with ID {user_id} does not exist")
        if CellarController.get_by_user_id(user_id):
            raise ValueError(f"Cellar with user ID {user_id} already exists")
        cellar = Cellar(name=name, user_id=user_id)
        db.session.add(cellar)
        db.session.commit()
        return cellar

    @staticmethod
    def get_all():
        """
        Get all cellars from the database.
        """
        return Cellar.query.all()

    @staticmethod
    def get_by_id(cellar_id):
        """
        Get a cellar by its ID.
        """
        if not isinstance(cellar_id, int):
            raise TypeError("Cellar ID must be an integer")
        return Cellar.query.filter_by(id=cellar_id).first()

    @staticmethod
    def get_by_user_id(user_id):
        """
        Get a cellar by its user ID.
        """
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")
        return Cellar.query.filter(Cellar.user_id == user_id).first()

    @staticmethod
    def rename(cellar_id, name):
        """
        Rename a cellar.
        """
        if not isinstance(cellar_id, int):
            raise TypeError("Cellar ID must be an integer")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        cellar = CellarController.get_by_id(cellar_id)
        if CellarController.get_by_name(name):
            raise ValueError(f"Cellar with name {name} already exists")
        cellar.name = name
        db.session.commit()
        return cellar

    @staticmethod
    def delete_by_id(cellar_id):
        """
        Delete a cellar.
        """
        if not isinstance(cellar_id, int):
            raise TypeError("Cellar ID must be an integer")
        cellar = CellarController.get_by_id(cellar_id)
        if not cellar:
            raise ValueError(f"Cellar with ID {cellar_id} does not exist")

        db.session.delete(cellar)
        db.session.commit()
        return True

    @staticmethod
    def get_by_name(name):
        """
        Get a cellar by its name.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        return Cellar.query.filter_by(name=name).first()
