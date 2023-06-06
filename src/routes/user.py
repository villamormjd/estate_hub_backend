from fastapi import APIRouter, Depends
from src.models.users import *
from src.api.user import AccountManager
from src.config.auth import jwtBearer

acc_mngr = AccountManager()
user = APIRouter()


@user.get('/user', dependencies=[Depends(jwtBearer())], tags=["Account"])
def find_all_users():
    return acc_mngr.retrieve_all_user()


@user.post('/user', tags=["Account"])
def signup_user(user: User):
    return acc_mngr.sign_up_user(user)


@user.post('/login', tags=["Account"])
def login_user(user: UserLogin):
    return acc_mngr.login_user({"username": user.username,
                                "password": user.password})


@user.post("/user/{id}/add-details", dependencies=[Depends(jwtBearer())], tags=["Account"])
def add_user_details(id: str, userProfile: UserProfile):
    return acc_mngr.create_user_profile(id, userProfile)


@user.get("/user/{id}/details", dependencies=[Depends(jwtBearer())], tags=["Account"])
def get_user_details(id: str):
    return acc_mngr.get_user_profile(id)


@user.put('/activate/{id}', tags=["Account"])
def activate_user(id: str):
    return acc_mngr.activate_user_account(id)
