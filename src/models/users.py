from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class UserProperty(BaseModel):
    cell_phone_num: str
    opaque_id: str
    role_id: int
