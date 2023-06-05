from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class UserProperty(User):
    cell_phone_num: str
    user: User


