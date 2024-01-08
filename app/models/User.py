from datetime import datetime

import bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, String

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    _password = Column("password", String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    cellars = db.relationship(
        "Cellar", back_populates="user", cascade="all, delete-orphan"
    )
    ratings = db.relationship(
        "Rating", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(
            plaintext_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password}, created_at={self.created_at})"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
        }
