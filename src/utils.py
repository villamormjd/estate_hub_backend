import re

from src.config.db import conn
from src.schemas.users import userEntity, usersEntity

db = db = conn.estatehub


def check_if_email_does_exist(user):
    u = db.users.find(
            {"$or": [
                {"email": user.email},
                {"username": user.username}
                ]
            }
        )

    return len(usersEntity(u))


def result_builder(message: str, data=None, is_error: bool = False):
    results = dict()
    results["error"] = is_error
    results["message"] = message

    if data:
        results["data"] = data

    return results
