from sqlalchemy import Column, ForeignKey, Integer

from app import db


class Shelf(db.Model):
    __tablename__ = "shelf"
    id = Column(Integer, primary_key=True)
    cellar_id = Column(Integer, ForeignKey("cellar.id"))
    number = Column(Integer)
    region_id = Column(Integer, ForeignKey("region.id"))
    available_spaces = Column(Integer)
    bottles_per_shelf = Column(Integer)
    region = db.relationship("Region")
    cellar = db.relationship("Cellar", back_populates="shelves")
    bottles = db.relationship(
        "Bottle", back_populates="shelf", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Shelf(id={self.id}, cellar_id={self.cellar_id}, number={self.number}, region={self.region}, available_spaces={self.available_spaces}, bottles_per_shelf={self.bottles_per_shelf})"

    def to_dict(self):
        return {
            "id": self.id,
            "cellar_id": self.cellar_id,
            "number": self.number,
            "region": self.region.to_dict(),
            "available_spaces": self.available_spaces,
            "bottles_per_shelf": self.bottles_per_shelf,
            "cellar": self.cellar.to_dict(),
        }
