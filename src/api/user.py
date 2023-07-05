import datetime

from bson import ObjectId
from src.config.constant import Cons
from src.config.db import conn
from src.schemas.users import *
from src.models.users import *
from src.utils import *
from src.schemas.unit import *
from src.utils import check_if_email_does_exist, result_builder
from src.config.auth import Authenticator


class AccountManager:
    def __init__(self):
        self.conn = conn.estatehub
        self.db = self.conn['users']
        self.userprofile_db = self.conn['userprofile']
        self.unit_db = self.conn['unit']
        self.unit_attrs_db = self.conn['unit_attributes']
        self.user_unit_role_db = self.conn['user_unit_role']
        self.auth = Authenticator()

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
        print(query)
        results = userLoginEntities(query)
        is_error = False
        token = ""
        try:
            
            message = Cons.USER_LOGIN_SUCCESS

            if len(results) == 0:
                message = Cons.USERNAME_NOT_FOUND
                is_error = True
            elif results[0]['password'] != user["password"]:
                message = Cons.PASSWORD_INCORRECT
                is_error = True
            elif not results[0]['is_active']:
                message = Cons.ACCOUNT_NOT_ACTIVE
                is_error = True
            else:
                token = self.auth.sign_jwt(user["username"])

            return result_builder(message, data=token, is_error=is_error)

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
            uur = userUnitRoles(self.user_unit_role_db.find({"user_id": user["user_profile"]["user_id"]}))
            units = []
            for u in uur:
                ue = unitEntity(self.unit_db.find_one({"_id": ObjectId(u['unit_id'])}))
                ue['role'] = u['role_id']
                units.append(ue)

            user['property_unit'] = units
            return result_builder("Retrieved", data=user)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_user_by_email(self, email: str):
        try:
            user = self.db.find_one({"email": email})
            if not user:
                return result_builder(f"Email '{email}' doesn't exist", is_error=True)

            user = userEntity(user)
            up = self.userprofile_db.find_one({"user_id": user["id"]})
            user["user_profile"] = userProfileEntity(up)

            return result_builder("User retrieved", data=user)

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
            if results["is_active"]:
                return {"message": "Account already activated"}
            return result_builder(Cons.ACCOUNT_ACTIVATED, is_error=False, data=results)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def reset_user_password(self, id: str, user: UserResetPassword):

        if not equal_password(user.password, user.confirm_password):
            return result_builder("Passwords do not match", is_error=True)

    def check_if_user_exist(self, user):
        return check_if_email_does_exist(user)
