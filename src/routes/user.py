from fastapi import APIRouter
from src.models.users import *
from src.api.user import AccountManager


acc_mngr = AccountManager()
user = APIRouter()


@user.get('/user', tags=["Account"])
def find_all_users():
    return acc_mngr.retrieve_all_user()


@user.post('/user', tags=["Account"])
def signup_user(user: User):
    return acc_mngr.sign_up_user(user)


@user.post('/login', tags=["Account"])
def login_user(username: str, password: str):
    return acc_mngr.login_user({"username": username,
                                "password": password})


@user.post("/user/{id}/add-details", tags=["Account"])
def add_user_details(id: str, userProfile: UserProfile):
    return acc_mngr.create_user_profile(id, userProfile)


@user.get("/user/{id}/details", tags=["Account"])
def get_user_details(id: str):
    return acc_mngr.get_user_profile(id)


@user.put('/activate/{id}', tags=["Account"])
def activate_user(id: str):
    return acc_mngr.activate_user_account(id)


