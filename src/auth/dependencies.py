from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request, status,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from typing import Optional
from .utils import decode_token
from src.db.redis import token_in_blocklist


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)

        token = creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invaild or has been revoked",
                    "resoluntion": "Please get new token",
                },
            )
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invaild or has been revoked",
                    "resoluntion": "Please get new token",
                },
            )
        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return True if token_data is not None else False

    def verify_token_data(self, token_data):
        raise NotImplementedError(
            "Please Override the verify_token_data method in the subclass."
        )


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token cannot be used as access token.",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token.",
            )
# def get_currrent_user(token_details: dict = Depends(AccessTokenBearer())):
#     user_email= token_details['user']['email']