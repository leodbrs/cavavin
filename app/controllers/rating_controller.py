from app import db
from app.controllers.user_controller import UserController
from app.controllers.wine_controller import WineController
from app.models.Rating import Rating


class RatingController(Rating):
    @staticmethod
    def get_all():
        """
        Get all rating from the database.
        """
        return Rating.query.all()

    @staticmethod
    def get_by_id(rating_id):
        """
        Get a rating by its ID.
        """
        return Rating.query.get(rating_id)

    @staticmethod
    def get_by_user_id(user_id):
        """
        Get a rating by its user ID.
        """
        return Rating.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_wine_id(wine_id):
        """
        Get a rating by its wine ID.
        """
        return Rating.query.filter_by(wine_id=wine_id).all()

    @staticmethod
    def create(user_id, wine_id, value, text):
        """
        Creates a new rating and add it to the database.
        """
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")
        if not UserController.get_user_by_id(user_id):
            raise ValueError(f"User with ID {user_id} does not exist")

        if not isinstance(wine_id, int):
            raise TypeError("Wine ID must be an integer")
        if not WineController.get_by_id(wine_id):
            raise ValueError(f"Wine with ID {wine_id} does not exist")

        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if value < 0 or value > 5:
            raise ValueError("Rating must be between 0 and 5")

        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        if len(text) > 255:
            raise ValueError("Text must be less than 255 characters")

        if Rating.query.filter_by(user_id=user_id, wine_id=wine_id).first():
            raise ValueError(
                f"Rating for wine with ID {wine_id} by user with ID {user_id} already exists"
            )
        try:
            rating = Rating(user_id=user_id, wine_id=wine_id, value=value, text=text)
            db.session.add(rating)
            db.session.commit()
            return rating
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_by_id(rating_id):
        """
        Delete a rating by its ID.
        """
        rating = RatingController.get_by_id(rating_id)
        if not rating:
            raise ValueError(f"Rating with ID {rating_id} does not exist")
        db.session.delete(rating)
        db.session.commit()
