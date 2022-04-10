from sqlalchemy.orm import class_mapper
import jwt
from flask import current_app


def serialize_object(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


def generate_token(user_id):
    return jwt.encode(
        {"user_id": user_id},
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
