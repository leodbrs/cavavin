from sqlalchemy import Column, ForeignKey, Integer, String

from app import db


class Cellar(db.Model):
    __tablename__ = "cellar"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = db.relationship("User", back_populates="cellars")
    shelves = db.relationship(
        "Shelf", back_populates="cellar", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cellar(id={self.id}, name={self.name}, user_id={self.user_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user": self.user.to_dict(),
        }
