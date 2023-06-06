# This file is responsible for signing, encoding, decoding and returning auth tokens

import time
import jwt
from decouple import config

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Authenticator:
    def __init__(self):
        self.SECRET = config("JWT_SECRET_KEY")
        self.ALGORITHM = config("JWT_ALGORITHM")

    def token_response(self, token: str):
        return {
            "access_token": token
        }

    def sign_jwt(self, userID: str):
        payload = {
            "userId": userID,
            "expiry": time.time() + 600
        }

        token = jwt.encode(payload, self.SECRET, algorithm=self.ALGORITHM)
        return self.token_response(token)

    def decode_jwt(self, token: str):
        try:
            decode_token = jwt.decode(token, self.SECRET, algorithms=self.ALGORITHM)
            return decode_token if decode_token['expires'] >= time.time() else None

        except Exception as e:
            return str(e)


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:

            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid Token")

            return credentials.credentials

        else:
            raise HTTPException(status_code=403, detail="Invalid Token")

    def verify_token(self, jwt_token: str):

        isTokenValid: bool = False
        payload = Authenticator().decode_jwt(jwt_token)
        if payload:
            isTokenValid = True

        return isTokenValid
