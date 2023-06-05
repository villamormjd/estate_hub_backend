from fastapi import APIRouter
from src.models.users import User


from src.api.user import AccountManager

acc_mngr = AccountManager()
user = APIRouter()


@user.get('/user')
def find_all_users():
    return acc_mngr.retrieve_all_user()


@user.post('/user')
def sign_up(user: User):
    return acc_mngr.sign_up_user(user)


@user.post('/login')
def login(username: str, password: str):
    return acc_mngr.login_user({"username": username,
                                "password": password})


@user.put('/activate/{id}')
def activate_user(id: str):
    return acc_mngr.activate_user_account(id)


