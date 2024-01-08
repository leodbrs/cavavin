import validators

from app import db
from app.models.Rating import Rating
from app.models.Region import Region
from app.models.Wine import Wine, WineType


class WineController(Wine):
    @staticmethod
    def create(
        vineyard,
        name,
        wine_type,
        year,
        region_id,
        description,
        community_rating,
        label_photo,
        price,
        archived,
    ):
        """
        Create a new wine and add it to the database.
        """
        # add flask logger for all inputs
        if not isinstance(vineyard, str):
            raise TypeError("vineyard must be a string")

        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if not isinstance(year, int):
            raise TypeError("year must be an integer")
        if not (0 <= year <= 9999):
            raise ValueError("year must be a number between 0 and 9999")

        if not isinstance(description, str):
            raise TypeError("description must be a string")

        if not validators.url(label_photo):
            raise ValueError("label_photo photo must be a valid URL")

        if not price:
            raise ValueError("price must be a number")
        if not isinstance(price, float):
            try:
                price = float(price)
            except ValueError:
                raise TypeError("price must be a float")
        if not 0 <= price:
            raise ValueError("price must be a positive number")

        if archived:
            if not isinstance(archived, bool):
                raise TypeError("archived must be a boolean")

        if community_rating:
            if not isinstance(community_rating, float):
                try:
                    community_rating = float(community_rating)
                except ValueError:
                    raise TypeError("community rating must be a float")
            if not 0 <= community_rating <= 5:
                raise ValueError("community rating must be a number between 0 and 5")

        if not isinstance(wine_type, WineType):
            raise TypeError("wine_type must be a WineType")

        if not isinstance(region_id, int):
            raise TypeError("region_id must be an integer")
        wine_region = Region.query.get(region_id)
        if wine_region is None:
            raise ValueError("region_id Region does not exist.")

        new_wine = Wine(
            vineyard=vineyard,
            name=name,
            type=wine_type,
            year=year,
            region=wine_region,
            description=description,
            community_rating=community_rating,
            label_photo=label_photo,
            price=price,
            archived=archived,
        )
        db.session.add(new_wine)
        db.session.commit()

        return new_wine

    @staticmethod
    def get_all():
        """
        Retrieve all wines from the database.
        """
        return Wine.query.all()

    @staticmethod
    def get_by_id(wine_id):
        """
        Retrieve a wine from the database by its id.
        """
        return Wine.query.get(wine_id)

    @staticmethod
    def delete_by_id(wine_id):
        """
        Delete a wine from the database by its id.
        """
        try:
            wine = Wine.query.get(wine_id)
            if wine is None:
                raise ValueError(f"Wine with id {wine_id} does not exist")
            db.session.delete(wine)
            db.session.commit()
        except ValueError as e:
            raise e

    @staticmethod
    def get_by_region_id(region_id):
        """
        Retrieve all wines from the database by their region id.
        """
        return Wine.query.filter_by(region_id=region_id).all()

    @staticmethod
    def get_all_with_existing_bottle():
        """
        Retrieve all wines from the database that have at least one bottle.
        """
        return Wine.query.filter(Wine.bottles.any()).all()

    @staticmethod
    def update_community_rating_by_id(wine_id):
        """
        Update the community rating of a wine.
        """
        wine = WineController.get_by_id(wine_id)
        if wine is None:
            raise ValueError(f"Wine with id {wine_id} does not exist")
        print(wine.id)
        ratings = Rating.query.filter_by(wine_id=wine.id).all()
        for rating in ratings:
            print(rating.value)
        print(len(ratings))

        if len(ratings) == 0:
            wine.community_rating = None
        else:
            wine.community_rating = sum([rating.value for rating in ratings]) / len(
                ratings
            )

        db.session.commit()
        return wine
