import datetime

from src.config.db import conn
from src.schemas.users import userEntity, usersEntity
from src.models.users import User
from src.utils import check_if_email_does_exist, result_builder
from bson import ObjectId
from src.config.constant import Cons


class AccountManager:
    def __init__(self):
        self.conn = conn.estatehub
        self.db = self.conn['users']

    def retrieve_all_user(self):
        try:
            users = self.db.find()
            results = usersEntity(users)
            return result_builder(Cons.USERS_RETRIEVED, data=results)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def sign_up_user(self, user: User):
        try:
            if self.check_if_user_exist(user) == 0:
                user_obj = dict(user)
                user_obj['created_date'] = datetime.datetime.utcnow()
                user_obj['updated_at'] = datetime.datetime.utcnow()
                user_obj['activated_at'] = None
                user_obj['is_active'] = False

                u = self.db.insert_one(user_obj)
                result = usersEntity(self.db.find({"_id": u.inserted_id}))
                return result_builder(Cons.USER_SIGNUP_SUCCESS,
                                      data=result)
            else:
                return result_builder(Cons.USER_ALREADY_EXISTS, is_error=True)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def login_user(self, user: dict):
        query = self.db.find({"username": user["username"]})
        results = usersEntity(query)
        is_error = False

        try:
            message = Cons.USER_LOGIN_SUCCESS

            if len(results) == 0:
                message = Cons.USERNAME_NOT_FOUND
                is_error = True

            if results[0]['password'] != user["password"]:
                message = Cons.PASSWORD_INCORRECT
                is_error = True

            if not results[0]['is_active']:
                message = Cons.ACCOUNT_NOT_ACTIVE
                is_error = True

            return result_builder(message, data=results, is_error=is_error)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def activate_user_account(self, id: str):
        try:
            u = self.db.find_one_and_update({"_id": ObjectId(id)},
                                             {"$set": {"is_active": True,
                                                       "updated_at": datetime.datetime.utcnow(),
                                                       "activated_at": datetime.datetime.utcnow()},
                                              }
                                             )

            user = self.db.find_one({"_id": ObjectId(id)})
            results = userEntity(user)
            return result_builder(Cons.ACCOUNT_ACTIVATED, is_error=False, data=results)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def check_if_user_exist(self, user):
        return check_if_email_does_exist(user)
