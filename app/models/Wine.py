from enum import Enum as PythonEnum

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String

from app import db


class WineType(PythonEnum):
    RED = "rouge"
    WHITE = "blanc"
    ROSE = "rosé"
    SPARKLING = "pétillant"


class Wine(db.Model):
    __tablename__ = "wine"

    id = Column(Integer, primary_key=True)
    vineyard = Column(String(255))
    name = Column(String(255), nullable=False)
    type = Column(Enum(WineType), nullable=False)
    year = Column(Integer, nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    description = Column(String(1023))
    community_rating = Column(Float(2))
    label_photo = Column(String(1023), nullable=False)
    price = Column(Float(2), nullable=False)
    archived = Column(Boolean, default=False)
    region = db.relationship("Region")
    ratings = db.relationship(
        "Rating", back_populates="wine", cascade="all, delete-orphan"
    )
    bottles = db.relationship(
        "Bottle", back_populates="wine", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        vineyard,
        name,
        type,
        year,
        region,
        description,
        community_rating,
        label_photo,
        price,
        archived,
    ):
        self.vineyard = vineyard
        self.name = name
        self.type = type
        self.year = year
        self.region = region
        self.description = description
        self.community_rating = community_rating
        self.label_photo = label_photo
        self.price = price
        self.archived = archived

    def __repr__(self):
        return (
            f"Wine(id={self.id}, vineyard='{self.vineyard}', name='{self.name}', "
            f"type={self.type}, year='{self.year}', region={self.region}, "
            f"community_rating={self.community_rating}, price={self.price}, archived={self.archived})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "vineyard": self.vineyard,
            "name": self.name,
            "type": {
                "name": self.type.name,
                "value": self.type.value,
            },
            "year": self.year,
            "region": self.region.to_dict(),
            "description": self.description,
            "community_rating": self.community_rating,
            "label_photo": self.label_photo,
            "price": self.price,
            "archived": self.archived,
        }
