from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint

from app import db


class Rating(db.Model):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True)
    wine_id = Column(Integer, ForeignKey("wine.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    value = Column(Integer, nullable=False)
    text = Column(Text)
    wine = db.relationship("Wine", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    __table_args__ = (UniqueConstraint("wine_id", "user_id"),)

    def __repr__(self):
        return f"Rating(id={self.id}, wine_id={self.wine_id}, user_id={self.user_id}, value={self.value}, text={self.text})"

    def to_dict(self):
        return {
            "id": self.id,
            "wine_id": self.wine_id,
            "user_id": self.user_id,
            "value": self.value,
            "text": self.text,
        }
