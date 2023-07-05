from src.config.db import conn
from src.schemas.users import userEntity, usersEntity
import random, string

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


def generate_opaque_id():
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"p-{x[:7]}"


def equal_password(password: str, confirm_password: str):
    if password == confirm_password:
        return True

    return False