import datetime

from src.config.constant import Cons
from src.config.db import conn
from src.schemas.users import *
from src.models.users import *
from src.utils import *
from src.utils import check_if_email_does_exist, result_builder
from bson import ObjectId


class AccountManager:
    def __init__(self):
        self.conn = conn.estatehub
        self.db = self.conn['users']
        self.userprofile_db = self.conn['userprofile']

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

    def create_user_profile(self, id: str, userProfile: UserProfile):
        try:
            users = usersEntity(self.db.find({"_id": ObjectId(id)}))
            if len(users) > 0:
                up = dict(userProfile)
                up["user_id"] = id
                up["opaque_id"] = generate_opaque_id()
                up["created_date"] = datetime.datetime.utcnow()
                up["updated_at"] = datetime.datetime.utcnow()
                u = self.userprofile_db.insert_one(up)
                result = userProfileEntity(self.userprofile_db.find_one({"_id": u.inserted_id}))

                users[0]["user_profile"] = result

                return result_builder("Created", data=users[0])

            return result_builder(Cons.USERNAME_NOT_FOUND, is_error=True)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_user_profile(self, id: str):

        try:
            user = userEntity(self.db.find_one({"_id": ObjectId(id)}))
            up = self.userprofile_db.find_one({"user_id": user["id"]})
            user["user_profile"] = userProfileEntity(up)

            return result_builder("Retrieved", data=user)

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
