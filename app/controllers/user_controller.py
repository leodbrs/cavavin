import re

import bcrypt

from app import db
from app.models.User import User


class UserController(User):
    @staticmethod
    def get_all():
        """
        Get all users from the database.
        """
        return User.query.all()

    @staticmethod
    def get_user_by_username(username):
        """
        Get a user by its username.
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get a user by its ID.
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def create(username, password):
        """
        Create a new user and add it to the database.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        # Check if username matches the regex pattern
        if not re.match("^[a-zA-Z0-9_-]+$", username):
            raise ValueError(
                "Invalid username. Only uppercase letters, lowercase letters, dash, and underscore are allowed."
            )
        if UserController.get_user_by_username(username):
            raise ValueError(f"Username {username} already exists")

        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()

    @staticmethod
    def delete_by_id(user_id):
        """
        Delete a user by its ID.
        """
        user = User.query.get(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} does not exist")
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def check_password_complexity(password):
        """
        Test the complexity of a password with regex.
        """

        # Check if password matches the regex pattern
        if not re.match(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{8,}$", password
        ):
            raise ValueError(
                "Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            )

    @staticmethod
    def update_password_by_id(user_id, password):
        """
        Update a user's password by its ID.
        """
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        UserController.check_password_complexity(password)

        user = User.query.get(User.id == user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} does not exist")
        user.password = password
        db.session.commit()
        return user.to_dict()

    @staticmethod
    def login(username, password):
        """
        Login a user.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        try:
            user = UserController.get_user_by_username(username)
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return user
        except AttributeError:
            return None
