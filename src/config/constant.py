from enum import Enum


class Cons:
    USERS_RETRIEVED = "User retrieved successfully"
    USER_SIGNUP_SUCCESS = "User signed up successfully"
    USER_SIGNUP_FAIL = "Failed to sign up"
    USER_LOGIN_SUCCESS = "User logged in successfully"
    USER_LOGIN_FAIL = "Failed to login"
    USER_ALREADY_EXISTS = "Email or Username already exists."
    USERNAME_NOT_FOUND = "Username not found."
    PASSWORD_INCORRECT = "Password is incorrect"
    ACCOUNT_NOT_ACTIVE = "Account is not yet activated."
    ACCOUNT_ACTIVATED = "Account activated successfully"


class Role(Enum):
    HOMEOWNER = 1
    TENANT = 2
    RELATIVE = 3
    VISITOR = 4
    STAFF = 5
    ADMIN = 6
