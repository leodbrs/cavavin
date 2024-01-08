from sqlalchemy import Column, Integer, String

from app import db


class Region(db.Model):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Region(id={self.id}, name={self.name})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
