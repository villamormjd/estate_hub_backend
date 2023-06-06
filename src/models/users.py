from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class UserProfile(BaseModel):
    cell_phone_num: str
    opaque_id: str


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "john doe",
                "password": "password"
            }
        }
