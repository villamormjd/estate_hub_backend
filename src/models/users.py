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
                "username": "user1",
                "password": "password"
            }
        }


class UserResident(BaseModel):
    email: str
    is_homeowner: bool


class UserResetPassword(BaseModel):
    password: str
    confirm_password: str
