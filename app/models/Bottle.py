from sqlalchemy import Column, ForeignKey, Integer

from app import db


class Bottle(db.Model):
    __tablename__ = "bottle"
    id = Column(Integer, primary_key=True)
    wine_id = Column(Integer, ForeignKey("wine.id"))
    shelf_id = Column(Integer, ForeignKey("shelf.id"))
    wine = db.relationship("Wine", back_populates="bottles")
    shelf = db.relationship("Shelf", back_populates="bottles")

    def __repr__(self):
        return f"Bottle(id={self.id}, wine_id={self.wine_id}, shelf_id={self.shelf_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "wine": self.wine.to_dict(),
            "shelf": self.shelf.to_dict(),
        }
